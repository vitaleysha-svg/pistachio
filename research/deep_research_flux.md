# FLUX for Photorealism — Deep Research (2026-02-11)

## KEY FINDING: FLUX is fundamentally superior to SDXL for photorealism. Worth switching.

## FLUX vs SDXL Architecture
- FLUX: 12B params, Diffusion Transformer (DiT), 16-channel VAE, T5-XXL text encoder
- SDXL: 2.5B params, UNet, 4-channel VAE, CLIP text encoder
- FLUX captures finer details, richer textures, better color gradients
- FLUX handles anatomy (hands, fingers) FAR better than SDXL
- FLUX understands subsurface scattering in skin, specular highlights, fabric light interaction
- Tradeoff: FLUX is 3-4x slower (57s vs 13s per image)

## FLUX Models Ranked for Photorealism
1. FLUX 1.1 Pro Ultra / FLUX.2 — absolute best
2. FLUX.1 Kontext [pro/max] — best for consistent characters
3. **FLUX.1 [dev]** — best freely available local model (THIS IS WHAT WE'D USE)
4. FLUX.1 [schnell] — fast but less detail

## RTX 4090 Compatibility (24GB VRAM)
- FP16/BF16: ~23-24GB (tight fit)
- **FP8: ~12-14GB** (minimal quality loss, RECOMMENDED)
- GGUF Q8: ~12-14GB (near-identical to full)
- With FP8: ~14-17 seconds per image at 1024x1024, 28 steps

## Face Identity Tools for FLUX
| Tool | Similarity | Notes |
|------|-----------|-------|
| FLUX Kontext + PuLID | 94-96% | BEST combination |
| ACE++ + Flux Fill | ~99% | For background swaps |
| PuLID-FLUX | High | Mirrors reference pose (bad for variety) |
| EcomID | High | Most complex setup |

## FLUX LoRA Training for Identity
- Tools: OneTrainer (best for faces), SimpleTuner, Kohya SS, FluxGym
- 23-28 images, 1024x1024 minimum
- Steps: 800-1500 (sweet spot ~1250)
- Network rank: 32-48
- Learning rate: 0.0008-0.0015
- FP8 quantization to fit on 24GB
- Training time: ~30-60 min on RTX 4090

## Recommended FLUX Pipeline for AI Influencer
### No-training approach:
- FLUX.1 Kontext [dev] + PuLID
- Single reference face → identity
- Kontext handles consistency
- ControlNet for pose

### With training (better):
- Train FLUX LoRA (23-28 images, OneTrainer)
- Combine LoRA + PuLID for double identity lock
- Use Kontext for scene variation

### Best base model:
- **Juggernaut Pro FLUX** — best photorealistic FLUX fine-tune on CivitAI

## ComfyUI Setup for FLUX
### Files needed:
- flux1-dev.safetensors (or fp8) → models/diffusion_models/
- T5-XXL encoder → models/clip/
- clip_l.safetensors → models/clip/
- ae.safetensors → models/vae/

### Nodes:
- UNETLoader, DualCLIPLoader, VAELoader, KSampler
- ComfyUI-PuLID-Flux (github.com/balazik/ComfyUI-PuLID-Flux)
- ComfyUI-IPAdapter-Flux (github.com/Shakker-Labs/ComfyUI-IPAdapter-Flux)
- x-flux-comfyui (github.com/XLabs-AI/x-flux-comfyui) for ControlNet

### Settings:
- CFG: 1-2 (much lower than SDXL!)
- Sampler: euler or euler_ancestral
- Steps: 20-28

## MIGRATION PATH: SDXL → FLUX
### What we keep:
- Reference images (same dataset)
- InsightFace models (same antelopev2)
- ComfyUI infrastructure
- Quality gate script

### What changes:
- New checkpoint (~12GB for FLUX dev)
- New LoRA training (retrain on FLUX)
- New nodes (PuLID-Flux instead of InstantID)
- New sampler settings (euler, CFG 1-2)
- No traditional negative prompts (FLUX ignores them)

## DECISION: Should We Switch?
### For V3 (immediate): NO — stick with SDXL + epiCRealism XL + all improvements
- We have working pipeline, just need optimization
- FLUX migration adds 2-3 hours of setup + LoRA retraining
- Let's exhaust SDXL improvements first

### For V4 (if V3 still not good enough): YES — migrate to FLUX
- Fundamentally better photorealism
- Better anatomy
- Better skin rendering
- Kontext + PuLID = 94-96% consistency
- RTX 4090 handles it well in FP8
