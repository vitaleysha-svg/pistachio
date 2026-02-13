#!/usr/bin/env python3
"""
CORRECTED Face-Locked Workflow
Based on proven community settings from CivitAI/Reddit/BlackHatWorld
Key fixes: CFG 3.5, FaceID v2 weight 2.0, DPM++ 2M Karras, weighted negatives
"""
import json, urllib.request, time, os, sys, glob

COMFYUI_URL = "http://127.0.0.1:8188"

# Use BEST reference images (ranked by InsightFace face detection area)
# Only images where InsightFace actually detects a clear face
REF_DIR = "/workspace/lora_dataset_v3/10_amiranoor"
BEST_REFS = [
    "img_008.png",  # 453x643 - largest face area
    "img_009.png",  # 460x608 - second largest
    "img_025.png",  # 419x667 - third largest
    "img_024.png",  # 464x518 - fourth largest
    "img_031.png",  # 349x490 - fifth largest
]

PROMPTS = [
    ("portrait1", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, close up portrait photo, natural lighting, soft smile, looking at camera, photorealistic, 8k, detailed skin texture, visible pores, natural skin imperfections, warm skin tone, brown eyes, dark hair"),
    ("portrait2", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, three quarter view portrait, warm golden hour lighting, photorealistic, 8k, natural skin texture, visible pores, beautiful face, brown eyes, full lips"),
    ("halfbody", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, half body shot, casual elegant outfit, outdoor cafe, golden hour, photorealistic, 8k, natural skin texture, warm tones"),
    ("glamour", "a stunning young woman with warm olive skin, Egyptian-Brazilian features, glamour photography, soft studio lighting, elegant pose, photorealistic, 8k, fashion photo, natural skin, warm lighting"),
    ("beach", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, beach sunset, wind in hair, natural pose, photorealistic, 8k, natural skin, warm golden light"),
    ("casual", "a beautiful young woman with warm olive skin, Egyptian-Brazilian features, casual selfie style, natural indoor lighting, relaxed smile, photorealistic, 8k, natural skin texture, iPhone quality"),
]

# CORRECTED negative prompt with weights (proven community settings)
NEGATIVE = "(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (overly smooth:1.2), (unrealistic skin texture:1.1), (doll-like:1.2), (wax figure:1.1), (blurry skin texture:1.1), ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, 3d render, cartoon, anime, painting, illustration, overexposed, worst quality, jpeg artifacts, pale skin"

# Test configs based on proven settings
CONFIGS = [
    # Proven community settings: low CFG + high FaceID v2
    {"label": "proven_nolora", "lora": None, "cfg": 3.5, "fw": 0.8, "fv2w": 2.0, "flora_str": 0.6},
    # With LoRA at low strength
    {"label": "proven_lora05", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.5, "cfg": 3.5, "fw": 0.8, "fv2w": 2.0, "flora_str": 0.6},
    # With LoRA at medium strength
    {"label": "proven_lora07", "lora": "amiranoor_v3-step00001500.safetensors", "lora_str": 0.7, "cfg": 3.5, "fw": 0.8, "fv2w": 2.0, "flora_str": 0.6},
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


def make_workflow(uploaded_names, lora_name, lora_str, cfg, fw, fv2w, flora_str, prompt, seed, prefix):
    """
    CORRECTED workflow with proven community settings:
    - CFG: 3.5 (not 7.0)
    - FaceID weight: 0.8, v2 weight: 2.0
    - DPM++ 2M Karras sampler
    - Weighted negative prompts
    - Multiple reference images batched together (5 best faces)
    """
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
            "inputs": {"text": prompt, "clip": None}  # clip source set below
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": None}  # clip source set below
        },
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },
        "13": {
            "class_type": "KSampler",
            "inputs": {
                "model": None,  # model source set below
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
            "inputs": {"images": ["14", 0], "filename_prefix": f"corrected/{prefix}"}
        }
    }

    # Load ALL reference images and batch them together
    # This gives FaceID multiple angles for stronger face embedding
    for i, ref_name in enumerate(uploaded_names):
        nodes[f"img_{i}"] = {
            "class_type": "LoadImage",
            "inputs": {"image": ref_name}
        }

    # Chain ImageBatch nodes to combine all references
    if len(uploaded_names) == 1:
        final_image_ref = ["img_0", 0]
    else:
        # Batch first two images
        nodes["batch_0"] = {
            "class_type": "ImageBatch",
            "inputs": {
                "image1": ["img_0", 0],
                "image2": ["img_1", 0]
            }
        }
        # Chain remaining images
        for i in range(2, len(uploaded_names)):
            nodes[f"batch_{i-1}"] = {
                "class_type": "ImageBatch",
                "inputs": {
                    "image1": [f"batch_{i-2}", 0],
                    "image2": [f"img_{i}", 0]
                }
            }
        final_batch_id = f"batch_{len(uploaded_names)-2}"
        final_image_ref = [final_batch_id, 0]

    if lora_name:
        # With LoRA
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
    else:
        # No LoRA
        model_for_faceid = ["1", 0]
        clip_source = ["1", 1]

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
            "embeds_scaling": "V only",
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
    # Upload BEST reference images (verified by InsightFace face detection)
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
    print(f"\nRunning {total} CORRECTED generations (CFG=3.5, FaceID v2=2.0, DPM++ 2M Karras)...\n")

    for cfg in CONFIGS:
        for pi, (plabel, prompt) in enumerate(PROMPTS):
            count += 1
            prefix = f"{cfg['label']}_{plabel}"
            print(f"[{count}/{total}] {prefix}")

            lora = cfg.get("lora")
            lora_str = cfg.get("lora_str", 0.0)

            workflow = make_workflow(
                uploaded_names, lora, lora_str,
                cfg["cfg"], cfg["fw"], cfg["fv2w"], cfg["flora_str"],
                prompt, 42 + pi, prefix
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
    print(f"CORRECTED SWEEP: {successes}/{total} images")
    print(f"Results in: /workspace/runpod-slim/ComfyUI/output/corrected/")
    print(f"{'='*50}")
