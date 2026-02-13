# PuLID vs InstantID — Deep Research (2026-02-11)

## Key Finding: EcomID is the BEST option (hybrid PuLID + InstantID)

## PuLID Architecture
- Dual-branch training: standard + Lightning T2I branch
- Contrastive alignment loss minimizes "model pollution" (preserves style/composition)
- Uses InsightFace + EVA-CLIP for face features
- Pure cross-attention injection (no ControlNet spatial conditioning)

## PuLID vs InstantID Comparison

| Aspect | PuLID | InstantID |
|---|---|---|
| Face similarity score | 0.733 | 0.725 |
| Pose freedom | LOW (locks to reference pose) | HIGH (IdentityNet gives spatial control) |
| Prompt adherence | Lower (fights creative prompts) | Higher |
| VRAM usage | 10.2 GB | 8.5 GB |
| Speed | ~35 sec/image | ~28 sec/image |
| Expression variety | Most restrictive | Good with angles |

## CRITICAL: PuLID LOCKS POSE
- PuLID mirrors reference image pose and hairstyle
- Cannot reliably generate different expressions/poses
- At lower strength, loses identity
- **For our use case (many varied poses), InstantID is BETTER**

## EcomID — Best of Both Worlds
- By Alibaba (Alimama Creative)
- Combines PuLID's ID-Encoder (identity fidelity) + InstantID's IdentityNet (pose control)
- GitHub: https://github.com/alimama-creative/SDXL_EcomID_ComfyUI
- SDXL compatible
- **THIS IS WHAT WE SHOULD TRY**

## PuLID ComfyUI Setup (if needed)
- Repo: https://github.com/cubiq/PuLID_ComfyUI (MAINTENANCE ONLY as of April 2025)
- Model: ip-adapter_pulid_sdxl_fp16.safetensors → ComfyUI/models/pulid/
- Also needs: EVA02-CLIP-L-14-336 (auto-downloads)
- Nodes: PulidModelLoader, PulidEvaClipLoader, PulidInsightFaceLoader, ApplyPulid, ApplyPulidAdvanced

## Known Issues
- VRAM leak with facexlib/EVA-CLIP preprocessors
- Small faces lose detail (distorted features at distance)
- Multi-person scenes: cannot target specific character
- No SD 1.5 support (SDXL and FLUX only)

## Recommendation for Pistachio
1. **Keep InstantID** for pose variety (our #1 need)
2. **Try EcomID** as potential upgrade (best identity + pose)
3. **Do NOT switch to PuLID alone** — would make pose variety worse
