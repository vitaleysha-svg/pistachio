# Windows Setup Guide for VS

Follow these steps IN ORDER. Claude will help you through each one.

---

## Step 1: Install Required Software

Open PowerShell as Administrator and run:

```powershell
# Install Git
winget install Git.Git

# Install Python 3.11
winget install Python.Python.3.11

# Install Node.js (for Claude Code)
winget install OpenJS.NodeJS
```

**Close and reopen PowerShell after installing.**

---

## Step 2: Install Claude Code

```powershell
npm install -g @anthropic-ai/claude-code
```

Test it works:
```powershell
claude --version
```

---

## Step 3: Create Project Folder

```powershell
# Create the pistachio folder
mkdir C:\Users\$env:USERNAME\pistachio

# Navigate to it
cd C:\Users\$env:USERNAME\pistachio
```

---

## Step 4: Copy Project Files

Get the project files from Matt. Copy them into your `pistachio` folder.

Your folder should look like:
```
pistachio/
├── CLAUDE.md
├── PROJECT-PISTACHIO-PLAN.md
├── context/
├── knowledge-base/
├── autonomous-research/
├── data/
├── tools/
└── outputs/
```

---

## Step 5: Start Claude Code

```powershell
cd C:\Users\$env:USERNAME\pistachio
claude
```

Claude will read the CLAUDE.md and know the full context.

---

## Step 6: Talk To Claude

Just type naturally:
- "Where are we on the project?"
- "I need to set up image generation"
- "Help me train a LoRA model"

Claude will guide you through everything.

---

## Troubleshooting

### "claude is not recognized"
Close and reopen PowerShell. The PATH needs to refresh.

### Python not found
Run: `python --version`
If nothing, reinstall: `winget install Python.Python.3.11`

### Permission errors
Run PowerShell as Administrator (right-click → Run as Administrator)

---

## Daily Workflow

1. Open PowerShell
2. `cd C:\Users\$env:USERNAME\pistachio`
3. `claude`
4. Tell Claude what you want to work on
5. Claude does the technical work
6. When done: "Done for today"

That's it. Claude handles the rest.
