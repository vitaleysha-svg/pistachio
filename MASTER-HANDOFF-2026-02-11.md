# MASTER HANDOFF - 2026-02-11

## End Goal
- Build a reliable AI influencer pipeline that can produce consistent images and short videos quickly.
- Avoid dependency/debug loops so execution can happen daily with low friction.
- Decide pragmatically between platform-first (Higgsfield) and self-owned API stack.

## Current Reality
- The repeated failures were primarily environment/ops failures, not a core ML impossibility.
- You have enough training data to start now (36 images is enough for a first production model).
- You need velocity today, plus a path to backend ownership later.

## Root Cause Audit (Why iterations were slow)
1. Dependency drift in mutable global Python environment on pod.
2. Script-level hardcoded flags that were fragile in your runtime:
- `--xformers`
- `--persistent_data_loader_workers` with workers effectively zero.
3. Version mismatch between sd-scripts behavior and installed transformers/scheduler enum handling.
4. BLIP-2 auto-caption path added instability (tokenizer/dtype/version edges).
5. Wrapper-level failures (`CalledProcessError`) often hid first root error in logs.
6. Manual partial pastes in terminal created syntax errors and false negatives.

## What was fixed / learned
- Training flow was moved to template captions (`--skip-auto-caption`) to remove BLIP-2 fragility for now.
- Patch approach identified for scheduler compatibility guard in sd-scripts.
- Known bad flags removed from training command where needed.
- Fresh-venv strategy chosen as the stable baseline.

## Known Good Working Strategy
1. Start fresh in new venv.
2. Fresh clone of sd-scripts.
3. Install dependencies in one pass (avoid editable line from sd-scripts requirements if present).
4. Enforce `numpy<2` + compatible opencv package.
5. Remove fragile training flags in retrain script.
6. Train with `--skip-install --skip-auto-caption` and stable template captions.
7. Generate batch outputs after successful training.
8. Convert approved outputs to short-form video.

## Build-vs-Buy Decision (Higgsfield vs DIY)
### Recommendation
- Use Higgsfield for one month for immediate publishing velocity.
- Build your own backend in parallel (clean-room, API-first) for long-term ownership and cost control.

### Why Higgsfield can feel faster
- It abstracts orchestration/model routing/preset logic.
- It reduces manual ops overhead.
- It gives production-ready workflow primitives.

### Why DIY can win long-term
- Full control over infra, cost levers, and data handling.
- Ability to customize deeply with ComfyUI + scripts.
- No dependency on one platform UX/pricing changes.

## ComfyUI Role in the Stack
### Practical hybrid model
1. Pre-production (ComfyUI): identity stills, optional LoRA training, deterministic look control.
2. Production generation (Higgsfield): fast shot/motion generation and iteration.
3. Post-processing (ComfyUI): upscaling/repairs/fixes on selected winners.

### When to train LoRA
- Train LoRA when identity consistency across many scenes is critical and drift is hurting approvals.
- Skip LoRA initially if immediate speed matters more than perfect long-run consistency.

## Midjourney Role
- Good for concept/look ideation and references.
- Not ideal as the core automation backend.

## Credits / Tokens Clarification
- Higgsfield uses credits, not LLM tokens.
- Credits can expire depending on policy/package terms.
- Burn rate depends on model/tool/quality/length settings.

## High-Confidence Next Plan
1. Run a fresh environment pipeline (do not reuse polluted environment).
2. Train one stable LoRA to completion.
3. Generate first publishable image batch.
4. Produce first short-form video.
5. Run 7-day benchmark:
- time-to-publish
- cost per approved output
- approval rate
- identity consistency
6. Decide keep/expand Higgsfield or migrate more workload to owned stack.

## Operational Rules to Prevent Regression
1. One golden environment; no ad-hoc package upgrades mid-run.
2. One full command block at a time; no partial pastes.
3. Capture first failure line before trying fixes.
4. Separate R&D branch from production branch.
5. Keep a single source-of-truth runbook and update it only after verified fixes.

## Key Repo References
- `tools/retrain_lora_v3.py`
- `tools/v3_go.py`
- `tools/generate_batch.py`
- `tools/production_pipeline.py`
- `tools/download_reg_images.py`
- `CODEX-CHANGES.md`
- `CODEX-PHASE2-CHANGES.md`
- `CODEX-PHASE3-CHANGES.md`
- `OPUS-MASTER-HANDOFF-PROMPT.md`

## Recent Local Commits (current branch snapshot seen)
- `c00a45c` Show pip output during dep fix + verify it works
- `97c2a9e` Fix huggingface_hub cached_download ImportError
- `577cc47` Skip BLIP-2 captioning, use template captions instead
- `b25b9a8` Fix: pkill was killing our own training process
- `8402d44` Fix auto-caption and manifest script paths for pod
- `7119c7a` Add realvisxl_v5 to checkpoint detection
- `8784b85` Add one-line pod setup script
- `ff790d1` Add one-command v3 pipeline script for pod

## Resume Prompt (use this when you come back)
"Open `MASTER-HANDOFF-2026-02-11.md`, summarize current state in 10 lines, then execute the fresh-start production runbook only. Do not patch old polluted env. Show me first-failure log lines if anything breaks."
