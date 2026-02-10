#!/usr/bin/env python3
"""Regression checks based on known historical failures in this project."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import py_compile
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from load_thresholds import _fallback_safe_load, load_thresholds

PACKAGE_TO_IMPORT = {
    "Pillow": "PIL",
    "opencv-python-headless": "cv2",
    "onnxruntime-gpu": "onnxruntime",
    "pyyaml": "yaml",
}

BANNED_REFERENCE_SNIPPETS = [
    "PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md",
    "/Users/mateuszjez/",
    "/home/mateuszjez/",
    "C:\\Users\\mateuszjez",
]

ALLOWED_RUNTIME_REFERENCES = {
    "memory.md",
    "pending-tasks.md",
    "predictions.md",
    "recommendations.md",
    "questions.md",
    "briefing-YYYY-MM-DD.md",
}


@dataclass
class TestResult:
    name: str
    passed: bool
    details: str


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("_", "-")


def parse_requirements(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing requirements file: {path}")

    requirements: dict[str, str] = {}
    duplicates: list[str] = []
    malformed: list[str] = []
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            malformed.append(line)
            continue
        package, version = line.split("==", 1)
        key = normalize_name(package)
        if key in requirements:
            duplicates.append(key)
        requirements[key] = version.strip()

    if malformed:
        raise RuntimeError("Unpinned or malformed requirements lines: " + ", ".join(malformed))
    if duplicates:
        raise RuntimeError("Duplicate requirements found: " + ", ".join(sorted(set(duplicates))))
    return requirements


def version_tuple(version: str) -> tuple[int, ...]:
    parts = re.split(r"[^\d]+", version)
    nums = [int(part) for part in parts if part.isdigit()]
    return tuple(nums)


def check_compatibility_rules(requirements: dict[str, str]) -> list[str]:
    issues: list[str] = []

    hub = requirements.get("huggingface-hub") or requirements.get("huggingface_hub")
    diffusers = requirements.get("diffusers")
    if hub and diffusers:
        hub_v = version_tuple(hub)
        if not ((0, 20, 0) <= hub_v < (0, 22, 0)):
            issues.append(
                f"diffusers=={diffusers} expects huggingface_hub in [0.20.0,0.22.0), found {hub}"
            )

    transformers = requirements.get("transformers")
    if transformers and hub:
        hub_v = version_tuple(hub)
        if hub_v < (0, 19, 0):
            issues.append(
                f"transformers=={transformers} is not compatible with huggingface_hub=={hub}"
            )

    return issues


def import_name_for_package(package: str) -> str:
    for raw_name, import_name in PACKAGE_TO_IMPORT.items():
        if normalize_name(raw_name) == normalize_name(package):
            return import_name
    return package.replace("-", "_")


def distribution_version(package: str, import_name: str) -> str | None:
    candidates = [package, normalize_name(package), import_name, import_name.replace("_", "-")]
    for candidate in candidates:
        try:
            return importlib.metadata.version(candidate)
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def dependency_chain_test(project_root: Path, strict_runtime: bool) -> TestResult:
    requirements_path = project_root / "tools" / "requirements-pod.txt"
    try:
        requirements = parse_requirements(requirements_path)
    except Exception as exc:  # noqa: BLE001
        return TestResult("dependency_chain_test", False, str(exc))

    compatibility_issues = check_compatibility_rules(requirements)
    if compatibility_issues:
        return TestResult("dependency_chain_test", False, "; ".join(compatibility_issues))

    missing_runtime: list[str] = []
    version_mismatches: list[str] = []
    checked = 0

    for package, pinned in sorted(requirements.items()):
        import_name = import_name_for_package(package)
        checked += 1
        try:
            importlib.import_module(import_name)
        except Exception:  # noqa: BLE001
            missing_runtime.append(f"{package}=={pinned}")
            continue

        installed = distribution_version(package, import_name)
        if installed and installed != pinned:
            version_mismatches.append(f"{package}: expected {pinned}, found {installed}")

    if strict_runtime and (version_mismatches or missing_runtime):
        return TestResult(
            "dependency_chain_test",
            False,
            "Runtime dependency issues in strict mode: "
            + ", ".join(missing_runtime + version_mismatches),
        )

    detail = f"requirements parsed={checked}, strict_runtime={strict_runtime}"
    if missing_runtime:
        detail += f", runtime_missing={len(missing_runtime)} (allowed in non-strict mode)"
    if version_mismatches:
        detail += f", runtime_version_mismatch={len(version_mismatches)} (allowed in non-strict mode)"
    return TestResult("dependency_chain_test", True, detail)


def training_flag_test(project_root: Path) -> TestResult:
    path = project_root / "tools" / "retrain_lora_v3.py"
    if not path.exists():
        return TestResult("training_flag_test", False, f"Missing script: {path}")

    text = path.read_text(encoding="utf-8", errors="ignore")
    has_cache_text_encoder = "--cache_text_encoder_outputs" in text
    has_text_encoder_lr = "--text_encoder_lr" in text
    has_train_encoder_gate = "--train-text-encoder" in text

    if has_cache_text_encoder and has_text_encoder_lr:
        return TestResult(
            "training_flag_test",
            False,
            "Found conflicting flags: --cache_text_encoder_outputs with --text_encoder_lr",
        )
    if has_text_encoder_lr and not has_train_encoder_gate:
        return TestResult(
            "training_flag_test",
            False,
            "--text_encoder_lr found without --train-text-encoder gating",
        )

    return TestResult("training_flag_test", True, "No conflicting training flags detected")


def stale_reference_test(project_root: Path) -> TestResult:
    active_files = [
        "CLAUDE.md",
        "PROGRESS.md",
        "context/projects/pistachio/context.md",
        "context/projects/pistachio/SKILL.md",
        "run-pistachio-agent.sh",
        "run-pistachio-agent.ps1",
        "agents/pistachio-agent-v2.md",
        "agents/pistachio-agent-v3.md",
    ]

    offenders: list[str] = []
    path_token_re = re.compile(r"`([^`]+)`")
    markdown_link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for rel in active_files:
        path = project_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")

        for needle in BANNED_REFERENCE_SNIPPETS:
            if needle in text:
                offenders.append(f"{rel}: contains '{needle}'")

        tokens = path_token_re.findall(text) + markdown_link_re.findall(text)
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token.startswith(("http://", "https://")):
                continue
            if token in ALLOWED_RUNTIME_REFERENCES:
                continue
            if token.startswith("--"):
                continue
            if token.startswith("/") and "." not in Path(token).name:
                # Skill invocation aliases like `/learned-mistakes`.
                continue
            if "YYYY" in token or "DD" in token:
                continue
            if token.lower().startswith(("python ", "bash ", "git ")):
                continue
            if "/" not in token and "\\" not in token and "." not in token:
                continue
            candidate = (project_root / token).resolve() if not Path(token).is_absolute() else Path(token)
            if candidate.exists():
                continue
            offenders.append(f"{rel}: missing path reference `{token}`")

    if offenders:
        preview = "; ".join(offenders[:12])
        more = "" if len(offenders) <= 12 else f" (+{len(offenders) - 12} more)"
        return TestResult("stale_reference_test", False, preview + more)
    return TestResult("stale_reference_test", True, "No stale active references detected")


def context_budget_test(project_root: Path) -> TestResult:
    script = project_root / "tools" / "lifeos_context_budget.py"
    if not script.exists():
        return TestResult("context_budget_test", False, f"Missing script: {script}")

    proc = subprocess.run(
        [sys.executable, str(script), "--project-root", str(project_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        details = proc.stdout.strip() or proc.stderr.strip() or "context budget check failed"
        return TestResult("context_budget_test", False, details)
    return TestResult("context_budget_test", True, "Startup context under budget")


def threshold_policy_test(project_root: Path) -> TestResult:
    path = project_root / "evals" / "thresholds.yaml"
    if not path.exists():
        return TestResult("threshold_policy_test", False, f"Missing threshold policy: {path}")

    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        import yaml  # type: ignore

        parsed = yaml.safe_load(text)
    except ImportError:
        try:
            parsed = _fallback_safe_load(text)
        except Exception as exc:  # noqa: BLE001
            return TestResult("threshold_policy_test", False, f"Invalid fallback YAML parse: {exc}")
    except Exception as exc:  # noqa: BLE001
        return TestResult("threshold_policy_test", False, f"Invalid YAML syntax: {exc}")

    if not isinstance(parsed, dict):
        return TestResult("threshold_policy_test", False, "thresholds.yaml did not parse to a mapping")

    try:
        thresholds = load_thresholds(project_root=project_root, thresholds_path=path)
    except Exception as exc:  # noqa: BLE001
        return TestResult("threshold_policy_test", False, f"Invalid threshold YAML: {exc}")

    required = {
        "face_similarity": ["pass_threshold", "warn_threshold", "metric", "description"],
        "skin_realism": [
            "texture_pass_threshold",
            "color_naturalness_pass_threshold",
            "overall_pass_threshold",
            "description",
        ],
        "scorecard": ["grade_boundaries", "promotion_minimum_grade", "description"],
        "context_budget": [
            "claude_md_max_lines",
            "goals_max_lines",
            "patterns_max_lines",
            "session_learnings_max_lines",
            "total_max_lines",
        ],
        "freshness": ["max_age_days", "ci_max_age_days"],
    }

    missing: list[str] = []
    for section, keys in required.items():
        if section not in thresholds:
            missing.append(section)
            continue
        for key in keys:
            if key not in thresholds[section]:
                missing.append(f"{section}.{key}")

    grade_boundaries = thresholds.get("scorecard", {}).get("grade_boundaries", {})
    for grade in ["A", "B", "C", "D", "F"]:
        if grade not in grade_boundaries:
            missing.append(f"scorecard.grade_boundaries.{grade}")

    if missing:
        return TestResult("threshold_policy_test", False, "Missing policy keys: " + ", ".join(missing))
    return TestResult("threshold_policy_test", True, "Threshold policy YAML valid with required keys")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dataset_manifest_test(project_root: Path) -> TestResult:
    manifests = sorted(project_root.rglob("dataset_manifest.json"), key=lambda p: p.stat().st_mtime)
    if not manifests:
        return TestResult("dataset_manifest_test", True, "No dataset manifest found; skipping integrity check")

    manifest_path = manifests[-1]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return TestResult("dataset_manifest_test", False, f"Invalid JSON in {manifest_path}: {exc}")

    dataset_dir_value = manifest.get("dataset_dir")
    if not dataset_dir_value:
        return TestResult("dataset_manifest_test", False, f"dataset_dir missing in {manifest_path}")
    dataset_dir = Path(dataset_dir_value)
    if not dataset_dir.is_absolute():
        dataset_dir = (manifest_path.parent / dataset_dir).resolve()

    failures: list[str] = []
    for item in manifest.get("images", []):
        rel_file = item.get("filename")
        expected_hash = item.get("sha256")
        if not rel_file or not expected_hash:
            failures.append(f"invalid item entry in manifest: {item}")
            continue

        image_path = (dataset_dir / rel_file).resolve()
        if not image_path.exists():
            failures.append(f"missing image: {rel_file}")
            continue
        actual_hash = sha256_file(image_path)
        if actual_hash != expected_hash:
            failures.append(f"hash mismatch image: {rel_file}")

        caption_rel = item.get("caption_file")
        caption_hash = item.get("caption_sha256")
        if caption_rel and caption_hash:
            caption_path = (dataset_dir / caption_rel).resolve()
            if not caption_path.exists():
                failures.append(f"missing caption: {caption_rel}")
            elif sha256_file(caption_path) != caption_hash:
                failures.append(f"hash mismatch caption: {caption_rel}")

    if failures:
        preview = "; ".join(failures[:10])
        more = "" if len(failures) <= 10 else f" (+{len(failures)-10} more)"
        return TestResult("dataset_manifest_test", False, preview + more)
    return TestResult("dataset_manifest_test", True, f"Manifest integrity verified: {manifest_path}")


def script_syntax_test(project_root: Path) -> TestResult:
    failures: list[str] = []
    checked = 0
    for rel_dir in ["tools", "evals"]:
        dir_path = project_root / rel_dir
        if not dir_path.exists():
            continue
        for py_file in sorted(dir_path.rglob("*.py")):
            checked += 1
            try:
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as exc:
                failures.append(f"{py_file}: {exc.msg}")

    if failures:
        preview = "; ".join(failures[:8])
        more = "" if len(failures) <= 8 else f" (+{len(failures) - 8} more)"
        return TestResult("script_syntax_test", False, preview + more)
    return TestResult("script_syntax_test", True, f"Compiled {checked} python files")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run regression checks from known project failures.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--strict-runtime-deps", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()

    results = [
        dependency_chain_test(root, strict_runtime=args.strict_runtime_deps),
        training_flag_test(root),
        stale_reference_test(root),
        threshold_policy_test(root),
        context_budget_test(root),
        dataset_manifest_test(root),
        script_syntax_test(root),
    ]

    passed = all(result.passed for result in results)

    if args.json:
        print(
            json.dumps(
                {
                    "project_root": str(root),
                    "overall_pass": passed,
                    "results": [asdict(result) for result in results],
                },
                indent=2,
            )
        )
    else:
        for result in results:
            status = "PASS" if result.passed else "FAIL"
            print(f"[{status}] {result.name}: {result.details}")
        print("[PASS] overall" if passed else "[FAIL] overall")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
