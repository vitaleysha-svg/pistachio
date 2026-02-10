#!/usr/bin/env python3
"""Context budget checks for startup files."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parents[1] / "evals"
if str(EVALS_DIR) not in sys.path:
    sys.path.insert(0, str(EVALS_DIR))

from load_thresholds import load_thresholds  # noqa: E402


@dataclass
class BudgetResult:
    file: str
    lines: int
    max_lines: int
    ok: bool


def count_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8", errors="ignore").splitlines())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check LifeOS context line budget")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--total-max", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    policy = load_thresholds(project_root=root)["context_budget"]

    budget = {
        "CLAUDE.md": int(policy["claude_md_max_lines"]),
        "context/goals.md": int(policy["goals_max_lines"]),
        "context/patterns.md": int(policy["patterns_max_lines"]),
        "context/session-learnings.md": int(policy["session_learnings_max_lines"]),
    }
    total_max = args.total_max if args.total_max is not None else int(policy["total_max_lines"])

    results: list[BudgetResult] = []
    total_lines = 0

    for rel, max_lines in budget.items():
        path = root / rel
        if not path.exists():
            results.append(BudgetResult(rel, -1, max_lines, False))
            continue
        lines = count_lines(path)
        total_lines += lines
        results.append(BudgetResult(rel, lines, max_lines, lines <= max_lines))

    total_ok = total_lines <= total_max
    overall = all(r.ok for r in results) and total_ok

    if args.json:
        print(
            json.dumps(
                {
                    "project_root": str(root),
                    "policy_source": str(root / "evals" / "thresholds.yaml"),
                    "total_lines": total_lines,
                    "total_max": total_max,
                    "total_ok": total_ok,
                    "overall_ok": overall,
                    "files": [asdict(r) for r in results],
                },
                indent=2,
            )
        )
    else:
        for r in results:
            status = "PASS" if r.ok else "FAIL"
            line_display = "missing" if r.lines < 0 else str(r.lines)
            print(f"[{status}] {r.file}: lines={line_display} max={r.max_lines}")
        print(f"[{'PASS' if total_ok else 'FAIL'}] total: lines={total_lines} max={total_max}")
        print("[PASS] overall" if overall else "[FAIL] overall")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())

