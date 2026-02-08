# White Label Playbook - AI Influencer Setup System

> Document every step, cost, tool, and decision so we can package and sell this as a service/product.
> Target: People like cousin who paid $4K for unknown system/platform.

---

## What We're Building (The Product)

A complete system to create and run an AI influencer from scratch:
- Face generation + consistency pipeline
- Content generation across scenarios
- Platform setup (Fanvue, Instagram, ManyChat)
- DM automation + monetization
- Prompt engineering system that compounds

---

## Setup Steps Completed (Chronological)

### 1. RunPod Cloud GPU Setup
- **What:** Cloud GPU rental for AI image generation
- **Platform:** RunPod (runpod.io)
- **GPU:** RTX 4090 (24GB VRAM)
- **Cost:** $0.62/hr running, $0.01/hr stopped (idle storage)
- **Template:** Official ComfyUI template
- **Pod name:** yabbering_orange_mammal-migration
- **Pod ID:** h0r68bqsw0lepy
- **Lesson:** Use official templates, not pytorch template (port exposure issues)
- **Lesson:** Pod migration happens when GPU gets claimed - choose "Automatically migrate"
- **Lesson:** Delete old pod after migration to stop idle charges

### 2. ComfyUI Installation
- **What:** Node-based AI image generation interface (like visual programming)
- **How:** Came pre-installed with RunPod template
- **Access:** Port 8188 via RunPod Connect menu
- **Path on server:** /workspace/runpod-slim/ComfyUI/
- **Lesson:** Path varies by template - use `find` to locate if unsure
- **Lesson:** Use python3 not python on RunPod

### 3. Custom Nodes Installed
- **ComfyUI-Manager** - Node marketplace (pre-installed with template)
- **ComfyUI_InstantID** - Face locking from reference photo (git cloned from cubiq)
- **comfyui_ipadapter_plus** - Additional face/style transfer
- **ComfyUI-KJNodes** - Utility nodes
- **Civi comfy** - CivitAI model integration
- **Lesson:** Original InstantID install was broken (folder existed but nodes didn't load)
- **Lesson:** Fix: rm -rf old folder, fresh git clone, pip install insightface onnxruntime-gpu
- **Lesson:** Always verify nodes show up in search after install

### 4. AI Models Downloaded
| Model | Purpose | Size | Path |
|-------|---------|------|------|
| InsightFace antelopev2 | Face detection | ~344MB | models/insightface/models/antelopev2/ |
| InstantID ip-adapter.bin | Face copying | ~1.6GB | models/instantid/ |
| InstantID ControlNet | Face structure preservation | ~2.3GB | models/controlnet/instantid-controlnet.safetensors |
| IP-Adapter FaceID plusv2 SDXL | Face consistency | ~1.4GB | models/ipadapter/ |
| RealVisXL v5 | Base image generation (realistic) | ~6.5GB | models/checkpoints/realvisxl_v5.safetensors |
- **Total download:** ~12GB
- **Lesson:** Download via wget in terminal, not through browser
- **Lesson:** Web terminal breaks long commands - paste short commands one at a time
- **Lesson:** unzip not available on some images - use python3 zipfile module instead
- **Lesson:** URLs change/break - RealVisXL_V5.0.safetensors 404'd, fp16 version worked

### 5. Workflow Building (IN PROGRESS)
- **Nodes needed:** Load Checkpoint, Load Image, Load InstantID Model, InstantID Face Analysis, Apply InstantID, 2x CLIP Text Encode, KSampler, Empty Latent Image, VAE Decode, Save Image
- **Reference image:** 1 Midjourney face image (master reference)
- **How it works:** InstantID copies face from reference onto any scenario you describe in prompt

### 6. InstantID Settings Optimization (Phase 1 Fix - 2026-02-06)
- **Problem:** First output was 3/10 - dark face, fake hat, wrong lighting, AI look
- **Root causes:** InstantID weight too high (burn effect), CFG too high, prompt fighting reference, txt2img losing OG quality
- **Optimized settings:**

| Setting | Before | After | Why |
|---------|--------|-------|-----|
| InstantID weight | 0.80 | **0.75** | Community consensus: 0.70-0.80 max |
| CFG | 8.0 | **4.0** | InstantID needs low CFG (4.0-4.5) |
| Steps | 20 | **35** | More refinement, smoother result |
| Resolution | 1024x1280 | **1016x1280** | Avoids SDXL training artifacts at exact 1024 |

- **Lesson:** InstantID weight > 0.85 causes "burn" effect - over-processed, fake AI look
- **Lesson:** CFG > 5.0 with InstantID amplifies artifacts
- **Lesson:** Positive prompt must MATCH reference image vibe (outdoor ref = outdoor prompt)
- **Lesson:** Use weighted negative prompts for SDXL: `(airbrushed:1.4), (smooth skin:1.3)`
- **Lesson:** If Phase 1 not enough, add IP-Adapter FaceID for style/quality transfer
- **Lesson:** If still not enough, switch to img2img (denoise 0.40) to preserve OG image quality

---

## Tools & Costs Summary

| Tool | Cost | What It Does |
|------|------|-------------|
| RunPod | ~$0.62/hr GPU, $0.01/hr idle | Cloud GPU for image generation |
| Midjourney | $30/month | Initial face/look creation |
| ComfyUI | Free (open source) | Image generation workflow builder |
| InstantID | Free (open source) | Face consistency from 1 photo |
| RealVisXL | Free (open source) | Realistic image generation model |
| ManyChat | Free to start | DM automation |
| Fanvue | Free (20% revenue cut) | Content monetization platform |

**Month 1 total overhead:** ~$35-50

---

## Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| Pod GPU not available | Choose "Automatically migrate" |
| Paste not working in web terminal | Right-click > Paste or Ctrl+Shift+V |
| Long commands break in terminal | Split into shorter commands, paste one at a time |
| Custom node installed but not showing | Delete folder, fresh git clone, install dependencies, restart ComfyUI |
| unzip not available | `python3 -c "import zipfile; zipfile.ZipFile('file.zip').extractall('.')"` |
| ComfyUI not loading models | Restart: pkill + python3 main.py --listen 0.0.0.0 --port 8188 & |
| wget URL 404 | Check HuggingFace for correct filename (fp16 vs full) |
| InstantIDFaceAnalysis AssertionError | antelopev2 models nested in subfolder. Fix: `mv .../antelopev2/antelopev2/* .../antelopev2/` then `rmdir` the nested folder |
| Missing control_net input on Apply InstantID | Add "Load ControlNet Model" node, select `instantid-controlnet.safetensors`, connect CONTROL_NET output to Apply InstantID control_net input |
| Output looks "AI burned" / dark face / plastic | InstantID weight too high (>0.85). Lower to 0.75. Also lower CFG to 4.0 |
| Output doesn't match reference vibe | Prompt fighting reference. If OG is outdoor/candid, prompt must be outdoor/candid |
| Face structure right but quality wrong | Add IP-Adapter FaceID (PLUS FACE portraits, weight 0.60-0.70) for quality transfer |
| Need tighter match to reference | Switch to img2img: Load Image + VAE Encode + denoise 0.40 instead of Empty Latent |

---

## White Label Pricing Research

- **Cousin paid:** $4,000 (unknown what system/platform - NEED TO FIND OUT)
- **Our actual cost:** ~$35-50/month
- **Potential pricing tiers:**
  - DIY Guide: $297-497 (documentation + video walkthrough)
  - Done-With-You: $1,500-2,500 (setup call + templates + support)
  - Done-For-You: $3,000-5,000 (we set everything up, they just create content)
- **TODO:** Ask cousin exactly what he paid for and what he got

---

## Skills/Knowledge Required (For White Label Training)

- [ ] RunPod account setup and pod management
- [ ] ComfyUI basics (nodes, connections, workflows)
- [ ] Model downloading and installation
- [ ] Midjourney prompt engineering for initial face
- [ ] InstantID workflow building
- [ ] Prompt engineering for scenarios
- [ ] Face consistency quality control
- [ ] Platform setup (Fanvue, Instagram)
- [ ] DM automation (ManyChat)
- [ ] Content calendar management

---

*Last updated: 2026-02-06*
*Status: IN PROGRESS - Phase 1 settings fix ready, awaiting test on ComfyUI*
