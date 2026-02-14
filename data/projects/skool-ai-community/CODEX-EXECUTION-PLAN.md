# Skool AI Community — Codex Execution Plan

**Owner:** Codex (reviewed by Opus)
**Date:** 2026-02-12
**Status:** Ready for Matt's review
**MVP Timeline:** 3 days of human time (Day 1: Plan, Day 2-3: Build + Launch)

---

## Executive Summary

Matt is building a Skool community teaching non-technical people how to use Claude Code/Codex the way he does (top 1% of 1%). The goal is $100K/month revenue at scale. This plan synthesizes findings from 4 deep research passes covering: Skool platform best practices, the AI education competitive landscape, Matt's actual usage patterns extracted from 14+ GitHub repos, and course design patterns from all existing projects.

**The gap is real and wide open.** There are zero paid communities teaching non-technical people to use Claude Code as a daily life tool. Every existing course is developer-oriented. Nobody occupies the "AI as your Chief of Staff / Life Operating System" position.

**Research artifacts (read these for full context):**
- `research-skool-best-practices.md` — Platform mechanics, pricing data, engagement tactics, revenue benchmarks
- `research-ai-education-landscape.md` — Competitor analysis, market gaps, positioning, 5-minute win designs
- `research-matt-usage-extraction.md` — All 14+ repos analyzed, 10 workflow patterns, cost analysis ($227K traditional value for ~$1,200 AI cost), module extraction
- `research-course-design-patterns.md` — Dream Job formula, pillar framework, 11 projects mapped to modules, cross-project design patterns

---

## Part 1: Community Architecture

### Name Options (for Matt to decide)
1. **AI Chief of Staff** — Direct, aspirational, universally understood metaphor
2. **The AI Operating System** — Technical-sounding but positions as meta-system
3. **Claude Insiders** — Community-first branding, implies access
4. **The 1% AI Lab** — Exclusivity positioning
5. **AI Power Users** — Simple, clear, slightly generic

### Platform: Skool (Confirmed)
- $99/month flat fee, 0% platform transaction fees
- Built-in gamification (points, levels, leaderboards)
- Native live calls (Skool Call) — critical for daily calls with first 100
- Course module hosting with progressive unlocking
- Community feed + classroom tabs

### Pricing Ladder
| Member Count | Monthly Price | MRR at Cap |
|-------------|--------------|------------|
| 1-50 | $39/month | $1,950 |
| 51-100 | $49/month | $4,900 |
| 101-150 | $59/month | $8,850 |
| 151-200 | $69/month | $13,800 |
| 201-250 | $79/month | $19,750 |
| 251-300 | $89/month | $26,700 |
| 301+ | $97/month (cap) | $97/member |

**Revenue path to $100K/month:**
- Blended average ~$65/month: Need ~1,538 members
- At $97 cap: Need 1,031 members
- Benchmark: Dan Henry does $116K/month with 1,200 members at $97/month on Skool

**Free tier exploration:** Skool supports tiered access. Consider a free community (top-of-funnel content, community access) with paid tier ($39+) for course modules, live calls, and WhatsApp/Telegram access. This maps to Liam Ottley's model (111K free members, upsell to $1,500 paid). But given Matt's high-touch model, starting paid-only with a money-back guarantee may be stronger.

### Gamification Structure (Skool Levels)
| Level | Points | Name | Unlock |
|-------|--------|------|--------|
| 1 | 0 | Normie | Community access, Module 1 |
| 2 | 50 | Intern | Module 2-3 |
| 3 | 150 | Operator | Module 4-5, templates library |
| 4 | 350 | Power User | Module 6-7, advanced templates |
| 5 | 700 | Chief of Staff | Module 8-10, AFK mode guides |
| 6 | 1200 | AI Architect | Full access, direct DMs with Matt |
| 7 | 2000 | Inner Circle | Monthly 1-on-1 with Matt |

Points earned: 1 like = 1 point. Encourages posting, commenting, helping others.

---

## Part 2: The 5-Minute Win (Critical)

This is the single most important design decision. Self-paced courses have 3% completion rates. The first 5 minutes determine whether someone stays.

### Recommended Flow: "Meet Your Chief of Staff"

**0:00 — Member signs up, lands on welcome page**
- Auto-play 90-second video from Matt: "You're about to meet your AI Chief of Staff. This is different from anything you've done with ChatGPT."

**1:30 — Guided action (Claude.ai, NOT Claude Code yet — zero friction)**
- Member opens Claude.ai in browser
- Pastes a pre-written prompt:

```
Act as my Chief of Staff. I'm [name], I work in [field].
My biggest challenge right now is [X].
Give me a 3-step action plan for today, then ask me one
question that will help you understand my situation better.
```

**3:00 — Member gets personalized output**
- Claude responds with a real action plan tailored to their input
- The follow-up question creates the first "this AI actually listens" moment

**4:00 — Post in community**
- Prompt: "Post your first Chief of Staff moment in the #wins channel"
- Gamification: first post = first points toward Level 2

**5:00 — WIN: "Holy shit, this is different from ChatGPT."**

### The Bridge to Claude Code (Weeks 1-4)
```
Day 1:    Win in Claude.ai (browser, zero friction)
Week 1:   "What if AI could do this automatically?"
Week 2:   Install Claude Code (guided video, exact clicks)
Week 3:   First Claude Code session — "tell it what you want"
Week 4:   CLAUDE.md — "AI that remembers everything about you"
Month 2:  Building your Life OS
```

This solves the terminal/CLI barrier by NOT front-loading it.

---

## Part 2.5: The One-Click Installer (THE Product Differentiator)

### The SimpleClaw Precedent

SimpleClaw (simpleclaw.com) made tens of thousands of dollars in its first week by solving one problem: OpenClaw (openclaw.com) is open source but technically painful to set up — terminal, Node.js, Python, configuration. SimpleClaw made it one-click. That's it. Same product, zero friction.

**Our community has the exact same problem.** Matt gave Vitaliy (his business partner) Life OS and even he struggled with the terminal, Node.js, Python setup. If Vitaliy can't do it easily, no normie can.

### What We Need

A **one-click installer** that:
1. A 6-year-old or a grandma clicks ONE button
2. It installs everything silently (Node.js, Claude Code CLI, project structure)
3. Terminal opens automatically
4. An interactive setup wizard starts asking questions to configure their Chief of Staff
5. When done, they have a working Life OS with their CLAUDE.md, goals, daily log — personalized to them

### Technical Architecture

**Option A: Native Installer Package (Recommended for MVP)**

macOS (.pkg) / Windows (.exe) installer that:

```
Step 1: Check system requirements
  - Is Node.js installed? If not, install it silently
  - Is npm available? Configure it
  - Does Claude Code CLI exist? If not: npm install -g @anthropic-ai/claude-code

Step 2: Create project structure
  - mkdir ~/my-chief-of-staff/
  - Drop in starter CLAUDE.md, daily-log template, goals template
  - Drop in .claude/ directory with pre-configured skills

Step 3: Launch setup wizard
  - Open Terminal (macOS) or PowerShell (Windows)
  - Run: claude --project ~/my-chief-of-staff/
  - First message from Claude: interactive onboarding
    "Welcome! I'm going to be your Chief of Staff. Let's set me up.
     What's your name?"
    → Saves to USER.md
    "What do you do for work?"
    → Saves to USER.md
    "What's the ONE THING you're focused on right now?"
    → Saves to goals.md
    "What's your biggest challenge today?"
    → Generates first action plan (THE 5-minute win)

Step 4: Done
  - Member has a personalized Chief of Staff running in Claude Code
  - All context files populated with their information
  - Ready to use immediately
```

**Option B: curl One-Liner (Fastest to ship)**
```bash
curl -fsSL https://install.aicos.community | bash
```
- Downloads and runs a shell script
- Handles all installation
- Opens terminal with setup wizard
- Pro: Ships in hours. Con: Requires terminal to start (chicken-and-egg for non-technical users)

**Option C: Electron Wrapper App (Most polished)**
- Desktop app with a friendly GUI
- "Install My AI Chief of Staff" button
- Progress bar showing installation
- Opens Claude Code in an embedded terminal
- Pro: Most user-friendly. Con: More engineering effort.

**Option D: Web-First + Desktop Bridge (Hybrid)**
- Start in Claude.ai (browser, zero friction) — this is the 5-minute win
- When ready for Claude Code: download the installer from community
- Installer picks up where Claude.ai left off (imports context from onboarding)
- Pro: Lowest initial friction. Con: Two-step process.

### Recommendation

**Ship Option B (curl one-liner) for launch. Build Option A (native installer) within first month.**

The curl script can be wrapped in a community page that says:
1. Open Terminal (with a screenshot showing EXACTLY where Terminal is on Mac)
2. Copy-paste this ONE line
3. Press Enter
4. Follow the prompts

This is how Homebrew, nvm, and most developer tools install. The difference: our script talks to them in plain English after installing.

### The Setup Wizard (Interactive Onboarding)

This is the CLAUDE.md that ships with the installer. It makes the first Claude Code session feel like talking to a person, not configuring software:

```markdown
# Chief of Staff Setup Mode

You are in SETUP MODE. The user just installed their AI Chief of Staff.
They are non-technical. They may have never used a terminal before.

## Your job:
1. Welcome them warmly but directly (no fluff)
2. Ask questions ONE AT A TIME
3. After each answer, SAVE to the appropriate file immediately
4. After all questions, generate their first Morning Brief
5. Then switch to normal Chief of Staff mode

## Setup Questions (ask in order):
1. "What's your name?" → Save to USER.md
2. "What do you do for work? (one sentence is fine)" → Save to USER.md
3. "What's the ONE THING you're focused on right now?" → Save to goals.md
4. "What does a typical day look like for you?" → Save to patterns.md
5. "What's your biggest challenge today?" → Generate action plan

## After setup:
- Generate their first Morning Brief
- Tell them: "Your Chief of Staff is ready. From now on, just open
  Terminal and type 'claude' to talk to me. I'll remember everything."
- Switch CLAUDE.md from setup mode to operational mode
```

### Why This Changes Everything

The current bridge plan (Week 2: install Claude Code with guided video) has massive dropout risk. Every step where someone has to follow a tutorial is a step where they quit.

The one-click installer turns the bridge from:
```
BEFORE: Video → Open Terminal → Type npm command → Wait → Configure → Setup files → Start using
AFTER:  Click button → Answer 5 questions → Start using
```

This is the difference between a 3% completion rate course and a 60%+ activation rate product.

### Codex Task for Installer

**Task 9: One-Click Installer Script**
**Input:** Starter kit templates, setup wizard CLAUDE.md
**Output:** `installer/`
**Deliverables:**
- `install.sh` — The curl-downloadable shell script (macOS + Linux)
- `install.ps1` — PowerShell equivalent (Windows)
- `setup-claude.md` — The setup-mode CLAUDE.md that runs onboarding
- `starter-files/` — All template files that get dropped into the user's project
- `README.md` — One-page guide: "How to install your AI Chief of Staff"
**Acceptance:** Running `bash install.sh` on a clean Mac installs everything and launches the setup wizard in under 2 minutes. A non-technical person can follow the instructions.

---

## Part 3: Course Module Structure

### The Curriculum (10 Modules, Progressive)

Based on extracting Matt's actual workflow patterns from 14+ repos:

**MODULE 1: "Your First AI Chief of Staff"** (Beginner, 30 min)
- Outcome: Member has a working CLAUDE.md and understands the CoS mindset
- What they do: Write their first system instruction, have first directed conversation
- The shift: From "chatbot" to "Chief of Staff"
- 5-Minute Win lives here

**MODULE 2: "The Auto-Save Brain"** (Beginner, 30 min)
- Outcome: AI saves information automatically, nothing falls through cracks
- What they do: Set up daily log template, teach AI to "save first, respond second"
- Key concept: Persistence — AI that remembers across sessions

**MODULE 3: "Goals, Patterns, and the ONE THING"** (Beginner, 45 min)
- Outcome: Member has goals.md and patterns.md, AI knows their north star
- What they do: Define their ONE THING, write behavioral patterns, create context files
- Key concept: The more AI knows you, the better it serves you

**MODULE 4: "Never Make the Same Mistake Twice"** (Intermediate, 30 min)
- Outcome: Learned Mistakes system running, AI visibly improves over time
- What they do: Create first 5 mistake rules, see compounding in action
- Key concept: "Fix the instructions, not the code" — AI gets smarter with every error

**MODULE 5: "The Morning Brief"** (Intermediate, 30 min)
- Outcome: Automated daily brief that knows their context, priorities, and schedule
- What they do: Set up morning brief template, integrate with their daily workflow
- Key concept: Start every day with AI as your co-pilot, not an afterthought

**MODULE 6: "AI Across Your Life"** (Intermediate, 60 min)
- Outcome: Member applies AI to 3+ domains (email, decisions, research, etc.)
- Verticals demonstrated:
  - Writing emails that sound like you
  - Idea generation and brainstorming
  - Decision frameworks (pros/cons, Elon 5-step filter)
  - Research and synthesis
  - Personality analysis / self-awareness
- Key concept: Same system, every vertical. Not separate tools for separate things.

**MODULE 7: "Skills and Context Architecture"** (Intermediate, 45 min)
- Outcome: Member has 3+ custom skills, understands always-on vs on-demand
- What they do: Create skills for their domain, set up context optimizer
- Key concept: Teaching AI specialized knowledge it can reference on demand

**MODULE 8: "The Ralph Workflow — Ship While You Sleep"** (Advanced, 60 min)
- Outcome: Member can run autonomous AI coding/writing loops
- What they do: Create first prd.json, run HITL loop, understand AFK mode
- Key concept: AI as a worker, not just an advisor. Give it a list, let it execute.
- Simplified for non-technical: "Give AI a checklist, let it work through it"

**MODULE 9: "Building Your Life OS"** (Advanced, 90 min)
- Outcome: Full Life OS architecture running — morning briefs, daily logs, pattern detection, context recovery
- What they do: Assemble all previous modules into an integrated system
- Key concept: The whole is greater than the sum of its parts

**MODULE 10: "Multi-Agent Power Moves"** (Advanced, 60 min)
- Outcome: Member can run multiple AI agents in parallel, delegate complex work
- What they do: Subagent delegation, Codex for autonomous tasks, two-Claude review
- Key concept: Scale beyond one conversation — AI teams working for you

### Module Design Principles
- Every module: 5-10 minute videos max, one concept per video
- Every module ends with an action: "Now you try it"
- Every module has a specific deliverable (not just knowledge)
- Progressive unlocking via Skool levels (prevents overwhelm)
- Binary outcomes: "It works or it doesn't" — easy to demonstrate

---

## Part 4: VSL (Video Sales Letter) Outline

### The Hook (0:00-0:30)
"You're using AI wrong. Not a little wrong — fundamentally wrong. You're treating a Chief of Staff like a search engine. I'm going to show you the difference."

### The Problem (0:30-2:00)
- "Most people open ChatGPT, ask a question, get an answer, close the tab. That's like hiring a world-class executive assistant and only asking them what the weather is."
- "You've probably tried: Perplexity for research, ChatGPT for writing, maybe Gemini. You get decent answers. But nothing changes. Your productivity is the same. Your life is the same."
- "Meanwhile, there's a small group of people — the top 1% of 1% — who use AI completely differently. For 10+ hours a day. As an operating system for their entire life."

### The Bridge (2:00-4:00)
- "My name is Matt. 7 months ago, I started using Claude Code — not as a chatbot, but as my Chief of Staff."
- Show the numbers: "I've built 14 projects that would cost $227,000 if I hired developers. My AI cost? About $300 a month."
- "I use AI to recruit, write emails, generate ideas, analyze my own personality, manage client relationships, build trading bots, create dashboards — all from ONE system."
- "And I'm not a developer. I'm a recruiter."

### The Offer (4:00-6:00)
- "I'm opening a community where I teach you exactly how I do this. Not theory. Not prompts. The actual system, the actual files, the actual workflow."
- "When you join, within 5 minutes you'll have your first AI Chief of Staff moment. Within a week, AI will be saving information for you automatically. Within a month, you'll have a Life Operating System that knows your goals, your patterns, and your priorities."
- Pricing: "$39/month to start. Every 50 members, the price goes up $10. It will cap at $97. Early members lock in the lowest price."

### The Proof (6:00-8:00)
- Live screenshare: Show morning brief, daily log, a real Claude Code session
- "This is what my AI knows about me" — scroll through context files
- "This is what it built for me last night while I slept" — show AFK Ralph output
- Show CoS Dashboard: "This is how I manage a $15K/month client relationship"

### The Close (8:00-9:00)
- "This community is for people who know AI is going to change everything but haven't figured out HOW to use it beyond basic chat."
- "If you can follow instructions and type on a keyboard, you can do this."
- "Your Chief of Staff is waiting. [Join button]"
- Money-back guarantee: "If you don't have your first AI win within 48 hours, I'll refund you. No questions."

---

## Part 5: Community Operations Plan

### First 100 Members (High-Touch Phase)

**Daily:**
- Daily live call (Skool Call) — Matt shows what he's working on, takes questions
- 3-5 community posts from Matt (everything he works on IS the content)
- Respond to all comments/questions within 4 hours

**Weekly:**
- "Win of the Week" spotlight (gamification + social proof)
- Weekly challenge (e.g., "Set up your morning brief and post a screenshot")
- Office hours Q&A session

**Channels (WhatsApp/Telegram/Skool):**
- WhatsApp: First 100 members private group (high-touch, real-time)
- Telegram: General community chat
- Skool: Course modules, long-form posts, structured discussions

**Content types:**
- Live screenshares of Matt's actual Claude Code sessions
- "What I built today" posts with before/after
- Member win celebrations
- Quick tip videos (1-3 min)
- "Ask me anything" threads

### Content Calendar (Week 1 Launch)

| Day | Content | Channel |
|-----|---------|---------|
| Mon | "Meet Your Chief of Staff" launch video | Skool + YouTube |
| Tue | "The #1 Mistake Everyone Makes with AI" (short) | YouTube Shorts, Skool |
| Wed | Live screenshare: "Watch me use AI for 30 min" | Skool Call |
| Thu | "How I Built a $15K/month Dashboard with AI" (tutorial) | Skool + YouTube |
| Fri | Member win spotlight + weekly challenge | Skool |
| Sat | "Weekend project: Set up your Daily Log" | Skool |
| Sun | "My AI Morning Brief — Here's what it looks like" | Skool |

Matt can produce 10 videos + 10 shorts per day. Everything he already works on = content.

---

## Part 6: MVP Definition (What Ships in 3 Days)

### Day 1: Plan Everything

**Codex tasks (autonomous):**
1. Set up Skool community with structure, levels, and course shell
2. Write all 10 module descriptions + outcomes (from Part 3 above)
3. Create Module 1 content: "Your First AI Chief of Staff"
   - Welcome video script (90 sec)
   - The CLAUDE.md template for non-technical users
   - The Daily Log template
   - Step-by-step installation guide for Claude Code (screenshots)
   - The "5-minute win" prompt and walkthrough
4. Write VSL script (from Part 4 above)
5. Create community guidelines and rules
6. Set up gamification levels (from Part 1)
7. Create onboarding automation (welcome DM, first action prompt)
8. Draft 7 days of launch content (from Part 5)

**Matt tasks (human):**
- Record VSL (use the script from Part 4)
- Review and approve all Codex outputs
- Set pricing in Skool ($39/month initial)
- Invite Vitaliy as admin
- Set up payment processing

### Day 2: Build

**Codex tasks:**
1. Create Module 2 content: "The Auto-Save Brain"
2. Create Module 3 content: "Goals, Patterns, and the ONE THING"
3. Build the "Chief of Staff Starter Kit" — downloadable templates:
   - CLAUDE.md template (non-technical version)
   - Daily Log template
   - Goals.md template
   - Morning Brief template
   - Learned Mistakes template
4. Create YouTube launch video script (longer form, 10-15 min)
5. Create 5 YouTube Shorts scripts showcasing different AI wins
6. Write Skool community welcome post
7. Write first 3 community discussion prompts

**Matt tasks:**
- Record Module 1 videos (5-10 min segments, screen recordings)
- Record 2-3 shorts from scripts
- Upload to Skool course section
- Test the full onboarding flow as a new member

### Day 3: Launch

**Codex tasks:**
1. Create email sequences (welcome, day 1, day 3, day 7)
2. Create social media launch posts (Twitter, LinkedIn, YouTube community)
3. Build landing page copy (if separate from Skool)
4. Create "Founding Member" badge/certificate template
5. Prepare FAQ document
6. Create content pipeline template (Matt's daily workflow → community content)

**Matt tasks:**
- Final review of everything
- Go live on Skool
- Post launch video to YouTube
- Send to existing network (WhatsApp, email, social)
- First live call with founding members
- Post "Day 1" content

---

## Part 7: Codex Task Specifications

These are the specific autonomous tasks Codex should execute. Each has clear inputs, outputs, and acceptance criteria.

### Task 1: Module 1 Full Content Package
**Input:** Vision notes, research-matt-usage-extraction.md (Section 6: "5-Minute Win")
**Output:** `/Users/mateuszjez/projects/life-os/data/projects/skool-ai-community/modules/module-01-first-chief-of-staff/`
**Deliverables:**
- `welcome-video-script.md` — 90-second script for welcome video
- `claude-md-template.md` — Non-technical CLAUDE.md template
- `daily-log-template.md` — Daily log for non-technical users
- `five-minute-win-walkthrough.md` — Step-by-step guide with exact prompts
- `installation-guide.md` — Claude Code installation for Mac/Windows (screenshot-ready)
- `module-outline.md` — Full module structure with video breakdowns (5-10 min each)
**Acceptance:** A non-technical person could follow every step without help

### Task 2: Module 2 + 3 Content Packages
**Input:** research-matt-usage-extraction.md (Sections 5-6)
**Output:** `modules/module-02-auto-save-brain/` and `modules/module-03-goals-patterns/`
**Deliverables per module:** Script, templates, exercises, module outline
**Acceptance:** Concrete deliverable at end of each module

### Task 3: Chief of Staff Starter Kit
**Input:** All research files, Matt's actual CLAUDE.md/SOUL.md/USER.md as reference
**Output:** `/Users/mateuszjez/projects/life-os/data/projects/skool-ai-community/starter-kit/`
**Deliverables:**
- `claude-md-non-technical.md` — Simplified CLAUDE.md anyone can use
- `daily-log-template.md` — Daily log system
- `goals-template.md` — Goals framework
- `morning-brief-template.md` — Morning brief setup
- `learned-mistakes-template.md` — Error tracking system
- `quick-start-guide.md` — "Do these 5 things in order"
**Acceptance:** Templates work in both Claude.ai and Claude Code

### Task 4: VSL Script (Final)
**Input:** Part 4 of this plan + research-ai-education-landscape.md (positioning)
**Output:** `marketing/vsl-script.md`
**Acceptance:** Under 10 minutes, has hook/problem/bridge/offer/proof/close structure

### Task 5: YouTube Launch Content
**Input:** Vision notes, all research files
**Output:** `marketing/youtube/`
**Deliverables:**
- `launch-video-script.md` — 10-15 min "Why I'm Building This" video
- `short-01-chief-of-staff.md` — 60-sec short
- `short-02-227k-for-1200.md` — 60-sec short (cost comparison)
- `short-03-sleep-coding.md` — 60-sec short (AFK Ralph)
- `short-04-normie-to-power-user.md` — 60-sec short
- `short-05-morning-brief.md` — 60-sec short
**Acceptance:** Each has hook in first 3 seconds, clear CTA at end

### Task 6: Community Operations Setup
**Input:** Part 5 of this plan
**Output:** `operations/`
**Deliverables:**
- `community-guidelines.md` — Rules, expectations, culture
- `onboarding-automation.md` — Welcome DM sequence, first action triggers
- `weekly-content-calendar.md` — Repeatable weekly content structure
- `gamification-levels.md` — Level names, point thresholds, unlock rewards
- `faq.md` — Anticipated questions + answers
**Acceptance:** Matt can hand this to Vitaliy and he can run operations day 1

### Task 7: Skool Page Copy
**Input:** VSL script, research-skool-best-practices.md
**Output:** `marketing/skool-page-copy.md`
**Deliverables:**
- Community name/headline
- About section (the "hook")
- What you'll learn (bullet points)
- Who this is for / who this is NOT for
- Pricing rationale
- Social proof section (Matt's numbers)
- FAQ section
**Acceptance:** Could be copy-pasted directly into Skool community settings

### Task 8: Email Sequences
**Input:** Module structure, 5-minute win design
**Output:** `marketing/email-sequences/`
**Deliverables:**
- `welcome-email.md` — Immediate post-signup, link to 5-min win
- `day-1-email.md` — "Did you complete your first Chief of Staff moment?"
- `day-3-email.md` — "Here's what members are building"
- `day-7-email.md` — "Your first week recap + what's next"
- `win-back-email.md` — For members who haven't engaged in 5 days
**Acceptance:** Each email has one clear CTA, under 200 words

---

## Part 8: Key Strategic Decisions (For Matt)

These need Matt's input before Codex executes:

### Decision 1: Community Name
Options: AI Chief of Staff, The AI Operating System, Claude Insiders, The 1% AI Lab, AI Power Users, or something else entirely.

### Decision 2: Free Tier vs Paid-Only
- **Paid-only ($39+):** Higher quality members, simpler operations, immediate revenue. Risk: slower growth.
- **Free + paid tier:** Massive top-of-funnel, social proof, upsell to $39. Risk: free members dilute community quality, more moderation.
- **Recommendation:** Start paid-only with 48-hour money-back guarantee. Add free tier later once there's social proof.

### Decision 3: Skool Only vs Multi-Platform
- **Skool only:** Simpler. Course + community in one place.
- **Skool + YouTube + WhatsApp + Telegram:** More reach, but more complexity.
- **Recommendation:** Skool as home base. YouTube for acquisition. WhatsApp for first 100 (kill it at 100 or when it becomes noise). Telegram as ongoing chat.

### Decision 4: Launch Strategy
- **Soft launch:** Invite 20 people Matt knows, get testimonials, then open.
- **Hard launch:** YouTube video + social media blast on day 1.
- **Recommendation:** Soft launch to 10-20 people (friends, Vitaliy's network). Get 5 win screenshots. Then hard launch with social proof.

### Decision 5: Matt's Daily Time Commitment
- First 100 members: daily calls + constant posting = 2-3 hours/day minimum
- Post-100: reduce to 3x/week calls + daily posts = 1-2 hours/day
- At scale: weekly calls + community moderators = 30 min/day
- **This needs to be sustainable alongside Charlie trial and other projects.**

### Decision 6: Vitaliy's Role
- Co-creator? Admin/moderator? Silent partner?
- Does he handle operations, content, or both?
- What's the revenue split?

---

## Part 9: Competitive Moat

**Why this is defensible:**

1. **Proof of concept.** 14 projects, $227K traditional value, built for $1,200. This is not theoretical.
2. **Content machine.** Everything Matt does IS the content. No separate "content creation" workload. 10-hour daily Claude sessions = 10+ hours of potential content.
3. **Non-technical empathy.** Matt thinks about his dad (50s+) as the target. This level of simplification is rare in AI education.
4. **Vertical diversity.** Recruiting, email, ideas, personality analysis, career, therapy, content creation — all from one system. No competitor covers this range.
5. **Claude Code depth.** Top 1% of 1% user. Nobody in education has this level of practical daily Claude Code expertise.
6. **Timing.** Tiago Forte pivoting AI-first in 2026. Anthropic released free course Jan 2026. Market is waking up. Window to establish the premium position is open but narrowing.

**Key competitors and why they're not threats:**
- Liam Ottley (111K members): Agency-focused, not life-focused
- Nick Saraev ($478K/mo): Technical automation, not non-technical users
- Anthropic Academy: Free, developer-centric, no community
- Claude Code for Everyone: Free, no monetization, no ongoing community
- Tiago Forte: Pivoting but still rooted in note-taking, not CLI tools

---

## Part 10: Success Metrics

### Launch (Week 1)
- [ ] 25+ founding members
- [ ] 90%+ complete the 5-minute win
- [ ] 10+ community posts from members
- [ ] First live call with 15+ attendees

### Month 1
- [ ] 100 members
- [ ] $4,900 MRR (100 x $49 average)
- [ ] 5+ member testimonials/screenshots
- [ ] Module 1-3 completion rate >60%
- [ ] Daily community posts from 20%+ of members

### Month 3
- [ ] 300 members
- [ ] $20,000+ MRR
- [ ] YouTube channel driving 30%+ of new members
- [ ] Module 1-5 completion rate >50%
- [ ] Churn rate <10%/month

### Month 6
- [ ] 750+ members
- [ ] $50,000+ MRR
- [ ] Community largely self-sustaining (members helping members)
- [ ] All 10 modules complete
- [ ] Vitaliy running daily operations

### Month 12
- [ ] 1,000-1,500 members
- [ ] $97,000-$145,000 MRR ($100K target achieved)
- [ ] Multiple moderators/community managers
- [ ] Matt's time: 30 min/day max
- [ ] YouTube channel: 10K+ subscribers

---

## Part 11: Multi-Agent Orchestration Strategy (CRITICAL)

**Problem:** We have 3 people on Codex and used only 15% of weekly tokens with 3 days left. This is a massive waste. Current workflow is too serial — one agent doing one thing at a time.

**Goal:** Hit 90%+ token usage by February 15th. Parallelize everything.

### The CEO Bot (Orchestrator)

One Codex terminal runs as the **CEO Bot** — it doesn't do work itself, it spins up and coordinates workers:

```
CEO Bot (Orchestrator)
├── Determines what needs to be built
├── Spins up 5-10 worker terminals simultaneously
├── Assigns each worker a specific role/task
├── Monitors progress via shared file system
├── Reallocates workers when tasks complete
└── Reports aggregate progress to Matt
```

**How it works:**
1. CEO Bot reads `CODEX-EXECUTION-PLAN.md` + `prd.json`
2. Identifies the next batch of parallelizable tasks
3. Creates task assignments in `tasks/` directory
4. Spins up worker terminals (each running as a Codex agent)
5. Each worker picks up its assignment, executes, writes output to shared directory
6. CEO Bot polls for completion, assigns next batch
7. Repeat until all tasks done or tokens depleted

### Worker Agent Roles

Each worker terminal runs as a specialized agent with its own system prompt and focus:

| Agent | Role | What It Produces |
|-------|------|-----------------|
| **Course Creator** | Builds module content | Video scripts, exercises, templates, module outlines |
| **Shorts Creator** | Writes YouTube Shorts scripts | 60-sec scripts with hooks, 10+ per batch |
| **VSL Writer** | Marketing copy | VSL script, Skool page copy, email sequences |
| **Life OS Researcher** | Extracts Matt's thinking patterns | "How does Matt think? What are the insights? How to teach this?" |
| **Web Scraper** | Researches competitors, Skool communities | Pricing data, community structures, what's working |
| **Template Builder** | Creates all user-facing templates | CLAUDE.md, daily logs, goals, starter kit files |
| **Community Ops** | Builds operational docs | Guidelines, FAQ, onboarding flows, gamification |
| **Content Calendar** | Plans all content for launch month | Daily posts, weekly themes, YouTube schedule |
| **Reviewer** | QA on all outputs | Reads other agents' work, flags issues, ensures non-technical language |
| **Installer Engineer** | Builds the one-click installer | Shell scripts, setup wizard, starter file packages |
| **Dashboard Agent** | Keeps CoS dashboard updated | Updates state.json with progress, metrics |

### Terminal Configuration

Each Codex terminal should run with:
- Its own `AGENTS.md` defining its role
- Access to the shared `skool-ai-community/` directory
- Write permissions to its own output directory
- Read permissions to all other agents' outputs
- A `progress.txt` (Ralph-style) for its own task tracking

### Orchestration Flow

```
Phase 1 (Immediate — 5 terminals):
  Terminal 1: CEO Bot (orchestrator)
  Terminal 2: Course Creator → Module 1 full content
  Terminal 3: Course Creator → Module 2 + 3 content
  Terminal 4: Template Builder → Starter kit
  Terminal 5: VSL Writer → VSL script + Skool page copy

Phase 2 (After Phase 1 outputs exist — 5 terminals):
  Terminal 1: CEO Bot (continues)
  Terminal 2: Shorts Creator → 10 YouTube Shorts scripts
  Terminal 3: Course Creator → Module 4 + 5 content
  Terminal 4: Community Ops → Guidelines + FAQ + onboarding
  Terminal 5: Content Calendar → Full launch month plan

Phase 3 (Parallel with Phase 2 — 5 terminals):
  Terminal 6: Web Scraper → Deep dive on top 20 Skool communities
  Terminal 7: Life OS Researcher → Extract all of Matt's thinking patterns
  Terminal 8: Email Writer → All email sequences
  Terminal 9: Reviewer → QA on Phase 1 outputs
  Terminal 10: Course Creator → Module 6 + 7 content

Phase 4 (Final push):
  All remaining modules (8-10)
  Landing page copy variants
  Social media launch content
  Testimonial request templates
  Affiliate/referral program design
```

### Token Budget Strategy

With 3 Codex seats and ~85% of weekly tokens remaining:

```
Current: 15% used, 85% remaining, 3 days left
Target:  90%+ used by Feb 15

Per day budget: ~28% of weekly tokens
Per terminal per day: ~5.6% (if running 5 terminals)
Per terminal per day: ~2.8% (if running 10 terminals)

At 10 terminals x 3 days = 30 terminal-days of work
Each terminal can produce 3-5 deliverables per day
Total potential output: 90-150 deliverables
```

### CEO Bot AGENTS.md (For Codex)

```markdown
# CEO Bot — Skool AI Community Orchestrator

You are the CEO Bot. Your job is NOT to do work — it is to ORCHESTRATE.

## Your Loop
1. Read CODEX-EXECUTION-PLAN.md
2. Read prd.json for current task status
3. Identify the next batch of parallelizable tasks
4. Create task files in tasks/ directory for each worker
5. Monitor worker outputs in their respective directories
6. When workers complete, validate output quality
7. Assign next batch
8. Update prd.json with completion status
9. Report to Matt via progress.txt

## Rules
- NEVER do the work yourself — delegate to workers
- ALWAYS maximize parallelism — if 5 things can happen at once, spin up 5 terminals
- ALWAYS validate outputs before marking complete
- Track token usage — aim for 90%+ by end of week
- If a worker produces low quality, reassign to Reviewer terminal
- If all tasks are done, create NEW tasks (more modules, more content variants, deeper research)

## Worker Directories
Each worker writes to: skool-ai-community/{role-name}/
Each worker reads from: skool-ai-community/ (full directory)
Shared progress: skool-ai-community/orchestrator-status.json
```

### prd.json for Codex (Ralph Format)

This is the task tracking file the CEO Bot and all workers reference:

```json
{
  "name": "Skool AI Community MVP",
  "orchestrator": "CEO Bot",
  "token_target": "90% by Feb 15",
  "features": [
    {"id": 1, "priority": 1, "story": "Module 1 full content package", "worker": "course-creator-1", "passes": false},
    {"id": 2, "priority": 1, "story": "Module 2 + 3 content packages", "worker": "course-creator-2", "passes": false},
    {"id": 3, "priority": 1, "story": "Chief of Staff Starter Kit (all templates)", "worker": "template-builder", "passes": false},
    {"id": 4, "priority": 1, "story": "VSL script (final, under 10 min)", "worker": "vsl-writer", "passes": false},
    {"id": 5, "priority": 1, "story": "Skool page copy", "worker": "vsl-writer", "passes": false},
    {"id": 6, "priority": 2, "story": "10 YouTube Shorts scripts", "worker": "shorts-creator", "passes": false},
    {"id": 7, "priority": 2, "story": "Module 4 + 5 content packages", "worker": "course-creator-1", "passes": false},
    {"id": 8, "priority": 2, "story": "Community guidelines + FAQ + onboarding", "worker": "community-ops", "passes": false},
    {"id": 9, "priority": 2, "story": "Full launch month content calendar", "worker": "content-calendar", "passes": false},
    {"id": 10, "priority": 2, "story": "Deep dive top 20 Skool communities", "worker": "web-scraper", "passes": false},
    {"id": 11, "priority": 2, "story": "Extract Matt's thinking patterns for teaching", "worker": "life-os-researcher", "passes": false},
    {"id": 12, "priority": 2, "story": "All email sequences (welcome through win-back)", "worker": "email-writer", "passes": false},
    {"id": 13, "priority": 2, "story": "QA review on all Phase 1 outputs", "worker": "reviewer", "passes": false},
    {"id": 14, "priority": 2, "story": "Module 6 + 7 content packages", "worker": "course-creator-2", "passes": false},
    {"id": 15, "priority": 3, "story": "Module 8 + 9 + 10 content packages", "worker": "course-creator-1", "passes": false},
    {"id": 16, "priority": 3, "story": "Landing page copy variants (3 versions)", "worker": "vsl-writer", "passes": false},
    {"id": 17, "priority": 3, "story": "Social media launch content (Twitter, LinkedIn, YouTube)", "worker": "content-calendar", "passes": false},
    {"id": 18, "priority": 3, "story": "YouTube launch video script (10-15 min)", "worker": "shorts-creator", "passes": false},
    {"id": 19, "priority": 3, "story": "Referral/affiliate program design", "worker": "community-ops", "passes": false},
    {"id": 20, "priority": 3, "story": "Gamification deep design + level rewards", "worker": "community-ops", "passes": false},
    {"id": 21, "priority": 1, "story": "One-click installer script (macOS + Windows) with setup wizard", "worker": "installer-engineer", "passes": false},
    {"id": 22, "priority": 1, "story": "Setup wizard CLAUDE.md — interactive onboarding that configures Chief of Staff", "worker": "installer-engineer", "passes": false},
    {"id": 23, "priority": 2, "story": "Installer landing page copy — 3 steps with screenshots", "worker": "vsl-writer", "passes": false}
  ]
}
```

### How to Activate This

When Matt hands this to Codex:

1. **Terminal 1:** "You are the CEO Bot. Read `CODEX-EXECUTION-PLAN.md` Part 11. Create the prd.json. Begin orchestration. Spin up worker terminals."
2. **Terminals 2-5:** CEO Bot creates them with role-specific AGENTS.md files
3. **Terminals 6-10:** CEO Bot spins these up as Phase 1 workers complete
4. **CEO Bot monitors** progress.txt from each worker, reassigns as needed
5. **Goal:** 90-150 deliverables across 3 days, 90%+ token usage

---

## Appendix: File Structure for Codex

```
life-os/data/projects/skool-ai-community/
├── CODEX-EXECUTION-PLAN.md          ← This file
├── vision-notes.md                   ← Matt's raw vision
├── research-skool-best-practices.md  ← Skool platform research
├── research-ai-education-landscape.md ← Competitor analysis
├── research-matt-usage-extraction.md  ← Usage patterns from repos
├── research-course-design-patterns.md ← Cross-project patterns
├── modules/
│   ├── module-01-first-chief-of-staff/
│   ├── module-02-auto-save-brain/
│   ├── module-03-goals-patterns/
│   ├── module-04-learned-mistakes/
│   ├── module-05-morning-brief/
│   ├── module-06-ai-across-your-life/
│   ├── module-07-skills-context/
│   ├── module-08-ralph-workflow/
│   ├── module-09-life-os/
│   └── module-10-multi-agent/
├── starter-kit/
│   ├── claude-md-non-technical.md
│   ├── daily-log-template.md
│   ├── goals-template.md
│   ├── morning-brief-template.md
│   ├── learned-mistakes-template.md
│   └── quick-start-guide.md
├── marketing/
│   ├── vsl-script.md
│   ├── skool-page-copy.md
│   ├── youtube/
│   │   ├── launch-video-script.md
│   │   └── shorts/
│   └── email-sequences/
├── installer/
│   ├── install.sh                    ← curl-downloadable setup script (macOS/Linux)
│   ├── install.ps1                   ← PowerShell equivalent (Windows)
│   ├── setup-claude.md               ← Setup-mode CLAUDE.md for onboarding wizard
│   ├── starter-files/                ← Templates dropped into user's project
│   └── README.md                     ← "How to install your AI Chief of Staff"
├── operations/
│   ├── community-guidelines.md
│   ├── onboarding-automation.md
│   ├── weekly-content-calendar.md
│   ├── gamification-levels.md
│   └── faq.md
└── prd.json                          ← Ralph-format task tracking
```

---

*This plan was compiled from 4 deep research passes analyzing: Skool platform best practices + 50+ sources, the complete AI education competitive landscape, Matt's usage patterns extracted from 14+ GitHub repos ($227K traditional development value), and course design patterns from all existing projects (Dream Job, How to Find Talent, Talent Scout AI, etc.). All research artifacts are in this directory for reference.*
