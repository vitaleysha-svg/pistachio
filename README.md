# Pistachio Life OS

AI-powered productivity system for non-technical operators. This is a ready-to-clone repo that gives you a persistent AI Chief of Staff running in Claude Code.

## What This Is

A complete system for running Claude Code as your technical co-founder. You talk naturally, Claude does the technical work.

**Built for:** Non-technical operators who want AI to handle the implementation
**Based on:** Matt's Life OS architecture + Ralph-Driven Development

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
   git clone https://github.com/YOUR-USERNAME/pistachio.git
   cd pistachio
   ```
6. Start Claude:
   ```powershell
   claude
   ```

Claude reads the CLAUDE.md file automatically and knows the full context.

## Quick Start (Mac)

```bash
# Install Node.js (if not installed)
brew install node

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Clone and start
git clone https://github.com/YOUR-USERNAME/pistachio.git
cd pistachio
claude
```

## How It Works

Just talk naturally:
- "Where are we on the project?"
- "I need to set up image generation"
- "Help me train a LoRA model"
- "What should I work on today?"

Claude will:
- Figure out what needs to happen technically
- Install dependencies
- Write code
- Guide you through step-by-step
- Track progress automatically

**You never write code.** Claude does that.

## File Structure

```
pistachio/
├── CLAUDE.md                    # Claude's instructions (read this to understand the system)
├── README.md                    # You are here
├── PROJECT-PISTACHIO-PLAN.md    # Master project plan
├── WINDOWS-SETUP.md             # Detailed Windows setup guide
├── context/
│   └── pistachio-context.md     # Full project context
├── knowledge-base/
│   ├── image-gen-workflow.md    # How to generate images
│   ├── face-consistency.md      # LoRA, IP-Adapter techniques
│   ├── prompts-library.md       # Working prompts
│   ├── funnel-playbook.md       # Conversion funnel design
│   ├── dm-psychology.md         # DM bot training
│   ├── content-strategy.md      # What content to post
│   └── video-gen-workflow.md    # Video generation
├── autonomous-research/
│   ├── GOLD-pistachio.md        # Top insights (9+ rated)
│   ├── findings-YYYY-MM-DD.md   # Daily research
│   ├── predictions.md           # Market predictions
│   ├── recommendations.md       # Action recommendations
│   ├── pending-tasks.md         # Task queue
│   └── memory.md                # Agent memory between sessions
├── data/
│   └── daily-logs/              # What happened each day
├── tools/                       # Technical tools
└── outputs/                     # Generated content
```

## Core Concepts

### The Ralph Loop (How Work Gets Done)

For any multi-step task:
1. Create `prd.json` with tasks that have `passes: true/false`
2. Work through ONE task at a time
3. Test that it works
4. Mark `passes: true`
5. Move to next task
6. Repeat until all pass

Claude does this automatically for complex work.

### Learned Mistakes (How The System Gets Smarter)

When something goes wrong, it gets added to the Learned Mistakes section in CLAUDE.md:

```markdown
### #1: [Short description]
**Mistake:** What went wrong
**Rule:** What to do instead
**Trigger:** When to apply this rule
```

This knowledge compounds. Same mistake never happens twice.

### Session Protocol

Every session, Claude automatically:
1. Runs `date` to know the time
2. Reads memory.md for context
3. Reads today's daily log
4. Checks pending-tasks.md
5. Gives you a quick status

You just say what you want to work on.

## Daily Workflow

1. Open terminal
2. `cd pistachio`
3. `claude`
4. Tell Claude what you want to work on
5. Claude does the technical work
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

## License

MIT - Do whatever you want with this.

---

*System based on Matt's Life OS architecture*
*Last updated: 2026-02-05*
