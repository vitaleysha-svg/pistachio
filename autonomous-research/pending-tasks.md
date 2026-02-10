# Pistachio Pending Tasks

Last updated: 2026-02-10

## Pending Review

### LoRA v3 Training Pipeline (Priority: HIGH)
1. Upload v3 scripts to pod: auto_caption.py, retrain_lora_v3.py, parameter_sweep_v2.py, download_reg_images.py
2. Run download_reg_images.py on pod to get regularization images (generic SDXL woman photos)
3. Run auto_caption.py on 36 training images (BLIP-2 generates per-image captions with "amiranoor" trigger)
4. Kill ComfyUI process to free VRAM
5. Run retrain_lora_v3.py (Prodigy optimizer, regularization data, 2500 steps, xformers)
6. Restart ComfyUI via fix_and_start.py
7. Run parameter_sweep_v2.py (LoRA-only + LoRA+InstantID, InsightFace face similarity scoring)
8. Review sweep_summary.csv and top10_by_similarity.csv, pick best combo

### Production Pipeline (Priority: MEDIUM, blocked by v3)
9. Test winning combo with InstantID at low weight (0.30-0.40) for reinforcement
10. Generate first batch of 50+ consistent images via generate_batch.py
11. Set up Wan2.2 video animation on ComfyUI
12. Inpainting body sculpting walkthrough

### Platform Launch (Priority: LOW, blocked by production images)
13. Finalize Fanvue account setup
14. Instagram @itsamiranoor content calendar
15. ManyChat DM automation flows

## Completed
- LoRA v1 trained and tested (quality insufficient)
- LoRA v2 trained with UNet + Text Encoder (228.5 MB)
- Parameter sweep v1 completed (9 images, manual review)
- Codex hardening pass (CLAUDE.md, skills, v3 scripts)
- Pod auto-fix system (startup.sh + post_start.sh)
