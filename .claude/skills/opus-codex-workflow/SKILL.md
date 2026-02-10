---
name: opus-codex-workflow
description: Claude plans, Codex implements, Claude reviews and learns. The new development workflow.
---
# Opus-Codex Development Workflow

## The Loop
1. **Claude (Opus 4.6) PLANS** - Creates detailed senior SWE system design documents
   - Architecture decisions, file structure, function signatures
   - Acceptance criteria and test cases
   - Constraints and anti-patterns to avoid
   - Saves as `CODEX-*.md` in repo root

2. **Codex (5.3) IMPLEMENTS** - Reads the plan and builds it
   - Commits locally (never pushes)
   - Writes a changes doc (CODEX-*-CHANGES.md)

3. **Claude REVIEWS** - Reads Codex's commits and changes doc
   - Identifies what Codex did better than Claude would have
   - Identifies gaps or bugs
   - Extracts patterns to add to learned-mistakes or skills
   - Pushes to GitHub after review

4. **Claude LEARNS** - Updates skills/rules based on Codex's approach
   - New patterns go into relevant skills
   - New anti-patterns go into learned-mistakes
   - Quality bar adjustments go into session-learnings

## When to Use This Workflow
- Any task with 5+ files to create/modify
- Any architectural decision with multiple valid approaches
- Any system where testing matters (evals, automation, pipelines)
- Any time Claude has failed at the same type of task before

## When NOT to Use This Workflow
- Quick single-file fixes
- Configuration changes
- Research/exploration tasks
- Urgent operational fixes (pod is down, etc.)

## Plan Document Template
Every plan for Codex should include:
1. **Read order** - Exactly which files Codex should read first
2. **Tasks** - Numbered, specific, with file paths and function signatures
3. **Constraints** - What NOT to do
4. **Success criteria** - How to verify the work is correct
5. **Commit instructions** - Message format, no push rule

## Codex Prompt Format
```
Read CODEX-[PLAN-NAME].md and implement all tasks.
Commit locally with the message specified in the plan.
Do NOT push. Write CODEX-[PLAN-NAME]-CHANGES.md documenting everything.
```
