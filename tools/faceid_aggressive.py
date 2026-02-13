#!/usr/bin/env python3
"""
AGGRESSIVE FaceID Test - Push weights harder for better face match
Based on community research: higher FaceID weights + lower CFG = stronger identity
Tests weight ranges beyond conservative defaults
"""
import json, urllib.request, time, os, sys

COMFYUI_URL = "http://127.0.0.1:8188"

# Best reference images (verified by InsightFace face detection)
REF_DIR = "/workspace/lora_dataset_v3/10_amiranoor"
BEST_REFS = [
    "img_008.png",  # 453x643 - largest face
    "img_009.png",  # 460x608
    "img_025.png",  # 419x667
    "img_024.png",  # 464x518
    "img_031.png",  # 349x490
]

# Focused prompts - portrait and half-body only (best for face comparison)
PROMPTS = [
    ("portrait_front", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, front facing portrait photo, looking directly at camera, natural lighting, soft smile, photorealistic, 8k, detailed skin texture, visible pores, natural skin imperfections, warm skin tone, brown eyes, dark hair"),
    ("portrait_3q", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, three quarter view portrait, warm golden hour lighting, photorealistic, 8k, natural skin texture, beautiful face, brown eyes, full lips, dark hair"),
    ("halfbody", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, half body shot, casual outfit, outdoor setting, natural lighting, photorealistic, 8k, natural skin texture, warm tones, dark hair"),
]

NEGATIVE = "(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (overly smooth:1.2), (unrealistic skin texture:1.1), (doll-like:1.2), (wax figure:1.1), (blurry skin texture:1.1), ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, 3d render, cartoon, anime, painting, illustration, overexposed, worst quality, jpeg artifacts, pale skin"

# Aggressive weight configs - pushing for stronger face identity
CONFIGS = [
    # Baseline (what we had) for comparison
    {"label": "baseline_fw0.8_v2.0", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5, "cfg": 3.5, "fw": 0.8, "fv2w": 2.0, "flora_str": 0.6},
    # Push FaceID v2 weight to 3.0
    {"label": "push_fw0.8_v3.0", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5, "cfg": 3.5, "fw": 0.8, "fv2w": 3.0, "flora_str": 0.6},
    # Push both weights up
    {"label": "push_fw1.2_v3.0", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5, "cfg": 3.0, "fw": 1.2, "fv2w": 3.0, "flora_str": 0.6},
    # Max FaceID, minimal CFG
    {"label": "max_fw1.5_v3.5", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5, "cfg": 2.5, "fw": 1.5, "fv2w": 3.5, "flora_str": 0.7},
    # Higher LoRA strength with strong FaceID
    {"label": "hilora_fw1.2_v3.0", "lora": "amiranoor_v3-step00001500.safetensors", "lora_str": 0.8, "cfg": 3.0, "fw": 1.2, "fv2w": 3.0, "flora_str": 0.6},
    # V only vs default embeds_scaling test
    {"label": "style_fw1.2_v3.0", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5, "cfg": 3.0, "fw": 1.2, "fv2w": 3.0, "flora_str": 0.6, "embeds_scaling": "K+mean(V) w/ C penalty"},
]


def upload_image(filepath):
    boundary = "----PythonBoundary"
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        file_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{COMFYUI_URL}/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return result.get("name", filename)
    except Exception as e:
        print(f"Upload failed: {e}")
        return None


def make_workflow(uploaded_names, lora_name, lora_str, cfg, fw, fv2w, flora_str, prompt, seed, prefix, embeds_scaling="V only"):
    nodes = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "realvisxl_v5.safetensors"}
        },
        "6": {
            "class_type": "IPAdapterInsightFaceLoader",
            "inputs": {"provider": "CUDA", "model_name": "antelopev2"}
        },
        "10": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": None}
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": None}
        },
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },
        "13": {
            "class_type": "KSampler",
            "inputs": {
                "model": None,
                "positive": ["10", 0],
                "negative": ["11", 0],
                "latent_image": ["12", 0],
                "seed": seed,
                "steps": 25,
                "cfg": cfg,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0
            }
        },
        "14": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["13", 0], "vae": ["1", 2]}
        },
        "15": {
            "class_type": "SaveImage",
            "inputs": {"images": ["14", 0], "filename_prefix": f"aggressive/{prefix}"}
        }
    }

    # Load and batch all reference images
    for i, ref_name in enumerate(uploaded_names):
        nodes[f"img_{i}"] = {
            "class_type": "LoadImage",
            "inputs": {"image": ref_name}
        }

    if len(uploaded_names) == 1:
        final_image_ref = ["img_0", 0]
    else:
        nodes["batch_0"] = {
            "class_type": "ImageBatch",
            "inputs": {"image1": ["img_0", 0], "image2": ["img_1", 0]}
        }
        for i in range(2, len(uploaded_names)):
            nodes[f"batch_{i-1}"] = {
                "class_type": "ImageBatch",
                "inputs": {"image1": [f"batch_{i-2}", 0], "image2": [f"img_{i}", 0]}
            }
        final_image_ref = [f"batch_{len(uploaded_names)-2}", 0]

    # LoRA
    nodes["2"] = {
        "class_type": "LoraLoader",
        "inputs": {
            "model": ["1", 0], "clip": ["1", 1],
            "lora_name": lora_name,
            "strength_model": lora_str,
            "strength_clip": lora_str
        }
    }
    model_for_faceid = ["2", 0]
    clip_source = ["2", 1]

    nodes["3"] = {
        "class_type": "IPAdapterUnifiedLoaderFaceID",
        "inputs": {
            "model": model_for_faceid,
            "preset": "FACEID PLUS V2",
            "lora_strength": flora_str,
            "provider": "CUDA"
        }
    }
    nodes["4"] = {
        "class_type": "IPAdapterFaceID",
        "inputs": {
            "model": ["3", 0],
            "ipadapter": ["3", 1],
            "image": final_image_ref,
            "weight": fw,
            "weight_faceidv2": fv2w,
            "weight_type": "linear",
            "combine_embeds": "concat",
            "start_at": 0.0,
            "end_at": 1.0,
            "embeds_scaling": embeds_scaling,
            "insightface": ["6", 0]
        }
    }

    nodes["10"]["inputs"]["clip"] = clip_source
    nodes["11"]["inputs"]["clip"] = clip_source
    nodes["13"]["inputs"]["model"] = ["4", 0]

    return nodes


def queue_prompt(workflow):
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt", data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        return result.get("prompt_id")
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def wait_for_completion(prompt_id, timeout=180):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = urllib.request.urlopen(
                f"{COMFYUI_URL}/history/{prompt_id}", timeout=10
            )
            history = json.loads(resp.read())
            if prompt_id in history:
                status = history[prompt_id].get("status", {})
                if status.get("status_str") == "error":
                    msgs = status.get("messages", [])
                    for m in msgs:
                        if isinstance(m, list) and len(m) > 1:
                            details = m[1] if isinstance(m[1], dict) else {}
                            if "exception_message" in details:
                                print(f"  ERROR: {details['exception_message'][:200]}")
                    return None
                return history[prompt_id]
        except:
            pass
        time.sleep(3)
    return None


if __name__ == "__main__":
    # Upload best reference images
    ref_images = [os.path.join(REF_DIR, f) for f in BEST_REFS]
    print(f"Uploading {len(ref_images)} best reference images...")
    uploaded_names = []
    for ref in ref_images:
        name = upload_image(ref)
        if name:
            uploaded_names.append(name)
            print(f"  -> {os.path.basename(ref)} -> {name}")

    if not uploaded_names:
        print("FATAL: No reference images uploaded")
        sys.exit(1)

    total = len(CONFIGS) * len(PROMPTS)
    count = 0
    successes = 0
    print(f"\nRunning {total} AGGRESSIVE FaceID generations...\n")

    for cfg in CONFIGS:
        for pi, (plabel, prompt) in enumerate(PROMPTS):
            count += 1
            prefix = f"{cfg['label']}_{plabel}"
            print(f"[{count}/{total}] {prefix}")

            embeds_scaling = cfg.get("embeds_scaling", "V only")
            workflow = make_workflow(
                uploaded_names, cfg["lora"], cfg["lora_str"],
                cfg["cfg"], cfg["fw"], cfg["fv2w"], cfg["flora_str"],
                prompt, 42 + pi, prefix, embeds_scaling
            )
            prompt_id = queue_prompt(workflow)
            if prompt_id:
                result = wait_for_completion(prompt_id)
                if result:
                    outputs = result.get("outputs", {})
                    for nid, nout in outputs.items():
                        for img in nout.get("images", []):
                            print(f"  -> {img.get('filename', '?')}")
                            successes += 1
                else:
                    print("  -> FAILED/TIMEOUT")
            else:
                print("  -> QUEUE FAILED")

    print(f"\n{'='*50}")
    print(f"AGGRESSIVE SWEEP: {successes}/{total} images")
    print(f"Results in: /workspace/runpod-slim/ComfyUI/output/aggressive/")
    print(f"{'='*50}")

    # Auto-run similarity check
    print("\nRunning face similarity analysis...")
    try:
        import insightface
        from insightface.app import FaceAnalysis
        import cv2, glob, numpy as np

        app = FaceAnalysis(name='antelopev2', root='/workspace/runpod-slim/ComfyUI/models/insightface/', providers=['CUDAExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        # Reference embedding
        ref_embeds = []
        for fname in BEST_REFS:
            img = cv2.imread(os.path.join(REF_DIR, fname))
            faces = app.get(img)
            if faces:
                best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
                ref_embeds.append(best.normed_embedding)
        ref_avg = np.mean(ref_embeds, axis=0)
        ref_avg = ref_avg / np.linalg.norm(ref_avg)

        # Check outputs
        out_dir = '/workspace/runpod-slim/ComfyUI/output/aggressive'
        results = []
        for f in sorted(glob.glob(os.path.join(out_dir, '*.png'))):
            img = cv2.imread(f)
            faces = app.get(img)
            name = os.path.basename(f).replace('_00001_.png', '')
            if faces:
                best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
                sim = float(np.dot(ref_avg, best.normed_embedding))
                results.append((name, sim))
                print(f"  {name}: {sim:.4f}")
            else:
                print(f"  {name}: NO FACE")

        if results:
            # Group by config label
            print(f"\n{'='*50}")
            print("SIMILARITY BY CONFIG:")
            config_labels = list(dict.fromkeys([r[0].rsplit('_', 1)[0] if '_portrait' in r[0] or '_halfbody' in r[0] else r[0] for r in results]))
            for cfg in CONFIGS:
                label = cfg['label']
                group = [r for r in results if r[0].startswith(label)]
                if group:
                    avg = np.mean([r[1] for r in group])
                    best_in_group = max(group, key=lambda x: x[1])
                    print(f"  {label}: avg={avg:.4f}, best={best_in_group[1]:.4f} ({best_in_group[0]})")
            print(f"\nOverall avg: {np.mean([r[1] for r in results]):.4f}")
            print(f"Best overall: {max(results, key=lambda x: x[1])}")
            print(f"{'='*50}")
    except Exception as e:
        print(f"Similarity check failed: {e}")
