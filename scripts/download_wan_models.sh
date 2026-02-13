#!/bin/bash
# ============================================================
# PISTACHIO — Download Wan 2.1 Base Models
# Replaces Discord-gated script. All files from Hugging Face.
# Run this in Terminal 2 on JupyterLab.
# No authentication needed — all Apache 2.0 licensed.
# ============================================================

set -e
echo "=========================================="
echo "  Downloading Wan 2.1 Base Models"
echo "=========================================="

# Create model directory
mkdir -p /workspace/models/wan
cd /workspace/models/wan

# 1. Download official checkpoint directory (config.json + metadata only, ~520MB)
# DiffusionPipe needs config.json from here
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

# 2. Download diffusion transformer model (Comfy-Org repackaged, single file)
# Using FP16 for best training quality. Use FP8 (~14.3GB) if disk space is tight.
echo "[2/4] Downloading diffusion model — wan2.1_t2v_14B_fp16.safetensors (~28.6GB)..."
echo "  (This is the largest file. Be patient.)"
if [ ! -f "wan2.1_t2v_14B_fp16.safetensors" ]; then
    wget -c -O wan2.1_t2v_14B_fp16.safetensors \
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/diffusion_models/wan2.1_t2v_14B_fp16.safetensors"
    echo "  Diffusion model downloaded."
else
    echo "  Diffusion model already exists, skipping."
fi

# 3. Download text encoder (FP8 quantized to save space — 6.7GB instead of 11.4GB)
echo "[3/4] Downloading text encoder — umt5_xxl_fp8_e4m3fn_scaled.safetensors (~6.7GB)..."
if [ ! -f "umt5_xxl_fp8_e4m3fn_scaled.safetensors" ]; then
    wget -c -O umt5_xxl_fp8_e4m3fn_scaled.safetensors \
        "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors"
    echo "  Text encoder downloaded."
else
    echo "  Text encoder already exists, skipping."
fi

# 4. Download VAE (small — 254MB)
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
echo ""
ls -lh /workspace/models/wan/*.safetensors 2>/dev/null || true
echo ""
echo "TOTAL DISK USAGE:"
du -sh /workspace/models/wan/
echo ""
