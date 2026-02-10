# CODEX Review Report

Date: 2026-02-10  
Scope: Phase 2 readiness audit of LifeOS + Pistachio operating layer

## 1) What Was Done Well (Keep)

1. **Context collapse was successful.**
- `CLAUDE.md` is now lean and focused on operating rules.
- High-noise material was moved out of startup into skills and archive paths.

2. **Portable launch path exists now.**
- `run-pistachio-agent.ps1` and `run-pistachio-agent.sh` removed machine-specific path assumptions.
- Guardrails are integrated before autonomous execution.

3. **Phase 1 guardrails are concrete and executable.**
- `tools/lifeos_preflight.py`, `tools/lifeos_freshness_check.py`, and `tools/lifeos_context_budget.py` converted policy into checks.
- This materially reduces hidden drift risk.

4. **Core LoRA v3 scripts were created.**
- `tools/auto_caption.py`, `tools/retrain_lora_v3.py`, and `tools/parameter_sweep_v2.py` cover key workflow stages.
- `tools/requirements-pod.txt` pins a baseline package set.

5. **Operational intent is clear in project context docs.**
- `PROGRESS.md`, `context/projects/pistachio/context.md`, and `context/session-learnings.md` are now concise and actionable.

## 2) What Was Done Poorly / Incompletely (Fix)

1. **No dependency validation gate existed for pod deployment.**
- Training and eval scripts reference heavy dependencies (`insightface`, `transformers`, `prodigyopt`, `xformers`-adjacent stack) without a single compatibility validator.

2. **No quantitative regression harness existed.**
- Output quality decisions remained mostly subjective.
- There was no required pass/fail score layer between v2 and v3.

3. **Autonomous memory loop was still weakly connected to execution.**
- Agent outputs were generated, but promotion into pending tasks, memory, and critical rules was not automated.

4. **Autonomous contract lacked strict controls.**
- `agents/pistachio-agent-v2.md` did not define explicit stop conditions, failure protocol, or output self-validation criteria.

5. **No single orchestrator for end-to-end cycle existed.**
- Guardrails, autonomous execution, memory promotion, evaluation, and commit were separate manual steps.

## 3) What Is Missing (Build)

1. `tools/validate_pod_deps.py` for pod dependency compatibility + version correction command + VRAM fit estimate.
2. Full `evals/` harness:
- `evals/face_similarity_eval.py`
- `evals/skin_realism_eval.py`
- `evals/scorecard.py`
- `evals/known_failures.py`
- `evals/eval_history.jsonl`
3. `tools/promote_findings.py` to close the autonomous memory feedback loop.
4. `agents/pistachio-agent-v3.md` with bounded loop contract.
5. `tools/run_full_cycle.py` and `run-full-cycle.ps1` for one-command repeatable execution.

## 4) Architecture Recommendations

1. **Adopt a strict control-plane / data-plane split.**
- Control-plane files: `CLAUDE.md`, `context/session-learnings.md`, `context/projects/pistachio/context.md`, agent contract.
- Data-plane files: eval outputs, sweep outputs, autonomous briefings, score history.
- Keep control-plane docs small and deterministic; keep volatile details in logs and artifacts.

2. **Treat evals as release criteria, not optional diagnostics.**
- Every model iteration should produce a scorecard record in `evals/eval_history.jsonl`.
- Promotion to production should require passing threshold policy (face similarity + realism floor).

3. **Promote autonomous findings through explicit reducers.**
- Agent output should never be the final state.
- Promotion script should translate briefing text into durable memory and actionable task queues.

4. **Enforce hard fail-fast before expensive operations.**
- Dependency validation + known-failure regression should run before pod training/generation cycles.
- This prevents cost burn from avoidable environment failures.

5. **Use one orchestrator as the operational API.**
- Daily execution should route through `run_full_cycle.py` / `run-full-cycle.ps1`.
- Avoid ad-hoc command chains for production loops.

## Bottom Line

Phase 0 and Phase 1 materially improved reliability. The remaining gap is **measurement and closed-loop autonomy**.  
Phase 2 should make quality improvement measurable, prevent recurrence of known failures, and convert autonomous outputs into deterministic progress.

