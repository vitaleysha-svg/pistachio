#!/bin/bash
# ============================================================
# PISTACHIO — Install JoyCaption (Image Captioning Tool)
# Replaces Discord-gated script. 100% open source.
# Run this in Terminal 1 on JupyterLab.
# ============================================================

set -e
echo "=========================================="
echo "  Installing JoyCaption Batch Captioner"
echo "=========================================="

cd /workspace

# Clone the open-source JoyCaption batch repo
if [ ! -d "joy-caption-batch" ]; then
    echo "[1/4] Cloning joy-caption-batch..."
    git clone https://github.com/MNeMoNiCuZ/joy-caption-batch.git
else
    echo "[1/4] joy-caption-batch already exists, pulling latest..."
    cd joy-caption-batch && git pull && cd ..
fi

cd joy-caption-batch

# Create Python virtual environment
echo "[2/4] Creating Python virtual environment..."
python -m venv venv
source venv/bin/activate

# Install PyTorch with CUDA support
echo "[3/4] Installing PyTorch with CUDA 12.8..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

# Install requirements
echo "[4/4] Installing requirements..."
pip install -r requirements.txt

# Create input folder if it doesn't exist
mkdir -p input

echo ""
echo "=========================================="
echo "  JoyCaption installed successfully!"
echo "=========================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Put your 20+ images into: /workspace/joy-caption-batch/input/"
echo "  2. Edit batch-alpha2.py to set your trigger word:"
echo "     PREPEND_STRING = \"yourkeyword, \""
echo "  3. Set BATCH_PROCESSING_COUNT = 4 (for 24GB GPU) or 8 (for 48GB+)"
echo "  4. Activate environment: source /workspace/joy-caption-batch/venv/bin/activate"
echo "  5. Run: cd /workspace/joy-caption-batch && python batch-alpha2.py"
echo "  6. Caption model (~17.9GB) will auto-download on first run"
echo ""
