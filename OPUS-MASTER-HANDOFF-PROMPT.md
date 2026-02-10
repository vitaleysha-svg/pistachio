# Opus 4.6 Master Handoff Prompt

Paste this into Opus 4.6:

---
You are taking over the Pistachio + LifeOS system after a hardening pass. Your job is to continue from current source-of-truth state, learn from prior failure modes, and execute with guardrails.

## Ground Rules
1. Do not push to GitHub unless explicitly instructed.
2. Use current source-of-truth files, not legacy snapshots.
3. Enforce preflight checks before major autonomous work.
4. Convert repeated mistakes into executable safeguards, not just notes.

## Read In This Exact Order
1. `PROGRESS.md`
2. `CODEX-CHANGES.md`
3. `LIFEOS-AUDIT-AND-OPUS-UPSKILL-PLAN.md`
4. `context/projects/pistachio/context.md`
5. `context/projects/pistachio/SKILL.md`
6. `context/session-learnings.md`

Then review the last commits:
- `f5527a9` (Codex audit + pipeline scripts)
- `0030730` (LifeOS phase 0 hardening)
- latest commit after these for Phase 1 guardrails

## Why Prior Workflow Underperformed
Use repository evidence to explain:
- stale or conflicting context
- non-portable autonomous loop
- documented-but-unenforced learnings
- weak preflight/freshness/context-budget checks (before Phase 1)

## Phase 1 Artifacts (must understand and keep green)
- `tools/lifeos_preflight.py`
- `tools/lifeos_freshness_check.py`
- `tools/lifeos_context_budget.py`
- `run-pistachio-agent.ps1`
- `run-pistachio-agent.sh`

## Required Validation Commands
Run and keep these passing:
- `python tools/lifeos_preflight.py --project-root .`
- `python tools/lifeos_freshness_check.py --project-root . --max-age-days 7`
- `python tools/lifeos_context_budget.py --project-root .`
- `powershell -ExecutionPolicy Bypass -File .\run-pistachio-agent.ps1 -DryRun`

## Your Immediate Mission
1. Confirm all guardrails pass.
2. Update autonomous-research memory artifacts from template-level to active operational state.
3. Build Phase 2 from `LIFEOS-AUDIT-AND-OPUS-UPSKILL-PLAN.md`:
- regression eval harness for known failure modes
- deterministic scorecard for first-pass execution quality
- structured logging of eval runs into autonomous memory
4. Keep context authoritative and mark legacy docs clearly if found.
5. Commit changes locally with clear messages (no push).

## Output Format
Return:
1. Findings (severity ordered)
2. Changes made (file list)
3. Validation results (exact commands + summarized output)
4. Remaining risks
5. Next 3 actions

If any check fails, stop and fix root cause before proceeding.
---
