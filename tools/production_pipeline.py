#!/usr/bin/env python3
"""End-to-end production generation pipeline with quality gates."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PROMPTS = [
    "amiranoor, candid photo at outdoor cafe, golden hour, shot on Canon 5D 85mm, shallow dof",
    "amiranoor, sitting on park bench, autumn leaves, natural sunlight, casual outfit",
    "amiranoor, walking down city street, golden hour, candid shot, urban background",
    "amiranoor, close up portrait, soft window light, indoor, natural expression",
    "amiranoor, beach sunset, looking at camera, warm tones, wind in hair",
    "amiranoor, restaurant table, evening lighting, elegant outfit, candid framing",
    "amiranoor, rooftop terrace, city skyline, magic hour, lifestyle photo",
    "amiranoor, garden setting, morning light, floral dress, natural pose",
    "amiranoor, coffee shop window seat, rainy day, cozy lighting, reading",
    "amiranoor, poolside, bright midday sun, swimwear, vacation candid",
]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_command(name: str, cmd: list[str], cwd: Path) -> str:
    print(f"[step] {name}")
    print("       " + " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)
    if proc.stdout.strip():
        print(proc.stdout.rstrip())
    if proc.stderr.strip():
        print(proc.stderr.rstrip())
    if proc.returncode != 0:
        raise RuntimeError(f"{name} failed (exit={proc.returncode})")
    return proc.stdout


def parse_json_output(stdout: str) -> dict[str, Any]:
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def load_prompts(args: argparse.Namespace) -> list[str]:
    prompts: list[str] = []
    if args.prompts:
        prompts.extend([line.strip() for line in args.prompts.read_text(encoding="utf-8").splitlines() if line.strip()])
    prompts.extend(args.prompt)
    if not prompts:
        prompts = list(DEFAULT_PROMPTS)
    return list(dict.fromkeys(prompts))


def iter_images(path: Path) -> list[Path]:
    images: list[Path] = []
    for candidate in sorted(path.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(candidate)
    return images


def write_report(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Production Batch Report",
        "",
        f"- Timestamp: `{payload['timestamp']}`",
        f"- LoRA: `{payload['lora']}`",
        f"- Settings: `strength={payload['settings']['lora_strength']}` `cfg={payload['settings']['cfg']}` `sampler={payload['settings']['sampler']}` `steps={payload['settings']['steps']}`",
        f"- Total Generated: `{payload['counts']['generated']}`",
        f"- Approved: `{payload['counts']['approved']}`",
        f"- Rejected: `{payload['counts']['rejected']}`",
        f"- Face Similarity Mean (approved): `{payload['approved_means']['face_similarity']:.4f}`",
        f"- Skin Realism Mean (approved): `{payload['approved_means']['skin_realism']:.4f}`",
        f"- Scorecard Grade: `{payload['scorecard_grade']}`",
        "",
        "## Best/Worst",
    ]
    if payload.get("best"):
        best = payload["best"]
        lines.append(
            f"- Best: `{best['file']}` face={best['face']:.4f} skin={best['skin']:.4f} combined={best['combined']:.4f}"
        )
    if payload.get("worst"):
        worst = payload["worst"]
        lines.append(
            f"- Worst: `{worst['file']}` face={worst['face']:.4f} skin={worst['skin']:.4f} combined={worst['combined']:.4f}"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run production generation + eval + filtering pipeline.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--workflow", type=Path, required=True)
    parser.add_argument("--prompts", type=Path, default=None, help="Prompt file (one prompt per line).")
    parser.add_argument("--prompt", action="append", default=[], help="Inline prompt. Can be repeated.")
    parser.add_argument("--lora", required=True, help="LoRA filename or identifier used for this batch.")
    parser.add_argument("--lora-version", default="v3")
    parser.add_argument("--count", type=int, default=5, help="Images per prompt.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--reference-dir", type=Path, required=True)
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--lora-strength", type=float, default=0.8)
    parser.add_argument("--cfg", type=float, default=4.0)
    parser.add_argument("--sampler", default="dpmpp_2m")
    parser.add_argument("--face-threshold", type=float, default=None)
    parser.add_argument("--skin-threshold", type=float, default=None)
    parser.add_argument("--skip-health-check", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_dir = output_dir / "generated_raw"
    approved_dir = output_dir / "approved"
    rejected_dir = output_dir / "rejected"
    generated_dir.mkdir(parents=True, exist_ok=True)
    approved_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)

    prompts = load_prompts(args)
    python_cmd = sys.executable

    if not args.skip_health_check:
        health_cmd = [
            python_cmd,
            str(project_root / "tools" / "pod_health_check.py"),
            "--comfy-url",
            args.comfy_url,
            "--json",
        ]
        if args.skip_install:
            health_cmd.append("--skip-install")
        run_command("health_check", health_cmd, cwd=project_root)

    generate_cmd = [
        python_cmd,
        str(project_root / "tools" / "generate_batch.py"),
        "--workflow",
        str(args.workflow.resolve()),
        "--comfy-url",
        args.comfy_url,
        "--images-per-prompt",
        str(args.count),
        "--output-dir",
        str(generated_dir),
        "--negative-prompt",
        args.negative_prompt,
        "--steps",
        str(args.steps),
    ]
    if args.skip_install:
        generate_cmd.append("--skip-install")
    for prompt in prompts:
        generate_cmd.extend(["--prompt", prompt])
    run_command("generate_batch", generate_cmd, cwd=project_root)

    face_cmd = [
        python_cmd,
        str(project_root / "evals" / "face_similarity_eval.py"),
        "--generated",
        str(generated_dir),
        "--reference",
        str(args.reference_dir.resolve()),
    ]
    if args.face_threshold is not None:
        face_cmd.extend(["--threshold", str(args.face_threshold)])
    if args.skip_install:
        face_cmd.append("--skip-install")
    face_result = parse_json_output(run_command("face_eval", face_cmd, cwd=project_root))

    skin_cmd = [
        python_cmd,
        str(project_root / "evals" / "skin_realism_eval.py"),
        "--generated",
        str(generated_dir),
        "--reference",
        str(args.reference_dir.resolve()),
    ]
    if args.skin_threshold is not None:
        skin_cmd.extend(["--threshold", str(args.skin_threshold)])
    if args.skip_install:
        skin_cmd.append("--skip-install")
    skin_result = parse_json_output(run_command("skin_eval", skin_cmd, cwd=project_root))

    scorecard_cmd = [
        python_cmd,
        str(project_root / "evals" / "scorecard.py"),
        "--generated",
        str(generated_dir),
        "--reference",
        str(args.reference_dir.resolve()),
        "--lora-version",
        args.lora_version,
        "--run-id",
        f"production_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}",
        "--notes",
        f"production batch lora={args.lora} cfg={args.cfg} sampler={args.sampler} steps={args.steps}",
    ]
    if args.face_threshold is not None:
        scorecard_cmd.extend(["--face-threshold", str(args.face_threshold)])
    if args.skin_threshold is not None:
        scorecard_cmd.extend(["--skin-threshold", str(args.skin_threshold)])
    if args.skip_install:
        scorecard_cmd.append("--skip-install")
    scorecard = parse_json_output(run_command("scorecard", scorecard_cmd, cwd=project_root))

    face_threshold = float(scorecard["thresholds"]["face_similarity"])
    skin_threshold = float(scorecard["thresholds"]["skin_realism"])

    face_map = {row["image"]: float(row["score"]) for row in face_result.get("per_image", [])}
    skin_map = {row["image"]: float(row["overall_realism_score"]) for row in skin_result.get("per_image", [])}

    ranked_rows: list[dict[str, Any]] = []
    for image_path in iter_images(generated_dir):
        key = str(image_path)
        face_score = face_map.get(key, 0.0)
        skin_score = skin_map.get(key, 0.0)
        combined = 0.60 * face_score + 0.40 * skin_score
        row = {
            "path": image_path,
            "face": face_score,
            "skin": skin_score,
            "combined": combined,
            "approved": face_score >= face_threshold and skin_score >= skin_threshold,
        }
        ranked_rows.append(row)

    ranked_rows.sort(key=lambda row: row["combined"], reverse=True)
    approved_rows = [row for row in ranked_rows if row["approved"]]
    rejected_rows = [row for row in ranked_rows if not row["approved"]]

    for row in approved_rows:
        target = approved_dir / row["path"].name
        shutil.move(str(row["path"]), str(target))
    for row in rejected_rows:
        target = rejected_dir / row["path"].name
        shutil.move(str(row["path"]), str(target))

    approved_face_mean = (
        sum(row["face"] for row in approved_rows) / len(approved_rows) if approved_rows else 0.0
    )
    approved_skin_mean = (
        sum(row["skin"] for row in approved_rows) / len(approved_rows) if approved_rows else 0.0
    )

    payload = {
        "timestamp": now_stamp(),
        "lora": args.lora,
        "settings": {
            "lora_strength": args.lora_strength,
            "cfg": args.cfg,
            "sampler": args.sampler,
            "steps": args.steps,
        },
        "counts": {
            "generated": len(ranked_rows),
            "approved": len(approved_rows),
            "rejected": len(rejected_rows),
        },
        "approved_means": {
            "face_similarity": approved_face_mean,
            "skin_realism": approved_skin_mean,
        },
        "scorecard_grade": scorecard.get("overall_grade", "F"),
        "thresholds": scorecard.get("thresholds", {}),
        "best": (
            {
                "file": ranked_rows[0]["path"].name,
                "face": ranked_rows[0]["face"],
                "skin": ranked_rows[0]["skin"],
                "combined": ranked_rows[0]["combined"],
            }
            if ranked_rows
            else None
        ),
        "worst": (
            {
                "file": ranked_rows[-1]["path"].name,
                "face": ranked_rows[-1]["face"],
                "skin": ranked_rows[-1]["skin"],
                "combined": ranked_rows[-1]["combined"],
            }
            if ranked_rows
            else None
        ),
    }

    report_path = output_dir / "batch_report.md"
    write_report(report_path, payload)
    (output_dir / "batch_report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"[done] output_dir={output_dir} report={report_path}")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

