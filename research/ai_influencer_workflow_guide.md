# Complete AI Influencer Face Consistency Workflow Guide (2025-2026)
# Saved from research agent - 2026-02-11

## THE THREE PROVEN METHODS (Ranked by Consistency)

### Method A: LoRA Training (Best - 97%+ Identity Match)
What $25k+/month creators use (BlackHatWorld verified).

**Kohya Training Settings:**
- Images: 15-25 high-quality (different angles, lighting, expressions)
- Network Rank (dim): 32 (64 for more detail)
- Network Alpha: 16 (half of rank)
- Learning Rate: 1e-4
- Epochs: 10-15
- Image Repeats: 15-20 (SDXL); 1-5 (Flux)
- Batch Size: 1
- Expected loss: Start ~0.2, end ~0.05-0.10

### Method B: IP-Adapter FaceID Plus V2 (No Training - 80%+ Consistency)
**Exact Parameters:**
- FaceID v2 weight: 0.8
- v2 strength: 2.0
- Associated LoRA weight: 0.5-0.7 (sweet spot 0.62)
- Full Face weight: 0.5
- Boost: 0.3
- Embed combination: "concat"
- CFG Scale: 3-4 (drop when IP-Adapter is strong)
- Reference photos: 3-5 (front, profile, three-quarter views)

### Method C: Flux PuLID (Newest - Best Single-Image Identity)
**Exact Settings:**
- id_weight: 0.8-0.95 (v0.9.0); 0.9-1.0 (v0.9.1)
- start_step: 4 for realistic; 0-1 for stylized
- end_step: 1.0
- FluxGuidance (true_cfg): 2.5-3.5
- Use "fake CFG" for photorealistic
- VRAM: 12GB+ minimum

## SDXL vs FLUX
Flux is preferred by serious creators. SDXL for quick testing.
FLUX.1 Kontext (2025) maintains character consistency across edits without fine-tuning.

## EXACT CHECKPOINT + LoRA + ADAPTER COMBOS

### SDXL Pipeline:
- Checkpoint: epiCRealism XL OR RealVisXL V5.0 OR Juggernaut XL Ragnarok
- Face Adapter: IP-Adapter FaceID Plus V2 SDXL
- Face LoRA: Auto-loaded by IPAdapter Unified Loader FaceID
- Skin texture: ReaLora (CivitAI model 137258)
- Face fix: FaceDetailer from Impact Pack

### Flux Pipeline:
- Base: Flux Dev (or Schnell for speed)
- Face identity: PuLID-Flux
- Style: Flux Redux (combine with PuLID)
- New option: FLUX.1 Kontext dev (12B parameter)

## GENERATION PARAMETERS

### SDXL Realistic Portraits:
- Steps: 20-30
- CFG: 7-9 normally; 3-4 with strong IP-Adapter
- Sampler: DPM++ 2M Karras
- Resolution: 1024x1024

### FaceDetailer Settings:
- Denoise: 0.1-0.2 for subtle fixes; 0.40-0.45 for face swaps
- face_margin: 1.6
- Feather: 16-32
- Steps: 50
- CFG: 5-8

## FIXING AI GLOW / PLASTIC SKIN

### Negative Prompts (Essential):
```
(smooth skin:1.3), (plastic skin:1.3), (airbrushed:1.2), (overly smooth:1.2),
(unrealistic skin texture:1.1), (doll-like:1.2), (wax figure:1.1),
(blurry skin texture:1.1), (smudged details:1.1), cartoon, anime, painting,
illustration, 3d render, deformed features, overexposed, worst quality,
low quality, jpeg artifacts, compression artifacts
```

### Additional Fixes:
- Skin texture LoRA: ReaLora (CivitAI 137258)
- FreeU node for detail rendering
- FaceDetailer low denoise (0.1-0.3)
- Film halation effects

## DOWNLOADABLE WORKFLOW TEMPLATES (CivitAI)
1. Flux PuLID Face Swap v2.0 - civitai.com/models/929131
2. Flux Redux + PuLID - civitai.com/models/989680
3. Consistent Face 3x3 Generator - civitai.com/models/1224719
4. Realistic AI Influencer SDXL - civitai.com/models/1937151
5. AI Influencer Dataset Maker v3.0 - civitai.com/models/2182806
6. FaceDetailer + InstantID + IP-Adapter - openart.ai
7. Fix Plastic Skin Workflow - openart.ai

## PRODUCTION WORKFLOW (Revenue-Generating Creators)

### Step 1: Character Creation
- Generate 1 perfect hero face
- Create 15-25 variants with PuLID/FaceID (different angles)
- Curate best images

### Step 2: LoRA Training
- Train custom LoRA with kohya_ss
- SDXL: rank 32, alpha 16, lr 1e-4, 15 epochs, 20-40 repeats
- Flux: rank 32, alpha 16, lr 1e-4, 12 epochs, 5 repeats

### Step 3: Content Production
- LoRA (0.7-1.0) + ControlNet/OpenPose
- FaceDetailer (denoise 0.1-0.2)
- Skin texture fixes + upscale 2x

### Step 4: Monetization
- Platform: Fanvue (80% payout, AI-friendly)
- Pricing: $7-15/month
- Posting: 3-5x/week
- Team: 1 designer + 2 chatters (20% of PPV+tips)
- Timeline: M1-3 $200-500, M3-6 $500-3000, M6-12 $5000-10000+
- Top operators: 4+ characters simultaneously

## COMMON MISTAKES
1. CFG too high with IP-Adapter (use 3-4)
2. Not using FaceDetailer as final pass
3. Only 1 reference photo (need 3-5)
4. PuLID id_weight 1.0 on v0.9.0 (use 0.8-0.95)
5. Skipping LoRA for production
6. Wrong checkpoint (need photorealism-specific)
7. No skin-specific negative prompts
8. Wrong resolution (SDXL: 1024x1024)
