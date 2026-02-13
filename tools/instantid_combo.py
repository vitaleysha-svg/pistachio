#!/usr/bin/env python3
"""
ULTIMATE Face Lock: InstantID + FaceID + LoRA + FaceDetailer
Combines all three face-locking methods for maximum identity match.
Research says this combo gets near 100% face similarity.
"""
import json, urllib.request, time, os, sys

COMFYUI_URL = "http://127.0.0.1:8188"

REF_DIR = "/workspace/lora_dataset_v3/10_amiranoor"
BEST_REFS = [
    "img_008.png",  # 453x643 - largest face
    "img_009.png",  # 460x608
    "img_025.png",  # 419x667
    "img_024.png",  # 464x518
    "img_031.png",  # 349x490
]

PROMPTS = [
    ("portrait_front", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, front facing portrait photo, looking directly at camera, natural lighting, soft smile, photorealistic, 8k, detailed skin texture, visible pores, natural skin imperfections, warm skin tone, brown eyes, dark hair"),
    ("portrait_3q", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, three quarter view portrait, warm golden hour lighting, photorealistic, 8k, natural skin texture, beautiful face, brown eyes, full lips, dark hair"),
    ("halfbody", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, half body shot, casual outfit, outdoor cafe, golden hour, photorealistic, 8k, natural skin texture, warm tones, dark hair"),
    ("glamour", "a stunning young woman with warm olive skin, Egyptian-Brazilian features, glamour photography, soft studio lighting, elegant pose, photorealistic, 8k, fashion photo, natural skin, warm lighting, dark hair"),
]

NEGATIVE = "(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (overly smooth:1.2), (unrealistic skin texture:1.1), (doll-like:1.2), (wax figure:1.1), (blurry skin texture:1.1), ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, 3d render, cartoon, anime, painting, illustration, overexposed, worst quality, jpeg artifacts, pale skin"

# Test configs - varying InstantID weight + FaceID combo
CONFIGS = [
    # InstantID only (no FaceID, no LoRA) - pure InstantID baseline
    {"label": "instantid_only_w0.8", "use_instantid": True, "iid_w": 0.8, "use_faceid": False, "lora": None},
    # InstantID + LoRA
    {"label": "instantid_lora_w0.8", "use_instantid": True, "iid_w": 0.8, "use_faceid": False, "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5},
    # InstantID stronger
    {"label": "instantid_only_w1.2", "use_instantid": True, "iid_w": 1.2, "use_faceid": False, "lora": None},
    # COMBO: InstantID + FaceID + LoRA (the ultimate)
    {"label": "combo_iid0.7_fid0.8", "use_instantid": True, "iid_w": 0.7, "use_faceid": True, "fw": 0.8, "fv2w": 2.0, "flora_str": 0.6, "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5},
    # COMBO stronger InstantID
    {"label": "combo_iid1.0_fid0.8", "use_instantid": True, "iid_w": 1.0, "use_faceid": True, "fw": 0.8, "fv2w": 2.0, "flora_str": 0.6, "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5},
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


def make_workflow(uploaded_names, cfg, prompt, seed, prefix):
    use_instantid = cfg.get("use_instantid", False)
    use_faceid = cfg.get("use_faceid", False)
    lora_name = cfg.get("lora")
    lora_str = cfg.get("lora_str", 0.5)
    ref_image = uploaded_names[0]

    nodes = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "realvisxl_v5.safetensors"}
        },
        "5": {
            "class_type": "LoadImage",
            "inputs": {"image": ref_image}
        },
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },
        "14": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["13", 0], "vae": ["1", 2]}
        },
        "15": {
            "class_type": "SaveImage",
            "inputs": {"images": ["14", 0], "filename_prefix": f"combo/{prefix}"}
        }
    }

    # Track current model and clip sources
    if lora_name:
        nodes["2"] = {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0], "clip": ["1", 1],
                "lora_name": lora_name,
                "strength_model": lora_str,
                "strength_clip": lora_str
            }
        }
        current_model = ["2", 0]
        clip_source = ["2", 1]
    else:
        current_model = ["1", 0]
        clip_source = ["1", 1]

    # InstantID path
    if use_instantid:
        nodes["20"] = {
            "class_type": "InstantIDModelLoader",
            "inputs": {"instantid_file": "ip-adapter.bin"}
        }
        nodes["21"] = {
            "class_type": "ControlNetLoader",
            "inputs": {"control_net_name": "instantid-controlnet.safetensors"}
        }
        # InstantID needs its own face analysis (type FACEANALYSIS)
        nodes["23"] = {
            "class_type": "InstantIDFaceAnalysis",
            "inputs": {"provider": "CUDA"}
        }

        # Encode prompts BEFORE InstantID (it modifies conditioning)
        nodes["10"] = {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": clip_source}
        }
        nodes["11"] = {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": clip_source}
        }

        nodes["22"] = {
            "class_type": "ApplyInstantID",
            "inputs": {
                "instantid": ["20", 0],
                "insightface": ["23", 0],
                "control_net": ["21", 0],
                "image": ["5", 0],
                "model": current_model,
                "positive": ["10", 0],
                "negative": ["11", 0],
                "weight": cfg.get("iid_w", 0.8),
                "start_at": 0.0,
                "end_at": 1.0
            }
        }
        current_model = ["22", 0]
        positive_cond = ["22", 1]
        negative_cond = ["22", 2]
    else:
        nodes["10"] = {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": clip_source}
        }
        nodes["11"] = {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": clip_source}
        }
        positive_cond = ["10", 0]
        negative_cond = ["11", 0]

    # FaceID path (on top of InstantID if both enabled)
    if use_faceid:
        # FaceID needs IPAdapterInsightFaceLoader (type INSIGHTFACE)
        nodes["29"] = {
            "class_type": "IPAdapterInsightFaceLoader",
            "inputs": {"provider": "CUDA", "model_name": "antelopev2"}
        }
        nodes["30"] = {
            "class_type": "IPAdapterUnifiedLoaderFaceID",
            "inputs": {
                "model": current_model,
                "preset": "FACEID PLUS V2",
                "lora_strength": cfg.get("flora_str", 0.6),
                "provider": "CUDA"
            }
        }
        nodes["31"] = {
            "class_type": "IPAdapterFaceID",
            "inputs": {
                "model": ["30", 0],
                "ipadapter": ["30", 1],
                "image": ["5", 0],
                "weight": cfg.get("fw", 0.8),
                "weight_faceidv2": cfg.get("fv2w", 2.0),
                "weight_type": "linear",
                "combine_embeds": "concat",
                "start_at": 0.0,
                "end_at": 1.0,
                "embeds_scaling": "V only",
                "insightface": ["29", 0]
            }
        }
        current_model = ["31", 0]

    # KSampler
    nodes["13"] = {
        "class_type": "KSampler",
        "inputs": {
            "model": current_model,
            "positive": positive_cond,
            "negative": negative_cond,
            "latent_image": ["12", 0],
            "seed": seed,
            "steps": 25,
            "cfg": 3.5,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1.0
        }
    }

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


def wait_for_completion(prompt_id, timeout=240):
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
                                print(f"  ERROR: {details['exception_message'][:300]}")
                    return None
                return history[prompt_id]
        except:
            pass
        time.sleep(3)
    return None


if __name__ == "__main__":
    ref_images = [os.path.join(REF_DIR, f) for f in BEST_REFS]
    print(f"Uploading {len(ref_images)} reference images...")
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
    print(f"\nRunning {total} InstantID COMBO generations...\n")

    for cfg_item in CONFIGS:
        for pi, (plabel, prompt) in enumerate(PROMPTS):
            count += 1
            prefix = f"{cfg_item['label']}_{plabel}"
            print(f"[{count}/{total}] {prefix}")

            workflow = make_workflow(uploaded_names, cfg_item, prompt, 42 + pi, prefix)
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
    print(f"COMBO SWEEP: {successes}/{total} images")
    print(f"Results in: /workspace/runpod-slim/ComfyUI/output/combo/")
    print(f"{'='*50}")

    # Similarity scoring
    print("\nRunning face similarity analysis...")
    try:
        import insightface
        from insightface.app import FaceAnalysis
        import cv2, glob, numpy as np

        app = FaceAnalysis(name='antelopev2', root='/workspace/runpod-slim/ComfyUI/models/insightface/', providers=['CUDAExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        ref_embeds = []
        for fname in BEST_REFS:
            img = cv2.imread(os.path.join(REF_DIR, fname))
            faces = app.get(img)
            if faces:
                best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
                ref_embeds.append(best.normed_embedding)
        ref_avg = np.mean(ref_embeds, axis=0)
        ref_avg = ref_avg / np.linalg.norm(ref_avg)

        out_dir = '/workspace/runpod-slim/ComfyUI/output/combo'
        results = []
        for f in sorted(glob.glob(os.path.join(out_dir, '*.png'))):
            img = cv2.imread(f)
            faces = app.get(img)
            name = os.path.basename(f).replace('_00001_.png', '')
            if faces:
                best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
                sim = float(np.dot(ref_avg, best.normed_embedding))
                results.append((name, sim))
            else:
                results.append((name, 0.0))

        print(f"\n{'='*50}")
        print("SIMILARITY BY CONFIG:")
        for cfg_item in CONFIGS:
            label = cfg_item['label']
            group = [r for r in results if r[0].startswith(label)]
            if group:
                valid = [r for r in group if r[1] > 0]
                avg = np.mean([r[1] for r in valid]) if valid else 0
                best_r = max(group, key=lambda x: x[1])
                print(f"\n  {label}: avg={avg:.4f} best={best_r[1]:.4f}")
                for name, sim in group:
                    print(f"    {name}: {sim:.4f}")

        overall_valid = [r for r in results if r[1] > 0]
        if overall_valid:
            print(f"\nOverall avg: {np.mean([r[1] for r in overall_valid]):.4f}")
            best_overall = max(results, key=lambda x: x[1])
            print(f"Best overall: {best_overall[0]} = {best_overall[1]:.4f}")
        print(f"{'='*50}")
    except Exception as e:
        print(f"Similarity check failed: {e}")
