#!/usr/bin/env bash
set -euo pipefail

# startup_v2.sh
# One-shot pod bootstrap for ComfyUI + LoRA workflow.
# Usage:
#   bash startup_v2.sh
# Optional:
#   COMFY_ROOT=/workspace/runpod-slim/ComfyUI bash startup_v2.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMFY_ROOT="${COMFY_ROOT:-/workspace/runpod-slim/ComfyUI}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PIP_BIN="${PIP_BIN:-pip}"
HEALTH_SCRIPT="${SCRIPT_DIR}/pod_health_check.py"
REQ_FILE="${SCRIPT_DIR}/requirements-pod.txt"
COMFY_PORT="${COMFY_PORT:-8188}"
LOG_FILE="${COMFY_LOG_FILE:-/workspace/comfyui.log}"

if [[ ! -d "${COMFY_ROOT}" ]]; then
  echo "[FAIL] ComfyUI root not found: ${COMFY_ROOT}" >&2
  exit 1
fi

if [[ ! -f "${REQ_FILE}" ]]; then
  echo "[FAIL] requirements file not found: ${REQ_FILE}" >&2
  exit 1
fi

echo "[1/6] Installing pinned dependencies"
"${PIP_BIN}" install --no-input -r "${REQ_FILE}"

# Keep frontend version pinned to avoid mismatch with backend on pod migrations.
echo "[2/6] Pinning ComfyUI frontend package"
"${PIP_BIN}" install --no-input comfyui-frontend-package==1.38.13

echo "[3/6] Fixing ComfyUI manager DB permissions"
chmod 666 "${COMFY_ROOT}/custom_nodes/ComfyUI-Manager"/*.db 2>/dev/null || true
chmod 777 "${COMFY_ROOT}/custom_nodes/ComfyUI-Manager" 2>/dev/null || true

echo "[4/6] Ensuring required custom nodes"
cd "${COMFY_ROOT}/custom_nodes"
if [[ ! -d "ComfyUI_InstantID" ]]; then
  git clone https://github.com/cubiq/ComfyUI_InstantID.git
fi
if [[ -f "ComfyUI_InstantID/requirements.txt" ]]; then
  "${PIP_BIN}" install --no-input -r ComfyUI_InstantID/requirements.txt
fi
if [[ ! -d "ComfyUI_IPAdapter_plus" ]]; then
  git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git
fi
if [[ -f "ComfyUI_IPAdapter_plus/requirements.txt" ]]; then
  "${PIP_BIN}" install --no-input -r ComfyUI_IPAdapter_plus/requirements.txt
fi

echo "[5/6] Running preflight health check (static checks only)"
"${PYTHON_BIN}" "${HEALTH_SCRIPT}" --skip-comfy-api || true

echo "[6/6] Restarting ComfyUI and running full health check"
pkill -f "main.py" 2>/dev/null || true
sleep 2
cd "${COMFY_ROOT}"
nohup "${PYTHON_BIN}" main.py --listen 0.0.0.0 --port "${COMFY_PORT}" > "${LOG_FILE}" 2>&1 &
sleep 10
"${PYTHON_BIN}" "${HEALTH_SCRIPT}" --comfy-url "http://127.0.0.1:${COMFY_PORT}"

echo "[done] startup_v2 complete. ComfyUI should be ready at port ${COMFY_PORT}."
