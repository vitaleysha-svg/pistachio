#!/usr/bin/env python3
"""Compare two evaluation runs from eval history and emit markdown report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from load_thresholds import load_thresholds  # noqa: E402


GRADE_ORDER = ["F", "D", "C", "B", "A"]


def grade_rank(grade: str) -> int:
    try:
        return GRADE_ORDER.index(grade.upper())
    except ValueError:
        return -1


def load_history(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def find_run(rows: list[dict[str, Any]], query: str) -> dict[str, Any] | None:
    exact = [row for row in rows if row.get("run_id") == query]
    if exact:
        return exact[-1]
    partial = [row for row in rows if query in str(row.get("run_id", ""))]
    if partial:
        return partial[-1]
    return None


def extract_metrics(run: dict[str, Any]) -> dict[str, Any]:
    scores = run.get("eval_scores", {})
    return {
        "face_similarity_mean": float(scores.get("face_similarity_mean", 0.0)),
        "skin_realism_mean": float(scores.get("skin_realism_mean", 0.0)),
        "overall_grade": str(scores.get("overall_grade", "F")),
        "best_config": scores.get("best_config", "n/a"),
        "worst_config": scores.get("worst_config", "n/a"),
        "promotion_recommended": bool(scores.get("promotion_recommended", False)),
        "training_params": run.get("training_params", {}),
    }


def verdict_for_delta(delta: float) -> str:
    if delta > 0.0001:
        return "IMPROVED"
    if delta < -0.0001:
        return "REGRESSED"
    return "UNCHANGED"


def format_training_params(params: dict[str, Any]) -> str:
    if not params:
        return "n/a"
    compact = ", ".join(f"{key}={value}" for key, value in sorted(params.items()))
    return compact[:3000]


def build_report(v1_id: str, v2_id: str, v1: dict[str, Any], v2: dict[str, Any], promotion_min_grade: str) -> str:
    m1 = extract_metrics(v1)
    m2 = extract_metrics(v2)

    face_delta = m2["face_similarity_mean"] - m1["face_similarity_mean"]
    skin_delta = m2["skin_realism_mean"] - m1["skin_realism_mean"]
    grade_delta_levels = grade_rank(m2["overall_grade"]) - grade_rank(m1["overall_grade"])
    grade_verdict = "IMPROVED" if grade_delta_levels > 0 else "REGRESSED" if grade_delta_levels < 0 else "UNCHANGED"

    promote = grade_rank(m2["overall_grade"]) >= grade_rank(promotion_min_grade)
    recommendation = (
        f"{v2_id} meets promotion threshold (grade >= {promotion_min_grade}). Recommend deploying latest LoRA."
        if promote
        else f"{v2_id} does not meet promotion threshold (grade >= {promotion_min_grade}). Keep previous version."
    )

    lines = [
        f"# Version Comparison: {v1_id} vs {v2_id}",
        "",
        "| Metric | " + v1_id + " | " + v2_id + " | Delta | Verdict |",
        "|--------|----------|----------|-------|---------|",
        f"| Face Similarity (mean) | {m1['face_similarity_mean']:.4f} | {m2['face_similarity_mean']:.4f} | {face_delta:+.4f} | {verdict_for_delta(face_delta)} |",
        f"| Skin Realism (mean) | {m1['skin_realism_mean']:.4f} | {m2['skin_realism_mean']:.4f} | {skin_delta:+.4f} | {verdict_for_delta(skin_delta)} |",
        f"| Overall Grade | {m1['overall_grade']} | {m2['overall_grade']} | {grade_delta_levels:+d} levels | {grade_verdict} |",
        f"| Best Config | {m1['best_config']} | {m2['best_config']} | - | - |",
        "",
        "## Recommendation",
        recommendation,
        "",
        "## Config Details",
        f"- {v1_id}: {format_training_params(m1['training_params'])}",
        f"- {v2_id}: {format_training_params(m2['training_params'])}",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two runs from eval history.")
    parser.add_argument("--history", type=Path, default=Path("evals/eval_history.jsonl"))
    parser.add_argument("--v1", required=True, help="Run ID (or substring) for baseline version.")
    parser.add_argument("--v2", required=True, help="Run ID (or substring) for candidate version.")
    parser.add_argument("--output", type=Path, default=Path("evals/comparison_report.md"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_history(args.history)
    if not rows:
        print("No eval history found. Run scorecard first to generate eval records.")
        return 1

    run_v1 = find_run(rows, args.v1)
    run_v2 = find_run(rows, args.v2)
    if run_v1 is None or run_v2 is None:
        missing = []
        if run_v1 is None:
            missing.append(args.v1)
        if run_v2 is None:
            missing.append(args.v2)
        print("Could not find run(s) in history: " + ", ".join(missing))
        return 1

    thresholds = load_thresholds(project_root=Path.cwd())
    promotion_min = str(thresholds["scorecard"].get("promotion_minimum_grade", "C"))

    report = build_report(
        v1_id=str(run_v1.get("run_id")),
        v2_id=str(run_v2.get("run_id")),
        v1=run_v1,
        v2=run_v2,
        promotion_min_grade=promotion_min,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"[ok] wrote comparison report: {args.output}")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

