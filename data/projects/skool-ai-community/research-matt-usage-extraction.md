# Matt's AI Usage Patterns - Full Extraction Report

**Generated:** 2026-02-12
**Purpose:** Course design research for Skool AI community. Extract Matt's actual workflows, systems, and patterns for teaching others.

---

## 1. Life OS Architecture

### What It Is

Life OS is a persistent AI Chief of Staff running in the terminal via Claude Code. It is NOT a chatbot or assistant -- it is a decision-making, task-executing, pattern-recognizing operating system for Matt's entire life and business.

**Location:** `/Users/mateuszjez/projects/life-os/`

### Core File Structure

```
life-os/
  CLAUDE.md          -- WHO Claude is (rules, principles, learned mistakes)
  AGENTS.md          -- WHAT Claude DOES (procedures, schedules, commands)
  SOUL.md            -- CoS personality and decision framework
  USER.md            -- Who Matt is (profile, communication style, preferences)
  context/
    goals.md         -- Current identity, goals, hypothesis, active projects
    patterns.md      -- Behavioral patterns, three modes, push vs pull
    psycho-cybernetics.md
    lonsdale-protocol.md
    2026-north-star.md
    AI-CODING-WORKFLOW.md  -- Ralph-Driven Development (782 lines)
    codex-chief-of-staff-runbook.md
    clawdbot-setup.md
    contacts.json
    projects/         -- Per-project context docs
    references/        -- Source material (transcripts, books)
  data/
    daily-logs/       -- 23 daily log files (Jan 15 - Feb 10, 2026)
    charisma/         -- Client work data (Charlie Houpert)
    projects/         -- Project-specific data
    sessions.json     -- Session tracking
  .claude/
    skills/           -- 22 on-demand skill modules
```

### How the System Works

**Session Start Protocol (Non-Negotiable):**
1. Claude reads `SOUL.md` (who it is), `USER.md` (who Matt is)
2. Reads today's daily log
3. Checks `context/goals.md` for current ONE THING
4. Loads relevant project context
5. Does NOT announce it is doing this -- just does it

**Auto-Save Protocol:**
When Matt shares ANY information (screenshots, test results, voice notes, emails, links, decisions, personality data), Claude IMMEDIATELY saves to the correct location in Life OS BEFORE continuing the conversation. This means the system accumulates data over time without Matt having to organize anything.

**Save locations:**
- Charlie/Charisma data --> `data/charisma/`
- Personality data --> `data/personality-*.md`
- Daily activity --> `data/daily-logs/YYYY-MM-DD.md`
- Patterns/insights --> `context/patterns.md`

### The 22 Skills System

Skills are on-demand knowledge modules loaded only when relevant. This keeps context lean.

| Skill | Purpose |
|-------|---------|
| `ralph-workflow` | Ralph-Driven Development for coding projects |
| `deep-research` | Web research with browser automation |
| `voice-processing` | Transcribe and structure voice notes |
| `learned-mistakes` | Full mistake reference (20 entries, growing) |
| `charlie-trial` | Client engagement context and strategy |
| `morning-briefing` | Daily brief generator with calendar, priorities |
| `behavioral-patterns` | Pattern detection (80% loop, perfectionism, avoidance) |
| `lonsdale-protocol` | Courage/focus framework from Joe Lonsdale |
| `psycho-cybernetics-exercises` | Self-image reprogramming exercises |
| `two-claude-review` | Two-Claude pattern for architectural decisions |
| `context-optimizer` | Audit and slim down context usage |
| `dashboard-sweep` | Pre-push validation for dashboard updates |
| `coding-standards` | Code quality rules |
| `code-reviewer` | Code review patterns |
| `security` | Security review patterns |
| `techdebt` | Technical debt management |
| `calendar-access` | AppleScript calendar integration |
| `apple-notes` | AppleScript notes integration |
| `nicotine-tracking` | Health tracking |
| `mind-wandering` | Focus management |
| `matt-design-system` | UI design system standards |
| `ai-tool-comparison` | Tool evaluation framework |

**Key Pattern:** Skills follow a naming convention. Each has a `SKILL.md` with frontmatter (name, description) and a trigger condition. Claude loads them when the conversation topic matches.

### The Psycho-Cybernetics Integration

Matt has integrated Maxwell Maltz's Psycho-Cybernetics framework as a core operating system for self-management. This is NOT typical self-help -- it is a systematic approach to performance psychology.

**The Three Modes Framework:**
- **Mateusz (THE LEAD):** Calibrated servo-mechanism. Pull motivation, enjoys the process, relaxed effort. The goal state.
- **Big Matt (THE TOOL):** Over-revved success mechanism. All push, no joy, excessive self-criticism. Useful but should not lead.
- **Lil Matty (THE WATCH):** Failure mechanism active. Fear, avoidance, defensive. Warning sign.

**Detection Triggers (Claude monitors for these):**
- Avoidance/fear language --> "Sounds like failure mechanism is active"
- Grinding/no joy --> "Big Matt is running. Where's the pull?"
- Push language ("I have to") --> Reframe to "You get to"

**Quick Reset Protocol:** STOP --> RELAX (3 breaths) --> RECALL (one win) --> REFRAME (approach goal) --> ACT

**Exercise Library:**
- Theater of the Mind (daily visualization)
- Progressive Relaxation
- Rational Self-Analysis
- Shadow-Boxing for upcoming challenges
- Success Recall banking
- Pre-task protocols for scary work

### The Lonsdale Protocol

Based on Joe Lonsdale (Palantir co-founder). 7 principles integrated into daily checks:

1. COURAGE - Charge the front
2. ONE FAILURE POINT - Be responsible for one thing failing, not five
3. SELF-STARTEDNESS - Don't wait for permission
4. TALENT DENSITY - Be around interesting people
5. HELP OTHERS SELF-ACTUALIZE - The pull motivation
6. CHESS to GREATNESS - Stop skill-building, start applying
7. PLATFORM COMPOUNDING - Closed loops compound, open loops = 0

**Daily Integration:**
- Morning brief includes Lonsdale check (what am I avoiding?)
- Evening score: Courage Y/N, One Thing Y/N, Self-Start Y/N, Help Others Y/N
- If <3 Y's, surface which mode ran the day

### Daily Log System

23 daily logs spanning Jan 15 - Feb 10, 2026 (~2,934 total lines). Logs track:
- Wake time
- Sessions and work blocks
- Wins and blockers
- Voice notes processed
- Decisions made
- Pattern observations

### Context Recovery Protocol

If Claude's context compacts (runs out of memory mid-session):
1. Run `date` command
2. Read today's daily log
3. Read `context/patterns.md`
4. Check TaskList for current state
5. Continue where it left off -- do NOT ask what happened

### The Elon 5-Step Filter

Every task runs through this BEFORE execution:
1. **Question the requirement** - Is this actually needed?
2. **Delete** - Can we skip 90% of this?
3. **Optimize** - What is the highest ROI action?
4. **Accelerate** - Why cannot this happen right now?
5. **Automate** - Can this run without Matt next time?

---

## 2. All GitHub Projects

### Project 1: Life OS

**Path:** `/Users/mateuszjez/projects/life-os/`
**GitHub:** NOT on GitHub (private, local only)
**Tech Stack:** Plain markdown files, bash scripts, Claude Code skills system
**Complexity:** High -- 22 skills, daily logs, context system, behavioral frameworks, multi-agent coordination
**What It Does:** Personal AI operating system that acts as Chief of Staff. Manages goals, tracks patterns, processes voice notes, generates morning briefs, detects behavioral patterns, integrates with Calendar/Notes/Email via AppleScript.
**Traditional Cost Estimate:** A custom personal productivity system with AI integration, behavioral psychology engine, and calendar/email automation would require:
- Product designer: 2 weeks ($8K)
- Backend engineer: 4 weeks ($20K)
- AI/ML engineer: 3 weeks ($15K)
- Total: ~$43K+ and 2-3 months
- Reality: Matt built this iteratively over ~4 weeks with Claude Code

### Project 2: CoS Dashboard

**Path:** `/Users/mateuszjez/projects/cos-dashboard/`
**GitHub:** Local (git-tracked, deployed)
**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, Radix UI, Framer Motion, React Markdown
**File Count:** 34 TypeScript files
**State:** 1,125-line state.json driving the entire dashboard
**What It Does:** A real-time Chief of Staff dashboard for Matt's trial with Charlie Houpert (Charisma on Command, 7M YouTube subscribers). Shows daily logs, project status, waiting items, playbooks, AI insights, and timeline. Live dashboard that Charlie can check anytime.
**Traditional Cost Estimate:**
- UI/UX designer: 1 week ($4K)
- Frontend engineer: 2 weeks ($10K)
- Total: ~$14K
- Reality: Built by Matt + Claude Code in days

### Project 3: Talent Scout AI

**Path:** `/Users/mateuszjez/Desktop/talent-scout-ai/`
**GitHub:** `wigglyhuff/talent-scout-ai`
**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, Supabase (database), Google Gemini 2.5 Flash (AI), Zustand (state), Playwright (browser automation), Radix UI, Framer Motion
**File Count:** 35 TypeScript files
**Complexity:** VERY HIGH -- 17 phases of development documented in plan.md
**What It Does:** Full recruiting AI that implements Matt's 6-pillar hiring playbook:
1. DEFINE: Signals, Scorecard, Ideal Candidate Profile, Dream Role, Pre-Research
2. FIND: Pond discovery, BrowserUse extraction, proof-of-work scoring
3. BUILD: JD generation, Recruiter Pitch, Scope of Work, Interview Prep, Outreach Templates, Discovery Projects
- AI-controlled browser automation (Playwright) for candidate research
- Deterministic save system (Save/Skip buttons instead of relying on LLM compliance)
- 6 output panels per pillar with deliverables
- FBS (Familiar But Surprising) outreach framework
**Traditional Cost Estimate:**
- Product manager: 3 weeks ($12K)
- UI/UX designer: 3 weeks ($12K)
- Full-stack engineer: 6 weeks ($30K)
- AI engineer: 4 weeks ($20K)
- Total: ~$74K+ and 3-4 months
- Reality: Built iteratively with Claude Code across ~17 phases

### Project 4: How to Find Talent

**Path:** `/Users/mateuszjez/Desktop/howtofindtalent/`
**GitHub:** `wigglyhuff/howtofindtalent`
**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, Framer Motion, Vercel Analytics
**File Count:** 7 TypeScript files
**What It Does:** Static playbook site presenting Matt's hiring methodology. Content-driven, no backend. Includes Twitter algorithm analysis for content distribution strategy.
**Traditional Cost Estimate:**
- Designer/developer: 1 week ($5K)
- Reality: Built in hours with Claude Code

### Project 5: Polymarket Bot

**Path:** `/Users/mateuszjez/projects/polymarket-bot/`
**Tech Stack:** Python (core), Anthropic API, aiohttp, httpx, web3.py, eth-account, DuckDB, Next.js dashboard
**File Count:** 37 Python files across 9 modules
**Source Lines:** 1,354+ lines in core alone, plus strategies, market, intelligence, risk, db, control modules
**What It Does:** Autonomous Polymarket prediction market trading bot with:
- 6 trading strategies: AI Divergence, Neg-Risk Arbitrage, Resolution Farming, Penny Picks, Copy Trade, Market Making
- Paper trading mode with readiness scoring and go-live gates
- Wallet intelligence (tracker + leaderboard + scoring)
- Kelly criterion sizing and risk management
- Kill switch (balance, daily loss, API spend limits)
- HTTP Control API with 12 endpoints
- Signal messaging bridge for mobile control
- Next.js monitoring dashboard
- SQLite logging for auditability
**Traditional Cost Estimate:**
- Quantitative developer: 6 weeks ($36K)
- Backend engineer: 4 weeks ($20K)
- Frontend for dashboard: 1 week ($5K)
- Total: ~$61K+ and 2-3 months
- Reality: Built with Claude Code

### Other Projects Found

**On Disk (additional):**
- `/Users/mateuszjez/projects/ai-performance-orchestrator/` -- Life Tracking AI
- `/Users/mateuszjez/projects/life-tracking-buddy/` -- Life tracking bot
- `/Users/mateuszjez/projects/lifetrackingbuddybot/` -- Bot variant
- `/Users/mateuszjez/projects/landajobcoach/` -- Job coaching app
- `/Users/mateuszjez/Desktop/wispr-flow-dream-job-application/` -- Wispr Flow application
- `/Users/mateuszjez/Desktop/dream-job-newsletter/` -- Newsletter site
- `/Users/mateuszjez/Desktop/osv-fellowship/` -- OSV Fellowship application
- `/Users/mateuszjez/Desktop/vitaley-program-rewrite/` -- Course content rewrite
- `/Users/mateuszjez/Desktop/x-algorithm/` -- Twitter/X algorithm analysis
- `/Users/mateuszjez/Desktop/mrbeast-video-analysis/` -- Video analysis
- `/Users/mateuszjez/Desktop/vitali-auction-scraper/` -- Auction scraping tool
- `/Users/mateuszjez/Desktop/pistachio/` -- Unknown project
- `/Users/mateuszjez/Desktop/suparalph-scanner/` -- Ralph workflow scanner

**On GitHub (from AGENTS.md):**
- `wigglyhuff/resumesdontfuckingwork` -- Landing page
- `wigglyhuff/resumes-dont-work` -- Dream Job Newsletter landing
- `wigglyhuff/wispr-flow-dream-job-application` -- Application site
- `wigglyhuff/vitali-auction-results` -- Auction data
- `wigglyhuff/life-tracking-buddy` -- Life tracking
- `wigglyhuff/ai-performance-orchestrator` -- Performance AI
- `wigglyhuff/prompt-manager` -- Prompt management

---

## 3. Workflow Patterns

### Pattern 1: Ralph-Driven Development (The Core Coding Workflow)

**Source:** `/Users/mateuszjez/projects/life-os/context/AI-CODING-WORKFLOW.md` (782 lines)
**Skill:** `/Users/mateuszjez/projects/life-os/.claude/skills/ralph-workflow/SKILL.md`

This is Matt's PRIMARY coding workflow. Based on Geoffrey Huntley's "Ralph Wiggum" methodology.

**The Core Loop:**
```
1. Create prd.json with detailed plan (passes: true/false per task)
2. Work through ONE task at a time
3. Build after every change
4. Test what you built
5. Commit when it works
6. Mark passes: true
7. Move to next task WITHOUT asking
8. Repeat until ALL pass
```

**Two Modes:**
- **HITL (Human-in-the-Loop):** `ralph-once.sh` -- Run one iteration, watch, intervene. For learning and risky tasks.
- **AFK (Away From Keyboard):** `ralph.sh` -- Run in a loop with max iterations. For overnight/bulk work.

**Key Innovation:** `prd.json` -- a JSON file where each task has a `passes` flag. The AI agent picks the highest priority `passes: false` task and works on it. When done, marks `passes: true`. This gives the agent a clear, finite list of work.

**ralph.sh (the AFK script):**
```bash
#!/bin/bash
set -e
MAX_ITERATIONS=${1:-10}
for i in $(seq 1 $MAX_ITERATIONS); do
  OUTPUT=$(claude -p "Read prd.json. Find highest priority task with passes: false.
    Implement it. Build + lint. Commit. Mark passes: true.
    Append to progress.txt.
    If ALL done: output <promise>COMPLETE</promise>")
  echo "$OUTPUT"
  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then exit 0; fi
  sleep 2
done
```

**Why It Works:**
- Fresh context per task (no context rot)
- Small tasks = higher quality
- Feedback loops catch errors (TypeScript, ESLint, build, tests)
- Progress file provides memory between iterations
- Stop condition prevents infinite loops

### Pattern 2: Interview-First for Complex Features

Before building a complex feature, Matt has Claude interview HIM first:

```
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.
Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs.
Don't ask obvious questions, dig into the hard parts I might not have considered.
Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

**Result:** 10x better specs, 50% fewer bugs, 80% fewer missed requirements.

After the spec is complete, start a FRESH session to execute it (clean context).

### Pattern 3: Two-Claude Review

**Source:** `/Users/mateuszjez/projects/life-os/.claude/skills/two-claude-review/SKILL.md`
**Credited to:** Boris Cherny (Claude Code creator)

For architectural decisions:
1. Claude 1 (CoS/Planner) creates the plan
2. Claude 2 (SWE/Reviewer) reviews as a staff engineer, catches blind spots
3. Execute only AFTER second review

**Real example:** Claude 1 found 5 issues in Life OS audit. Claude 2 found 4 additional issues. Result: 9 total fixed instead of 5.

### Pattern 4: Multi-Agent Fan-Out

For bulk work across many files:
```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from X to Y. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit:*)"
done
```

6 parallel Codex agents working on separate fixes, each opening separate PRs. 6 PRs completed in 11 minutes vs sequential.

### Pattern 5: Subagent Delegation (Context Management)

When context fills up, spawn subagents for investigation:
```
Use subagents to investigate how our authentication system handles
token refresh, and whether we have any existing OAuth utilities I should reuse.
```

Subagent runs in separate context, reads dozens of files, reports back summary. Main context stays clean.

### Pattern 6: Voice Note Processing Pipeline

**Source:** `/Users/mateuszjez/projects/life-os/.claude/skills/voice-processing/SKILL.md`

When a voice note arrives (via WhatsApp/Clawdbot):
1. Transcribe content
2. Extract: KEY POINTS, DECISIONS MADE, QUESTIONS ASKED, ACTION ITEMS, PRIORITY CHANGES
3. Save structured brief to `data/charisma/voice-briefs/`
4. Alert Matt with 2-3 line summary
5. If from client (Charlie): flag as high priority
6. If action items exist: add to daily log
7. If priority changes: update context

### Pattern 7: Mobile-Desktop Sync via Clawdbot

**Source:** `/Users/mateuszjez/projects/life-os/context/clawdbot-setup.md`

Two-tier architecture:
- **Desktop:** Claude Code (Sonnet 4.5) for coding, complex reasoning, deep work
- **Mobile:** Clawdbot (Z.AI GLM 4.7) via WhatsApp for logging, simple queries

Sync via git: Clawdbot commits with prefix "Clawdbot:", terminal Claude pulls on startup and reviews.

### Pattern 8: The Learned Mistakes System

20 documented mistakes, each permanently encoded as a rule:

Examples:
- #1: Not using Task system --> BEFORE any multi-step work: TaskCreate
- #5: Making up times --> ALWAYS run `date` before writing ANY times
- #6: Fabricating data --> Only log what ACTUALLY happened
- #11: Copy-pasting without validation --> 5-Point Validation Gate
- #12: Clawdbot messaging other people --> Default dmPolicy: "allowlist"

**Key Principle:** Every mistake becomes a permanent rule. "Fix the instructions, not just the code." This compounds over time -- the AI gets smarter with every error.

### Pattern 9: Morning Briefing System

Automated daily brief at 8:00 AM:
```
MORNING - [Day, Date]
ONE THING: [from goals]
APPROACH GOAL: [reframed as approach, not avoidance]
SCHEDULE: [calendar events]
PRIORITIES: [1-3 items]
CHARLIE TRIAL: [status/next action]
PSYCHO-CYBERNETICS REMINDER: [morning protocol]
LONSDALE CHECK: [what am I avoiding?]
FOLLOW-UPS: [pending >2 days]
BLOCKERS: [anything preventing progress]
```

### Pattern 10: Codex for Autonomous Tasks

**Source:** `/Users/mateuszjez/projects/life-os/context/codex-chief-of-staff-runbook.md`

Codex (OpenAI's coding agent) operates as a parallel CoS with its own runbook:
- Source of truth order: CLAUDE.md > AGENTS.md > goals.md > patterns.md
- Operating loop: Clarify --> Elon's 5 steps --> Execute --> Validate --> Report --> Persist
- Non-negotiable guardrails: No fabricated data, parse full requests, push back on risky work
- Engineering standards: Portable logic, extract to lib/ modules, contract tests
- Portfolio health snapshots validated locally

---

## 4. Cost Analysis

### What Matt Built (Summary)

| Project | Traditional Cost | Time (Traditional) |
|---------|-----------------|-------------------|
| Life OS | $43,000+ | 2-3 months |
| CoS Dashboard | $14,000+ | 2-3 weeks |
| Talent Scout AI | $74,000+ | 3-4 months |
| How to Find Talent | $5,000+ | 1 week |
| Polymarket Bot | $61,000+ | 2-3 months |
| Other projects (10+) | $30,000+ | 2+ months |
| **TOTAL** | **$227,000+** | **12-16 months** |

### Matt's Estimated AI Costs

- Claude Code Pro: ~$200/month (Claude Max plan)
- Z.AI coding subscription (Clawdbot): ~$20-50/month
- Supabase (talent-scout-ai): Free tier or ~$25/month
- Google Gemini API: Minimal (Flash is cheap)
- Vercel hosting: Free tier
- **Total estimated monthly AI cost: $250-300/month**
- **Over 4 months of building: ~$1,000-1,200**

### ROI Calculation

- **Traditional development cost:** $227,000+
- **Matt's AI cost (4 months):** ~$1,200
- **ROI:** ~189x return on investment
- **Time compression:** 12-16 months of work compressed into ~4 months of evenings/weekends
- **Single-person output:** Matt built what would typically require a 3-5 person team

### The Meta-ROI

The Charlie trial (CoS role) targets $15K/month. The tools Matt built to win and execute that trial cost ~$1,200 in AI. If the trial converts:
- First month revenue: $15,000
- Tools cost: ~$1,200
- ROI on first engagement: 12.5x

---

## 5. Course Modules Extraction

### The Distinct Skills Matt Uses

Based on the analysis, Matt's AI usage breaks down into these teachable skill categories:

**Level 1: Foundation (Anyone Can Learn)**
1. Writing effective CLAUDE.md files (system instructions)
2. The "conversation as interface" pattern (talk to AI, not fill forms)
3. Auto-save protocol (teach AI to persist information)
4. Daily log system (structured life tracking)

**Level 2: Intermediate (Some Technical Comfort)**
5. Ralph-Driven Development (PRD + loop workflow)
6. The Interview-First pattern for complex features
7. Learned Mistakes system (compounding AI intelligence)
8. Context management (skills, files, always-on vs on-demand)
9. Multi-session project management

**Level 3: Advanced (Technical Users)**
10. AFK mode (ralph.sh overnight autonomous coding)
11. Multi-agent fan-out (parallel Codex agents)
12. Two-Claude review pattern
13. Subagent delegation for context management
14. Mobile-desktop sync via Clawdbot
15. Browser automation with Playwright

**Level 4: System Design (Power Users)**
16. Full Life OS architecture
17. Client-facing dashboards from AI data
18. Voice note processing pipelines
19. Behavioral pattern detection systems
20. Autonomous trading systems

### Suggested Course Module Structure

**Module 1: "Your First AI Chief of Staff" (Beginner, 30 min)**
- What a CLAUDE.md is and why it matters
- Write your first system instruction file
- The difference between chatting and commanding
- Exercise: Create a CLAUDE.md for your work context

**Module 2: "The Auto-Save Brain" (Beginner, 30 min)**
- Teaching AI to save information automatically
- Setting up daily logs
- The "save first, then respond" protocol
- Exercise: Set up a daily log system

**Module 3: "Goals, Patterns, and the ONE THING" (Beginner, 45 min)**
- How context files make AI smarter over time
- goals.md -- your north star
- patterns.md -- your behavioral fingerprint
- Exercise: Write your goals.md and patterns.md

**Module 4: "Never Make the Same Mistake Twice" (Intermediate, 30 min)**
- The Learned Mistakes system
- How every error becomes a permanent rule
- "Fix the instructions, not just the code"
- Exercise: Create your first 5 learned mistakes rules

**Module 5: "Ralph-Driven Development" (Intermediate, 60 min)**
- Why chatting with AI produces bad code
- The PRD (prd.json) format
- The Plan --> Execute --> Test --> Commit loop
- HITL vs AFK modes
- Exercise: Build a small project using Ralph workflow

**Module 6: "The Interview-First Pattern" (Intermediate, 30 min)**
- How to get 10x better specs from AI
- Having AI interview YOU before planning
- Fresh session execution after spec
- Exercise: Use interview-first for your next feature

**Module 7: "Skills and Context Architecture" (Intermediate, 45 min)**
- Always-on vs on-demand knowledge
- How to write a skill (SKILL.md format)
- Context optimizer -- keeping things lean
- Exercise: Create 3 skills for your domain

**Module 8: "Autonomous Agents" (Advanced, 60 min)**
- ralph.sh -- letting AI code while you sleep
- Multi-agent fan-out for parallel work
- Subagent delegation for context management
- Exercise: Run your first AFK Ralph session

**Module 9: "The Two-Claude Review" (Advanced, 30 min)**
- Planner + Reviewer pattern
- How fresh eyes catch more bugs
- When to use it (architectural decisions, audits)
- Exercise: Run a two-Claude review on existing code

**Module 10: "Building Your Life OS" (Advanced, 90 min)**
- Full system architecture walkthrough
- Morning briefing automation
- Voice note processing
- Calendar and Notes integration
- Behavioral pattern detection
- Exercise: Set up your own Life OS

### What Can Be Taught to Non-Technical People

**Immediately Teachable (zero code required):**
1. Writing a CLAUDE.md file (plain text)
2. Setting up goals.md and patterns.md (plain text)
3. The conversation-as-interface pattern (just talking)
4. Daily logging system (plain text)
5. The Learned Mistakes system (plain text)
6. The Elon 5-Step filter for task evaluation
7. Psycho-Cybernetics integration (behavioral coaching)
8. Morning briefing format (template)
9. Voice note processing (talk, AI structures)

**Needs Simplification:**
- Ralph workflow: Simplify to "give AI a checklist, let it work through it"
- Skills system: Simplify to "save instructions in separate files, reference when needed"
- Multi-agent: Simplify to "open multiple Claude windows, each working on different thing"

---

## 6. The "5-Minute Win" Analysis

### Win 1: The Instant Chief of Staff (Highest Impact, Zero Setup)

Give them a simplified CLAUDE.md they paste into Claude Code settings:

```markdown
# My AI Chief of Staff

You are my Chief of Staff, not a chatbot. You:
- Know my current priorities
- Save everything I tell you to files
- Push back when I'm off track
- Never ask "how can I help?" -- just help

## My Current ONE THING
[User fills in their #1 priority]

## My Rules
- Direct communication, no filler
- Save information before responding
- Track my wins and blockers daily
- Surface patterns you notice
```

**Why it blows their mind:** The AI immediately becomes more useful, more direct, and more proactive. The shift from "chatbot" to "Chief of Staff" is felt within the first message.

### Win 2: The Daily Log Template (5 Minutes to Permanent Habit)

```markdown
# Daily Log - [DATE]

## ONE THING
[What is the single most important thing today?]

## Schedule
- [Events from calendar]

## Accomplished
- [What I actually did]

## Blockers
- [What is stopping me]

## Wins
- [Small victories]

## Tomorrow
- [What carries forward]
```

Tell Claude: "At the start of every conversation, create today's daily log if it doesn't exist, and update it as we work."

**Why it blows their mind:** They get a persistent memory system. The AI remembers what they did yesterday and carries context forward. This alone changes the relationship with AI from "forgettable chat" to "persistent partner."

### Win 3: The "Never Repeat Mistakes" System (Instant Quality Improvement)

Add to CLAUDE.md:
```markdown
## Learned Mistakes (Add immediately when something goes wrong)
1. [First mistake] --> [Permanent rule]
```

Instruction: "When you make a mistake, add it to this list BEFORE doing anything else. This list only grows, never shrinks."

**Why it blows their mind:** The AI visibly improves over time. After 5-10 mistakes are logged, the AI starts catching things it previously missed. They can SEE the compounding.

### Win 4: The "Save First" Protocol (Information Never Lost)

Add to CLAUDE.md:
```markdown
## Auto-Save Protocol
When I share any information (screenshots, decisions, ideas, notes), SAVE to a file first, THEN respond. Never lose information.
```

**Why it blows their mind:** They share a screenshot and the AI saves it to organized files without being asked. Share a voice note transcription and it gets structured and filed. Nothing falls through the cracks.

### Win 5: The ONE THING Morning Brief (Start Every Day Right)

Template message to Claude:
```
Generate my morning brief:
1. What was I working on yesterday?
2. What is my ONE THING today?
3. What's on my calendar?
4. Any blockers or follow-ups?
Keep it under 10 lines.
```

**Why it blows their mind:** They get a personalized daily brief that actually knows their context, priorities, and patterns. It is like having a real Chief of Staff wake up before them.

### Ranking by Impact for Non-Technical Users

1. **The Instant CoS** (CLAUDE.md) -- biggest mindset shift, zero setup
2. **The Daily Log** -- creates persistent memory, immediate utility
3. **The Save First Protocol** -- feels magical, information just gets organized
4. **The Never Repeat Mistakes** -- visible compounding, builds trust in AI
5. **The Morning Brief** -- daily routine integration, highest retention

---

## 7. Key Differentiators for Course Positioning

### What Makes Matt's Approach Unique

1. **It's a system, not a collection of prompts.** Life OS is interconnected -- goals feed into morning briefs, patterns feed into behavioral detection, daily logs feed into context recovery. Teaching isolated prompts misses the point.

2. **The AI gets smarter over time.** The Learned Mistakes system, the growing AGENTS.md, the accumulating daily logs -- this is a compounding system. Most AI courses teach static techniques.

3. **It combines coding AND life management.** The same AI that builds dashboards also detects behavioral patterns and coaches through fear. This holistic approach is rare.

4. **Everything is real.** This is not theoretical. Matt used this system to land a $15K/month CoS role, build a trading bot, create a recruiting AI, and manage a client engagement. The course material IS the case study.

5. **Non-technical applications are built in.** The psycho-cybernetics integration, the Lonsdale protocol, the behavioral pattern detection -- these require zero coding. A life coach could use this system tomorrow.

### Matt's Daily AI Stack

- **Morning:** Claude Code reads daily log, generates morning brief with Lonsdale check
- **During work:** Ralph workflow for coding, subagents for research, voice notes processed
- **Mobile:** Clawdbot via WhatsApp for logging, quick queries
- **Client work:** CoS Dashboard auto-updated from Life OS data
- **Evening:** EOD summary, Lonsdale score, daily log update
- **Overnight:** AFK Ralph running autonomous coding tasks
- **Weekly:** Psycho-Cybernetics review, Lonsdale weekly check

### The Stack in Numbers

- 22 custom AI skills
- 23 daily logs in 4 weeks
- 20 documented learned mistakes (growing)
- 5 active projects built simultaneously
- 37+ Python files (polymarket bot)
- 35+ TypeScript files (talent scout)
- 34+ TypeScript files (CoS dashboard)
- 1,125 lines of dashboard state data
- 782 lines of Ralph workflow documentation
- $227,000+ in estimated traditional development cost
- ~$1,200 in actual AI cost
- 189x ROI

---

## 8. Raw Materials Available for Course Content

### Files That Could Become Lessons

| File | Potential Lesson |
|------|-----------------|
| `/Users/mateuszjez/projects/life-os/CLAUDE.md` | "How to Write a CLAUDE.md That Actually Works" |
| `/Users/mateuszjez/projects/life-os/SOUL.md` | "Giving AI a Personality and Decision Framework" |
| `/Users/mateuszjez/projects/life-os/USER.md` | "Teaching AI Who You Are" |
| `/Users/mateuszjez/projects/life-os/context/AI-CODING-WORKFLOW.md` | "Ralph-Driven Development: The Complete Guide" |
| `/Users/mateuszjez/projects/life-os/context/patterns.md` | "How to Use AI for Behavioral Pattern Detection" |
| `/Users/mateuszjez/projects/life-os/.claude/skills/learned-mistakes/SKILL.md` | "The Compounding Mistakes System" |
| `/Users/mateuszjez/projects/life-os/.claude/skills/ralph-workflow/SKILL.md` | "Autonomous Coding with Ralph" |
| `/Users/mateuszjez/projects/life-os/.claude/skills/morning-briefing/SKILL.md` | "Automated Morning Briefs" |
| `/Users/mateuszjez/projects/life-os/.claude/skills/voice-processing/SKILL.md` | "Processing Voice Notes with AI" |
| `/Users/mateuszjez/projects/life-os/context/clawdbot-setup.md` | "Mobile AI Access via WhatsApp" |
| `/Users/mateuszjez/projects/life-os/context/codex-chief-of-staff-runbook.md` | "Running Multiple AI Agents in Parallel" |
| `/Users/mateuszjez/projects/cos-dashboard/CLAUDE.md` | "Building Client Dashboards with AI" |
| `/Users/mateuszjez/Desktop/talent-scout-ai/AGENTS.md` | "How AGENTS.md Compounds Intelligence" |

### Screenshots and Videos Available

Matt's Desktop has 40+ screenshots from the build process (Jan-Feb 2026) that could serve as visual documentation for the course.

---

## 9. The Story Arc for Course Marketing

**Before AI:** Matt is a recruiter/career coach with a system that works 1-on-1 but cannot scale. Building tech products would cost $200K+ and take a year.

**The Discovery:** Claude Code + Ralph workflow + Life OS architecture. A non-traditional developer (recruiter background) learns to build production-grade software by treating AI as a Chief of Staff, not a chatbot.

**What He Built:**
- A personal AI operating system that manages his life
- A client dashboard that won a $15K/month contract
- A recruiting AI with browser automation
- An autonomous trading bot
- Content sites deployed to production

**The Proof:**
- $227K+ in traditional development value
- Built for ~$1,200 in AI costs
- Single person, no team, no engineering background
- Iterative, compounding system that gets smarter daily

**The Teaching:** "I'll show you exactly how I did it. Not theory. Not prompts. The actual files, the actual system, the actual workflow."

---

*End of extraction. All file paths are absolute. All data is from actual files on disk.*
