#!/usr/bin/env python3
"""Create and compare dataset manifests for LoRA training reproducibility."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_dimensions(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image

        with Image.open(path) as image:
            return int(image.width), int(image.height)
    except Exception:  # noqa: BLE001
        return (0, 0)


def iter_images(dataset_dir: Path) -> list[Path]:
    images: list[Path] = []
    for candidate in sorted(dataset_dir.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(candidate)
    return images


def create_manifest(dataset_dir: Path, caption_extension: str = ".txt") -> dict[str, Any]:
    dataset_dir = dataset_dir.resolve()
    images = iter_images(dataset_dir)

    items: list[dict[str, Any]] = []
    caption_counter: Counter[str] = Counter()
    resolutions: set[str] = set()
    total_caption_files = 0
    size_sum = 0

    for image_path in images:
        rel_image = image_path.relative_to(dataset_dir).as_posix()
        caption_path = image_path.with_suffix(caption_extension)
        caption_rel = caption_path.relative_to(dataset_dir).as_posix() if caption_path.exists() else None
        caption_text = caption_path.read_text(encoding="utf-8", errors="ignore").strip() if caption_path.exists() else ""
        caption_sha = sha256_file(caption_path) if caption_path.exists() else None
        dimensions = image_dimensions(image_path)
        resolution_label = f"{dimensions[0]}x{dimensions[1]}"
        resolutions.add(resolution_label)

        if caption_path.exists():
            total_caption_files += 1
        if caption_text:
            caption_counter[caption_text] += 1

        file_size = image_path.stat().st_size
        size_sum += file_size

        items.append(
            {
                "filename": rel_image,
                "sha256": sha256_file(image_path),
                "size_bytes": file_size,
                "dimensions": [dimensions[0], dimensions[1]],
                "caption_file": caption_rel,
                "caption_text": caption_text or None,
                "caption_sha256": caption_sha,
            }
        )

    mean_size = float(size_sum) / len(items) if items else 0.0
    manifest = {
        "manifest_version": 1,
        "created": now_iso(),
        "dataset_dir": str(dataset_dir),
        "total_images": len(items),
        "total_captions": total_caption_files,
        "images": items,
        "summary": {
            "unique_captions": len(caption_counter),
            "caption_distribution": dict(caption_counter),
            "mean_image_size_bytes": mean_size,
            "resolution_set": sorted(resolutions),
        },
    }
    return manifest


def compare_manifests(old_manifest: dict[str, Any], new_manifest: dict[str, Any]) -> dict[str, Any]:
    old_items = {item["filename"]: item for item in old_manifest.get("images", [])}
    new_items = {item["filename"]: item for item in new_manifest.get("images", [])}

    old_names = set(old_items.keys())
    new_names = set(new_items.keys())

    added = sorted(new_names - old_names)
    removed = sorted(old_names - new_names)
    shared = sorted(old_names & new_names)

    changed_images: list[str] = []
    changed_captions: list[str] = []
    changed_resolutions: list[str] = []

    for name in shared:
        old_item = old_items[name]
        new_item = new_items[name]
        if old_item.get("sha256") != new_item.get("sha256"):
            changed_images.append(name)
        if old_item.get("caption_sha256") != new_item.get("caption_sha256"):
            changed_captions.append(name)
        if old_item.get("dimensions") != new_item.get("dimensions"):
            changed_resolutions.append(name)

    old_res = set(old_manifest.get("summary", {}).get("resolution_set", []))
    new_res = set(new_manifest.get("summary", {}).get("resolution_set", []))

    return {
        "older_manifest_created": old_manifest.get("created"),
        "newer_manifest_created": new_manifest.get("created"),
        "images_added": added,
        "images_removed": removed,
        "images_content_changed": changed_images,
        "captions_changed": changed_captions,
        "resolution_changed_images": changed_resolutions,
        "resolution_set_added": sorted(new_res - old_res),
        "resolution_set_removed": sorted(old_res - new_res),
        "counts": {
            "added": len(added),
            "removed": len(removed),
            "content_changed": len(changed_images),
            "captions_changed": len(changed_captions),
            "resolution_changed": len(changed_resolutions),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or compare dataset manifests.")
    parser.add_argument("--dataset-dir", type=Path, help="Dataset directory containing images and captions.")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON file for manifest.")
    parser.add_argument("--caption-extension", default=".txt")
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("OLDER_MANIFEST", "NEWER_MANIFEST"),
        type=Path,
        default=None,
        help="Compare two manifest JSON files.",
    )
    parser.add_argument("--comparison-output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.compare:
        older_path, newer_path = [path.resolve() for path in args.compare]
        if not older_path.exists() or not newer_path.exists():
            raise FileNotFoundError(f"Manifest file missing: {older_path} or {newer_path}")

        older_manifest = json.loads(older_path.read_text(encoding="utf-8"))
        newer_manifest = json.loads(newer_path.read_text(encoding="utf-8"))
        result = compare_manifests(older_manifest, newer_manifest)

        if args.comparison_output:
            args.comparison_output.parent.mkdir(parents=True, exist_ok=True)
            args.comparison_output.write_text(json.dumps(result, indent=2), encoding="utf-8")

        print(json.dumps(result, indent=2))
        return 0

    if not args.dataset_dir:
        raise SystemExit("Either --dataset-dir or --compare must be provided.")
    dataset_dir = args.dataset_dir.resolve()
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    manifest = create_manifest(dataset_dir=dataset_dir, caption_extension=args.caption_extension)
    output_path = args.output.resolve() if args.output else dataset_dir / "manifest.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[ok] wrote manifest: {output_path}")
    print(json.dumps({"total_images": manifest["total_images"], "total_captions": manifest["total_captions"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

