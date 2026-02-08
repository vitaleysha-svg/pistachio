# Prompt Iteration Log

> Every iteration makes the system smarter. Never delete entries - they're training data.

---

## How to Use This Log

Each iteration entry captures the full loop:
1. Reference image description
2. Decomposition (what Claude saw)
3. Prompt generated
4. Output result (what MJ/ComfyUI produced)
5. User feedback (what's right, what's wrong)
6. Adjustments made
7. Pattern extracted (reusable learning)

---

## Extracted Patterns (Compounds Over Time)

<!-- Add patterns here as they're discovered. Format: -->
<!-- - **[PATTERN NAME]**: [What works / what to avoid] -->

- **[BURN EFFECT]**: InstantID weight > 0.85 = over-processed, fake AI look. Sweet spot: 0.75. Max: 0.80.
- **[CFG CEILING]**: CFG > 5.0 with InstantID amplifies AI sharpness artifacts. Sweet spot: 4.0-4.5.
- **[PROMPT ALIGNMENT]**: Positive prompt MUST match reference image vibe. Outdoor ref + indoor prompt = muddy result.
- **[ACCESSORY TRANSFER]**: InstantID preserves accessories (caps, glasses) from reference even when prompt mentions them.
- **[RESOLUTION TRICK]**: Avoid exact 1024 width - use 1016 to dodge SDXL training artifact triggers.
- **[WEIGHTED NEGATIVES]**: SDXL responds to `(term:weight)` syntax in negatives. Key terms: `(airbrushed:1.4), (smooth skin:1.3), (3d render:1.5)`
- **[DUAL SYSTEM]**: InstantID = face structure. IP-Adapter FaceID = style/quality transfer. Use both for pro results.
- **[IMG2IMG FALLBACK]**: When txt2img can't match OG quality, switch to img2img with denoise 0.40 to preserve 60% of original.
- **[SAMPLER MATTERS]**: DPM++ 2M Karras is community consensus best for photorealism. DO NOT use Euler + Karras combo = blurry artifacts.
- **[END_AT TRICK]**: Set InstantID end_at to 0.85-0.90 to let final denoising steps run without InstantID = more natural results.
- **[NOISE INJECTION]**: Default Apply InstantID injects 35% noise to negatives. Use Advanced node to tune 20-50%. Higher noise = more natural, less identity.
- **[COMBO WEIGHTS]**: In FaceDetailer+InstantID+IP-Adapter combo, InstantID drops to 0.60, IP-Adapter stays at 0.70. Lower than standalone.
- **[TURBO CHECKPOINT]**: RealVisXL v3.0 Turbo called out as "hands-down winner" for photorealistic faces over v5.

---

## Iteration Log

<!-- TEMPLATE FOR NEW ENTRIES:

### Iteration #[N] - [DATE]

**Reference**: [Description of input image or file path]

**Decomposition**:
- Face: [structure, features]
- Skin: [tone, texture, imperfections]
- Hair: [type, color, style]
- Expression: [mood, eye direction]
- Body/Pose: [type, position]
- Clothing: [what they're wearing]
- Environment: [setting, props]
- Lighting: [direction, quality, source]
- Camera: [framing, angle, lens estimate]
- Vibe: [overall aesthetic]

**MJ Prompt Generated**:
```
[full prompt with parameters]
```

**ComfyUI Settings** (if applicable):
- IP-Adapter weight: [value]
- ControlNet scale: [value]
- Checkpoint: [model name]

**Output**: [Description of what was generated / screenshot path]

**User Feedback**:
- Liked: [what was right]
- Disliked: [what was wrong]
- Score: [1-10 overall]

**Adjustments**: [What changed in the prompt]

**Pattern Extracted**: [Reusable learning from this iteration]

-->

### Iteration #1 - 2026-02-06

**Reference**: Pistachio741_Mixed_Japanese-Br... (Fukushima Larissa, Japanese/Brazilian, 21)

**Decomposition**:
- Face: Oval, soft jawline, almond-shaped dark eyes, subtle high cheekbones
- Skin: Warm golden-olive, natural texture, minimal makeup
- Hair: Dark, straight-to-wavy, under navy baseball cap
- Expression: Relaxed, casual, looking at camera
- Body/Pose: Upper body visible, natural posture
- Clothing: Dark casual top
- Environment: Outdoor, trees/greenery, natural setting
- Lighting: Natural outdoor, soft/diffused
- Camera: Medium close-up, ~50-85mm, shallow DOF
- Vibe: Candid, natural, approachable

**ComfyUI Positive Prompt**:
```
Mixed Japanese-Brazilian woman, 21, warm golden-olive skin, soft oval face, almond-shaped dark eyes, dark hair under navy cap, relaxed casual expression, cropped navy zip jacket, natural outdoor lighting, shot on Canon 5D Mark IV 50mm f1.4, shallow depth of field, natural skin texture, no retouching
```

**ComfyUI Negative Prompt**:
```
ugly, deformed, blurry, bad anatomy, bad hands, extra fingers, watermark, text, logo, plastic skin, overexposed, underexposed, oversaturated, cartoon, anime, 3d render
```

**ComfyUI Settings**:
- InstantID weight: 0.80
- InstantID start_at: 0.000, end_at: 1.000
- ControlNet: instantid-controlnet.safetensors
- Checkpoint: realvisxl_v5.safetensors
- KSampler: 20 steps, cfg 8.0, euler, simple scheduler, denoise 1.00
- Resolution: 1024x1280
- Seed: 248153786148954

**Output**: Successfully generated. Woman with navy cap, dark hair, navy jacket, outdoor blurred green background. Face structure transferred well from reference. Realistic quality, not obviously AI.

**User Feedback**:
- Liked: [PENDING - awaiting user feedback]
- Disliked: [PENDING]
- Score: [PENDING]

**Initial Claude Assessment**:
- Face transfer: 7/10 - good structural match, recognizable as same person
- Skin tone: 8/10 - golden-olive maintained well
- Realism: 7/10 - skin slightly too clean, could use more texture/imperfections
- Vibe: 7/10 - natural and candid, not stock-photo

**Adjustments for Next Run**: Try adding more imperfection triggers ("visible pores, slight blemishes"), test different scenario (indoor, different outfit), lower cfg to 7.0 for softer look

**Pattern Extracted**: InstantID weight 0.80 with RealVisXL v5 produces solid face transfer at 1024x1280. Outdoor scenes with blurred backgrounds are safe first tests. The navy cap from reference carried into output even though prompt also mentioned it - InstantID preserves accessories from reference photo.

---

### Iteration #2 - 2026-02-06 (Phase 1 Fix - Settings Overhaul)

**Reference**: Same as Iteration #1 (Pistachio741_Mixed_Japanese-Br... / Fukushima Larissa)

**Problem Statement**: Output from Iteration #1 scored 3/10 by user - dark face, fake hat, wrong lighting, heavily AI-generated look. Doesn't look like the OG reference at all.

**Root Cause Analysis** (5 issues identified):
1. **InstantID "burn" effect** - Weight too high, over-processing the image
2. **Wrong generation mode** - Using txt2img (empty latent + denoise 1.0) instead of img2img
3. **Prompt fights reference** - Indoor bedroom prompt vs outdoor reference image
4. **CFG too high** - Amplifies AI sharpness and contrast artifacts
5. **Missing IP-Adapter FaceID** - Only using InstantID (structure), missing style/quality transfer

**Changes Made (Phase 1 - Settings Fix)**:

| Setting | Iteration #1 | Iteration #2 | Why |
|---------|-------------|-------------|-----|
| InstantID weight | 0.80 | **0.75** | Community consensus: 0.70-0.80 max. Higher = burn effect |
| CFG | 8.0 | **4.0** | InstantID ceiling is 4.0-4.5. Higher = AI sharpness artifacts |
| Steps | 20 | **35** | More refinement steps, smoother result |
| Resolution | 1024x1280 | **1016x1280** | Avoids SDXL training artifact triggers at exact 1024 |
| Denoise | 1.00 | 1.00 | (Phase 1 stays txt2img; Phase 3 switches to img2img 0.40) |

**ComfyUI Positive Prompt (Rewritten to match OG vibe)**:
```
candid photo of a young mixed Japanese-Brazilian woman, 21, golden olive skin with visible pores and natural texture, dark hair under baseball cap, natural relaxed expression, outdoor setting with trees and greenery, warm natural sunlight, shot on Canon 5D 85mm f1.4, shallow depth of field, Kodak Portra 400 film grain, candid framing, no retouching, slight under-eye shadows, asymmetrical features, realistic skin imperfections
```

**ComfyUI Negative Prompt (Weighted for SDXL)**:
```
(airbrushed:1.4), (smooth skin:1.3), (perfect skin:1.3), (studio lighting:1.2), (professional photo:1.2), (glamour:1.2), (retouched:1.3), (3d render:1.5), (cartoon:1.5), (anime:1.5), (illustration:1.4), (painting:1.4), (symmetrical face:1.2), (stock photo:1.3), (plastic skin:1.4), (waxy:1.3), (oversaturated:1.2), (HDR:1.2), double head, extra limbs, watermark, text, logo
```

**ComfyUI Settings**:
- InstantID weight: 0.75
- InstantID start_at: 0.000, end_at: 1.000
- ControlNet: instantid-controlnet.safetensors
- Checkpoint: realvisxl_v5.safetensors
- KSampler: 35 steps, cfg 4.0, **dpmpp_2m** sampler, **karras** scheduler, denoise 1.00
- Resolution: 1016x1280
- InstantID end_at: 0.90 (let final 10% of steps run without InstantID for more natural look)
- Seed: [TBD - will log after generation]
- NOTE: Do NOT use euler + karras combo (blurry artifacts). DPM++ 2M + Karras is the community standard.

**Output**: [PENDING - needs to be run on ComfyUI]

**User Feedback**:
- Liked: [PENDING]
- Disliked: [PENDING]
- Score: [PENDING] (target: 7/10+, was 3/10)

**If Score < 7/10, Phase 2 Plan**:
- Add IP-Adapter FaceID (IPAdapter Unified Loader FaceID, "PLUS FACE (portraits)")
- IP-Adapter weight: 0.60-0.70
- This adds style/quality transfer from OG image, not just face structure

**If Still < 7/10, Phase 3 Plan**:
- Switch from txt2img to img2img
- Remove Empty Latent Image, add Load Image (OG reference) -> VAE Encode -> KSampler latent_image
- Set denoise to 0.40 (keep 60% of OG quality/composition, change 40%)

**Pattern Extracted**: [PENDING - will extract after testing]
