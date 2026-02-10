#!/usr/bin/env python3
"""Validate pod dependencies referenced by tools scripts.

Usage:
  python3 /workspace/validate_pod_deps.py
  python3 tools/validate_pod_deps.py --project-root .
"""

from __future__ import annotations

import argparse
import ast
import importlib
import importlib.metadata
import importlib.util
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_PINNED = {
    "transformers": "4.38.2",
    "diffusers": "0.25.1",
    "huggingface_hub": "0.21.4",
    "accelerate": "0.27.2",
    "safetensors": "0.4.2",
    "bitsandbytes": "0.43.1",
    "voluptuous": "0.15.2",
    "imagesize": "1.4.1",
    "toml": "0.10.2",
    "insightface": "0.7.3",
    "onnxruntime-gpu": "1.17.1",
    "requests": "2.31.0",
    "Pillow": "10.2.0",
    "numpy": "1.26.4",
    "opencv-python-headless": "4.9.0.80",
    "prodigyopt": "1.1.2",
    "xformers": "0.0.25.post1",
}

IMPORT_TO_PACKAGE = {
    "PIL": "Pillow",
    "cv2": "opencv-python-headless",
    "onnxruntime": "onnxruntime-gpu",
}

PACKAGE_TO_IMPORT = {
    "Pillow": "PIL",
    "opencv-python-headless": "cv2",
    "onnxruntime-gpu": "onnxruntime",
    "pyyaml": "yaml",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


@dataclass
class PackageStatus:
    package: str
    pinned_version: str | None
    installed_version: str | None
    import_name: str
    state: str
    message: str


def normalize_name(name: str) -> str:
    return name.strip().lower().replace("_", "-")


def parse_requirements(path: Path) -> dict[str, str]:
    pinned: dict[str, str] = {}
    if not path.exists():
        return pinned

    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            continue
        package, version = line.split("==", 1)
        pinned[normalize_name(package)] = version.strip()
    return pinned


def discover_tools_dir(project_root: Path) -> Path:
    default = project_root / "tools"
    if default.exists():
        return default
    return project_root


def collect_script_import_roots(py_file: Path) -> set[str]:
    roots: set[str] = set()
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"), filename=str(py_file))
    except SyntaxError:
        return roots

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.module is None:
                continue
            if node.module:
                roots.add(node.module.split(".", 1)[0])
    return roots


def discover_third_party_packages(tools_dir: Path) -> set[str]:
    stdlib = set(getattr(sys, "stdlib_module_names", set()))
    package_set: set[str] = set()
    local_module_names = {p.stem for p in tools_dir.glob("*.py")}

    for py_file in tools_dir.glob("*.py"):
        for root in collect_script_import_roots(py_file):
            if root in {"__future__"}:
                continue
            if root in stdlib:
                continue
            if root in local_module_names:
                continue
            package = IMPORT_TO_PACKAGE.get(root, root)
            package_set.add(package)

    # Runtime dependency used by train command flags even without direct import.
    package_set.add("xformers")
    return package_set


def resolve_import_name(package: str) -> str:
    if package in PACKAGE_TO_IMPORT:
        return PACKAGE_TO_IMPORT[package]
    return package.replace("-", "_")


def resolve_installed_version(package: str, import_name: str) -> str | None:
    candidates = [package, normalize_name(package), import_name, import_name.replace("_", "-")]
    for candidate in candidates:
        try:
            return importlib.metadata.version(candidate)
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def evaluate_package(package: str, pinned_version: str | None) -> PackageStatus:
    import_name = resolve_import_name(package)
    try:
        if importlib.util.find_spec(import_name) is None:
            return PackageStatus(
                package=package,
                pinned_version=pinned_version,
                installed_version=None,
                import_name=import_name,
                state="missing",
                message=f"Module '{import_name}' not importable",
            )
        importlib.import_module(import_name)
    except Exception as exc:  # noqa: BLE001
        return PackageStatus(
            package=package,
            pinned_version=pinned_version,
            installed_version=None,
            import_name=import_name,
            state="missing",
            message=f"Import failed: {exc}",
        )

    installed_version = resolve_installed_version(package, import_name)
    if pinned_version and installed_version and installed_version != pinned_version:
        return PackageStatus(
            package=package,
            pinned_version=pinned_version,
            installed_version=installed_version,
            import_name=import_name,
            state="version_mismatch",
            message=f"Expected {pinned_version}, found {installed_version}",
        )

    if pinned_version and installed_version is None:
        return PackageStatus(
            package=package,
            pinned_version=pinned_version,
            installed_version=None,
            import_name=import_name,
            state="version_unknown",
            message="Imported but distribution version metadata not found",
        )

    return PackageStatus(
        package=package,
        pinned_version=pinned_version,
        installed_version=installed_version,
        import_name=import_name,
        state="ok",
        message="Import and version check passed",
    )


def detect_gpu_vram_gb() -> float | None:
    try:
        proc = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:  # noqa: BLE001
        return None

    values: list[float] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            mib = float(line)
        except ValueError:
            continue
        values.append(mib / 1024.0)
    return max(values) if values else None


def build_vram_report(gpu_total_gb: float) -> dict[str, object]:
    # Rough, conservative ranges for this project's workload.
    blip2_range_gb = [14.0, 18.0]
    lora_range_gb = [12.0, 18.0]
    sequential_peak_gb = max(blip2_range_gb[1], lora_range_gb[1])
    concurrent_peak_gb = blip2_range_gb[1] + lora_range_gb[1] + 2.0

    return {
        "gpu_total_gb": round(gpu_total_gb, 2),
        "blip2_estimated_gb_range": blip2_range_gb,
        "lora_training_estimated_gb_range": lora_range_gb,
        "sequential_peak_gb": round(sequential_peak_gb, 2),
        "concurrent_peak_gb": round(concurrent_peak_gb, 2),
        "fits_sequential": sequential_peak_gb <= gpu_total_gb,
        "fits_concurrent": concurrent_peak_gb <= gpu_total_gb,
        "note": "Captioning and training should be run sequentially; concurrent execution is not recommended.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate pod dependencies for Pistachio tooling.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--tools-dir", type=Path, default=None)
    parser.add_argument("--requirements", type=Path, default=None)
    parser.add_argument("--gpu-vram-gb", type=float, default=24.0, help="Fallback VRAM if nvidia-smi is unavailable.")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    tools_dir = args.tools_dir.resolve() if args.tools_dir else discover_tools_dir(project_root)
    if not tools_dir.exists():
        raise SystemExit(f"Tools directory not found: {tools_dir}")

    default_requirements = project_root / "tools" / "requirements-pod.txt"
    requirements_path = args.requirements.resolve() if args.requirements else default_requirements

    pinned = DEFAULT_PINNED.copy()
    pinned.update(parse_requirements(requirements_path))

    discovered_packages = discover_third_party_packages(tools_dir)
    packages_to_check = sorted({normalize_name(p) for p in discovered_packages}.union(set(pinned.keys())))

    statuses: list[PackageStatus] = []
    for package in packages_to_check:
        display_name = package
        # Restore case for Pillow in install command readability.
        if package == "pillow":
            display_name = "Pillow"
        pinned_version = pinned.get(package)
        statuses.append(evaluate_package(display_name, pinned_version))

    missing = [s for s in statuses if s.state == "missing"]
    mismatches = [s for s in statuses if s.state == "version_mismatch"]

    install_specs: list[str] = []
    for status in statuses:
        if status.state in {"missing", "version_mismatch"}:
            if status.pinned_version:
                install_specs.append(f"{status.package}=={status.pinned_version}")
            else:
                install_specs.append(status.package)
    install_specs = sorted(set(install_specs), key=str.lower)

    detected_gpu = detect_gpu_vram_gb()
    gpu_total = detected_gpu if detected_gpu is not None else args.gpu_vram_gb
    vram_report = build_vram_report(gpu_total)

    payload = {
        "project_root": str(project_root),
        "tools_dir": str(tools_dir),
        "requirements_path": str(requirements_path),
        "packages_checked": len(statuses),
        "missing_count": len(missing),
        "version_mismatch_count": len(mismatches),
        "statuses": [asdict(s) for s in statuses],
        "suggested_install_command": (
            f"python3 -m pip install --no-input {' '.join(install_specs)}" if install_specs else None
        ),
        "vram_report": vram_report,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"[info] project_root={project_root}")
        print(f"[info] requirements={requirements_path}")
        for status in statuses:
            if status.state == "ok":
                prefix = "PASS"
            elif status.state == "version_mismatch":
                prefix = "FAIL"
            elif status.state == "missing":
                prefix = "FAIL"
            else:
                prefix = "WARN"
            print(
                f"[{prefix}] {status.package}: import={status.import_name} "
                f"installed={status.installed_version or 'missing'} "
                f"pinned={status.pinned_version or 'n/a'} "
                f"({status.message})"
            )

        if install_specs:
            print("[fix] Install/update in one shot:")
            print("python3 -m pip install --no-input " + " ".join(install_specs))
        else:
            print("[fix] No dependency fixes required.")

        print("[vram] BLIP-2 estimate: "
              f"{vram_report['blip2_estimated_gb_range'][0]}-{vram_report['blip2_estimated_gb_range'][1]} GB")
        print("[vram] LoRA training estimate: "
              f"{vram_report['lora_training_estimated_gb_range'][0]}-{vram_report['lora_training_estimated_gb_range'][1]} GB")
        print(f"[vram] GPU total considered: {vram_report['gpu_total_gb']} GB")
        print(f"[vram] Sequential fit on 24GB-class GPU: {'PASS' if vram_report['fits_sequential'] else 'FAIL'}")
        print(f"[vram] Concurrent fit on 24GB-class GPU: {'PASS' if vram_report['fits_concurrent'] else 'FAIL'}")

    return 1 if missing or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
