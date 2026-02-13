# CODEX EXECUTION BRIEFING — Pistachio LoRA Training Pipeline

## YOUR MISSION
You are executing the complete LoRA training pipeline for Project Pistachio on a RunPod GPU instance. This involves installing tools, downloading models, captioning images, configuring training, running training, and extracting the best LoRA checkpoint. Everything below is the knowledge you need.

---

## PROJECT CONTEXT

**Project:** Pistachio — AI image generation business building consistent character images
**Team:** Vitaley (business lead), Mark (workflow practitioner), Matt (partner)
**Character:** Amira Noor, 21, Egyptian/Brazilian mix. Trigger word: "amiranoor"
**Goal:** Train a LoRA (Low-Rank Adaptation) fine-tune on a base model so that every time the trigger word "amiranoor" is used in a prompt, the model generates the same consistent face.

**Previous approach (being replaced):** SDXL + InstantID + FaceDetailer + Kohya LoRA training
**New approach (you are executing):** Wan 2.1 T2V-14B + DiffusionPipe LoRA training + JoyCaption captioning + wandb evaluation

**Why the new approach:**
- DiffusionPipe provides wandb evaluation graphs so you can pick the mathematically best checkpoint (no guesswork)
- Wan 2.1 produces better results than SDXL for this use case
- All tools are 100% open-source, no Discord paywalls

---

## RUNPOD POD DETAILS

- **Pod Name:** yabbering_orange_mammal_migration
- **Pod ID:** on91uybqyagtnk
- **GPU:** RTX 4090 (24GB VRAM) — Cost: ~$0.60/hr
- **Storage:** 50GB persistent at /workspace
- **Services running:** FileBrowser (8080), ComfyUI (8188), JupyterLab (8888)
- **SSH Key:** Located at `C:\Users\Vital\.ssh\id_ed25519`
- **SSH public key:** `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ56MCk0GjScua9CY5VPbWWvuJ95Gj7JKxEc4r+DLkUe vitaleysha@gmail.com`

### SSH Connection Methods (try in order):
1. **Exposed TCP:** `ssh -i ~/.ssh/id_ed25519 -p 11925 -o StrictHostKeyChecking=no -T root@213.173.99.10`
2. **RunPod proxy:** `ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no -T on91uybqyagtnk-64410dec@ssh.runpod.io`
3. **JupyterLab:** `https://on91uybqyagtnk-8888.proxy.runpod.net/` (may need token)
4. **FileBrowser:** `https://on91uybqyagtnk-8080.proxy.runpod.net/`

**Known SSH issues:**
- Exposed TCP previously hung/timed out. May work now if pod was restarted.
- RunPod proxy returned "Your SSH client doesn't support PTY" — try with `-T` flag, or try `ssh -o RequestTTY=no`.
- JupyterLab returned 403. May need auth token from pod logs.
- If SSH key not recognized after pod migration, add it via RunPod web terminal or dashboard.

### Existing stuff on the pod from previous work:
- ComfyUI at `/workspace/runpod-slim/ComfyUI/`
- Previous LoRA checkpoints (v3, v4) in ComfyUI loras folder
- Previous scripts: `instantid_production_v2.py`, `retrain_lora_v4.py`, `startup_v2.sh`, etc.
- epiCRealism XL checkpoint at `models/checkpoints/epicrealismxl.safetensors`
- **DO NOT delete any existing files. The new pipeline goes in separate directories.**

---

## COMPLETE TECHNICAL KNOWLEDGE

### What is a LoRA and Why Train One

Base image models contain millions of training images but can never produce a consistent face. Every generation gives a different person. LoRA training solves this:
- Feed 20+ images of your character into the base model
- Caption each image with a unique trigger word (e.g., "amiranoor")
- The model learns to associate that trigger word with that specific face
- After training, using the trigger word in any prompt produces the same consistent face

### The Three Tools

**1. JoyCaption** — Automated image captioning
- Repo: `github.com/MNeMoNiCuZ/joy-caption-batch`
- Takes a folder of images, generates a `.txt` description file for each one
- Example: image of woman → "amiranoor, a young woman with dark hair sitting on a wooden chair in a sunlit room"
- The trigger word is PREPENDED to every caption automatically
- Model auto-downloads on first run (~17.9GB from HuggingFace: `fancyfeast/llama-joycaption-alpha-two-hf-llava`)

Key settings in `batch-alpha2.py`:
- `PREPEND_STRING = "amiranoor, "` — trigger word prepended to all captions
- `BATCH_PROCESSING_COUNT = 4` — images at once (use 4 for 24GB GPU, 8 for 48GB+)
- `INPUT_FOLDER` — default: `./input/`
- `OVERWRITE = True`
- `MAX_NEW_TOKENS = 300`
- `TEMPERATURE = 0.5`

**2. DiffusionPipe** — LoRA training framework
- Repo: `github.com/tdrussell/diffusion-pipe`
- Config format: TOML files
- Key advantage: Built-in wandb evaluation graphs for picking best checkpoint
- Supports Wan 2.1, Flux, SDXL, HunyuanVideo, LTX-Video, and 20+ models
- Training command:
```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
NCCL_P2P_DISABLE="1" NCCL_IB_DISABLE="1" \
deepspeed --num_gpus=1 train.py --deepspeed --config examples/training_config.toml
```

**3. wandb (Weights & Biases)** — Training monitoring
- Free account at wandb.ai
- Shows real-time loss graphs during training
- Loss goes DOWN = learning
- Loss BOTTOMS OUT = convergence = BEST checkpoint
- Loss goes UP or shows overfit artifacts = overtrained
- Pick the checkpoint at the lowest point on the graph

### Wan 2.1 Base Model

**What:** 14B parameter open-source diffusion model. Apache 2.0 licensed. Freely downloadable.

**Files needed (total ~36GB):**

| File | Size | Source | Purpose |
|------|------|--------|---------|
| Wan2.1-T2V-14B config dir | ~520MB | Wan-AI/Wan2.1-T2V-14B on HuggingFace | config.json needed by DiffusionPipe |
| wan2.1_t2v_14B_fp16.safetensors | ~28.6GB | Comfy-Org/Wan_2.1_ComfyUI_repackaged | Diffusion transformer |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | ~6.7GB | Comfy-Org/Wan_2.1_ComfyUI_repackaged | Text encoder |
| wan_2.1_vae.safetensors | ~254MB | Comfy-Org/Wan_2.1_ComfyUI_repackaged | VAE decoder |

No HuggingFace authentication needed — all Apache 2.0, no gating.

**Wan 2.1 vs 2.2:** Wan 2.2 uses Mixture-of-Experts (27B params). More complex to train. Stick with 2.1.

### GPU Memory Optimization (Critical for 24GB RTX 4090)

The tutorial video used an H200 (80GB VRAM, $3.50/hr). We're using RTX 4090 (24GB VRAM, $0.60/hr). These settings compensate:

| Setting | H200 (80GB) | RTX 4090 (24GB) |
|---------|-------------|-----------------|
| micro_batch_size_per_gpu | 8 | **1** |
| gradient_accumulation_steps | 1 | **4-8** |
| activation_checkpointing | optional | **true** (required) |
| blocks_to_swap | 0 | **24-32** (offloads transformer blocks from VRAM to RAM) |
| transformer_dtype | bfloat16 | **float8** (halves transformer memory) |
| optimizer | AdamW | **AdamW8bitKahan** (8-bit optimizer uses less VRAM) |

**Gradient accumulation** makes results mathematically equivalent:
- Effective Batch = micro_batch × gradient_accumulation
- 1 × 8 = 8 (same effective batch as H200's 8 × 1 = 8)
- Just takes longer per step, same quality

### Key Concepts

- **Convergence:** The point on the loss graph where it bottoms out. This is the best checkpoint.
- **Overtrained:** Model memorized training images. Can only reproduce training data, can't generalize. Happens past convergence.
- **Undertrained:** Model hasn't learned enough. Can't reproduce the face consistently. Happens before convergence.
- **Epoch:** One complete pass through all training images.
- **Trigger word:** Unique token ("amiranoor") that activates the LoRA character in prompts. Must be something not in the base model's training data.

---

## THE 6 SCRIPTS TO EXECUTE

### Script 1: install_joycaption.sh
Run in Terminal 1 on JupyterLab. Creates `/workspace/joy-caption-batch/`.

```bash
#!/bin/bash
set -e
echo "=========================================="
echo "  Installing JoyCaption Batch Captioner"
echo "=========================================="

cd /workspace

if [ ! -d "joy-caption-batch" ]; then
    echo "[1/4] Cloning joy-caption-batch..."
    git clone https://github.com/MNeMoNiCuZ/joy-caption-batch.git
else
    echo "[1/4] joy-caption-batch already exists, pulling latest..."
    cd joy-caption-batch && git pull && cd ..
fi

cd joy-caption-batch

echo "[2/4] Creating Python virtual environment..."
python -m venv venv
source venv/bin/activate

echo "[3/4] Installing PyTorch with CUDA 12.8..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

echo "[4/4] Installing requirements..."
pip install -r requirements.txt

mkdir -p input

echo ""
echo "=========================================="
echo "  JoyCaption installed successfully!"
echo "=========================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Put your 20+ images into: /workspace/joy-caption-batch/input/"
echo "  2. Edit batch-alpha2.py to set your trigger word:"
echo "     PREPEND_STRING = \"amiranoor, \""
echo "  3. Set BATCH_PROCESSING_COUNT = 4 (for 24GB GPU)"
echo "  4. Activate environment: source /workspace/joy-caption-batch/venv/bin/activate"
echo "  5. Run: cd /workspace/joy-caption-batch && python batch-alpha2.py"
echo "  6. Caption model (~17.9GB) will auto-download on first run"
echo ""
```

### Script 2: download_wan_models.sh
Run in Terminal 2. Downloads ~36GB of model files. Takes a while.

```bash
#!/bin/bash
set -e
echo "=========================================="
echo "  Downloading Wan 2.1 Base Models"
echo "=========================================="

mkdir -p /workspace/models/wan
cd /workspace/models/wan

echo "[1/4] Downloading Wan 2.1 T2V-14B config directory (~520MB)..."
if [ ! -d "Wan2.1-T2V-14B" ]; then
    pip install -q huggingface_hub
    huggingface-cli download Wan-AI/Wan2.1-T2V-14B \
        --local-dir Wan2.1-T2V-14B \
        --exclude "diffusion_pytorch_model*" "models_t5*"
    echo "  Config directory downloaded."
else
    echo "  Config directory already exists, skipping."
fi

echo "[2/4] Downloading diffusion model — wan2.1_t2v_14B_fp16.safetensors (~28.6GB)..."
echo "  (This is the largest file. Be patient.)"
if [ ! -f "wan2.1_t2v_14B_fp16.safetensors" ]; then
    wget -c -O wan2.1_t2v_14B_fp16.safetensors \
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/diffusion_models/wan2.1_t2v_14B_fp16.safetensors"
    echo "  Diffusion model downloaded."
else
    echo "  Diffusion model already exists, skipping."
fi

echo "[3/4] Downloading text encoder — umt5_xxl_fp8_e4m3fn_scaled.safetensors (~6.7GB)..."
if [ ! -f "umt5_xxl_fp8_e4m3fn_scaled.safetensors" ]; then
    wget -c -O umt5_xxl_fp8_e4m3fn_scaled.safetensors \
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors"
    echo "  Text encoder downloaded."
else
    echo "  Text encoder already exists, skipping."
fi

echo "[4/4] Downloading VAE — wan_2.1_vae.safetensors (~254MB)..."
if [ ! -f "wan_2.1_vae.safetensors" ]; then
    wget -c -O wan_2.1_vae.safetensors \
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors"
    echo "  VAE downloaded."
else
    echo "  VAE already exists, skipping."
fi

echo ""
echo "=========================================="
echo "  All Wan 2.1 models downloaded!"
echo "=========================================="
echo ""
echo "FILES DOWNLOADED TO: /workspace/models/wan/"
ls -lh /workspace/models/wan/*.safetensors 2>/dev/null || true
echo ""
echo "TOTAL DISK USAGE:"
du -sh /workspace/models/wan/
echo ""
```

### Script 3: install_diffusion_pipe.sh
Run in Terminal 3. **IMPORTANT: Wait until JoyCaption install finishes first** to avoid Python environment conflicts.

```bash
#!/bin/bash
set -e
echo "=========================================="
echo "  Installing DiffusionPipe LoRA Trainer"
echo "=========================================="

cd /workspace

if [ ! -d "diffusion-pipe" ]; then
    echo "[1/5] Cloning diffusion-pipe (with submodules)..."
    git clone --recurse-submodules https://github.com/tdrussell/diffusion-pipe.git
else
    echo "[1/5] diffusion-pipe already exists, updating..."
    cd diffusion-pipe
    git pull
    git submodule update --init --recursive
    cd ..
fi

cd diffusion-pipe

echo "[2/5] Setting up Python environment..."
if command -v conda &> /dev/null; then
    echo "  Using conda..."
    conda create -n diffusion-pipe python=3.12 -y 2>/dev/null || true
    source activate diffusion-pipe 2>/dev/null || conda activate diffusion-pipe
else
    echo "  Conda not found, using venv..."
    python -m venv venv
    source venv/bin/activate
fi

echo "[3/5] Installing PyTorch..."
pip install torch torchvision

if command -v conda &> /dev/null; then
    echo "[3.5/5] Installing CUDA NVCC via conda..."
    conda install -c nvidia cuda-nvcc -y 2>/dev/null || true
fi

echo "[4/5] Installing requirements (this takes a few minutes)..."
pip install -r requirements.txt

echo "[5/5] Installing flash-attn (optional, may take a while)..."
pip install flash-attn 2>/dev/null || echo "  flash-attn install failed (non-critical, training will still work)"

echo ""
echo "=========================================="
echo "  DiffusionPipe installed successfully!"
echo "=========================================="
echo ""
echo "ACTIVATION COMMAND:"
if command -v conda &> /dev/null; then
    echo "  conda activate diffusion-pipe"
else
    echo "  source /workspace/diffusion-pipe/venv/bin/activate"
fi
echo ""
echo "TRAINING COMMAND (after configuring your .toml files):"
echo "  cd /workspace/diffusion-pipe"
echo "  PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \\"
echo "  NCCL_P2P_DISABLE=\"1\" NCCL_IB_DISABLE=\"1\" \\"
echo "  deepspeed --num_gpus=1 train.py --deepspeed --config examples/training_config.toml"
echo ""
```

### Config 1: training_config.toml
Place at `/workspace/diffusion-pipe/examples/training_config.toml`

```toml
# ============================================================
# PISTACHIO — DiffusionPipe Training Config (Wan 2.1 T2V-14B)
# Optimized for RTX/budget GPUs (24-48GB VRAM)
# ============================================================

# --- OUTPUT ---
output_dir = '/workspace/training_output'

# --- DATASET ---
dataset = '/workspace/diffusion-pipe/examples/dataset_config.toml'
eval_datasets = [
    {name = 'eval', config = '/workspace/diffusion-pipe/examples/eval_dataset_config.toml'},
]

# --- TRAINING SETTINGS ---
epochs = 1000
micro_batch_size_per_gpu = 1
pipeline_stages = 1
gradient_accumulation_steps = 4
gradient_clipping = 1.0
warmup_steps = 10

# --- MEMORY OPTIMIZATION (for 24-48GB GPUs) ---
activation_checkpointing = true
blocks_to_swap = 24
caching_batch_size = 1
partition_method = 'parameters'

# --- EVAL SETTINGS ---
eval_every_n_epochs = 1
eval_before_first_step = true
eval_micro_batch_size_per_gpu = 1
eval_gradient_accumulation_steps = 1

# --- SAVING ---
save_every_n_steps = 50
save_dtype = 'bfloat16'
checkpoint_every_n_minutes = 120
steps_per_print = 1

# --- MISC ---
video_clip_mode = 'single_beginning'

# --- MODEL ---
[model]
type = 'wan'
ckpt_path = '/workspace/models/wan/Wan2.1-T2V-14B'
transformer_path = '/workspace/models/wan/wan2.1_t2v_14B_fp16.safetensors'
llm_path = '/workspace/models/wan/umt5_xxl_fp8_e4m3fn_scaled.safetensors'
dtype = 'bfloat16'
transformer_dtype = 'float8'
timestep_sample_method = 'logit_normal'

# --- LORA ADAPTER ---
[adapter]
type = 'lora'
rank = 32
dtype = 'bfloat16'

# --- OPTIMIZER (8-bit for lower VRAM) ---
[optimizer]
type = 'AdamW8bitKahan'
lr = 2e-5
betas = [0.9, 0.99]
weight_decay = 0.01
stabilize = false

# --- MONITORING (wandb) ---
# Create free account at wandb.ai and get your API key
[monitoring]
enable_wandb = true
wandb_api_key = 'PASTE_YOUR_WANDB_API_KEY_HERE'
wandb_tracker_name = 'pistachio-lora'
wandb_run_name = 'run1'
```

### Config 2: dataset_config.toml
Place at `/workspace/diffusion-pipe/examples/dataset_config.toml`

```toml
# ============================================================
# PISTACHIO — Dataset Config (Training Data)
# Points to your TRAIN folder with captioned images
# ============================================================

resolutions = [512]

enable_ar_bucket = true
min_ar = 0.5
max_ar = 2.0
num_ar_buckets = 7

frame_buckets = [1]

[[directory]]
path = '/workspace/dataset/train'
num_repeats = 4
```

### Config 3: eval_dataset_config.toml
Place at `/workspace/diffusion-pipe/examples/eval_dataset_config.toml`

```toml
# ============================================================
# PISTACHIO — Eval Dataset Config
# Points to your EVAL folder (20% of captioned images)
# Used for convergence graphs on wandb
# ============================================================

resolutions = [512]

enable_ar_bucket = true
min_ar = 0.5
max_ar = 2.0
num_ar_buckets = 7

frame_buckets = [1]

[[directory]]
path = '/workspace/dataset/eval'
num_repeats = 1
```

---

## EXECUTION PLAN (Step by Step)

### Phase 1: IMAGE COLLECTION (User does this manually)
- Collect 20+ consistent images of Amira Noor (varied poses, settings, same face)
- Upload images to the pod at `/workspace/joy-caption-batch/input/`
- Previous MJ reference images may already be on the pod at `/workspace/lora_dataset_v4/` — these can be reused

### Phase 2: INSTALL JOYCAPTION
1. SSH into the pod
2. Upload `install_joycaption.sh` to `/workspace/`
3. Run: `chmod +x /workspace/install_joycaption.sh && bash /workspace/install_joycaption.sh`
4. Verify: `ls /workspace/joy-caption-batch/venv/bin/python` should exist

### Phase 3: DOWNLOAD WAN 2.1 MODELS (can run parallel with Phase 2)
1. Upload `download_wan_models.sh` to `/workspace/`
2. Run: `chmod +x /workspace/download_wan_models.sh && bash /workspace/download_wan_models.sh`
3. This downloads ~36GB — takes 30-60 minutes depending on network speed
4. Verify: `ls -lh /workspace/models/wan/*.safetensors` — should show 3 files totaling ~35GB
5. **DISK SPACE WARNING:** Pod has 50GB persistent storage. Previous data may use 20-30GB. Check `df -h /workspace` before downloading. May need to clean up old checkpoints.

### Phase 4: INSTALL DIFFUSIONPIPE (wait for Phase 2 to finish)
1. Upload `install_diffusion_pipe.sh` to `/workspace/`
2. Run: `chmod +x /workspace/install_diffusion_pipe.sh && bash /workspace/install_diffusion_pipe.sh`
3. Verify: `ls /workspace/diffusion-pipe/train.py` should exist

### Phase 5: CAPTION IMAGES WITH JOYCAPTION
1. Ensure images are in `/workspace/joy-caption-batch/input/`
2. Edit `batch-alpha2.py`:
   - Set `PREPEND_STRING = "amiranoor, "`
   - Set `BATCH_PROCESSING_COUNT = 4` (for 24GB RTX 4090)
3. Activate environment: `source /workspace/joy-caption-batch/venv/bin/activate`
4. Run: `cd /workspace/joy-caption-batch && python batch-alpha2.py`
5. First run downloads captioning model (~17.9GB). Subsequent runs are fast.
6. Verify: Each image in `input/` should now have a matching `.txt` file
7. Spot-check a few `.txt` files — they should start with "amiranoor, " followed by a description

### Phase 6: PREPARE DATASET (80/20 train/eval split)
1. Create dataset directories:
```bash
mkdir -p /workspace/dataset/train
mkdir -p /workspace/dataset/eval
```
2. Move captioned images (image + matching .txt) from `joy-caption-batch/input/` to dataset folders:
   - 80% of image+txt pairs → `/workspace/dataset/train/`
   - 20% of image+txt pairs → `/workspace/dataset/eval/`
3. Example with 25 images: 20 to train, 5 to eval
4. Each folder should have pairs: `image001.png` + `image001.txt`, etc.

### Phase 7: CONFIGURE TRAINING
1. Upload the 3 TOML config files to `/workspace/diffusion-pipe/examples/`:
   - `training_config.toml`
   - `dataset_config.toml`
   - `eval_dataset_config.toml`
2. **CRITICAL:** Edit `training_config.toml` and replace `PASTE_YOUR_WANDB_API_KEY_HERE` with a real wandb API key
   - Get from: wandb.ai → Settings → API Keys (or wandb.ai/quickstart)
   - The user needs to provide this
3. Create output directory: `mkdir -p /workspace/training_output`

### Phase 8: RUN TRAINING
1. Activate DiffusionPipe environment:
```bash
cd /workspace/diffusion-pipe
source venv/bin/activate  # or: conda activate diffusion-pipe
```
2. Launch training:
```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
NCCL_P2P_DISABLE="1" NCCL_IB_DISABLE="1" \
deepspeed --num_gpus=1 train.py --deepspeed --config examples/training_config.toml
```
3. Training will print a wandb URL — click to monitor in real-time
4. Expected duration on RTX 4090: 3-6 hours for 20 images
5. Checkpoints saved every 50 steps to `/workspace/training_output/`
6. **DO NOT STOP TRAINING** until the loss graph shows clear convergence (bottoming out)

### Phase 9: PICK BEST CHECKPOINT
1. Open the wandb dashboard link (printed at training start)
2. Look at the eval loss graph
3. Find where the loss bottoms out = convergence point
4. Note the step number (e.g., step 250)
5. Go to `/workspace/training_output/` → find the checkpoint folder for that step
6. The file you want: `adapter_model.safetensors` inside that checkpoint folder
7. This is your trained LoRA file

### Phase 10: DEPLOY TO COMFYUI
1. Copy the best LoRA to ComfyUI:
```bash
cp /workspace/training_output/checkpoint-STEP/adapter_model.safetensors \
   /workspace/runpod-slim/ComfyUI/models/loras/amiranoor_wan21.safetensors
```
2. Load a Wan 2.1 workflow in ComfyUI (download from CivitAI)
3. Select the LoRA in the workflow
4. Use trigger word "amiranoor" in prompts
5. Generate test images to verify consistent face

---

## TROUBLESHOOTING

### Out of VRAM during training
- Reduce `gradient_accumulation_steps` from 4 to 2
- Increase `blocks_to_swap` from 24 to 32
- Change `transformer_dtype` from 'float8' to 'nf4' (more aggressive quantization)
- Set `caching_batch_size = 1` (already set)

### Out of disk space
- Check: `df -h /workspace`
- Delete old LoRA checkpoints: `rm -rf /workspace/lora_dataset_v3/ /workspace/lora_dataset_v4/` (after confirming with user)
- Use FP8 transformer instead of FP16: change download URL to fp8 variant (~14.3GB instead of 28.6GB)

### wandb not connecting
- Verify API key is correct in training_config.toml
- Try: `pip install wandb && wandb login YOUR_API_KEY`

### JoyCaption fails to download model
- Run `pip install huggingface_hub` and retry
- If HuggingFace is slow: `export HF_HUB_DOWNLOAD_TIMEOUT=600`

### ComfyUI doesn't recognize the LoRA
- Ensure it's copied to `/workspace/runpod-slim/ComfyUI/models/loras/`
- Restart ComfyUI: kill the process and restart with `python3 main.py --listen 0.0.0.0 --port 8188`
- Make sure the workflow is for Wan 2.1 (not SDXL) — different model architectures need different LoRA formats

### SSH connection fails
- Pod may have migrated. Check RunPod dashboard for new SSH command/IP/port.
- After migration: SSH key needs to be re-added via RunPod web terminal
- Then run: `bash /workspace/startup_v2.sh` to restore environment

---

## FILE STRUCTURE ON POD (after full setup)

```
/workspace/
├── joy-caption-batch/           ← JoyCaption captioning tool
│   ├── input/                   ← Put 20+ images here
│   ├── batch-alpha2.py          ← Main script (edit trigger word here)
│   └── venv/                    ← Python environment
├── diffusion-pipe/              ← LoRA training framework
│   ├── train.py                 ← Main training script
│   ├── examples/                ← Config files go here
│   │   ├── training_config.toml
│   │   ├── dataset_config.toml
│   │   └── eval_dataset_config.toml
│   └── venv/                    ← Python environment
├── models/
│   └── wan/                     ← Base model files
│       ├── Wan2.1-T2V-14B/      ← Config directory
│       ├── wan2.1_t2v_14B_fp16.safetensors  (28.6GB)
│       ├── umt5_xxl_fp8_e4m3fn_scaled.safetensors  (6.7GB)
│       └── wan_2.1_vae.safetensors  (254MB)
├── dataset/                     ← Prepared training data
│   ├── train/                   ← 80% of captioned images + .txt files
│   └── eval/                    ← 20% of captioned images + .txt files
├── training_output/             ← Training output (checkpoints here)
│   ├── checkpoint-50/
│   ├── checkpoint-100/
│   └── ...                      ← Each has adapter_model.safetensors
├── runpod-slim/ComfyUI/         ← EXISTING ComfyUI installation
│   └── models/loras/            ← Copy best LoRA here when done
└── [existing scripts from previous phases — DO NOT TOUCH]
```

---

## CRITICAL RULES

1. **DO NOT delete existing files** on the pod. Previous work (LoRA v3/v4, InstantID scripts, ComfyUI) must be preserved.
2. **DO NOT use Wan 2.2** — stick with Wan 2.1. 2.2 uses MoE and is more complex.
3. **The trigger word is "amiranoor"** — use exactly this, lowercase, no spaces.
4. **Save every 50 steps** — more frequent saves = more checkpoint options.
5. **Pick the convergence point** — not the lowest step, not the highest step. The point where loss bottoms out.
6. **Disk space is limited** (50GB total). Monitor with `df -h /workspace` before large downloads.
7. **wandb API key is required** — user must provide this. Training works without it but you lose the eval graphs which are the entire point of using DiffusionPipe.
8. **The user's SSH key** is at `~/.ssh/id_ed25519` on their Windows machine. Public key is `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ56MCk0GjScua9CY5VPbWWvuJ95Gj7JKxEc4r+DLkUe vitaleysha@gmail.com`
9. **ComfyUI uses python3** not python on this RunPod pod.
10. **pkill python3 will kill SSH** — never do this directly. Use `bash -c 'nohup bash -c "sleep 2; pkill ..." &'` pattern if needed.
