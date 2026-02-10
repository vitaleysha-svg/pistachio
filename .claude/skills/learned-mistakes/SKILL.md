---
name: learned-mistakes
description: Catalog of repeated failure modes with triggers and prevention rules. Check before acting.
---

# Learned Mistakes Skill

## Usage Rule
Before executing work, scan for matching triggers and apply the linked prevention rule.

## Mistake Catalog

### M1: Skipping session context
- Trigger: first user message in a new session.
- Rule: read goals, patterns, session learnings, and current progress before planning.

### M2: Starting multi-step work without structured loop
- Trigger: request has 3+ steps.
- Rule: use Ralph loop/task tracking, then execute sequentially.

### M3: Context blowup from heavy reads in main thread
- Trigger: reading many long files at once.
- Rule: summarize aggressively and isolate heavy exploration to dedicated passes.

### M4: Overloaded CLAUDE.md always-on context
- Trigger: urge to add large guidance blocks to CLAUDE.md.
- Rule: keep CLAUDE.md lean; move domain content into on-demand skills.

### M5: Incremental dependency fixes causing cascade failures
- Trigger: package/version error chains.
- Rule: solve with one known-compatible pinned set, not one-package-at-a-time patching.

### M6: Dismissing warnings as cosmetic
- Trigger: version mismatch or startup warnings.
- Rule: investigate warnings first; treat as potential root cause.

### M7: Fragile web-terminal command pastes
- Trigger: command is long or multiline.
- Rule: provide uploadable script files (`.py`/`.sh`) instead of paste-heavy instructions.

### M8: Temporary fix instead of durable automation
- Trigger: recurring operational issue.
- Rule: implement permanent startup/check automation immediately.

### M9: Unclear taxonomy when routing info between businesses
- Trigger: content may belong to Pistachio, RedLine Gen, or BMV.
- Rule: map to business objective first; if unclear, ask before saving.

### M10: Generic captions reducing LoRA identity learning
- Trigger: caption files are repetitive templates.
- Rule: generate per-image detailed captions with fixed trigger token.

### M11: Training without regularization images
- Trigger: identity LoRA training plan lacks class images.
- Rule: include regularization data and pass `--reg_data_dir` during training.

### M12: Mixing incompatible training flags
- Trigger: changing optimization/memory flags.
- Rule: verify flag compatibility before launch; prefer tested SDXL presets.

## Maintenance
Add new mistakes immediately with trigger and prevention rule.
