# Pistachio Progress Tracker
# AUTO-COMPACT RECOVERY FILE - Claude dumps state here before/during every session

## Last Updated: 2026-02-10 (Session 6 - Active)

## Current Phase: LoRA v2 TRAINED + PARAMETER SWEEP DONE - Awaiting User Review

## What Just Happened (Latest Session - 2026-02-10, Session 6)
- **LoRA v1 TESTED AND FAILED** - face didn't match training images well enough
  - Tested LoRA-only (InstantID off): face structure improved but not close enough
  - Tested LoRA 0.90 + InstantID 0.35: still not matching
  - Root cause: v1 was UNet-only (text encoder not trained), duplicates in dataset, identical captions
- **LoRA v2 TRAINED SUCCESSFULLY** - amiranoor_v2.safetensors (228.5 MB)
  - Key fixes: trains BOTH UNet + Text Encoder (TE at 1e-5)
  - Clean dataset: 36 unique images (deduped), varied captions (5 templates)
  - network_dim 16 (down from 32 to free VRAM for TE training)
  - 2000 steps, 6 epochs, final loss 0.116
  - Checkpoints saved: steps 500, 1000, 1500, 2000 (all copied to ComfyUI loras folder)
  - Script: retrain_lora_v2.py (on pod at /workspace/retrain_lora_v2.py)
  - Additional deps needed: `pip install voluptuous imagesize toml`
  - Must kill ComfyUI before training (VRAM conflict)
  - Used `nohup` to survive terminal disconnects
- **PARAMETER SWEEP COMPLETED** - 9 images auto-generated via ComfyUI API
  - Script: parameter_sweep.py (on pod at /workspace/parameter_sweep.py)
  - Tests: 3 checkpoints (step 1000, 1500, final) x 3 strengths (0.70, 0.80, 0.90)
  - Same seed (42424242) for fair comparison
  - Results in /workspace/sweep_results/ - USER NEEDS TO REVIEW THESE
- **fix_and_start.py CREATED AND WORKS** - one-click ComfyUI fix script
  - Fixes frontend, InstantID deps, IPAdapter deps, db permissions, restarts ComfyUI
  - All 5 steps pass clean
- **OpenAI Codex CLI installed** - `npm install -g @openai/codex` (Node v25.6.0)
- **Self-audit agent launched** - analyzing entire codebase for performance degradation
  - Report will be at pistachio/AUDIT-REPORT.md
- **All pod fixes still permanent** via startup.sh + post_start.sh hook

### Previous Session (2026-02-10, 1:05 AM - Session 5)
- **LoRA v1 TRAINING COMPLETE** - amiranoor_v1.safetensors (340.8 MB) saved and copied to ComfyUI
  - 72 images (30 originals + duplicates from re-runs), 720 with repeats
  - Resolution: 1024x1024, network_dim 32, network_alpha 16
  - Training UNet only (SDXL too big for text encoder + UNet on 24GB)
  - Gradient checkpointing enabled
  - Output: /workspace/lora_output/amiranoor_v1.safetensors
  - Script auto-copies to /workspace/runpod-slim/ComfyUI/models/loras/ when done
  - Trigger word: "amiranoor"
- **All pod fixes applied permanently:**
  - SQLite database permissions fix
  - ComfyUI frontend pip package updated (1.37.11 -> 1.38.13)
  - Custom node auto-install via startup.sh
  - Startup script at /workspace/startup.sh, hooked into post_start.sh
- **Dependency hell resolved for kohya sd-scripts:**
  - Pinned: transformers==4.38.2, diffusers==0.25.1, huggingface_hub==0.21.4
  - Additional deps needed: voluptuous, imagesize, toml
  - Final working v2 script: retrain_lora_v2.py (trains both UNet + TE)
- **Knowledge base comprehensively updated:**
  - face-consistency.md, runpod-automation-playbook.md (NEW), session-learnings.md
- **Clawra repo cloned locally** to pistachio/tools/clawra

### Previous Session (2026-02-09)
- **Pod restarted** - new proxy URL: 4c2w38t8qf52os-8188.proxy.runpod.net
- **Two pods existed after migration** - identified correct active pod, old migration pod can be terminated
- **Custom nodes were MISSING AGAIN** (red X boxes in workflow) - recurring problem on every pod restart
- **Created fix_nodes_permanent.ipynb** - ONE notebook that: (1) installs nodes now, (2) creates /workspace/startup.sh for auto-install on boot, (3) hooks into post_start.sh so it runs automatically, (4) restarts ComfyUI
- **fix_nodes_permanent.ipynb ran SUCCESSFULLY** on the pod - ComfyUI-Manager confirmed "All startup tasks completed"
- **ComfyUI currently loading** (splash screen showing) - waiting for it to finish booting with custom nodes
- **Clawra repo cloned locally** to C:\Users\Vital\pistachio\tools\clawra (full source code)
- **Clawra research completed** - saved to knowledge-base/clawra-ai-girlfriend-research.md
- **Video animation tools research completed** - saved to knowledge-base/video-animation-tools.md
- **Recommended video stack:** Wan2.2 (ComfyUI, RTX 4090, zero restrictions), LivePortrait + MuseTalk (lip sync), Kling AI Pro (quick SFW)
- **User preferences saved:** permanent fixes always, proactive thinking, code-first approach
- **DealerCenter ADF integration done** (side project, NOT saved to Pistachio - user explicitly said don't save)
  - Built GHL workflow to send survey leads to DealerCenter CRM in ADF XML format
  - Vendor: Space Auto Group, Provider: Derrick Core Marketing
  - Email: 19008401@leadsprod.dealercenter.net
  - Fixed survey query key mapping so custom field merge tags populate correctly

### Previous Session (2026-02-08, End of Day)
- **Generated all 30 LoRA training prompts** - 8 close-up face, 10 three-quarter body, 8 full body, 4 bonus variety angles
- **All prompts use MJ-safe body terms** (hourglass figure, slim waist, naturally curvy) to avoid moderator flags
- **User downloaded all 30 training images from Midjourney** - ready for LoRA prep
- **Researched Playwright automation for MJ** - confirmed NOT safe, permanent ban risk per MJ ToS. Do not attempt.
- **MJ Editor / Vary (Region) tested** - successfully removed glasses from olive dress photo using Smart Select mask. Minor face shift noted (regenerates nearby features)
- **User confirmed understanding of LoRA vs Inpainting distinction** - LoRA = identity/face consistency, Inpainting = sculpt body parts post-generation in ComfyUI

### Previous Session (earlier 2026-02-08)
- **Researched MJ banned words list** - Documented safe vs banned body description terms for Midjourney prompts
- **MJ-safe body terms confirmed:** hourglass figure, slim waist, naturally curvy, feminine curves, fit figure, athletic build, elegant silhouette
- **MJ banned terms documented:** cup sizes, bust/breasts/busty, glutes/booty/ass, thick thighs, voluptuous, provocative, lingerie, sexy, body measurements
- **Key insight:** `--oref` reference image at `--ow 250` carries body shape automatically. Text prompt only needs scene/outfit/pose - NOT body measurements
- **Learned MJ Editor / Vary (Region) workflow** for targeted image edits (mask area -> reprompt -> regenerate only masked region)
- **User testing Smart Select in MJ Editor** to remove glasses from favorite image
- **MJ-safe body description strategy:** Use "hourglass figure, slim waist, naturally curvy" instead of explicit terms. Save explicit body work for ComfyUI post-LoRA (zero filter)
- **Updated knowledge base files:** white-label-playbook.md, image-gen-workflow.md, session-learnings.md

### Previous Session (2026-02-07)
- **PHASE 2 CONFIRMED WORKING** - InstantID + IPAdapter FaceID combo produces consistent faces across scenarios
- **Face consistency validated** - Same person recognizable across outdoor/cap prompt AND cafe prompt (8-9/10 realism)
- **Additional models downloaded** - CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors (clip_vision), ip-adapter-faceid-plusv2_sdxl_lora.safetensors (loras)
- **Hat transfer issue identified** - InstantID bleeds accessories from reference. Fix: crop reference to face-only
- **Pipeline is production-ready** for face generation. Next: LoRA training for body consistency.

### Previous Session (earlier 2026-02-07)
- New Midjourney hero image created - Darker skin, fewer freckles, subtle green eyes. User approved.
- RunPod pod restarted - Models and workflows wiped (pod storage didn't persist properly)
- Multiple failed download attempts - JupyterLab terminal corrupts pasted URLs (line-break issues)
- Created download_models.ipynb - Jupyter notebook that bypasses terminal entirely
- Created download_models.py - Backup script at C:\Users\Vital\Downloads\
- Pistachio business ideas expanded - Added Channel #6 (Website Funnel) from Matt
- Session learnings updated - Added Pistachio fast-track mandate, business map, multiple corrections
- Bank statement analysis completed - ~$1,600/mo recurring charges identified across all accounts

## Previous Session Summary (2026-02-06)
- Diagnosed InstantID output quality issues - Output was 3/10 vs OG 10/10
- Identified 5 root causes: burn effect, wrong gen mode, prompt fighting, CFG too high, missing IP-Adapter FaceID
- Created 3-phase fix plan: Phase 1 (settings), Phase 2 (IP-Adapter FaceID), Phase 3 (img2img)
- Updated ALL knowledge base files with corrected settings

## What We're Doing RIGHT NOW
- **LoRA v2 TRAINED** - amiranoor_v2.safetensors (228.5 MB) at /workspace/runpod-slim/ComfyUI/models/loras/
- **Pod ID: tli3h17sfekhpn** (migrated from 4c2w38t8qf52os)
- **ComfyUI IS RUNNING** on port 8188
- **Trigger word:** "amiranoor"
- **v2 Training details:** 36 unique images, 2000 steps, 6 epochs, network_dim 16, network_alpha 8, UNet + Text Encoder
- **v2 Checkpoints saved:** steps 500, 1000, 1500, 2000 (all in ComfyUI loras folder)
- **Parameter sweep DONE** - 9 images in /workspace/sweep_results/ - USER NEEDS TO REVIEW
- **Scripts on pod:** fix_and_start.py, retrain_lora_v2.py, parameter_sweep.py, train_lora.py
- **Codex CLI installed** on local machine (npm global)
- **Self-audit running** - will save to pistachio/AUDIT-REPORT.md
- **Clawra repo cloned locally** at pistachio/tools/clawra
- **Two hero images exist:** original with hat (Pistachio741), new without hat (blue zipper jacket)
- **Working combo for later:** InstantID (weight 0.35) + LoRA v2 (0.75-0.90) - IPAdapter OFF initially
- **IMMEDIATE next steps:**
  1. User reviews 9 sweep result images and picks best checkpoint + strength combo
  2. Test winning combo with InstantID at low weight (0.30-0.40) for reinforcement
  3. If face matches: start batch generation
  4. If face still off: consider auto-captioning with BLIP-2 and retrain v3
  5. Video animation setup (Wan2.2 on ComfyUI)
  6. Inpainting body sculpting walkthrough

## What We're Working On NEXT (Completed Items)
1. ~~Finish generating 20 Midjourney prompts~~ DONE
2. ~~Cherry-pick images from generations~~ DONE
3. ~~Prep images for LoRA training~~ DONE
4. ~~Train LoRA v1 on RunPod RTX 4090~~ DONE (but quality insufficient)
5. ~~Retrain LoRA v2 with text encoder~~ DONE - amiranoor_v2.safetensors (228.5 MB)
6. ~~Parameter sweep (9 images, 3 checkpoints x 3 strengths)~~ DONE - awaiting user review
7. ~~Add Load LoRA node to ComfyUI workflow~~ DONE (connected between checkpoint and pipeline)
8. ~~Install Codex CLI~~ DONE
9. Pick best checkpoint + strength from sweep results - NEXT
10. Test with InstantID reinforcement at low weight
11. Use inpainting to sculpt body proportions as desired
12. Generate batch of 50+ consistent images (zero restrictions, zero cost per image)

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
1. **Start ComfyUI** on the pod (may need to run startup.sh or restart process)
2. **Add Load LoRA node** to ComfyUI workflow (connect between model loader and KSampler)
3. **Test LoRA with trigger word "amiranoor"** in positive prompt
4. **Compare checkpoint quality** - test steps 500, 1000, 1500 to find sweet spot
5. **Video animation setup** - Install Wan2.2 on ComfyUI for video generation
6. **Use inpainting to sculpt body proportions** as desired (user wants step-by-step walkthrough)
7. **Generate first batch of production images**
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
- [x] Download InstantID model (~1.7GB)
- [x] Download IP-Adapter FaceID model (~1.4GB)
- [x] Download InsightFace/antelopev2 face detection models
- [x] Upload Midjourney hero images
- [x] Build face consistency workflow
- [x] Generate first test image
- [ ] Generate batch of 50+ consistent images

## Pod Details (CURRENT)
- Pod ID: h74hl96oos9brr
- Pod Name: yabbering_orange_mammal
- GPU: RTX 4090 (24GB VRAM)
- Cost: ~$0.60/hr
- Storage: 50GB persistent volume (/workspace)
- Status: RUNNING (2026-02-10)
- Current pod proxy ID: tli3h17sfekhpn (migrated from 4c2w38t8qf52os on 2026-02-10)
- Previous proxy IDs: 4c2w38t8qf52os, fa6kxojaa6wt55
- OLD migration pod (h0r68bqsw0lepy) can be TERMINATED to save $0.01/hr idle cost
- Custom nodes now auto-install on boot via /workspace/startup.sh + /workspace/runpod-slim/post_start.sh hook
- startup.sh now also restarts ComfyUI automatically after applying all fixes
- fix_nodes_permanent.ipynb uploaded and ran successfully
- LoRA trained and deployed: /workspace/runpod-slim/ComfyUI/models/loras/amiranoor_v1.safetensors
- Training script: /workspace/train_lora.py (working, all deps pinned)

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

## Clawra / AI Girlfriend Chatbot Research (2026-02-09)
- **Completed deep research on Clawra** (github.com/SumeLabs/clawra) - open-source AI girlfriend selfie skill for OpenClaw
- **Full analysis saved to:** `knowledge-base/clawra-ai-girlfriend-research.md`
- **Key findings:**
  - Clawra is a skill/plugin for OpenClaw (open-source AI assistant platform), NOT a standalone app
  - Uses OpenClaw Gateway + Baileys for WhatsApp (reverse-engineered, free but risky)
  - Image generation via fal.ai Grok Imagine (reference image editing, not LoRA)
  - LLM backend: Claude Opus or GPT (configurable)
  - NSFW NOT possible with Grok Imagine (content filters) - dealbreaker for Fanvue
  - Our LoRA + ComfyUI pipeline is SUPERIOR for face/body consistency and has zero content restrictions
  - Architecture pattern is reusable: OpenClaw Gateway + custom skill calling our ComfyUI API
  - Phase 2 implementation plan drafted: 4 phases over ~4 weeks after LoRA training
  - Estimated production cost: $70-175/month for full AI chatbot + image gen stack

## Files That Matter
- `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` - The bible (1860 lines)
- `knowledge-base/face-consistency.md` - LoRA + ComfyUI workflow
- `knowledge-base/image-gen-workflow.md` - Midjourney prompts
- `knowledge-base/dm-psychology.md` - DM conversion sequence
- `knowledge-base/clawra-ai-girlfriend-research.md` - Clawra/OpenClaw research + Phase 2 plan
- `knowledge-base/video-animation-tools.md` - Wan2.2, LivePortrait, Kling AI research + recommended stack
- `tools/clawra/` - Cloned Clawra source code (OpenClaw AI girlfriend skill)
- `PROJECT-PISTACHIO-PLAN.md` - Context recovery doc
- `autonomous-research/GOLD-pistachio.md` - Top 12 insights
- `context/session-learnings.md` - User preferences, mistakes, learnings (updated with proactive thinking rule)

## Notebooks (in C:\Users\Vital\Downloads\, upload to JupyterLab on pod)
- `fix_nodes_permanent.ipynb` - PERMANENT fix for custom nodes (installs + startup script + post_start hook)
- `download_models.ipynb` - Downloads all 5 core models (checkpoint, controlnet, insightface, ipadapter, instantid)
- `download_clipvision.ipynb` - Downloads CLIP vision + FaceID LoRA models
- `install_nodes.ipynb` - Basic node installer (superseded by fix_nodes_permanent.ipynb)
