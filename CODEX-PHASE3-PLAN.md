# Codex 5.3 Phase 3: Production Readiness

## Context

You are extending a system that has been through 3 phases of hardening:
- **Phase 0** (commit `0030730`): Portable launcher, source-of-truth refresh
- **Phase 1** (commit `fe6baa6`): Preflight, freshness, context budget guardrails
- **Phase 2** (commit `e33d19b`): Regression eval harness, structured scoring, autonomous loop maturity

Phase 3 makes the system **production-ready**: CI enforcement, dataset reproducibility, version comparison, end-to-end production pipeline, and cost tracking.

## Read Order (Before Writing Any Code)

1. `CODEX-PHASE2-CHANGES.md` - What Phase 2 built (eval harness, orchestrator, promote_findings)
2. `CODEX-REVIEW-REPORT.md` - Architecture recommendations from Phase 2 review
3. `LIFEOS-AUDIT-AND-OPUS-UPSKILL-PLAN.md` - Master upskill plan (Phase 3 section)
4. `PROGRESS.md` - Current operational state
5. `context/projects/pistachio/context.md` - Current stack and priorities
6. `evals/known_failures.py` - Existing regression tests (extend, don't replace)
7. `tools/run_full_cycle.py` - Existing orchestrator (extend, don't replace)
8. `evals/scorecard.py` - Existing scoring system (extend, don't replace)

Also review:
```
git log --oneline -8
```

---

## Task 1: CI Guardrails Workflow

### Problem
All guardrails currently require manual execution. A bad commit can break context budget, introduce stale references, or fail syntax checks with no automated warning.

### Implementation

Create `.github/workflows/guardrails.yml`:

```yaml
name: LifeOS Guardrails
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  guardrails:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run known failures regression
        run: python evals/known_failures.py --project-root .
      - name: Run context budget check
        run: python tools/lifeos_context_budget.py --project-root .
      - name: Run preflight check
        run: python tools/lifeos_preflight.py --project-root .
      - name: Run freshness check
        run: python tools/lifeos_freshness_check.py --project-root . --max-age-days 14
        # Relaxed to 14 days for CI since autonomous loop may not run daily
```

**Verification:** Push a test branch, confirm all 4 checks run and pass in GitHub Actions.

**Edge case:** Freshness check uses file modification time which resets on checkout. If `lifeos_freshness_check.py` uses `os.path.getmtime()`, it will always pass in CI because checkout is fresh. Check the implementation:
- If it uses git commit dates: fine
- If it uses filesystem mtime: add a `--skip-in-ci` flag or detect `CI` env var and skip freshness in CI context
- Document which approach you chose in the changes doc

---

## Task 2: Threshold Policy File

### Problem
Pass/fail thresholds are hardcoded across multiple eval scripts (face_similarity_eval.py defaults to 0.60, skin_realism_eval.py has its own defaults, scorecard.py has grade boundaries). Changing a threshold requires editing multiple files.

### Implementation

Create `evals/thresholds.yaml`:
```yaml
# Centralized pass/fail policy for all evals
# Edit this file to adjust quality gates - all eval scripts read from here

face_similarity:
  pass_threshold: 0.60
  warn_threshold: 0.50
  metric: cosine_similarity
  description: "InsightFace embedding cosine similarity between generated and reference faces"

skin_realism:
  texture_pass_threshold: 0.60
  color_naturalness_pass_threshold: 0.55
  overall_pass_threshold: 0.60
  description: "Laplacian variance + skin-tone histogram comparison"

scorecard:
  grade_boundaries:
    A: 0.85
    B: 0.70
    C: 0.55
    D: 0.40
    F: 0.0
  promotion_minimum_grade: "C"
  description: "Combined face similarity + skin realism weighted average"

context_budget:
  claude_md_max_lines: 120
  goals_max_lines: 10
  patterns_max_lines: 10
  session_learnings_max_lines: 80
  total_max_lines: 220

freshness:
  max_age_days: 7
  ci_max_age_days: 14
```

Create `evals/load_thresholds.py`:
- Reads `evals/thresholds.yaml` using `yaml.safe_load()` (add `pyyaml` to requirements if not present)
- Returns a dict
- Falls back to hardcoded defaults if YAML is missing (for backward compat)
- Used by face_similarity_eval.py, skin_realism_eval.py, scorecard.py, lifeos_context_budget.py

**Modify** these existing files to import from `load_thresholds.py` instead of using hardcoded values:
- `evals/face_similarity_eval.py` - use `thresholds['face_similarity']['pass_threshold']`
- `evals/skin_realism_eval.py` - use `thresholds['skin_realism']` values
- `evals/scorecard.py` - use `thresholds['scorecard']['grade_boundaries']`
- `tools/lifeos_context_budget.py` - use `thresholds['context_budget']` values

**Do NOT break existing CLI `--threshold` arguments.** CLI args override YAML values. Priority: CLI arg > YAML file > hardcoded default.

---

## Task 3: Dataset Manifest and Versioning

### Problem
There's no way to know which exact training images and captions produced a given LoRA. If training images change, there's no record of the previous set. Makes A/B comparison unreliable.

### Implementation

Create `tools/dataset_manifest.py`:

```
Usage: python tools/dataset_manifest.py --dataset-dir /workspace/lora_dataset_v2 --output manifest.json
```

Output (`manifest.json`):
```json
{
  "manifest_version": 1,
  "created": "2026-02-11T15:00:00Z",
  "dataset_dir": "/workspace/lora_dataset_v2",
  "total_images": 36,
  "total_captions": 36,
  "images": [
    {
      "filename": "img_001.png",
      "sha256": "abc123...",
      "size_bytes": 1048576,
      "dimensions": [1024, 1024],
      "caption_file": "img_001.txt",
      "caption_text": "amiranoor, a young woman, close up portrait, photorealistic",
      "caption_sha256": "def456..."
    }
  ],
  "summary": {
    "unique_captions": 5,
    "caption_distribution": {
      "amiranoor, a young woman, close up portrait, photorealistic": 8,
      "amiranoor, a young mixed heritage woman, natural lighting, photo": 7
    },
    "mean_image_size_bytes": 1048576,
    "resolution_set": ["1024x1024"]
  }
}
```

Features:
- SHA256 hash of each image and caption for exact reproducibility
- Caption distribution analysis (catches the "all identical captions" problem)
- Resolution verification (catches mixed resolution issues)
- Can compare two manifests: `python tools/dataset_manifest.py --compare manifest_v2.json manifest_v3.json`
- Comparison outputs: images added/removed/changed, captions changed, resolution changes

**Integration:** Modify `tools/retrain_lora_v3.py` to:
- Auto-generate manifest before training starts
- Save manifest alongside the LoRA output as `{output_dir}/dataset_manifest.json`
- Include manifest hash in scorecard entries

---

## Task 4: Version Comparison Tool

### Problem
After training LoRA v3, there's no structured way to compare it against v2. Currently it's "look at images and guess." The eval harness scores individual runs but doesn't compare across versions.

### Implementation

Create `evals/compare_versions.py`:

```
Usage: python evals/compare_versions.py --history evals/eval_history.jsonl --v1 v2_sweep --v2 v3_sweep
```

Output (`evals/comparison_report.md`):
```markdown
# Version Comparison: v2_sweep vs v3_sweep

| Metric | v2_sweep | v3_sweep | Delta | Verdict |
|--------|----------|----------|-------|---------|
| Face Similarity (mean) | 0.52 | 0.71 | +0.19 | IMPROVED |
| Skin Realism (mean) | 0.48 | 0.67 | +0.19 | IMPROVED |
| Overall Grade | D | B | +2 levels | IMPROVED |
| Best Config | step1500_str0.80 | step2000_str0.75 | - | - |

## Recommendation
v3_sweep meets promotion threshold (grade >= C). Recommend deploying v3 LoRA.

## Config Details
- v2: network_dim=16, UNet+TE, AdamW8bit, 2000 steps, generic captions
- v3: network_dim=32, UNet+TE, Prodigy, 2500 steps, BLIP-2 auto-captions + regularization
```

Features:
- Reads from `eval_history.jsonl` (structured log from scorecard.py)
- Side-by-side comparison with delta and verdict per metric
- Automatic promotion recommendation based on threshold policy
- Can compare any two run_ids in history
- If no history exists, outputs instructions for how to generate scores first

---

## Task 5: Production Batch Pipeline

### Problem
Going from "LoRA is trained" to "50 production images ready" is still manual: start ComfyUI, load workflow, type prompts, queue one at a time. `tools/generate_batch.py` exists but isn't integrated with evals or quality gates.

### Implementation

Create `tools/production_pipeline.py`:

```
Usage: python tools/production_pipeline.py --prompts prompts.txt --lora amiranoor_v3.safetensors --count 5 --output-dir /workspace/production_batch_001
```

Pipeline steps (in order):
1. **Health check** - Verify ComfyUI is running, required models present (calls `pod_health_check.py` logic)
2. **Load prompts** - Read from file or use built-in defaults
3. **Generate batch** - Call ComfyUI API for each prompt x count combination (calls `generate_batch.py` logic)
4. **Run face eval** - Score all generated images against reference set
5. **Run skin eval** - Score skin realism
6. **Generate scorecard** - Produce combined score and grade
7. **Filter** - Move images below threshold to `rejected/` subfolder, keep passing images in `approved/`
8. **Report** - Write `batch_report.md` with:
   - Total generated, approved, rejected counts
   - Mean scores for approved set
   - Best and worst images with scores
   - Settings used (LoRA, strength, CFG, sampler)

Built-in prompt templates (for when `--prompts` is not provided):
```
amiranoor, candid photo at outdoor cafe, golden hour, shot on Canon 5D 85mm, shallow dof
amiranoor, sitting on park bench, autumn leaves, natural sunlight, casual outfit
amiranoor, walking down city street, golden hour, candid shot, urban background
amiranoor, close up portrait, soft window light, indoor, natural expression
amiranoor, beach sunset, looking at camera, warm tones, wind in hair
amiranoor, restaurant table, evening lighting, elegant outfit, candid framing
amiranoor, rooftop terrace, city skyline, magic hour, lifestyle photo
amiranoor, garden setting, morning light, floral dress, natural pose
amiranoor, coffee shop window seat, rainy day, cozy lighting, reading
amiranoor, poolside, bright midday sun, swimwear, vacation candid
```

**This script is designed to run on the pod.** Include all necessary imports and handle ComfyUI API connection.

---

## Task 6: Cost Tracker

### Problem
No visibility into how much RunPod time and money is being spent. User is paying ~$0.60/hr for RTX 4090. Training takes ~45 min. Generation takes ~8 sec per image. No aggregate tracking.

### Implementation

Create `tools/runpod_cost_tracker.py`:

```
Usage: python tools/runpod_cost_tracker.py --action start   # Start timing
       python tools/runpod_cost_tracker.py --action stop    # Stop timing, log session
       python tools/runpod_cost_tracker.py --action report  # Show cost summary
```

Data file: `tools/cost_log.jsonl` (append-only):
```json
{"session_id": "2026-02-11_001", "start": "2026-02-11T15:00:00Z", "end": "2026-02-11T16:15:00Z", "duration_min": 75, "activity": "lora_v3_training", "cost_usd": 0.75, "gpu": "RTX 4090", "rate_per_hr": 0.60}
```

Report output:
```
=== RunPod Cost Report ===
Total sessions: 12
Total hours: 18.5
Total cost: $11.10
By activity:
  LoRA training: 3 sessions, 2.25 hrs, $1.35
  Generation: 6 sessions, 1.5 hrs, $0.90
  ComfyUI idle: 3 sessions, 14.75 hrs, $8.85
```

Features:
- Configurable GPU rate (default $0.60/hr for RTX 4090)
- Activity tagging (training, generation, idle, setup)
- JSON Lines for easy parsing
- Running total across all sessions
- Can detect if a session was never stopped (warn on `--action start` if previous session still open)

**Integration:** `tools/run_full_cycle.py` should auto-start/stop cost tracking around the autonomous agent step.

---

## Task 7: Update Orchestrator and Known Failures

### Extend `tools/run_full_cycle.py`:
Add steps for:
- Cost tracking start/stop around agent execution
- Dataset manifest generation after training
- Version comparison after new scorecard is generated
- Production pipeline trigger (optional, with `--run-production` flag)

### Extend `evals/known_failures.py`:
Add test case:
- `threshold_policy_test`: Verify `evals/thresholds.yaml` exists, is valid YAML, contains all required keys
- `dataset_manifest_test`: If a manifest exists in latest training output, verify all referenced images have matching hashes (detect data corruption)

---

## Task 8: Commit and Document

```
git add -A
git commit -m "Phase 3: CI, threshold policy, dataset versioning, production pipeline, cost tracking"
```

Do NOT push.

Write `CODEX-PHASE3-CHANGES.md` documenting:
- Every file created/modified with purpose
- How to run each new tool (exact commands)
- How the CI workflow triggers
- How threshold policy cascades into eval scripts
- How dataset manifests link to LoRA outputs
- How the production pipeline end-to-end flow works
- How cost tracking integrates with the orchestrator
- What Phase 4 should focus on (your recommendation)

---

## Constraints

- Do NOT push to GitHub
- Do NOT modify `CLAUDE.md` (53 lines, clean)
- Do NOT modify `PROGRESS.md` (46 lines, clean)
- Do NOT modify `context/session-learnings.md` (37 lines, clean)
- Do NOT break any existing passing tests (`known_failures.py`, `lifeos_preflight.py`, `lifeos_freshness_check.py`, `lifeos_context_budget.py`)
- All Python must pass `python -m py_compile`
- All paths must use `pathlib` (cross-platform)
- Pin all new dependency versions
- Existing CLI interfaces must not break (backward compat)
- CLI args always override YAML config which overrides hardcoded defaults

## Success Criteria

1. `.github/workflows/guardrails.yml` is valid GitHub Actions syntax
2. `evals/thresholds.yaml` exists with all required sections
3. `evals/load_thresholds.py` works and all eval scripts use it (with CLI override preserved)
4. `tools/dataset_manifest.py` produces valid JSON with SHA256 hashes
5. `evals/compare_versions.py` produces a readable markdown comparison
6. `tools/production_pipeline.py` chains health check → generate → eval → filter → report
7. `tools/runpod_cost_tracker.py` start/stop/report cycle works
8. `python evals/known_failures.py --project-root .` still passes (including new test cases)
9. `python tools/run_full_cycle.py --project-root . --dry-run` still passes
10. All changes committed locally with clear message
11. `CODEX-PHASE3-CHANGES.md` documents everything
