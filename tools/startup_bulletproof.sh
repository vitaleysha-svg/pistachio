#!/bin/bash
# =============================================================
# PISTACHIO - Bulletproof RunPod Startup Script
# =============================================================
# PURPOSE: Runs on every pod boot (new, restart, or migration).
#          Ensures all nodes, models, deps are installed and
#          ComfyUI starts cleanly every single time.
#
# INSTALL: Set this as your pod's "Docker Command" or place in
#          /workspace/startup_bulletproof.sh and add to post_start.sh
# =============================================================

set -e
LOG="/workspace/startup.log"
exec > >(tee -a "$LOG") 2>&1
echo ""
echo "=========================================="
echo "PISTACHIO STARTUP - $(date)"
echo "=========================================="

# ---- 1. Detect ComfyUI Location ----
COMFYUI_DIR=""
for d in /workspace/runpod-slim/ComfyUI /workspace/ComfyUI /opt/ComfyUI; do
    if [ -d "$d" ]; then
        COMFYUI_DIR="$d"
        break
    fi
done

if [ -z "$COMFYUI_DIR" ]; then
    echo "[ERROR] ComfyUI not found. Installing fresh..."
    cd /workspace
    git clone https://github.com/comfyanonymous/ComfyUI.git
    cd ComfyUI
    pip install -r requirements.txt -q
    COMFYUI_DIR="/workspace/ComfyUI"
fi
echo "[OK] ComfyUI at: $COMFYUI_DIR"

# ---- 2. Fix Python/pip ----
echo ""
echo "[2] Checking Python environment..."
python3 -m pip install --upgrade pip -q 2>/dev/null || true

# ---- 3. Install/Update Custom Nodes ----
echo ""
echo "[3] Checking custom nodes..."
cd "$COMFYUI_DIR/custom_nodes"

declare -A NODES
NODES[ComfyUI_InstantID]="https://github.com/cubiq/ComfyUI_InstantID.git"
NODES[ComfyUI_IPAdapter_plus]="https://github.com/cubiq/ComfyUI_IPAdapter_plus.git"
NODES[ComfyUI-Manager]="https://github.com/ltdrdata/ComfyUI-Manager.git"

for name in "${!NODES[@]}"; do
    if [ ! -d "$name" ]; then
        echo "  -> Installing $name..."
        git clone "${NODES[$name]}" 2>/dev/null || echo "  [WARN] Failed to clone $name"
    else
        echo "  -> $name already installed"
        cd "$name"
        git pull -q 2>/dev/null || true
        cd ..
    fi
    if [ -f "$name/requirements.txt" ]; then
        pip install -r "$name/requirements.txt" -q 2>/dev/null || true
    fi
done

# ---- 4. Install Core Dependencies ----
echo ""
echo "[4] Installing core dependencies..."
pip install insightface onnxruntime-gpu -q 2>/dev/null || pip install insightface onnxruntime -q 2>/dev/null || true
pip install prodigyopt -q 2>/dev/null || true

# Fix torchvision if mismatched
TORCH_VER=$(python3 -c "import torch; print(torch.__version__.split('+')[0])" 2>/dev/null || echo "unknown")
TV_VER=$(python3 -c "import torchvision; print(torchvision.__version__.split('+')[0])" 2>/dev/null || echo "unknown")
echo "  torch=$TORCH_VER torchvision=$TV_VER"

# Detect CUDA version from torch
CUDA_TAG=$(python3 -c "import torch; v=torch.__version__; print(v.split('+')[1] if '+' in v else 'cpu')" 2>/dev/null || echo "cpu")
if [ "$CUDA_TAG" != "cpu" ]; then
    # Verify torchvision works
    python3 -c "import torchvision" 2>/dev/null || {
        echo "  [FIX] Reinstalling torchvision for $CUDA_TAG..."
        pip install --force-reinstall torchvision --index-url "https://download.pytorch.org/whl/$CUDA_TAG" --no-deps -q
    }
fi

# ---- 5. Download Models (idempotent) ----
echo ""
echo "[5] Checking models..."
cd "$COMFYUI_DIR"

# InsightFace antelopev2
ANTE_DIR="models/insightface/models/antelopev2"
mkdir -p "$ANTE_DIR"
if [ ! -f "$ANTE_DIR/1k3d68.onnx" ]; then
    echo "  -> Downloading antelopev2 face models..."
    for f in 1k3d68.onnx 2d106det.onnx genderage.onnx glintr100.onnx scrfd_10g_bnkps.onnx; do
        wget -q "https://huggingface.co/MonsterMMORPG/tools/resolve/main/antelopev2/$f" -O "$ANTE_DIR/$f" || true
    done
else
    echo "  -> antelopev2 already present"
fi

# InstantID models
mkdir -p models/instantid models/controlnet
if [ ! -f "models/instantid/ip-adapter.bin" ]; then
    echo "  -> Downloading InstantID ip-adapter..."
    wget -q "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin" -O models/instantid/ip-adapter.bin || true
fi
if [ ! -f "models/controlnet/diffusion_pytorch_model.safetensors" ]; then
    echo "  -> Downloading InstantID ControlNet..."
    wget -q "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors" -O models/controlnet/diffusion_pytorch_model.safetensors || true
    wget -q "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/config.json" -O models/controlnet/config.json || true
fi

# IP-Adapter FaceID Plus V2
mkdir -p models/ipadapter models/loras
if [ ! -f "models/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin" ]; then
    echo "  -> Downloading IP-Adapter FaceID Plus V2..."
    wget -q "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin" -O models/ipadapter/ip-adapter-faceid-plusv2_sdxl.bin || true
fi
if [ ! -f "models/loras/ip-adapter-faceid-plusv2_sdxl_lora.safetensors" ]; then
    echo "  -> Downloading IP-Adapter FaceID LoRA..."
    wget -q "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl_lora.safetensors" -O models/loras/ip-adapter-faceid-plusv2_sdxl_lora.safetensors || true
fi

# ---- 6. Copy LoRA models from training output ----
echo ""
echo "[6] Checking for trained LoRA models..."
for v in v1 v2 v3; do
    LORA_FILE="/workspace/lora_output_${v}/amiranoor_${v}.safetensors"
    if [ -f "$LORA_FILE" ] && [ ! -f "models/loras/amiranoor_${v}.safetensors" ]; then
        echo "  -> Copying amiranoor_${v}.safetensors to ComfyUI loras folder"
        cp "$LORA_FILE" "models/loras/amiranoor_${v}.safetensors"
    fi
done
# Also check for checkpoint variants
for f in /workspace/lora_output_v3/amiranoor_v3-step*.safetensors; do
    if [ -f "$f" ]; then
        BASENAME=$(basename "$f")
        if [ ! -f "models/loras/$BASENAME" ]; then
            echo "  -> Copying checkpoint $BASENAME to ComfyUI loras folder"
            cp "$f" "models/loras/$BASENAME"
        fi
    fi
done

# ---- 7. Fix sd-scripts if present ----
echo ""
echo "[7] Patching sd-scripts (if present)..."
SD_SCRIPTS="/workspace/sd-scripts"
if [ -d "$SD_SCRIPTS" ]; then
    # Fix COSINE_WITH_MIN_LR crash
    TRAIN_UTIL="$SD_SCRIPTS/library/train_util.py"
    if [ -f "$TRAIN_UTIL" ]; then
        if grep -q 'if name == SchedulerType.COSINE_WITH_MIN_LR:' "$TRAIN_UTIL" 2>/dev/null; then
            sed -i 's/    if name == SchedulerType.COSINE_WITH_MIN_LR:/    if hasattr(SchedulerType, "COSINE_WITH_MIN_LR") and name == SchedulerType.COSINE_WITH_MIN_LR:/' "$TRAIN_UTIL"
            echo "  -> Patched COSINE_WITH_MIN_LR"
        else
            echo "  -> sd-scripts already patched"
        fi
    fi
fi

# ---- 8. SSH key setup ----
echo ""
echo "[8] Ensuring SSH access..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh
if ! grep -q "AAAAC3NzaC1lZDI1NTE5AAAAIJ56MCk0GjScua9CY5VPbWWvuJ95Gj7JKxEc4r+DLkUe" ~/.ssh/authorized_keys 2>/dev/null; then
    echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ56MCk0GjScua9CY5VPbWWvuJ95Gj7JKxEc4r+DLkUe vitaleysha@gmail.com" >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    echo "  -> SSH key added"
else
    echo "  -> SSH key already present"
fi

# ---- 9. Start ComfyUI ----
echo ""
echo "[9] Starting ComfyUI..."
cd "$COMFYUI_DIR"

# Kill any existing ComfyUI process
pkill -f "main.py.*--listen" 2>/dev/null || true
sleep 2

# Start ComfyUI in background
nohup python3 main.py --listen 0.0.0.0 --port 8188 > /workspace/comfyui.log 2>&1 &
COMFY_PID=$!
echo "  -> ComfyUI started (PID: $COMFY_PID)"

# Wait for startup
echo "  -> Waiting for ComfyUI to be ready..."
for i in $(seq 1 30); do
    if curl -s http://localhost:8188 > /dev/null 2>&1; then
        echo "  -> ComfyUI is READY on port 8188"
        break
    fi
    sleep 2
done

echo ""
echo "=========================================="
echo "PISTACHIO STARTUP COMPLETE - $(date)"
echo "=========================================="
echo ""
echo "Services:"
echo "  ComfyUI: http://localhost:8188"
echo "  Pod SSH: ssh -i ~/.ssh/id_ed25519 -p 18631 root@<POD_IP>"
echo ""
echo "LoRA models available:"
ls -la "$COMFYUI_DIR/models/loras/"*.safetensors 2>/dev/null | awk '{print "  " $NF}'
echo "=========================================="
