# Pistachio Progress Tracker
# AUTO-COMPACT RECOVERY FILE - Claude dumps state here before/during every session

## Last Updated: 2026-02-07 (current session)

## Current Phase: MODELS NEED RE-DOWNLOAD → Then Apply Phase 1 Fix

## What Just Happened (Latest Session - 2026-02-07)
- **New Midjourney hero image created** - Darker skin, fewer freckles, subtle green eyes. User approved.
- **RunPod pod restarted** - Models and workflows wiped (pod storage didn't persist properly)
- **Multiple failed download attempts** - JupyterLab terminal corrupts pasted URLs (line-break issues)
- **Created download_models.ipynb** - Jupyter notebook that bypasses terminal entirely. User uploads to JupyterLab, clicks Run All, models download automatically.
- **Created download_models.py** - Backup script at C:\Users\Vital\Downloads\
- **Pistachio business ideas expanded** - Added Channel #6 (Website Funnel) from Matt
- **Session learnings updated** - Added Pistachio fast-track mandate, business map, multiple corrections
- **Bank statement analysis completed** - ~$1,600/mo recurring charges identified across all accounts

## Previous Session Summary (2026-02-06)
- Diagnosed InstantID output quality issues - Output was 3/10 vs OG 10/10
- Identified 5 root causes: burn effect, wrong gen mode, prompt fighting, CFG too high, missing IP-Adapter FaceID
- Created 3-phase fix plan: Phase 1 (settings), Phase 2 (IP-Adapter FaceID), Phase 3 (img2img)
- Updated ALL knowledge base files with corrected settings

## What We're Doing RIGHT NOW
- **STEP 1: Download models to RunPod** - Use download_models.ipynb (upload to JupyterLab, click Run All)
- **STEP 2: Rebuild workflow** in ComfyUI (9 nodes, save JSON to /workspace/)
- **STEP 3: Apply Phase 1 fix settings** and run generation:

### Phase 1 Settings to Apply in ComfyUI:
| Setting | Change To |
|---------|-----------|
| InstantID weight | **0.75** |
| InstantID end_at | **0.90** |
| KSampler CFG | **4.0** |
| KSampler steps | **35** |
| KSampler sampler | **dpmpp_2m** (NOT euler) |
| KSampler scheduler | **karras** |
| Empty Latent Image | **1016x1280** |
| Positive prompt | See prompt-iterations.md Iteration #2 |
| Negative prompt | See prompt-iterations.md Iteration #2 (weighted for SDXL) |

**WARNING: Do NOT use euler + karras combo = blurry. DPM++ 2M + Karras is correct.**

### If Phase 1 Score < 7/10, Phase 2:
- Add IPAdapter Unified Loader FaceID node ("PLUS FACE portraits")
- Add IPAdapter Apply node, connect to pipeline
- IP-Adapter weight: 0.60-0.70

### If Still < 7/10, Phase 3:
- Remove Empty Latent Image
- Add Load Image (OG reference) → VAE Encode → KSampler latent_image
- Set denoise to 0.40

## What We're Working On NEXT
1. Start RunPod pod
2. Apply Phase 1 settings in ComfyUI
3. Run generation, screenshot output
4. Compare to OG side by side, user scores it
5. If < 7/10, apply Phase 2 (IP-Adapter FaceID)
6. If still < 7/10, apply Phase 3 (img2img)
7. Log results in prompt-iterations.md
8. Once face is 7/10+, generate scenario variants

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
- Status: RUNNING (proxy URL: fa6kxojaa6wt55)
- ComfyUI URL: https://fa6kxojaa6wt55-8188.proxy.runpod.net
- JupyterLab URL: https://fa6kxojaa6wt55-8888.proxy.runpod.net
- NOTE: Models were wiped on restart. Need to re-download via download_models.ipynb

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
