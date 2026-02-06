---
name: ralph-workflow
description: Ralph-Driven Development workflow - PRD-based task loop, subagent delegation, autonomous operation, multi-agent fan-out. Auto-loads when coding/building tasks have 3+ steps.
---

# AI Coding Workflow (Ralph-Driven Development)

> Based on Geoffrey Huntley's Ralph Wiggum methodology, Luke Parker's refinements, and Matt Pocock's 11 Tips.

## The Core Insight

**Old way:** Chat with AI, fix things as you go, context drifts, AI starts hallucinating.

**Ralph way:** Design the end state (PRD), let AI loop through tasks one at a time, fix the *instructions* when it fails (not just the code).

**Why it works:** LLMs get stupid as context grows (context rot). Fresh context per task = smarter outputs. The loop mimics how real engineers work: grab task from board, complete it, mark done, repeat.

---

## Tasks + Ralph Loop (How We Track Work)

**As of January 2026, Claude Code introduced Tasks** - a better tracking system for complex multi-session projects.

### Ralph Loop = THE WORKFLOW (How You Work)

1. Create `prd.json` with detailed plan (passes: true/false)
2. Work through ONE task at a time
3. Build after every change
4. Test what you built
5. Commit when it works
6. Mark `passes: true`
7. Move to next task
8. Repeat until ALL pass

**This is your "plan in excruciating detail, then build" process.**

### Tasks = THE TRACKING SYSTEM (How Claude Tracks Progress)

- Tasks stored in `~/.claude/tasks` (persisted to filesystem)
- Tasks have **dependencies and blockers** (not just status)
- Multiple sessions/agents collaborate on same task list
- Updates broadcast across all sessions in real-time
- Better for complex multi-session projects

### How They Work Together

**Use BOTH for any multi-step project:**

1. **Planning:** Create `prd.json` with detailed plan (Ralph style)
2. **Execution:** Claude creates Tasks that map to PRD items
3. **Tracking:** Tasks track dependencies between PRD items automatically
4. **Collaboration:** Multiple sessions work on same task list if needed
5. **Loop:** Ralph loop still runs (plan -> execute -> test -> commit)

**prd.json (your detailed plan):**
```json
{
  "name": "Feature X",
  "features": [
    {"id": 1, "story": "Build component", "passes": false},
    {"id": 2, "story": "Add tests", "passes": false}
  ]
}
```

**Tasks + Ralph Loop = Your default workflow for any multi-step project.**

---

## The Plan Loop (Matt Pocock)

Every piece of code goes through the same cycle:

```
Plan -> Execute -> Test -> Commit
```

1. **Plan** with the AI first. Think through the approach together before writing any code.
2. **Execute** by asking the AI to write code that matches the plan.
3. **Test** the code together. Run unit tests, check types, manual QA.
4. **Commit** and start the cycle again.

### Interview-First for Complex Features

For larger features, have Claude interview you first using the `AskUserQuestion` tool.

### Plan Mode Rules

- Make plans extremely concise. Sacrifice grammar for concision.
- At the end of each plan, give a list of unresolved questions to answer, if any.

---

## Subagent Delegation (Keep Context Clean)

**When context is your constraint, subagents are your superpower.**

**Subagents run in separate context windows and report back summaries.** This keeps your main context clean for implementation.

### When to Use Subagents

- **Research/Investigation:** Exploring codebase patterns, understanding architecture
- **Code Review:** Having fresh eyes review implementation
- **Bulk Analysis:** Analyzing many files without polluting main context

**This is the single biggest context management technique from Claude Code best practices.**

---

## Autonomous Operation

**The loop runs without user intervention.** This is the whole point.

### Two Modes of Operation

**1. AFK Mode (ralph.sh):**
- Bash script runs `claude -p` in a loop
- Each iteration gets fresh context automatically
- Agent works until all PRD tasks pass, then exits

**2. Interactive Mode (user invokes workflow):**
- Keep working through tasks continuously
- Do NOT ask user what to do next
- Just keep going: complete task -> commit -> next task -> repeat
- If context gets compacted, recover from AGENTS.md and prd.json
- Only stop when ALL tasks are done or user interrupts

### Autonomous Workflow
```
1. Read AGENTS.md, prd.json
2. Create Tasks from prd.json
3. Pick highest priority task with passes: false
4. Implement it (small steps, build after each change)
5. Run build to verify no errors
6. TEST IT
7. Ask yourself: "Does this make sense?"
8. If broken -> fix it before committing
9. Commit with descriptive message
10. Mark passes: true in prd.json (and update Task)
11. IMMEDIATELY move to next task
12. Repeat until all tasks pass
13. When ALL done, say "All PRD tasks complete."
```

### MANDATORY: Test Before You Commit
After EVERY change, BEFORE committing:
1. **Run the build** - must pass
2. **Actually use what you built**
3. **Ask yourself: "Does this make sense?"**
4. **Fix any issues BEFORE committing**

### What NOT To Do
- Do NOT ask user "what should I do next?"
- Do NOT exit and tell user to start new conversation
- Do NOT wait for user approval between tasks
- Do NOT stop working after completing one task

### Context Recovery
If context gets compacted mid-session:
1. Read AGENTS.md for project rules
2. Read prd.json to find next task with passes: false
3. Continue working - don't ask user what happened

---

## File Structure

```
project/
  AGENTS.md          # AI instructions (grows over time)
  CLAUDE.md          # Claude Code specific rules
  prd.json           # Task list with passes: true/false
  progress.txt       # AI's memory for this sprint (append-only)
  ralph.sh           # The AFK loop script
  ralph-once.sh      # Single iteration for human-in-loop

~/.claude/tasks/     # Tasks stored by Claude Code (multi-session)
```

---

## The PRD Format (prd.json)

A JSON file where each task has a `passes` flag:

**Rules:**
- Each item is a SMALL task (30 min - 1 hour max for a human)
- `passes: false` = not yet implemented
- `passes: true` = done and verified
- AI marks `passes: true` after completing
- Keep acceptance criteria specific and testable

---

## Task Sizing (Take Small Steps)

| Too Big | Right Size |
|---------|------------|
| "Add authentication" | "Add login form UI" |
| "Redesign the app" | "Update color palette" |
| "Build the API" | "Add GET /users endpoint" |

Each task should be completable in ~30 minutes by a human. If bigger, break it down.

---

## Task Prioritization (Risky First)

| Task Type | Priority | Why |
|-----------|----------|-----|
| Architectural work | High | Decisions cascade through entire codebase |
| Integration points | High | Reveals incompatibilities early |
| Unknown unknowns | High | Better to fail fast than fail late |
| Standard features | Medium | Core functionality |
| UI polish | Low | Can be parallelized later |

**Use HITL Ralph for risky tasks.** Save AFK Ralph for when the foundation is solid.

---

## When AI Fails: Fix Instructions, Not Just Code

Bad output = bad input. When AI makes the same mistake twice:
1. Don't just fix the code
2. Add a rule to AGENTS.md so it never happens again
3. That knowledge compounds forever

---

## Multi-Agent Fan-Out (Parallel Execution)

For bulk migrations, refactors, or fixing errors across many files, distribute work across parallel Claude invocations.

**Use headless mode (`claude -p`) for fan-out. Use Ralph Loop for sequential work.**

---

## When to Use Ralph vs. Normal Chat

| Use Ralph | Use Normal Chat |
|-----------|-----------------|
| Migrations | Exploring ideas |
| Refactors | Creative brainstorming |
| Boilerplate generation | Debugging weird issues |
| Well-defined features | "I don't know what I want yet" |
| Multiple similar tasks | One-off fixes |
| Overnight autonomous work | Real-time collaboration |

---

## Sources

- Geoffrey Huntley's Ralph Wiggum: https://awesomeclaude.ai/ralph-wiggum
- Luke Parker's refinements: https://lukeparker.dev/stop-chatting-with-ai-start-loops-ralph-driven-development
- Matt Pocock's 11 Tips: https://www.mattpocock.com/11-tips-for-ai-coding-with-ralph-wiggum
- Anthropic's "Effective Harnesses for Long-Running Agents": https://www.anthropic.com/research/long-running-agents
