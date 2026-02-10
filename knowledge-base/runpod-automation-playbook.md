# RunPod Automation Playbook

> Complete guide to setting up, maintaining, and scaling RunPod pods for Pistachio AI image generation.
> Last updated: 2026-02-10

---

## Table of Contents

1. [Pod From Scratch Setup (One-Click)](#pod-from-scratch-setup-one-click)
2. [Permanent Fixes Reference](#permanent-fixes-reference)
3. [The Full Startup Script](#the-full-startup-script)
4. [Notebooks Reference](#notebooks-reference)
5. [LoRA Training Pipeline](#lora-training-pipeline)
6. [Future Automation Opportunities](#future-automation-opportunities)
7. [Cost Tracking and Optimization](#cost-tracking-and-optimization)
8. [Replicating for a New Persona/Character](#replicating-for-a-new-personacharacter)

---

## Pod From Scratch Setup (One-Click)

### Prerequisites
- RunPod account with funds loaded
- RTX 4090 (24GB VRAM) pod selected
- Official "ComfyUI" template (creates `/workspace/runpod-slim/ComfyUI/`)

### Step-by-Step: Fresh Pod to Production-Ready

**Step 1: Deploy Pod**
1. Go to RunPod dashboard > Deploy > GPU Cloud
2. Select RTX 4090 (24GB VRAM), ~$0.60/hr
3. Template: "RunPod ComfyUI" (official)
4. Volume: 50GB persistent (/workspace)
5. Click Deploy

**Step 2: Open JupyterLab**
1. Wait for pod to show "Running"
2. Click "Connect" > "Jupyter Lab" (NOT the web terminal)
3. JupyterLab opens in browser

**Step 3: Upload and Run Setup Notebooks**

Upload these files from `C:\Users\Vital\Downloads\` to JupyterLab:
1. `fix_nodes_permanent.ipynb` - Installs custom nodes + creates permanent startup script
2. `download_models.ipynb` - Downloads all 5 core models (checkpoint, controlnet, insightface, ipadapter, instantid)
3. `download_clipvision.ipynb` - Downloads CLIP vision + FaceID LoRA models

Run order:
1. `fix_nodes_permanent.ipynb` (Shift+Enter) - Installs nodes, creates startup hooks, restarts ComfyUI
2. `download_models.ipynb` (Shift+Enter) - Downloads ~15GB of models
3. `download_clipvision.ipynb` (Shift+Enter) - Downloads CLIP vision + FaceID LoRA (~3GB)

**Step 4: Upload Reference Images**
- Upload Midjourney hero image(s) to `/workspace/runpod-slim/ComfyUI/input/`
- Use JupyterLab file browser (left sidebar) to drag and drop

**Step 5: Upload Workflow**
- Upload `InstantID-Pistachio.json` workflow to ComfyUI
- Open ComfyUI via RunPod proxy URL (the 8188 port link)
- Load workflow via ComfyUI menu

**Step 6: Verify Everything Works**
- No red X boxes in workflow (custom nodes loaded)
- ComfyUI Manager accessible (no database errors)
- Reference image loads in workflow
- Generate a test image

**Total setup time: ~20 minutes (mostly model downloads)**

---

## Permanent Fixes Reference

### Fix 1: SQLite Database Permissions
**Problem:** After pod migration, ComfyUI Manager's SQLite database becomes read-only. SQLite requires write access to both the .db file AND its parent directory (for WAL/journal files).

**Fix:**
```bash
chmod 666 /workspace/runpod-slim/ComfyUI/custom_nodes/ComfyUI-Manager/*.db 2>/dev/null
chmod 777 /workspace/runpod-slim/ComfyUI/custom_nodes/ComfyUI-Manager/ 2>/dev/null
```

**When it happens:** Every pod migration (RunPod moves your pod to a different physical host). Also possible after pod stop/start cycles.

### Fix 2: ComfyUI Frontend Pip Package
**Problem:** ComfyUI's frontend is now a separate pip package (`comfyui-frontend-package`), not bundled. Pod images may have an old/incompatible version.

**Fix:**
```bash
pip install --upgrade comfyui-frontend-package
```

**When it happens:** After pod migration, or when the ComfyUI backend updates but the frontend package doesn't auto-update.

### Fix 3: Custom Node Auto-Install
**Problem:** Custom nodes in `/workspace/runpod-slim/ComfyUI/custom_nodes/` disappear after pod restart/migration.

**Fix:**
```bash
cd /workspace/runpod-slim/ComfyUI/custom_nodes
git clone https://github.com/cubiq/ComfyUI_InstantID.git
pip install -r ComfyUI_InstantID/requirements.txt 2>/dev/null
git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
pip install -r ComfyUI_IPAdapter_plus/requirements.txt 2>/dev/null
```

**When it happens:** Any pod restart where the storage layer doesn't persist custom_nodes properly.

### Fix 4: Web Terminal Paste Issues
**Problem:** JupyterLab's web terminal mangles multi-line pasted commands (auto-indents, line breaks in URLs).

**Fix:** Never paste multi-line commands into the web terminal. Instead:
- Use `.ipynb` notebook files (upload to JupyterLab, run cells)
- Use `.sh` script files (upload, then `bash /workspace/script.sh`)
- For single commands, type them manually or use single-line paste

---

## The Full Startup Script

### `/workspace/startup.sh`

This is the master startup script. It runs on every pod boot via the post_start.sh hook.

```bash
#!/bin/bash
# === Pistachio Pod Startup Script ===
# Fixes ALL known issues on every boot. No manual intervention needed.
# Updated: 2026-02-10 - now includes ComfyUI auto-restart

# Fix 1: Database permissions (breaks on every pod migration)
chmod 666 /workspace/runpod-slim/ComfyUI/custom_nodes/ComfyUI-Manager/*.db 2>/dev/null
chmod 777 /workspace/runpod-slim/ComfyUI/custom_nodes/ComfyUI-Manager/ 2>/dev/null

# Fix 2: Update frontend pip package (frontend is a separate pip package now)
pip install --upgrade comfyui-frontend-package 2>/dev/null

# Fix 3: Auto-install custom nodes if missing
cd /workspace/runpod-slim/ComfyUI/custom_nodes

if [ ! -d "ComfyUI_InstantID" ]; then
    git clone https://github.com/cubiq/ComfyUI_InstantID.git
    pip install -r ComfyUI_InstantID/requirements.txt 2>/dev/null
    echo "Installed ComfyUI_InstantID"
fi

if [ ! -d "ComfyUI_IPAdapter_plus" ]; then
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
    pip install -r ComfyUI_IPAdapter_plus/requirements.txt 2>/dev/null
    echo "Installed ComfyUI_IPAdapter_plus"
fi

echo "Custom nodes ready."

# Fix 4: Restart ComfyUI after all fixes applied
# Kill any existing ComfyUI process and restart fresh
pkill -f "main.py" 2>/dev/null
sleep 2
cd /workspace/runpod-slim/ComfyUI
nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfyui.log 2>&1 &
echo "ComfyUI restarted."

echo "All startup fixes applied."
```

### `/workspace/runpod-slim/post_start.sh`

This is RunPod's hook file. It triggers our startup script:

```bash
#!/bin/bash
# Auto-install custom nodes and apply fixes on every boot
bash /workspace/startup.sh
```

**How the hook works:** The official RunPod ComfyUI template automatically runs `/workspace/runpod-slim/post_start.sh` after the container starts and before ComfyUI finishes loading. By placing our startup call there, all fixes apply transparently.

---

## Notebooks Reference

All notebooks are stored locally at `C:\Users\Vital\Downloads\` and uploaded to JupyterLab on the pod as needed.

| Notebook | Purpose | Run When |
|----------|---------|----------|
| `fix_nodes_permanent.ipynb` | Installs custom nodes NOW + creates startup.sh + hooks post_start.sh + restarts ComfyUI | First time on a fresh pod (one-time setup) |
| `download_models.ipynb` | Downloads all 5 core models: SDXL checkpoint, InstantID controlnet, InsightFace antelopev2, IP-Adapter, InstantID ip-adapter | First time on a fresh pod |
| `download_clipvision.ipynb` | Downloads CLIP-ViT-H-14 (2.5GB) + FaceID LoRA (371MB) | First time on a fresh pod |
| `install_nodes.ipynb` | Basic node installer (SUPERSEDED by fix_nodes_permanent.ipynb) | Do not use - kept for reference only |

---

## LoRA Training Pipeline

### Overview
Train a LoRA (Low-Rank Adaptation) on SDXL so the model learns Pistachio's face/body identity. After training, generate unlimited images with just a trigger word -- no reference image needed, zero content restrictions.

### PROVEN WORKING APPROACH (2026-02-10)

**Use a standalone Python script (`train_lora.py`), NOT notebook cells or terminal commands.**

The working training script lives at `/workspace/train_lora.py` on the pod. It uses `subprocess.run()` to call kohya's `sdxl_train_network.py` with all parameters. This approach:
- Avoids web terminal paste issues (multi-line commands break)
- Avoids notebook subprocess management issues
- Is portable, debuggable, and repeatable
- Auto-copies the final .safetensors to ComfyUI's loras folder when done

### Pinned Dependency Versions (CRITICAL)

These MUST be installed together BEFORE training. Do not install them separately or let pip resolve versions automatically.

```bash
pip install transformers==4.38.2 diffusers==0.25.1 huggingface_hub==0.21.4
```

**Why these specific versions:**
- `transformers>=4.39` removed `CLIPFeatureExtractor` (kohya uses it)
- `diffusers>=0.26` requires newer `huggingface_hub` that removed `cached_download`
- `huggingface_hub>=0.22` removed `cached_download` (kohya uses it)
- These three versions are tested and confirmed working together with kohya sd-scripts for SDXL

### Training Parameters That WORK on RTX 4090 (24GB VRAM)

```
Base model: SDXL 1.0 (sd_xl_base_1.0.safetensors)
Network type: LoRA
Network dim (rank): 32
Network alpha: 16
Learning rate: 1e-4
Text encoder LR: NOT USED (UNet only training)
Optimizer: AdamW8bit
Scheduler: cosine
Epochs: 3 (with 72 images = 1500 steps at 10 repeats)
Batch size: 1
Resolution: 1024
Mixed precision: fp16
Gradient checkpointing: ENABLED (required for 24GB)
--network_train_unet_only: ENABLED (SDXL too big for UNet + text encoder on 24GB)
Save every N steps: 500 (gives checkpoints at 500, 1000, 1500)
```

**CRITICAL FLAGS:**
- `--network_train_unet_only` -- REQUIRED for 24GB VRAM. Full SDXL training needs 48GB+.
- `--gradient_checkpointing` -- REQUIRED. Trades compute for VRAM. Without it, OOM on 24GB.
- Do NOT use `--cache_text_encoder_outputs` with `--text_encoder_lr` (they conflict: caching freezes the encoder, lr tries to train it)
- Do NOT use `--cache_text_encoder_outputs` with `--network_train_unet_only` (redundant and can cause errors)

### Actual Training Results (amiranoor_v1)
- **Output:** amiranoor_v1.safetensors (340.8 MB)
- **Location:** /workspace/runpod-slim/ComfyUI/models/loras/amiranoor_v1.safetensors
- **Trigger word:** "amiranoor"
- **Training images:** 72 (30 originals + duplicates from re-runs)
- **Effective dataset:** 720 images (10 repeats x 72)
- **Steps:** 1500 (3 epochs x 500 steps/epoch)
- **Checkpoints:** /workspace/lora_output/ at steps 500, 1000, 1500
- **Training time:** ~25-30 minutes on RTX 4090

### Full Pipeline: Image Prep -> Caption -> Train -> Deploy

**Phase 1: Image Preparation**
1. Generate 30 training images in Midjourney using `--oref [hero ID] --ow 250 --ar 9:16 --style raw`
2. Download all images from Midjourney
3. Crop/resize images to 1024x1024 (SDXL training resolution)
   - Use Python PIL/Pillow for batch processing
   - Center-crop to square, then resize to 1024x1024
   - Maintain aspect ratio diversity if using bucketing (512-1536 range)

**Phase 2: Captioning**
1. Create a `.txt` file for each image with the same filename (e.g., `image01.png` + `image01.txt`)
2. Every caption starts with the trigger word (e.g., `amiranoor`)
3. Caption format: `photo of amiranoor, a 21 year old woman with [description], [outfit], [setting], [lighting], [pose]`
4. Keep descriptions factual: what she looks like, what she's wearing, setting, lighting, pose
5. Variety in captions matters -- don't use the same template for every image

**Phase 3: Training**
1. Upload prepped images + captions to training data folder on the pod (e.g., `/workspace/lora_training/10_amiranoor/`)
   - Folder name format: `[repeats]_[trigger word]` (e.g., `10_amiranoor` = 10 repeats)
2. Install pinned dependencies: `pip install transformers==4.38.2 diffusers==0.25.1 huggingface_hub==0.21.4`
3. Upload and run `train_lora.py` script: `python3 /workspace/train_lora.py`
4. Training takes ~25-30 min on RTX 4090 with parameters above
5. Script auto-copies output to `/workspace/runpod-slim/ComfyUI/models/loras/`

**Phase 4: Deploy**
1. LoRA is auto-copied to ComfyUI by the training script
2. In ComfyUI workflow, add a "Load LoRA" node between the model loader and KSampler
3. Set trigger word in positive prompt: `photo of amiranoor, [rest of prompt]`
4. LoRA strength: 0.7-1.0 (start at 0.8, adjust up/down)
5. Can combine with InstantID + IP-Adapter for maximum consistency, or use LoRA alone for faster generation
6. Test all checkpoints (500, 1000, 1500 steps) to find optimal quality

### Training Data Breakdown (Current - amiranoor_v1)
- 72 training images total (30 originals + duplicates from re-runs)
- Mix of close-up face, three-quarter body, full body, variety angles
- All generated via Midjourney --oref
- 10 repeats per image in training = 720 effective samples

---

## Future Automation Opportunities

### 1. One-Click Pod Setup Script (Does EVERYTHING)

**Goal:** Single script that takes a bare RunPod pod from zero to fully configured in one command.

**What it would do:**
- Install all custom nodes (InstantID, IPAdapter, ComfyUI-Manager)
- Download all models (~15GB: SDXL checkpoint, InstantID, IP-Adapter, InsightFace, CLIP Vision, FaceID LoRA)
- Apply all permanent fixes (DB permissions, frontend update, startup hooks)
- Set up LoRA training environment (kohya_ss, dataset directories, config files)
- Upload workflow JSON files
- Create and hook startup.sh + post_start.sh
- Print a final status report with the proxy URL

**Implementation:** Combine `runpod-comfyui-setup.sh` + `fix_nodes_permanent.ipynb` + `download_clipvision.ipynb` logic into one master script. Store as `tools/runpod-one-click-setup.sh`.

**Time savings:** Reduces 20+ minute manual setup to one command that runs unattended.

### 2. Automated Image Prep Pipeline

**Goal:** Upload raw Midjourney images -> auto crop/resize/caption -> ready for LoRA training.

**What it would do:**
- Accept a folder of raw images
- Auto-detect faces and crop to square (face-centered)
- Resize to 1024x1024 (or use bucketing for variable aspect ratios)
- Auto-caption using BLIP-2 or Florence-2 (running on the pod GPU)
- Prepend trigger word to all captions
- Output organized training-ready dataset

**Implementation:** Python script using Pillow, InsightFace (for face detection), and a captioning model. Run on the pod's GPU.

**Time savings:** Eliminates manual cropping and captioning of 30+ images.

### 3. Batch Generation Pipeline

**Goal:** Feed a list of prompts -> get generated images automatically.

**What it would do:**
- Accept a .txt or .json file with prompts
- Queue all prompts in ComfyUI
- Generate images with consistent settings (LoRA, InstantID, etc.)
- Save outputs to organized folders with metadata
- Optional: auto-watermark, auto-resize for different platforms

**Implementation:** Use ComfyUI's API endpoint (`/prompt`) to queue generations programmatically. Python script that reads prompts and posts to the API.

**Time savings:** Generate 50-100 images unattended instead of manually queueing one at a time.

### 4. API Endpoint for ComfyUI (Headless Generation for Chatbot Integration)

**Goal:** Expose ComfyUI as an API that the AI chatbot (Clawra/OpenClaw) can call to generate images on demand.

**What it would do:**
- REST API wrapper around ComfyUI's `/prompt` and `/history` endpoints
- Accept: prompt text, reference image (optional), generation parameters
- Return: generated image URL/base64
- Authentication layer for security
- Rate limiting to control costs

**Implementation:** FastAPI or Flask wrapper deployed on the same pod, proxied through RunPod's serverless or HTTP proxy. The chatbot sends a request, the API queues it in ComfyUI, polls for completion, returns the image.

**Why it matters:** This is the bridge between the AI girlfriend chatbot (WhatsApp/Telegram) and the image generation pipeline. Subscriber asks for a selfie -> chatbot calls API -> ComfyUI generates -> subscriber gets the image.

**Architecture:**
```
Subscriber (WhatsApp/Telegram)
    |
OpenClaw / Chatbot LLM
    |
ComfyUI API Wrapper (FastAPI on pod)
    |
ComfyUI (LoRA + InstantID pipeline)
    |
Generated Image -> sent back to subscriber
```

### 5. Template Pod Image (Everything Pre-Installed)

**Goal:** Save the fully configured pod as a RunPod template/snapshot so new pods start ready to go.

**What it would do:**
- Snapshot current pod state (all models, nodes, scripts, hooks installed)
- Create a custom RunPod template from the snapshot
- New pods deployed from this template start with everything pre-installed
- No setup time, no downloads, no fixes needed

**Implementation:** RunPod supports creating templates from running pods. Once the pod is fully configured:
1. Stop the pod
2. Go to RunPod dashboard > My Templates > Create Template
3. Use the pod's volume as the base
4. Deploy new pods from this template

**Time savings:** Zero setup time for new pods. Also useful for scaling (spin up multiple pods for batch generation).

**Cost note:** Custom templates may have storage costs for the saved volume. Compare against re-downloading models each time.

---

## Cost Tracking and Optimization

### Current Costs
| Item | Cost | Frequency |
|------|------|-----------|
| RTX 4090 pod (running) | ~$0.60/hr | Per hour while active |
| RTX 4090 pod (stopped) | ~$0.01/hr | Idle storage cost |
| Volume storage (50GB) | Included | With pod |
| Midjourney subscription | $30/mo | Monthly |
| **Estimated monthly (moderate use)** | **$50-80** | **~80 hrs pod time + MJ** |

### Optimization Strategies

**1. Stop the pod when not using it**
- Running cost: $0.60/hr = $14.40/day if left on
- Stopped cost: $0.01/hr = $0.24/day
- Rule: Always stop the pod after a session. Never leave it running overnight.

**2. Use the right GPU for the task**
- LoRA training: RTX 4090 (24GB VRAM) - worth the cost, training is time-sensitive
- Image generation: RTX 4080 or even RTX 3090 may suffice for inference at lower cost
- Batch generation: Consider RTX 4090 for speed, but cheaper GPUs work if time is not critical

**3. Batch your work**
- Don't spin up the pod for one image. Queue up 20-50 prompts, generate them all, stop the pod.
- LoRA training + batch generation in one session = most efficient use of pod time.

**4. Terminate duplicate/migration pods**
- After pod migration, the OLD pod may still exist and charge idle storage
- Check dashboard for duplicate pods and terminate the old one

**5. Pre-download models to a persistent volume**
- Models (~15GB) persist on `/workspace/` between pod stops
- Only re-download if the volume is wiped (rare) or if you terminate the pod entirely
- Stopping (not terminating) preserves the volume

**6. Consider RunPod Serverless for production**
- For the API endpoint (chatbot integration), RunPod Serverless charges per-second only when processing
- No idle cost. Scale to zero when no requests.
- Better for production workloads with variable demand

### Break-Even Analysis
- LoRA training: ~$0.50-1.00 one-time cost (30-60 min on RTX 4090)
- Per image generation: ~$0.005-0.01 (each image takes ~10-20 seconds on RTX 4090)
- After LoRA training, marginal cost per image is essentially zero (just GPU time)
- Compare to Midjourney: $30/mo for limited generations vs unlimited on your own pod

---

## Replicating for a New Persona/Character

### The Template Process

To create a new AI persona (different face, different brand), the pipeline is identical. Only three things change:

1. **Trigger word** - Change `pistachio_character` to `newpersona_character`
2. **Training images** - Generate new Midjourney images with a different hero/reference image
3. **Captions** - New captions with the new trigger word and character description

### Step-by-Step Replication

**1. Create the new persona identity**
- Generate a hero image in Midjourney (face, body type, skin tone, features)
- Save the hero image as the reference for --oref

**2. Generate training data**
- Use the same 30-prompt template (8 close-up, 10 three-quarter, 8 full body, 4 variety)
- Replace character description with new persona
- Generate all 30 images using `--oref [new hero] --ow 250 --ar 9:16 --style raw`

**3. Prep and caption**
- Same crop/resize pipeline (1024x1024)
- Same captioning approach, different trigger word and description
- Example: `photo of aurora_character, a 23 year old Scandinavian woman with...`

**4. Train a new LoRA**
- Same training settings (network_dim 32, alpha 16, 10 epochs, etc.)
- Different output name: `aurora_lora_v1.safetensors`
- Same ~30-60 min training time

**5. Deploy**
- Copy new LoRA to `models/loras/`
- Load in ComfyUI workflow with new trigger word
- Same InstantID + IP-Adapter combo works for additional face consistency

**6. Generate content**
- Same batch generation pipeline, different prompts for the new persona
- Same chatbot integration (just swap which LoRA to load)

### Scaling Notes
- Multiple LoRAs can coexist on the same pod (just load a different one per workflow)
- Each LoRA is ~150-350MB (amiranoor_v1 was 340.8MB at dim 32) -- storage is not an issue
- Training time scales linearly: 2 personas = 2 hours of training, not 4
- The startup script, model downloads, and custom nodes are shared -- only the LoRA is persona-specific
- A single pod can serve multiple personas by swapping LoRAs in the API call

### Business Scaling Path
```
1 persona  ->  Prove the model (revenue, engagement, chatbot conversion)
2 personas ->  Test replication speed and audience overlap
5 personas ->  Hire VA for content posting, automate generation pipeline
10+ personas -> Full automation: API endpoint, scheduled generation, multi-platform posting
```

The infrastructure cost stays roughly the same. More personas = more LoRAs (tiny files) + more generation time (pennies per image). The bottleneck shifts from tech to content strategy and audience building.

---

*Created by Pistachio CoS Agent - 2026-02-10*
