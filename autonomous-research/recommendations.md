# Recommendations

Last updated: 2026-02-10

## Operational Rules (Learned the Hard Way)

### R1: Always use scripts, never terminal commands
**Why:** Web terminal mangles pasted URLs (line breaks), multi-line commands fail silently, and disconnects kill running processes.
**Do:** Write .py scripts, upload via JupyterLab, run with nohup.

### R2: Always pin dependencies with exact versions
**Why:** kohya sd-scripts broke 3 times from unpinned transformers/diffusers/huggingface_hub. Each fix cost 30+ minutes.
**Do:** Use requirements-pod.txt with ==versions. Never bare pip install.

### R3: Always kill ComfyUI before training
**Why:** ComfyUI holds ~8GB VRAM. Training needs full 24GB. Concurrent use causes OOM crashes.
**Do:** Kill ComfyUI process, run training, then restart via fix_and_start.py.

### R4: Always use nohup for operations over 5 minutes
**Why:** Terminal disconnects kill foreground processes. LoRA training takes 30-60 minutes.
**Do:** `nohup python3 script.py > output.log 2>&1 &` then monitor with `tail -f output.log`.

### R5: Always deduplicate training images before LoRA training
**Why:** v1 had 72 images (30 unique + dupes from re-runs). Duplicates biased the model and wasted steps.
**Do:** Run dedup check before training. Target: all unique images, varied poses/angles.

### R6: Always crop reference images to face-only for InstantID
**Why:** InstantID bleeds accessories (hats, glasses) from reference into output. Face-only crop prevents this.
**Do:** Crop to face before using as InstantID reference.

### R7: Always test checkpoint + strength combos via sweep, not manually
**Why:** Manual testing is slow, inconsistent, and misses subtle quality differences. Automated sweep with face similarity scoring is reproducible.
**Do:** Use parameter_sweep_v2.py with InsightFace scoring for all evaluations.

## Strategic Recommendations

### R8: Fix image quality before anything else
**Why:** Platform setup, DM scripts, and content calendar are all blocked by image quality. Current 5-6/10 won't convert.
**Priority:** All engineering effort on LoRA v3 until face match reaches 8+/10.

### R9: Consider alternative base models if v3 still falls short
**Options:** JuggernautXL, LEOSAM HelloWorld XL, or a different RealVisXL version.
**Why:** Base model quality ceiling affects LoRA output ceiling.

### R10: Plan for face-cropped training images as v4 fallback
**Why:** If v3 with full-body training images still struggles with face match, face-cropped images concentrate the model's attention on identity features.
