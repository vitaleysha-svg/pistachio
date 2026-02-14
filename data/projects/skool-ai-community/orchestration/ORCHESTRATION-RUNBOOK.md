# Orchestration Runbook (Practical)

Use this if you want parallel execution without fragile automation.

## Roles
- Orchestrator
- Course Creator
- Template Builder
- Marketing Writer
- Ops Reviewer

## Cadence (90-minute cycles)
1. Orchestrator assigns batch.
2. Workers produce output files.
3. Ops Reviewer audits against acceptance checks.
4. Orchestrator marks status in `prd.json`.

## Assignment Format
Write task assignments as markdown in `orchestration/tasks/` with:
- Task ID
- Inputs
- Output path
- Acceptance checks
- Deadline

## Quality Gate
No task is marked `passes=true` without:
1. Deliverable exists at expected path.
2. Acceptance criteria are checked.
3. Ops reviewer signs off.

## Anti-Patterns
- Do not create new MVP tasks mid-sprint.
- Do not split context into too many docs.
- Do not ship if launch readiness checklist has open P0 items.
