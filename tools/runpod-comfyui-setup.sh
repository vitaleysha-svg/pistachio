#!/bin/bash
# =============================================================
# PISTACHIO - RunPod ComfyUI One-Click Setup Script
# =============================================================
# USAGE: After deploying "ComfyUI" template on RunPod,
# open the terminal and paste this entire script.
# It downloads all models and installs all extensions.
# =============================================================

echo "=========================================="
echo "PISTACHIO - ComfyUI Setup Starting..."
echo "=========================================="

# Navigate to ComfyUI directory
cd /workspace/ComfyUI || cd /opt/ComfyUI || { echo "ERROR: ComfyUI directory not found. Check your RunPod template."; exit 1; }

COMFYUI_DIR=$(pwd)
echo "ComfyUI directory: $COMFYUI_DIR"

# ----- STEP 1: Install Custom Nodes -----
echo ""
echo "[1/6] Installing Custom Nodes..."

cd custom_nodes

# InstantID
if [ ! -d "ComfyUI_InstantID" ]; then
    echo "  -> Cloning ComfyUI_InstantID..."
    git clone https://github.com/cubiq/ComfyUI_InstantID.git
else
    echo "  -> ComfyUI_InstantID already installed"
fi

# IP-Adapter Plus
if [ ! -d "ComfyUI_IPAdapter_plus" ]; then
    echo "  -> Cloning ComfyUI_IPAdapter_plus..."
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
else
    echo "  -> ComfyUI_IPAdapter_plus already installed"
fi

# ComfyUI Manager (if not already installed)
if [ ! -d "ComfyUI-Manager" ]; then
    echo "  -> Cloning ComfyUI-Manager..."
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
else
    echo "  -> ComfyUI-Manager already installed"
fi

# Install node dependencies
echo "  -> Installing node dependencies..."
for dir in ComfyUI_InstantID ComfyUI_IPAdapter_plus; do
    if [ -f "$dir/requirements.txt" ]; then
        pip install -r "$dir/requirements.txt" -q
    fi
done

cd "$COMFYUI_DIR"

# ----- STEP 2: Download SDXL Base Model -----
echo ""
echo "[2/6] Downloading SDXL Base Model..."

mkdir -p models/checkpoints
if [ ! -f "models/checkpoints/sd_xl_base_1.0.safetensors" ]; then
    echo "  -> Downloading sd_xl_base_1.0.safetensors (6.9GB)..."
    wget -q --show-progress -O models/checkpoints/sd_xl_base_1.0.safetensors \
        "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"
else
    echo "  -> SDXL base already downloaded"
fi

# ----- STEP 3: Download InstantID Models -----
echo ""
echo "[3/6] Downloading InstantID Models..."

mkdir -p models/instantid
mkdir -p models/controlnet

# InstantID IP-Adapter
if [ ! -f "models/instantid/ip-adapter.bin" ]; then
    echo "  -> Downloading InstantID ip-adapter.bin..."
    wget -q --show-progress -O models/instantid/ip-adapter.bin \
        "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin"
else
    echo "  -> InstantID ip-adapter.bin already downloaded"
fi

# InstantID ControlNet
if [ ! -f "models/controlnet/diffusion_pytorch_model.safetensors" ]; then
    echo "  -> Downloading InstantID ControlNet..."
    wget -q --show-progress -O models/controlnet/diffusion_pytorch_model.safetensors \
        "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors"
    # Also download config
    wget -q -O models/controlnet/config.json \
        "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/config.json"
else
    echo "  -> InstantID ControlNet already downloaded"
fi

# ----- STEP 4: Download IP-Adapter FaceID Plus V2 Models -----
echo ""
echo "[4/6] Downloading IP-Adapter FaceID Plus V2..."

mkdir -p models/ipadapter
mkdir -p models/loras

# IP-Adapter FaceID Plus V2 for SDXL
if [ ! -f "models/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin" ]; then
    echo "  -> Downloading ip-adapter-faceid-plusv2_sdxl.bin..."
    wget -q --show-progress -O models/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin \
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin"
else
    echo "  -> IP-Adapter FaceID Plus V2 already downloaded"
fi

# IP-Adapter FaceID LoRA for SDXL
if [ ! -f "models/loras/ip-adapter-faceid-plusv2_sdxl_lora.safetensors" ]; then
    echo "  -> Downloading ip-adapter-faceid-plusv2_sdxl_lora.safetensors..."
    wget -q --show-progress -O models/loras/ip-adapter-faceid-plusv2_sdxl_lora.safetensors \
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl_lora.safetensors"
else
    echo "  -> IP-Adapter FaceID LoRA already downloaded"
fi

# ----- STEP 5: Download InsightFace / Antelopev2 -----
echo ""
echo "[5/6] Downloading InsightFace (antelopev2)..."

mkdir -p models/insightface/models/antelopev2

# Install insightface and onnxruntime
pip install insightface onnxruntime-gpu -q

# Download antelopev2 models
if [ ! -f "models/insightface/models/antelopev2/1k3d68.onnx" ]; then
    echo "  -> Downloading antelopev2 face analysis models..."
    cd models/insightface/models/antelopev2

    # These are the individual model files needed
    wget -q --show-progress "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2/1k3d68.onnx"
    wget -q --show-progress "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2/2d106det.onnx"
    wget -q --show-progress "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2/genderage.onnx"
    wget -q --show-progress "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2/glintr100.onnx"
    wget -q --show-progress "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2/scrfd_10g_bnkps.onnx"

    cd "$COMFYUI_DIR"
else
    echo "  -> antelopev2 already downloaded"
fi

# ----- STEP 6: Create Reference Image Directory -----
echo ""
echo "[6/6] Setting up workspace..."

mkdir -p input/pistachio_reference
echo "  -> Created input/pistachio_reference/ directory"
echo "  -> Upload your Midjourney hero image(s) to this folder"

# ----- DONE -----
echo ""
echo "=========================================="
echo "PISTACHIO SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Models downloaded:"
echo "  [x] SDXL Base 1.0"
echo "  [x] InstantID (ip-adapter + ControlNet)"
echo "  [x] IP-Adapter FaceID Plus V2 (adapter + LoRA)"
echo "  [x] InsightFace antelopev2"
echo ""
echo "Custom nodes installed:"
echo "  [x] ComfyUI_InstantID"
echo "  [x] ComfyUI_IPAdapter_plus"
echo "  [x] ComfyUI-Manager"
echo ""
echo "NEXT STEPS:"
echo "  1. Restart ComfyUI (or reload the page)"
echo "  2. Upload your Midjourney hero image to input/pistachio_reference/"
echo "  3. Build the InstantID + IP-Adapter workflow"
echo "  4. Generate variations!"
echo ""
echo "Estimated disk usage: ~15GB"
echo "=========================================="
