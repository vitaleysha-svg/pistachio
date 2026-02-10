#!/usr/bin/env python3
"""LifeOS preflight checks.

Purpose:
- catch stale hardcoded paths in authoritative files
- catch broken references in active skill/context docs
- verify required files and tools exist
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class CheckResult:
    name: str
    ok: bool
    message: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def check_required_files(root: Path, rel_paths: list[str]) -> CheckResult:
    missing = [p for p in rel_paths if not (root / p).exists()]
    if missing:
        return CheckResult("required_files", False, "Missing: " + ", ".join(missing))
    return CheckResult("required_files", True, "All required files present")


def check_required_commands(commands: list[str]) -> CheckResult:
    missing = [cmd for cmd in commands if shutil.which(cmd) is None]
    if missing:
        return CheckResult("required_commands", False, "Missing commands: " + ", ".join(missing))
    return CheckResult("required_commands", True, "Required commands present")


def check_hardcoded_paths(root: Path, rel_files: list[str]) -> CheckResult:
    patterns = [
        re.compile(r"/Users/[A-Za-z0-9._-]+/"),
        re.compile(r"/home/[A-Za-z0-9._-]+/"),
        re.compile(r"[A-Za-z]:\\Users\\mateuszjez", re.IGNORECASE),
    ]
    violations: list[str] = []

    for rel in rel_files:
        path = root / rel
        if not path.exists():
            violations.append(f"{rel}: file missing")
            continue
        text = read_text(path)
        for pattern in patterns:
            if pattern.search(text):
                violations.append(f"{rel}: contains hardcoded user path ({pattern.pattern})")
                break

    if violations:
        return CheckResult("hardcoded_paths", False, " | ".join(violations))
    return CheckResult("hardcoded_paths", True, "No hardcoded user paths in authoritative files")


def check_stale_manual_reference(root: Path, rel_files: list[str]) -> CheckResult:
    needle = "PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md"
    offenders = []
    for rel in rel_files:
        path = root / rel
        if not path.exists():
            continue
        if needle in read_text(path):
            offenders.append(rel)

    if offenders:
        return CheckResult(
            "stale_manual_reference",
            False,
            f"Legacy manual path referenced in: {', '.join(offenders)}",
        )
    return CheckResult("stale_manual_reference", True, "No legacy manual path in authoritative files")


def check_broken_backtick_refs(root: Path, rel_files: list[str]) -> CheckResult:
    token_re = re.compile(r"`([^`]+)`")
    offenders: list[str] = []

    for rel in rel_files:
        path = root / rel
        if not path.exists():
            continue
        text = read_text(path)
        for token in token_re.findall(text):
            token = token.strip()
            if not token:
                continue
            if token.startswith("http://") or token.startswith("https://"):
                continue
            if token.startswith("--"):
                continue
            if token in {"PROGRESS.md", "CODEX-CHANGES.md", "CLAUDE.md"}:
                candidate = root / token
            else:
                candidate = root / token
            if "/" not in token and "\\" not in token and "." not in token:
                continue
            if candidate.exists():
                continue
            # tolerate output filename template references
            if "YYYY" in token or "DD" in token:
                continue
            # tolerate command examples
            if token.lower().startswith("python") or token.lower().startswith("bash"):
                continue
            offenders.append(f"{rel} -> `{token}`")

    if offenders:
        preview = "; ".join(offenders[:10])
        more = "" if len(offenders) <= 10 else f" (+{len(offenders)-10} more)"
        return CheckResult("broken_backtick_refs", False, preview + more)
    return CheckResult("broken_backtick_refs", True, "Backtick path references resolve")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run LifeOS preflight checks")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--skip-commands", action="store_true", help="Skip command availability checks (for CI).")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()

    required_files = [
        "CLAUDE.md",
        "PROGRESS.md",
        "agents/pistachio-agent-v2.md",
        "context/projects/pistachio/SKILL.md",
        "context/projects/pistachio/context.md",
        "context/session-learnings.md",
        "run-pistachio-agent.ps1",
    ]

    authoritative_files = [
        "run-pistachio-agent.ps1",
        "run-pistachio-agent.sh",
        "agents/pistachio-agent-v2.md",
        "context/projects/pistachio/SKILL.md",
        "context/projects/pistachio/context.md",
    ]

    results = [
        check_required_files(root, required_files),
    ]
    if not args.skip_commands:
        results.append(check_required_commands(["claude", "python"]))
    results.extend([
        check_hardcoded_paths(root, authoritative_files),
        check_stale_manual_reference(root, authoritative_files),
        check_broken_backtick_refs(root, ["context/projects/pistachio/SKILL.md", "context/projects/pistachio/context.md"]),
    ])

    overall = all(r.ok for r in results)

    if args.json:
        payload = {
            "project_root": str(root),
            "overall_ok": overall,
            "checks": [asdict(r) for r in results],
        }
        print(json.dumps(payload, indent=2))
    else:
        for r in results:
            status = "PASS" if r.ok else "FAIL"
            print(f"[{status}] {r.name}: {r.message}")
        print("[PASS] overall" if overall else "[FAIL] overall")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
