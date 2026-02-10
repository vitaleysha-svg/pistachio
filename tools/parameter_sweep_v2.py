#!/usr/bin/env python3
"""ComfyUI parameter sweep v2 with face similarity scoring and montage output.

This script expects a ComfyUI API-format workflow JSON ("Save (API format)").
"""

from __future__ import annotations

import argparse
import copy
import csv
import io
import itertools
import json
import math
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REQUIRED_PACKAGES = {
    "requests": "2.31.0",
    "numpy": "1.26.4",
    "Pillow": "10.2.0",
    "insightface": "0.7.3",
    "opencv-python-headless": "4.9.0.80",
}


@dataclass
class SweepCase:
    mode: str
    checkpoint: str
    lora_strength: float
    cfg: float
    sampler: str
    seed: int


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_dependencies(skip_install: bool) -> None:
    missing = []
    for package, version in REQUIRED_PACKAGES.items():
        import_name = "PIL" if package == "Pillow" else package.split("-")[0]
        if package == "opencv-python-headless":
            import_name = "cv2"
        try:
            __import__(import_name)
        except Exception:  # noqa: BLE001
            missing.append(f"{package}=={version}")

    if not missing:
        return
    if skip_install:
        raise RuntimeError("Missing dependencies: " + ", ".join(missing))
    run([sys.executable, "-m", "pip", "install", "--no-input", *missing])


def parse_csv_values(raw: str, cast_type: Any) -> list[Any]:
    values = [x.strip() for x in raw.split(",") if x.strip()]
    return [cast_type(v) for v in values]


def to_node_id(node_id: str | int) -> str:
    return str(node_id)


def set_input(workflow: dict[str, Any], node_id: str | int, key: str, value: Any) -> None:
    nid = to_node_id(node_id)
    if nid not in workflow:
        raise KeyError(f"Node id not found in workflow: {nid}")
    node = workflow[nid]
    if "inputs" not in node:
        raise KeyError(f"Node {nid} does not contain 'inputs'. Use API-format workflow JSON.")
    node["inputs"][key] = value


def post_prompt(requests_mod, comfy_url: str, prompt: dict[str, Any], client_id: str) -> str:
    url = comfy_url.rstrip("/") + "/prompt"
    response = requests_mod.post(url, json={"prompt": prompt, "client_id": client_id}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    if "prompt_id" not in payload:
        raise RuntimeError(f"Unexpected /prompt response: {payload}")
    return payload["prompt_id"]


def wait_for_history(requests_mod, comfy_url: str, prompt_id: str, timeout_sec: int, poll_interval: float) -> dict[str, Any]:
    deadline = time.time() + timeout_sec
    history_url = comfy_url.rstrip("/") + f"/history/{prompt_id}"

    while time.time() < deadline:
        response = requests_mod.get(history_url, timeout=60)
        response.raise_for_status()
        payload = response.json()
        if prompt_id in payload:
            return payload[prompt_id]
        time.sleep(poll_interval)

    raise TimeoutError(f"Timed out waiting for ComfyUI history: prompt_id={prompt_id}")


def extract_first_image_ref(history_item: dict[str, Any]) -> dict[str, str]:
    outputs = history_item.get("outputs", {})
    for _, output in outputs.items():
        images = output.get("images") or []
        if images:
            return images[0]
    raise RuntimeError("No images found in ComfyUI history output.")


def download_image_bytes(requests_mod, comfy_url: str, image_ref: dict[str, str]) -> bytes:
    view_url = comfy_url.rstrip("/") + "/view"
    params = {
        "filename": image_ref.get("filename", ""),
        "subfolder": image_ref.get("subfolder", ""),
        "type": image_ref.get("type", "output"),
    }
    response = requests_mod.get(view_url, params=params, timeout=120)
    response.raise_for_status()
    return response.content


class FaceScorer:
    def __init__(self, reference_image: Path):
        import cv2
        import numpy as np
        from insightface.app import FaceAnalysis

        self.cv2 = cv2
        self.np = np
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        self.app = FaceAnalysis(name="buffalo_l", providers=providers)
        self.app.prepare(ctx_id=0, det_size=(640, 640))

        ref = cv2.imread(str(reference_image))
        if ref is None:
            raise RuntimeError(f"Could not read reference image: {reference_image}")
        ref_faces = self.app.get(ref)
        if not ref_faces:
            raise RuntimeError("No face detected in reference image for similarity scoring.")
        self.ref_embedding = ref_faces[0].embedding.astype(np.float32)

    def score_bytes(self, image_bytes: bytes) -> float:
        buf = self.np.frombuffer(image_bytes, dtype=self.np.uint8)
        image = self.cv2.imdecode(buf, self.cv2.IMREAD_COLOR)
        if image is None:
            return 0.0

        faces = self.app.get(image)
        if not faces:
            return 0.0
        emb = faces[0].embedding.astype(self.np.float32)

        denom = float(self.np.linalg.norm(self.ref_embedding) * self.np.linalg.norm(emb))
        if denom == 0:
            return 0.0
        return float(self.np.dot(self.ref_embedding, emb) / denom)


def create_montage(rows: list[dict[str, Any]], output_path: Path, thumb_size: int = 512, columns: int = 4) -> None:
    from PIL import Image, ImageDraw

    if not rows:
        return

    text_h = 92
    count = len(rows)
    columns = max(1, columns)
    rows_count = math.ceil(count / columns)
    canvas = Image.new("RGB", (columns * thumb_size, rows_count * (thumb_size + text_h)), color=(20, 20, 20))
    draw = ImageDraw.Draw(canvas)

    for idx, row in enumerate(rows):
        x = (idx % columns) * thumb_size
        y = (idx // columns) * (thumb_size + text_h)

        image = Image.open(row["local_path"]).convert("RGB").resize((thumb_size, thumb_size))
        canvas.paste(image, (x, y))

        label = (
            f"{row['mode']}\n"
            f"ckpt={row['checkpoint']}\n"
            f"lora={row['lora_strength']:.2f} cfg={row['cfg']:.1f} {row['sampler']}\n"
            f"sim={row['face_similarity']:.4f} seed={row['seed']}"
        )
        draw.text((x + 8, y + thumb_size + 6), label, fill=(230, 230, 230))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


def build_cases(args: argparse.Namespace) -> list[SweepCase]:
    checkpoints = parse_csv_values(args.checkpoints, str)
    lora_strengths = parse_csv_values(args.lora_strengths, float)
    cfg_values = parse_csv_values(args.cfg_values, float)
    samplers = parse_csv_values(args.samplers, str)
    modes = ["lora_only", "lora_plus_instantid"]

    cases = []
    seed = args.base_seed
    for mode, ckpt, lora, cfg, sampler in itertools.product(modes, checkpoints, lora_strengths, cfg_values, samplers):
        cases.append(
            SweepCase(
                mode=mode,
                checkpoint=ckpt,
                lora_strength=lora,
                cfg=cfg,
                sampler=sampler,
                seed=seed,
            )
        )
        seed += 1

    if args.max_cases > 0:
        cases = cases[: args.max_cases]
    return cases


def patch_workflow(base_prompt: dict[str, Any], args: argparse.Namespace, case: SweepCase) -> dict[str, Any]:
    prompt = copy.deepcopy(base_prompt)

    set_input(prompt, args.positive_node_id, args.positive_key, args.prompt)
    set_input(prompt, args.negative_node_id, args.negative_key, args.negative_prompt)
    set_input(prompt, args.checkpoint_node_id, args.checkpoint_key, case.checkpoint)
    set_input(prompt, args.ksampler_node_id, args.cfg_key, case.cfg)
    set_input(prompt, args.ksampler_node_id, args.sampler_key, case.sampler)
    set_input(prompt, args.ksampler_node_id, args.seed_key, case.seed)
    set_input(prompt, args.ksampler_node_id, args.steps_key, args.steps)

    if args.lora_node_id:
        set_input(prompt, args.lora_node_id, args.lora_model_strength_key, case.lora_strength)
        if args.lora_clip_strength_key:
            set_input(prompt, args.lora_node_id, args.lora_clip_strength_key, case.lora_strength)

    if args.instantid_weight_node_id:
        weight = args.instantid_weight_enabled if case.mode == "lora_plus_instantid" else args.instantid_weight_disabled
        set_input(prompt, args.instantid_weight_node_id, args.instantid_weight_key, weight)

    return prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Comprehensive parameter sweep with face similarity scoring.")
    parser.add_argument("--workflow", type=Path, required=True, help="ComfyUI API-format workflow JSON.")
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--reference-image", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/sweep_results_v2"))

    parser.add_argument("--checkpoints", default="realvisxl_v5.safetensors,juggernautxl_v9.safetensors,epicrealismxl.safetensors")
    parser.add_argument("--lora-strengths", default="0.70,0.80,0.90")
    parser.add_argument("--cfg-values", default="3.5,4.0,4.5")
    parser.add_argument("--samplers", default="dpmpp_2m,euler_a,dpmpp_sde")
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--base-seed", type=int, default=42424242)
    parser.add_argument("--max-cases", type=int, default=0, help="Set >0 to cap total sweep cases.")

    parser.add_argument("--positive-node-id", default="6")
    parser.add_argument("--positive-key", default="text")
    parser.add_argument("--negative-node-id", default="7")
    parser.add_argument("--negative-key", default="text")
    parser.add_argument("--checkpoint-node-id", default="4")
    parser.add_argument("--checkpoint-key", default="ckpt_name")
    parser.add_argument("--ksampler-node-id", default="3")
    parser.add_argument("--cfg-key", default="cfg")
    parser.add_argument("--sampler-key", default="sampler_name")
    parser.add_argument("--seed-key", default="seed")
    parser.add_argument("--steps-key", default="steps")

    parser.add_argument("--lora-node-id", default="")
    parser.add_argument("--lora-model-strength-key", default="strength_model")
    parser.add_argument("--lora-clip-strength-key", default="strength_clip")

    parser.add_argument("--instantid-weight-node-id", default="")
    parser.add_argument("--instantid-weight-key", default="weight")
    parser.add_argument("--instantid-weight-enabled", type=float, default=0.35)
    parser.add_argument("--instantid-weight-disabled", type=float, default=0.0)

    parser.add_argument("--poll-interval", type=float, default=1.5)
    parser.add_argument("--timeout-sec", type=int, default=600)
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    import requests

    if not args.workflow.exists():
        raise FileNotFoundError(f"Workflow file not found: {args.workflow}")
    if not args.reference_image.exists():
        raise FileNotFoundError(f"Reference image not found: {args.reference_image}")

    base_prompt = json.loads(args.workflow.read_text(encoding="utf-8"))
    if "nodes" in base_prompt:
        raise RuntimeError(
            "Detected UI workflow JSON. Export API-format workflow JSON from ComfyUI and rerun."
        )

    scorer = FaceScorer(args.reference_image)
    client_id = str(uuid.uuid4())
    cases = build_cases(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []

    print(f"[init] total_cases={len(cases)} output_dir={args.output_dir}")
    for index, case in enumerate(cases, start=1):
        prompt = patch_workflow(base_prompt, args, case)
        prompt_id = post_prompt(requests, args.comfy_url, prompt, client_id)
        history_item = wait_for_history(
            requests,
            args.comfy_url,
            prompt_id,
            timeout_sec=args.timeout_sec,
            poll_interval=args.poll_interval,
        )
        image_ref = extract_first_image_ref(history_item)
        image_bytes = download_image_bytes(requests, args.comfy_url, image_ref)

        filename = (
            f"{index:03d}_{case.mode}_{Path(case.checkpoint).stem}_"
            f"l{case.lora_strength:.2f}_cfg{case.cfg:.1f}_{case.sampler}_seed{case.seed}.png"
        )
        output_path = args.output_dir / filename
        output_path.write_bytes(image_bytes)

        similarity = scorer.score_bytes(image_bytes)
        row = {
            "index": index,
            "mode": case.mode,
            "checkpoint": case.checkpoint,
            "lora_strength": case.lora_strength,
            "cfg": case.cfg,
            "sampler": case.sampler,
            "seed": case.seed,
            "face_similarity": similarity,
            "local_path": str(output_path),
        }
        rows.append(row)
        print(
            f"[case {index}/{len(cases)}] mode={case.mode} ckpt={case.checkpoint} "
            f"lora={case.lora_strength:.2f} cfg={case.cfg:.1f} {case.sampler} sim={similarity:.4f}"
        )

    csv_path = args.output_dir / "sweep_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["index", "mode", "checkpoint", "lora_strength", "cfg", "sampler", "seed", "face_similarity", "local_path"],
        )
        writer.writeheader()
        writer.writerows(rows)

    ranked = sorted(rows, key=lambda r: r["face_similarity"], reverse=True)
    top_path = args.output_dir / "top10_by_similarity.csv"
    with top_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["index", "mode", "checkpoint", "lora_strength", "cfg", "sampler", "seed", "face_similarity", "local_path"],
        )
        writer.writeheader()
        writer.writerows(ranked[:10])

    montage_path = args.output_dir / "sweep_montage.png"
    create_montage(rows, montage_path)

    print(f"[done] summary={csv_path} top10={top_path} montage={montage_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
