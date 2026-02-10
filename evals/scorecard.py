#!/usr/bin/env python3
"""Run the Phase 2 eval suite and emit a structured scorecard."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from face_similarity_eval import evaluate_face_similarity  # noqa: E402
from skin_realism_eval import evaluate_skin_realism  # noqa: E402


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_training_params(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    candidate = Path(raw)
    text = candidate.read_text(encoding="utf-8") if candidate.exists() else raw
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def grade_for_score(value: float) -> str:
    if value >= 0.80:
        return "A"
    if value >= 0.70:
        return "B"
    if value >= 0.60:
        return "C"
    if value >= 0.50:
        return "D"
    return "F"


def config_id_from_image(path_str: str) -> str:
    path = Path(path_str)
    stem = path.stem
    match = re.search(r"(step\d+_str[\d.]+_cfg[\d.]+)", stem)
    if match:
        return match.group(1)
    return stem


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_latest_report(path: Path, payload: dict[str, Any], top_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Latest Eval Report",
        "",
        f"- Run ID: `{payload['run_id']}`",
        f"- Timestamp: `{payload['timestamp']}`",
        f"- LoRA Version: `{payload['lora_version']}`",
        f"- Images Evaluated: `{payload['images_evaluated']}`",
        f"- Face Similarity Mean: `{payload['face_similarity_mean']:.4f}` ({'PASS' if payload['face_similarity_pass'] else 'FAIL'})",
        f"- Skin Realism Mean: `{payload['skin_realism_mean']:.4f}`",
        f"- Overall Grade: `{payload['overall_grade']}`",
        f"- Best Config: `{payload['best_config']}`",
        f"- Worst Config: `{payload['worst_config']}`",
        "",
        "## Top Samples",
    ]
    for row in top_rows[:5]:
        lines.append(
            f"- `{Path(row['image']).name}`: combined={row['combined']:.4f} "
            f"(face={row['face']:.4f}, realism={row['realism']:.4f})"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_scorecard(
    face_result: dict[str, Any],
    skin_result: dict[str, Any],
    run_id: str,
    lora_version: str,
    face_threshold: float,
    skin_threshold: float,
    notes: str,
    training_params: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    face_map = {item["image"]: item["score"] for item in face_result["per_image"]}
    skin_map = {item["image"]: item["overall_realism_score"] for item in skin_result["per_image"]}
    combined_rows: list[dict[str, Any]] = []

    for image, face_score in face_map.items():
        realism_score = skin_map.get(image)
        if realism_score is None:
            continue
        combined = 0.60 * face_score + 0.40 * realism_score
        combined_rows.append(
            {
                "image": image,
                "face": face_score,
                "realism": realism_score,
                "combined": combined,
                "config": config_id_from_image(image),
            }
        )

    if not combined_rows:
        raise RuntimeError("No overlapping image rows between face and skin eval results.")

    ranked = sorted(combined_rows, key=lambda row: row["combined"], reverse=True)
    best = ranked[0]
    worst = ranked[-1]

    face_mean = float(face_result["mean_similarity"])
    skin_mean = float(skin_result["overall_realism_score_mean"])
    combined_mean = 0.60 * face_mean + 0.40 * skin_mean

    payload = {
        "run_id": run_id,
        "timestamp": now_iso(),
        "lora_version": lora_version,
        "face_similarity_mean": face_mean,
        "face_similarity_pass": face_mean >= face_threshold,
        "skin_realism_mean": skin_mean,
        "skin_realism_pass": skin_mean >= skin_threshold,
        "overall_grade": grade_for_score(combined_mean),
        "images_evaluated": len(ranked),
        "best_config": best["config"],
        "worst_config": worst["config"],
        "thresholds": {"face_similarity": face_threshold, "skin_realism": skin_threshold},
        "notes": notes,
        "training_params": training_params,
        "detail_files": {
            "face_similarity": "evals/face_similarity_latest.json",
            "skin_realism": "evals/skin_realism_latest.json",
        },
    }

    return payload, ranked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build structured scorecard from face + skin evals.")
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--lora-version", default="v3")
    parser.add_argument("--face-threshold", type=float, default=0.60)
    parser.add_argument("--skin-threshold", type=float, default=0.60)
    parser.add_argument("--notes", default="")
    parser.add_argument("--training-params", default=None, help="JSON string or path to JSON file.")
    parser.add_argument("--history-file", type=Path, default=Path("evals/eval_history.jsonl"))
    parser.add_argument("--output-json", type=Path, default=Path("evals/latest_scorecard.json"))
    parser.add_argument("--latest-report", type=Path, default=Path("evals/latest_report.md"))
    parser.add_argument("--fail-on-threshold", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_id = args.run_id or f"{args.lora_version}_sweep_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    training_params = parse_training_params(args.training_params)

    ensure_parent(Path("evals/face_similarity_latest.json"))
    face_output = Path("evals/face_similarity_latest.json")
    skin_output = Path("evals/skin_realism_latest.json")

    # Re-run detail evals and persist the latest snapshots for traceability.
    face_detail = evaluate_face_similarity(
        generated_dir=args.generated,
        reference_dir=args.reference,
        threshold=args.face_threshold,
        skip_install=args.skip_install,
    )
    face_output.write_text(json.dumps(face_detail, indent=2), encoding="utf-8")

    skin_detail = evaluate_skin_realism(
        generated_dir=args.generated,
        reference_dir=args.reference,
        threshold=args.skin_threshold,
        skip_install=args.skip_install,
    )
    skin_output.write_text(json.dumps(skin_detail, indent=2), encoding="utf-8")

    payload, ranked = build_scorecard(
        face_result=face_detail,
        skin_result=skin_detail,
        run_id=run_id,
        lora_version=args.lora_version,
        face_threshold=args.face_threshold,
        skin_threshold=args.skin_threshold,
        notes=args.notes,
        training_params=training_params,
    )

    ensure_parent(args.output_json)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    history_entry = {
        "run_id": payload["run_id"],
        "timestamp": payload["timestamp"],
        "lora_version": payload["lora_version"],
        "training_params": payload["training_params"],
        "eval_scores": {
            "face_similarity_mean": payload["face_similarity_mean"],
            "face_similarity_pass": payload["face_similarity_pass"],
            "skin_realism_mean": payload["skin_realism_mean"],
            "skin_realism_pass": payload["skin_realism_pass"],
            "overall_grade": payload["overall_grade"],
            "images_evaluated": payload["images_evaluated"],
            "best_config": payload["best_config"],
            "worst_config": payload["worst_config"],
        },
        "notes": payload["notes"],
    }

    ensure_parent(args.history_file)
    with args.history_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(history_entry) + "\n")

    ensure_parent(args.latest_report)
    write_latest_report(args.latest_report, payload, ranked)

    print(json.dumps(payload, indent=2))
    if args.fail_on_threshold and not (payload["face_similarity_pass"] and payload["skin_realism_pass"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
