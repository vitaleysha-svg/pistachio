# Project Pistachio - Current Context (Authoritative)

> Updated for current state. This file is authoritative for active project context.
> Legacy snapshots are in `archive/` and `PROJECT-PISTACHIO-PLAN.md`.

## Outcome Target
- Primary business target: scale toward $30k/month using a multi-channel AI content platform.
- Current technical target: face-consistent, photorealistic outputs with natural skin texture.

## Current Stack
| Category | Current Stack |
|---|---|
| Image generation | Midjourney references + ComfyUI production generation |
| Identity consistency | InstantID + IPAdapter FaceID + LoRA checkpoints |
| Training | SDXL LoRA pipeline on RunPod (RTX 4090) |
| Core scripts | `tools/auto_caption.py`, `tools/retrain_lora_v3.py`, `tools/parameter_sweep_v2.py` |
| Pod automation | `tools/startup_v2.sh`, `tools/pod_health_check.py`, `tools/backup_and_download.py` |
| Batch production | `tools/generate_batch.py` |

## Current Status
- LoRA v2 exists and parameter sweep baseline is complete.
- v3 training/automation scripts are implemented locally and ready for pod upload/run.
- Context system has been compacted and moved to skills to reduce prompt bloat.

## Active Bottlenecks
1. Close identity/quality gap vs OG references through v3 training loop.
2. Ensure pod startup path is zero-manual and verifiably healthy.
3. Convert documented learnings into executable checks to prevent regressions.
4. Keep source-of-truth docs fresh so autonomous loops do not drift.

## Execution Priorities
1. Pod bootstrap + health check (`tools/startup_v2.sh` + `tools/pod_health_check.py`).
2. Dataset prep: auto-captions + regularization image set.
3. LoRA v3 training run with Prodigy + xformers.
4. Sweep and rank outputs by face similarity + visual review.
5. Run batch generation pipeline for production inventory.

## Non-Authoritative / Legacy
- `archive/operations-manual-v1.md`
- `PROJECT-PISTACHIO-PLAN.md`

Use them only for historical context, not current decisions.
