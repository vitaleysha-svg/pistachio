# Life OS

AI-powered productivity system for operators. A ready-to-clone repo that gives you a persistent AI Chief of Staff running in Claude Code.

## What This Is

A complete system for running Claude Code as your technical co-founder. You talk naturally, Claude does the work.

**Built for:** Operators who want AI to handle implementation
**Based on:** Ralph-Driven Development + Life OS architecture

## What Makes This Valuable

- **Ralph Loop** - AI works through tasks autonomously (prd.json + passes: true/false)
- **Learned Mistakes** - Same mistake never happens twice (compounds forever)
- **Session Tracking** - Daily logs, context recovery, persistent memory
- **Skills System** - Domain knowledge loads on-demand
- **Three Modes** - Self-awareness framework for productivity patterns
- **CoS Task Intake** - Elon's 5-Step applied to every task

## Quick Start (Windows)

1. Open PowerShell as Administrator
2. Install dependencies:
   ```powershell
   winget install Git.Git
   winget install Python.Python.3.11
   winget install OpenJS.NodeJS
   ```
3. Close and reopen PowerShell
4. Install Claude Code:
   ```powershell
   npm install -g @anthropic-ai/claude-code
   ```
5. Clone this repo:
   ```powershell
   git clone https://github.com/YOUR-USERNAME/life-os.git
   cd life-os
   ```
6. Start Claude:
   ```powershell
   claude
   ```

## Quick Start (Mac)

```bash
# Install Node.js (if not installed)
brew install node

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Clone and start
git clone https://github.com/YOUR-USERNAME/life-os.git
cd life-os
claude
```

## How It Works

Just talk naturally:
- "Where are we on the project?"
- "What should I work on today?"
- "Help me with [task]"
- "I'm stuck on [problem]"

Claude will:
- Figure out what needs to happen
- Break it into tasks
- Track progress
- Guide you step-by-step
- Learn from mistakes

## File Structure

```
life-os/
├── CLAUDE.md                    # Claude's operating system (customize this)
├── README.md                    # You are here
├── context/
│   ├── AI-CODING-WORKFLOW.md    # Ralph workflow documentation
│   ├── goals.md                 # Your goals and identity (fill this in)
│   ├── patterns.md              # Behavioral patterns to watch for
│   └── projects/
│       └── [project-name]/      # Project-specific context
│           ├── context.md
│           └── SKILL.md
├── data/
│   └── daily-logs/              # What happened each day
│       └── YYYY-MM-DD.md
├── knowledge-base/              # Domain knowledge
├── autonomous-research/         # Research findings
│   ├── GOLD-[topic].md          # Top insights
│   ├── findings-YYYY-MM-DD.md   # Daily research
│   ├── predictions.md
│   ├── recommendations.md
│   ├── pending-tasks.md
│   └── memory.md                # Agent memory between sessions
├── tools/                       # Technical tools
└── outputs/                     # Generated content
```

## Setup (First Time)

1. **Fill in your identity** - Edit `context/goals.md`:
   - Professional Identity
   - Mission
   - Current Primary Goal
   - Identity Statements
   - Values

2. **Customize CLAUDE.md** - Replace `[YOUR NAME]` placeholders

3. **Add your project** - Create `context/projects/[your-project]/context.md`

4. Start Claude and say "Let's get started"

## Core Concepts

### The Ralph Loop (How Work Gets Done)

For any multi-step task:
1. Create `prd.json` with tasks that have `passes: true/false`
2. Work through ONE task at a time
3. Test that it works
4. Mark `passes: true`
5. Move to next task
6. Repeat until all pass

Claude does this automatically.

### Learned Mistakes (How The System Gets Smarter)

When something goes wrong, it gets added to the Learned Mistakes section in CLAUDE.md:

```markdown
### #1: [Short description]
**Mistake:** What went wrong
**Rule:** What to do instead
**Trigger:** When to apply this rule
```

This knowledge compounds. Same mistake never happens twice.

### Three Modes (Self-Awareness)

Define your own three modes:
- **Lead Mode** - Balanced, grounded, connected (this should lead)
- **Execute Mode** - Analytical, sharp, executing (useful tool)
- **Fear Mode** - Avoidant, defensive (warning sign)

Use the SUCCESS/FAILURE diagnostics in `context/patterns.md` to identify which mode is active.

### Session Protocol

Every session, Claude automatically:
1. Runs `date` to know the time
2. Reads context files
3. Reads today's daily log
4. Checks pending tasks
5. Gives you a quick status

You just say what you want to work on.

## Daily Workflow

1. Open terminal
2. `cd life-os`
3. `claude`
4. Tell Claude what you want to work on
5. Claude handles the rest
6. When done: "Done for today"

## Troubleshooting

### "claude is not recognized"
Close and reopen your terminal. The PATH needs to refresh.

### Python not found
```powershell
python --version
# If nothing, reinstall:
winget install Python.Python.3.11
```

### Permission errors (Windows)
Run PowerShell as Administrator.

### Context lost
Say "recover context" - Claude will read the recovery files and continue.

## Adding Projects

Create a new project folder:
```
context/projects/my-project/
├── context.md    # Full project context
└── SKILL.md      # Skill definition for Claude
```

SKILL.md format:
```markdown
---
name: my-project
description: What this project is about
---
# My Project

Reference files and key information here.
```

## License

MIT - Do whatever you want with this.

---

*Last updated: 2026-02-05*
