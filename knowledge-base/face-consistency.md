# Face Consistency Techniques

> How to maintain the same face across multiple images.
> Last updated: 2026-02-03

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

### Key Settings

- IP-Adapter weight: 0.7-0.9 (higher = more similar)
- ControlNet strength: 0.8-1.0
- CFG Scale: 7-8

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

## Sources

- [InstantID Official](https://instantid.github.io/)
- [100% Face Similarity Workflow](https://medium.com/@wei_mao/100-face-similarity-the-ultimate-face-swap-workflow-better-than-any-pulid-instantid-b7fa2daa5659)
- [ComfyUI InstantID + IP-Adapter Tutorial](https://myaiforce.com/comfyui-instantid-ipadapter/)
- [Stable Diffusion Art - InstantID Guide](https://stable-diffusion-art.com/instantid/)

---

*Updated by Pistachio CoS Agent - 2026-02-03*
