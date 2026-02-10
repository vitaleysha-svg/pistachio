#!/usr/bin/env python3
"""Generate batch images from prompt list via ComfyUI API."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

REQUIRED_PACKAGES = {
    "requests": "2.31.0",
}


def ensure_dependencies(skip_install: bool) -> None:
    missing = []
    for package, version in REQUIRED_PACKAGES.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(f"{package}=={version}")

    if not missing:
        return
    if skip_install:
        raise RuntimeError("Missing dependencies: " + ", ".join(missing))
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-input", *missing], check=True)


def load_prompts(args: argparse.Namespace) -> list[str]:
    prompts = []
    if args.prompts_file:
        prompts.extend([line.strip() for line in args.prompts_file.read_text(encoding="utf-8").splitlines() if line.strip()])
    prompts.extend(args.prompt)
    unique = []
    seen = set()
    for prompt in prompts:
        if prompt not in seen:
            unique.append(prompt)
            seen.add(prompt)
    if not unique:
        raise RuntimeError("No prompts provided. Use --prompts-file and/or --prompt.")
    return unique


def set_input(prompt: dict[str, Any], node_id: str, key: str, value: Any) -> None:
    if node_id not in prompt:
        raise KeyError(f"Node id not found in workflow: {node_id}")
    prompt[node_id]["inputs"][key] = value


def queue_prompt(requests_mod, comfy_url: str, prompt: dict[str, Any], client_id: str) -> str:
    response = requests_mod.post(
        comfy_url.rstrip("/") + "/prompt",
        json={"prompt": prompt, "client_id": client_id},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["prompt_id"]


def wait_result(requests_mod, comfy_url: str, prompt_id: str, timeout_sec: int, poll_interval: float) -> dict[str, Any]:
    deadline = time.time() + timeout_sec
    url = comfy_url.rstrip("/") + f"/history/{prompt_id}"
    while time.time() < deadline:
        response = requests_mod.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        if prompt_id in data:
            return data[prompt_id]
        time.sleep(poll_interval)
    raise TimeoutError(f"Timeout waiting for prompt_id={prompt_id}")


def first_image(history_item: dict[str, Any]) -> dict[str, str]:
    for output in history_item.get("outputs", {}).values():
        images = output.get("images") or []
        if images:
            return images[0]
    raise RuntimeError("No images in history output")


def download_image(requests_mod, comfy_url: str, image_ref: dict[str, str]) -> bytes:
    response = requests_mod.get(
        comfy_url.rstrip("/") + "/view",
        params={
            "filename": image_ref.get("filename", ""),
            "subfolder": image_ref.get("subfolder", ""),
            "type": image_ref.get("type", "output"),
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.content


def sanitize_filename(text: str) -> str:
    keep = []
    for ch in text.lower():
        keep.append(ch if ch.isalnum() else "_")
    collapsed = "".join(keep)
    while "__" in collapsed:
        collapsed = collapsed.replace("__", "_")
    return collapsed.strip("_")[:80] or "prompt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch image generation through ComfyUI API.")
    parser.add_argument("--workflow", type=Path, required=True, help="API-format workflow JSON.")
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument("--prompts-file", type=Path)
    parser.add_argument("--prompt", action="append", default=[])
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--images-per-prompt", type=int, default=1)
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/batch_outputs"))
    parser.add_argument("--base-seed", type=int, default=42420000)
    parser.add_argument("--steps", type=int, default=30)

    parser.add_argument("--positive-node-id", default="6")
    parser.add_argument("--positive-key", default="text")
    parser.add_argument("--negative-node-id", default="7")
    parser.add_argument("--negative-key", default="text")
    parser.add_argument("--ksampler-node-id", default="3")
    parser.add_argument("--seed-key", default="seed")
    parser.add_argument("--steps-key", default="steps")

    parser.add_argument("--timeout-sec", type=int, default=600)
    parser.add_argument("--poll-interval", type=float, default=1.5)
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    import requests

    if not args.workflow.exists():
        raise FileNotFoundError(f"Workflow file not found: {args.workflow}")

    workflow = json.loads(args.workflow.read_text(encoding="utf-8"))
    if "nodes" in workflow:
        raise RuntimeError("Detected UI workflow JSON. Export API-format workflow JSON and retry.")

    prompts = load_prompts(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    client_id = str(uuid.uuid4())
    seed = args.base_seed
    total_jobs = len(prompts) * args.images_per_prompt
    job_index = 0

    for prompt_idx, prompt_text in enumerate(prompts, start=1):
        for variant in range(1, args.images_per_prompt + 1):
            job_index += 1
            prompt = copy.deepcopy(workflow)
            set_input(prompt, args.positive_node_id, args.positive_key, prompt_text)
            set_input(prompt, args.negative_node_id, args.negative_key, args.negative_prompt)
            set_input(prompt, args.ksampler_node_id, args.seed_key, seed)
            set_input(prompt, args.ksampler_node_id, args.steps_key, args.steps)

            prompt_id = queue_prompt(requests, args.comfy_url, prompt, client_id)
            history = wait_result(
                requests,
                args.comfy_url,
                prompt_id,
                timeout_sec=args.timeout_sec,
                poll_interval=args.poll_interval,
            )
            image_ref = first_image(history)
            image_bytes = download_image(requests, args.comfy_url, image_ref)

            filename = (
                f"{job_index:04d}_p{prompt_idx:03d}_v{variant:02d}_"
                f"seed{seed}_{sanitize_filename(prompt_text)}.png"
            )
            out_path = args.output_dir / filename
            out_path.write_bytes(image_bytes)

            print(f"[job {job_index}/{total_jobs}] saved {out_path}")
            seed += 1

    print(f"[done] generated={total_jobs} output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
