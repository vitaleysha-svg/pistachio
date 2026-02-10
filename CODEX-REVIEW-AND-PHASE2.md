# Codex 5.3 Review + Phase 2 Implementation

## Your Role
You are a senior software engineer auditing and extending a system that was hardened across three commits by two different AI models (Claude Opus 4.6 and Codex). Your job is to:
1. Review what was done and identify gaps
2. Implement Phase 2 from the upskill plan
3. Fix remaining risks
4. Commit locally (do NOT push)

---

## Step 1: Review (Read These First)

Read in this order:
1. `LIFEOS-AUDIT-AND-OPUS-UPSKILL-PLAN.md` - The master plan. You're implementing Phase 2.
2. `CODEX-CHANGES.md` - What Codex already implemented (Phase 0 + partial Phase 1)
3. `PROGRESS.md` - Current operational state
4. `context/projects/pistachio/context.md` - Current stack and priorities
5. `context/session-learnings.md` - Critical rules (30 rules)
6. `CLAUDE.md` - Current operating config (53 lines, lean)

Review these commits for context:
```
git log --oneline -6
```

After reading, write a `CODEX-REVIEW-REPORT.md` with:
- What was done well (keep)
- What was done poorly or incompletely (fix)
- What's missing (build)
- Architecture recommendations

---

## Step 2: Fix Remaining Risks

### Risk 1: v3 Training Scripts Have Untested Dependencies
**Problem:** `tools/retrain_lora_v3.py` references `prodigyopt` and `xformers`. `tools/auto_caption.py` references BLIP-2 via `transformers`. These have never been validated on the RTX 4090 pod environment.

**Fix:** Create `tools/validate_pod_deps.py`:
- Attempts to import every package referenced across all tools/*.py scripts
- Reports which are missing, which versions are wrong
- Outputs a `pip install` command that fixes everything in one shot
- Includes VRAM estimation for BLIP-2 + LoRA training (will they fit on 24GB?)
- Must be uploadable to pod and runnable as: `python3 /workspace/validate_pod_deps.py`

### Risk 2: No Regression Eval Harness (Phase 2 Core)
**Problem:** There's no way to quantitatively measure if LoRA v3 is better than v2. Quality assessment is purely subjective ("does this look right?").

**Fix:** Create `evals/` directory with:

#### `evals/face_similarity_eval.py`
- Takes a directory of generated images + a directory of reference images (training images)
- Uses InsightFace to compute face embeddings for each
- Computes cosine similarity between generated and reference faces
- Outputs per-image scores + mean score + pass/fail against threshold
- Threshold: 0.60 cosine similarity = PASS (adjustable)
- Usage: `python3 evals/face_similarity_eval.py --generated /workspace/sweep_results --reference /workspace/training_images --threshold 0.60`

#### `evals/skin_realism_eval.py`
- Takes generated images
- Computes texture metrics: Laplacian variance (sharpness/detail), color histogram distribution (natural skin tones vs AI-flat)
- Compares against reference image texture metrics
- Outputs: texture_score, color_naturalness_score, overall_realism_score
- This is a heuristic, not perfect, but better than nothing

#### `evals/scorecard.py`
- Runs face_similarity_eval and skin_realism_eval together
- Produces a structured scorecard JSON:
```json
{
  "run_id": "v3_sweep_2026-02-11",
  "timestamp": "2026-02-11T15:00:00Z",
  "lora_version": "v3",
  "face_similarity_mean": 0.72,
  "face_similarity_pass": true,
  "skin_realism_mean": 0.65,
  "overall_grade": "B",
  "images_evaluated": 9,
  "best_config": "step1500_str0.80_cfg4.0",
  "worst_config": "step500_str0.90_cfg4.5"
}
```
- Appends result to `evals/eval_history.jsonl` so we can track improvement over time
- Writes human-readable summary to `evals/latest_report.md`

#### `evals/known_failures.py`
- Regression tests based on actual failures from this project:
  1. **dependency_chain_test**: Verify all pinned deps in `tools/requirements-pod.txt` are mutually compatible (import each, check versions)
  2. **training_flag_test**: Verify that `retrain_lora_v3.py` doesn't use conflicting flags (e.g., --cache_text_encoder_outputs with --text_encoder_lr)
  3. **stale_reference_test**: Verify no active files reference archived/missing paths
  4. **context_budget_test**: Verify startup context stays under 220 lines
  5. **script_syntax_test**: `py_compile` every .py file in tools/ and evals/
- Each test outputs PASS/FAIL
- Exit code is non-zero if any test fails
- Usage: `python3 evals/known_failures.py --project-root .`

### Risk 3: No Structured Logging of Eval Runs
**Problem:** When we run LoRA v3 and evaluate it, there's no persistent memory of what worked and what didn't beyond PROGRESS.md prose.

**Fix:** Create `evals/eval_history.jsonl` (append-only structured log):
- Each line is a JSON object with: run_id, timestamp, lora_version, training_params, eval_scores, notes
- `scorecard.py` appends automatically
- This becomes the ground truth for "what actually improved quality"

### Risk 4: Autonomous Loop Memory Isn't Feeding Back
**Problem:** The autonomous agent runs, writes briefings, but findings don't get promoted into actionable changes.

**Fix:** Create `tools/promote_findings.py`:
- Reads latest briefing from `autonomous-research/briefing-*.md`
- Extracts action items and appends them to `autonomous-research/pending-tasks.md`
- Extracts learnings and appends them to `autonomous-research/memory.md`
- Detects if any finding should update `context/session-learnings.md` CRITICAL rules
- Outputs a diff of what was promoted

---

## Step 3: Architecture Improvements

### Improve the Autonomous Loop Contract
Read `agents/pistachio-agent-v2.md`. It's good but missing:
- **Stop conditions**: When should the agent stop instead of continuing? Add explicit criteria.
- **Failure protocol**: What happens if a tool call fails? Currently undefined.
- **Output validation**: How do we know the briefing is good? Add self-check criteria.

Create `agents/pistachio-agent-v3.md` with these additions.

### Add a Run Orchestrator
Create `tools/run_full_cycle.py`:
- Runs the complete pipeline in order:
  1. Preflight checks (lifeos_preflight.py)
  2. Freshness checks (lifeos_freshness_check.py)
  3. Context budget check (lifeos_context_budget.py)
  4. Known failures regression (evals/known_failures.py)
  5. If all pass: run autonomous agent
  6. After agent: run promote_findings.py
  7. After promote: run eval checks if new images exist
  8. Commit results locally
- Stops on any failure and reports which step failed
- Usage: `python tools/run_full_cycle.py --project-root .`
- Also create `run-full-cycle.ps1` for Windows

---

## Step 4: Commit

After all implementations:
```
git add -A
git commit -m "Phase 2: regression eval harness, structured scoring, autonomous loop maturity"
```

Do NOT push.

Write `CODEX-PHASE2-CHANGES.md` documenting:
- Every file created/modified
- How to run each new tool
- How the eval system works
- What the next phase should be

---

## Constraints
- Do NOT push to GitHub
- Do NOT modify CLAUDE.md (it's already at 53 lines and clean)
- Do NOT modify tools that already pass syntax checks unless fixing bugs
- All Python must pass `py_compile`
- All scripts must be self-contained and uploadable to the pod
- Pin all dependency versions
- Use pathlib for all paths (cross-platform)

## Success Criteria
1. `python evals/known_failures.py --project-root .` passes all 5 tests
2. `evals/face_similarity_eval.py` runs without error when pointed at image directories
3. `evals/scorecard.py` produces valid JSON output
4. `tools/run_full_cycle.py --project-root . --dry-run` completes without error
5. `agents/pistachio-agent-v3.md` has explicit stop conditions and failure protocol
6. All changes committed locally with clear message
