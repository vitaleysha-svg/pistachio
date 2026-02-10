#!/usr/bin/env python3
"""Promote autonomous briefing findings into persistent task/memory artifacts."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ACTION_KEYWORDS = {
    "fix",
    "run",
    "update",
    "create",
    "implement",
    "test",
    "verify",
    "ship",
    "promote",
    "add",
    "remove",
    "document",
    "train",
    "evaluate",
}

LEARNING_KEYWORDS = {
    "learned",
    "lesson",
    "insight",
    "finding",
    "root cause",
    "because",
    "mistake",
}

CRITICAL_RULE_HINTS = {
    "never",
    "always",
    "do not",
    "must",
    "critical",
}


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_bullet_line(line: str) -> bool:
    stripped = line.strip()
    return bool(re.match(r"^(- |\* |\d+\.\s+)", stripped))


def normalize_item(line: str) -> str:
    stripped = line.strip()
    stripped = re.sub(r"^(- |\* |\d+\.\s+)", "", stripped)
    stripped = re.sub(r"^\[[ xX]\]\s*", "", stripped)
    return stripped.strip()


def classify_item(item: str, heading: str) -> str:
    lower = item.lower()
    heading_lower = heading.lower()

    if any(keyword in heading_lower for keyword in ("action", "next", "todo", "task", "recommend")):
        return "action"
    if any(keyword in heading_lower for keyword in ("learn", "insight", "finding", "lesson", "mistake")):
        return "learning"

    if any(keyword in lower for keyword in LEARNING_KEYWORDS):
        return "learning"

    words = set(re.findall(r"[a-zA-Z]+", lower))
    if words.intersection(ACTION_KEYWORDS):
        return "action"
    return "other"


def parse_briefing(briefing_path: Path) -> tuple[list[str], list[str]]:
    actions: list[str] = []
    learnings: list[str] = []
    heading = ""
    lines = briefing_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            continue
        if not is_bullet_line(line):
            continue
        item = normalize_item(line)
        if not item:
            continue
        kind = classify_item(item, heading)
        if kind == "action":
            actions.append(item)
        elif kind == "learning":
            learnings.append(item)

    # De-duplicate while preserving order.
    actions = list(dict.fromkeys(actions))
    learnings = list(dict.fromkeys(learnings))
    return actions, learnings


def latest_briefing(autonomous_dir: Path) -> Path | None:
    briefings = sorted(autonomous_dir.glob("briefing-*.md"))
    if not briefings:
        return None
    # Prefer newest by timestamp/name.
    briefings = sorted(briefings, key=lambda p: (p.stat().st_mtime, p.name))
    return briefings[-1]


def append_block(path: Path, title: str, lines: list[str]) -> tuple[str, str]:
    before = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    after = before
    if not after.endswith("\n") and after:
        after += "\n"
    after += f"\n## {title}\n"
    for line in lines:
        after += line + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(after, encoding="utf-8")
    return before, after


def print_diff(path: Path, before: str, after: str) -> None:
    diff = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"{path} (before)",
            tofile=f"{path} (after)",
            lineterm="",
        )
    )
    if not diff:
        return
    print(f"--- Diff for {path} ---")
    for line in diff:
        print(line)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote autonomous briefing findings into task + memory files.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--briefing", type=Path, default=None, help="Override briefing path.")
    parser.add_argument("--apply-critical", action="store_true", help="Append candidate critical-rule updates.")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    autonomous_dir = root / "autonomous-research"
    pending_path = autonomous_dir / "pending-tasks.md"
    memory_path = autonomous_dir / "memory.md"
    session_learnings_path = root / "context" / "session-learnings.md"

    briefing_path = args.briefing.resolve() if args.briefing else latest_briefing(autonomous_dir)
    if briefing_path is None or not briefing_path.exists():
        print("[FAIL] No briefing file found (expected autonomous-research/briefing-*.md).")
        return 1

    actions, learnings = parse_briefing(briefing_path)
    if not actions and not learnings:
        print(f"[WARN] No actionable bullets found in {briefing_path.name}. Nothing promoted.")
        return 0

    promotion_title = f"Promotion {now_date()} from {briefing_path.name}"

    pending_lines = [f"- [ ] {item}" for item in actions] if actions else ["- [ ] Manual review: no explicit action bullets detected."]
    memory_lines = [f"- {item}" for item in learnings] if learnings else ["- No explicit learning bullets found in briefing."]

    pending_before, pending_after = append_block(pending_path, promotion_title, pending_lines)
    memory_before, memory_after = append_block(memory_path, promotion_title, memory_lines)

    critical_candidates: list[str] = []
    for item in actions + learnings:
        lower = item.lower()
        if any(hint in lower for hint in CRITICAL_RULE_HINTS):
            critical_candidates.append(item)
    critical_candidates = list(dict.fromkeys(critical_candidates))

    if args.apply_critical and critical_candidates:
        critical_title = f"Candidate Updates from Autonomous Findings ({now_iso()})"
        critical_lines = [f"- {candidate}" for candidate in critical_candidates]
        session_before, session_after = append_block(session_learnings_path, critical_title, critical_lines)
        if not args.quiet:
            print_diff(session_learnings_path, session_before, session_after)

    if not args.quiet:
        print_diff(pending_path, pending_before, pending_after)
        print_diff(memory_path, memory_before, memory_after)

    print(
        f"[done] briefing={briefing_path.name} actions_promoted={len(actions)} "
        f"learnings_promoted={len(learnings)} critical_candidates={len(critical_candidates)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

