#!/usr/bin/env python3
"""
PRODUCTION V2 — InstantID Advanced + FaceDetailer + LoRA
Fixes three user-reported issues:
1. AI-ish look → FaceDetailer adds realistic skin texture + pore detail
2. Same position → ApplyInstantIDAdvanced with low cn_strength for pose freedom
3. Inconsistency → ip_weight stays high (0.8) for identity lock
"""
import json, urllib.request, time, os, sys

COMFYUI_URL = "http://127.0.0.1:8188"

REF_DIR = "/workspace/lora_dataset_v4/10_amiranoor"
BEST_REFS = [
    "img_002.png",  # 428744 - largest face
    "img_003.png",  # 349193
    "img_007.png",  # 309517
    "img_001.png",  # 298754
    "img_000.png",  # 297127
]

# V2 PROMPTS — dramatically varied compositions, poses, and realism keywords
PROMPTS = [
    # CLOSE-UP PORTRAITS — varied angles and expressions
    ("closeup_front_smile", "amiranoor, close-up portrait, beautiful young woman, warm olive skin with visible pores and natural skin texture, Egyptian-Brazilian features, front facing, genuine warm smile showing teeth, natural window light, shallow depth of field, shot on Canon R5, 85mm f1.4, brown eyes, dark wavy hair"),
    ("closeup_3quarter_serious", "amiranoor, three-quarter view close-up, beautiful young woman, warm olive skin with subtle freckles and natural imperfections, serious contemplative expression, dramatic side lighting, one side in shadow, shot on Sony A7IV, 50mm, dark hair tucked behind ear, brown eyes"),
    ("closeup_profile_wind", "amiranoor, profile view portrait, beautiful young woman, warm olive skin, wind blowing hair across face, golden hour backlighting, sun flare, looking into distance, natural skin texture with fine lines, shot on film, dark flowing hair, elegant jawline"),
    ("closeup_looking_down", "amiranoor, looking downward, beautiful young woman, warm olive skin, reading a book, soft natural light from window, eyelashes visible, peaceful expression, close-up, intimate moment, natural skin with slight imperfections, dark hair falling forward"),

    # MEDIUM SHOTS — different environments and activities
    ("medium_cafe_laughing", "amiranoor, medium shot, beautiful young woman sitting at outdoor cafe in Paris, warm olive skin, laughing candidly, holding espresso cup, wearing white blouse, dappled sunlight through trees, bokeh background, candid photography, natural pose, dark hair loose"),
    ("medium_rooftop_sunset", "amiranoor, medium shot, beautiful young woman on a rooftop at sunset, warm olive skin glowing in golden light, leaning on railing, city skyline behind, wearing fitted dress, wind in dark hair, contemplative look to the side, cinematic lighting"),
    ("medium_mirror_bathroom", "amiranoor, medium shot, beautiful young woman in bathroom mirror, warm olive skin, morning routine, minimal makeup, oversized t-shirt, messy dark hair, soft bathroom lighting, authentic everyday moment, natural imperfect skin, phone selfie style"),
    ("medium_gym_workout", "amiranoor, medium shot, beautiful young woman at the gym, warm olive skin glistening with sweat, athletic crop top and leggings, mid-workout with dumbbells, bright gym lighting, confident strong expression, dark hair in high ponytail, fit physique"),

    # HALF/FULL BODY — dramatic compositions
    ("halfbody_beach_walking", "amiranoor, half body shot, beautiful young woman walking along the beach at golden hour, warm olive skin with tan lines, white bikini, feet in shallow waves, ocean spray, natural wind-blown dark hair, looking back over shoulder at camera, cinematic golden light"),
    ("halfbody_couch_reading", "amiranoor, half body shot, beautiful young woman curled up on a modern couch, warm olive skin, wearing cozy oversized sweater and shorts, reading on tablet, soft warm lamp light, evening mood, bare legs tucked under, relaxed natural pose, dark hair messy bun"),
    ("fullbody_street_fashion", "amiranoor, full body street style photo, beautiful young woman walking confidently on city sidewalk, warm olive skin, wearing trendy outfit with jacket and jeans, carrying bag, urban background with motion blur, shot from slight low angle, dark hair flowing, candid street photography"),
    ("fullbody_bed_morning", "amiranoor, full body shot, beautiful young woman lying in white bed sheets, morning light streaming through sheer curtains, warm olive skin, wearing silk camisole, stretching lazily, relaxed natural expression, tousled dark hair on pillow, soft dreamy atmosphere, bedroom setting"),
]

NEGATIVE = "(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (overly smooth:1.2), (unrealistic skin texture:1.1), (doll-like:1.2), (wax figure:1.1), (blurry skin texture:1.1), (cgi:1.2), (3d render:1.3), (digital art:1.2), ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, cartoon, anime, painting, illustration, overexposed, worst quality, jpeg artifacts, pale skin, multiple people, two faces, duplicate, cross-eyed, plastic looking"

# V2 CONFIG — key changes: ApplyInstantIDAdvanced with split controls
CONFIG = {
    "lora": "amiranoor_v4-step00001000.safetensors",
    "lora_str": 0.5,
    "ip_weight": 0.8,      # Identity preservation — keep HIGH
    "cn_strength": 0.35,    # Pose control — keep LOW for pose freedom
    "cfg": 3.5,
    "steps": 28,            # Slightly more steps for quality
}

QUALITY_THRESHOLD = 0.50  # Lowered slightly since poses are more varied now


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
        # --- Model Loading ---
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

        # --- Reference Image ---
        "5": {
            "class_type": "LoadImage",
            "inputs": {"image": ref_image}
        },

        # --- Text Encoding ---
        "10": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["2", 1]}
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": ["2", 1]}
        },

        # --- Latent ---
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },

        # --- InstantID Setup ---
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

        # --- V2: ApplyInstantIDAdvanced (separate ip_weight and cn_strength) ---
        "22": {
            "class_type": "ApplyInstantIDAdvanced",
            "inputs": {
                "instantid": ["20", 0],
                "insightface": ["23", 0],
                "control_net": ["21", 0],
                "image": ["5", 0],
                "model": ["2", 0],
                "positive": ["10", 0],
                "negative": ["11", 0],
                "ip_weight": cfg["ip_weight"],       # 0.8 — identity lock
                "cn_strength": cfg["cn_strength"],   # 0.35 — low for pose freedom
                "start_at": 0.0,
                "end_at": 1.0,
                "noise": 0.0,
                "combine_embeds": "average"
            }
        },

        # --- KSampler (main generation) ---
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

        # --- VAE Decode (initial image) ---
        "14": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["13", 0], "vae": ["1", 2]}
        },

        # --- V2: Face Detector for FaceDetailer ---
        "30": {
            "class_type": "UltralyticsDetectorProvider",
            "inputs": {"model_name": "bbox/face_yolov8m.pt"}
        },

        # --- V2: FaceDetailer (realistic skin refinement) ---
        "31": {
            "class_type": "FaceDetailer",
            "inputs": {
                "image": ["14", 0],
                "model": ["2", 0],
                "clip": ["2", 1],
                "vae": ["1", 2],
                "guide_size": 512,
                "guide_size_for": True,     # bbox mode
                "max_size": 1024,
                "seed": seed,
                "steps": 20,
                "cfg": 3.5,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "positive": ["10", 0],
                "negative": ["11", 0],
                "denoise": 0.42,            # Sweet spot: enough detail, not too much change
                "feather": 5,
                "noise_mask": True,
                "force_inpaint": True,
                "bbox_threshold": 0.5,
                "bbox_dilation": 10,
                "bbox_crop_factor": 1.3,    # Tight crop around face (NOT default 3.0)
                "sam_detection_hint": "center-1",
                "sam_dilation": 0,
                "sam_threshold": 0.93,
                "sam_bbox_expansion": 0,
                "sam_mask_hint_threshold": 0.7,
                "sam_mask_hint_use_negative": "False",
                "drop_size": 10,
                "bbox_detector": ["30", 0],
                "wildcard": "",
                "cycle": 1
            }
        },

        # --- Save (FaceDetailer output) ---
        "15": {
            "class_type": "SaveImage",
            "inputs": {"images": ["31", 0], "filename_prefix": f"v2/{prefix}"}
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


def wait_for_completion(prompt_id, timeout=300):
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
    print("=" * 60)
    print("PRODUCTION V2 — InstantIDAdvanced + FaceDetailer + LoRA v4")
    print("=" * 60)
    print(f"Config: ip_weight={CONFIG['ip_weight']}, cn_strength={CONFIG['cn_strength']}, "
          f"lora_str={CONFIG['lora_str']}, cfg={CONFIG['cfg']}, steps={CONFIG['steps']}")
    print()

    # Upload reference image
    ref_path = os.path.join(REF_DIR, BEST_REFS[0])
    print(f"Uploading reference: {BEST_REFS[0]}")
    ref_name = upload_image(ref_path)
    if not ref_name:
        print("FATAL: Reference upload failed")
        sys.exit(1)
    print(f"  -> {ref_name}")

    # Generate with 3 different seeds per prompt
    seeds = [42, 777, 1337]
    total = len(PROMPTS) * len(seeds)
    count = 0
    successes = 0
    generated_files = []
    print(f"\nGenerating {total} images ({len(PROMPTS)} prompts x {len(seeds)} seeds)...\n")

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

    print(f"\n{'=' * 60}")
    print(f"GENERATION: {successes}/{total} images")
    print(f"{'=' * 60}")

    # QUALITY GATE
    print("\n--- QUALITY GATE ---")
    print("Loading InsightFace for similarity check...")
    try:
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
            padded = cv2.copyMakeBorder(img, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            faces = app.get(padded)
            if faces:
                best = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
                ref_embeds.append(best.normed_embedding)
        if not ref_embeds:
            print("ERROR: No reference faces detected")
            sys.exit(1)
        ref_avg = np.mean(ref_embeds, axis=0)
        ref_avg = ref_avg / np.linalg.norm(ref_avg)
        print(f"Reference embedding built from {len(ref_embeds)} faces")

        # Score generated images
        out_dir = '/workspace/runpod-slim/ComfyUI/output/v2'
        passed_dir = os.path.join(out_dir, 'PASSED')
        failed_dir = os.path.join(out_dir, 'FAILED')
        os.makedirs(passed_dir, exist_ok=True)
        os.makedirs(failed_dir, exist_ok=True)

        results = []
        passed = 0
        failed = 0
        no_face = 0
        import shutil

        for f in sorted(glob.glob(os.path.join(out_dir, '*.png'))):
            img = cv2.imread(f)
            if img is None:
                continue
            padded = cv2.copyMakeBorder(img, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            faces = app.get(padded)
            basename = os.path.basename(f)
            name = basename.rsplit('_', 1)[0]  # strip ComfyUI suffix

            if faces:
                best = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
                sim = float(np.dot(ref_avg, best.normed_embedding))
                results.append((name, sim, basename))

                if sim >= QUALITY_THRESHOLD:
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
                shutil.copy2(f, os.path.join(failed_dir, basename))

        total_scored = passed + failed + no_face
        print(f"\n{'=' * 60}")
        print(f"QUALITY GATE RESULTS")
        print(f"  PASSED: {passed} (similarity >= {QUALITY_THRESHOLD})")
        print(f"  FAILED: {failed}")
        print(f"  NO FACE: {no_face}")
        if total_scored > 0:
            print(f"  Pass rate: {passed / total_scored * 100:.0f}%")

        if results:
            sims = [r[1] for r in results]
            print(f"\n  Avg similarity: {np.mean(sims):.4f}")
            print(f"  Min similarity: {np.min(sims):.4f}")
            print(f"  Max similarity: {np.max(sims):.4f}")
            best_r = max(results, key=lambda x: x[1])
            print(f"  Best: {best_r[0]} = {best_r[1]:.4f}")

            print(f"\nBY PROMPT TYPE:")
            for plabel, _ in PROMPTS:
                group = [r for r in results if r[0].startswith(plabel)]
                if group:
                    gavg = np.mean([r[1] for r in group])
                    gbest = max(group, key=lambda x: x[1])
                    print(f"  {plabel}: avg={gavg:.4f} best={gbest[1]:.4f}")

        print(f"\nPassed images in: {passed_dir}")
        print(f"Failed images in: {failed_dir}")
        print(f"{'=' * 60}")

    except Exception as e:
        print(f"Quality check failed: {e}")
        import traceback
        traceback.print_exc()
