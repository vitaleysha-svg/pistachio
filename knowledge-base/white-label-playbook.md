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

*Last updated: 2026-02-08*
*Status: All 30 LoRA training images generated and downloaded. Next: prep images + train LoRA on pod.*

### LoRA Training Roadmap (Documented 2026-02-07)
1. Generate 20 varied prompts in Midjourney with --oref --ow 250
2. Each prompt generates 4 images = 80 total
3. Cherry-pick 20-30 best (consistent face, varied angles/lighting/outfits)
4. Use MJ-safe body terms only (see section below) - save explicit descriptions for ComfyUI after LoRA training
5. Prep images: crop/resize to 1024x1024, create caption .txt files
6. Train LoRA on RunPod RTX 4090 (~30-60 min)
7. Load LoRA in ComfyUI workflow
8. All future generation: ComfyUI + LoRA (zero restrictions, zero cost per image)

---

## Midjourney Body Description Terms (Documented 2026-02-08)

### MJ-Safe Body Description Terms (Confirmed Working)
- `hourglass figure` - confirmed working, go-to replacement for explicit body terms
- `slim waist` - safe
- `toned athletic feminine figure` - safe
- `naturally curvy` - safe
- `feminine curves` - safe
- `fit figure` - safe
- `athletic build` - safe
- `elegant silhouette` - safe
- `full body photo` - safe

### MJ Banned/Filtered Body Terms (DO NOT USE)
- Any cup size (D cup, C cup, etc.)
- bust, breasts, busty
- glutes, booty, ass
- thick thighs
- voluptuous
- provocative
- lingerie, scantily clad, skimpy
- sexy
- Any specific body part measurements

### Key Insight
`--oref` at `--ow 250` does the heavy lifting for body shape from the reference image. The text prompt only needs scene/outfit/pose - not body measurements. Save explicit body descriptions for ComfyUI after LoRA training (zero content filter).

---

## Midjourney Editor / Vary (Region) Workflow (Documented 2026-02-08)

### How to Use MJ Editor for Targeted Edits
1. Click image in MJ -> open in Editor
2. Use Smart Select or Paint > Erase to mask the area to change
3. Type replacement prompt in "What will you imagine?" bar
4. Hit Submit Edit
5. MJ regenerates ONLY the masked area, keeping everything else

### Use Cases
- Remove accessories (glasses, hats)
- Modify clothing
- Change background elements

### Body Modifications via Editor
- Mask the area, prompt with safe terms (see MJ-Safe list above)
- If MJ flags the edit, use ComfyUI inpainting instead (zero filter)

---

## RunPod/ComfyUI Troubleshooting Log (2026-02-07)

### Issue: Models and custom nodes wiped on pod restart
- **Cause:** Pod was TERMINATED instead of STOPPED. Terminate destroys the volume.
- **Fix:** Always STOP, never TERMINATE. Everything under /workspace/ persists on stop.
- **Recovery:** Run download_models.ipynb (models) + install_nodes.ipynb (custom nodes). Both saved at /workspace/.
- **Prevention:** Keep download_models.ipynb, install_nodes.ipynb, and workflow JSON at /workspace/

### Issue: JupyterLab terminal corrupts pasted URLs
- **Cause:** Long URLs get split across lines when pasted into JupyterLab terminal
- **Fix:** Use Jupyter notebooks (.ipynb) instead of terminal for scripts with long URLs. Paste into notebook cells (text editor), not terminal. The notebook approach completely bypasses terminal paste issues.

### Issue: ComfyUI workflows lost after pod restart
- **Cause:** ComfyUI saves workflows to browser localStorage, tied to the proxy URL. New pod = new URL = empty localStorage.
- **Fix:** Always export workflow as .json and save to /workspace/. Import via hamburger menu > Load if localStorage is empty.

### Issue: "No results found" for InstantID nodes
- **Cause:** Custom nodes need to be installed separately from models. They live in /workspace/runpod-slim/ComfyUI/custom_nodes/
- **Fix:** Run install_nodes.ipynb which git clones ComfyUI-InstantID and ComfyUI_IPAdapter_plus, then restart ComfyUI

### Issue: Apply InstantID missing control_net and model inputs
- **Cause:** ControlNet loader node was not added. Model wire from Load Checkpoint disconnected.
- **Fix:** Add "Load ControlNet Model" node, select instantid-controlnet.safetensors, connect to Apply InstantID control_net input. Connect Load Checkpoint MODEL to Apply InstantID model.

### Issue: IPAdapter node names don't match documentation
- **Cause:** cubiq's ComfyUI_IPAdapter_plus extension uses different node names than commonly documented
- **Actual node names found:** "IPAdapter Unified Loader", "IPAdapter Advanced", "IPAdapter FaceID", "IPAdapter InsightFace Loader", "IPAdapter Unified Loader FaceID", "IPAdapter Encoder"
- **For Phase 2 face transfer:** Use "IPAdapter FaceID" (the apply node) + "IPAdapter Unified Loader FaceID" (the loader)

### ComfyUI InstantID Correct Node Setup (Verified Working)
1. Load Image (reference face)
2. Load Checkpoint (realvisxl_v5.safetensors)
3. Load InstantID Model (ip-adapter.bin)
4. Load ControlNet Model (instantid-controlnet.safetensors)
5. InstantID Face Analysis (provider: CUDA)
6. Apply InstantID (weight 0.75, end_at 0.90)
7. CLIP Text Encode x2 (positive + negative)
8. Empty Latent Image (1016x1280)
9. KSampler (steps 35, cfg 4.0, dpmpp_2m, karras)
10. VAE Decode
11. Save Image

### Issue: IPAdapter model not found
- **Cause:** Preset on IPAdapter Unified Loader FaceID was set to "FACEID" but model downloaded was FaceID Plus V2
- **Fix:** Change preset dropdown to "FACEID PLUS V2" to match the downloaded model filename (ip-adapter-faceid-plusv2_sdxl.bin)

### Issue: ClipVision model not found
- **Cause:** IPAdapter FaceID requires CLIP Vision model and FaceID LoRA, which weren't in the original download list
- **Models needed:** CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors (2.5GB, goes in models/clip_vision/), ip-adapter-faceid-plusv2_sdxl_lora.safetensors (371MB, goes in models/loras/)
- **Fix:** Created download_clipvision.ipynb to download both. Added to pod at /workspace/

### Issue: Considered automating MJ with Playwright (2026-02-08)
- **Risk:** Permanent account ban per MJ ToS, no refund, no appeal
- MJ actively detects automation tools (confirmed bans as of Jan 2025)
- **Solution:** Manual copy-paste (30 prompts = ~30 min). Save automation for ComfyUI on pod (no restrictions)
- **Source:** MJ Community Guidelines, GitHub issues, Make Community reports
- **Rule:** NEVER automate Midjourney. Manual only. Automate everything on ComfyUI/RunPod side instead.

### Recovery Checklist (If Pod Wipes)
1. Upload download_models.ipynb -> Run (downloads all models)
2. Upload install_nodes.ipynb -> Run (installs custom nodes + restarts ComfyUI)
3. Upload instantid-phase1.json -> Import in ComfyUI
4. Upload hero image
5. Ready to generate in ~10 minutes
