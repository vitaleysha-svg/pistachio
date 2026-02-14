# Matt's Course/Product Design Patterns - Comprehensive Research Report

> Research Date: February 12, 2026
> Purpose: Map all of Matt's projects to potential Skool AI community course content

---

## TABLE OF CONTENTS

1. [Dream Job / Land A Job Coach Program](#1-dream-job--land-a-job-coach-program)
2. [How To Find Talent (Playbook Structure)](#2-how-to-find-talent-playbook-structure)
3. [AI Coding Workflow](#3-ai-coding-workflow)
4. [Talent Scout AI (Product Design)](#4-talent-scout-ai-product-design)
5. [Andre Prep Site](#5-andre-prep-site)
6. [Life Tracking Buddy / Bot](#6-life-tracking-buddy--bot)
7. [AI Performance Orchestrator](#7-ai-performance-orchestrator)
8. [Polymarket Bot](#8-polymarket-bot)
9. [CoS Dashboard](#9-cos-dashboard)
10. [Cross-Project Design Patterns](#10-cross-project-design-patterns)
11. [Course Content Mapping](#11-course-content-mapping)

---

## 1. DREAM JOB / LAND A JOB COACH PROGRAM

### What It Is

A 133-page program (with 12+ hours of video content) that teaches people how to land their dream job by bypassing traditional application systems. It has been distilled into an AI chatbot (`landajobcoach`) that embodies Matt's coaching methodology through RAG-powered conversations.

### Course Structure (7 Modules)

| Module | Title | Core Outcome |
|--------|-------|--------------|
| 0 | The Great Unlearning | Break all outdated job search assumptions (resumes, one-click apply, HR gatekeepers, "need experience", generic networking) |
| 1 | Know Thyself | Identify your character (Entry/Mid/Senior), run the 33-Minute Skill & Energy Audit, build "Hell No" list of deal-breakers |
| 2 | Research Like Heaven | Find 5 companies, narrow to 3, deep research people (not companies), find "Familiar But Surprising" hooks |
| 3 | The Trial Run Project | Build a 4-page website proving you can do the job BEFORE getting hired. Uses a pre-written template |
| 4 | How to Reach Anyone | Email formula (FBS hook + personal tie + bridge to project), 10 outreach methods, "Double-Up" multi-channel strategy |
| 5 | Acing Every Interview | Turn interviews into "vibe checks" (research already did the hard work), negotiation rules, 15-min pre-interview message, 60-min follow-up |
| 6 | Your Final First Impression | 90-day ramp-up plan, 2-5-5 networking plan, "Pull" career trajectory, fresh lens documentation |

### How Outcomes Are Defined Per Module

Each module ends with an **Action Item for the Tracker** -- a specific written deliverable the student must complete before moving on. Examples:

- "Write down the MAIN four-minute mile barrier holding you back"
- "Be honest: for the last 30 days, have you been a Lost Pilot?"
- "Write down one skill you could learn on the job. Brainstorm one way to prove you are learning that skill today"
- "Write down one person you admire. Internalize the fact that they too are desperately looking for great talent"

### How Progress Is Measured

- Module completion milestones with explicit pass/fail quizzes
- The program references quizzing via the "Dream Job Bot" (the AI chatbot)
- Tier system from F-Tier (0.005% success rate, resume spam) to S-Tier (80% success rate, full system)
- Case studies serve as proof points (Swedish friend: 20x salary, Katie Loves Airbnb, 180 Websites, GQ Magazine)

### Grant's 5-Step Formula (Redesign Notes)

Found in `/Users/mateuszjez/Desktop/Dream-Job-Benchmarks/PROGRAM-MASTER-ANALYSIS.md`. Grant simplified Matt's 7 modules down to 5 core questions:

1. Do you actually FEEL like you wanna work there? Y/N
2. Is your research CRACKED on the COMPANY?
3. Is your research CRACKED on the SPECIFIC PERSON you're DMing?
4. Does your project take ALL GUESSWORK off the hiring manager?
5. Did you follow up relentlessly?

**Key critique:** Matt's program was identified as "too much before action" -- Grant's version is outcome-based, not number-based. The redesign notes recommend cutting complexity (character system, excessive numbers) and focusing on "what to DO" rather than "why it matters."

Additional benchmark files exist at `/Users/mateuszjez/Desktop/Dream-Job-Benchmarks/path-a-ambitious/` with per-module implementation guides (MODULE-1 through MODULE-6 plus AI-GRADING-PROMPTS).

### Tech Stack

- **LandAJobCoach chatbot:** Next.js 15, Supabase (PostgreSQL + pgvector), Gemini 2.0 Flash / 3.0 Pro, Google Drive API, Whisper API, Stripe, Tailwind + shadcn/ui, Vercel
- **Course content:** 133-page PDF, 12+ hours of video, extracted text stored for RAG

### Complexity Level

Medium. The chatbot is technically complex (RAG, vector search, AI). But the course content itself is very accessible -- it uses stories, examples, and step-by-step instructions that any non-technical person can follow.

### Potential Course Module

**"How I Used AI to Build My Dream Job Coaching Bot"** -- covers RAG architecture, Google Drive sync for content, vector search, and how to turn expertise into an AI product.

### Key Files

- `/Users/mateuszjez/projects/landajobcoach/CLAUDE.md` -- Project architecture
- `/Users/mateuszjez/Desktop/dream-job-guide-extracted.txt` -- Full 133-page course content
- `/Users/mateuszjez/projects/life-tracking-buddy/DREAM_JOB_PROGRAM_SUMMARY.md` -- 7-module summary prepared for Grant
- `/Users/mateuszjez/Desktop/Dream-Job-Benchmarks/PROGRAM-MASTER-ANALYSIS.md` -- Grant's 5-question redesign framework
- `/Users/mateuszjez/Desktop/Dream-Job-Benchmarks/WHATS-MISSING-STEP-BY-STEP.md` -- Gap analysis and what to add

---

## 2. HOW TO FIND TALENT (Playbook Structure)

### What It Is

Matt's complete 6-pillar recruiting methodology turned into a beautiful, interactive playbook website. This is his professional expertise packaged as a static Next.js site with markdown-rendered content. Originally created as a job application for Wispr Flow.

### The 6-Pillar Framework

| Pillar | Title | Core Insight | Documents |
|--------|-------|-------------|-----------|
| 1 | Correctly Defining the Role | "Don't hire for a job title. Hire for the 2 outcomes that matter most." | Job Scorecard, 2 Variables, Assess Team, ML Engineer Scorecard Example |
| 2 | Making Your JD Your Best Sales Page | "From 'here's what we need' to 'here's who you'll become.'" | 10-Section JD Formula, VSL Template, Application Form, Recruiter Pitch |
| 3 | Using Talent Dense Hiring Channels | "The best ML engineers aren't on LinkedIn. They're in GitHub repos, Discord servers, and academic labs." | Pond Philosophy, Research Framework, Advanced Sourcing, Master Outreach, Referral Networks |
| 4 | Interviewing to Sell, Not to Assess | "The real question isn't 'can they do the job?' It's 'do we want to build together?'" | Valve Philosophy, 7 Recruiter Mindsets, Interview Prep, Asset Stack, Email Automation |
| 5 | Assessing Fit Through Discovery Projects | "A 4-hour project tells you more than 4 hours of interviews." | Project Structure, Personalization, Email Template, Follow-up Cadence, Review Process |
| 6 | The Last Company They'll Ever Work With | "Every hire will improve 100x during their time here." | 100x Frame, Close Candidate, Scope of Work, First 7 Days, 25-5 Playbook, Fresh Lens |

### Teaching Methodology

1. **Pillar-based progression:** Each pillar builds on the previous (you cannot find candidates before defining the role)
2. **Template + SOP + Example pattern:** Every concept has three layers:
   - **Template** -- the blank form to fill out
   - **SOP** -- step-by-step instructions on how to complete it
   - **Example** -- a fully completed real-world example (Wispr Flow ML Engineer)
3. **Philosophy first, then tactics:** Each pillar opens with a philosophical overview ("Fish Where the Big Fish Swim") before giving tactical documents
4. **One source of truth:** The Job Scorecard from Pillar 1 cascades into everything else (JD, outreach, interview questions, discovery project)

### How Complex Hiring Concepts Are Made Accessible

- **Metaphors:** "Ponds" for talent-dense channels, "Fish where the fish swim" for sourcing strategy
- **Anti-patterns:** Each pillar contrasts HR mindset vs. Sales mindset
- **Real examples:** Wispr Flow ML Engineer runs through all 6 pillars as a concrete case study
- **TL;DR summaries:** Every pillar has a `tldr` object with `coreInsight` and 2-3 `keyPoints`
- **Document typing:** Content categorized as `template | sop | example | overview` so readers know what each document IS

### The "Pillar" Framework as a Course Design Pattern

This is Matt's strongest design pattern. The pillar framework is:
- **Sequential but modular** -- pillars unlock in order but each stands alone
- **Deliverable-driven** -- each pillar produces specific artifacts (scorecard, JD, pond map, etc.)
- **Philosophy + Template + Example** -- every pillar has all three layers
- **One source of truth** -- early deliverables cascade into later ones
- **Color-coded** -- each pillar has a distinct visual identity

### Tech Stack

- Next.js (App Router), TypeScript, Tailwind CSS, JetBrains Mono + Source Serif 4 fonts
- Static site -- no backend, no database
- Markdown content rendered from `/public/playbook/` directory
- Twitter Algorithm Guide as bonus content

### Complexity Level

Low for users (beautifully readable playbook). Medium for builders (Next.js site with markdown rendering and complex content architecture).

### Potential Course Module

**"Turn Your Expertise Into a Playbook Website"** -- how to structure domain knowledge into pillars, write templates/SOPs/examples, and build a professional-looking site with AI assistance.

### Key Files

- `/Users/mateuszjez/Desktop/howtofindtalent/lib/playbook/playbook-config.ts` -- Complete data model for 6 pillars, all documents, and helper functions
- `/Users/mateuszjez/Desktop/howtofindtalent/public/playbook/README.md` -- Full playbook overview
- `/Users/mateuszjez/Desktop/howtofindtalent/public/playbook/role-kickoff-checklist.md` -- The 5-step operational workflow
- `/Users/mateuszjez/Desktop/howtofindtalent/COC-Scriptwriter-Talent-Ponds.md` -- Real talent pond research report (for Charisma on Command)

---

## 3. AI CODING WORKFLOW

### What It Is

A comprehensive documentation of Matt's AI-assisted development methodology, combining Geoffrey Huntley's Ralph Wiggum approach, Luke Parker's refinements, and Matt Pocock's 11 Tips for AI Coding.

### The Workflow

**Core insight:** "LLMs get stupid as context grows (context rot). Fresh context per task = smarter outputs."

**The Ralph Loop:**
1. Create `prd.json` with detailed plan (each task has `passes: true/false`)
2. Work through ONE task at a time
3. Build after every change
4. Test what you built
5. Commit when it works
6. Mark `passes: true`
7. Move to next task
8. Repeat until ALL pass

### Key Principles

1. **CLI-first** -- Agents can call CLIs and verify output, closing the loop
2. **Short prompts** -- Show images, few words are enough
3. **docs/*.md for context** -- Maintain docs for subsystems, force model to read them
4. **Never revert** -- Ask model to change it
5. **Commit to main** -- No branches for solo work
6. **Cross-reference projects** -- "Look at ../other-project and do the same here"
7. **Engineer for agents** -- Design codebases so agents work efficiently, not humans
8. **Iterate fast** -- Build, play with it, feel it, evolve it
9. **Queue tasks** -- While one runs, add next idea to pipeline
10. **Prompt immediately** -- If you find a bug, fix it now

### Two Modes

- **HITL (Human-in-the-Loop):** Run once, watch, intervene. Best for learning and risky tasks.
- **AFK (Away From Keyboard):** Run in a loop with max iterations. Best for bulk work, overnight runs.

### File Structure Pattern

```
project/
  AGENTS.md       -- AI instructions (grows over time)
  CLAUDE.md       -- Claude Code specific rules
  prd.json        -- Task list with passes: true/false
  progress.txt    -- AI's memory for this sprint (append-only)
  ralph.sh        -- The AFK loop script
  ralph-once.sh   -- Single iteration for HITL
```

### Tools Described

- Claude Code (CLI), PRD-driven task management, `ralph.sh` bash loop script
- Feedback loops: TypeScript types, unit tests, ESLint, build, pre-commit hooks
- Task sizing: 30 min per task for a human, smaller for AFK mode

### Potential Course Module

**"The AI Coding Workflow: How to Ship Code While You Sleep"** -- THE cornerstone module. Teaches the Ralph Loop, PRD format, AGENTS.md pattern, HITL vs AFK modes, and how to fix instructions when AI fails.

### Key Files

- `/Users/mateuszjez/Desktop/AI-CODING-WORKFLOW.md` -- Complete 643-line workflow documentation

---

## 4. TALENT SCOUT AI (Product Design)

### What It Is

An AI-powered recruiting tool that walks users through defining a role and finding candidates. The AI acts as a recruiting coach, following the 6-pillar playbook methodology. Built as a desktop-only Next.js app.

### UX Decisions

1. **Chat IS the interface** -- No forms. Users interact with an AI that follows the playbook
2. **Progressive disclosure** -- Pillars unlock sequentially, users cannot skip ahead
3. **One continuous conversation** -- Context carries across all 6 pillars (not 6 separate chats)
4. **Save/Skip buttons** -- Deterministic saves (user clicks to confirm, not LLM decision)
5. **Deliverables panel** -- Right sidebar shows what has been created per pillar
6. **AI asks, never hallucinates** -- Bot must ask for facts (company metrics, funding, team size), never fabricate them
7. **Asset-specific chats** -- Each deliverable (JD, Recruiter Pitch, Outreach Templates) is its own focused chat with only that asset's playbook content

### How AI Capabilities Were Surfaced

- **Function calling** -- Gemini 2.5 Flash uses structured function calls to save deliverables (save_job_scorecard, save_vsl_script, etc.)
- **Proposal detection** -- UI detects when bot proposes content (markdown headers + confirmation question) and shows Save/Skip buttons
- **Context panel** -- Each pillar has a specialized panel showing saved deliverables (VariablesPanel, JDPanel, PondsPanel, etc.)
- **Pillar-specific instructions** -- Full playbook methodology injected as system prompt per pillar, not summaries
- **Pond Discovery** -- AI-controlled browser automation (Playwright) for candidate research with human-like delays

### Evolution Through 17 Phases

The project went through extensive iteration:
- Phase 1-7: Foundation, layout, chat, polish
- Phase 8: Full playbook integration (replaced summaries with complete methodology)
- Phase 9: Complete redesign (one conversation, progressive disclosure)
- Phase 10: All deliverables per pillar (25+ function calls)
- Phase 11: Deterministic saves (Save/Skip buttons)
- Phase 12: Playwright browser automation for candidate research
- Phase 13-15: Design polish (Manus-style, terminal aesthetic, light theme)
- Phase 16: RAG architecture (planned, not yet implemented)
- Phase 17: Define + Find architecture redesign

### Tech Stack

- Next.js 14 (App Router), TypeScript strict mode, Tailwind CSS v4 + shadcn/ui
- Supabase for database
- Gemini 2.5 Flash for AI
- Zustand for state management, Framer Motion for animations
- Playwright + Chromium for browser automation

### Complexity Level

High. This is a sophisticated AI product with function calling, browser automation, RAG (planned), and complex state management. A non-technical person would need significant guidance to understand the architecture.

### Potential Course Module

**"Building AI Products That Follow a Methodology"** -- how to turn domain expertise into AI-guided workflows, use function calling for structured outputs, build Save/Skip patterns for reliability, and design progressive disclosure UX.

### Key Files

- `/Users/mateuszjez/Desktop/talent-scout-ai/CLAUDE.md` -- Full architecture and design system
- `/Users/mateuszjez/Desktop/talent-scout-ai/plan.md` -- 17-phase build plan showing the complete evolution
- `/Users/mateuszjez/Desktop/talent-scout-ai/prd-define-find.json` -- Latest PRD for Define + Find architecture

---

## 5. ANDRE PREP SITE

### What It Is

A single-page HTML call preparation tool built for a specific meeting with "Andrey" (likely Andrey from a content creation collaboration). It is a structured call flow with interactive checkboxes, copy-to-clipboard scripts, and a live note-taking textarea.

### How Information Was Organized

The page follows a precise 9-section structure:
1. **Call Goal** -- One sentence: "Lock 5 decisions on handoff format, workflow, tools, cadence, first lane"
2. **30-Minute Agenda** -- Time-boxed segments (0-3, 3-12, 12-22, 22-27, 27-30 minutes)
3. **Opening Script** -- Verbatim script with copy button
4. **Top Questions** -- 12 questions in priority order with checkboxes
5. **Vague Answer Probes** -- Backup questions when answers are not specific enough
6. **Live Decision Capture** -- Textarea with pre-structured categories (Workflow, Bottlenecks, Capacity, etc.)
7. **Non-Negotiables** -- 5 checkbox items that must be locked before the call ends
8. **Closing Script** -- Verbatim closing with copy button
9. **Post-Call Actions** -- Immediate to-do list

### Design Choices

- Pure HTML/CSS/JS -- no framework, no build step, no dependencies
- CSS variables for theming, sticky header, responsive grid
- Interactive checkboxes for live tracking during the call
- Copy-to-clipboard buttons for scripts
- Monospace textarea for structured note-taking
- Clean, functional design (similar to Notion but purpose-built)

### Tech Stack

- Single `index.html` file, vanilla HTML/CSS/JS
- No framework, no build process

### Complexity Level

Very low. Anyone could understand and create something similar with AI assistance. This is a perfect example of "AI as a quick tool builder."

### Potential Course Module

**"Build a Meeting Prep Tool in 10 Minutes with AI"** -- quick win module showing how to use AI to build single-purpose HTML tools. Demonstrates the "prompt immediately" principle from the AI Coding Workflow.

### Key Files

- `/Users/mateuszjez/Desktop/andre-prep-site/index.html` -- Complete 274-line single-file tool

---

## 6. LIFE TRACKING BUDDY / BOT

### What It Is

Two related projects representing the evolution of a personal productivity tracking concept:

**Life Tracking Buddy** (`/Users/mateuszjez/projects/life-tracking-buddy/`): A command-based time tracking app. No AI -- just simple pattern matching. Type commands like `start work`, `end`, `break`, `stats`, `eod`. Deployed to production at life-tracking-buddy.vercel.app.

**Life Tracking Buddy Bot** (`/Users/mateuszjez/projects/lifetrackingbuddybot/`): A Next.js app that was being evolved to integrate an AI conversational layer on top of the command system. The bot version has a Master Integration Plan for adding an "alive" AI personality using a 3-layer architecture:
- Layer 1: Pattern matching (100% reliable, no AI)
- Layer 2: Command execution (direct database operations)
- Layer 3: AI response generation (personality layer only)

### Architecture Pattern: "Commands Are Sacred, AI Is Cosmetic"

The critical design insight: commands (start work, end work, etc.) run via deterministic pattern matching, never through AI. The AI layer only generates the response text. If AI fails, a generic fallback message is shown. This ensures 100% reliability for core features.

### The Onboarding System

7-step onboarding stored in database:
1. Get name
2. Professional identity (<10 words)
3. Current primary goal
4. Working hypothesis for achieving goal
5. Identity statements (3-5 "I [action]" statements)
6. Review and confirm
7. System active

### Tech Stack

**Life Tracking Buddy:**
- Next.js 15.5.4 (App Router + Turbopack), React 19, TypeScript strict mode
- Tailwind CSS 4, PostgreSQL (Supabase) + Drizzle ORM, Supabase Auth
- Sentry (monitoring), Upstash Redis (rate limiting), Vercel hosting
- 159 passing unit tests

**Life Tracking Buddy Bot:**
- Next.js, TypeScript, feature flag system for safe rollout
- Parallel v2 API route alongside production v1
- OpenAI GPT-4o-mini for conversational responses

### Complexity Level

Medium. The core time tracking is simple (pattern matching), but the production infrastructure (Sentry, Redis rate limiting, Drizzle ORM, 159 tests) shows enterprise-grade practices. The AI integration plan demonstrates sophisticated rollout strategy.

### Potential Course Modules

1. **"Build a Chat-Based Productivity Tracker"** -- pattern matching, database operations, simple but useful
2. **"Ship to Production Like a Pro"** -- Sentry monitoring, Redis rate limiting, 159 tests, emergency procedures, deployment workflow
3. **"Add AI to an Existing App (Without Breaking It)"** -- the 3-layer architecture, feature flags, parallel API routes, safe rollout

### Key Files

- `/Users/mateuszjez/projects/life-tracking-buddy/CLAUDE.md` -- Project overview and architecture
- `/Users/mateuszjez/projects/life-tracking-buddy/WORKFLOW.md` -- Complete development and operations workflow (533 lines)
- `/Users/mateuszjez/projects/life-tracking-buddy/AI_CONVERSATIONAL_LAYER_PLAN.md` -- AI integration architecture
- `/Users/mateuszjez/projects/lifetrackingbuddybot/MASTER_INTEGRATION_PLAN.md` -- Full implementation guide with code

---

## 7. AI PERFORMANCE ORCHESTRATOR

### What It Is

A conversational AI assistant that helps users track productivity naturally through chat. No forms, no clicking -- just conversation. This is the most ambitious version of the productivity tracking concept, using a fine-tuned GPT-4o-mini model with 2,461 training examples.

### The Hybrid Architecture

- **Fine-tuning (2,461 examples):** Teaches the AI WHEN to use tools and HOW to call them
- **Runtime prompts (8.3k chars):** Provides current context, user data, and business rules

### The 5 AI Tools

1. `updateProfile` -- User settings and states
2. `manageGoals` -- Ranked goals (1-5 by importance)
3. `manageItems` -- Projects, tasks, and open loops
4. `trackTime` -- Time tracking for work and breaks
5. `searchConversations` -- Past chat search (semantic or date range)

### What Worked vs. What Failed

**Worked (60% pass rate):**
- Friendly tone, tool calling, start/end sessions, time reporting, multi-turn context, goal/task management, dashboard data

**Failed:**
- Onboarding enforcement (skips steps), cancel sessions (zero training examples), ambiguous commands (tracks immediately without asking), feature boundaries (promises features that don't exist), context loss (restarts conversation mid-flow)

### Critical Learning

"The fine-tuned model seems to ignore runtime prompts." Three different prompt approaches (v86-v88) failed. This is a key insight for the course: fine-tuning is hard, and the relationship between training data and runtime prompts is not straightforward.

### Tech Stack

- Next.js 15, TypeScript, Tailwind
- OpenAI GPT-4o-mini (fine-tuned, model ID: ft:gpt-4o-mini-2024-07-18:personal:ai-orch-v11:CW2V9fNb)
- PostgreSQL (Supabase), 9 database tables
- Sentry monitoring, Vercel hosting

### Complexity Level

High. Fine-tuning LLMs, structured outputs with 5 tools, hybrid architecture. A non-technical person would need extensive guidance.

### Potential Course Module

**"Fine-Tuning AI Models: What I Learned from 2,461 Training Examples"** -- the real story of trying to fine-tune GPT-4o-mini, what worked, what failed, and why the Life Tracking Buddy's simpler approach (pattern matching + AI cosmetic layer) ultimately won.

### Key Files

- `/Users/mateuszjez/projects/ai-performance-orchestrator/README.md` -- Complete project documentation with test results
- `/Users/mateuszjez/projects/ai-performance-orchestrator/TRAINING_DATA_EXPLANATION.md` -- What the AI was taught
- `/Users/mateuszjez/projects/ai-performance-orchestrator/v11-training-data.jsonl` -- 2,461 training examples

---

## 8. POLYMARKET BOT

### What It Is

An autonomous Polymarket prediction market trading bot with paper/live execution, risk limits, wallet intelligence, and a local dashboard. Controllable via HTTP API and Signal messaging.

### Architecture

- **Trading engine** -- Python main loop with multiple strategies
- **Dashboard** -- Next.js localhost monitoring UI
- **Control API** -- HTTP endpoints for remote management
- **Signal bridge** -- Control the bot via Signal messages

### Strategies

1. AI Divergence -- LLM-based market analysis
2. Negrisk Arbitrage -- Negative risk arbitrage
3. Resolution Farming -- Near-resolution market opportunities
4. Penny Picks -- Low-probability high-reward bets
5. Copy Trade -- Follow smart wallet traders

### Safety Features

- Kill switch (balance, daily loss, API spend limits)
- Paper trading mode with readiness evaluation
- Paper-to-live criteria: 25+ trades, 2+ strategies, +2% P&L, <10% drawdown
- All decisions logged to SQLite for auditability

### Tech Stack

- Python (core engine), Next.js (dashboard)
- SQLite for logging, Polygon RPC for blockchain
- Anthropic API for AI strategies
- Signal CLI for remote control

### Complexity Level

Very high. Blockchain, trading strategies, Kelly sizing, wallet intelligence. Requires financial and technical knowledge.

### Potential Course Module

**"Build a Trading Bot Dashboard with AI"** -- focuses on the dashboard/monitoring aspect, not the trading logic. Shows how to build a real-time monitoring UI for any automated system. Could also be **"AI for Trading: Paper Mode to Live"** for advanced users.

### Key Files

- `/Users/mateuszjez/projects/polymarket-bot/README.md` -- Complete documentation
- `/Users/mateuszjez/projects/polymarket-bot/src/strategies/` -- 5 trading strategies
- `/Users/mateuszjez/projects/polymarket-bot/dashboard/` -- Next.js monitoring UI

---

## 9. COS DASHBOARD

### What It Is

A shared dashboard between Matt and "Charlie" (likely a business partner/collaborator). It tracks their working relationship, daily logs, projects, lessons learned, playbooks, AI insights, and parked items. Built as a Next.js app deployed to production.

### Design Principles

1. **No assumptions** -- Never add anything Charlie didn't actually say
2. **5-Point Validation Gate** -- Every item must pass: factually correct, still true, Matt's responsibility, real task (not ongoing behavior), right time
3. **Full dashboard sweep on every update** -- Review ALL sections for stale data when changing anything
4. **Auto-push** -- Commit and push immediately after any changes
5. **Never destructively modify data** -- Make types more flexible, never delete entries

### Architecture

- Single source of truth: `src/data/state.json`
- UI component: `src/components/dashboard.tsx`
- Tabs: NOW, Projects, Playbooks, AI Insights, Timeline, Parked

### Tech Stack

- Next.js, TypeScript, Tailwind, shadcn/ui
- Static JSON data file (no database)
- Vercel hosting

### Complexity Level

Low-medium. Simple data structure, but sophisticated operational rules for keeping data clean.

### Potential Course Module

**"Build a Collaboration Dashboard for Your Team"** -- how to create a shared visibility tool for working relationships, with rules for data integrity.

### Key Files

- `/Users/mateuszjez/projects/cos-dashboard/CLAUDE.md` -- Rules and architecture
- `/Users/mateuszjez/projects/cos-dashboard/src/data/state.json` -- All dashboard data

---

## 10. CROSS-PROJECT DESIGN PATTERNS

### Pattern 1: The Pillar Framework

**Used in:** How To Find Talent, Dream Job Program, Talent Scout AI

Structure knowledge into sequential pillars where each builds on the previous. Each pillar has:
- A core insight (one sentence)
- Philosophy/overview
- Templates (blank forms)
- SOPs (step-by-step instructions)
- Examples (completed real-world instances)
- Deliverables (specific artifacts the user creates)

### Pattern 2: Chat-as-Interface

**Used in:** LandAJobCoach, Talent Scout AI, Life Tracking Buddy, AI Performance Orchestrator

The chat window IS the product. No forms, no complex navigation. Users accomplish everything through conversation. This pattern appears across 4 of Matt's 8 projects.

### Pattern 3: Commands Are Sacred, AI Is Cosmetic

**Used in:** Life Tracking Buddy, Life Tracking Buddy Bot, AI Performance Orchestrator

Core operations run through deterministic pattern matching. AI only adds personality to responses. If AI fails, the core system still works. This is a hard-won lesson from the AI Performance Orchestrator's 60% pass rate.

### Pattern 4: PRD-Driven Development (Ralph Loop)

**Used in:** EVERY project with code

Every project has a `prd.json`, `CLAUDE.md`, and/or `AGENTS.md`. Tasks are tracked as `passes: true/false`. AI agents work through tasks one at a time. This is Matt's fundamental workflow for building with AI.

### Pattern 5: Progressive Disclosure

**Used in:** Dream Job Program (modules unlock sequentially), Talent Scout AI (pillars unlock in order), How To Find Talent (pillar progression)

Users cannot skip ahead. Each level must be completed before the next is available. This prevents overwhelm and ensures foundational concepts are internalized.

### Pattern 6: Familiar But Surprising (FBS)

**Used in:** Dream Job Program (outreach module), How To Find Talent (outreach framework), Talent Scout AI (outreach templates)

The FBS framework is Matt's signature concept: reference something specific about the recipient that most people would miss. It appears in both the hiring playbook (recruiter outreach) and the job-seeking guide (candidate outreach). The "WTF Test" validates FBS quality.

### Pattern 7: Proof Before Hire / Prove Before Claiming

**Used in:** Dream Job Program (Trial Run Project), How To Find Talent (Discovery Projects), Talent Scout AI (Discovery Project builder)

Both sides of the hiring equation use the same principle: prove you can do the work before anyone commits. Job seekers build trial projects. Companies design discovery projects. Matt uses this concept in both his hiring and job-seeking methodologies.

### Pattern 8: Document Everything, Let AI Learn From It

**Used in:** Every project via AGENTS.md "Learned" sections

When AI makes a mistake, Matt adds a rule to AGENTS.md so it never happens again. This compounds over time. The AI Coding Workflow explicitly states: "Bad output = bad input. When AI makes the same mistake twice, add a rule to AGENTS.md."

---

## 11. COURSE CONTENT MAPPING

### Full Mapping: Projects to Potential Course Modules

| Project | Module Title | Difficulty | Audience | Prerequisite |
|---------|-------------|------------|----------|-------------|
| AI Coding Workflow | **The AI Coding Workflow: Ship Code While You Sleep** | Beginner-Intermediate | Anyone who codes with AI | Basic familiarity with terminal |
| Andre Prep Site | **Build a Meeting Prep Tool in 10 Minutes** | Beginner | Anyone | None |
| CoS Dashboard | **Build a Team Collaboration Dashboard** | Beginner-Intermediate | Managers, founders | Basic understanding of web apps |
| Life Tracking Buddy | **Build a Chat-Based Productivity Tracker** | Intermediate | Builders | Basic coding knowledge |
| Life Tracking Buddy (production) | **Ship to Production Like a Pro** | Intermediate | Builders | Has built an app |
| Life Tracking Buddy Bot | **Add AI to Any App Without Breaking It** | Intermediate | Builders | Has a working app |
| How To Find Talent | **Turn Your Expertise Into a Playbook Website** | Beginner-Intermediate | Domain experts | Has domain knowledge to share |
| LandAJobCoach | **Build an AI Coach From Your Content** | Intermediate-Advanced | Content creators | Has existing content (docs/videos) |
| Talent Scout AI | **Build an AI Product That Follows a Methodology** | Advanced | Product builders | Understands AI basics |
| AI Performance Orchestrator | **Fine-Tuning AI: What I Learned From 2,461 Examples** | Advanced | AI enthusiasts | Understands API calling |
| Polymarket Bot | **Build a Trading Bot Dashboard** | Advanced | Traders, quant-curious | Python + finance basics |
| Dream Job Program | **How to Package Expertise Into a Course** | Meta-module | Course creators | Has expertise to package |

### Recommended Course Sequence (Beginner to Advanced)

**Week 1-2: Foundations**
1. The AI Coding Workflow (Ralph Loop, PRDs, AGENTS.md)
2. Build a Meeting Prep Tool in 10 Minutes (quick win, builds confidence)

**Week 3-4: Building Real Things**
3. Build a Chat-Based Productivity Tracker (pattern matching, databases)
4. Build a Team Collaboration Dashboard (data architecture, deployment)

**Week 5-6: Adding AI**
5. Add AI to Any App Without Breaking It (3-layer architecture, feature flags)
6. Build an AI Coach From Your Content (RAG, vector search, content sync)

**Week 7-8: Productizing Expertise**
7. Turn Your Expertise Into a Playbook Website (pillar framework, content architecture)
8. How to Package Expertise Into a Course (meta-module: Dream Job Program as case study)

**Advanced Tracks (Optional)**
9. Build an AI Product That Follows a Methodology (function calling, progressive disclosure)
10. Fine-Tuning AI: Lessons from 2,461 Examples (what works, what fails)
11. Build a Trading Bot Dashboard (real-time monitoring, automated systems)

### The Meta-Narrative

Matt's projects tell a clear story: **Take domain expertise, build AI-powered tools around it, and ship to production.** Every project follows this arc:

1. Matt has deep expertise (recruiting, job coaching, productivity)
2. He documents that expertise into structured frameworks (pillars, modules, playbooks)
3. He builds AI-powered tools that embody the frameworks (chatbots, product tools, dashboards)
4. He uses AI to build the tools themselves (Ralph Loop, PRD-driven development)

This IS the course: **"How to Turn What You Know Into AI-Powered Products."**

---

## APPENDIX: Project Inventory Summary

| Project | Path | Tech | Status |
|---------|------|------|--------|
| LandAJobCoach | `/Users/mateuszjez/projects/landajobcoach/` | Next.js, Supabase, Gemini, pgvector | Active |
| Dream Job Guide | `/Users/mateuszjez/Desktop/dream-job-guide-extracted.txt` | PDF (133 pages) | Complete |
| Dream Job Benchmarks | `/Users/mateuszjez/Desktop/Dream-Job-Benchmarks/` | Markdown analysis docs | Complete |
| How To Find Talent | `/Users/mateuszjez/Desktop/howtofindtalent/` | Next.js, static playbook | Active |
| Talent Scout AI | `/Users/mateuszjez/Desktop/talent-scout-ai/` | Next.js, Supabase, Gemini, Playwright | Active (Phase 17) |
| Andre Prep Site | `/Users/mateuszjez/Desktop/andre-prep-site/` | Single HTML file | Complete |
| Life Tracking Buddy | `/Users/mateuszjez/projects/life-tracking-buddy/` | Next.js, Supabase, Drizzle, Sentry | Production |
| Life Tracking Buddy Bot | `/Users/mateuszjez/projects/lifetrackingbuddybot/` | Next.js, OpenAI | In progress |
| AI Performance Orchestrator | `/Users/mateuszjez/projects/ai-performance-orchestrator/` | Next.js, fine-tuned GPT-4o-mini | Pre-MVP |
| Polymarket Bot | `/Users/mateuszjez/projects/polymarket-bot/` | Python, Next.js dashboard | Active |
| CoS Dashboard | `/Users/mateuszjez/projects/cos-dashboard/` | Next.js, static JSON | Production |
| AI Coding Workflow | `/Users/mateuszjez/Desktop/AI-CODING-WORKFLOW.md` | Documentation | Complete |
| Recruiting Playbook (source) | `/Users/mateuszjez/Desktop/wispr-flow-dream-job-application/mattsrecruitingplaybook/` | Markdown docs | Complete |
