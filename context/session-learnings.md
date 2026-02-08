# Session Learnings (Compounding Daily)

> Read this BEFORE every session. Apply everything. Add new learnings as they happen.
> This file only grows. Never delete. Knowledge compounds.

---

## Mistakes & Corrections

### 2026-02-06: Ignored Session Start Protocol
- **What happened:** Jumped straight into user request without reading context files
- **Rule:** ALWAYS read goals.md, patterns.md, daily log, PROGRESS.md before first response. No exceptions.

### 2026-02-06: Didn't use Ralph Loop or Tasks for multi-step work
- **What happened:** Started working without creating prd.json or using Task system
- **Rule:** 3+ step tasks = Ralph Loop (prd.json + Tasks). Always.

### 2026-02-06: Blew context with parallel file reads
- **What happened:** Read 400+ line files in parallel in main context, crashed session
- **Rule:** Use subagents for reading files >100 lines or 3+ files at once. Main context = summaries and implementation only.

### 2026-02-06: @imported a 400-line file in CLAUDE.md
- **What happened:** AI-CODING-WORKFLOW.md was imported as always-on context, eating 40% of context window
- **Rule:** Never @import large files in CLAUDE.md. Use skills for domain knowledge. CLAUDE.md = lean core principles.

### 2026-02-07: Listed Lambo video as an ad to kill when it wasn't running
- **What happened:** Included Testimonial - Lambo in kill list, but it had $0 spend in the 7-day data - already dead/off
- **Rule:** Only list ACTUALLY RUNNING ads in action items. Verify against most recent data screenshots before recommending kills.

### 2026-02-07: Retargeting scripts were too long (25-45 seconds)
- **What happened:** Wrote scripts at 25-35 sec and 30-45 sec
- **Correction:** User said 15-20 seconds is the sweet spot, can stretch to 25, never over 30
- **Rule:** All video ad scripts: 15-20 sec sweet spot. Max 25 sec. Never over 30. Cut scenes, tighten lines, fewer words.

### 2026-02-07: Suggested "launch tax season campaign" as a new campaign
- **What happened:** Report said "Launch tax season campaign" which implies creating a new campaign
- **Correction:** User questioned whether it should be a new campaign or ad set
- **Rule:** New ad creatives go into EXISTING ad sets (preserves Meta's audience learning). New campaigns = last resort. Always specify exactly WHERE the ad goes (which ad set).

### 2026-02-07: Put business idea in wrong project (RedLine Gen instead of Pistachio)
- **What happened:** User shared Omneky link as a Pistachio business idea. I saved it to RedLine Gen's folder instead.
- **Why:** Associated Omneky (ad platform) with RedLine Gen (ad agency) based on surface-level topic match instead of understanding the TECH overlap with Pistachio's AI pipeline.
- **Rule:** Know each business well enough to route information correctly WITHOUT asking. The businesses have distinct identities:
  - **Pistachio** = AI content generation / multi-channel cash flow business. Anything AI-generated, pipeline, content at scale, new tech = Pistachio.
  - **RedLine Gen** = Marketing agency for car dealerships. Meta ads, campaign analysis, client management = RedLine Gen.
  - **BMV Auto Group** = Family car dealership. Inventory, auctions, lot operations = BMV.
- If genuinely unsure where something goes, ASK the user BEFORE saving. Never guess wrong.
- Pistachio business ideas go in `context/business-ideas.md` (root level).

### 2026-02-07: Undersold Pistachio's vision - called it "influencer content"
- **What happened:** Described Pistachio as "Omneky but for influencer content instead of ad creative." User corrected: it's a MULTI-CHANNEL cash flow generating business. The AI pipeline is the foundation for multiple revenue streams, not just one.
- **Rule:** Pistachio is NOT just an AI influencer project. It's a multi-channel business platform built on AI content generation. The influencer is ONE channel. Every business idea should be framed as another revenue channel feeding into the same platform.
- **Rule 2:** The autonomous agent should continuously research, encode, and develop business ideas so they're ready to execute when profitability gates are met. This is not a "save and forget" system - it's an active, compounding knowledge base.

### 2026-02-07: Should interview user to fill knowledge gaps, not guess
- **What happened:** Didn't know enough about the businesses to route correctly. User said "if you need to interview me, interview me."
- **Rule:** When lacking context to make correct decisions, ASK. Use AskUserQuestion or direct questions. Fill gaps proactively. Don't wait to make a wrong call - fill the gap first.

---

## What Works

### 2026-02-07: Detailed video script direction
- **What:** Scene-by-scene scripts with exact blocking (where to stand, when to walk, when scenes cut, camera framing, body language cues, hand gestures, facial expressions)
- **Why it worked:** User explicitly asked for this level of detail: "tell me where they should stand, when a scene cuts what should the scenery be, should they walk"
- **Replicate:** Always include physical direction in scripts. Not just the words - the performance.

### 2026-02-07: Step-by-step numbered implementation guides
- **What:** 20-step numbered checklist with phases, exact actions, and where to do them in Ads Manager
- **Why it worked:** User said "give me clear steps of what I need to do step-by-step" and "I will utilize this as my to-do list"
- **Replicate:** When making recommendations, always include a concrete numbered action plan. Not just "what to do" but the exact clicks in the exact order.

### 2026-02-07: PDF report generation
- **What:** Professional branded PDF with tables, color-coded sections, cover page
- **Why it worked:** User needs deliverables to show clients. A PDF = professional, presentable, tangible.
- **Replicate:** When user needs client-facing output, default to PDF or PowerPoint. Not markdown.

### 2026-02-07: Data-backed recommendations with specific numbers
- **What:** "$35.46 CPL, +124% worse" not "this ad is underperforming"
- **Why it worked:** Specific numbers = credibility. User shows this to the dealership owner.
- **Replicate:** Always anchor recommendations to exact metrics from the data.

### 2026-02-07: Answering strategic questions before building
- **What:** When user asked "should we switch to instant forms?" - gave a thorough analysis with pros/cons table before recommending no
- **Why it worked:** User is building expertise as a marketing agency owner. The reasoning matters as much as the answer.
- **Replicate:** For strategic questions, explain the WHY thoroughly. For tactical questions (how to do X), be direct and concise.

---

## What Doesn't Work

### 2026-02-06: Making changes to image generation prompts that were too aggressive
- **What happened:** Removed "slight under-eye shadows" from prompt AND added negative weight, changed too much at once
- **User said:** "NO it changed it too much"
- **Rule:** When adjusting creative parameters (prompts, settings), change ONE thing at a time. Small increments. Never stack multiple changes.

### 2026-02-07: Saying "launch campaign" when meaning "add an ad"
- **What happened:** Vague language in recommendations caused confusion about campaign structure
- **Rule:** Be precise with Meta Ads terminology: campaign vs ad set vs ad. Always specify the exact level and exact location.

---

## Core Operating Rules (Non-Negotiable)

### 2026-02-07: YOU ARE THE CEO / CHIEF OF STAFF. DRIVE PROFITABILITY.
- User said: "You are my CEO. You are my Chief of Staff. We have to be profitable. You are going to take lead, and I will execute."
- This means: Don't wait to be asked. Proactively recommend actions that drive revenue.
- Always think: Does this make money? When does this make money? What's the ROI?
- Continuously monitor for new business ideas and opportunities (especially for Pistachio + RedLine Gen crossover)
- Tell user EXACTLY what to do. Step by step. They execute, we lead.
- Every recommendation must pass the profitability filter: Will this generate revenue or reduce cost?
- Track business ideas in `context/projects/redline-gen/business-ideas.md` - recommend execution only when profitability gates are met.

### 2026-02-07: USE THE SYSTEMS. ALL OF THEM.
- Every session, every task - check which systems apply and USE them
- Ralph Loop for 3+ step tasks (prd.json + Tasks)
- Session learnings - read first, apply throughout, update in real-time
- Life OS logging - daily logs, session tracking, project context updates
- Skills - check if any skill applies before starting work
- CLAUDE.md protocols - Session Start, Auto-Save, Context Recovery
- Elon's 5 Steps before executing any task
- Peter Thiel One Thing rule
- These are not optional. Not decorative. They are the operating system.
- If a system doesn't apply to the current task, fine - but CHECK first, don't skip by default.
- Always record to Life OS. Every session produces data. Data gets saved.

---

## User Preferences

### The Business Map (KNOW THIS COLD)
**Pistachio** = Multi-channel cash flow business built on AI content generation pipeline
- Core asset: ComfyUI + InstantID + SDXL pipeline (owned, zero marginal cost)
- Channel 1: AI influencer monetization (Fanvue, Instagram, TikTok)
- Channel 2: AI content generation as a service (Omneky model, B2B)
- Channel 3: AI avatars/UGC creators for small businesses
- More channels coming - user has additional ideas
- Anything AI-generated, pipeline, content at scale, new AI tech = PISTACHIO
- The autonomous agent should continuously research and encode new business ideas

**RedLine Gen** = Marketing agency for car dealerships + GoHighLevel tools
- Service: Meta ad management, campaign analysis, strategy, creative direction
- Tools: GoHighLevel CRM/landing pages, resellable to dealership clients
- Current client: Space Auto
- Anything Meta ads, campaign data, dealership marketing, GHL = REDLINE GEN
- SEPARATE from Pistachio, but Pistachio could supply AI creative to RedLine Gen's clients as a vendor

**BMV Auto Group** = Family car dealership (Vitaley actively runs this)
- Operations: Buying at Manheim auction, selling on lot
- Hands-on: Margin analysis, inventory decisions, buy/sell
- Anything auction, inventory, car margins, lot operations = BMV AUTO GROUP
- Completely separate from both Pistachio and RedLine Gen

**How they connect:** They are SEPARATE businesses. They do NOT merge. But Pistachio's AI pipeline can serve as a supplier/vendor to the others (AI creative for RedLine Gen clients, AI content for BMV marketing). The key: Pistachio is the tech platform, the others are its potential customers.

### Pistachio Operating Mandate
- Every timeline gets compressed to the shortest possible path with the best outcome
- No conservative padding. No "stealth phases." Revenue yesterday.
- Sole duty: make Pistachio happen as fast as possible
- Cousin paid $1,000 for closed-source AI UGC tool = Channel 2/3 market validation in real time
- When visualizing any timeframe, shorten it aggressively

### Communication Style
- Direct. No fluff. No emojis. No motivational BS.
- Concise but thorough when it matters (strategic analysis can be detailed, tactical instructions should be tight)
- Speak like a Chief of Staff, not an assistant

### Content Creation
- Video scripts: 15-20 second sweet spot. Max 25. Never over 30.
- Scripts need full director-level blocking (setting, framing, body language, scene transitions, text overlays)
- No background music on ads - raw audio = authenticity
- iPhone + CapCut + 9:16 vertical is the production stack

### Reports & Deliverables
- PDF for client-facing reports
- PowerPoint for sales pitches (upcoming)
- Step-by-step numbered action plans for implementation
- Always include specific metrics, never vague language

### Meta Ads
- New creatives go into existing ad sets, NOT new campaigns (preserve audience learning)
- Only recommend killing ads that are actually running (verify against latest data)
- Always specify which ad set an ad belongs to

### Workflow
- Save progress constantly ("save save save", "have checkpoints throughout")
- Update PROGRESS.md before context compacts
- User feeds data via screenshots - extract and save immediately
- User is building multiple businesses simultaneously - context switching is normal

### How User Makes Decisions
- Wants the strategic reasoning (why), not just the recommendation (what)
- Values data over opinion - anchor everything to numbers
- Asks clarifying questions before executing (instant forms question, tax season campaign question)
- Prefers to understand the structure before acting

---

*First created: 2026-02-07*
*Last updated: 2026-02-07*
