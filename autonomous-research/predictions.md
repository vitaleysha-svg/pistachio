# Predictions

Last updated: 2026-02-10

## Technical Predictions

### P1: v3 with auto-captions + regularization will significantly improve face match
**Confidence:** 7/10
**Reasoning:** v2 failed primarily due to generic captions and no regularization. BLIP-2 per-image captions + prior preservation regularization are the two most impactful fixes for identity disentanglement. Both are addressed in v3.
**If wrong:** Try face-cropped training images, different base model, or higher network_dim.

### P2: Prodigy optimizer will auto-tune better than AdamW8bit
**Confidence:** 6/10
**Reasoning:** Prodigy auto-adjusts learning rate, removing manual LR tuning. AdamW8bit required careful LR selection (1e-4 UNet, 1e-5 TE). Less tuning = fewer failed runs.
**If wrong:** Fall back to AdamW8bit with known-good LR from v2.

### P3: InsightFace scoring will surface combos manual review missed
**Confidence:** 8/10
**Reasoning:** v1 sweep was manual-only. Quantitative face embedding similarity will catch subtle differences humans miss, especially across 50+ parameter combinations.
**If wrong:** Face similarity metric may not correlate with perceived quality -- add CLIP aesthetic score as backup.

### P4: 2500 steps will be the sweet spot for v3
**Confidence:** 5/10
**Reasoning:** v2 at 2000 steps had loss 0.116 and still underfitting on identity. Extra 500 steps + better data should converge. But overfitting risk increases.
**If wrong:** Use checkpoint comparison from sweep to find actual sweet spot.

## Business Predictions

### P5: $30K in 60 days is achievable only if image quality reaches 8+/10
**Confidence:** 4/10
**Reasoning:** Current image quality (~5-6/10) won't convert. Need face consistency at 8+/10 for believable persona. Technical pipeline is the actual bottleneck to revenue.

### P6: PPV will outperform subscription revenue 2:1
**Confidence:** 7/10
**Reasoning:** Industry pattern -- base subscription drives volume, PPV/customs drive margin. Fanvue's PPV system is built for this.

## Tracking

| Prediction | Status | Outcome |
|------------|--------|---------|
| P1 | Pending -- awaiting v3 training | |
| P2 | Pending -- awaiting v3 training | |
| P3 | Pending -- awaiting sweep v2 | |
| P4 | Pending -- awaiting v3 training | |
| P5 | Pending -- awaiting launch | |
| P6 | Pending -- awaiting launch | |
