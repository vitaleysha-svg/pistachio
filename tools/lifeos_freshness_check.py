#!/usr/bin/env python3
"""Freshness checks for autonomous-research memory files."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class FreshnessResult:
    file: str
    exists: bool
    age_days: float | None
    ok: bool
    message: str


def age_days(path: Path) -> float:
    now = time.time()
    mtime = path.stat().st_mtime
    return (now - mtime) / 86400.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check freshness of autonomous-research files")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--max-age-days", type=float, default=7.0)
    parser.add_argument("--require-today-briefing", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    ar = root / "autonomous-research"

    targets = [
        "memory.md",
        "pending-tasks.md",
        "predictions.md",
        "recommendations.md",
        "questions.md",
        "GOLD-pistachio.md",
    ]

    results: list[FreshnessResult] = []

    for rel in targets:
        path = ar / rel
        if not path.exists():
            results.append(
                FreshnessResult(rel, False, None, False, "missing")
            )
            continue

        age = age_days(path)
        ok = age <= args.max_age_days
        msg = f"age={age:.2f}d threshold={args.max_age_days:.2f}d"
        results.append(FreshnessResult(rel, True, age, ok, msg))

    if args.require_today_briefing:
        today = time.strftime("%Y-%m-%d")
        briefing = ar / f"briefing-{today}.md"
        if not briefing.exists():
            results.append(
                FreshnessResult(f"briefing-{today}.md", False, None, False, "missing today briefing")
            )
        else:
            age = age_days(briefing)
            results.append(
                FreshnessResult(f"briefing-{today}.md", True, age, True, f"exists age={age:.2f}d")
            )

    overall = all(r.ok for r in results)

    if args.json:
        print(
            json.dumps(
                {
                    "project_root": str(root),
                    "overall_ok": overall,
                    "results": [asdict(r) for r in results],
                },
                indent=2,
            )
        )
    else:
        for r in results:
            status = "PASS" if r.ok else "FAIL"
            print(f"[{status}] {r.file}: {r.message}")
        print("[PASS] overall" if overall else "[FAIL] overall")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
