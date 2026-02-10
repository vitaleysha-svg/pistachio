# Pistachio Progress Tracker

## Last Updated: 2026-02-10
## Current Phase: LoRA v2 Trained + v3 Scripts Ready - Upload and Retrain Next
Full session history available in git log.

## What Just Happened (Session 6 - 2026-02-10)
- LoRA v2 trained: amiranoor_v2.safetensors (228.5 MB), 36 images, 2000 steps, UNet + Text Encoder
- Parameter sweep completed: 9 images (3 checkpoints x 3 strengths), all showed quality issues
- Root causes identified: generic captions, no regularization images, manual-only face scoring
- Codex created v3 pipeline scripts: auto_caption.py, retrain_lora_v3.py, parameter_sweep_v2.py
- Codex hardened system: CLAUDE.md trimmed to 53 lines, guardrails passing, skills created
- Supporting scripts added: download_reg_images.py, pod_health_check.py, startup_v2.sh, generate_batch.py

## What We're Doing RIGHT NOW
- **Pod ID:** tli3h17sfekhpn | GPU: RTX 4090 (24GB) | ComfyUI running on port 8188
- **LoRA v2 deployed:** /workspace/runpod-slim/ComfyUI/models/loras/amiranoor_v2.safetensors
- **Trigger word:** "amiranoor"
- **v3 scripts ready locally** in tools/ -- need to be uploaded to pod
- **Sweep results** in /workspace/sweep_results/ -- quality insufficient, proceeding to v3
- **ComfyUI path:** /workspace/runpod-slim/ComfyUI/ (NOT /workspace/ComfyUI/)
- **Python:** python3 (NOT python)

## Immediate Next Steps
1. Upload v3 scripts to pod (auto_caption.py, retrain_lora_v3.py, parameter_sweep_v2.py, download_reg_images.py)
2. Download regularization images on pod (generic SDXL woman photos for prior preservation)
3. Run auto_caption.py on training images (BLIP-2 captions with trigger word)
4. Kill ComfyUI, train LoRA v3 with retrain_lora_v3.py (Prodigy optimizer + regularization)
5. Restart ComfyUI, run parameter_sweep_v2.py (includes InsightFace face similarity scoring)
6. Review scored results and pick best combo for production

## Pod Details
- Pod ID: tli3h17sfekhpn
- GPU: RTX 4090 (24GB VRAM) | Cost: ~$0.60/hr
- Storage: 50GB persistent at /workspace
- Auto-fix on boot: startup.sh + post_start.sh hook (nodes, deps, permissions, ComfyUI restart)
- Scripts on pod: fix_and_start.py, retrain_lora_v2.py, parameter_sweep.py, train_lora.py

## Key Decisions
- Persona: Amira Noor, 21, Egyptian/Brazilian mix
- Mean Framework: 8/10 who thinks she's a 6/10, accessible fantasy
- Platform: Fanvue (explicit AI creator support)
- Revenue target: $30K/month in 60 days
- Partners: Matt (MJ) + Vitaley's Cousin (VS)
- GitHub: vitaleysha-svg/pistachio (private)
