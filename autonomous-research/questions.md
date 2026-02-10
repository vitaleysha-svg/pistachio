# Open Questions

Last updated: 2026-02-10

## Technical Questions (LoRA / Image Pipeline)

### Q1: Is RealVisXL v5 the best base model for this use case?
**Context:** All training so far used RealVisXL. Other SDXL checkpoints (JuggernautXL, LEOSAM HelloWorld XL) may produce better skin texture or face structure for this persona.
**How to answer:** Train a quick LoRA on JuggernautXL, compare face similarity scores against RealVisXL.

### Q2: Would face-cropped training images improve LoRA face match?
**Context:** Current 36 training images are mixed (close-up, three-quarter, full body). Face identity is diluted across body/scene features. Face-only crops would concentrate training on identity.
**How to answer:** Crop existing 36 images to face-only, retrain, compare.

### Q3: Is network_dim 16 too low for identity capture?
**Context:** Dropped from 32 to 16 to free VRAM for text encoder. But lower dim = less model capacity. v2 quality issues may partly be underfitting.
**How to answer:** v3 sweep should test dim 16 vs dim 32 if VRAM allows with Prodigy optimizer.

### Q4: Should we use a face-specific loss function instead of standard MSE?
**Context:** Standard training loss treats all pixels equally. Face-weighted loss or perceptual loss could prioritize identity features.
**How to answer:** Research if kohya sd-scripts supports custom loss, or if any fork does.

### Q5: Will Prodigy optimizer work well with SDXL LoRA on 24GB VRAM?
**Context:** Prodigy has higher memory overhead than AdamW8bit due to internal state tracking. May cause OOM on RTX 4090.
**How to answer:** Monitor VRAM during first v3 training run. If OOM, fall back to AdamW8bit.

## Strategic Questions

### Q6: Is 36 images enough training data for a high-quality SDXL LoRA?
**Context:** Some guides recommend 50-100 images for SDXL. Others say 20-30 is fine with good captions. v2 used 36 deduped.
**How to answer:** If v3 quality is still low, generate more Midjourney training images.

### Q7: Should we add video frames as training data?
**Context:** If we generate video with Wan2.2 later, having video-frame-style training data could improve consistency across modalities.
**How to answer:** Defer until after v3 results are evaluated.

### Q8: At what face similarity score is quality "production ready"?
**Context:** parameter_sweep_v2.py will output InsightFace cosine similarity scores. Need to define the threshold for "good enough" vs "needs more training."
**How to answer:** Generate known-good reference pairs, measure their similarity, use as baseline.
