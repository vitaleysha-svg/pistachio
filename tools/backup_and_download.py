#!/usr/bin/env python3
"""Backup workflow artifacts and package them for download.

Artifacts:
- Workflow JSON files from common ComfyUI workflow dirs
- ComfyUI history snapshot from API (if reachable)
- LoRA file manifest (name + size + sha256)
- Custom node directory list
- Zipped bundle
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_workflows(comfy_root: Path, backup_root: Path) -> list[str]:
    candidates = [
        comfy_root / "user" / "default" / "workflows",
        comfy_root / "workflows",
    ]

    copied = []
    out_dir = backup_root / "workflows"
    out_dir.mkdir(parents=True, exist_ok=True)

    for source in candidates:
        if not source.exists():
            continue
        for workflow_file in sorted(source.rglob("*.json")):
            rel_name = workflow_file.name
            target = out_dir / rel_name
            shutil.copy2(workflow_file, target)
            copied.append(str(workflow_file))

    return copied


def fetch_history_snapshot(requests_mod, comfy_url: str, out_path: Path, timeout: int = 15) -> bool:
    try:
        response = requests_mod.get(comfy_url.rstrip("/") + "/history", timeout=timeout)
        response.raise_for_status()
        out_path.write_text(json.dumps(response.json(), indent=2), encoding="utf-8")
        return True
    except Exception:  # noqa: BLE001
        return False


def build_lora_manifest(lora_dir: Path) -> list[dict[str, Any]]:
    records = []
    if not lora_dir.exists():
        return records

    for path in sorted(lora_dir.glob("*.safetensors")):
        records.append(
            {
                "filename": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return records


def build_custom_nodes_manifest(custom_nodes_dir: Path) -> list[str]:
    if not custom_nodes_dir.exists():
        return []
    return sorted([p.name for p in custom_nodes_dir.iterdir() if p.is_dir()])


def create_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                zf.write(file_path, arcname=file_path.relative_to(source_dir))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backup ComfyUI workflow and model metadata for download.")
    parser.add_argument("--comfy-root", type=Path, default=Path("/workspace/runpod-slim/ComfyUI"))
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/backups"))
    parser.add_argument("--name-prefix", default="pistachio_backup")
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    import requests

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_root = args.output_dir / f"{args.name_prefix}_{timestamp}"
    backup_root.mkdir(parents=True, exist_ok=True)

    workflow_sources = copy_workflows(args.comfy_root, backup_root)

    history_path = backup_root / "api_history_snapshot.json"
    history_ok = fetch_history_snapshot(requests, args.comfy_url, history_path)

    lora_manifest = build_lora_manifest(args.comfy_root / "models" / "loras")
    (backup_root / "lora_manifest.json").write_text(json.dumps(lora_manifest, indent=2), encoding="utf-8")

    custom_nodes = build_custom_nodes_manifest(args.comfy_root / "custom_nodes")
    (backup_root / "custom_nodes.json").write_text(json.dumps(custom_nodes, indent=2), encoding="utf-8")

    metadata = {
        "timestamp": timestamp,
        "comfy_root": str(args.comfy_root),
        "workflow_files_copied": workflow_sources,
        "history_snapshot_saved": history_ok,
        "lora_count": len(lora_manifest),
        "custom_node_count": len(custom_nodes),
    }
    (backup_root / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    zip_path = args.output_dir / f"{args.name_prefix}_{timestamp}.zip"
    create_zip(backup_root, zip_path)

    print(f"[done] backup_folder={backup_root}")
    print(f"[done] backup_zip={zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
