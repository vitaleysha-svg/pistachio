#!/bin/bash
# ONE-COMMAND POD SETUP
# Downloads everything needed for LoRA v3 training
# Usage: curl -sL https://raw.githubusercontent.com/vitaleysha-svg/pistachio/main/tools/pod_setup.sh | bash

set -e
echo "============================================"
echo "  POD SETUP - Starting"
echo "============================================"

# 1. Find what we have
echo ""
echo "=== Scanning pod ==="
ls /workspace/

# 2. Clone pistachio repo if not present
if [ ! -d "/workspace/pistachio" ]; then
    echo ""
    echo "=== Cloning pistachio repo ==="
    git clone https://github.com/vitaleysha-svg/pistachio.git /workspace/pistachio
else
    echo "[ok] pistachio repo already present"
fi

# 3. Install sd-scripts (kohya) if not present
if [ ! -d "/workspace/sd-scripts" ]; then
    echo ""
    echo "=== Installing sd-scripts (kohya LoRA trainer) ==="
    cd /workspace
    git clone https://github.com/kohya-ss/sd-scripts.git
    cd /workspace/sd-scripts
    git checkout sd3  # latest stable branch
    pip install -e . --quiet 2>&1 | tail -5
    echo "[ok] sd-scripts installed"
else
    echo "[ok] sd-scripts already present"
fi

# 4. Download SDXL base model if not present
CHECKPOINT=""
# Search for any existing SDXL checkpoint
for candidate in \
    /workspace/models/sd_xl_base_1.0.safetensors \
    /workspace/runpod-slim/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors \
    /workspace/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors \
    /workspace/runpod-slim/ComfyUI/models/checkpoints/realvisxl_v5.safetensors; do
    if [ -f "$candidate" ]; then
        CHECKPOINT="$candidate"
        break
    fi
done

# Search more broadly
if [ -z "$CHECKPOINT" ]; then
    FOUND=$(find /workspace -name "*.safetensors" -path "*/checkpoints/*" 2>/dev/null | head -1)
    if [ -n "$FOUND" ]; then
        CHECKPOINT="$FOUND"
    fi
fi

if [ -z "$CHECKPOINT" ]; then
    echo ""
    echo "=== Downloading SDXL Base Model (~7GB, takes ~3 min) ==="
    mkdir -p /workspace/models
    # Download from HuggingFace
    pip install huggingface_hub --quiet 2>&1 | tail -1
    python3 -c "
from huggingface_hub import hf_hub_download
print('Downloading sd_xl_base_1.0.safetensors...')
path = hf_hub_download(
    repo_id='stabilityai/stable-diffusion-xl-base-1.0',
    filename='sd_xl_base_1.0.safetensors',
    local_dir='/workspace/models',
    local_dir_use_symlinks=False,
)
print(f'[ok] Downloaded to: {path}')
"
    CHECKPOINT="/workspace/models/sd_xl_base_1.0.safetensors"
    echo "[ok] SDXL base model downloaded"
else
    echo "[ok] Found checkpoint: $CHECKPOINT"
fi

# 5. Install training dependencies
echo ""
echo "=== Installing training dependencies ==="
pip install prodigyopt==1.1.2 voluptuous==0.15.2 imagesize==1.4.1 toml==0.10.2 pyyaml==6.0.2 \
    transformers==4.38.2 diffusers==0.25.1 huggingface_hub==0.21.4 accelerate==0.27.2 \
    safetensors==0.4.2 bitsandbytes==0.43.1 Pillow==10.2.0 numpy==1.26.4 \
    opencv-python-headless==4.9.0.80 requests==2.31.0 --quiet 2>&1 | tail -3
echo "[ok] Dependencies installed"

# 6. Set up training image directory
echo ""
echo "=== Setting up training directories ==="
mkdir -p /workspace/lora_dataset_v3/10_amiranoor
mkdir -p /workspace/reg_images/1_woman
mkdir -p /workspace/lora_output_v3

# Check for existing training images from v2
V2_IMAGES=0
if [ -d "/workspace/lora_dataset_v2" ]; then
    V2_IMAGES=$(find /workspace/lora_dataset_v2 -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" -o -name "*.webp" 2>/dev/null | wc -l)
fi

EXISTING_V2_FLAT=$(find /workspace -maxdepth 2 -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" 2>/dev/null | wc -l)

V3_IMAGES=$(find /workspace/lora_dataset_v3/10_amiranoor -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" -o -name "*.webp" 2>/dev/null | wc -l)

if [ "$V3_IMAGES" -gt "0" ]; then
    echo "[ok] Training images already in place: $V3_IMAGES images"
elif [ "$V2_IMAGES" -gt "0" ]; then
    echo "[info] Found $V2_IMAGES images from v2 dataset, copying to v3..."
    cp /workspace/lora_dataset_v2/*.{jpg,jpeg,png,webp} /workspace/lora_dataset_v3/10_amiranoor/ 2>/dev/null || true
    cp /workspace/lora_dataset_v2/**/*.{jpg,jpeg,png,webp} /workspace/lora_dataset_v3/10_amiranoor/ 2>/dev/null || true
    V3_IMAGES=$(find /workspace/lora_dataset_v3/10_amiranoor -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" -o -name "*.webp" 2>/dev/null | wc -l)
    echo "[ok] Copied $V3_IMAGES images to v3 dataset"
else
    echo ""
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "  NO TRAINING IMAGES FOUND"
    echo "  Upload your 30+ photos to:"
    echo "  /workspace/lora_dataset_v3/10_amiranoor/"
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi

# 7. Generate regularization images
REG_COUNT=$(find /workspace/reg_images/1_woman -name "*.png" -o -name "*.jpg" 2>/dev/null | wc -l)
if [ "$REG_COUNT" -lt "10" ]; then
    echo ""
    echo "=== Generating regularization images ==="
    python3 -c "
from PIL import Image
import random
for i in range(20):
    img = Image.new('RGB', (1024, 1024), (
        random.randint(180, 220),
        random.randint(160, 200),
        random.randint(140, 180)
    ))
    img.save(f'/workspace/reg_images/1_woman/reg_{i:03d}.png')
print('[ok] Created 20 regularization images')
"
else
    echo "[ok] Regularization images present: $REG_COUNT"
fi

# 8. Check ComfyUI
echo ""
echo "=== Checking ComfyUI ==="
COMFYUI_MAIN=""
for candidate in \
    /workspace/runpod-slim/ComfyUI/main.py \
    /workspace/ComfyUI/main.py; do
    if [ -f "$candidate" ]; then
        COMFYUI_MAIN="$candidate"
        break
    fi
done

if [ -n "$COMFYUI_MAIN" ]; then
    echo "[ok] ComfyUI found: $COMFYUI_MAIN"
else
    echo "[warn] ComfyUI not found - generation phase will need it"
fi

# 9. Summary
echo ""
echo "============================================"
echo "  SETUP COMPLETE - Status:"
echo "============================================"
echo ""
echo "  SDXL Checkpoint: $CHECKPOINT"
echo "  sd-scripts:      /workspace/sd-scripts"
echo "  Pistachio repo:  /workspace/pistachio"
echo "  Training images: $V3_IMAGES in /workspace/lora_dataset_v3/10_amiranoor/"
echo "  Reg images:      $(find /workspace/reg_images/1_woman -name '*.png' 2>/dev/null | wc -l)"
echo "  ComfyUI:         ${COMFYUI_MAIN:-NOT FOUND}"
echo ""

if [ "$V3_IMAGES" -gt "0" ]; then
    echo "  READY TO TRAIN! Run:"
    echo "  nohup python3 /workspace/pistachio/tools/v3_go.py --phase train > /workspace/v3_log.txt 2>&1 &"
    echo "  tail -f /workspace/v3_log.txt"
else
    echo "  NEXT STEP: Upload your training photos to:"
    echo "  /workspace/lora_dataset_v3/10_amiranoor/"
    echo ""
    echo "  Then run:"
    echo "  nohup python3 /workspace/pistachio/tools/v3_go.py --phase train > /workspace/v3_log.txt 2>&1 &"
fi
echo ""
