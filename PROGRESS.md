# Pistachio Progress Tracker
# AUTO-COMPACT RECOVERY FILE - Claude dumps state here before/during every session

## Last Updated: 2026-02-06 (late night session)

## Current Phase: PRE-LAUNCH SETUP - Models Installed, Ready to Build Workflow

## What Just Happened (Latest Session)
- Pod migrated to new GPU (yabbering_orange_mammal-migration, ID: h0r68bqsw0lepy)
- OLD pod (h74hl96oos9brr) should be deleted if not already
- ALL models downloaded and verified:
  - InsightFace antelopev2 (face detection) - /workspace/runpod-slim/ComfyUI/models/insightface/models/antelopev2/
  - InstantID ip-adapter.bin (face copying) - /workspace/runpod-slim/ComfyUI/models/instantid/
  - InstantID ControlNet (face structure) - /workspace/runpod-slim/ComfyUI/models/controlnet/instantid-controlnet.safetensors
  - IP-Adapter FaceID plusv2 SDXL - /workspace/runpod-slim/ComfyUI/models/ipadapter/
  - RealVisXL v5 checkpoint (6.5GB) - /workspace/runpod-slim/ComfyUI/models/checkpoints/realvisxl_v5.safetensors
- Reinstalled ComfyUI_InstantID custom node (fresh git clone from cubiq)
- Installed insightface + onnxruntime-gpu dependencies
- InstantID nodes now show up in ComfyUI (Apply InstantID, Apply InstantID Advanced, InstantID Apply ControlNet)
- First reference image decomposed (Fukushima Larissa - Japanese/Brazilian, 21)
- MJ prompts generated in prompt-reverse-engineering workflow
- Built prompt reverse-engineering system (knowledge-base/prompt-reverse-engineering.md)
- Created iteration log (knowledge-base/prompt-iterations.md)
- Created prd.json for Ralph Loop tracking
- Persona changed: Egyptian/Brazilian -> Japanese/Brazilian mix

## What We're Doing RIGHT NOW
- Building InstantID workflow in ComfyUI - connecting nodes
- Reference face image UPLOADED (Pistachio741_Mixed_Japanese-Br...)
- All models loaded and working
- Connections completed so far (7 of 14):
  1. Load Checkpoint MODEL → Apply InstantID model (DONE)
  2. Load Image IMAGE → Apply InstantID image (DONE)
  3. Load InstantID Model INSTANTID → Apply InstantID instantid (DONE)
  4. InstantID Face Analysis FACEANALYSIS → Apply InstantID insightface (DONE)
  5. Load Checkpoint CLIP → both CLIP Text Encode clip inputs (DONE)
  6. Top CLIP Text Encode CONDITIONING → Apply InstantID positive (DONE)
  7. Bottom CLIP Text Encode CONDITIONING → Apply InstantID negative (DONE)
- REMAINING connections:
  8. Apply InstantID MODEL → KSampler model
  9. Apply InstantID positive → KSampler positive
  10. Apply InstantID negative → KSampler negative
  11. Empty Latent Image LATENT → KSampler latent_image
  12. KSampler LATENT → VAE Decode samples
  13. Load Checkpoint VAE → VAE Decode vae
  14. VAE Decode IMAGE → Save Image images
- AFTER connections: set Empty Latent Image to 1024x1280, add prompts, run

## What We're Working On NEXT (after workflow)
- Generate first test image with face consistency
- Compare output to reference, iterate on prompts
- Generate scenario variants (different poses, settings, outfits)

## IMPORTANT PATH INFO
- ComfyUI is at: /workspace/runpod-slim/ComfyUI/ (NOT /workspace/ComfyUI/)
- Python is python3 (NOT python)
- Web terminal paste: use right-click > Paste or Ctrl+Shift+V
- unzip not available via apt - use python3 zipfile module instead
- Previous: Deployed NEW pod with official ComfyUI template (yabbering_orange_mammal)
- Previous: Pod ID: h74hl96oos9brr
- ComfyUI is WORKING and accessible via web browser
- Installed custom nodes via ComfyUI Manager:
  - ✅ ComfyUI-InstantID (ID 43)
  - ✅ ComfyUI_IPAdapter_plus (ID 3, by Matteo)
- Both nodes verified as installed
- User stopping pod for the night

## What We're Working On NEXT SESSION
- Open JupyterLab terminal and download face models:
  - InstantID model (~1.7GB)
  - IP-Adapter FaceID model (~1.4GB)
  - InsightFace/antelopev2 face detection models
- Upload Midjourney hero image as reference face
- Build workflow and generate first test image
- Screenshots folder: `C:\Users\Vital\OneDrive\Pictures\Screenshots\`
- Screenshot workflow: Win+Print Screen → say "check screenshot" → Claude reads latest

## Files Created This Session
- `tools/runpod-comfyui-setup.sh` - One-click model + extension install for ComfyUI
- `tools/runpod-lora-training-setup.sh` - One-click LoRA training setup
- `tools/TECH-SETUP-CHECKLIST.md` - Complete checklist (tech vs manual work)
- `PROGRESS.md` - This file (auto-compact recovery)
- Updated `CLAUDE.md` with pre-compact dump rules
- Updated memory file with screenshot convention

## RunPod Setup Status (IN PROGRESS)
- [x] Signed up for RunPod
- [x] Deployed pod with official ComfyUI template (RTX 4090)
- [x] ComfyUI working and accessible via web UI
- [x] Installed ComfyUI-InstantID custom node
- [x] Installed ComfyUI_IPAdapter_plus custom node
- [ ] Download InstantID model (~1.7GB)
- [ ] Download IP-Adapter FaceID model (~1.4GB)
- [ ] Download InsightFace/antelopev2 face detection models
- [ ] Upload Midjourney hero images
- [ ] Build face consistency workflow
- [ ] Generate first test image
- [ ] Generate batch of 50+ consistent images

## Pod Details (CURRENT)
- Pod ID: h74hl96oos9brr
- Pod Name: yabbering_orange_mammal
- GPU: RTX 4090 (24GB VRAM)
- Cost: ~$0.60/hr
- Storage: 50GB persistent volume (/workspace)
- Status: STOPPED (resume anytime)

## Next Steps (Ordered)
1. **LoRA/Face Consistency Setup** - Install Python, ComfyUI, download models
2. **Text Stack for LoRA Training** - Get training data organized
3. **Image Pipeline** - Midjourney images exist, need face consistency workflow
4. **Platform Setup** - Fanvue account, Instagram @itsamiranoor, ManyChat
5. **Content Generation** - First batch of 50+ consistent images
6. **Launch** - Week 1 execution plan

## Key Decisions Made
- Persona: Amira Noor, 21, Egyptian/Brazilian mix
- Mean Framework: 8/10 who thinks she's a 6/10, accessible fantasy
- Platform: Fanvue (not OF - explicit AI creator support)
- Revenue target: $30K/month in 60 days
- Partners: Matt (MJ) + Vitaley's Cousin (VS)
- GitHub: vitaleysha-svg/pistachio (private)

## Blockers
- GPU VRAM: RTX 3070 Laptop = 8GB VRAM. LoRA/InstantID needs 12-24GB. Need cloud GPU (RunPod) or optimized local approach.

## Deferred Tasks (Do Later)
### 1. Life OS Interview Session
**Priority:** After tech stack setup
**What:** The Pistachio project doubles as a Life OS (Claude as Chief of Staff). The CLAUDE.md and context/ folder have templates for patterns, beliefs, visions, identity, goals — all currently blank/templated. Need to run a full interview session with Vitaley to fill these in. This makes every future session more personalized and contextual.
**Files to fill:** `context/goals.md`, `context/patterns.md`, identity statements in `CLAUDE.md`
**How:** Use AskUserQuestion interview-first approach, go deep on who he is, what drives him, behavioral patterns, energy drains, motivations. Save everything to the context files.

## Files That Matter
- `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` - The bible (1860 lines)
- `knowledge-base/face-consistency.md` - LoRA + ComfyUI workflow
- `knowledge-base/image-gen-workflow.md` - Midjourney prompts
- `knowledge-base/dm-psychology.md` - DM conversion sequence
- `PROJECT-PISTACHIO-PLAN.md` - Context recovery doc
- `autonomous-research/GOLD-pistachio.md` - Top 12 insights
