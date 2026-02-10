#!/usr/bin/env python3
"""Run the eval suite and emit a structured scorecard."""

from __future__ import annotations

import argparse
import hashlib
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
from load_thresholds import load_thresholds  # noqa: E402
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


def grade_for_score(value: float, boundaries: dict[str, float]) -> str:
    ordered = sorted(boundaries.items(), key=lambda item: item[1], reverse=True)
    for grade, floor in ordered:
        if value >= float(floor):
            return grade
    return "F"


def grade_rank(grade: str) -> int:
    order = ["F", "D", "C", "B", "A"]
    try:
        return order.index(grade.upper())
    except ValueError:
        return -1


def config_id_from_image(path_str: str) -> str:
    path = Path(path_str)
    stem = path.stem
    match = re.search(r"(step\d+_str[\d.]+_cfg[\d.]+)", stem)
    if match:
        return match.group(1)
    return stem


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        f"- Promotion Recommended: `{'yes' if payload['promotion_recommended'] else 'no'}`",
        f"- Best Config: `{payload['best_config']}`",
        f"- Worst Config: `{payload['worst_config']}`",
    ]
    if payload.get("dataset_manifest_hash"):
        lines.append(f"- Dataset Manifest Hash: `{payload['dataset_manifest_hash']}`")
    lines.extend(["", "## Top Samples"])
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
    texture_threshold: float,
    color_threshold: float,
    grade_boundaries: dict[str, float],
    promotion_minimum_grade: str,
    notes: str,
    training_params: dict[str, Any],
    dataset_manifest_path: str | None,
    dataset_manifest_hash: str | None,
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
    overall_grade = grade_for_score(combined_mean, grade_boundaries)

    payload = {
        "run_id": run_id,
        "timestamp": now_iso(),
        "lora_version": lora_version,
        "face_similarity_mean": face_mean,
        "face_similarity_pass": face_mean >= face_threshold,
        "skin_realism_mean": skin_mean,
        "skin_realism_pass": skin_mean >= skin_threshold,
        "skin_texture_pass": float(skin_result["texture_score_mean"]) >= texture_threshold,
        "skin_color_pass": float(skin_result["color_naturalness_score_mean"]) >= color_threshold,
        "overall_grade": overall_grade,
        "promotion_minimum_grade": promotion_minimum_grade,
        "promotion_recommended": grade_rank(overall_grade) >= grade_rank(promotion_minimum_grade),
        "images_evaluated": len(ranked),
        "best_config": best["config"],
        "worst_config": worst["config"],
        "thresholds": {
            "face_similarity": face_threshold,
            "skin_realism": skin_threshold,
            "skin_texture": texture_threshold,
            "skin_color": color_threshold,
        },
        "notes": notes,
        "training_params": training_params,
        "dataset_manifest_path": dataset_manifest_path,
        "dataset_manifest_hash": dataset_manifest_hash,
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
    parser.add_argument("--face-threshold", type=float, default=None)
    parser.add_argument("--skin-threshold", type=float, default=None)
    parser.add_argument("--skin-texture-threshold", type=float, default=None)
    parser.add_argument("--skin-color-threshold", type=float, default=None)
    parser.add_argument("--notes", default="")
    parser.add_argument("--training-params", default=None, help="JSON string or path to JSON file.")
    parser.add_argument("--dataset-manifest", type=Path, default=None)
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
    thresholds = load_thresholds(project_root=Path.cwd())

    face_policy = thresholds["face_similarity"]
    skin_policy = thresholds["skin_realism"]
    scorecard_policy = thresholds["scorecard"]

    grade_boundaries = {
        str(key): float(value)
        for key, value in scorecard_policy.get("grade_boundaries", {}).items()
    } or {"A": 0.85, "B": 0.70, "C": 0.55, "D": 0.40, "F": 0.0}
    promotion_minimum_grade = str(scorecard_policy.get("promotion_minimum_grade", "C"))

    face_threshold = (
        args.face_threshold
        if args.face_threshold is not None
        else float(face_policy["pass_threshold"])
    )
    skin_threshold = (
        args.skin_threshold
        if args.skin_threshold is not None
        else float(skin_policy["overall_pass_threshold"])
    )
    texture_threshold = (
        args.skin_texture_threshold
        if args.skin_texture_threshold is not None
        else float(skin_policy["texture_pass_threshold"])
    )
    color_threshold = (
        args.skin_color_threshold
        if args.skin_color_threshold is not None
        else float(skin_policy["color_naturalness_pass_threshold"])
    )

    dataset_manifest_path = None
    dataset_manifest_hash = None
    manifest_candidate: Path | None = None
    if args.dataset_manifest:
        manifest_candidate = args.dataset_manifest.resolve()
    else:
        auto_candidates = [
            args.generated / "dataset_manifest.json",
            args.generated.parent / "dataset_manifest.json",
            Path.cwd() / "dataset_manifest.json",
            Path.cwd() / "outputs" / "dataset_manifest.json",
        ]
        for candidate in auto_candidates:
            if candidate.exists():
                manifest_candidate = candidate.resolve()
                break
    if manifest_candidate is not None:
        if not manifest_candidate.exists():
            raise FileNotFoundError(f"Dataset manifest not found: {manifest_candidate}")
        dataset_manifest_path = str(manifest_candidate)
        dataset_manifest_hash = file_sha256(manifest_candidate)

    ensure_parent(Path("evals/face_similarity_latest.json"))
    face_output = Path("evals/face_similarity_latest.json")
    skin_output = Path("evals/skin_realism_latest.json")

    face_detail = evaluate_face_similarity(
        generated_dir=args.generated,
        reference_dir=args.reference,
        threshold=face_threshold,
        skip_install=args.skip_install,
    )
    face_output.write_text(json.dumps(face_detail, indent=2), encoding="utf-8")

    skin_detail = evaluate_skin_realism(
        generated_dir=args.generated,
        reference_dir=args.reference,
        threshold=skin_threshold,
        texture_threshold=texture_threshold,
        color_threshold=color_threshold,
        skip_install=args.skip_install,
    )
    skin_output.write_text(json.dumps(skin_detail, indent=2), encoding="utf-8")

    payload, ranked = build_scorecard(
        face_result=face_detail,
        skin_result=skin_detail,
        run_id=run_id,
        lora_version=args.lora_version,
        face_threshold=face_threshold,
        skin_threshold=skin_threshold,
        texture_threshold=texture_threshold,
        color_threshold=color_threshold,
        grade_boundaries=grade_boundaries,
        promotion_minimum_grade=promotion_minimum_grade,
        notes=args.notes,
        training_params=training_params,
        dataset_manifest_path=dataset_manifest_path,
        dataset_manifest_hash=dataset_manifest_hash,
    )

    ensure_parent(args.output_json)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    history_entry = {
        "run_id": payload["run_id"],
        "timestamp": payload["timestamp"],
        "lora_version": payload["lora_version"],
        "training_params": payload["training_params"],
        "dataset_manifest_path": payload["dataset_manifest_path"],
        "dataset_manifest_hash": payload["dataset_manifest_hash"],
        "eval_scores": {
            "face_similarity_mean": payload["face_similarity_mean"],
            "face_similarity_pass": payload["face_similarity_pass"],
            "skin_realism_mean": payload["skin_realism_mean"],
            "skin_realism_pass": payload["skin_realism_pass"],
            "skin_texture_pass": payload["skin_texture_pass"],
            "skin_color_pass": payload["skin_color_pass"],
            "overall_grade": payload["overall_grade"],
            "promotion_recommended": payload["promotion_recommended"],
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
