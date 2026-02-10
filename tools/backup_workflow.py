#!/usr/bin/env python3
"""Lightweight workflow backup helper for ComfyUI.

This exports API history and local workflow JSON files into a timestamped folder.
Use backup_and_download.py for full zipped backup.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REQUIRED_PACKAGES = {"requests": "2.31.0"}


def ensure_dependencies(skip_install: bool) -> None:
    try:
        __import__("requests")
    except ImportError:
        if skip_install:
            raise RuntimeError("Missing dependency: requests==2.31.0")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-input", f"requests=={REQUIRED_PACKAGES['requests']}"]
        , check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backup current ComfyUI workflow artifacts.")
    parser.add_argument("--comfy-url", default="http://127.0.0.1:8188")
    parser.add_argument("--comfy-root", type=Path, default=Path("/workspace/runpod-slim/ComfyUI"))
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/workflows"))
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    import requests

    stamp = time.strftime("%Y%m%d-%H%M%S")
    dest = args.output_dir / f"workflow-backup-{stamp}"
    dest.mkdir(parents=True, exist_ok=True)

    # Local workflow files
    for source in [args.comfy_root / "user" / "default" / "workflows", args.comfy_root / "workflows"]:
        if source.exists():
            for json_file in source.rglob("*.json"):
                target = dest / json_file.name
                target.write_text(json_file.read_text(encoding="utf-8"), encoding="utf-8")

    # API snapshots
    for endpoint in ["/history", "/queue", "/object_info"]:
        try:
            response = requests.get(args.comfy_url.rstrip("/") + endpoint, timeout=20)
            response.raise_for_status()
            (dest / f"api_{endpoint.strip('/').replace('/', '_')}.json").write_text(
                json.dumps(response.json(), indent=2),
                encoding="utf-8",
            )
        except Exception as exc:  # noqa: BLE001
            (dest / f"api_{endpoint.strip('/').replace('/', '_')}.error.txt").write_text(str(exc), encoding="utf-8")

    print(f"[done] workflow backup saved to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
