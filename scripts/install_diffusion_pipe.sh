#!/bin/bash
# ============================================================
# PISTACHIO — Install DiffusionPipe (LoRA Training Framework)
# Replaces Discord-gated script. 100% open source.
# Run this in Terminal 3 on JupyterLab.
# IMPORTANT: Wait until JoyCaption install finishes first
# to avoid Python environment conflicts.
# ============================================================

set -e
echo "=========================================="
echo "  Installing DiffusionPipe LoRA Trainer"
echo "=========================================="

cd /workspace

# Clone DiffusionPipe with submodules
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

# Create conda environment (or venv if conda not available)
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

# Install PyTorch
echo "[3/5] Installing PyTorch..."
pip install torch torchvision

# Install CUDA NVCC if using conda
if command -v conda &> /dev/null; then
    echo "[3.5/5] Installing CUDA NVCC via conda..."
    conda install -c nvidia cuda-nvcc -y 2>/dev/null || true
fi

# Install all requirements
echo "[4/5] Installing requirements (this takes a few minutes)..."
pip install -r requirements.txt

# Install flash attention (optional but recommended for speed)
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
echo "  deepspeed --num_gpus=1 train.py --deepspeed --config examples/your_config.toml"
echo ""
