#!/usr/bin/env python3
"""Load centralized threshold policy with safe fallbacks."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

DEFAULT_THRESHOLDS: dict[str, Any] = {
    "face_similarity": {
        "pass_threshold": 0.60,
        "warn_threshold": 0.50,
        "metric": "cosine_similarity",
        "description": "InsightFace embedding cosine similarity between generated and reference faces",
    },
    "skin_realism": {
        "texture_pass_threshold": 0.60,
        "color_naturalness_pass_threshold": 0.55,
        "overall_pass_threshold": 0.60,
        "description": "Laplacian variance + skin-tone histogram comparison",
    },
    "scorecard": {
        "grade_boundaries": {
            "A": 0.85,
            "B": 0.70,
            "C": 0.55,
            "D": 0.40,
            "F": 0.0,
        },
        "promotion_minimum_grade": "C",
        "description": "Combined face similarity + skin realism weighted average",
    },
    "context_budget": {
        "claude_md_max_lines": 120,
        "goals_max_lines": 10,
        "patterns_max_lines": 10,
        "session_learnings_max_lines": 80,
        "total_max_lines": 220,
    },
    "freshness": {
        "max_age_days": 7,
        "ci_max_age_days": 14,
    },
}


def _fallback_safe_load(text: str) -> dict[str, Any]:
    """Minimal YAML mapping parser used only if PyYAML is unavailable.

    Supports the subset used by `evals/thresholds.yaml`:
    - nested dictionaries using indentation
    - scalar values (int/float/bool/string)
    """
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue

        indent = len(line) - len(line.lstrip(" "))
        key_part, value_part = stripped.split(":", 1)
        key = key_part.strip()
        value_part = value_part.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if value_part == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
            continue

        value: Any
        lower = value_part.lower()
        if lower in {"true", "false"}:
            value = lower == "true"
        else:
            if (value_part.startswith('"') and value_part.endswith('"')) or (
                value_part.startswith("'") and value_part.endswith("'")
            ):
                value = value_part[1:-1]
            else:
                try:
                    if "." in value_part:
                        value = float(value_part)
                    else:
                        value = int(value_part)
                except ValueError:
                    value = value_part
        parent[key] = value

    return root


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def resolve_thresholds_path(project_root: Path | None, thresholds_path: Path | None) -> Path:
    if thresholds_path is not None:
        return thresholds_path.resolve()
    if project_root is not None:
        return (project_root / "evals" / "thresholds.yaml").resolve()
    return (Path(__file__).resolve().parent / "thresholds.yaml").resolve()


def load_thresholds(project_root: Path | None = None, thresholds_path: Path | None = None) -> dict[str, Any]:
    path = resolve_thresholds_path(project_root=project_root, thresholds_path=thresholds_path)
    merged = copy.deepcopy(DEFAULT_THRESHOLDS)
    if not path.exists():
        return merged

    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        import yaml  # type: ignore

        parsed = yaml.safe_load(text)  # required primary parser
    except ImportError:
        parsed = _fallback_safe_load(text)
    except Exception:
        return merged

    if not isinstance(parsed, dict):
        return merged
    return _deep_merge(merged, parsed)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load and print merged threshold policy.")
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--thresholds-path", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    thresholds = load_thresholds(project_root=args.project_root, thresholds_path=args.thresholds_path)
    print(json.dumps(thresholds, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

