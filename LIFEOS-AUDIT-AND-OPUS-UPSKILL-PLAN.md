# LifeOS Audit and Opus 4.6 Upskill Plan

Date: 2026-02-10
Scope: LifeOS operating layer + Pistachio execution layer + autonomous loop reliability

## Executive Diagnosis
LifeOS is directionally strong but operationally fragile. The core failure is not model capability, it is system hygiene: stale instructions, non-portable automation, and weak enforcement loops. Opus 4.6 degraded because it was forced to reason through contradictory/stale state instead of executing against a small, current, testable control surface.

## Findings (Severity-Ordered)

### Critical
1. Autonomous loop is not runnable in this environment.
- `run-pistachio-agent.sh:10` hardcodes `/Users/mateuszjez/Desktop/pistachio`.
- `run-pistachio-agent.sh:29` requires `bash` workflow on Windows where `bash` is unavailable by default.
- `agents/pistachio-agent-v2.md:10` and `agents/pistachio-agent-v2.md:11` hardcode Mac-only absolute paths.
- Impact: the supposed autonomous loop cannot execute reliably across machines.

2. Agent memory loop is effectively dead.
- `autonomous-research/memory.md`, `autonomous-research/pending-tasks.md` remain template-level.
- `autonomous-research/predictions.md:4`, `autonomous-research/recommendations.md:4`, `autonomous-research/questions.md:4`, `autonomous-research/GOLD-pistachio.md:4` all still show last update 2026-02-03.
- Impact: no compounding intelligence despite design intent.

3. Source-of-truth drift remains active.
- `context/projects/pistachio/SKILL.md:9` still references removed path `/PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md`.
- `context/projects/pistachio/context.md:63`, `context/projects/pistachio/context.md:64`, `context/projects/pistachio/context.md:74` still reference stale stack/paths (Nano Banana, Wan2.1, Mac absolute path).
- Impact: autonomous and manual agents are primed with outdated instructions.

### High
4. Workflow control artifacts are stale and misaligned.
- `prd.json:10`, `prd.json:17`, `prd.json:24`, `prd.json:31` still all `passes=false` for old plan.
- `prd.json:38` still encodes old "No git push" note while pipeline state changed.
- Impact: loop planners can pick dead tasks and misprioritize work.

5. Contradictory strategy guidance still exists in active docs.
- `knowledge-base/prompt-reverse-engineering.md:219` and `knowledge-base/prompt-reverse-engineering.md:222` still include Playwright automation direction for MJ despite ban-risk learnings.
- Impact: regressions to known-bad actions remain possible.

6. Context architecture is improved but not fully cleaned.
- `CLAUDE.md` is now lean, but large stale docs still sit in high-signal paths (`PROJECT-PISTACHIO-PLAN.md`, `context/projects/pistachio/context.md`, stale autonomous files).
- Impact: startup quality is better than before but still exposed to stale-state contamination.

### Medium
7. LifeOS telemetry and QA gates are underpowered.
- No CI checks for stale absolute paths or broken references.
- No freshness checks enforcing max age on autonomous-research outputs.
- No deterministic eval harness for Opus quality drift.
- Impact: quality decay is detected late, manually.

8. README and project docs are partially stale.
- `README.md` and multiple context docs describe behavior no longer matching actual state.
- Impact: onboarding and handoff quality degrade over time.

## Why Opus 4.6 Felt Degraded
1. Instruction density and contradiction overloaded decision bandwidth.
2. Core tasking docs pointed to stale reality, causing wrong first moves.
3. Autonomous loop was not executable, so "self-correction by loop" never actually ran.
4. Learnings were documented, but not promoted into hard gates/scripts/tests.

## Upskill Opus 4.6 to High-Reliability Coding Output

## Principle
Do not ask Opus to "remember better." Force quality through architecture: smaller trusted context, executable guardrails, deterministic evals, and automated freshness checks.

## Phase 0 (Same Day): Stabilize Control Surface
1. Replace hardcoded paths with workspace-relative/env-based paths.
2. Add Windows-native autonomous entrypoint (`run-pistachio-agent.ps1`) and keep shell parity.
3. Update `context/projects/pistachio/SKILL.md` and `context/projects/pistachio/context.md` to current stack.
4. Mark stale/legacy docs as archived or non-authoritative.

Acceptance:
- Autonomous loop runs on this machine with one command.
- No active doc points to missing files.

## Phase 1 (48 Hours): Enforceable Guardrails
1. Add `tools/lifeos_preflight.py`:
- checks stale absolute paths
- checks missing referenced files
- checks stale "last updated" thresholds
- fails non-zero on violations
2. Add `tools/lifeos_freshness_check.py`:
- require autonomous-research core files refreshed every N days
3. Add `tools/lifeos_context_budget.py`:
- reports line budget for startup files and warns on bloat thresholds

Acceptance:
- Preflight fails fast before autonomous runs.
- Freshness and context budget become machine-enforced.

## Phase 2 (Week 1): Opus Capability Harness
1. Build `evals/` regression suite from real failures:
- dependency-chain fix test
- warning-first root-cause test
- multi-step task decomposition test
- stale-doc contradiction detection test
2. Add scorecard dimensions:
- correctness
- completeness
- first-pass success
- unnecessary back-and-forth
- adherence to known mistakes
3. Store run results in `autonomous-research/memory.md` as structured entries.

Acceptance:
- Opus performance can be measured per run, not guessed.
- Regressions are visible within one cycle.

## Phase 3 (Week 2): Autonomous Loop Maturity
1. Replace free-form "read everything" directive with bounded execution contract:
- explicit file allowlist
- explicit outputs
- explicit stop conditions
- explicit failure protocol
2. Add briefing writer that always persists to dated file.
3. Add daily orchestration command that runs: preflight -> autonomous loop -> post-run validator.

Acceptance:
- Autonomous loop is deterministic, auditable, and repeatable.

## Implementation Backlog (Prioritized)
1. `run-pistachio-agent.ps1` (portable launcher)
2. `agents/pistachio-agent-v3.md` (bounded contract prompt)
3. `tools/lifeos_preflight.py`
4. `tools/lifeos_freshness_check.py`
5. `tools/lifeos_context_budget.py`
6. `evals/` test corpus and scoring runner
7. Update stale project context docs + source-of-truth index

## KPI Targets (for Opus Upskill)
- First-pass task completion rate: >= 85%
- Repeat-mistake rate: <= 5%
- Mean clarification turns per complex task: <= 1.5
- Stale-reference incidents: 0
- Autonomous loop success rate: >= 95% (no manual intervention)

## No-Click Automation Approval Pack
If you want near-zero prompt approvals during operations, persist scoped command prefixes for:
- `git add`
- `git commit`
- `python -m py_compile`
- `claude -p`
- `powershell -Command Get-Content`
- `powershell -Command rg`

Do not approve broad destructive prefixes.

## Bottom Line
Pistachio did not miss outcomes because the model is weak. It missed because the operating system around the model allowed stale state, non-portable automation, and unenforced rules to accumulate. Tightening the system around Opus 4.6 will produce reliable high-end coding output.
