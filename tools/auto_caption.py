#!/usr/bin/env python3
"""Auto-caption LoRA training images with BLIP-2.

Example:
  python3 auto_caption.py \
    --input-dir /workspace/lora_dataset_v3/10_amiranoor \
    --trigger-word amiranoor \
    --overwrite
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
DEFAULT_MODEL = "Salesforce/blip2-flan-t5-xl"

REQUIRED_PACKAGES = {
    "transformers": "4.38.2",
    "huggingface_hub": "0.21.4",
    "Pillow": "10.2.0",
    "accelerate": "0.27.2",
}


def ensure_dependencies(skip_install: bool) -> None:
    missing = []
    for package, version in REQUIRED_PACKAGES.items():
        import_name = "PIL" if package == "Pillow" else package
        try:
            __import__(import_name)
        except ImportError:
            missing.append(f"{package}=={version}")

    if not missing:
        return
    if skip_install:
        raise RuntimeError(
            "Missing required packages: "
            + ", ".join(missing)
            + ". Re-run without --skip-install to auto-install."
        )

    cmd = [sys.executable, "-m", "pip", "install", "--no-input", *missing]
    print("[deps] Installing:", " ".join(missing))
    subprocess.run(cmd, check=True)


def iter_images(input_dir: Path, recursive: bool) -> Iterable[Path]:
    if recursive:
        candidates = input_dir.rglob("*")
    else:
        candidates = input_dir.glob("*")
    for path in sorted(candidates):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def normalize_caption(trigger_word: str, raw_caption: str) -> str:
    cleaned = re.sub(r"\s+", " ", raw_caption).strip(" ,.;:\t\n\r")
    if not cleaned:
        cleaned = "a portrait photo"
    cleaned = re.sub(rf"(?i)^\b{re.escape(trigger_word)}\b\s*,?\s*", "", cleaned).strip()
    cleaned = cleaned[0].lower() + cleaned[1:] if cleaned else cleaned
    return f"{trigger_word}, {cleaned}"


def load_model(model_id: str, device: str):
    import torch
    from transformers import Blip2ForConditionalGeneration, Blip2Processor

    dtype = torch.float16 if device.startswith("cuda") else torch.float32
    processor = Blip2Processor.from_pretrained(model_id)
    model = Blip2ForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    )
    model.to(device)
    model.eval()
    return processor, model, dtype


def generate_caption(processor, model, dtype, device: str, image_path: Path, prompt: str, max_new_tokens: int) -> str:
    import torch
    from PIL import Image

    image = Image.open(image_path).convert("RGB")
    model_inputs = processor(images=image, text=prompt, return_tensors="pt")
    model_inputs = {k: v.to(device) for k, v in model_inputs.items()}
    if "pixel_values" in model_inputs:
        model_inputs["pixel_values"] = model_inputs["pixel_values"].to(dtype)

    with torch.inference_mode():
        output = model.generate(**model_inputs, max_new_tokens=max_new_tokens)

    return processor.batch_decode(output, skip_special_tokens=True)[0].strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate BLIP-2 captions for LoRA images.")
    parser.add_argument("--input-dir", type=Path, required=True, help="Directory with source images.")
    parser.add_argument("--trigger-word", default="amiranoor", help="Identity token prepended to every caption.")
    parser.add_argument("--model-id", default=DEFAULT_MODEL, help="BLIP-2 model id.")
    parser.add_argument(
        "--caption-prompt",
        default="Describe this image in detailed photographic terms: person, pose, expression, clothing, setting, camera angle, and lighting.",
        help="Prompt fed into BLIP-2.",
    )
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--suffix", default=".txt", help="Caption file extension.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing caption files.")
    parser.add_argument("--recursive", action="store_true", help="Search recursively for images.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--skip-install", action="store_true", help="Disable pip auto-install for missing deps.")
    return parser.parse_args()


def resolve_device(raw_device: str) -> str:
    if raw_device != "auto":
        return raw_device
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def main() -> int:
    args = parse_args()
    ensure_dependencies(skip_install=args.skip_install)

    if not args.input_dir.exists() or not args.input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {args.input_dir}")

    device = resolve_device(args.device)
    print(f"[init] device={device} model={args.model_id}")
    processor, model, dtype = load_model(args.model_id, device)

    written = 0
    skipped = 0
    errors = 0

    for image_path in iter_images(args.input_dir, args.recursive):
        caption_path = image_path.with_suffix(args.suffix)
        if caption_path.exists() and not args.overwrite:
            skipped += 1
            continue

        try:
            raw_caption = generate_caption(
                processor=processor,
                model=model,
                dtype=dtype,
                device=device,
                image_path=image_path,
                prompt=args.caption_prompt,
                max_new_tokens=args.max_new_tokens,
            )
            caption = normalize_caption(args.trigger_word, raw_caption)
            if args.dry_run:
                print(f"[dry-run] {caption_path}: {caption}")
            else:
                caption_path.write_text(caption + "\n", encoding="utf-8")
                print(f"[ok] {caption_path.name}: {caption}")
            written += 1
        except Exception as exc:  # noqa: BLE001
            errors += 1
            print(f"[error] {image_path.name}: {exc}")

    print(
        f"[done] written={written} skipped={skipped} errors={errors} "
        f"input_dir={args.input_dir}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
