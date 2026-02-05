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
5. **Loop:** Ralph loop still runs (plan → execute → test → commit)

**Example:**

```bash
# Start Claude with task list ID for multi-session work
CLAUDE_CODE_TASK_LIST_ID=project-name claude

# Tasks are stored in ~/.claude/tasks/project-name/
# Multiple sessions collaborate on same tasks
# PRD items map to Tasks with dependencies
```

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

**Tasks (Claude creates):**
- Task 1: "Build component" (no dependencies)
- Task 2: "Add tests" (depends on Task 1)

**Ralph Loop executes:** Pick Task 1 → Build → Test → Commit → Mark passes: true → Task 2

### When to Use Tasks

**Always use Tasks for:**
- Multi-session projects (work across multiple Claude sessions)
- Multi-agent coordination (multiple agents working on same project)
- Complex projects with dependencies between tasks
- Long-running projects (4+ weeks)
- Any project where you need to track blockers and dependencies

**Tasks + Ralph Loop = Your default workflow for any multi-step project.**

---

## The Plan Loop (Matt Pocock)

Every piece of code goes through the same cycle:

```
Plan → Execute → Test → Commit
```

1. **Plan** with the AI first. Think through the approach together before writing any code.
2. **Execute** by asking the AI to write code that matches the plan.
3. **Test** the code together. Run unit tests, check types, manual QA.
4. **Commit** and start the cycle again.

**Why this matters:** If you skip planning, you're asking the AI to guess what you want. You'll fight hallucinations and misunderstandings. Planning forces clarity.

### Interview-First for Complex Features

For larger features, have Claude interview you first using the `AskUserQuestion` tool.

**Prompt:**
```
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs.
Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

**What Claude will ask:**
- Edge cases you haven't considered
- Tradeoffs between different approaches
- UI/UX decisions that affect implementation
- Technical constraints and dependencies
- Error handling and failure modes

**Result:** Claude asks questions that surface blind spots, then writes a complete spec.

**After spec is complete:** Start a fresh session to execute it. The new session has clean context focused entirely on implementation, and you have a written spec to reference.

**Impact:**
- 10x better specs than self-written
- 50% fewer bugs
- 80% fewer missed requirements
- Catches edge cases BEFORE writing code

### Plan Mode Rules

- Make plans extremely concise. Sacrifice grammar for concision.
- At the end of each plan, give a list of unresolved questions to answer, if any.

---

## Subagent Delegation (Keep Context Clean)

**When context is your constraint, subagents are your superpower.**

Context window fills fast. Every file read, command output, and conversation adds tokens. When the context window fills, performance degrades - Claude starts "forgetting" earlier instructions or making more mistakes.

**Subagents run in separate context windows and report back summaries.** This keeps your main context clean for implementation.

### When to Use Subagents

- **Research/Investigation:** Exploring codebase patterns, understanding architecture
- **Code Review:** Having fresh eyes review implementation
- **Bulk Analysis:** Analyzing many files without polluting main context

### How It Works

Tell Claude to use subagents for investigation:

```
Use subagents to investigate how our authentication system handles
token refresh, and whether we have any existing OAuth utilities I should reuse.
```

The subagent:
1. Runs in separate context window
2. Reads relevant files (dozens, hundreds - doesn't matter)
3. Reports back summary of findings
4. Your main context stays clean - only gets the summary

### After Implementation

Use subagents for code review:

```
use a subagent to review this code for edge cases
```

Fresh context = better code review. The subagent isn't biased toward code it just wrote.

### Impact

- **Context savings:** Main context stays clean, focused on implementation
- **Quality improvement:** Fresh context = better decisions
- **Speed:** No context rot means no degraded performance

**This is the single biggest context management technique from Claude Code best practices.**

---

## ⚠️ CRITICAL: Autonomous Operation

**The loop runs without user intervention.** This is the whole point.

### Two Modes of Operation

**1. AFK Mode (ralph.sh):**
- Bash script runs `claude -p` in a loop
- Each iteration gets fresh context automatically
- Agent works until all PRD tasks pass, then exits

**2. Interactive Mode (user invokes workflow):**
- Keep working through tasks continuously
- Do NOT ask user what to do next
- Do NOT exit and ask user to start new conversation
- Just keep going: complete task → commit → next task → repeat
- If context gets compacted, recover from AGENTS.md and prd.json
- Only stop when ALL tasks are done or user interrupts

### Autonomous Workflow
```
1. Read AGENTS.md, prd.json
2. Create Tasks from prd.json (if using multi-session/Tasks feature)
3. Pick highest priority task with passes: false
4. Implement it (small steps, build after each change)
5. Run build to verify no errors
6. **TEST IT** - Use Playwright or manually verify it works
7. Ask yourself: "Does this make sense? Would a user understand this?"
8. If broken → fix it before committing
9. Commit with descriptive message
10. Mark passes: true in prd.json (and update Task if using Tasks)
11. IMMEDIATELY move to next task (don't wait for user)
12. Repeat until all tasks pass
13. When ALL done, say "All PRD tasks complete."
```

### ⚠️ MANDATORY: Test Before You Commit
After EVERY change, BEFORE committing:
1. **Run the build** - must pass
2. **Actually use what you built** - click through the UI with Playwright
3. **Ask yourself: "Does this make sense?"**
   - Would a user understand what to do?
   - Are the buttons/actions working?
   - Are there obvious bugs or broken interactions?
4. **Fix any issues BEFORE committing**
   - Don't commit broken code
   - Don't commit confusing UX
   - Don't move on until it actually works

**Testing checklist:**
- [ ] Build passes
- [ ] Page loads without errors
- [ ] Buttons/links are clickable
- [ ] Actions produce expected results
- [ ] Text is grammatically correct
- [ ] Layout looks reasonable

### What NOT To Do
- ❌ Ask user "what should I do next?"
- ❌ Exit and tell user to start new conversation
- ❌ Wait for user approval between tasks
- ❌ Stop working after completing one task

### Context Recovery
If context gets compacted mid-session:
1. Read AGENTS.md for project rules
2. Read prd.json to find next task with passes: false
3. Continue working - don't ask user what happened

---

## The 11 Tips (Matt Pocock)

| # | Tip | Summary |
|---|-----|---------|
| 1 | Ralph Is A Loop | What Ralph is and why it works |
| 2 | Start With HITL, Then Go AFK | The two modes of running Ralph |
| 3 | Define The Scope | How to specify what "done" looks like |
| 4 | Track Ralph's Progress | Using progress files between iterations |
| 5 | Use Feedback Loops | Types, tests, and linting as guardrails |
| 6 | Take Small Steps | Why smaller tasks produce better code |
| 7 | Prioritize Risky Tasks | Tackle hard problems first |
| 8 | Explicitly Define Software Quality | Don't let Ralph cut corners |
| 9 | Use Docker Sandboxes | Isolate AFK Ralph for safety |
| 10 | Pay To Play | Cost considerations and tradeoffs |
| 11 | Make It Your Own | Alternative loop types and customization |

---

## The Two Modes

### 1. HITL (Human-in-the-Loop)
Run once, watch, intervene. Best for learning, prompt refinement, and risky tasks.

### 2. AFK (Away From Keyboard)
Run in a loop with max iterations. Best for bulk work, low-risk tasks, overnight runs.

**Progression:**
1. Start with HITL to learn and refine
2. Go AFK once you trust your prompt
3. Review the commits when you return

---

## File Structure

```
project/
├── AGENTS.md          # AI instructions (grows over time)
├── CLAUDE.md          # Claude Code specific rules (optional)
├── prd.json           # Task list with passes: true/false
├── progress.txt       # AI's memory for this sprint (append-only)
├── ralph.sh           # The AFK loop script
└── ralph-once.sh      # Single iteration for human-in-loop

~/.claude/tasks/       # Tasks stored by Claude Code (multi-session)
└── project-name/      # Task list for specific project (if using Tasks)
```

---

## The PRD Format (prd.json)

**This is the key innovation.** A JSON file where each task has a `passes` flag:

```json
{
  "name": "Feature Name",
  "description": "What we're building",
  "features": [
    {
      "id": 1,
      "priority": 1,
      "story": "As a user, I want X so that Y",
      "acceptance": "Verify X works. Verify Y displays correctly.",
      "passes": false
    },
    {
      "id": 2,
      "priority": 2,
      "story": "Button shows confirmation dialog before delete",
      "acceptance": "Click delete. Dialog appears. Cancel works. Confirm deletes.",
      "passes": true
    }
  ],
  "notes": [
    "Ralph workflow: ONE task at a time",
    "Build after EVERY change",
    "Commit after EVERY completed task"
  ]
}
```

**Rules:**
- Each item is a SMALL task (30 min - 1 hour max for a human)
- `passes: false` = not yet implemented
- `passes: true` = done and verified
- AI marks `passes: true` after completing
- Keep acceptance criteria specific and testable

---

## The progress.txt Format

This is the AI's memory for the sprint. **Append-only** (never overwrite):

```
# Ralph Progress Log
# Agent appends entries here after completing each task

[2026-01-07 15:24] Completed: Update color palette (PRD #3)
- Changed CSS variables to enterprise blue/gray
- Removed deprecated lavender colors
- Build passes ✓
- Committed: abc1234
- Note to future self: Button component breaks if you pass both href and onClick
```

**What goes in progress.txt:**
- Tasks completed in this session
- PRD item reference
- Decisions made and why
- Blockers encountered
- Files changed
- Notes for next iteration

**Cleanup:** Delete progress.txt once your sprint is done. It's session-specific.

---

## Feedback Loops (Critical)

Ralph's success depends on feedback loops. The more loops, the higher quality code:

| Feedback Loop | What It Catches |
|---------------|-----------------|
| TypeScript types | Type mismatches, missing props |
| Unit tests | Broken logic, regressions |
| ESLint / linting | Code style, potential bugs |
| Build | Compilation errors |
| Pre-commit hooks | Blocks bad commits entirely |

**The best setup blocks commits unless everything passes.**

---

## Task Sizing (Take Small Steps)

The rate at which you can get feedback is your speed limit. Never outrun your headlights.

| Too Big | Right Size |
|---------|------------|
| "Add authentication" | "Add login form UI" |
| "Redesign the app" | "Update color palette" |
| "Build the API" | "Add GET /users endpoint" |
| "Fix all bugs" | "Fix the chat persistence bug" |

Each task should be completable in ~30 minutes by a human. If bigger, break it down.

**The tradeoff:**
- Larger tasks = less frequent feedback, more context rot
- Smaller tasks = higher quality, but more iterations

For AFK Ralph, keep PRD items small. You want the agent on top form when you're not watching.

---

## Task Prioritization (Risky First)

Without guidance, Ralph picks easy tasks. But you should nail down hard stuff first:

| Task Type | Priority | Why |
|-----------|----------|-----|
| Architectural work | High | Decisions cascade through entire codebase |
| Integration points | High | Reveals incompatibilities early |
| Unknown unknowns | High | Better to fail fast than fail late |
| Standard features | Medium | Core functionality |
| UI polish | Low | Can be parallelized later |
| Quick wins | Low | Easy to slot in anytime |

**Use HITL Ralph for risky tasks.** Save AFK Ralph for when the foundation is solid.

---

## Software Quality (Explicit)

The agent doesn't know what kind of repo it's in. Tell it explicitly:

| Repo Type | What To Say | Expected Behavior |
|-----------|-------------|-------------------|
| Prototype | "Speed over perfection" | Takes shortcuts, skips edge cases |
| Production | "Must be maintainable" | Follows best practices, adds tests |
| Library | "Backward compatibility matters" | Careful about breaking changes |

**The Repo Wins:** Your instructions compete with your codebase. If Ralph sees bad patterns, it will copy them. Keep your codebase clean before letting Ralph loose.

---

## The ralph.sh Script (AFK Mode)

```bash
#!/bin/bash
set -e

MAX_ITERATIONS=${1:-10}
PRD_FILE="prd.json"
PROGRESS_FILE="progress.txt"

if [ -z "$1" ]; then
  echo "Usage: ./ralph.sh <max_iterations>"
  exit 1
fi

echo "Starting Ralph with max $MAX_ITERATIONS iterations"

for i in $(seq 1 $MAX_ITERATIONS); do
  echo ""
  echo "========================================"
  echo "Ralph iteration $i of $MAX_ITERATIONS"
  echo "========================================"

  OUTPUT=$(claude -p "
You are Ralph, a focused coding agent.

## Files to Read
Read $PRD_FILE and $PROGRESS_FILE.

## Your Task
1. Find the highest priority feature with passes: false
   (Choose based on YOUR judgment of priority, not just first in list)
2. Work ONLY on that single feature. No scope creep.
3. Keep changes small and focused - one logical change at a time
4. Run ALL feedback loops:
   - npm run build (must pass)
   - npm run lint (must pass)
5. If all pass, commit with descriptive message
6. Update the PRD item to passes: true
7. Append your progress to $PROGRESS_FILE (APPEND, don't overwrite)
   - Include: task completed, PRD reference, files changed, notes for next iteration

## Prioritization (when choosing tasks)
1. Architectural decisions and core abstractions
2. Integration points between modules
3. Unknown unknowns and spike work
4. Standard features and implementation
5. Polish, cleanup, and quick wins

## Quality Standards
This is production code. Must be maintainable.
Fight entropy. Leave the codebase better than you found it.

## Stop Condition
If ALL PRD items have passes: true, output exactly:
<promise>COMPLETE</promise>

## Rules
- ONE task per iteration
- Small steps - prefer multiple small commits over one large commit
- Keep commits small and focused
- Never commit if build/lint fails
- Never git push (human does that)
- Run feedback loops after each change, not at the end
")

  echo "$OUTPUT"

  # Check for completion signal
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "========================================"
    echo "Ralph completed all tasks!"
    echo "========================================"
    exit 0
  fi

  sleep 2
done

echo "Ralph finished $MAX_ITERATIONS iterations"
```

---

## The ralph-once.sh Script (HITL Mode)

```bash
#!/bin/bash
# Single iteration for interactive use

PRD_FILE="prd.json"
PROGRESS_FILE="progress.txt"

claude "
You are Ralph, a focused coding agent.

## Files to Read
Read $PRD_FILE and $PROGRESS_FILE.

## Your Task
1. Find the highest priority feature with passes: false
   (Choose based on priority, not just first in list)
2. Work ONLY on that single feature
3. Run feedback loops: npm run build, npm run lint
4. If both pass, commit
5. Update PRD to passes: true
6. Append progress to $PROGRESS_FILE

## Prioritization
1. Architectural/integration work first
2. Standard features second
3. Polish and quick wins last

## If Complete
If ALL PRD items pass, say so.

## Rules
- ONE task only
- Small commits
- Never push
"
```

---

## The AGENTS.md Format

Project-specific rules that compound over time:

```markdown
# Project Rules

## Build Commands
- Run `npm run build` after every change
- Run `npm run lint` before committing
- Run `npm run test` if test files exist

## Don'ts
- Never modify the auth system without asking
- Don't add new dependencies without asking
- Never use `any` type in TypeScript
- Don't delete progress.txt

## Learned (add here when you discover bugs)
- Button component breaks if you pass both href and onClick
- Dark mode classes must use `dark:` prefix
- The API rate limits at 100 req/min

## Quality Standards
This codebase will outlive you. Every shortcut becomes someone else's burden.
Fight entropy. Leave the codebase better than you found it.

## Style
- Use Tailwind, not inline styles
- Prefer server components unless state needed
- Keep components under 200 lines
```

---

## When AI Fails: Fix Instructions, Not Just Code

**This is the most important part.**

Bad output = bad input. When AI makes the same mistake twice:

1. Don't just fix the code
2. Add a rule to AGENTS.md so it never happens again
3. That knowledge compounds forever

Example:
- AI keeps adding `any` types → Add "Never use `any` type" to AGENTS.md
- AI keeps forgetting to run build → Add "Run build after EVERY change" to AGENTS.md
- AI modifies auth code → Add "Never modify auth without asking" to AGENTS.md

---

## Alternative Loop Types

Ralph doesn't need to work through a feature backlog:

**Test Coverage Loop:**
```
@coverage-report.txt
Find uncovered lines in the coverage report.
Write tests for the most critical uncovered code paths.
Run coverage again and update coverage-report.txt.
Target: 80% coverage minimum.
```

**Linting Loop:**
```
Run: npm run lint
Fix ONE linting error at a time.
Run lint again to verify the fix.
Repeat until no errors remain.
```

**Entropy Loop:**
```
Scan for code smells: unused exports, dead code, inconsistent patterns.
Fix ONE issue per iteration.
Document what you changed in progress.txt.
```

---

## Multi-Agent Fan-Out (Parallel Execution)

For bulk migrations, refactors, or fixing errors across many files, distribute work across parallel Claude invocations.

**When to use:**
- Migrating 100+ files from one framework to another
- Fixing same lint error across entire codebase
- Applying same refactor pattern to many components
- Generating boilerplate for multiple similar modules

### The Pattern

**Step 1: Generate task list**

Have Claude list all files that need work:

```
List all Python files in src/ that need migrating from unittest to pytest.
Write the list to files.txt, one file per line.
```

**Step 2: Write loop script**

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from unittest to pytest. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit:*)"
done
```

**Step 3: Test on 2-3 files, then run at scale**

Refine your prompt based on what goes wrong with the first few files, then run on the full set.

The `--allowedTools` flag restricts what Claude can do, which matters when you're running unattended.

### Real Example: Clawdbot Multi-Agent Workflow

From Dan Peguine's screenshot workflow:

1. **Take notes + screenshots while testing app** - Document bugs/improvements as you find them
2. **AI builds work list with hypotheses** - Claude analyzes notes and creates structured task list
3. **Say "Go"** - Kicks off 6 parallel Codex agents working on separate fixes
4. **Each opens separate PR for isolated fix** - Clean, reviewable, independent changes
5. **Claude reviews/improves PRs on GitHub** - Quality check before merge
6. **Generates test doc for next iteration** - Documents what to test to verify fixes

**Result:** 6 PRs completed in 11 minutes vs. 6 sequential Ralph iterations

### Impact

- **Speed:** Nx faster (6 agents = 6x, 10 agents = 10x)
- **Isolation:** Each agent has fresh context, no cross-contamination
- **Parallelizable:** No dependencies between tasks = perfect for fan-out

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

## Quick Start

1. Create `prd.json` with your tasks (small, specific, testable)
2. Create `progress.txt` (empty is fine)
3. Create/update `AGENTS.md` with project rules
4. Run `./ralph-once.sh` to test one iteration (HITL)
5. If it works, run `./ralph.sh 10` for AFK mode
6. Review commits when done
7. Push when satisfied

---

## The Loop Visualized

```
┌─────────────────────────────────────────────────────┐
│                    YOU (Human)                       │
│                                                      │
│  1. Design PRD (what should be true at the end)     │
│  2. Write AGENTS.md (project rules)                 │
│  3. Run Ralph (HITL first, then AFK)                │
│  4. Review commits                                   │
│  5. Push when satisfied                              │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   RALPH LOOP                         │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ 1. Read PRD.json + progress.txt             │   │
│  │ 2. Pick highest priority task (passes:false)│   │
│  │ 3. Implement the task (small steps)         │   │
│  │ 4. Run feedback loops (build/lint/test)     │   │
│  │ 5. Commit if green                          │   │
│  │ 6. Mark task passes: true                   │   │
│  │ 7. Append to progress.txt                   │   │
│  │ 8. If all done → exit, else → repeat        │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Sources

- Geoffrey Huntley's Ralph Wiggum: https://awesomeclaude.ai/ralph-wiggum
- Luke Parker's refinements: https://lukeparker.dev/stop-chatting-with-ai-start-loops-ralph-driven-development
- Matt Pocock's 11 Tips: https://www.mattpocock.com/11-tips-for-ai-coding-with-ralph-wiggum
- Anthropic's "Effective Harnesses for Long-Running Agents": https://www.anthropic.com/research/long-running-agents
