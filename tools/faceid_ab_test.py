#!/usr/bin/env python3
"""
A/B Test: Pure FaceID (no LoRA) vs LoRA + FaceID with lower LoRA weight
Tests if removing the LoRA improves face matching
"""
import json, urllib.request, time, os, sys

COMFYUI_URL = "http://127.0.0.1:8188"
REF_IMAGE = "/workspace/lora_dataset_v3/10_amiranoor/img_001.png"

PROMPTS = [
    ("portrait", "a beautiful young Egyptian-Brazilian woman, close up portrait photo, natural lighting, soft smile, looking at camera, photorealistic, 8k, detailed skin texture, pores, natural skin, warm skin tone"),
    ("halfbody", "a beautiful young Egyptian-Brazilian woman, half body shot, casual elegant outfit, urban background, golden hour, photorealistic, 8k, natural skin texture, warm skin tone"),
    ("glamour", "a stunning young Egyptian-Brazilian woman, glamour photography, studio lighting, elegant pose, photorealistic, 8k, fashion photo, natural skin, warm lighting"),
    ("beach", "a beautiful young Egyptian-Brazilian woman, beach setting, sunset lighting, natural pose, wind in hair, photorealistic, 8k, natural skin, warm tones"),
]

# Test configs
CONFIGS = [
    # Pure FaceID - no LoRA at all
    {"label": "pure_faceid_fw0.9", "lora": None, "faceid_w": 0.9, "faceid_lora_str": 0.6},
    {"label": "pure_faceid_fw1.2", "lora": None, "faceid_w": 1.2, "faceid_lora_str": 0.6},
    # Very low LoRA + strong FaceID
    {"label": "lowlora_fw1.0", "lora": "amiranoor_v3-step00001000.safetensors", "lora_str": 0.3, "faceid_w": 1.0, "faceid_lora_str": 0.6},
    # Medium LoRA + strong FaceID
    {"label": "medlora_fw1.0", "lora": "amiranoor_v3-step00001500.safetensors", "lora_str": 0.5, "faceid_w": 1.0, "faceid_lora_str": 0.6},
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


def make_workflow_no_lora(uploaded_name, faceid_w, faceid_lora_str, prompt, seed, prefix):
    """Workflow WITHOUT LoRA - pure FaceID face lock"""
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "realvisxl_v5.safetensors"}
        },
        "3": {
            "class_type": "IPAdapterUnifiedLoaderFaceID",
            "inputs": {
                "model": ["1", 0],
                "preset": "FACEID PLUS V2",
                "lora_strength": faceid_lora_str,
                "provider": "CUDA"
            }
        },
        "4": {
            "class_type": "IPAdapterFaceID",
            "inputs": {
                "model": ["3", 0],
                "ipadapter": ["3", 1],
                "image": ["5", 0],
                "weight": faceid_w,
                "weight_faceidv2": faceid_w,
                "weight_type": "linear",
                "combine_embeds": "concat",
                "start_at": 0.0,
                "end_at": 1.0,
                "embeds_scaling": "V only",
                "insightface": ["6", 0]
            }
        },
        "5": {
            "class_type": "LoadImage",
            "inputs": {"image": uploaded_name}
        },
        "6": {
            "class_type": "IPAdapterInsightFaceLoader",
            "inputs": {"provider": "CUDA", "model_name": "antelopev2"}
        },
        "10": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["1", 1]}
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, airbrushed skin, plastic skin, overly smooth skin, cgi, 3d render, pale skin",
                "clip": ["1", 1]
            }
        },
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },
        "13": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["4", 0],
                "positive": ["10", 0],
                "negative": ["11", 0],
                "latent_image": ["12", 0],
                "seed": seed,
                "steps": 30,
                "cfg": 7.0,
                "sampler_name": "euler_ancestral",
                "scheduler": "normal",
                "denoise": 1.0
            }
        },
        "14": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["13", 0], "vae": ["1", 2]}
        },
        "15": {
            "class_type": "SaveImage",
            "inputs": {"images": ["14", 0], "filename_prefix": f"abtest/{prefix}"}
        }
    }


def make_workflow_with_lora(uploaded_name, lora_name, lora_str, faceid_w, faceid_lora_str, prompt, seed, prefix):
    """Workflow WITH LoRA + FaceID face lock"""
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "realvisxl_v5.safetensors"}
        },
        "2": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0], "clip": ["1", 1],
                "lora_name": lora_name,
                "strength_model": lora_str,
                "strength_clip": lora_str
            }
        },
        "3": {
            "class_type": "IPAdapterUnifiedLoaderFaceID",
            "inputs": {
                "model": ["2", 0],
                "preset": "FACEID PLUS V2",
                "lora_strength": faceid_lora_str,
                "provider": "CUDA"
            }
        },
        "4": {
            "class_type": "IPAdapterFaceID",
            "inputs": {
                "model": ["3", 0],
                "ipadapter": ["3", 1],
                "image": ["5", 0],
                "weight": faceid_w,
                "weight_faceidv2": faceid_w,
                "weight_type": "linear",
                "combine_embeds": "concat",
                "start_at": 0.0,
                "end_at": 1.0,
                "embeds_scaling": "V only",
                "insightface": ["6", 0]
            }
        },
        "5": {
            "class_type": "LoadImage",
            "inputs": {"image": uploaded_name}
        },
        "6": {
            "class_type": "IPAdapterInsightFaceLoader",
            "inputs": {"provider": "CUDA", "model_name": "antelopev2"}
        },
        "10": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["2", 1]}
        },
        "11": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "ugly, deformed, blurry, low quality, distorted face, extra fingers, bad anatomy, watermark, text, disfigured, airbrushed skin, plastic skin, overly smooth skin, cgi, 3d render, pale skin",
                "clip": ["2", 1]
            }
        },
        "12": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
        },
        "13": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["4", 0],
                "positive": ["10", 0],
                "negative": ["11", 0],
                "latent_image": ["12", 0],
                "seed": seed,
                "steps": 30,
                "cfg": 7.0,
                "sampler_name": "euler_ancestral",
                "scheduler": "normal",
                "denoise": 1.0
            }
        },
        "14": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["13", 0], "vae": ["1", 2]}
        },
        "15": {
            "class_type": "SaveImage",
            "inputs": {"images": ["14", 0], "filename_prefix": f"abtest/{prefix}"}
        }
    }


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
    print("Uploading reference face image...")
    uploaded_name = upload_image(REF_IMAGE)
    if not uploaded_name:
        print("FATAL: Could not upload reference image")
        sys.exit(1)
    print(f"  -> Uploaded as: {uploaded_name}")

    total = len(CONFIGS) * len(PROMPTS)
    count = 0
    successes = 0
    print(f"\nRunning {total} A/B test generations...\n")

    for cfg in CONFIGS:
        for pi, (plabel, prompt) in enumerate(PROMPTS):
            count += 1
            prefix = f"{cfg['label']}_{plabel}"
            print(f"[{count}/{total}] {prefix}")

            if cfg["lora"] is None:
                workflow = make_workflow_no_lora(
                    uploaded_name, cfg["faceid_w"], cfg["faceid_lora_str"],
                    prompt, 42 + pi, prefix
                )
            else:
                workflow = make_workflow_with_lora(
                    uploaded_name, cfg["lora"], cfg["lora_str"],
                    cfg["faceid_w"], cfg["faceid_lora_str"],
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
    print(f"A/B TEST COMPLETE: {successes}/{total} images")
    print(f"Results in: /workspace/runpod-slim/ComfyUI/output/abtest/")
    print(f"{'='*50}")
