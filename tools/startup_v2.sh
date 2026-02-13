#!/usr/bin/env bash
set -euo pipefail

# startup_v2.sh - BULLETPROOF pod bootstrap
# Run after ANY pod start/migration: bash /workspace/startup_v2.sh
# Handles: SSH keys, pip packages, custom nodes, models, ComfyUI startup

COMFY_ROOT="${COMFY_ROOT:-/workspace/runpod-slim/ComfyUI}"
COMFY_PORT="${COMFY_PORT:-8188}"
LOG_FILE="${COMFY_LOG_FILE:-/workspace/comfyui.log}"

echo "=========================================="
echo "PISTACHIO STARTUP V2 - $(date)"
echo "=========================================="

if [[ ! -d "${COMFY_ROOT}" ]]; then
  echo "[FAIL] ComfyUI root not found: ${COMFY_ROOT}" >&2
  exit 1
fi

# 1. SSH Key
echo "[1/8] SSH key setup..."
mkdir -p ~/.ssh && chmod 700 ~/.ssh
SSH_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ56MCk0GjScua9CY5VPbWWvuJ95Gj7JKxEc4r+DLkUe vitaleysha@gmail.com"
if ! grep -q "vitaleysha" ~/.ssh/authorized_keys 2>/dev/null; then
    echo "$SSH_KEY" >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    echo "  -> SSH key added"
else
    echo "  -> SSH key present"
fi

# 2. Python packages
echo "[2/8] Python packages..."
pip install -q insightface onnxruntime-gpu 2>/dev/null || pip install insightface onnxruntime-gpu
python3 -c "import insightface; print('  -> insightface OK')" 2>/dev/null || echo "  -> WARNING: insightface failed"

# 3. Custom nodes
echo "[3/8] Custom nodes..."
CUSTOM="${COMFY_ROOT}/custom_nodes"
cd "${CUSTOM}"

# InstantID
if [[ -d "ComfyUI_InstantID" ]] || [[ -d "ComfyUI-InstantID" ]]; then
    echo "  -> InstantID node OK"
else
    git clone https://github.com/cubiq/ComfyUI_InstantID.git
    [[ -f "ComfyUI_InstantID/requirements.txt" ]] && pip install -q -r ComfyUI_InstantID/requirements.txt
fi

# IP-Adapter Plus
if [[ -d "ComfyUI_IPAdapter_plus" ]]; then
    echo "  -> IPAdapter Plus OK"
else
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
    [[ -f "ComfyUI_IPAdapter_plus/requirements.txt" ]] && pip install -q -r ComfyUI_IPAdapter_plus/requirements.txt
fi

# Impact Pack (FaceDetailer)
if [[ -d "ComfyUI-Impact-Pack" ]]; then
    echo "  -> Impact Pack OK"
else
    git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git
    cd ComfyUI-Impact-Pack && pip install -q -r requirements.txt 2>/dev/null; cd "${CUSTOM}"
fi

# 4. Models
echo "[4/8] Models..."
MODELS="${COMFY_ROOT}/models"

# InstantID adapter
if [[ -f "${MODELS}/instantid/ip-adapter.bin" ]]; then
    echo "  -> InstantID adapter OK ($(du -h ${MODELS}/instantid/ip-adapter.bin | cut -f1))"
else
    mkdir -p "${MODELS}/instantid"
    echo "  -> Downloading InstantID adapter..."
    wget -q "https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin" \
        -O "${MODELS}/instantid/ip-adapter.bin"
fi

# InstantID ControlNet
if [[ -f "${MODELS}/controlnet/instantid-controlnet.safetensors" ]]; then
    echo "  -> InstantID ControlNet OK"
else
    mkdir -p "${MODELS}/controlnet"
    echo "  -> Downloading InstantID ControlNet..."
    wget -q "https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors" \
        -O "${MODELS}/controlnet/instantid-controlnet.safetensors"
fi

# Face detection model
if [[ -f "${MODELS}/ultralytics/bbox/face_yolov8m.pt" ]]; then
    echo "  -> Face detector OK"
else
    mkdir -p "${MODELS}/ultralytics/bbox"
    echo "  -> Downloading face detector..."
    wget -q "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt" \
        -O "${MODELS}/ultralytics/bbox/face_yolov8m.pt"
fi

# InsightFace
if [[ -d "${MODELS}/insightface/models/antelopev2" ]]; then
    echo "  -> InsightFace antelopev2 OK"
else
    echo "  -> WARNING: InsightFace models missing"
fi

# Checkpoint
if [[ -f "${MODELS}/checkpoints/realvisxl_v5.safetensors" ]]; then
    echo "  -> RealVisXL V5 OK"
else
    echo "  -> WARNING: Checkpoint missing!"
fi

# LoRA
if [[ -f "${MODELS}/loras/amiranoor_v3-step00001000.safetensors" ]]; then
    echo "  -> LoRA amiranoor_v3 OK"
else
    if [[ -f "/workspace/lora_output_v3/amiranoor_v3-step00001000.safetensors" ]]; then
        cp /workspace/lora_output_v3/amiranoor_v3-step00001000.safetensors "${MODELS}/loras/"
        echo "  -> LoRA copied from training output"
    else
        echo "  -> WARNING: LoRA missing!"
    fi
fi

# 5. ComfyUI Manager permissions
echo "[5/8] ComfyUI Manager permissions..."
chmod 666 "${COMFY_ROOT}/custom_nodes/ComfyUI-Manager"/*.db 2>/dev/null || true
chmod 777 "${COMFY_ROOT}/custom_nodes/ComfyUI-Manager" 2>/dev/null || true
echo "  -> Done"

# 6. Start/Restart ComfyUI
echo "[6/8] ComfyUI startup..."
if curl -s "http://127.0.0.1:${COMFY_PORT}/system_stats" > /dev/null 2>&1; then
    echo "  -> ComfyUI already running, restarting..."
    pkill -f "main.py" 2>/dev/null || true
    sleep 3
fi
cd "${COMFY_ROOT}"
nohup python3 main.py --listen 0.0.0.0 --port "${COMFY_PORT}" > "${LOG_FILE}" 2>&1 &
echo "  -> Waiting for startup..."
for i in $(seq 1 60); do
    if curl -s "http://127.0.0.1:${COMFY_PORT}/system_stats" > /dev/null 2>&1; then
        echo "  -> ComfyUI ready on port ${COMFY_PORT}"
        break
    fi
    sleep 2
done

# 7. Verify nodes loaded
echo "[7/8] Verifying nodes..."
python3 -c "
import urllib.request, json
try:
    r = urllib.request.urlopen('http://127.0.0.1:${COMFY_PORT}/object_info', timeout=10)
    d = json.loads(r.read())
    checks = {
        'InstantID': 'ApplyInstantID' in d,
        'IPAdapter': 'IPAdapterFaceID' in d,
        'FaceDetailer': 'FaceDetailer' in d,
        'LoraLoader': 'LoraLoader' in d,
    }
    for name, ok in checks.items():
        print(f'  -> {name}: {\"OK\" if ok else \"MISSING\"}')
    if not all(checks.values()):
        print('  -> WARNING: Some nodes missing, check ComfyUI logs')
except Exception as e:
    print(f'  -> ERROR: Cannot reach ComfyUI API: {e}')
" 2>/dev/null || echo "  -> Could not verify nodes"

# 8. System info
echo "[8/8] System info..."
python3 -c "
import urllib.request, json
r = urllib.request.urlopen('http://127.0.0.1:${COMFY_PORT}/system_stats', timeout=10)
d = json.loads(r.read())
dev = d['devices'][0]
print(f'  -> GPU: {dev[\"name\"]}')
print(f'  -> VRAM: {dev[\"vram_total\"]/1e9:.1f}GB total, {dev[\"vram_free\"]/1e9:.1f}GB free')
" 2>/dev/null || echo "  -> Could not read system stats"

echo ""
echo "=========================================="
echo "STARTUP COMPLETE - $(date)"
echo "=========================================="
echo ""
echo "PRODUCTION COMMANDS:"
echo "  python3 -u /workspace/instantid_production.py  # 36 varied images + quality gate"
echo "  python3 -u /workspace/instantid_combo.py       # InstantID sweep test"
echo ""
