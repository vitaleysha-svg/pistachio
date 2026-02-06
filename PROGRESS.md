# Pistachio Progress Tracker
# AUTO-COMPACT RECOVERY FILE - Claude dumps state here before/during every session

## Last Updated: 2026-02-06 (night session)

## Current Phase: PRE-LAUNCH SETUP - Prompt System Built

## What Just Happened (Latest Session)
- Built prompt reverse-engineering system (knowledge-base/prompt-reverse-engineering.md)
- Created iteration log (knowledge-base/prompt-iterations.md)
- Created prd.json for Ralph Loop tracking
- Persona changed: Egyptian/Brazilian -> Japanese/Brazilian mix
- Moved AI-CODING-WORKFLOW.md from @import to on-demand skill (.claude/skills/ralph-workflow/)
- Set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 in settings.json
- Fixed GitHub push rule - repo IS private, pushing is part of workflow
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
