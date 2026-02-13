#!/usr/bin/env python3
"""
PRODUCTION InstantID + LoRA Generator
- Varied poses, angles, and settings
- Auto quality gate (rejects <0.60 similarity)
- InstantID weight 0.8 + LoRA 0.5 (proven best config)
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

# DIVERSE prompts - different angles, poses, settings, compositions
PROMPTS = [
    # PORTRAITS - face focus, varied angles
    ("portrait_front", "amiranoor, a beautiful young woman with warm olive skin, Egyptian-Brazilian features, front facing portrait photo, looking directly at camera, natural lighting, soft smile, photorealistic, 8k, detailed skin texture, visible pores, warm skin tone, brown eyes, dark hair"),
    ("portrait_3quarter", "amiranoor, a beautiful young woman with warm olive skin, three quarter view portrait, head tilted slightly, warm golden hour side lighting, gentle smile, photorealistic, 8k, natural skin texture, brown eyes, full lips, dark hair"),
    ("portrait_profile", "amiranoor, a beautiful young woman with warm olive skin, profile view portrait, looking to the side, dramatic studio lighting, elegant pose, photorealistic, 8k, jawline visible, ear showing, dark hair pulled back"),
    ("portrait_looking_up", "amiranoor, a beautiful young woman with warm olive skin, looking upward, soft dreamy expression, natural daylight from above, chin slightly raised, photorealistic, 8k, detailed skin texture, brown eyes, dark hair"),

    # HALF BODY - different settings and poses
    ("halfbody_cafe", "amiranoor, a beautiful young woman with warm olive skin, sitting at a cozy cafe, holding coffee cup, casual outfit, warm indoor lighting, half body shot, relaxed pose, photorealistic, 8k, natural skin, dark hair"),
    ("halfbody_outdoor", "amiranoor, a beautiful young woman with warm olive skin, standing outdoors in a park, leaning against a tree, casual summer dress, dappled sunlight, half body shot, photorealistic, 8k, natural skin, dark hair"),
    ("halfbody_beach", "amiranoor, a beautiful young woman with warm olive skin, at the beach, ocean in background, bikini top, wind in hair, golden hour lighting, half body shot, photorealistic, 8k, warm tones, dark hair"),
    ("halfbody_gym", "amiranoor, a beautiful young woman with warm olive skin, athletic wear, gym setting, confident pose, bright lighting, half body shot, fit physique, photorealistic, 8k, natural skin, dark hair in ponytail"),

    # FULL BODY / LIFESTYLE - complete compositions
    ("lifestyle_couch", "amiranoor, a beautiful young woman with warm olive skin, lounging on a white couch, casual home outfit, soft natural window light, full body shot, relaxed comfortable pose, photorealistic, 8k, cozy setting, dark hair"),
    ("lifestyle_street", "amiranoor, a beautiful young woman with warm olive skin, walking on a city street, fashionable outfit, urban background, golden hour, three quarter body shot, candid look, photorealistic, 8k, dark hair"),
    ("glamour_studio", "amiranoor, a stunning young woman with warm olive skin, glamour photography, soft studio lighting, elegant black dress, seated pose with legs crossed, professional photo, photorealistic, 8k, fashion lighting, dark hair styled"),
    ("selfie_mirror", "amiranoor, a beautiful young woman with warm olive skin, mirror selfie, casual outfit, bedroom setting, natural phone photo style, warm indoor lighting, photorealistic, 8k, candid authentic look, dark hair"),
]

NEGATIVE = "(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (overly smooth:1.2), (unrealistic skin texture:1.1), (doll-like:1.2), (wax figure:1.1), (blurry skin texture:1.1), ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, 3d render, cartoon, anime, painting, illustration, overexposed, worst quality, jpeg artifacts, pale skin, multiple people, two faces, duplicate"

# Production config
CONFIG = {
    "lora": "amiranoor_v3-step00001000.safetensors",
    "lora_str": 0.5,
    "iid_w": 0.8,
    "cfg": 3.5,
    "steps": 25,
}

QUALITY_THRESHOLD = 0.55  # Reject below this similarity


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


def make_workflow(ref_image, prompt, seed, prefix):
    cfg = CONFIG
    nodes = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "realvisxl_v5.safetensors"}
        },
        "2": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0], "clip": ["1", 1],
                "lora_name": cfg["lora"],
                "strength_model": cfg["lora_str"],
                "strength_clip": cfg["lora_str"]
            }
        },
        "5": {
            "class_type": "LoadImage",
            "inputs": {"image": ref_image}
        },
        "10": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["2", 1]}
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": ["2", 1]}
        },
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },
        "20": {
            "class_type": "InstantIDModelLoader",
            "inputs": {"instantid_file": "ip-adapter.bin"}
        },
        "21": {
            "class_type": "ControlNetLoader",
            "inputs": {"control_net_name": "instantid-controlnet.safetensors"}
        },
        "23": {
            "class_type": "InstantIDFaceAnalysis",
            "inputs": {"provider": "CUDA"}
        },
        "22": {
            "class_type": "ApplyInstantID",
            "inputs": {
                "instantid": ["20", 0],
                "insightface": ["23", 0],
                "control_net": ["21", 0],
                "image": ["5", 0],
                "model": ["2", 0],
                "positive": ["10", 0],
                "negative": ["11", 0],
                "weight": cfg["iid_w"],
                "start_at": 0.0,
                "end_at": 1.0
            }
        },
        "13": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["22", 0],
                "positive": ["22", 1],
                "negative": ["22", 2],
                "latent_image": ["12", 0],
                "seed": seed,
                "steps": cfg["steps"],
                "cfg": cfg["cfg"],
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
            "inputs": {"images": ["14", 0], "filename_prefix": f"production/{prefix}"}
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
    # Upload reference image (best single reference)
    ref_path = os.path.join(REF_DIR, BEST_REFS[0])
    print(f"Uploading reference: {BEST_REFS[0]}")
    ref_name = upload_image(ref_path)
    if not ref_name:
        print("FATAL: Reference upload failed")
        sys.exit(1)
    print(f"  -> {ref_name}")

    # Generate with 3 different seeds per prompt for variety
    seeds = [42, 777, 1337]
    total = len(PROMPTS) * len(seeds)
    count = 0
    successes = 0
    generated_files = []
    print(f"\nGenerating {total} PRODUCTION images (12 prompts x 3 seeds)...\n")

    for plabel, prompt in PROMPTS:
        for si, seed in enumerate(seeds):
            count += 1
            prefix = f"{plabel}_s{seed}"
            print(f"[{count}/{total}] {prefix}")

            workflow = make_workflow(ref_name, prompt, seed, prefix)
            prompt_id = queue_prompt(workflow)
            if prompt_id:
                result = wait_for_completion(prompt_id)
                if result:
                    outputs = result.get("outputs", {})
                    for nid, nout in outputs.items():
                        for img in nout.get("images", []):
                            fname = img.get("filename", "?")
                            print(f"  -> {fname}")
                            generated_files.append(fname)
                            successes += 1
                else:
                    print("  -> FAILED/TIMEOUT")
            else:
                print("  -> QUEUE FAILED")

    print(f"\n{'='*60}")
    print(f"GENERATION: {successes}/{total} images")
    print(f"{'='*60}")

    # QUALITY GATE - auto-reject low similarity
    print("\n--- QUALITY GATE ---")
    print("Loading InsightFace for similarity check...")
    try:
        import insightface
        from insightface.app import FaceAnalysis
        import cv2, glob, numpy as np

        app = FaceAnalysis(name='antelopev2',
                          root='/workspace/runpod-slim/ComfyUI/models/insightface/',
                          providers=['CUDAExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        # Build reference embedding from top 5 images
        ref_embeds = []
        for fname in BEST_REFS:
            img = cv2.imread(os.path.join(REF_DIR, fname))
            if img is None:
                continue
            faces = app.get(img)
            if faces:
                best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
                ref_embeds.append(best.normed_embedding)
        if not ref_embeds:
            print("ERROR: No reference faces detected")
            sys.exit(1)
        ref_avg = np.mean(ref_embeds, axis=0)
        ref_avg = ref_avg / np.linalg.norm(ref_avg)
        print(f"Reference embedding built from {len(ref_embeds)} faces")

        # Score all generated images
        out_dir = '/workspace/runpod-slim/ComfyUI/output/production'
        os.makedirs(out_dir, exist_ok=True)
        passed_dir = os.path.join(out_dir, 'PASSED')
        failed_dir = os.path.join(out_dir, 'FAILED')
        os.makedirs(passed_dir, exist_ok=True)
        os.makedirs(failed_dir, exist_ok=True)

        results = []
        passed = 0
        failed = 0
        no_face = 0

        for f in sorted(glob.glob(os.path.join(out_dir, '*.png'))):
            img = cv2.imread(f)
            if img is None:
                continue
            faces = app.get(img)
            basename = os.path.basename(f)
            name = basename.replace('_00001_.png', '').replace('_00002_.png', '')

            if faces:
                best = max(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]))
                sim = float(np.dot(ref_avg, best.normed_embedding))
                results.append((name, sim, basename))

                if sim >= QUALITY_THRESHOLD:
                    # Copy to PASSED
                    import shutil
                    shutil.copy2(f, os.path.join(passed_dir, basename))
                    print(f"  PASS {name}: {sim:.4f}")
                    passed += 1
                else:
                    shutil.copy2(f, os.path.join(failed_dir, basename))
                    print(f"  FAIL {name}: {sim:.4f} (below {QUALITY_THRESHOLD})")
                    failed += 1
            else:
                print(f"  NO FACE: {name}")
                no_face += 1
                import shutil
                shutil.copy2(f, os.path.join(failed_dir, basename))

        print(f"\n{'='*60}")
        print(f"QUALITY GATE RESULTS")
        print(f"  PASSED: {passed} (similarity >= {QUALITY_THRESHOLD})")
        print(f"  FAILED: {failed} (similarity < {QUALITY_THRESHOLD})")
        print(f"  NO FACE: {no_face}")
        print(f"  Pass rate: {passed/(passed+failed+no_face)*100:.0f}%" if (passed+failed+no_face) > 0 else "")

        if results:
            sims = [r[1] for r in results]
            print(f"\n  Avg similarity: {np.mean(sims):.4f}")
            print(f"  Min similarity: {np.min(sims):.4f}")
            print(f"  Max similarity: {np.max(sims):.4f}")
            best_r = max(results, key=lambda x: x[1])
            print(f"  Best: {best_r[0]} = {best_r[1]:.4f}")

            # Group by prompt type
            print(f"\nBY PROMPT TYPE:")
            for plabel, _ in PROMPTS:
                group = [r for r in results if r[0].startswith(plabel)]
                if group:
                    gavg = np.mean([r[1] for r in group])
                    gbest = max(group, key=lambda x: x[1])
                    print(f"  {plabel}: avg={gavg:.4f} best={gbest[1]:.4f}")

        print(f"\nPassed images in: {passed_dir}")
        print(f"Failed images in: {failed_dir}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"Quality check failed: {e}")
        import traceback
        traceback.print_exc()
