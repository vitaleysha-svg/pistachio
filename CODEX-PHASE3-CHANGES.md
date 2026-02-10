# CODEX Phase 3 Changes

Date: 2026-02-10  
Scope: `CODEX-PHASE3-PLAN.md` Tasks 1-8

## Summary

Phase 3 production-readiness work is implemented:
- CI guardrails workflow is added.
- Threshold policy is centralized and wired into eval/context checks.
- Dataset manifest/versioning is added and integrated into LoRA training + scorecard metadata.
- Version comparison reporting is added.
- Production batch pipeline is added (health -> generate -> eval -> filter -> report).
- RunPod cost tracking is added and integrated into the full-cycle orchestrator.
- Known-failure regressions were extended with threshold policy and manifest integrity tests.

## Files Created

- `.github/workflows/guardrails.yml`
- `evals/thresholds.yaml`
- `evals/load_thresholds.py`
- `evals/compare_versions.py`
- `tools/dataset_manifest.py`
- `tools/production_pipeline.py`
- `tools/runpod_cost_tracker.py`
- `tools/cost_log.jsonl`
- `CODEX-PHASE3-CHANGES.md`

## Files Modified

- `evals/face_similarity_eval.py`
- `evals/skin_realism_eval.py`
- `evals/scorecard.py`
- `evals/known_failures.py`
- `tools/lifeos_context_budget.py`
- `tools/lifeos_freshness_check.py`
- `tools/retrain_lora_v3.py`
- `tools/run_full_cycle.py`
- `run-full-cycle.ps1`
- `tools/requirements-pod.txt`
- `tools/validate_pod_deps.py`

## Task-by-Task Implementation

### Task 1: CI Guardrails Workflow
- Added `.github/workflows/guardrails.yml` with:
  - known failures regression
  - context budget check
  - preflight check
  - freshness check
- CI trigger:
  - push to `main`
  - pull requests to `main`
- Freshness CI edge-case handling:
  - `tools/lifeos_freshness_check.py` now supports `--skip-in-ci`
  - when `CI=true` and `--skip-in-ci` is passed, mtime-based freshness is skipped with a PASS message
  - this avoids false confidence from fresh checkout mtimes

### Task 2: Threshold Policy File + Loader
- Added policy file: `evals/thresholds.yaml`
- Added loader: `evals/load_thresholds.py`
  - primary parser: `yaml.safe_load()`
  - fallback parser + hardcoded defaults if YAML is unavailable/missing
- Wired policy into:
  - `evals/face_similarity_eval.py`
  - `evals/skin_realism_eval.py`
  - `evals/scorecard.py`
  - `tools/lifeos_context_budget.py`
- CLI precedence preserved exactly as required:
  - CLI args override YAML values
  - YAML overrides hardcoded defaults

### Task 3: Dataset Manifest and Versioning
- Added `tools/dataset_manifest.py`
  - generates manifest JSON with image SHA256, caption SHA256, dimensions, caption text, summary distribution
  - supports compare mode:
    - images added/removed
    - image content hash changes
    - caption hash changes
    - resolution changes
- Integrated into training:
  - `tools/retrain_lora_v3.py` now auto-generates manifest before training starts
  - default manifest output is `{output_dir}/dataset_manifest.json`
- Scorecard linkage:
  - `evals/scorecard.py` now records:
    - `dataset_manifest_path`
    - `dataset_manifest_hash`
  - these fields are also appended into `evals/eval_history.jsonl`

### Task 4: Version Comparison Tool
- Added `evals/compare_versions.py`
  - compares two runs from `evals/eval_history.jsonl`
  - outputs side-by-side markdown report with deltas/verdicts
  - includes promotion recommendation based on threshold policy minimum grade
  - supports exact run ID or substring matching

### Task 5: Production Batch Pipeline
- Added `tools/production_pipeline.py`
- End-to-end flow implemented:
  1. health check (`tools/pod_health_check.py`)
  2. prompt load (file or built-in default prompt set)
  3. generation (`tools/generate_batch.py`)
  4. face eval (`evals/face_similarity_eval.py`)
  5. skin eval (`evals/skin_realism_eval.py`)
  6. scorecard (`evals/scorecard.py`)
  7. quality filter to `approved/` and `rejected/`
  8. report generation (`batch_report.md`, `batch_report.json`)
- Report includes:
  - generated/approved/rejected counts
  - mean approved scores
  - best/worst samples
  - settings used (LoRA, strength, CFG, sampler, steps)

### Task 6: Cost Tracker
- Added `tools/runpod_cost_tracker.py`
  - `--action start`
  - `--action stop`
  - `--action report`
- Default append-only log:
  - `tools/cost_log.jsonl`
- Features:
  - configurable rate per hour (default `$0.60`)
  - activity tags
  - open-session detection on start
  - aggregate report by activity

### Task 7: Orchestrator + Known Failures Extensions

#### `tools/run_full_cycle.py` extensions
- Added cost tracking start/stop around autonomous agent step.
- Added optional dataset manifest generation step:
  - `--training-dataset-dir`
  - `--training-output-dir`
  - `--dataset-manifest-out`
- Added optional version comparison after scorecard:
  - `--compare-with-run-id`
- Added optional production trigger:
  - `--run-production` plus production args

#### `evals/known_failures.py` extensions
- Added `threshold_policy_test`:
  - verifies `evals/thresholds.yaml` exists
  - validates YAML parsing
  - validates required sections/keys
- Added `dataset_manifest_test`:
  - if a manifest exists, verifies image/caption hash integrity
  - detects corrupted or mismatched data references

### Task 8: Commit + Documentation
- This document (`CODEX-PHASE3-CHANGES.md`) is written.
- All Phase 3 files are committed locally (no push).

## How To Run Each New Tool

1. Guardrails locally:
```bash
python evals/known_failures.py --project-root .
python tools/lifeos_context_budget.py --project-root .
python tools/lifeos_preflight.py --project-root .
python tools/lifeos_freshness_check.py --project-root . --max-age-days 7
```

2. Load merged threshold policy:
```bash
python evals/load_thresholds.py --project-root .
```

3. Create dataset manifest:
```bash
python tools/dataset_manifest.py --dataset-dir /workspace/lora_dataset_v3/10_amiranoor --output /workspace/lora_output_v3/dataset_manifest.json
```

4. Compare manifests:
```bash
python tools/dataset_manifest.py --compare manifest_v2.json manifest_v3.json
```

5. Compare versions:
```bash
python evals/compare_versions.py --history evals/eval_history.jsonl --v1 v2_sweep --v2 v3_sweep --output evals/comparison_report.md
```

6. Run production pipeline:
```bash
python tools/production_pipeline.py --workflow /workspace/workflow_api.json --lora amiranoor_v3.safetensors --count 5 --output-dir /workspace/production_batch_001 --reference-dir /workspace/lora_dataset_v3/10_amiranoor
```

7. Run cost tracker:
```bash
python tools/runpod_cost_tracker.py --action start --activity lora_v3_training
python tools/runpod_cost_tracker.py --action stop
python tools/runpod_cost_tracker.py --action report
```

8. Run full cycle:
```bash
python tools/run_full_cycle.py --project-root . --dry-run
```

## CI Workflow Trigger Details

- File: `.github/workflows/guardrails.yml`
- Trigger events:
  - `push` on `main`
  - `pull_request` on `main`
- CI freshness behavior:
  - uses `--skip-in-ci` to avoid misleading mtime freshness checks in clean checkouts

## Threshold Policy Cascade

- Single source: `evals/thresholds.yaml`
- Loader: `evals/load_thresholds.py`
- Consumed by:
  - face eval default threshold
  - skin eval default thresholds
  - scorecard grade boundaries + promotion minimum
  - context budget line limits

## Dataset Manifests and LoRA Output Link

- `tools/retrain_lora_v3.py` now writes `{output_dir}/dataset_manifest.json` before training.
- `evals/scorecard.py` can ingest the manifest and stores `dataset_manifest_hash` in history entries.
- This enables traceability from scored outputs back to exact dataset state.

## Production Pipeline End-to-End

- Health gate first.
- Batch generation next.
- Quantitative evals applied immediately.
- Automatic pass/fail filtering into `approved/` and `rejected/`.
- Batch-level report generated for operational decisions.

## Cost Tracking Integration with Orchestrator

- `tools/run_full_cycle.py` starts cost tracking before autonomous agent execution.
- It stops cost tracking in a guarded `finally` block after agent execution.
- This captures autonomous-loop runtime cost automatically per cycle.

## Verification Performed

- `python -m py_compile` on all modified/new Phase 3 Python files: PASS
- `python evals/known_failures.py --project-root .`: PASS (including new test cases)
- `python tools/run_full_cycle.py --project-root . --dry-run`: PASS
- `powershell -ExecutionPolicy Bypass -File .\run-full-cycle.ps1 -DryRun`: PASS
- `python tools/runpod_cost_tracker.py --action report`: PASS
- `python evals/compare_versions.py` smoke test with sample history: PASS

## Phase 4 Recommendation

1. Add CI matrix job that validates both Linux and Windows wrappers (`run-full-cycle.ps1`, shell launcher parity).
2. Add deterministic fixture dataset + synthetic image set for automated eval unit tests.
3. Add promotion automation:
  - auto-open PR/issue when scorecard grade crosses promotion threshold.
4. Add cost anomaly alerts:
  - warn when idle cost exceeds configured daily budget.

