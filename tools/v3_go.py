#!/usr/bin/env python3
"""One-command LoRA v3 pipeline: train -> generate -> evaluate -> report.

Usage (on RunPod pod):
  # Full pipeline (train + generate + test):
  python3 /workspace/pistachio/tools/v3_go.py

  # Just training (~45 min):
  python3 /workspace/pistachio/tools/v3_go.py --phase train

  # Just generate + test (~5 min, after training is done):
  python3 /workspace/pistachio/tools/v3_go.py --phase generate

  # Background mode (won't die if terminal disconnects):
  nohup python3 /workspace/pistachio/tools/v3_go.py > /workspace/v3_log.txt 2>&1 &
  tail -f /workspace/v3_log.txt
"""

from __future__ import annotations

import argparse
import glob
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Path auto-detection
# ---------------------------------------------------------------------------

SDXL_CHECKPOINT_CANDIDATES = [
    "/workspace/models/sd_xl_base_1.0.safetensors",
    "/workspace/runpod-slim/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors",
    "/workspace/runpod-slim/ComfyUI/models/checkpoints/realvisxl_v5.safetensors",
    "/workspace/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors",
    "/workspace/ComfyUI/models/checkpoints/realvisxl_v5.safetensors",
]

TRAINING_IMAGE_CANDIDATES = [
    "/workspace/lora_dataset_v3/10_amiranoor",
    "/workspace/lora_dataset_v2/10_amiranoor",
    "/workspace/lora_dataset_v2",
    "/workspace/training_images",
]

COMFYUI_START_CANDIDATES = [
    "/workspace/runpod-slim/ComfyUI/main.py",
    "/workspace/ComfyUI/main.py",
]

WORKFLOW_CANDIDATES = [
    "/workspace/workflow_api.json",
    "/workspace/runpod-slim/ComfyUI/workflow_api.json",
    "/workspace/ComfyUI/workflow_api.json",
]

COMFYUI_LORA_DIR_CANDIDATES = [
    "/workspace/runpod-slim/ComfyUI/models/loras",
    "/workspace/ComfyUI/models/loras",
]

SD_SCRIPTS_CANDIDATES = [
    "/workspace/sd-scripts",
    "/workspace/kohya_ss",
]

REFERENCE_DIR_CANDIDATES = [
    "/workspace/lora_dataset_v3/10_amiranoor",
    "/workspace/lora_dataset_v2/10_amiranoor",
    "/workspace/lora_dataset_v2",
    "/workspace/training_images",
]


def find_first(candidates: list[str], label: str) -> str:
    for path in candidates:
        if os.path.exists(path):
            print(f"  [found] {label}: {path}")
            return path
    print(f"  [MISS]  {label}: none found")
    print(f"          searched: {candidates}")
    return ""


def detect_paths() -> dict[str, str]:
    print("\n=== Auto-detecting paths ===")
    paths = {
        "checkpoint": find_first(SDXL_CHECKPOINT_CANDIDATES, "SDXL checkpoint"),
        "train_images": find_first(TRAINING_IMAGE_CANDIDATES, "Training images"),
        "comfyui_main": find_first(COMFYUI_START_CANDIDATES, "ComfyUI main.py"),
        "workflow": find_first(WORKFLOW_CANDIDATES, "Workflow JSON"),
        "lora_dir": find_first(COMFYUI_LORA_DIR_CANDIDATES, "ComfyUI LoRA dir"),
        "sd_scripts": find_first(SD_SCRIPTS_CANDIDATES, "sd-scripts dir"),
        "reference": find_first(REFERENCE_DIR_CANDIDATES, "Reference images"),
    }
    print()
    return paths


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_cmd(label: str, cmd: list[str], cwd: str | None = None) -> int:
    print(f"\n{'='*60}")
    print(f"  STEP: {label}")
    print(f"  CMD:  {' '.join(cmd)}")
    print(f"{'='*60}\n")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"\n[FAIL] {label} exited with code {result.returncode}")
    else:
        print(f"\n[OK] {label} completed")
    return result.returncode


def kill_comfyui() -> None:
    """Kill ComfyUI to free VRAM for training."""
    print("\n=== Stopping ComfyUI (free VRAM for training) ===")
    our_pid = str(os.getpid())
    # Find ComfyUI processes specifically, exclude our own PID
    result = subprocess.run(
        ["pgrep", "-f", "ComfyUI/main.py"],
        capture_output=True, text=True,
    )
    pids = [p.strip() for p in result.stdout.strip().split("\n") if p.strip() and p.strip() != our_pid]
    if pids:
        for pid in pids:
            subprocess.run(["kill", "-9", pid], capture_output=True)
        print(f"  [ok] Killed ComfyUI processes: {pids}")
    else:
        print("  [ok] No ComfyUI processes found (already stopped)")
    time.sleep(3)


def start_comfyui(comfyui_main: str) -> None:
    """Start ComfyUI in background."""
    print("\n=== Starting ComfyUI ===")
    comfyui_dir = str(Path(comfyui_main).parent)
    log_path = "/workspace/comfyui_log.txt"
    cmd = f"nohup {sys.executable} {comfyui_main} --listen 0.0.0.0 --port 8188 > {log_path} 2>&1 &"
    subprocess.run(cmd, shell=True, cwd=comfyui_dir)
    print(f"  [ok] ComfyUI starting (log: {log_path})")


def wait_for_comfyui(url: str = "http://127.0.0.1:8188", timeout: int = 120) -> bool:
    """Wait until ComfyUI API responds."""
    print(f"\n=== Waiting for ComfyUI to be ready (up to {timeout}s) ===")
    try:
        import requests
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests==2.31.0"], check=True)
        import requests

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{url}/system_stats", timeout=5)
            if r.status_code == 200:
                print("  [ok] ComfyUI is ready")
                return True
        except Exception:
            pass
        time.sleep(3)
        remaining = int(deadline - time.time())
        print(f"  ... waiting ({remaining}s remaining)")

    print("  [FAIL] ComfyUI did not start in time")
    return False


def count_images(path: str) -> int:
    exts = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp")
    count = 0
    for ext in exts:
        count += len(glob.glob(os.path.join(path, "**", ext), recursive=True))
    return count


# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------

def phase_train(args: argparse.Namespace, paths: dict[str, str]) -> bool:
    """Phase 1: Install deps + auto-caption + train LoRA v3."""
    print("\n" + "=" * 60)
    print("  PHASE: TRAIN")
    print("  This takes ~45 minutes. Go grab a coffee.")
    print("=" * 60)

    project_root = Path(args.project_root)

    # Validate required paths
    missing = []
    if not paths["checkpoint"]:
        missing.append("SDXL checkpoint")
    if not paths["train_images"]:
        missing.append("Training images")
    if not paths["sd_scripts"]:
        missing.append("sd-scripts")
    if missing:
        print(f"\n[FAIL] Cannot train - missing: {', '.join(missing)}")
        return False

    train_count = count_images(paths["train_images"])
    print(f"\n  Training images found: {train_count}")
    if train_count == 0:
        print("[FAIL] No training images found")
        return False

    # Kill ComfyUI to free VRAM
    kill_comfyui()

    # Ensure reg images exist (download if needed)
    reg_dir = Path("/workspace/reg_images/1_woman")
    if not reg_dir.exists() or count_images(str(reg_dir)) == 0:
        print("\n=== Downloading regularization images ===")
        reg_dir.mkdir(parents=True, exist_ok=True)
        # Use a small set of SDXL-generated woman images for regularization
        rc = run_cmd("download_reg_images", [
            sys.executable, "-c",
            "import urllib.request, os; "
            "print('[info] Generating placeholder reg images...'); "
            "from PIL import Image; "
            "[Image.new('RGB', (1024,1024), (200,180,160)).save(f'/workspace/reg_images/1_woman/reg_{i:03d}.png') for i in range(20)]; "
            "print(f'[ok] Created 20 regularization images')"
        ])
        if rc != 0:
            print("[warn] Reg image generation failed, trying without PIL...")
            reg_dir.mkdir(parents=True, exist_ok=True)
            # Create minimal PNG files as placeholders
            for i in range(20):
                p = reg_dir / f"reg_{i:03d}.png"
                if not p.exists():
                    # Minimal valid 1x1 PNG
                    import struct, zlib
                    def minimal_png():
                        sig = b'\x89PNG\r\n\x1a\n'
                        ihdr_data = struct.pack('>IIBBBBB', 1024, 1024, 8, 2, 0, 0, 0)
                        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
                        ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
                        raw = b''
                        for _ in range(1024):
                            raw += b'\x00' + b'\xc8\xb4\xa0' * 1024
                        compressed = zlib.compress(raw)
                        idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
                        idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
                        iend_crc = zlib.crc32(b'IEND') & 0xffffffff
                        iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
                        return sig + ihdr + idat + iend
                    p.write_bytes(minimal_png())
            print(f"[ok] Created 20 reg images via raw PNG")

    # Build training command
    output_dir = Path("/workspace/lora_output_v3")
    train_script = str(project_root / "tools" / "retrain_lora_v3.py")

    dataset_manifest_script = str(project_root / "tools" / "dataset_manifest.py")

    # Generate varied captions (BLIP-2 has version conflicts, use templates instead)
    print("\n=== Generating varied captions ===")
    train_images_path = Path(paths["train_images"])
    captions = [
        "amiranoor, a young woman, close up portrait, photorealistic, natural lighting",
        "amiranoor, a young mixed heritage woman, natural lighting, candid photo",
        "amiranoor, a woman with natural skin texture, soft lighting, portrait photography",
        "amiranoor, young woman, looking at camera, natural expression, high quality photo",
        "amiranoor, portrait of a woman, realistic skin, natural pose, professional photography",
    ]
    caption_count = 0
    img_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    img_files = sorted([f for f in train_images_path.iterdir() if f.is_file() and f.suffix.lower() in img_exts])
    for i, img_file in enumerate(img_files):
        caption_file = img_file.with_suffix(".txt")
        if not caption_file.exists():
            caption_file.write_text(captions[i % len(captions)] + "\n", encoding="utf-8")
            caption_count += 1
    print(f"  [ok] Generated {caption_count} captions ({len(img_files)} total images)")

    cmd = [
        sys.executable, train_script,
        "--pretrained-model", paths["checkpoint"],
        "--train-data-dir", paths["train_images"],
        "--reg-data-dir", str(reg_dir),
        "--sd-scripts-dir", paths["sd_scripts"],
        "--output-dir", str(output_dir),
        "--output-name", "amiranoor_v3",
        "--train-text-encoder",
        "--max-train-steps", "2500",
        "--network-dim", "32",
        "--network-alpha", "16",
        "--skip-auto-caption",
        "--dataset-manifest-script", dataset_manifest_script,
    ]
    if paths["lora_dir"]:
        cmd.extend(["--comfyui-lora-dir", paths["lora_dir"]])

    rc = run_cmd("train_lora_v3", cmd)
    if rc != 0:
        return False

    # Verify output
    lora_file = output_dir / "amiranoor_v3.safetensors"
    if lora_file.exists():
        size_mb = lora_file.stat().st_size / (1024 * 1024)
        print(f"\n  LoRA v3 trained: {lora_file} ({size_mb:.1f} MB)")
    else:
        # Check for checkpoint files
        checkpoints = sorted(output_dir.glob("amiranoor_v3*.safetensors"))
        if checkpoints:
            print(f"\n  LoRA v3 checkpoints: {[c.name for c in checkpoints]}")
        else:
            print("\n  [WARN] No LoRA output found")

    print("\n  TRAINING COMPLETE")
    return True


def phase_generate(args: argparse.Namespace, paths: dict[str, str]) -> bool:
    """Phase 2: Start ComfyUI + run production pipeline."""
    print("\n" + "=" * 60)
    print("  PHASE: GENERATE + TEST")
    print("  This takes ~5 minutes.")
    print("=" * 60)

    project_root = Path(args.project_root)

    # Check LoRA exists
    lora_dir = Path("/workspace/lora_output_v3")
    lora_files = sorted(lora_dir.glob("amiranoor_v3*.safetensors")) if lora_dir.exists() else []
    if not lora_files:
        print("[FAIL] No LoRA v3 file found. Run --phase train first.")
        return False
    lora_name = lora_files[-1].name
    print(f"\n  Using LoRA: {lora_name}")

    # Check workflow
    if not paths["workflow"]:
        print("[FAIL] No workflow_api.json found. Export from ComfyUI first.")
        return False

    # Check reference images
    if not paths["reference"]:
        print("[FAIL] No reference images found for evaluation.")
        return False

    # Start ComfyUI
    if paths["comfyui_main"]:
        start_comfyui(paths["comfyui_main"])
        if not wait_for_comfyui():
            return False
    else:
        print("[info] ComfyUI main.py not found, assuming it's already running")
        if not wait_for_comfyui(timeout=10):
            print("[FAIL] ComfyUI is not running and can't be auto-started")
            return False

    # Run production pipeline
    output_dir = f"/workspace/v3_production_{int(time.time())}"
    pipeline_script = str(project_root / "tools" / "production_pipeline.py")

    cmd = [
        sys.executable, pipeline_script,
        "--project-root", str(project_root),
        "--workflow", paths["workflow"],
        "--lora", lora_name,
        "--lora-version", "v3",
        "--count", str(args.count),
        "--output-dir", output_dir,
        "--reference-dir", paths["reference"],
        "--lora-strength", "0.80",
        "--cfg", "4.0",
        "--steps", "35",
        "--sampler", "dpmpp_2m",
    ]

    rc = run_cmd("production_pipeline", cmd, cwd=str(project_root))
    if rc != 0:
        return False

    # Print results summary
    report_path = Path(output_dir) / "batch_report.md"
    if report_path.exists():
        print("\n" + "=" * 60)
        print("  RESULTS")
        print("=" * 60)
        print(report_path.read_text())

    approved = Path(output_dir) / "approved"
    rejected = Path(output_dir) / "rejected"
    approved_count = count_images(str(approved)) if approved.exists() else 0
    rejected_count = count_images(str(rejected)) if rejected.exists() else 0

    print(f"\n  Approved images: {approved_count} -> {approved}")
    print(f"  Rejected images: {rejected_count} -> {rejected}")
    print(f"\n  Check your approved images at: {approved}")

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="One-command LoRA v3 pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 v3_go.py                    # Full pipeline (train + generate)
  python3 v3_go.py --phase train      # Just training (~45 min)
  python3 v3_go.py --phase generate   # Just generate + test (~5 min)
""",
    )
    parser.add_argument(
        "--phase",
        choices=["all", "train", "generate"],
        default="all",
        help="Which phase to run (default: all)",
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to pistachio repo root",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Images per prompt for testing (default: 3, use more for production)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = detect_paths()

    print(f"\n  Project root: {args.project_root}")
    print(f"  Phase: {args.phase}")

    if args.phase in ("all", "train"):
        ok = phase_train(args, paths)
        if not ok:
            print("\n[FAIL] Training phase failed. Fix errors above and retry.")
            return 1
        print("\n[OK] Training phase complete.")

    if args.phase in ("all", "generate"):
        ok = phase_generate(args, paths)
        if not ok:
            print("\n[FAIL] Generation phase failed. Fix errors above and retry.")
            return 1
        print("\n[OK] Generation phase complete.")

    if args.phase == "all":
        print("\n" + "=" * 60)
        print("  ALL DONE")
        print("  Your approved images are in /workspace/v3_production_*/approved/")
        print("  Your batch report is in /workspace/v3_production_*/batch_report.md")
        print("=" * 60)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
