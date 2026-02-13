# Pistachio Progress Tracker

## Last Updated: 2026-02-12
## Current Phase: Phase 15 — NEW DIRECTION: DiffusionPipe + Wan 2.1 LoRA Training Pipeline
## Status: New approach adopted. Created 6 open-source scripts (replacing Discord-gated ones). SSH connection to RunPod pod FAILED all 3 methods. Need to resolve connection before executing Phase 2+. Knowledge base created from 2 YouTube video transcriptions.

## PHASE 15 — NEW DIRECTION SUMMARY
### What Changed
- User ingested 2 YouTube tutorial videos and pivoted approach
- **OLD approach:** SDXL + InstantID + FaceDetailer + Kohya LoRA training
- **NEW approach:** Wan 2.1 T2V-14B + DiffusionPipe LoRA training + JoyCaption + wandb evaluation
- Key advantage: DiffusionPipe provides wandb eval graphs → pick mathematically best checkpoint (no guesswork)
- All tools are open-source, no Discord paywall needed

### New Scripts Created (C:\Users\Vital\pistachio\scripts\)
1. **install_joycaption.sh** — Clones MNeMoNiCuZ/joy-caption-batch, creates venv, installs deps
2. **install_diffusion_pipe.sh** — Clones tdrussell/diffusion-pipe with submodules, creates env
3. **download_wan_models.sh** — Downloads 4 files (~36GB) from HuggingFace (Apache 2.0, no auth)
4. **training_config.toml** — DiffusionPipe config optimized for RTX/24-48GB GPUs
5. **dataset_config.toml** — Training data config (80% split, /workspace/dataset/train/)
6. **eval_dataset_config.toml** — Eval data config (20% split, /workspace/dataset/eval/)

### New Knowledge Base Created
- **C:\Users\Vital\pistachio\KNOWLEDGE_BASE.md** (~420 lines)
- Covers: ComfyUI fundamentals, LoRA training pipeline, DiffusionPipe, JoyCaption, Wan 2.1, wandb, GPU configs, error resolution

### SSH Connection Issue (BLOCKING)
- Pod: yabbering_orange_mammal_migration (ID: on91uybqyagtnk)
- All 3 methods failed:
  1. Exposed TCP (root@213.173.99.10:11925) — hung/timed out after adding host key
  2. RunPod proxy (on91uybqyagtnk-64410dec@ssh.runpod.io) — "Your SSH client doesn't support PTY" even with -T
  3. JupyterLab API (https://on91uybqyagtnk-8888.proxy.runpod.net/) — 403 Forbidden
- **Solutions to try:** runpodctl CLI, Web Terminal in RunPod, get JupyterLab token, manual file upload via browser

### Execution Plan (Once Connected)
- Phase 1 (User does): Collect 20+ images, choose trigger word
- Phase 2 (Claude does): Upload scripts, run install_joycaption.sh
- Phase 3 (Claude does): Run download_wan_models.sh (~36GB download)
- Phase 4 (Claude does): Run install_diffusion_pipe.sh
- Phase 5 (Claude does): Caption images with JoyCaption, split 80/20 train/eval
- Phase 6 (Claude does): Configure TOML files, set wandb API key, launch training
- Phase 7 (Claude does): Monitor wandb, pick best checkpoint, test in ComfyUI

## RECOVERY INFO (if session resets)
- SSH: `ssh -i ~/.ssh/id_ed25519 -p 17373 root@213.173.99.10`
- Pod ID: on91uybqyagtnk (migrated from tli3h17sfekhpn)
- SSH key was re-added via web terminal after migration
- After migration run: `bash /workspace/startup_v2.sh`
- SSH public key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ56MCk0GjScua9CY5VPbWWvuJ95Gj7JKxEc4r+DLkUe vitaleysha@gmail.com`
- LoRA v3 training: COMPLETED (2500 steps, 63 min, loss 0.0624)
- LoRA v4 training: COMPLETED (2500 steps, 46 min, loss 0.0616)
- All v3 + v4 LoRA checkpoints in ComfyUI loras folder
- insightface + onnxruntime-gpu installed on pod
- InstantID models installed: ip-adapter.bin + instantid-controlnet.safetensors
- ComfyUI-Impact-Pack + Impact-Subpack installed (FaceDetailer + UltralyticsDetectorProvider)
- face_yolov8m.pt + hand_yolov8s.pt in models/ultralytics/bbox/
- ultralytics pip package installed

## WHAT TO DO WHEN RESUMING
1. Check pod status — if SSH refused, pod likely migrated. Get new SSH command from RunPod dashboard.
2. Run `bash /workspace/startup_v2.sh` to restore environment.
3. Verify ComfyUI is running: `curl -s http://127.0.0.1:8188/object_info | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d), "nodes loaded")'`
4. Continue with NEXT STEPS below.

## V2 CONFIG (InstantIDAdvanced + FaceDetailer + LoRA v4)
```python
# V2 Production: close-ups avg 0.60, overall avg 0.46 (multi-ref scoring)
Checkpoint = "realvisxl_v5.safetensors"     # REPLACE with epiCRealism XL
LoRA_identity = "amiranoor_v4-step00001000.safetensors" at strength 0.5
LoRA_realism = None                          # ADD PhotorealTouch or Skin Realism
Node = ApplyInstantIDAdvanced                # V2: separate ip_weight and cn_strength
ip_weight = 0.8                              # Identity preservation (HIGH)
cn_strength = 0.35                           # Pose control (LOW for variety)
InstantID_model = "ip-adapter.bin"
ControlNet = "instantid-controlnet.safetensors"
FaceAnalysis = InstantIDFaceAnalysis (NOT IPAdapterInsightFaceLoader)
CFG = 3.5
Sampler = "dpmpp_2m" + "karras"
Steps = 28
Resolution = 1024x1024
FaceDetailer = ON (denoise 0.42, bbox_crop_factor 1.3, face_yolov8m.pt)
Reference_image = img_002.png
```

## USER FEEDBACK (Critical — What to Fix)
1. **"Still looks AI-ish"** — Skin too smooth, missing real-photo imperfections
   - FaceDetailer helped but not enough
   - Need: photorealism LoRA (PhotorealTouch/Skin Realism) + better checkpoint (epiCRealism XL)
2. **"All same position"** — FIXED in V2 with cn_strength=0.35
   - Close-ups show great variety (front, 3/4, profile, looking down)
   - Wider shots lost identity → need cn_strength=0.55 for half/full body
3. **"Not consistent"** — Face varies between shots
   - Close-ups are consistent (avg 0.60)
   - Wider shots lose identity (avg 0.33) due to low cn_strength

## CRITICAL FIXES (Don't Repeat)
1. ApplyInstantID expects `insightface` input of type `FACEANALYSIS` from `InstantIDFaceAnalysis` node.
   IPAdapterInsightFaceLoader outputs type `INSIGHTFACE` — WRONG TYPE, causes HTTP 400.
2. Face detection on close-up images: must add 200px padding with `cv2.copyMakeBorder()` before `app.get()`.
   v4 LoRA generates tighter crops that fill the frame — InsightFace can't detect without padding.
3. Training script fixes (all baked into retrain_lora_v4.py):
   - Removed bitsandbytes dependency (not needed for Prodigy optimizer)
   - Changed `--xformers` to `--sdpa` (built into PyTorch 2.0+)
   - Removed `--persistent_data_loader_workers` (incompatible with num_workers=0)
   - Set learning rate default to 1.0 for Prodigy (was 1e-4)
   - Pinned huggingface_hub==0.21.4, transformers==4.38.2
4. `pkill python3` kills SSH — use `bash -c 'nohup bash -c "sleep 2; pkill ..." &'` pattern.
5. ComfyUI needs `python3` not `python` on RunPod.
6. Impact Pack Subpack must be cloned separately: `git clone https://github.com/ltdrdata/ComfyUI-Impact-Subpack.git` into custom_nodes/

## V2 Results Summary
| Category | Avg Sim | Best | Count Passed | Notes |
|----------|---------|------|--------------|-------|
| Close-up portraits | 0.60 | 0.71 | 11/12 | Great variety, good identity |
| Medium shots | 0.45 | 0.63 | 4/12 | Mixed — some lost identity |
| Half/full body | 0.33 | 0.45 | 0/12 | cn_strength too low |
| **Overall** | **0.46** | **0.71** | **15/36** | Pose variety achieved |

## LoRA v4 Checkpoint Comparison
| Checkpoint | Avg Sim | Best | Worst |
|-----------|---------|------|-------|
| Step 500  | 0.633   | 0.727 | 0.571 |
| **Step 1000** | **0.652** | **0.709** | **0.584** |
| Step 1500 | 0.653   | 0.717 | 0.592 |
| Step 2000 | 0.655   | 0.710 | 0.581 |

## NEXT STEPS (Priority Order)
1. **Download photorealism LoRA** to pod:
   - PhotorealTouch (CivitAI model 1464286) — strength 0.5-0.7
   - OR Skin Realism (CivitAI model 248951) — strength 0.5
   - Stack with identity LoRA for double LoRA loading
2. **Download epiCRealism XL checkpoint** (CivitAI model 277058) — ~6.5GB
   - Best rated photorealistic SDXL checkpoint in 2026
   - Replace realvisxl_v5.safetensors
3. **Graduated cn_strength by shot type**:
   - Close-ups: cn_strength=0.35 (current, works great)
   - Medium shots: cn_strength=0.50
   - Half/full body: cn_strength=0.65
4. **Run V3 production batch** with photorealism LoRA + epiCRealism XL + graduated cn_strength
5. **User review** — show side-by-side comparison
6. Target: photos indistinguishable from real at close-up, near-real at wider shots

## Photorealism Research (from CivitAI/web)
### Top Photorealism LoRAs for SDXL:
1. **PhotorealTouch** (model 1464286) — pores, vellus hair, imperfections, strength 0.5-0.8
2. **Skin Realism** (model 248951) — acne, blemishes, no-makeup look, strength 0.5
3. **Real Skin Slider** (model 1486921) — strength 2-3 (slider type)
4. **Realistic Skin Texture Style** (model 580857) — strength 0.8, trigger "detailed skin pore style"
5. **Realism LoRA by Stable Yogi** (model 1100721) — designed for realistic checkpoints

### Top Checkpoints (alternatives to RealVisXL):
1. **epiCRealism XL** (model 277058) — #1 rated, 6.46GB, best skin/lighting
2. **Juggernaut XL** (model 133005) — most versatile, 18M+ downloads
3. **Halcyon SDXL** (model 299933) — strong photorealism
4. **CyberRealistic XL** (model 312530) — consistent results

### Anti-AI Techniques:
- Negative prompt: `(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (cgi:1.2)`
- Positive prompt keywords: `visible pores, natural skin texture, subtle freckles, skin imperfections`
- LoRA stacking: identity LoRA + photorealism LoRA
- FaceDetailer post-processing with denoise 0.40-0.45

## Session History

### Phase 11: LoRA v4 Training (COMPLETED)
- User uploaded 48 MJ reference images (10 new + 38 originals)
- Ran face analysis: 48/49 faces detected, 46 passed consistency threshold
- Created training dataset: 47 images + captions in /workspace/lora_dataset_v4/10_amiranoor/
- Fixed 5 PyTorch/dependency compatibility issues in training script
- Training: 2500 steps, 46 min, final loss 0.0616 (better than v3's 0.0624)
- 6 checkpoints saved (500, 1000, 1500, 2000, 2500, final)

### Phase 12: v4 Production Batch (COMPLETED)
- Updated production script: v4 LoRA, v4 references, padding fix for face detection
- Tested all checkpoints (500, 1000, 1500, 2000) — all similar, step 1000 chosen
- 36/36 generated, 36/36 passed quality gate, 100% pass rate
- v4 avg: 0.652 (multi-ref scoring) vs v3 avg: 0.696
- v4 uses stricter scoring (5-ref average vs single-ref)
- All 36 v4 images downloaded to `sweep_results/production_v4/`

### Phase 13: V2 Pipeline — InstantIDAdvanced + FaceDetailer (COMPLETED)
- User feedback: still AI-ish, same positions, inconsistent
- Installed Impact Pack Subpack (UltralyticsDetectorProvider)
- Created `instantid_production_v2.py` with:
  - ApplyInstantIDAdvanced (ip_weight=0.8, cn_strength=0.35)
  - FaceDetailer (denoise=0.42, bbox_crop_factor=1.3, face_yolov8m.pt)
  - 12 dramatically varied prompts with realism keywords
- Generated 36 images, 15 passed quality gate (42%)
- Close-ups: excellent variety + realism, avg 0.60
- Wider shots: lost identity due to low cn_strength
- Downloaded all results to `sweep_results/production_v2/`
- User: "realism is getting better, still not looking anywhere near our locked image"

### Phase 14: Deep Research + V3 Prep (IN PROGRESS)
- Researched top photorealism LoRAs and checkpoints
- Pod migrated (new SSH: port 17373, IP 213.173.99.10)
- Reconnected, verified all scripts/LoRAs intact on /workspace
- **Installed AGAIN (lost in migration)**: `insightface`, `onnxruntime-gpu`, `segment-anything` — DONE (2026-02-11)
- **Downloaded**: epiCRealism XL checkpoint (6.5GB) at models/checkpoints/epicrealismxl.safetensors DONE
- **Deleted**: Wrong skin realism file (was 6.5GB checkpoint, not LoRA)
- **ComfyUI**: NOT RUNNING — killed old process, port 8188 freed, needs restart after deps installed
- **Deep research launched** (5 agents): PuLID vs InstantID, FLUX models, AI influencer best practices, correct skin realism LoRA URLs, image_kps pose decoupling
- **PuLID research COMPLETED** — saved to research/deep_research_pulid.md
  - KEY FINDING: PuLID has better face similarity (0.733 vs 0.725) but LOCKS POSE (bad for us)
  - EcomID (Alibaba hybrid of PuLID+InstantID) is the best option — combines identity fidelity with pose control
  - Recommendation: Keep InstantID for now, try EcomID as upgrade
- **FLUX research COMPLETED** — saved to research/deep_research_flux.md
  - KEY: FLUX fundamentally better than SDXL (12B params, 16-channel VAE, better anatomy/skin)
  - Runs on 4090 in FP8 (~14-17s/image), Kontext+PuLID = 94-96% consistency
  - DECISION: V3 stays SDXL (exhaust improvements), V4 migrates to FLUX if needed
- **AI influencer techniques COMPLETED** — saved to research/deep_research_ai_influencer.md
  - KEY FINDING: FaceDetailer with LoRA as second pass = 97% identity (we don't do this yet!)
  - Professional stack: LoRA + FaceDetailer(with LoRA) + ControlNet + IP-Adapter FaceID
  - Film grain is single most effective anti-AI-detection technique
  - CFG should be 5-6 not 3.5, add camera/lens prompts, better negative prompts
- **image_kps research COMPLETED** — saved to research/deep_research_image_kps.md
  - image_kps decouples head angle from identity (zero-effort pose variety)
  - For body pose: stack DWPose ControlNet via ApplyInstantIDControlNet node
  - Three-layer: InstantID (identity) + image_kps (head) + DWPose (body)
- **Skin realism LoRA research** — was still running at pause time, may have completed
- User provided major feedback requesting: analysis of why images still don't match, what research found vs implemented, extensive new research, completion today
- Analysis of 5 core downfalls already provided to user:
  1. Single checkpoint (RealVisXL) not top-tier for photorealism
  2. No photorealism LoRA stacking
  3. cn_strength too uniform (0.35 for all shots)
  4. Only one reference image fed to InstantID
  5. No post-processing (film grain, color grading)
- 8 techniques identified but NOT YET IMPLEMENTED:
  1. PuLID (alternative to InstantID)
  2. image_kps pose decoupling
  3. FLUX architecture
  4. Rotating reference images
  5. euler_ancestral sampler
  6. Film grain / chromatic aberration
  7. Higher FaceDetailer denoise
  8. IP-Adapter face-only mode

## WHAT TO DO WHEN RESUMING (Phase 14)
1. SSH: `ssh -i ~/.ssh/id_ed25519 -p 17373 root@213.173.99.10`
   - If refused, pod migrated again — get new SSH from RunPod dashboard
   - After migration: add SSH key, run `bash /workspace/startup_v2.sh`, reinstall insightface+segment_anything+onnxruntime-gpu
2. **RE-RUN only 1 research agent** whose results were lost:
   - Skin realism LoRA URLs (agent ac1e3d9) — re-run to get correct download URLs
   - ALL OTHER RESEARCH SAVED LOCALLY:
     - research/deep_research_pulid.md — EcomID hybrid is best, keep InstantID for pose variety
     - research/deep_research_flux.md — FLUX better but stay SDXL for V3, FLUX for V4
     - research/deep_research_ai_influencer.md — FaceDetailer+LoRA second pass is our biggest gap
     - research/deep_research_image_kps.md — image_kps decouples head angle from identity
3. Start ComfyUI: `cd /workspace/runpod-slim/ComfyUI && nohup python3 main.py --listen 0.0.0.0 --port 8188 > /tmp/comfyui.log 2>&1 &`
4. Verify nodes loaded: `sleep 20 && curl -s http://127.0.0.1:8188/object_info | python3 -c 'import sys,json; d=json.load(sys.stdin); print("FaceDetailer:", "YES" if "FaceDetailer" in d else "NO"); print("Ultralytics:", "YES" if "UltralyticsDetectorProvider" in d else "NO"); print("InstantIDAdv:", "YES" if "ApplyInstantIDAdvanced" in d else "NO")'`
5. Based on all research findings, make decisions:
   - Keep InstantID + improvements, OR try EcomID (hybrid PuLID+InstantID)
   - Which skin realism LoRA to download
   - Whether to explore FLUX (may need different identity approach)
6. Find and download correct skin realism LoRA (small file, <200MB, SDXL)
7. Create V3 production script: epiCRealism XL + double LoRA + graduated cn_strength + FaceDetailer + anti-AI prompts
8. Run V3 batch, quality gate, download results

## Scripts on Pod
- `/workspace/instantid_production_v2.py` - V2 production script (Advanced + FaceDetailer) **LATEST**
- `/workspace/instantid_production.py` - V1 production script (basic InstantID)
- `/workspace/retrain_lora_v4.py` - LoRA training script (all compat fixes baked in) **REUSABLE**
- `/workspace/analyze_references.py` - Face analysis + dataset creation
- `/workspace/startup_v2.sh` - Bulletproof startup (SSH, packages, nodes, models, ComfyUI)
- `/workspace/test_v2.py` - Quick single-image V2 test script

## Local Files
- `tools/instantid_production_v2.py` - V2 production script **LATEST**
- `tools/instantid_production.py` - V1 production script
- `tools/retrain_lora_v3.py` - LoRA training script (v3 version, v4 on pod only)
- `tools/analyze_references.py` - Face analysis script
- `tools/startup_v2.sh` - Bulletproof pod startup v2
- `workflows/instantid_lora_production.json` - Reusable ComfyUI workflow
- `research/pose_variation_research.md` - Pose decoupling + FaceDetailer research
- `research/ai_influencer_workflow_guide.md` - Full research guide
- `sweep_results/production_v2/PASSED/` - 15 V2 production images that passed **LATEST**
- `sweep_results/production_v2/FAILED/` - 21 V2 images that failed quality gate
- `sweep_results/production_v4/` - 36 v4 production images (all passed)
- `sweep_results/production/` - 36 v3 production images (all passed)
- `sweep_results/combo/` - 20 InstantID combo results
- `references/midjourney/` - 48 MJ reference images uploaded for v4 training

## v4 Reference Image Quality
Top 5 references (by face area):
- img_002: area=428744 (BEST)
- img_003: area=349193
- img_007: area=309517
- img_001: area=298754
- img_000: area=297127

47 of 48 training images have faces detected (up from 14/36 in v3).

## Similarity Score History
| Method | Avg | Best | Notes |
|--------|-----|------|-------|
| LoRA only | ~0.30 | 0.35 | No face lock |
| FaceID + LoRA | 0.41 | 0.475 | First corrected |
| Aggressive FaceID | 0.42 | 0.524 | Ceiling reached |
| InstantID + LoRA v3 (combo test) | 0.71 | 0.74 | Breakthrough |
| InstantID + LoRA v3 (production) | 0.70 | 0.75 | 36 varied images, single-ref scoring |
| InstantID + LoRA v4 (production v1) | 0.65 | 0.71 | 36 images, multi-ref scoring |
| **InstantID + LoRA v4 (V2 close-ups)** | **0.60** | **0.71** | **FaceDetailer + Advanced, pose variety** |

Note: v4+ uses stricter 5-reference-average scoring. Single-ref scoring on v4 = 0.74 avg.

## Pod Details
- Pod ID: tli3h17sfekhpn
- GPU: RTX 4090 (24GB VRAM) | Cost: ~$0.60/hr
- Storage: 50GB persistent at /workspace
- ComfyUI path: /workspace/runpod-slim/ComfyUI/
- Trigger word: "amiranoor"
- SSH: Check RunPod dashboard for current SSH command (may change after migration)
- SSH public key must be added after each migration
- After migration run: `bash /workspace/startup_v2.sh`

## Key Decisions
- Persona: Amira Noor, 21, Egyptian/Brazilian mix
- Mean Framework: 8/10 who thinks she's a 6/10, accessible fantasy
- Platform: Fanvue (explicit AI creator support)
- Revenue target: $30K/month in 60 days
- Partners: Matt (MJ) + Vitaley's Cousin (VS)
- GitHub: vitaleysha-svg/pistachio (private)
