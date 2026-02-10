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
    parser = argparse.ArgumentParser(description="Run complete autonomous cycle.")
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
    parser.add_argument("--skip-cost-tracking", action="store_true")
    parser.add_argument("--cost-activity", default="autonomous_loop")
    parser.add_argument("--cost-rate-per-hr", type=float, default=0.60)
    parser.add_argument("--cost-gpu", default="RTX 4090")
    parser.add_argument("--training-dataset-dir", type=Path, default=None)
    parser.add_argument("--training-output-dir", type=Path, default=None)
    parser.add_argument("--dataset-manifest-out", type=Path, default=None)
    parser.add_argument("--compare-with-run-id", default=None)
    parser.add_argument("--comparison-output", type=Path, default=Path("evals/comparison_report.md"))
    parser.add_argument("--run-production", action="store_true")
    parser.add_argument("--production-workflow", type=Path, default=None)
    parser.add_argument("--production-prompts", type=Path, default=None)
    parser.add_argument("--production-count", type=int, default=5)
    parser.add_argument("--production-output-dir", type=Path, default=None)
    parser.add_argument("--production-reference-dir", type=Path, default=None)
    parser.add_argument("--production-lora", default=None)
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

    manifest_path: Path | None = None
    scorecard_run_id = args.run_id or f"{args.lora_version}_sweep_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    agent_failed = False
    cost_started = False

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

        if args.training_dataset_dir and args.training_output_dir:
            dataset_dir = args.training_dataset_dir.resolve()
            training_output_dir = args.training_output_dir.resolve()
            manifest_path = (
                args.dataset_manifest_out.resolve()
                if args.dataset_manifest_out
                else training_output_dir / "dataset_manifest.json"
            )
            run_command(
                "dataset_manifest",
                [
                    python_cmd,
                    str(project_root / "tools" / "dataset_manifest.py"),
                    "--dataset-dir",
                    str(dataset_dir),
                    "--output",
                    str(manifest_path),
                ],
                cwd=project_root,
                dry_run=args.dry_run,
            )

        if not args.skip_cost_tracking:
            run_command(
                "cost_start",
                [
                    python_cmd,
                    str(project_root / "tools" / "runpod_cost_tracker.py"),
                    "--action",
                    "start",
                    "--activity",
                    args.cost_activity,
                    "--rate-per-hr",
                    str(args.cost_rate_per_hr),
                    "--gpu",
                    args.cost_gpu,
                ],
                cwd=project_root,
                dry_run=args.dry_run,
            )
            cost_started = True

        try:
            run_agent_step(project_root=project_root, agent_prompt=agent_prompt, dry_run=args.dry_run)
        except Exception:  # noqa: BLE001
            agent_failed = True
            raise
        finally:
            if cost_started:
                try:
                    run_command(
                        "cost_stop",
                        [
                            python_cmd,
                            str(project_root / "tools" / "runpod_cost_tracker.py"),
                            "--action",
                            "stop",
                        ],
                        cwd=project_root,
                        dry_run=args.dry_run,
                    )
                except StepError as exc:
                    if agent_failed:
                        print(f"[warn] cost_stop failed after agent failure: {exc}")
                    else:
                        raise

        run_command(
            "promote_findings",
            [python_cmd, str(project_root / "tools" / "promote_findings.py"), "--project-root", str(project_root)],
            cwd=project_root,
            dry_run=args.dry_run,
        )

        scorecard_generated = False
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
                    "--run-id",
                    scorecard_run_id,
                    "--notes",
                    args.notes,
                ]
                if manifest_path is not None:
                    scorecard_cmd.extend(["--dataset-manifest", str(manifest_path)])
                run_command("eval_scorecard", scorecard_cmd, cwd=project_root, dry_run=False)
                scorecard_generated = True
            else:
                print("[step] eval_scorecard")
                print("       No new generated images (or no reference set) detected, skipping eval step.")

        if scorecard_generated and args.compare_with_run_id:
            run_command(
                "compare_versions",
                [
                    python_cmd,
                    str(project_root / "evals" / "compare_versions.py"),
                    "--history",
                    str(project_root / "evals" / "eval_history.jsonl"),
                    "--v1",
                    args.compare_with_run_id,
                    "--v2",
                    scorecard_run_id,
                    "--output",
                    str(args.comparison_output.resolve()),
                ],
                cwd=project_root,
                dry_run=args.dry_run,
            )

        if args.run_production:
            if args.production_workflow is None:
                raise StepError("--run-production requires --production-workflow")
            production_output = (
                args.production_output_dir.resolve()
                if args.production_output_dir
                else (project_root / "outputs" / f"production_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}")
            )
            production_reference = (
                args.production_reference_dir.resolve()
                if args.production_reference_dir
                else (args.reference_dir.resolve() if args.reference_dir else detect_reference_dir(project_root))
            )
            if production_reference is None:
                raise StepError("--run-production could not resolve reference directory")

            production_cmd = [
                python_cmd,
                str(project_root / "tools" / "production_pipeline.py"),
                "--project-root",
                str(project_root),
                "--workflow",
                str(args.production_workflow.resolve()),
                "--lora",
                args.production_lora or f"{args.lora_version}.safetensors",
                "--lora-version",
                args.lora_version,
                "--count",
                str(args.production_count),
                "--output-dir",
                str(production_output),
                "--reference-dir",
                str(production_reference),
            ]
            if args.production_prompts is not None:
                production_cmd.extend(["--prompts", str(args.production_prompts.resolve())])
            run_command("production_pipeline", production_cmd, cwd=project_root, dry_run=args.dry_run)

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

