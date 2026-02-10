# Codex Implementation Plan - Pistachio AI Influencer Project

## Context

This is an AI influencer project ("Amira Noor") that generates consistent images of a fictional persona using:
- **Midjourney** for hero/training images (these are the "OG" quality standard - 10/10)
- **ComfyUI** on RunPod (RTX 4090) for batch generation with face consistency
- **LoRA** (Low-Rank Adaptation) trained on 36 Midjourney images for identity
- **InstantID + IPAdapter FaceID** for face structure reinforcement

**The Problem:** The ComfyUI pipeline produces images that are 3-4/10 quality compared to the OG Midjourney images (10/10). Face doesn't match, skin looks fake/AI, overall photographic quality is significantly worse. Two LoRA versions have been trained:
- v1: UNet-only training, failed (face didn't match)
- v2: UNet + Text Encoder training, better but still not matching OG quality

**Your job:** Audit everything, implement fixes, commit to GitHub. Do NOT push - just commit locally.

---

## Repository Structure

```
C:\Users\Vital\pistachio\
├── CLAUDE.md                    # Claude Code config (480 lines - too bloated)
├── PROGRESS.md                  # State tracker
├── AUDIT-REPORT.md              # Self-audit findings
├── CODEX-PLAN.md                # This file
├── PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md  # 1869 lines, stale
├── PROJECT-PISTACHIO-PLAN.md    # Context recovery doc
├── context/
│   ├── goals.md                 # BLANK TEMPLATES (107 lines of [FILL IN])
│   ├── patterns.md              # BLANK TEMPLATES (216 lines of [FILL IN])
│   ├── session-learnings.md     # 367 lines of learnings + mistakes
│   └── AI-CODING-WORKFLOW.md    # Ralph workflow (was @imported, now skill)
├── knowledge-base/
│   ├── face-consistency.md      # LoRA + ComfyUI workflow docs
│   ├── image-gen-workflow.md    # Midjourney prompts
│   ├── runpod-automation-playbook.md  # Pod setup/automation
│   ├── white-label-playbook.md  # Production workflow
│   ├── video-animation-tools.md # Wan2.2, LivePortrait research
│   ├── clawra-ai-girlfriend-research.md
│   └── prompt-iterations.md     # Prompt iteration log
├── .claude/skills/
│   └── ralph-workflow/SKILL.md  # Ralph dev workflow (on-demand)
├── tools/
│   └── clawra/                  # Cloned AI girlfriend repo
└── autonomous-research/
    └── GOLD-pistachio.md        # Top 12 insights
```

### Files on RunPod Pod (NOT in this repo - reference only)
```
/workspace/
├── training_images/             # 36 Midjourney source images
├── lora_dataset_v2/             # Processed training data (1024x1024 + captions)
├── lora_output_v2/              # Training output + checkpoints
├── sweep_results/               # 9 parameter sweep test images
├── sd-scripts/                  # kohya-ss/sd-scripts (training framework)
├── runpod-slim/ComfyUI/         # ComfyUI installation
│   └── models/loras/            # LoRA files deployed here
├── fix_and_start.py             # One-click ComfyUI fix script
├── retrain_lora_v2.py           # LoRA v2 training script
├── parameter_sweep.py           # Auto-generates test images via API
├── train_lora.py                # Original v1 training script
└── startup.sh                   # Auto-runs on pod boot
```

### Files in Downloads (uploaded to pod manually)
```
C:\Users\Vital\Downloads\
├── train_lora.py                # v1 training script
├── retrain_lora_v2.py           # v2 training script (CURRENT)
├── fix_and_start.py             # ComfyUI fix script
├── parameter_sweep.py           # Parameter sweep via API
├── lora_training.ipynb          # Superseded by .py scripts
└── fix_nodes_permanent.ipynb    # Custom node installer
```

---

## Task 1: Fix CLAUDE.md (Context Optimization)

### Problem
CLAUDE.md is 480 lines. Combined with session-learnings.md (367), PROGRESS.md (240), and blank template files (goals.md 107, patterns.md 216), Claude loads ~1,500 lines of context before doing anything. This crowds out working memory for actual tasks.

### What to Do

1. **Rewrite CLAUDE.md to ~100-120 lines max.** Keep ONLY:
   - Identity (2-3 lines)
   - Core principles (top 5 most impactful, not 12)
   - Session start protocol (simplified - 5 lines)
   - Auto-save protocol (5 lines)
   - Quality standards (3 lines)
   - What NOT to do (5 lines)
   - Learned Mistakes (move to a skill, keep only a 5-line "check mistakes skill before acting" reminder)

2. **Create these skills in `.claude/skills/`:**
   - `pistachio-workflow/SKILL.md` - ComfyUI workflow, LoRA training, RunPod management, all technical details
   - `life-os-frameworks/SKILL.md` - Elon 5-step, Peter Thiel one-thing, bottleneck clearing, CoS task intake
   - `learned-mistakes/SKILL.md` - All 8+ learned mistakes with triggers
   - `interview-protocol/SKILL.md` - The interview-first approach, AskUserQuestion patterns

3. **Delete or archive blank template files:**
   - `context/goals.md` - Replace with a 5-line file that says "NOT YET FILLED - Run Life OS interview to populate"
   - `context/patterns.md` - Same treatment
   - Don't delete, just shrink to stubs so they don't waste context

4. **Consolidate session-learnings.md:**
   - Create a 30-line CRITICAL RULES section at the top (the stuff that matters most)
   - Move historical detail to an archive section that's only loaded on-demand

5. **Archive PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md:**
   - Rename to `archive/operations-manual-v1.md`
   - It's 1,869 lines, increasingly stale, superseded by knowledge-base files

### Verification
After changes, count total lines loaded on session start. Target: under 200 lines (currently ~1,500).

---

## Task 2: Fix Image Quality Pipeline

### Problem
LoRA v2 was trained with text encoder support and produces better face structure, but:
- Face still doesn't match OG Midjourney images closely enough
- Skin looks fake/airbrushed (not enough texture, pores, imperfections)
- Overall photographic quality is significantly below the Midjourney source images
- Parameter sweep of 9 images (3 checkpoints x 3 strengths) all showed same problems

### Root Cause Analysis
1. **Generic captions** - All 36 images have one of 5 rotating templates like "amiranoor, a young woman, close up portrait, photorealistic." Professional LoRA trainers use per-image auto-captioning (BLIP-2 or Florence-2) that describes each image in detail (pose, lighting, expression, clothing, background). This helps the model isolate "amiranoor" = face identity, separate from all other attributes.

2. **No regularization images** - Standard technique: include 200+ generic "woman" images alongside training images. This teaches the model the DIFFERENCE between "amiranoor" and "any woman." Without it, the trigger word's effect is diluted.

3. **Training images are AI-generated** - Midjourney images have a specific "look" (slight color grading, particular lighting style). The LoRA may be learning MJ's artistic style rather than actual facial features. This creates a style mismatch when generating with RealVisXL v5.

4. **Checkpoint/model mismatch** - RealVisXL v5 may not be the best base for this use case. Other options: JuggernautXL v9, epiCRealism XL.

### What to Do

1. **Create an auto-captioning script** (`tools/auto_caption.py`):
   - Use BLIP-2 or Florence-2 to generate detailed per-image captions
   - Prepend trigger word "amiranoor" to each caption
   - Example output: "amiranoor, a young woman with dark hair in a messy bun, looking over her shoulder, wearing an olive green dress, golden hour outdoor lighting, garden background with flowers"
   - Save as .txt files alongside images
   - This script should be uploadable to the pod and runnable

2. **Create a regularization image download script** (`tools/download_reg_images.py`):
   - Download 200 diverse "woman" photos from a public dataset (or generate them with the base model)
   - Save to `/workspace/reg_images/`
   - These get passed to training with `--reg_data_dir`

3. **Update retrain_lora_v2.py -> create retrain_lora_v3.py:**
   - Add `--reg_data_dir /workspace/reg_images` for regularization
   - Increase steps to 2500 (more data with reg images)
   - Try Prodigy optimizer instead of AdamW8bit (auto-tunes learning rate)
   - Add xformers for memory efficiency: `--xformers`
   - Consider network_dim 32 (more capacity) if VRAM allows with xformers
   - Include all dependency installs (transformers==4.38.2, diffusers==0.25.1, huggingface_hub==0.21.4, voluptuous, imagesize, toml)

4. **Create a comprehensive parameter sweep v2** (`tools/parameter_sweep_v2.py`):
   - Test LoRA-only AND LoRA+InstantID combos
   - Test multiple CFG values (3.5, 4.0, 4.5)
   - Test different samplers (dpmpp_2m, euler_a, dpmpp_sde)
   - Generate a labeled grid/montage image for easy comparison
   - Include face similarity scoring if possible (using insightface embedding comparison)

5. **Create a workflow backup script** (`tools/backup_workflow.py`):
   - Export current ComfyUI workflow as JSON via API
   - Save to pistachio repo under `workflows/`
   - Version control the workflow

### Verification
- Auto-captioned LoRA should produce faces that are recognizably the same person as training images
- Skin should show natural texture (pores, slight imperfections)
- Overall quality should be 7/10 or higher (user judgment)

---

## Task 3: Build Missing Automation

### Problem
Every pod restart requires manual intervention. Dependency issues recur. No health checks. Workflow files not backed up.

### What to Do

1. **Create `tools/requirements-pod.txt`:**
   ```
   transformers==4.38.2
   diffusers==0.25.1
   huggingface_hub==0.21.4
   accelerate
   safetensors
   bitsandbytes
   voluptuous
   imagesize
   toml
   insightface
   onnxruntime-gpu
   ```
   This gets installed on every pod boot via startup.sh.

2. **Create `tools/pod_health_check.py`:**
   - Check ComfyUI is running on 8188
   - Check all custom nodes loaded (no red X boxes)
   - Check all models present (checkpoint, LoRA, InstantID, etc.)
   - Check VRAM availability
   - Check disk space
   - Print clear PASS/FAIL status
   - Uploadable to pod, runnable as single command

3. **Create `tools/startup_v2.sh`:**
   - Install pinned requirements from requirements-pod.txt
   - Fix database permissions
   - Ensure custom nodes installed
   - Run health check
   - Start ComfyUI
   - One file replaces all manual setup

4. **Create `tools/backup_and_download.py`:**
   - Backup ComfyUI workflow JSON
   - Backup LoRA files list (names + sizes)
   - Backup custom node list
   - Save all to a zip that can be downloaded
   - Useful for pod migration or disaster recovery

5. **Create `tools/generate_batch.py`:**
   - Takes a list of prompts (from a .txt file or inline)
   - Generates N images per prompt via ComfyUI API
   - Saves with labeled filenames
   - Supports different poses, outfits, settings
   - This is the production image generation tool

### Verification
- Pod restart → run startup_v2.sh → health check passes → ComfyUI ready
- Zero manual commands needed between pod boot and first image generation

---

## Task 4: Review and Learn

After implementing Tasks 1-3:

1. **Commit all changes** (do NOT push):
   ```
   git add -A
   git commit -m "Codex audit: CLAUDE.md optimization, image pipeline fixes, automation scripts"
   ```

2. **Write a summary** of what was changed and why in `CODEX-CHANGES.md`

3. **Document any insights** about the codebase, workflow, or approach that weren't in the audit report

---

## Key Constraints

- **Do NOT push to GitHub** - only commit locally
- **Do NOT modify files on the RunPod pod** - only create scripts locally that can be uploaded
- **Do NOT delete any files** without creating backups first
- **All Python scripts must be self-contained** - include all imports and dependency installs
- **Pin all dependency versions** - no unpinned packages
- **CLAUDE.md must stay under 120 lines** after optimization
- **Test nothing** - you don't have access to the pod or ComfyUI. Create the scripts, document how to use them.

---

## Success Criteria

1. CLAUDE.md is under 120 lines with all knowledge moved to skills
2. Auto-captioning script exists and is ready to upload to pod
3. LoRA v3 training script exists with regularization, auto-captions, and better optimizer
4. Pod startup is fully automated (single script, zero manual commands)
5. All changes committed locally with clear commit message
6. CODEX-CHANGES.md documents everything that was done
