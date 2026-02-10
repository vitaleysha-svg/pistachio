# CODEX Changes

Date: 2026-02-10
Scope: Implementation of `CODEX-PLAN.md` Tasks 1-4 (local commit only, no push)

## Task 1: Context Optimization

### Rewrote core file
- Replaced `CLAUDE.md` with a lean operating file.
- New size: 44 lines (target was under 120).
- Kept only core identity, principles, startup protocol, autosave protocol, quality bar, do-not rules, and learned-mistakes reminder.

### Moved heavy guidance into skills
Created:
- `.claude/skills/pistachio-workflow/SKILL.md`
- `.claude/skills/life-os-frameworks/SKILL.md`
- `.claude/skills/learned-mistakes/SKILL.md`
- `.claude/skills/interview-protocol/SKILL.md`

### Shrunk template context files
- `context/goals.md` -> 5-line stub
- `context/patterns.md` -> 5-line stub

### Consolidated session learnings
- `context/session-learnings.md` now starts with a 30-rule CRITICAL section.
- Historical detail moved to `context/archive/session-learnings-history.md`.

### Archived stale manual
- Moved `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` -> `archive/operations-manual-v1.md`.

### Startup context footprint (post-change)
- `CLAUDE.md`: 44 lines
- `context/goals.md`: 5 lines
- `context/patterns.md`: 5 lines
- `context/session-learnings.md`: 35 lines
- Total for these files: 89 lines (well below previous 900+ for same set)

## Task 2: Image Pipeline Scripts

Created:
- `tools/auto_caption.py`
- `tools/retrain_lora_v3.py`
- `tools/parameter_sweep_v2.py`

Also added supporting scripts aligned to plan details:
- `tools/download_reg_images.py`
- `tools/backup_workflow.py`

### `tools/auto_caption.py`
- BLIP-2 caption generation for training images.
- Prepends trigger word (default `amiranoor`) to every caption.
- Writes `.txt` sidecar files next to images.
- Supports overwrite, recursive scan, dry-run, and pinned dependency bootstrap.

### `tools/retrain_lora_v3.py`
- Adds regularization data support (`--reg-data-dir`).
- Uses Prodigy optimizer with SDXL-safe defaults.
- Defaults to 2500 steps, `--xformers`, gradient checkpointing.
- Auto-calls `auto_caption.py` before training (unless disabled).
- Writes dataset TOML including train + reg subsets.
- Copies generated `.safetensors` outputs into ComfyUI LoRA folder.

### `tools/parameter_sweep_v2.py`
- Sweeps across:
  - LoRA-only vs LoRA+InstantID mode
  - checkpoints
  - CFG values
  - samplers
  - LoRA strengths
- Runs jobs through ComfyUI API.
- Scores face similarity via InsightFace embeddings against a reference image.
- Exports:
  - `sweep_summary.csv`
  - `top10_by_similarity.csv`
  - `sweep_montage.png`

## Task 3: Missing Automation

Created:
- `tools/requirements-pod.txt`
- `tools/pod_health_check.py`
- `tools/startup_v2.sh`
- `tools/backup_and_download.py`
- `tools/generate_batch.py`

### `tools/requirements-pod.txt`
- Added pinned versions for training/runtime packages including transformers/diffusers/hf-hub compatibility set, insightface stack, and prodigyopt.

### `tools/pod_health_check.py`
Checks:
- ComfyUI API reachability
- Required node classes via `/object_info`
- Required model files presence
- Disk free threshold
- VRAM free threshold (`nvidia-smi`)
- Exit code is non-zero on failure for automation chaining

### `tools/startup_v2.sh`
Flow:
1. Install pinned requirements
2. Pin ComfyUI frontend package
3. Fix DB permissions
4. Ensure InstantID and IPAdapter custom nodes + requirements
5. Run preflight health check
6. Restart ComfyUI and run full health check

### `tools/backup_and_download.py`
Backs up and zips:
- Workflow JSON files
- API history snapshot
- LoRA manifest (name/size/hash)
- Custom node list
- Metadata summary

### `tools/generate_batch.py`
- Reads prompts from file and/or CLI.
- Generates N images per prompt through ComfyUI API.
- Saves deterministic, labeled output filenames.

## Verification Done Locally

- Python syntax check passed:
  - `tools/auto_caption.py`
  - `tools/retrain_lora_v3.py`
  - `tools/parameter_sweep_v2.py`
  - `tools/pod_health_check.py`
  - `tools/backup_and_download.py`
  - `tools/generate_batch.py`
  - `tools/download_reg_images.py`
  - `tools/backup_workflow.py`
- Confirmed manual archived at `archive/operations-manual-v1.md`.
- Confirmed task-specific skills and archive files are present.

## Workflow Breakdown: What Happened and Why Outcomes Missed

## Desired outcome (from project docs)
- Business goal: scale toward `$30k/month` by launching a high-quality, consistent AI persona pipeline.
- Technical target: generated images should be recognizably the same identity with natural skin texture and quality near OG Midjourney references (target >= 7/10).
- Operational target: pod restart to generation-ready with near-zero manual intervention.

## What happened in the last 2 days
- `f379a75` added major technical progress (LoRA v2, sweep, automation docs) but also a large context expansion (+3564 lines).
- `a897e82` added `CODEX-PLAN.md` with clear corrective direction.
- Net effect: execution data improved, but decision/context overhead also increased significantly.

## Why Opus 4.6 performance appeared degraded
- Context overload: too much always-on text (large CLAUDE/session/progress/manual/template files) reduced effective working memory for current tasks.
- Knowledge duplication: same rules and troubleshooting logic spread across CLAUDE, session learnings, progress logs, and KB docs.
- Rule collision: multiple mandatory frameworks competing for the same decision point caused slower, inconsistent task intake.
- Recovery drag: blank template files were still consuming startup context with no actionable signal.

## Why Pistachio output quality missed target
Technical causes:
- Captions were still too generic for identity disentanglement.
- No regularization image integration in prior training pass.
- Model/style mismatch risk remained under-tested across checkpoints/samplers/CFG combinations.
- Face consistency controls were not scored quantitatively during sweeps (manual judgement only).

Operational causes:
- Pod reliability fixes were learned incrementally across sessions, not encoded early into a single startup+healthcheck contract.
- Some fixes existed as knowledge but not as executable scripts, causing repeated manual variance.

## How this change set addresses those gaps
- Context system trimmed and restructured for faster decisions.
- Image training path now includes auto-caption + regularization + Prodigy + xformers in one script.
- Sweep now includes structured parameter matrix plus face similarity scoring output.
- Pod boot path now has pinned dependencies, health checks, and one startup entrypoint.
- Backup and batch generation scripts reduce manual repetition and make workflows reproducible.

## Commit Policy
- Changes were prepared for local commit only.
- No push is performed by this implementation.
