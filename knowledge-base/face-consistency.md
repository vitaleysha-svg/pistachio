# Face Consistency Techniques

> How to maintain the same face across multiple images.
> Last updated: 2026-02-06

## Technique Comparison

| Technique | Difficulty | Quality | Speed | VRAM | Best For |
|-----------|------------|---------|-------|------|----------|
| **InstantID** | Medium | 9/10 | Fast | ~20GB | Best overall balance |
| IP-Adapter FaceID | Medium | 8/10 | Fast | ~12GB | Faster, less VRAM |
| LoRA Training | High | 10/10 | Slow setup | Varies | Maximum control |
| Face Swap (post) | Low | 7/10 | Fast | Low | Quick fixes |
| Reference Images | Low | 6/10 | Fast | N/A | Basic consistency |

## RECOMMENDED: InstantID + IP-Adapter Combo

This workflow achieves near 100% face similarity while allowing pose/outfit changes.

### How It Works

1. **InsightFace** detects, crops, and extracts face embedding from reference
2. **IP-Adapter** controls generation using that embedding
3. **ControlNet** fixes facial landmarks (eyes, nose, mouth)
4. Combined = high fidelity face copying with style flexibility

### ComfyUI Workflow

**Required Models:**
- SDXL base model
- InstantID ControlNet
- IP-Adapter FaceID
- InsightFace model

**Node Connection:**
```
Reference Image → InsightFace → Face Embedding
Face Embedding → IP-Adapter → Model
Face Embedding → InstantID ControlNet → Model
Prompt → KSampler → Output
```

### Key Settings (Updated 2026-02-06 - Community Tested)

**InstantID Settings:**
- InstantID weight: **0.70-0.80** (NOT higher - causes "burn" effect, makes output look heavily AI-processed)
- ControlNet strength: 0.8-1.0
- CFG Scale: **4.0-4.5** (NOT 7-8 - higher CFG with InstantID = AI sharpness artifacts)
- Steps: **25-35** (sweet spot for quality vs speed)
- Sampler: **DPM++ 2M** with **Karras** scheduler (community consensus best for photorealism)
- WARNING: Do NOT use Euler + Karras combo = blurry artifacts
- Resolution: **1016x1280** (avoid exact 1024 - triggers SDXL training artifacts)
- end_at: **0.85-0.90** (let final steps run without InstantID = more natural finish)

**IP-Adapter FaceID Settings (use WITH InstantID):**
- IP-Adapter weight: 0.60-0.70
- Model: PLUS FACE (portraits) variant
- This transfers photographic QUALITY from reference, not just face structure

**Generation Mode:**
- **txt2img** (Empty Latent + denoise 1.0): Good for new scenes, but loses OG image quality
- **img2img** (Load Image + denoise 0.35-0.45): Better match to OG image's lighting/color/vibe
- Start with txt2img, switch to img2img if results need tighter match

**CRITICAL: The "Burn" Effect**
- InstantID weight > 0.85 = over-processed, fake look
- Community consensus: 0.75 is the sweet spot
- Combined with high CFG (>5.0), burn effect is amplified
- Signs of burn: dark faces, plastic skin, wrong lighting, "heavily AI" look

## Solving the "Composition Lock" Problem

**Problem:** InstantID tends to maintain reference image composition. Headshot input = headshot output.

**Solution:** Use FaceDetailer + InstantID + IP-Adapter workflow
- Generates base portrait with SDXL first
- FaceDetailer adjusts facial features
- InstantID swaps face while matching pose/lighting
- Result: Any composition with consistent face

## LoRA Training (Maximum Control)

**When to Use:**
- Need 100+ images of exact same person
- Want complete control over every detail
- Willing to invest 2-4 hours in setup

**Process:**
1. Collect 15-30 high-quality reference images
2. Caption each image (use BLIP or manual)
3. Train LoRA on SDXL (Kohya trainer)
4. Training time: 30-60 minutes on RTX 4090
5. Use trained LoRA with trigger word

**Trigger Word Example:**
```
photo of pistachio_character, [rest of prompt]
```

## The 3-Phase Fix (Proven Workflow)

### Phase 1: Settings Fix (Do First)
1. Set InstantID weight to **0.75**
2. Set CFG to **4.0**
3. Set steps to **35**
4. Set resolution to **1016x1280**
5. Write positive prompt that **matches** OG image vibe (don't fight it)
6. Use weighted negative prompt for SDXL: `(airbrushed:1.4), (smooth skin:1.3)` etc.
7. Generate and compare to OG

### Phase 2: Add IP-Adapter FaceID (If Phase 1 Not Enough)
1. Add **IPAdapter Unified Loader FaceID** node - select "PLUS FACE (portraits)"
2. Add **IPAdapter Apply** node - connect to pipeline
3. Connect same reference image to IP-Adapter
4. Set IP-Adapter weight: 0.60-0.70
5. This transfers photographic quality, not just face structure

### Phase 3: Switch to img2img (If Need Tighter Match)
1. Remove Empty Latent Image node
2. Add Load Image node with OG reference
3. Add VAE Encode node between Load Image and KSampler latent_image input
4. Set KSampler denoise to **0.40** (keep 60% of OG, change 40%)
5. Preserves OG's lighting, color grading, composition

## Quick Start: Face Consistency Today

**Step 1:** Generate your best portrait in Midjourney
**Step 2:** Use that as reference for InstantID in ComfyUI
**Step 3:** Generate variations with different poses/outfits
**Step 4:** If quality drops, consider LoRA training

## Reference Image Best Practices

For best InstantID/IP-Adapter results:

- High resolution (1024px+ face)
- Clear, well-lit face
- Neutral expression OR match target expression
- 3-5 angles if possible
- Consistent lighting across references

## VRAM Requirements

| Setup | Minimum VRAM |
|-------|--------------|
| InstantID alone | 16GB |
| InstantID + IP-Adapter | 20GB |
| Full workflow + upscale | 24GB |
| LoRA training | 12GB (with optimization) |

**Cloud GPU Option:** RunPod, Vast.ai - ~$0.50/hour for 24GB

## Community Research Findings (2026-02-06)

Researched via WebSearch across Reddit, CivitAI, GitHub, tutorials. Key validated findings:

**From cubiq/ComfyUI_InstantID (official repo):**
- Default Apply InstantID node automatically injects 35% noise to negative embeds to reduce burn
- Use Advanced InstantID node to fine-tune noise injection (20-50%)
- InstantID model influences composition ~25%, ControlNet does the rest
- CFG must be lowered to 4-5, or use RescaleCFG node

**From community tutorials & CivitAI:**
- FaceDetailer + InstantID + IP-Adapter combo = best face swap quality
- IP-Adapter FaceID Plus V2 weight: 0.65-0.80 for face consistency
- For img2img: test denoise at 0.35, 0.45, 0.55 - 0.35 keeps face tight, 0.55 lets style breathe
- RealVisXL v3.0 Turbo and v5 produce most life-like faces
- InstantID is designed more for styling than photorealism - set expectations accordingly

**From img2img best practices:**
- Denoise 0.0 = output identical to input, 1.0 = complete regeneration
- Sweet spot for identity preservation: 0.35-0.50
- If identity too loose, lower denoise OR increase ControlNet weight
- Fixed seed helps consistency across variations

## Sources

- [InstantID Official](https://instantid.github.io/)
- [cubiq/ComfyUI_InstantID GitHub](https://github.com/cubiq/ComfyUI_InstantID)
- [100% Face Similarity Workflow](https://medium.com/@wei_mao/100-face-similarity-the-ultimate-face-swap-workflow-better-than-any-pulid-instantid-b7fa2daa5659)
- [ComfyUI InstantID + IP-Adapter Tutorial](https://myaiforce.com/comfyui-instantid-ipadapter/)
- [Stable Diffusion Art - InstantID Guide](https://stable-diffusion-art.com/instantid/)
- [FaceDetailer + InstantID + IP-Adapter (OpenArt)](https://openart.ai/workflows/myaiforce/better-face-swap-facedetailer-instantid-ip-adapter/KMFUVKakzXeepb2pMEnT)
- [CivitAI img2img All-in-One Guide](https://civitai.com/articles/15480/img2img-comfyui-all-in-one-workflow-guide)
- [Character Consistency with img2img](https://z-image.ai/blog/character-consistency-img2img)
- [ComfyUI InstantID DeepWiki](https://deepwiki.com/cubiq/ComfyUI_InstantID/4.1-basic-usage)

---

## Prompt Strategy for Realism

**Positive prompt must MATCH the reference image vibe.** If OG is outdoor/candid, don't prompt for indoor/studio. InstantID tries to merge both signals = muddy result.

**Negative prompt with SDXL weights** (parentheses + number = emphasis):
```
(airbrushed:1.4), (smooth skin:1.3), (perfect skin:1.3), (studio lighting:1.2),
(professional photo:1.2), (glamour:1.2), (retouched:1.3), (3d render:1.5),
(cartoon:1.5), (anime:1.5), (illustration:1.4), (painting:1.4),
(symmetrical face:1.2), (stock photo:1.3), (plastic skin:1.4), (waxy:1.3),
(oversaturated:1.2), (HDR:1.2), double head, extra limbs, watermark, text, logo
```

## Future Optimization

- **LoRA Training**: Train on 20-30 images for 95-98% consistency. Break-even after ~15 images.
- **FaceDetailer**: Post-processing node for face refinement after generation
- **ControlNet OpenPose**: Control exact poses from reference images
- **Checkpoint A/B Test**: JuggernautXL v9, epiCRealism XL vs RealVisXL v5
- **4x-UltraSharp Upscaler**: Final output quality boost

---

*Updated by Pistachio CoS Agent - 2026-02-06*
