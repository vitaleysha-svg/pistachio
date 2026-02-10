#!/usr/bin/env python3
"""Heuristic skin realism evaluation for generated images."""

from __future__ import annotations

import argparse
import importlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from load_thresholds import load_thresholds

REQUIRED_PACKAGES = {
    "numpy": "1.26.4",
    "opencv-python-headless": "4.9.0.80",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def ensure_dependencies(skip_install: bool) -> None:
    missing: list[str] = []
    import_names = {"opencv-python-headless": "cv2"}
    for package, version in REQUIRED_PACKAGES.items():
        import_name = import_names.get(package, package)
        try:
            importlib.import_module(import_name)
        except Exception:  # noqa: BLE001
            missing.append(f"{package}=={version}")

    if not missing:
        return
    if skip_install:
        raise RuntimeError("Missing dependencies: " + ", ".join(missing))
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-input", *missing], check=True)


def iter_images(path: Path) -> list[Path]:
    images: list[Path] = []
    for candidate in sorted(path.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(candidate)
    return images


def skin_mask(image):
    import cv2
    import numpy as np

    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    return cv2.inRange(ycrcb, lower, upper)


def laplacian_variance(image) -> float:
    import cv2

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())


def skin_histogram(image) -> tuple[Any, float]:
    import cv2
    import numpy as np

    mask = skin_mask(image)
    skin_ratio = float(np.count_nonzero(mask)) / float(mask.size)
    if skin_ratio < 0.01:
        # If face coverage is tiny, evaluate color distribution on full image.
        mask = None
        skin_ratio = 0.0

    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    hist = cv2.calcHist([ycrcb], [1, 2], mask, [32, 32], [0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist, skin_ratio


def texture_score(generated_lap: float, reference_lap: float) -> float:
    if reference_lap <= 0:
        return 0.0
    ratio = max(generated_lap / reference_lap, 1e-6)
    # 1.0 at ratio=1, decreases as generated sharpness diverges from reference.
    score = 1.0 - abs(math.log(ratio, 2.0)) / 2.0
    return max(0.0, min(1.0, score))


def color_score(generated_hist, reference_hist) -> float:
    import cv2

    distance = float(cv2.compareHist(generated_hist, reference_hist, cv2.HISTCMP_BHATTACHARYYA))
    return max(0.0, 1.0 - min(1.0, distance))


def evaluate_skin_realism(
    generated_dir: Path,
    reference_dir: Path,
    threshold: float = 0.60,
    texture_threshold: float = 0.60,
    color_threshold: float = 0.55,
    skip_install: bool = False,
) -> dict[str, Any]:
    ensure_dependencies(skip_install=skip_install)

    import cv2
    import numpy as np

    generated_images = iter_images(generated_dir)
    reference_images = iter_images(reference_dir)
    if not generated_images:
        raise RuntimeError(f"No generated images found in: {generated_dir}")
    if not reference_images:
        raise RuntimeError(f"No reference images found in: {reference_dir}")

    ref_laplacians: list[float] = []
    ref_hists: list[Any] = []

    for ref_path in reference_images:
        ref_img = cv2.imread(str(ref_path))
        if ref_img is None:
            continue
        ref_laplacians.append(laplacian_variance(ref_img))
        ref_hist, _ = skin_histogram(ref_img)
        ref_hists.append(ref_hist)

    if not ref_laplacians or not ref_hists:
        raise RuntimeError("Could not derive reference skin metrics.")

    reference_lap = float(np.median(np.array(ref_laplacians)))
    reference_hist = np.mean(np.stack(ref_hists, axis=0), axis=0)
    reference_hist = cv2.normalize(reference_hist, reference_hist).flatten()

    per_image: list[dict[str, Any]] = []
    for image_path in generated_images:
        image = cv2.imread(str(image_path))
        if image is None:
            continue

        lap = laplacian_variance(image)
        hist, skin_ratio = skin_histogram(image)
        tex_score = texture_score(lap, reference_lap)
        col_score = color_score(hist, reference_hist)
        overall = 0.55 * tex_score + 0.45 * col_score

        per_image.append(
            {
                "image": str(image_path),
                "laplacian_variance": lap,
                "skin_pixel_ratio": skin_ratio,
                "texture_score": tex_score,
                "color_naturalness_score": col_score,
                "overall_realism_score": overall,
            }
        )

    if not per_image:
        raise RuntimeError("No valid generated images could be evaluated.")

    texture_mean = sum(item["texture_score"] for item in per_image) / len(per_image)
    color_mean = sum(item["color_naturalness_score"] for item in per_image) / len(per_image)
    overall_mean = sum(item["overall_realism_score"] for item in per_image) / len(per_image)
    texture_pass = texture_mean >= texture_threshold
    color_pass = color_mean >= color_threshold
    overall_pass = overall_mean >= threshold

    return {
        "generated_dir": str(generated_dir),
        "reference_dir": str(reference_dir),
        "threshold": threshold,
        "texture_threshold": texture_threshold,
        "color_naturalness_threshold": color_threshold,
        "images_evaluated": len(per_image),
        "texture_score_mean": texture_mean,
        "color_naturalness_score_mean": color_mean,
        "overall_realism_score_mean": overall_mean,
        "texture_pass": texture_pass,
        "color_naturalness_pass": color_pass,
        "overall_pass": overall_pass,
        "pass": texture_pass and color_pass and overall_pass,
        "per_image": per_image,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate skin texture and color realism against references.")
    parser.add_argument("--generated", type=Path, required=True, help="Directory of generated images.")
    parser.add_argument("--reference", type=Path, required=True, help="Directory of reference images.")
    parser.add_argument("--threshold", type=float, default=None, help="Overall realism pass threshold.")
    parser.add_argument("--texture-threshold", type=float, default=None)
    parser.add_argument("--color-threshold", type=float, default=None)
    parser.add_argument("--output-json", type=Path, default=None)
    parser.add_argument("--fail-on-threshold", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    thresholds = load_thresholds(project_root=Path.cwd())
    skin_policy = thresholds["skin_realism"]
    overall_threshold = (
        args.threshold if args.threshold is not None else float(skin_policy["overall_pass_threshold"])
    )
    texture_threshold = (
        args.texture_threshold
        if args.texture_threshold is not None
        else float(skin_policy["texture_pass_threshold"])
    )
    color_threshold = (
        args.color_threshold
        if args.color_threshold is not None
        else float(skin_policy["color_naturalness_pass_threshold"])
    )

    result = evaluate_skin_realism(
        generated_dir=args.generated,
        reference_dir=args.reference,
        threshold=overall_threshold,
        texture_threshold=texture_threshold,
        color_threshold=color_threshold,
        skip_install=args.skip_install,
    )
    result["policy_defaults"] = {
        "overall": float(skin_policy["overall_pass_threshold"]),
        "texture": float(skin_policy["texture_pass_threshold"]),
        "color": float(skin_policy["color_naturalness_pass_threshold"]),
    }

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    if args.fail_on_threshold and not result["pass"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
