#!/bin/bash
# =============================================================
# PISTACHIO - RunPod LoRA Training Setup Script
# =============================================================
# USAGE: Deploy "Kohya_ss" template on RunPod (RTX 4090),
# open terminal, paste this script.
# OR: Run this on your existing ComfyUI pod if it has enough disk.
# =============================================================

echo "=========================================="
echo "PISTACHIO - LoRA Training Setup Starting..."
echo "=========================================="

cd /workspace || cd /root

# ----- STEP 1: Install Kohya SS -----
echo ""
echo "[1/4] Installing Kohya SS..."

if [ ! -d "kohya_ss" ]; then
    git clone https://github.com/bmaltais/kohya_ss.git
    cd kohya_ss
    pip install -r requirements.txt -q
    cd ..
else
    echo "  -> Kohya SS already installed"
fi

# ----- STEP 2: Download SDXL Base for Training -----
echo ""
echo "[2/4] Downloading SDXL Base Model for Training..."

mkdir -p models
if [ ! -f "models/sd_xl_base_1.0.safetensors" ]; then
    wget -q --show-progress -O models/sd_xl_base_1.0.safetensors \
        "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"
else
    echo "  -> SDXL base already downloaded"
fi

# ----- STEP 3: Set Up Training Dataset Directory -----
echo ""
echo "[3/4] Setting up training directories..."

mkdir -p training_data/pistachio/img
mkdir -p training_data/pistachio/model
mkdir -p training_data/pistachio/log

echo "  -> Created training_data/pistachio/img/"
echo "  -> Created training_data/pistachio/model/"
echo "  -> Created training_data/pistachio/log/"

# Create the dataset config
cat > training_data/pistachio/dataset_config.toml << 'DATASET_EOF'
[general]
shuffle_caption = true
caption_extension = '.txt'
keep_tokens = 1

[[datasets]]
resolution = 1024
batch_size = 1
keep_tokens = 1

  [[datasets.subsets]]
  image_dir = '/workspace/training_data/pistachio/img'
  num_repeats = 10
DATASET_EOF

echo "  -> Created dataset_config.toml"

# ----- STEP 4: Create Training Launch Script -----
echo ""
echo "[4/4] Creating training launch script..."

cat > train_pistachio_lora.sh << 'TRAIN_EOF'
#!/bin/bash
# =============================================================
# PISTACHIO LoRA Training Script
# =============================================================
# Before running: Put 15-30 captioned images in
# training_data/pistachio/img/
# Each image needs a matching .txt caption file
# Example: image01.png + image01.txt
# =============================================================

cd /workspace/kohya_ss

accelerate launch --num_cpu_threads_per_process=2 sdxl_train_network.py \
  --pretrained_model_name_or_path="/workspace/models/sd_xl_base_1.0.safetensors" \
  --dataset_config="/workspace/training_data/pistachio/dataset_config.toml" \
  --output_dir="/workspace/training_data/pistachio/model" \
  --output_name="pistachio_lora_v1" \
  --save_model_as=safetensors \
  --prior_loss_weight=1.0 \
  --max_train_epochs=10 \
  --learning_rate=1e-4 \
  --optimizer_type="AdamW8bit" \
  --xformers \
  --mixed_precision="fp16" \
  --cache_latents \
  --gradient_checkpointing \
  --save_every_n_epochs=2 \
  --network_module=networks.lora \
  --network_dim=32 \
  --network_alpha=16 \
  --train_batch_size=1 \
  --bucket_reso_steps=64 \
  --min_bucket_reso=512 \
  --max_bucket_reso=1536 \
  --logging_dir="/workspace/training_data/pistachio/log" \
  --log_prefix="pistachio_" \
  --caption_extension=".txt" \
  --seed=42

echo ""
echo "=========================================="
echo "LoRA TRAINING COMPLETE!"
echo "=========================================="
echo "Output: /workspace/training_data/pistachio/model/pistachio_lora_v1.safetensors"
echo ""
echo "To use in ComfyUI:"
echo "  1. Copy .safetensors to ComfyUI/models/loras/"
echo "  2. Use trigger word: pistachio_character"
echo "  3. LoRA strength: 0.7-1.0"
echo "=========================================="
TRAIN_EOF

chmod +x train_pistachio_lora.sh

echo ""
echo "=========================================="
echo "LoRA TRAINING SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Upload 15-30 images to training_data/pistachio/img/"
echo "  2. Create a .txt caption file for each image"
echo "     Example caption: 'photo of pistachio_character, a 21 year old"
echo "     Egyptian Brazilian woman with tooth gap and frizzy dark hair'"
echo "  3. Run: bash /workspace/train_pistachio_lora.sh"
echo "  4. Training takes ~30-60 min on RTX 4090"
echo "  5. Output goes to training_data/pistachio/model/"
echo ""
echo "CAPTIONING TIP:"
echo "  Each .txt file should describe what's in the image,"
echo "  starting with the trigger word 'pistachio_character'"
echo "  Keep descriptions factual: what she looks like, wearing,"
echo "  setting, lighting, pose."
echo "=========================================="
