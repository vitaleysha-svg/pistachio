#!/usr/bin/env python3
"""Run full autonomous cycle with guardrails, promotion, evals, and local commit."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


class StepError(RuntimeError):
    pass


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def run_command(
    name: str,
    cmd: list[str],
    cwd: Path,
    dry_run: bool,
    env: dict[str, str] | None = None,
) -> None:
    print(f"[step] {name}")
    print("       " + " ".join(cmd))
    if dry_run:
        print("       [dry-run] skipped execution")
        return

    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.stdout.strip():
        print(proc.stdout.rstrip())
    if proc.stderr.strip():
        print(proc.stderr.rstrip())
    if proc.returncode != 0:
        raise StepError(f"{name} failed (exit={proc.returncode})")


def resolve_python_cmd() -> str:
    return sys.executable or "python"


def candidate_image_dirs(project_root: Path) -> list[Path]:
    return [
        project_root / "outputs",
        project_root / "sweep_results",
        project_root / "sweep_results_v2",
        project_root / "outputs" / "sweep_results",
        project_root / "outputs" / "sweep_results_v2",
    ]


def has_images(path: Path, since_unix_ts: float | None = None) -> bool:
    if not path.exists():
        return False
    for candidate in path.rglob("*"):
        if not candidate.is_file() or candidate.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if since_unix_ts is not None and candidate.stat().st_mtime < since_unix_ts:
            continue
        return True
    return False


def detect_generated_dir(project_root: Path, since_unix_ts: float) -> Path | None:
    for candidate in candidate_image_dirs(project_root):
        if has_images(candidate, since_unix_ts=since_unix_ts):
            return candidate
    return None


def detect_reference_dir(project_root: Path) -> Path | None:
    candidates = [
        project_root / "data" / "training_images",
        project_root / "data" / "reference_images",
        project_root / "data",
    ]
    for candidate in candidates:
        if has_images(candidate):
            return candidate
    return None


def run_agent_step(project_root: Path, agent_prompt: Path, dry_run: bool) -> None:
    ps_launcher = project_root / "run-pistachio-agent.ps1"
    sh_launcher = project_root / "run-pistachio-agent.sh"

    if os.name == "nt" and ps_launcher.exists():
        cmd = [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ps_launcher),
            "-ProjectRoot",
            str(project_root),
            "-AgentPromptPath",
            str(agent_prompt),
        ]
        run_command("autonomous_agent", cmd, cwd=project_root, dry_run=dry_run)
        return

    if sh_launcher.exists() and shutil.which("bash"):
        env = os.environ.copy()
        env["PISTACHIO_DIR"] = str(project_root)
        env["AGENT_PROMPT_FILE"] = str(agent_prompt)
        run_command("autonomous_agent", ["bash", str(sh_launcher)], cwd=project_root, dry_run=dry_run, env=env)
        return

    # Fallback: call claude directly if launchers are unavailable.
    if not shutil.which("claude"):
        raise StepError("autonomous_agent failed: neither launcher nor 'claude' command is available.")
    prompt = agent_prompt.read_text(encoding="utf-8")
    runtime_context = (
        "\nRUNTIME CONTEXT\n"
        f"- project_root: {project_root}\n"
        f"- output_dir: {project_root / 'autonomous-research'}\n"
        f"- today: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n"
    )
    run_command(
        "autonomous_agent",
        ["claude", "-p", prompt + runtime_context],
        cwd=project_root,
        dry_run=dry_run,
    )


def commit_results(project_root: Path, dry_run: bool, message: str) -> None:
    run_command("git_add", ["git", "add", "-A"], cwd=project_root, dry_run=dry_run)
    if dry_run:
        return

    diff_proc = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=str(project_root),
        check=False,
    )
    if diff_proc.returncode == 0:
        print("[step] git_commit")
        print("       No staged changes detected. Skipping commit.")
        return

    run_command("git_commit", ["git", "commit", "-m", message], cwd=project_root, dry_run=dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run complete Phase 2 autonomous cycle.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--agent-prompt", type=Path, default=Path("agents/pistachio-agent-v3.md"))
    parser.add_argument("--generated-dir", type=Path, default=None, help="Optional override for generated images dir.")
    parser.add_argument("--reference-dir", type=Path, default=None, help="Optional override for reference images dir.")
    parser.add_argument("--lora-version", default="v3")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--notes", default="")
    parser.add_argument("--max-age-days", type=float, default=7.0)
    parser.add_argument("--skip-commit", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--commit-message",
        default=f"Full cycle automation update ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    python_cmd = resolve_python_cmd()
    start_ts = time.time()

    agent_prompt = args.agent_prompt
    if not agent_prompt.is_absolute():
        agent_prompt = (project_root / agent_prompt).resolve()

    if not agent_prompt.exists():
        raise SystemExit(f"Agent prompt not found: {agent_prompt}")

    try:
        run_command(
            "preflight",
            [python_cmd, str(project_root / "tools" / "lifeos_preflight.py"), "--project-root", str(project_root)],
            cwd=project_root,
            dry_run=args.dry_run,
        )
        run_command(
            "freshness",
            [
                python_cmd,
                str(project_root / "tools" / "lifeos_freshness_check.py"),
                "--project-root",
                str(project_root),
                "--max-age-days",
                str(args.max_age_days),
            ],
            cwd=project_root,
            dry_run=args.dry_run,
        )
        run_command(
            "context_budget",
            [python_cmd, str(project_root / "tools" / "lifeos_context_budget.py"), "--project-root", str(project_root)],
            cwd=project_root,
            dry_run=args.dry_run,
        )
        run_command(
            "known_failures",
            [python_cmd, str(project_root / "evals" / "known_failures.py"), "--project-root", str(project_root)],
            cwd=project_root,
            dry_run=args.dry_run,
        )

        run_agent_step(project_root=project_root, agent_prompt=agent_prompt, dry_run=args.dry_run)

        run_command(
            "promote_findings",
            [python_cmd, str(project_root / "tools" / "promote_findings.py"), "--project-root", str(project_root)],
            cwd=project_root,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            print("[step] eval_scorecard")
            print("       [dry-run] generation/eval detection skipped")
        else:
            generated_dir = args.generated_dir.resolve() if args.generated_dir else detect_generated_dir(project_root, start_ts)
            reference_dir = args.reference_dir.resolve() if args.reference_dir else detect_reference_dir(project_root)

            if generated_dir and reference_dir:
                scorecard_cmd = [
                    python_cmd,
                    str(project_root / "evals" / "scorecard.py"),
                    "--generated",
                    str(generated_dir),
                    "--reference",
                    str(reference_dir),
                    "--lora-version",
                    args.lora_version,
                    "--notes",
                    args.notes,
                ]
                if args.run_id:
                    scorecard_cmd.extend(["--run-id", args.run_id])
                run_command("eval_scorecard", scorecard_cmd, cwd=project_root, dry_run=False)
            else:
                print("[step] eval_scorecard")
                print("       No new generated images (or no reference set) detected, skipping eval step.")

        if not args.skip_commit:
            commit_results(project_root=project_root, dry_run=args.dry_run, message=args.commit_message)
        else:
            print("[step] git_commit")
            print("       Skipped by --skip-commit")

    except StepError as exc:
        print(f"[FAIL] {exc}")
        return 1

    print(f"[done] Full cycle completed at {now_stamp()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

