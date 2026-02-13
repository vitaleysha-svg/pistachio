#!/usr/bin/env python3
"""
Analyze reference images for LoRA training suitability.
- Detects faces with InsightFace
- Scores inter-reference similarity (consistency)
- Ranks images by face area + quality
- Outputs recommended training set
"""
import os, sys, glob, json
import cv2
import numpy as np
from insightface.app import FaceAnalysis

REF_DIR = "/workspace/new_references"
OUTPUT_FILE = "/workspace/reference_analysis.json"

print("Loading InsightFace (antelopev2)...")
app = FaceAnalysis(
    name='antelopev2',
    root='/workspace/runpod-slim/ComfyUI/models/insightface/',
    providers=['CUDAExecutionProvider']
)
app.prepare(ctx_id=0, det_size=(640, 640))
print("  -> Ready\n")

# Analyze all images
results = []
images = sorted(glob.glob(os.path.join(REF_DIR, "*.png")))
print(f"Found {len(images)} images\n")

for i, path in enumerate(images):
    fname = os.path.basename(path)
    img = cv2.imread(path)
    if img is None:
        print(f"[{i+1}/{len(images)}] {fname[:60]}... SKIPPED (unreadable)")
        continue

    h, w = img.shape[:2]
    faces = app.get(img)

    if not faces:
        print(f"[{i+1}/{len(images)}] {fname[:60]}... NO FACE")
        results.append({
            "file": fname,
            "has_face": False,
            "resolution": f"{w}x{h}",
        })
        continue

    # Use largest face
    best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
    bw = best.bbox[2] - best.bbox[0]
    bh = best.bbox[3] - best.bbox[1]
    face_area = bw * bh
    face_ratio = face_area / (w * h)

    print(f"[{i+1}/{len(images)}] {fname[:60]}... FACE {int(bw)}x{int(bh)} ({face_ratio:.0%} of image)")

    results.append({
        "file": fname,
        "has_face": True,
        "resolution": f"{w}x{h}",
        "face_size": f"{int(bw)}x{int(bh)}",
        "face_area": int(face_area),
        "face_ratio": round(face_ratio, 3),
        "embedding": best.normed_embedding.tolist(),
    })

# Compute pairwise similarities
face_results = [r for r in results if r["has_face"]]
no_face = [r for r in results if not r["has_face"]]

print(f"\n{'='*60}")
print(f"FACE DETECTION: {len(face_results)}/{len(results)} images have faces")
print(f"NO FACE: {len(no_face)} images")
if no_face:
    for r in no_face:
        print(f"  - {r['file'][:60]}")

if len(face_results) < 2:
    print("Not enough faces for similarity analysis")
    sys.exit(1)

embeddings = np.array([r["embedding"] for r in face_results])

# Average embedding
avg_embed = np.mean(embeddings, axis=0)
avg_embed = avg_embed / np.linalg.norm(avg_embed)

# Compute similarity of each to the average (consistency score)
print(f"\n{'='*60}")
print(f"INTER-REFERENCE CONSISTENCY (similarity to group average)")
print(f"{'='*60}")

for r in face_results:
    emb = np.array(r["embedding"])
    sim = float(np.dot(avg_embed, emb))
    r["consistency_score"] = round(sim, 4)
    # Remove embedding from output (too large)
    del r["embedding"]

# Sort by consistency
face_results.sort(key=lambda x: x["consistency_score"], reverse=True)

for r in face_results:
    status = "KEEP" if r["consistency_score"] >= 0.50 else "DROP"
    print(f"  {status} {r['consistency_score']:.4f} | {r['face_size']:>9s} | {r['file'][:55]}")

# Recommended set: faces with consistency >= 0.50 and face_area >= 5000
recommended = [r for r in face_results if r["consistency_score"] >= 0.50 and r["face_area"] >= 5000]
dropped = [r for r in face_results if r not in recommended]

print(f"\n{'='*60}")
print(f"RECOMMENDED TRAINING SET: {len(recommended)} images")
print(f"DROPPED: {len(dropped)} (low consistency or tiny face)")
print(f"NO FACE: {len(no_face)}")
print(f"{'='*60}")

# Pairwise similarity matrix for top images
if len(recommended) >= 2:
    # Recompute embeddings for recommended
    rec_embeds = []
    for r in recommended:
        path = os.path.join(REF_DIR, r["file"])
        img = cv2.imread(path)
        faces = app.get(img)
        if faces:
            best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
            rec_embeds.append(best.normed_embedding)

    if len(rec_embeds) >= 2:
        rec_embeds = np.array(rec_embeds)
        sim_matrix = np.dot(rec_embeds, rec_embeds.T)
        # Get off-diagonal similarities
        mask = ~np.eye(len(rec_embeds), dtype=bool)
        pairwise_sims = sim_matrix[mask]
        print(f"\nPAIRWISE SIMILARITY (recommended set):")
        print(f"  Mean: {np.mean(pairwise_sims):.4f}")
        print(f"  Min:  {np.min(pairwise_sims):.4f}")
        print(f"  Max:  {np.max(pairwise_sims):.4f}")

# Save results
output = {
    "total_images": len(results),
    "faces_detected": len(face_results),
    "no_face": len(no_face),
    "recommended_count": len(recommended),
    "recommended_files": [r["file"] for r in recommended],
    "dropped_files": [r["file"] for r in dropped],
    "no_face_files": [r["file"] for r in no_face],
    "details": face_results + no_face,
}
with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nFull results saved to {OUTPUT_FILE}")

# Create symlinks for recommended images
rec_dir = "/workspace/lora_dataset_v4"
os.makedirs(os.path.join(rec_dir, "10_amiranoor"), exist_ok=True)
for i, r in enumerate(recommended):
    src = os.path.join(REF_DIR, r["file"])
    # Rename to simple names for training
    dst = os.path.join(rec_dir, "10_amiranoor", f"img_{i:03d}.png")
    if not os.path.exists(dst):
        import shutil
        shutil.copy2(src, dst)
print(f"\nTraining dataset created: {rec_dir}/10_amiranoor/ ({len(recommended)} images)")
print(f"Ready for LoRA v4 training!")
