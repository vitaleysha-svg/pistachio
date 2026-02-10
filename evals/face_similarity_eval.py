#!/usr/bin/env python3
"""Face similarity evaluation using InsightFace embeddings."""

from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from load_thresholds import load_thresholds

REQUIRED_PACKAGES = {
    "insightface": "0.7.3",
    "onnxruntime-gpu": "1.17.1",
    "numpy": "1.26.4",
    "opencv-python-headless": "4.9.0.80",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def ensure_dependencies(skip_install: bool) -> None:
    missing: list[str] = []
    import_names = {
        "onnxruntime-gpu": "onnxruntime",
        "opencv-python-headless": "cv2",
    }
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


def cosine_similarity(vector_a, vector_b) -> float:
    import numpy as np

    denom = float(np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
    if denom == 0:
        return 0.0
    return float(np.dot(vector_a, vector_b) / denom)


def extract_embedding(app, image_path: Path):
    import cv2

    image = cv2.imread(str(image_path))
    if image is None:
        return None
    faces = app.get(image)
    if not faces:
        return None
    # Prefer the largest detected face for consistency.
    faces = sorted(
        faces,
        key=lambda face: (face.bbox[2] - face.bbox[0]) * (face.bbox[3] - face.bbox[1]),
        reverse=True,
    )
    return faces[0].embedding


def build_face_app(prefer_cpu: bool):
    from insightface.app import FaceAnalysis

    if prefer_cpu:
        providers = ["CPUExecutionProvider"]
    else:
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    app = FaceAnalysis(name="buffalo_l", providers=providers)
    app.prepare(ctx_id=0 if not prefer_cpu else -1, det_size=(640, 640))
    return app


def evaluate_face_similarity(
    generated_dir: Path,
    reference_dir: Path,
    threshold: float,
    prefer_cpu: bool = False,
    skip_install: bool = False,
) -> dict[str, Any]:
    ensure_dependencies(skip_install=skip_install)

    generated_images = iter_images(generated_dir)
    reference_images = iter_images(reference_dir)
    if not generated_images:
        raise RuntimeError(f"No generated images found in: {generated_dir}")
    if not reference_images:
        raise RuntimeError(f"No reference images found in: {reference_dir}")

    app = build_face_app(prefer_cpu=prefer_cpu)

    reference_embeddings: list[tuple[Path, Any]] = []
    for ref_image in reference_images:
        embedding = extract_embedding(app, ref_image)
        if embedding is not None:
            reference_embeddings.append((ref_image, embedding))

    if not reference_embeddings:
        raise RuntimeError("No faces detected in reference images.")

    per_image: list[dict[str, Any]] = []
    for gen_image in generated_images:
        embedding = extract_embedding(app, gen_image)
        if embedding is None:
            per_image.append(
                {
                    "image": str(gen_image),
                    "score": 0.0,
                    "face_detected": False,
                    "best_reference": None,
                }
            )
            continue

        best_score = -1.0
        best_reference = None
        for ref_path, ref_embedding in reference_embeddings:
            score = cosine_similarity(embedding, ref_embedding)
            if score > best_score:
                best_score = score
                best_reference = ref_path

        per_image.append(
            {
                "image": str(gen_image),
                "score": float(max(best_score, 0.0)),
                "face_detected": True,
                "best_reference": str(best_reference) if best_reference else None,
            }
        )

    mean_similarity = sum(item["score"] for item in per_image) / len(per_image)
    passed = mean_similarity >= threshold

    return {
        "generated_dir": str(generated_dir),
        "reference_dir": str(reference_dir),
        "threshold": threshold,
        "images_evaluated": len(per_image),
        "reference_faces": len(reference_embeddings),
        "mean_similarity": mean_similarity,
        "pass": passed,
        "per_image": per_image,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate face similarity against reference images.")
    parser.add_argument("--generated", type=Path, required=True, help="Directory of generated images.")
    parser.add_argument("--reference", type=Path, required=True, help="Directory of reference images.")
    parser.add_argument("--threshold", type=float, default=None, help="Pass threshold for mean cosine similarity.")
    parser.add_argument("--output-json", type=Path, default=None)
    parser.add_argument("--fail-on-threshold", action="store_true")
    parser.add_argument("--prefer-cpu", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    thresholds = load_thresholds(project_root=Path.cwd())
    default_threshold = float(thresholds["face_similarity"]["pass_threshold"])
    threshold = args.threshold if args.threshold is not None else default_threshold

    result = evaluate_face_similarity(
        generated_dir=args.generated,
        reference_dir=args.reference,
        threshold=threshold,
        prefer_cpu=args.prefer_cpu,
        skip_install=args.skip_install,
    )
    result["policy_default_threshold"] = default_threshold

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    if args.fail_on_threshold and not result["pass"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
