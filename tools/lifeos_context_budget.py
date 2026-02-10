#!/usr/bin/env python3
"""Context budget checks for startup files."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path


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
    parser.add_argument("--total-max", type=int, default=220)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()

    budget = {
        "CLAUDE.md": 120,
        "context/goals.md": 10,
        "context/patterns.md": 10,
        "context/session-learnings.md": 80,
    }

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

    total_ok = total_lines <= args.total_max
    overall = all(r.ok for r in results) and total_ok

    if args.json:
        print(
            json.dumps(
                {
                    "project_root": str(root),
                    "total_lines": total_lines,
                    "total_max": args.total_max,
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
        print(f"[{'PASS' if total_ok else 'FAIL'}] total: lines={total_lines} max={args.total_max}")
        print("[PASS] overall" if overall else "[FAIL] overall")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
