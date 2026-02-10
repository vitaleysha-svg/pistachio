# Pistachio Agent Long-Term Memory

Last updated: 2026-02-10

## What Works (Keep Doing)
- Scripts over terminal commands: nohup + .py files survive disconnects, terminal mangles pasted URLs
- Pin ALL dependencies for kohya sd-scripts: transformers==4.38.2, diffusers==0.25.1, huggingface_hub==0.21.4
- Kill ComfyUI before training (VRAM conflict on 24GB GPU)
- Use nohup for any operation over 5 minutes (training, downloads)
- Permanent fixes via startup.sh + post_start.sh hook -- stops recurring "custom nodes missing" on reboot
- Jupyter notebooks bypass terminal paste corruption issues
- Same seed across sweep for fair comparison (seed 42424242)

## What Doesn't Work (Stop Doing)
- UNet-only LoRA training: v1 was UNet-only, face didn't match. Must train BOTH UNet + Text Encoder
- Duplicate images in dataset: v1 had 72 images (30 originals + dupes), hurt quality
- Identical captions across all images: v1 used same caption everywhere, no identity disentanglement
- Manual-only sweep evaluation: no quantitative face similarity scoring, judgement was inconsistent
- Pasting multi-line commands in web terminal: line breaks corrupt commands silently
- Installing packages without version pins: dependency hell every time

## Learned Patterns
- LoRA quality progression: v1 (UNet-only, dupes, generic captions) -> v2 (UNet+TE, deduped, varied captions) -> v3 planned (auto-captions, regularization, Prodigy optimizer)
- Pod restarts wipe custom node state unless hooked into post_start.sh
- ComfyUI frontend package version matters: pin to known-good version
- SQLite DB permissions break on pod restart -- fix_and_start.py handles this
- network_dim 16 frees VRAM for text encoder training (down from 32)
- InstantID bleeds accessories from reference photos (hats, glasses) -- crop to face-only

## Run History

| Date | Key Insight | Acted On? | Notes |
|------|-------------|-----------|-------|
| 2026-02-07 | InstantID + IPAdapter combo works for face consistency | Yes | Phase 2 validated |
| 2026-02-08 | MJ automation = permanent ban risk | Yes | Manual generation only |
| 2026-02-09 | Custom nodes vanish on pod restart | Yes | Created startup.sh hook |
| 2026-02-10 | LoRA v1 failed: UNet-only + dupes + generic captions | Yes | Trained v2 with fixes |
| 2026-02-10 | v2 sweep showed quality still insufficient | Yes | Codex created v3 pipeline |
| 2026-02-10 | Context overload degraded Claude performance | Yes | CLAUDE.md trimmed to 53 lines |
