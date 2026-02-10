---
name: pistachio-workflow
description: End-to-end workflow for RunPod, ComfyUI, LoRA training, parameter sweeps, and production batch generation for Pistachio.
---

# Pistachio Workflow Skill

## Scope
Use this skill for AI influencer image pipeline work: pod setup, LoRA retraining, inference quality checks, and automation scripts.

## Core Stack
- RunPod RTX 4090 pod
- ComfyUI API on port `8188`
- SDXL checkpoints (RealVisXL v5 baseline, compare with alternatives)
- InstantID + IPAdapter FaceID for face consistency
- LoRA trained from curated Midjourney set

## Canonical Paths (Pod)
- `/workspace/training_images/` source images
- `/workspace/lora_dataset_v3/` resized images + captions
- `/workspace/reg_images/` regularization images
- `/workspace/lora_output_v3/` training output/checkpoints
- `/workspace/runpod-slim/ComfyUI/` ComfyUI root
- `/workspace/runpod-slim/ComfyUI/models/loras/` deployed LoRA files

## Session Flow
1. Run startup script and verify pod health checks pass.
2. Generate or refresh per-image captions.
3. Verify regularization image directory exists and is populated.
4. Train LoRA v3 with pinned dependencies and reproducible params.
5. Run sweep to compare checkpoints/settings and score face similarity.
6. Deploy best LoRA to ComfyUI and run production batch generation.
7. Backup workflow artifacts before ending session.

## LoRA v3 Training Defaults
- Trigger token: `amiranoor`
- Resolution: `1024x1024`
- Steps: `2500`
- Optimizer: `Prodigy`
- `--network_dim 32` when VRAM permits
- Use `--xformers` and gradient checkpointing
- Use regularization with `--reg_data_dir /workspace/reg_images`

## Captioning Rules
- One caption file per image (`image.ext` -> `image.txt`)
- Start every caption with trigger token
- Keep identity token fixed; vary pose, clothing, lighting, camera angle, and environment details
- Do not use generic repeated template captions

## Inference Baseline
- Test LoRA-only and LoRA + InstantID variants
- Sweep CFG values (`3.5`, `4.0`, `4.5`)
- Sweep samplers (`dpmpp_2m`, `euler_a`, `dpmpp_sde`)
- Keep denoise/steps constant per sweep cell for fair comparison
- Save labeled filenames and comparison montage

## Quality Gates
- Face resemblance is stable across poses/outfits
- Skin texture remains natural (not plastic or over-smoothed)
- Prompt obedience is consistent across tested scenes
- User review target: at least `7/10` vs OG references

## RunPod Operational Rules
- Pin dependency versions; never leave training deps unpinned
- Prefer uploadable `.py` or `.sh` scripts over copied multi-line terminal commands
- Automate startup checks so pod boot requires zero manual fix commands
- Treat warnings as possible root causes until disproved

## Troubleshooting Priorities
1. Dependency/version mismatch
2. Missing models or custom nodes
3. ComfyUI API unreachable
4. Disk/VRAM resource limits
5. Workflow JSON drift vs expected graph

## Deliverables Per Iteration
- Updated scripts committed locally
- New checkpoint evaluation artifacts
- Workflow backup archive
- Brief change log entry in `CODEX-CHANGES.md`
