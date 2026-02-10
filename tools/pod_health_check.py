#!/usr/bin/env python3
"""RunPod/ComfyUI health check utility.

Checks:
- ComfyUI API availability
- Required node classes available in /object_info
- Required model files exist
- VRAM availability
- Disk space
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REQUIRED_PACKAGES = {
    "requests": "2.31.0",
}


def ensure_dependencies(skip_install: bool) -> None:
    missing = []
    for package, version in REQUIRED_PACKAGES.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(f"{package}=={version}")

    if not missing:
        return
    if skip_install:
        raise RuntimeError("Missing dependencies: " + ", ".join(missing))

    subprocess.run([sys.executable, "-m", "pip", "install", "--no-input", *missing], check=True)


def check_comfy_api(requests_mod, comfy_url: str) -> tuple[bool, str, dict[str, Any] | None]:
    try:
        response = requests_mod.get(comfy_url.rstrip("/") + "/system_stats", timeout=15)
        response.raise_for_status()
        data = response.json()
        return True, "ComfyUI API reachable", data
    except Exception as exc:  # noqa: BLE001
        return False, f"ComfyUI API unavailable: {exc}", None


def check_nodes(requests_mod, comfy_url: str, required_nodes: list[str]) -> tuple[bool, str, dict[str, Any] | None]:
    if not required_nodes:
        return True, "No required node checks configured", None

    try:
        response = requests_mod.get(comfy_url.rstrip("/") + "/object_info", timeout=20)
        response.raise_for_status()
        data = response.json()
        available = set(data.keys())

        missing = []
        for required in required_nodes:
            found = any(required.lower() in node_name.lower() for node_name in available)
            if not found:
                missing.append(required)

        if missing:
            return False, f"Missing node classes: {', '.join(missing)}", data
        return True, "Required node classes found", data
    except Exception as exc:  # noqa: BLE001
        return False, f"Failed node check: {exc}", None


def check_models(paths: list[str]) -> tuple[bool, str, list[str]]:
    if not paths:
        return True, "No required model paths configured", []

    missing = [p for p in paths if not Path(p).exists()]
    if missing:
        return False, f"Missing model files: {len(missing)}", missing
    return True, f"All required model files found: {len(paths)}", []


def check_disk(min_free_gb: float, disk_path: str) -> tuple[bool, str, float]:
    total, used, free = shutil.disk_usage(disk_path)
    free_gb = free / (1024**3)
    ok = free_gb >= min_free_gb
    return ok, f"Disk free: {free_gb:.2f}GB (threshold {min_free_gb:.2f}GB)", free_gb


def parse_nvidia_smi() -> tuple[bool, str, dict[str, float] | None]:
    try:
        cmd = [
            "nvidia-smi",
            "--query-gpu=memory.total,memory.free",
            "--format=csv,noheader,nounits",
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        first_line = result.stdout.strip().splitlines()[0]
        total_mb, free_mb = [float(x.strip()) for x in first_line.split(",")]
        return True, f"VRAM free: {free_mb:.0f}MB / {total_mb:.0f}MB", {"total_mb": total_mb, "free_mb": free_mb}
    except Exception as exc:  # noqa: BLE001
        return False, f"Unable to read VRAM via nvidia-smi: {exc}", None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RunPod health check for ComfyUI workflow readiness.")
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument("--skip-comfy-api", action="store_true", help="Skip API and node checks.")
    parser.add_argument(
        "--required-node",
        action="append",
        default=["InstantID", "IPAdapter FaceID", "Load LoRA"],
        help="Node class substring expected in /object_info.",
    )
    parser.add_argument(
        "--required-model",
        action="append",
        default=[
            "/workspace/runpod-slim/ComfyUI/models/checkpoints/realvisxl_v5.safetensors",
            "/workspace/runpod-slim/ComfyUI/models/controlnet/instantid-controlnet.safetensors",
            "/workspace/runpod-slim/ComfyUI/models/instantid/ip-adapter.bin",
            "/workspace/runpod-slim/ComfyUI/models/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin",
        ],
        help="Absolute path that must exist.",
    )
    parser.add_argument("--disk-path", default="/workspace")
    parser.add_argument("--min-free-disk-gb", type=float, default=20.0)
    parser.add_argument("--min-free-vram-mb", type=float, default=1024.0)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON summary.")
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    import requests

    checks: list[dict[str, Any]] = []

    if not args.skip_comfy_api:
        ok, msg, api_data = check_comfy_api(requests, args.comfy_url)
        checks.append({"name": "comfy_api", "ok": ok, "message": msg})

        ok_nodes, msg_nodes, _ = check_nodes(requests, args.comfy_url, args.required_node)
        checks.append({"name": "node_classes", "ok": ok_nodes, "message": msg_nodes})
    else:
        api_data = None
        checks.append({"name": "comfy_api", "ok": True, "message": "Skipped by flag"})
        checks.append({"name": "node_classes", "ok": True, "message": "Skipped by flag"})

    ok_models, msg_models, missing_models = check_models(args.required_model)
    checks.append(
        {
            "name": "model_files",
            "ok": ok_models,
            "message": msg_models,
            "missing": missing_models,
        }
    )

    ok_disk, msg_disk, free_gb = check_disk(args.min_free_disk_gb, args.disk_path)
    checks.append({"name": "disk", "ok": ok_disk, "message": msg_disk, "free_gb": free_gb})

    ok_vram, msg_vram, vram_data = parse_nvidia_smi()
    if ok_vram and vram_data is not None:
        ok_vram = vram_data["free_mb"] >= args.min_free_vram_mb
        msg_vram = (
            f"{msg_vram} (threshold {args.min_free_vram_mb:.0f}MB)"
            if ok_vram
            else f"{msg_vram} below threshold {args.min_free_vram_mb:.0f}MB"
        )
    checks.append({"name": "vram", "ok": ok_vram, "message": msg_vram, "data": vram_data})

    overall_ok = all(check["ok"] for check in checks)

    summary = {
        "overall_ok": overall_ok,
        "checks": checks,
        "system_stats": api_data,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        for item in checks:
            status = "PASS" if item["ok"] else "FAIL"
            print(f"[{status}] {item['name']}: {item['message']}")
        print("[PASS] overall" if overall_ok else "[FAIL] overall")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
