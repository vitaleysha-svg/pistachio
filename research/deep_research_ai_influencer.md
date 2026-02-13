# Professional AI Influencer Techniques — Deep Research (2026-02-11)

## KEY FINDING: Our biggest gap is NOT using FaceDetailer with LoRA as a second pass

## The Professional Stack (What Top Creators Actually Use)
1. Base generation: Flux Dev or SDXL (via ComfyUI)
2. Identity lock: Custom LoRA (trained on character)
3. Face reinforcement: **FaceDetailer + LoRA second pass** (97% identity scores)
4. Pose control: ControlNet (OpenPose/DWPose)
5. Face reference: IP-Adapter FaceID (supplementary)
6. Post-processing: Color grading, film grain, imperfections
7. Upscaling: Topaz Photo AI or 4x-UltraSharp

## The "Triple Stack" (Community Consensus)
1. Character LoRA for base identity
2. IP-Adapter FaceID for additional face consistency
3. ControlNet for pose control

## Face Similarity Comparison
| Method | Face Similarity | Best For |
|--------|----------------|----------|
| Custom LoRA + FaceDetailer | 97-100% | Ongoing projects (THIS IS US) |
| HyperLoRA | ~95% | Creative variations |
| ACE++ | ~99% | Background swaps |
| InstantID | ~90% | Quick one-offs |
| PuLID | ~85% | Quick reference-based |
| IP-Adapter FaceID | ~80% | Supplementary guidance |

## CRITICAL: FaceDetailer as Second Pass (What We're Missing)
- After generating base image, run FaceDetailer with OUR LoRA loaded
- This detects face region and regenerates JUST the face with our LoRA
- Achieves 97% identity recognition scores
- Settings: denoise 0.40-0.50, LoRA strength 0.8-1.0, feather 16-32, face_margin 1.6
- Multi-pass: first pass 0.50 denoise, second pass 0.30 denoise

## Breaking the AI Look — Specific Techniques

### Prompt-Level
- Specify camera equipment: "Canon EOS R5, 85mm f/1.4, ISO 400"
- Real lighting: "softbox at 45 degrees, window light, golden hour, catchlights in eyes"
- Micro-imperfections: "subtle skin pores, flyaway hair, slight asymmetry"
- Film stocks: "shot on Kodak Portra 400" for organic color science

### Negative Prompts (SDXL)
```
(worst quality, low quality:1.4), (blurry:1.2), (deformed face, distorted face, bad anatomy:1.3),
(asymmetrical eyes, dead eyes, crossed eyes:1.3), (plastic skin, waxy skin, poreless skin:1.3),
(bad teeth, unnatural smile:1.2), (cartoon, anime, illustration, painting:1.4),
3d render, cgi, doll, mannequin, uncanny valley, text, watermark, signature,
over-smoothed, harsh color cast, banding
```

### Post-Processing (Critical)
- Film grain using Perlin noise (ComfyUI-post-processing-nodes: FilmGrain node)
- Film LUTs (Kodak Portra, Fuji Pro 400H) via ProPostApplyLUT
- Subtle vignetting
- Chromatic aberration at edges
- Slight lens distortion
- JPEG compression artifacts (real photos have these!)
- GitHub repos: comfyui-propost, ComfyUI-post-processing-nodes

### What Makes AI Images Look Fake
1. Porcelain/plastic skin with zero pores (OUR #1 PROBLEM)
2. Over-smoothed/airbrushed skin
3. Waxy/glossy sheen on foreheads/cheeks (OUR #2 PROBLEM)
4. Conflicting light sources
5. Glassy, lifeless eyes
6. Too-perfect symmetry
7. Stiff mannequin poses (OUR #3 PROBLEM — FIXED with cn_strength)
8. Identical expression across every image

## Sampler Settings for Maximum Photorealism

### SDXL
- Sampler: DPM++ 2M SDE Karras (community standard)
- CFG: 5-7 (portraits: 5-6) — WE USE 3.5, MAY BE TOO LOW
- Steps: 30 (we use 28, close enough)
- Scheduler: Karras

### Flux
- Sampler: Euler
- Scheduler: Simple
- CFG: ~2
- Steps: 20-30

## LoRA Training Best Practices
- 20-30 high quality images (we have 47 — good)
- Must include: front, 3/4, side profile, varied expressions, varied lighting
- Network Rank: 32 (we may need to check ours)
- Epochs: 10-30 for SDXL
- Quality > quantity

## Reference Image Strategy
- Multiple angles ALWAYS (we do this — good)
- 3-5 front, 3-5 three-quarter, 2-3 profile, 2-3 up/down, 3-5 expressions
- No heavy filters on training images

## ACTION ITEMS FOR V3
1. **FaceDetailer with LoRA loaded** — regenerate face with identity LoRA (biggest quick win)
2. **Better negative prompts** — add anti-plastic, anti-smooth terms
3. **Camera/lens prompts** — "Canon EOS R5, 85mm f/1.4"
4. **Film grain post-processing** — install ComfyUI-post-processing-nodes
5. **CFG 5-6** instead of 3.5 (may improve prompt adherence)
6. **Film LUT color grading** — Kodak Portra style
7. Consider FLUX migration for fundamentally better results
