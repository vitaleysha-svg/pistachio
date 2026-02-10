#!/usr/bin/env python3
"""Download regularization images for LoRA identity training.

Downloads portrait photos from Unsplash source endpoint by query terms.
No API key required.
"""

from __future__ import annotations

import argparse
import random
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

REQUIRED_PACKAGES = {
    "Pillow": "10.2.0",
}

QUERIES = [
    "portrait woman",
    "female street portrait",
    "studio portrait woman",
    "natural light woman portrait",
    "candid woman photo",
    "fashion portrait woman",
]


def ensure_dependencies(skip_install: bool) -> None:
    try:
        __import__("PIL")
    except ImportError:
        if skip_install:
            raise RuntimeError("Missing dependency: Pillow==10.2.0")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-input", f"Pillow=={REQUIRED_PACKAGES['Pillow']}"]
        , check=True)


def fetch_image(url: str, timeout: int = 30) -> bytes:
    request = Request(url, headers={"User-Agent": "pistachio-reg-image-downloader/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download regularization images from Unsplash source endpoint.")
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/reg_images/1_woman"))
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    from PIL import Image
    import io

    args.output_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    attempts = 0
    max_attempts = args.count * 4

    while downloaded < args.count and attempts < max_attempts:
        attempts += 1
        query = random.choice(QUERIES)
        sig = random.randint(0, 1_000_000)
        source_url = (
            f"https://source.unsplash.com/{args.width}x{args.height}/?{quote(query)}&sig={sig}"
        )

        try:
            raw = fetch_image(source_url)
            image = Image.open(io.BytesIO(raw)).convert("RGB")
            out_path = args.output_dir / f"reg_{downloaded + 1:04d}.jpg"
            image.save(out_path, format="JPEG", quality=95)
            downloaded += 1
            if downloaded % 10 == 0 or downloaded == args.count:
                print(f"[ok] downloaded {downloaded}/{args.count}")
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] attempt={attempts} failed: {exc}")

    print(f"[done] saved={downloaded} requested={args.count} output_dir={args.output_dir}")
    return 0 if downloaded >= args.count else 1


if __name__ == "__main__":
    raise SystemExit(main())
