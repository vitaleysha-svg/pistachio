# Pistachio — Knowledge Base
## AI Image Generation Workflow Project

### Team
- **Vitaley Shaulov** — Business lead
- **Matt** — Business partner
- **Mark** (Vitaley's cousin) — Current practitioner, workflow expertise

### Project Goal
Build a consistent, scalable AI image generation workflow using ComfyUI that overcomes the limitations of cloud-based platforms.

### Mark's Current Workflow (Pre-Pistachio)
- **Platform:** Higgs Field
- **Model/Tool:** Grok
- **Method:** Prompts for detailed, explicit image generation
- **Limitations:** Inconsistent results, platform restrictions, not sustainable long-term
- **Solution direction:** ComfyUI (local, open-source, unrestricted)

### Target Stack
- **ComfyUI** — Node-based UI for Stable Diffusion workflows (local execution)
- **DiffusionPipe** — LoRA training framework (github.com/tdrussell/diffusion-pipe)
- **JoyCaption** — Automated image captioning for training datasets
- **Wan 2.1** — Base model for LoRA training (T2V-14B)
- **wandb (Weights & Biases)** — Training evaluation/monitoring

---

## INCOMING DATA LOG

### Source 1: YouTube Video — "The Only Video You Need to Watch to Master ComfyUI/AI Models"
- **Status:** INGESTED
- **Type:** Foundational ComfyUI knowledge — terminology, setup, workflow loading, error resolution

### Source 2: YouTube Video — "Most Comprehensive LoRA Training Tutorial"
- **Status:** INGESTED
- **Type:** Full LoRA training pipeline — DiffusionPipe, JoyCaption, Wan 2.1, evaluation, workflow integration

### Source 3: Mark's Current Workflow Call
- **Status:** UPCOMING — Vitaley & Mark call to document exact current process
- **Notes:** Will detail Higgs Field workflow, Grok usage, prompting techniques, current limitations

---

## SYNTHESIZED KNOWLEDGE

### 1. CORE TERMINOLOGY

| Term | Definition |
|------|-----------|
| **Model** | The AI file (ones and zeros) that generates images. Open-source models are downloadable .safetensors files you run locally. Closed-source models (NanoBanana Pro, SeeDream) are accessed via API and cost per generation. |
| **Node** | A single processing block in ComfyUI that performs one function (load model, load image, denoise, encode, etc.). Nodes are the building blocks. |
| **Workflow** | A collection of connected nodes that form a complete image generation pipeline. Saved as .json files. The entire canvas of connected nodes = one workflow. |
| **Custom Nodes** | Community-created nodes for specific use cases. Must be installed separately. This is where most errors come from when loading new workflows. |
| **LoRA** | Low-Rank Adaptation — small fine-tuned model files that modify a base model's output (style, character, concept). Much smaller than full models. The key to consistent character faces. |
| **VAE** | Variational Auto-Encoder — handles encoding/decoding between pixel space and latent space. Some workflows require specific VAEs. |
| **Checkpoint** | A full model file (large, multi-GB). Contains all weights needed to generate images. |
| **CLIP** | Text encoder that converts your prompt into tokens the model understands. Some workflows need specific CLIP models. |
| **Diffusion Model** | The core image generation model. Works by starting with noise → predicting noise → subtracting it → repeating for N steps → final image. |
| **Steps** | Number of denoising iterations. More steps = sharper/more detailed image but slower. Fewer steps = faster but potentially less refined. Fully customizable in ComfyUI. |
| **.safetensors** | File format for AI models. Safe, efficient, standard format for Stable Diffusion models. |
| **.json** | File format for ComfyUI workflows. Drag-and-drop into ComfyUI to load. |
| **Trigger Word / Keyword** | A unique token (e.g., "blonde3g") prepended to every caption during LoRA training. Used in prompts to activate the LoRA character. Must be something unique that wasn't in the base model's training data. |
| **DiffusionPipe** | Open-source LoRA training framework (github.com/tdrussell/diffusion-pipe). Supports Wan 2.1, Flux, SDXL, and 20+ models. Key advantage: built-in evaluation graphs via wandb so you can pick the mathematically best checkpoint. |
| **JoyCaption** | AI-powered image captioning tool. Takes a folder of images and generates .txt description files for each one. Critical for LoRA training dataset preparation. |
| **wandb (Weights & Biases)** | Training monitoring platform. Shows loss graphs during LoRA training so you can identify which checkpoint (step) converged best. Free account at wandb.ai. |
| **Epoch** | One complete pass through all training images. Multiple epochs = model sees images multiple times. |
| **Convergence** | The point where the loss graph bottoms out — this is the best checkpoint to use. Before = undertrained. After = overtrained. |
| **Overtrained** | Model has memorized training images too precisely. Can only reproduce the training data, loses ability to generalize to new poses/settings. Happens at high step counts past convergence. |
| **Undertrained** | Model hasn't seen images enough times. Can't consistently reproduce the face/character. Happens at low step counts before convergence. |

### 2. WHY COMFYUI (vs. API Models)

**Advantages over NanoBanana Pro / SeeDream / other API services:**
1. **Full customization** — control steps, CFG, sampler, scheduler, resolution, and 1000+ other parameters
2. **NSFW capability** — API models have content restrictions. ComfyUI running open-source models locally has none
3. **Cost** — open-source models are free to run. You only pay for compute (GPU rental or your own hardware)
4. **Open source models** — downloadable files you own and control, not dependent on a company's API staying online
5. **Workflow flexibility** — build any pipeline you want by connecting nodes
6. **LoRA compatibility** — load custom-trained LoRA models for consistent characters

**Disadvantages:**
- Steeper learning curve
- Requires GPU (local or rented via RunPod etc.)
- Error troubleshooting is part of the process (but learnable)

### 3. HOW IMAGE GENERATION WORKS (Diffusion Process)

1. Start with a **noise image** (random static)
2. Model predicts what noise is present
3. Subtract predicted noise from the image
4. Repeat for N steps (configurable)
5. Final result = generated image

More steps = more refinement. This is why ComfyUI's step control matters — API models give you no control over this.

### 4. KEY PLATFORMS & RESOURCES

| Platform | Purpose |
|----------|---------|
| **CivitAI.com** | Primary source for workflows, models, LoRAs, checkpoints. Download workflows as .json files. Browse by model type. |
| **Hugging Face** | Primary repository for AI model files. Many models require HF account + API token to download. Token: HuggingFace.co/settings/tokens → create new token → "access repositories" permission. |
| **RunPod** | Virtual GPU rental service. Run ComfyUI in the cloud without local hardware. Uses JupyterLab as CLI interface. |
| **JupyterLab** | Terminal/CLI interface used on RunPod to execute download commands, manage files, restart ComfyUI. |
| **wandb.ai** | Training monitoring. Free account. Provides real-time loss graphs during LoRA training. API key needed for config. |
| **GitHub: tdrussell/diffusion-pipe** | LoRA training framework. Open source. Supports 22+ models including Wan 2.1, Flux, SDXL. |
| **GitHub: MNeMoNiCuZ/joy-caption-batch** | Batch image captioning tool for dataset preparation. |

### 5. WORKFLOW LOADING PROCESS (Step-by-Step)

**Step 1: Find and download a workflow**
- Go to CivitAI.com
- Find the workflow you want (e.g., Flux Client High Resolution)
- Download it (downloads as .zip or .json)
- Extract if .zip → you'll get .json workflow file(s)
- Note: different parameter versions may be available (e.g., 9B = higher quality, 4B = lighter/faster)

**Step 2: Load into ComfyUI**
- Drag and drop the .json file directly into ComfyUI
- Workflow loads with all its nodes visible

**Step 3: You WILL get errors — this is normal**

### 6. UNIVERSAL ERROR RESOLUTION (The Two Errors You'll Always Get)

Every workflow you download will produce one or both of these errors. Once you can solve them, you can run ANY workflow.

#### ERROR TYPE 1: Missing Custom Nodes
**Symptom:** Red squares on nodes, error message saying "some nodes are missing"

**Fix:**
1. Go to **Manager** (ComfyUI Manager must be installed)
2. Click **"Install Missing Custom Nodes"**
3. You'll see a list of node sets that need installing
4. Install them **one at a time** — wait for each to complete before starting the next
5. After all are installed, click **Restart** and confirm
6. Wait 3-5 minutes for ComfyUI to reload
7. Red squares should be gone

**Edge case:** Sometimes a custom node isn't found in the Manager. In that case:
- Copy the exact error message
- Paste into any AI (GPT, Gemini, Claude)
- Give context: "I'm trying to run ComfyUI workflow on [RunPod/local] and getting this error"
- AI will provide exact terminal commands to install manually
- 99% success rate

#### ERROR TYPE 2: Missing Models / LoRAs / VAEs / Checkpoints
**Symptom:** Click Run → error about missing model files, missing LoRAs, missing VAEs, etc.

**Fix:**
1. Click **Run** to trigger the error
2. **Copy the entire error message**
3. Paste into any AI assistant
4. Tell it: *"I am trying to run ComfyUI workflow on [RunPod/local] and this is the error I'm getting. Search for these models on the internet, especially Hugging Face, and give me the exact command to download them. Install path: Workspace/ComfyUI/models/[category]"*
   - Categories: `diffusion_models/`, `loras/`, `vae/`, `clip/`, etc.
5. AI searches Hugging Face, finds the models, gives you exact download commands (usually `wget` or `huggingface-cli download`)
6. Paste commands into JupyterLab/terminal
7. Wait for downloads (model files are often multiple GB)
8. Restart ComfyUI

**Hugging Face authentication (sometimes required):**
- Some models are gated and require HF token
- Go to HuggingFace.co → Settings → Tokens → Create New Token
- Permission needed: "Access repositories"
- Run `huggingface-cli login` and paste your token when prompted

---

## 7. LORA TRAINING — COMPLETE PIPELINE

### Why Train a LoRA

Base image models contain millions of training images but can never produce a **consistent face**. Every generation gives you a different person. LoRA training solves this:
- You feed 20 images of your character into the base model
- You caption each image with a unique trigger word (e.g., "blonde3g")
- The model learns to associate that trigger word with that specific face
- After training, every time you use the trigger word in a prompt, you get the same consistent face

### Why DiffusionPipe (vs. AI Toolkit, Kohya, etc.)

DiffusionPipe is the only tool that provides **evaluation graphs via wandb**. This eliminates guesswork:
- Training saves checkpoints every N steps
- The loss graph shows where the model converged (bottomed out)
- You pick the checkpoint at the lowest point = mathematically best result
- Without eval: you'd have to manually test every checkpoint visually
- With eval: you just read the graph and download the right one

### The Complete LoRA Training Process (Overview)

1. **Generate/collect 20+ images** of your character (consistent face, varied poses/settings)
2. **Caption every image** using JoyCaption (automated) — each image gets a .txt file with trigger word + description
3. **Prepare training data** — split into train (80%) and eval (20%) folders
4. **Install DiffusionPipe** on your GPU instance
5. **Download base model** (Wan 2.1 T2V-14B) files
6. **Configure training** — set output folder, batch size, steps, wandb monitoring
7. **Run training** — wait 1-6 hours depending on GPU
8. **Read the eval graph** on wandb — find where loss bottomed out
9. **Download the best checkpoint** — the adapter_model.safetensors at the convergence step
10. **Load into ComfyUI** — drop into models/loras/, select in workflow, use trigger word in prompts

### 7A. JOYCAPTION — Image Captioning

**What it does:** Takes a folder of images and generates a .txt caption file for each one. Example: image of girl sitting on chair → "blonde3g, a young woman with platinum blonde hair sitting on a wooden chair in a sunlit room"

**Open-source repo:** `github.com/MNeMoNiCuZ/joy-caption-batch`

**Key settings in batch-alpha2.py:**
- `PREPEND_STRING = "blonde3g, "` — your trigger word, prepended to every caption
- `BATCH_PROCESSING_COUNT = 8` — images processed at once. Lower for smaller GPUs (4 or 2 for 24GB)
- `INPUT_FOLDER` — where your images go (default: ./input/)
- `OVERWRITE = True` — regenerate existing captions
- `MAX_NEW_TOKENS = 300` — caption length limit
- `TEMPERATURE = 0.5` — caption creativity (lower = more literal)

**Model:** Auto-downloads ~17.9GB from HuggingFace on first run (`fancyfeast/llama-joycaption-alpha-two-hf-llava`)

**Output:** For each image.png, creates image.txt with "trigger_word, detailed description of the image"

### 7B. DIFFUSIONPIPE — Training Framework

**Open-source repo:** `github.com/tdrussell/diffusion-pipe`

**Config format:** TOML files (not YAML)

**Two config files needed:**
1. **Training config** — model paths, optimizer, batch size, save frequency, wandb settings
2. **Dataset config** — data folder paths, resolutions, aspect ratio buckets

**Training command:**
```
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
NCCL_P2P_DISABLE="1" NCCL_IB_DISABLE="1" \
deepspeed --num_gpus=1 train.py --deepspeed --config training_config.toml
```

**Output:** Saves checkpoints at configured intervals. Each checkpoint contains `adapter_model.safetensors` (the LoRA file). LoRA saves in ComfyUI-compatible format for Wan models.

**Supported models:** Wan 2.1/2.2, Flux, SDXL, HunyuanVideo, LTX-Video, Cosmos, Lumina, HiDream, Z-Image, and 15+ more.

### 7C. WAN 2.1 — Base Model

**HuggingFace:** All openly downloadable (Apache 2.0, NO gating)

**Files needed for LoRA training (minimum ~22GB):**

| File | Size | Source | Purpose |
|------|------|--------|---------|
| Wan2.1-T2V-14B config directory | ~0.5 GB | Wan-AI/Wan2.1-T2V-14B | config.json + VAE (required by DiffusionPipe) |
| wan2.1_t2v_14B_fp16.safetensors | 28.6 GB | Comfy-Org repackaged | Diffusion transformer (or fp8 at 14.3 GB) |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | 6.7 GB | Comfy-Org repackaged | Text encoder |
| wan_2.1_vae.safetensors | 254 MB | Comfy-Org repackaged | VAE |

**Wan 2.1 vs 2.2:** Wan 2.2 uses Mixture-of-Experts (27B params, 14B active). More complex to train (need separate LoRAs for high/low noise experts). Wan 2.1 is simpler — single model, single LoRA. **Stick with 2.1 for now.**

### 7D. WANDB — Training Evaluation

**What it does:** Real-time graphs showing training loss at each step. The loss curve shows where the model converged.

**How to read the graph:**
- Loss goes DOWN = model is learning
- Loss BOTTOMS OUT = convergence point = BEST checkpoint
- Loss goes back UP or flattens with overfit artifacts = overtrained

**Setup:**
1. Create free account at wandb.ai
2. Get API key from wandb.ai/settings (or wandb.ai/quickstart)
3. Add to training config: `wandb_api_key`, `wandb_tracker_name`, `wandb_run_name`
4. During training, wandb provides a link to view graphs in real-time

**Picking the best checkpoint:**
- Hover over the convergence point on the graph
- Note the step number (e.g., step 250)
- Go to your output folder → find the checkpoint at that step
- Download `adapter_model.safetensors` from that checkpoint folder

### 7E. GPU CONFIGURATION — RTX vs H200

**RTX (24GB VRAM, ~$0.34-0.70/hr) vs H200 (80GB VRAM, ~$3.50/hr):**

| Setting | H200 (80GB) | RTX 4090 (24GB) |
|---------|-------------|-----------------|
| micro_batch_size_per_gpu | 8 | **1** |
| gradient_accumulation_steps | 1 | **4-8** |
| activation_checkpointing | optional | **true** (required) |
| blocks_to_swap | 0 | **24-32** |
| transformer_dtype | bfloat16 | **nf4** or float8 |
| optimizer | AdamW | **AdamW8bitKahan** |
| Training time (20 images) | ~30-90 min | **~3-6 hours** |
| Cost per training run | ~$3-5 | **~$1-2** |

**Gradient accumulation** compensates for smaller batch size:
- Effective Batch = micro_batch × gradient_accumulation
- 1 × 8 = 8 (same effective batch as H200)
- Mathematically equivalent results, just takes longer

**Best budget GPUs on RunPod:**
| GPU | VRAM | $/hr | Notes |
|-----|------|------|-------|
| RTX A6000 | 48GB | $0.33 | Best value — 48GB means less config hassle |
| A40 | 48GB | $0.35 | Similar to A6000 |
| RTX 4090 | 24GB | $0.34 | Fast but needs memory optimizations |
| RTX 3090 | 24GB | $0.22 | Cheapest, still works great |

**Recommendation:** RTX A6000 or A40 ($0.33-0.35/hr) — 48GB VRAM means you can use batch_size 2-4 without aggressive memory hacks. Cheaper than the RTX the user mentioned at $0.60-0.70/hr and MORE VRAM.

---

## 8. MODELS REFERENCE

| Model | Type | Notes |
|-------|------|-------|
| **Wan 2.1 T2V-14B** | Open-source diffusion model | Base model for LoRA training. 14B parameters. Best results per the video creator. |
| **Wan 2.2** | Open-source diffusion model (MoE) | Newer but more complex to train. Skip for now. |
| **Flux (Flux Client)** | Diffusion model | Available in 9B and 4B parameter versions. Popular for high-res generation. |
| **NanoBanana Pro** | Closed-source API model | Good results but no customization, costs per generation, content restrictions |
| **SeeDream** | Closed-source API model | Similar limitations to NanoBanana Pro |
| **SDXL** | Open-source diffusion model | Stable Diffusion XL, widely used base model |

---

## 9. FILE STRUCTURE ON VIRTUAL GPU (RunPod)

### For LoRA Training:
```
/workspace/
├── joycaption-batch/           ← JoyCaption captioning tool
│   ├── input/                  ← Put your 20+ images here
│   ├── batch-alpha2.py         ← Main captioning script
│   └── venv/                   ← Python environment
├── diffusion-pipe/             ← Training framework
│   ├── train.py                ← Main training script
│   ├── examples/               ← Put your config files here
│   └── models/                 ← Base model files go here
│       └── wan/
│           ├── Wan2.1-T2V-14B/ ← Official checkpoint dir (config.json)
│           ├── wan2.1_t2v_14B_fp16.safetensors
│           ├── umt5_xxl_fp8_e4m3fn_scaled.safetensors
│           └── wan_2.1_vae.safetensors
├── your_dataset/               ← Prepared training data
│   ├── train/                  ← 80% of captioned images
│   └── eval/                   ← 20% of captioned images
└── output/                     ← Training output (checkpoints)
```

### For ComfyUI (inference after training):
```
/workspace/ComfyUI/
└── models/
    ├── diffusion_models/       ← Base models (.safetensors)
    ├── loras/                  ← Your trained LoRA goes here
    ├── vae/                    ← VAE files
    ├── clip/                   ← CLIP/text encoder models
    └── checkpoints/            ← Full checkpoint files
```

---

## 10. KEY TAKEAWAYS

### From Video 1 (ComfyUI Fundamentals):
1. ComfyUI is the software that runs open-source models with full control
2. Workflows are everything — download from CivitAI, don't build from scratch
3. Every workflow breaks on first load — NORMAL
4. Two-error pattern is universal — missing custom nodes (Manager) + missing models (AI + HuggingFace)
5. Open source = no restrictions — core reason for ComfyUI

### From Video 2 (LoRA Training):
1. LoRA training = the solution to consistent faces/characters
2. DiffusionPipe is the best training tool because of eval graphs (wandb)
3. JoyCaption automates the tedious captioning step
4. The eval graph eliminates guesswork — pick the convergence point checkpoint
5. Wan 2.1 produces the best results for this use case
6. RTX GPUs work fine — just adjust batch size and enable memory optimizations
7. The entire pipeline is open source — no Discord paywall needed

---

## WORKFLOW CHECKLIST (For Any New Workflow)

- [ ] Download .json from CivitAI
- [ ] Drag into ComfyUI
- [ ] Manager → Install Missing Custom Nodes (one at a time)
- [ ] Restart ComfyUI (wait 3-5 min)
- [ ] Click Run → copy model errors
- [ ] Paste errors into AI → get download commands
- [ ] Run download commands in terminal (check HF auth if needed)
- [ ] Restart ComfyUI
- [ ] Run workflow — should work

## LORA TRAINING CHECKLIST

- [ ] Generate/collect 20+ consistent images of character
- [ ] Upload images to GPU instance
- [ ] Run JoyCaption to generate captions (set trigger word first)
- [ ] Review captions (spot check a few .txt files)
- [ ] Create dataset folders (train/ + eval/, 80/20 split)
- [ ] Move captioned images+txts to train/ and eval/
- [ ] Install DiffusionPipe
- [ ] Download Wan 2.1 base model files
- [ ] Configure training TOML (output dir, model paths, batch size, wandb)
- [ ] Configure dataset TOML (data folder path, resolutions, AR buckets)
- [ ] Set up wandb account + API key
- [ ] Run training
- [ ] Monitor loss graph on wandb
- [ ] Identify convergence step
- [ ] Download adapter_model.safetensors from best checkpoint
- [ ] Upload LoRA to ComfyUI models/loras/
- [ ] Load Wan workflow in ComfyUI
- [ ] Select LoRA, add trigger word to prompt
- [ ] Generate and verify consistent character

---

## STILL NEEDED (Gaps to Fill)

- Mark's exact current workflow details (Higgs Field + Grok process)
- Initial 20-image dataset generation method (Airtable method referenced in video, or alternative)
- Prompt engineering strategies for consistent character output
- Upscaling workflows for final output quality
- Batch generation / automation workflows
- Video generation workflows (Wan 2.1 T2V capabilities)
- Multiple character LoRAs (can you combine them?)
- Best practices for trigger word selection

