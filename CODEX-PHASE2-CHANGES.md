# CODEX Phase 2 Changes

Date: 2026-02-10  
Scope: `CODEX-REVIEW-AND-PHASE2.md` Steps 1-4

## Summary

Phase 2 is now implemented for regression evaluation, autonomous loop maturity, and findings promotion.

Key outcomes:
- Added quantitative eval harness (`evals/`) for face similarity + skin realism + scorecards.
- Added dependency validation for pod uploads (`tools/validate_pod_deps.py`).
- Added autonomous findings promotion into memory/task artifacts (`tools/promote_findings.py`).
- Added explicit v3 autonomous contract (`agents/pistachio-agent-v3.md`).
- Added one-command full-cycle orchestrator (`tools/run_full_cycle.py`, `run-full-cycle.ps1`).
- Wrote architecture review report (`CODEX-REVIEW-REPORT.md`).

## Files Created

- `CODEX-REVIEW-REPORT.md`
- `CODEX-PHASE2-CHANGES.md`
- `agents/pistachio-agent-v3.md`
- `tools/validate_pod_deps.py`
- `tools/promote_findings.py`
- `tools/run_full_cycle.py`
- `run-full-cycle.ps1`
- `evals/face_similarity_eval.py`
- `evals/skin_realism_eval.py`
- `evals/scorecard.py`
- `evals/known_failures.py`
- `evals/eval_history.jsonl`

## Files Modified

- `tools/requirements-pod.txt`
- Added `xformers==0.0.25.post1` for the training runtime dependency referenced by LoRA v3 scripts.

## How To Run New Tools

1. Validate pod dependencies and VRAM fit:
```bash
python tools/validate_pod_deps.py --project-root .
```
Uploadable pod usage:
```bash
python3 /workspace/validate_pod_deps.py
```

2. Run face similarity eval:
```bash
python evals/face_similarity_eval.py --generated /workspace/sweep_results --reference /workspace/training_images --threshold 0.60
```

3. Run skin realism eval:
```bash
python evals/skin_realism_eval.py --generated /workspace/sweep_results --reference /workspace/training_images --threshold 0.60
```

4. Run full scorecard + history append:
```bash
python evals/scorecard.py --generated /workspace/sweep_results --reference /workspace/training_images --lora-version v3 --run-id v3_sweep_2026-02-11
```

5. Run known failure regressions:
```bash
python evals/known_failures.py --project-root .
```
Strict runtime dependency mode:
```bash
python evals/known_failures.py --project-root . --strict-runtime-deps
```

6. Promote latest autonomous briefing into memory/tasks:
```bash
python tools/promote_findings.py --project-root .
```
Also append candidate critical-rule updates:
```bash
python tools/promote_findings.py --project-root . --apply-critical
```

7. Run full cycle orchestrator:
```bash
python tools/run_full_cycle.py --project-root .
```
Dry-run contract check:
```bash
python tools/run_full_cycle.py --project-root . --dry-run
```
Windows wrapper:
```powershell
powershell -ExecutionPolicy Bypass -File .\run-full-cycle.ps1 -DryRun
```

## Eval System Design

1. `face_similarity_eval.py`
- Computes InsightFace embeddings for generated and reference images.
- Scores each generated image by max cosine similarity to reference set.
- Produces per-image scores + mean + pass/fail at threshold (default `0.60`).

2. `skin_realism_eval.py`
- Computes Laplacian variance (texture/detail proxy) and skin-tone color histogram naturalness.
- Compares generated metrics against reference metrics.
- Outputs `texture_score`, `color_naturalness_score`, and `overall_realism_score`.

3. `scorecard.py`
- Runs both evals, aggregates scores, computes overall grade.
- Writes:
  - `evals/latest_scorecard.json`
  - `evals/latest_report.md`
  - appends structured entry to `evals/eval_history.jsonl`
- Tracks `best_config` and `worst_config` from per-image combined scoring.

4. `known_failures.py`
- Encodes project-specific regression tests:
  - dependency chain
  - training flag conflict check
  - stale reference check
  - context budget check
  - python syntax compilation
- Returns non-zero if any test fails.

## Autonomous Loop Maturity Changes

1. Agent contract upgraded:
- `agents/pistachio-agent-v3.md` now defines:
  - explicit stop conditions
  - explicit failure protocol
  - output validation self-check criteria

2. Feedback loop automation:
- `tools/promote_findings.py` consumes latest `autonomous-research/briefing-*.md`
- promotes actionable tasks to `autonomous-research/pending-tasks.md`
- promotes learnings to `autonomous-research/memory.md`
- detects candidates for `context/session-learnings.md` critical rule updates
- prints diffs of promoted changes

3. Orchestration:
- `tools/run_full_cycle.py` enforces:
  1. preflight
  2. freshness
  3. context budget
  4. known failures
  5. autonomous agent execution
  6. findings promotion
  7. scorecard eval when new images are detected
  8. local git commit
- stops immediately on first failing step

## Verification Performed

- `python -m py_compile tools/validate_pod_deps.py tools/promote_findings.py evals/face_similarity_eval.py evals/skin_realism_eval.py evals/scorecard.py evals/known_failures.py tools/run_full_cycle.py`
- `python evals/known_failures.py --project-root .`
- `python tools/run_full_cycle.py --project-root . --dry-run`

## Next Phase Recommendation

1. Add CI job that runs `evals/known_failures.py` and `tools/run_full_cycle.py --dry-run` on every PR.
2. Add dataset/version identifiers to scorecard entries so eval history lines are fully reproducible.
3. Add threshold policy file (YAML/JSON) so grade logic and pass criteria are centralized and versioned.

