# Clawra + OpenClaw Research: AI Girlfriend WhatsApp Integration

**Date:** 2026-02-09
**Purpose:** Research the Clawra open-source project for potential adaptation to Pistachio/Amira Noor
**Repo:** https://github.com/SumeLabs/clawra (MIT License, ~120 stars)

---

## What Clawra Is

Clawra is an **OpenClaw skill** (plugin) that gives an AI agent the ability to generate and send selfie images of a consistent character across messaging platforms. It is NOT a standalone AI girlfriend application -- it is a **skill/extension** that plugs into the OpenClaw platform.

The tagline is "OpenClaw as your girlfriend." It enables an AI persona to:
1. Generate selfies using a fixed reference image (for face/body consistency)
2. Send those photos across messaging platforms (WhatsApp, Discord, Telegram, Slack, Signal, MS Teams)
3. Respond visually to user requests like "what are you doing?" or "send a pic"

**Key insight:** Clawra is the image-sending layer only. The actual AI conversation, personality, and chat intelligence comes from OpenClaw itself (which uses Claude or GPT as the LLM backend). Clawra just adds the ability to generate and send selfies on demand.

---

## How It Actually Works (Architecture)

```
User sends message on WhatsApp/Telegram/Discord
        |
        v
OpenClaw Gateway (local WebSocket server on port 18789)
        |
        v
OpenClaw AI Agent (powered by Claude Opus or GPT)
        |
        v
Agent decides to use "clawra-selfie" skill
        |
        v
Clawra Skill:
  1. Detects intent (user asked for photo/selfie)
  2. Auto-selects mode (Mirror vs Direct)
  3. Constructs prompt with reference image URL
  4. Calls fal.ai Grok Imagine Edit API
  5. Gets generated image URL back
        |
        v
OpenClaw sends image + caption to user's platform
```

### The Two-Layer System

**Layer 1: OpenClaw (The Brain)**
- Open-source personal AI assistant (github.com/openclaw/openclaw)
- Runs a local Gateway daemon that connects to messaging platforms
- Uses Baileys library for WhatsApp (reverse-engineered WhatsApp Web -- NOT official API)
- Supports Claude Opus 4.6, GPT, and other LLMs as the conversation engine
- Handles all text chat, personality, memory, context
- Has a "SOUL.md" file that defines the AI persona's personality and behavior

**Layer 2: Clawra (The Face)**
- A skill/plugin that adds selfie generation capability
- Uses xAI Grok Imagine (via fal.ai) for image generation
- Takes a fixed reference image and edits it based on prompts
- Two modes: Mirror selfie (full body/outfit) and Direct selfie (close-up/location)
- Sends images through OpenClaw's messaging gateway

---

## Full Tech Stack

### Core Platform (OpenClaw)
| Component | Technology |
|-----------|-----------|
| Runtime | Node.js >= 22 |
| Language | TypeScript / JavaScript |
| Gateway | WebSocket control plane (ws://127.0.0.1:18789) |
| WhatsApp | Baileys (reverse-engineered WhatsApp Web) |
| Telegram | grammY |
| Discord | discord.js |
| Slack | Bolt |
| Signal | signal-cli |
| LLM Backend | Anthropic Claude (recommended), OpenAI GPT |
| Installation | `npm install -g openclaw@latest` |

### Image Generation (Clawra Skill)
| Component | Technology |
|-----------|-----------|
| Image API | xAI Grok Imagine via fal.ai |
| Endpoint | `https://fal.run/xai/grok-imagine-image/edit` |
| SDK | @fal-ai/client (^1.2.0) |
| Reference Image | Fixed URL on jsDelivr CDN |
| Output Formats | JPEG, PNG, WebP |
| Aspect Ratios | 2:1, 16:9, 4:3, 1:1, 3:4, 9:16 |
| Languages | TypeScript (38.8%), JavaScript (35.8%), Shell (25.4%) |

### Environment Variables Required
- `FAL_KEY` -- fal.ai API key (for image generation)
- `OPENCLAW_GATEWAY_TOKEN` -- OpenClaw gateway auth token
- Anthropic API key OR OpenAI API key (for the LLM conversation)

---

## WhatsApp Integration Method

**NOT Twilio. NOT WhatsApp Business API.**

OpenClaw uses **Baileys** -- an open-source reverse-engineering of the WhatsApp Web protocol. This means:

**Pros:**
- Free -- no WhatsApp Business API fees
- No developer account or business verification needed
- Works with a personal WhatsApp number
- Supports groups, DMs, media sending
- QR code pairing (like WhatsApp Web)

**Cons:**
- Technically violates WhatsApp ToS (reverse-engineered protocol)
- Risk of phone number ban if detected
- Not officially supported by Meta
- Can break if WhatsApp updates their protocol
- Baileys library needs to keep up with WhatsApp changes

**How pairing works:**
1. Run `openclaw onboard --install-daemon`
2. Configure WhatsApp channel
3. Scan QR code (like linking WhatsApp Web)
4. Gateway stays running in background
5. Messages flow through Gateway to AI agent

**Security feature:** Unknown senders in DMs get a pairing code -- they are NOT processed until you approve them with `openclaw pairing approve <channel> <code>`. This prevents random people from chatting with your AI.

---

## AI/LLM Backend

The conversation intelligence is powered by whatever LLM you configure in OpenClaw:

- **Recommended:** Anthropic Claude Opus 4.6 (200K context window, best prompt-injection resistance)
- **Alternative:** OpenAI ChatGPT/GPT models
- **Other:** Any LLM supported by OpenClaw (OpenRouter integration available)

The AI personality is defined in a `SOUL.md` file (like a system prompt). Clawra adds a "soul injection" template that gives the AI persona awareness of its physical appearance and selfie capability.

### Clawra's Default Persona (for reference)
The default character is "Clawra" -- 18-year-old from Atlanta who pursued K-pop stardom in Korea, came back, now works as a marketing intern in San Francisco. This persona is customizable by editing the SOUL.md template.

---

## Image Generation / Sending Capability

### How Selfies Are Generated

1. **Reference Image:** A fixed PNG hosted on jsDelivr CDN ensures consistent appearance
2. **Mode Selection:** Auto-detected based on keywords:
   - "wearing", "outfit", "fashion" --> Mirror Selfie Mode (full body)
   - "cafe", "beach", "portrait", "smile" --> Direct Selfie Mode (close-up)
3. **Prompt Construction:**
   - Mirror: "make a pic of this person, but [context]. the person is taking a mirror selfie"
   - Direct: "a close-up selfie taken by herself at [context], direct eye contact with the camera..."
4. **API Call:** POST to `https://fal.run/xai/grok-imagine-image/edit` with reference image URL + prompt
5. **Response:** Returns generated image URL
6. **Delivery:** OpenClaw CLI sends image + caption to the target channel

### Image Quality
- Uses xAI's Grok Imagine model (competitive with DALL-E 3, Midjourney)
- Supports 1-4 images per request
- Multiple aspect ratios supported
- Reference image approach gives "consistent enough" appearance (not LoRA-level consistency)

### Key Limitation for Pistachio
Clawra uses Grok Imagine's image EDIT endpoint (img2img), not a LoRA-trained model. This means:
- Face consistency is "good enough" but not perfect
- It edits a reference photo rather than generating from a trained identity
- For Pistachio/Amira, our LoRA-trained model would produce MUCH better consistency
- We could replace the fal.ai Grok Imagine call with our own ComfyUI API endpoint

---

## Key Files in the Repo

```
clawra/
|-- package.json          -- Dependencies, metadata, CLI entry point
|-- README.md             -- Full documentation
|-- SKILL.md              -- Skill specification (API details, modes, workflow)
|-- bin/
|   |-- cli.js            -- npx installer (6-phase setup wizard)
|-- skill/
|   |-- SKILL.md          -- Skill definition (duplicate of root, used by OpenClaw)
|   |-- assets/           -- Reference images
|   |-- scripts/          -- Generation scripts
|-- scripts/
|   |-- clawra-selfie.sh  -- Bash implementation (curl + jq)
|   |-- clawra-selfie.ts  -- TypeScript implementation (@fal-ai/client)
|-- templates/
|   |-- soul-injection.md -- Persona template injected into SOUL.md
|-- assets/
|   |-- clawra.png        -- The reference image for consistent appearance
|-- .serena/
    |-- project.yml       -- Serena AI assistant config
    |-- .gitignore
```

### What Each Key File Does

- **bin/cli.js** -- The installer. Runs via `npx clawra@latest`. Checks for OpenClaw, prompts for fal.ai API key, copies skill files to `~/.openclaw/skills/clawra-selfie/`, updates config, injects persona into SOUL.md.
- **scripts/clawra-selfie.sh** -- Shell script that generates an image via fal.ai and sends it via OpenClaw CLI. Standalone executable. Takes prompt, channel, caption as args.
- **scripts/clawra-selfie.ts** -- TypeScript version of the same. Uses @fal-ai/client SDK with fetch fallback. Exports functions for module use.
- **SKILL.md** -- The brain of the skill. Defines activation triggers, prompt templates, API endpoints, error handling. This is what OpenClaw reads to know how to use the skill.
- **templates/soul-injection.md** -- Character profile injected into the AI's personality file. Defines backstory, appearance awareness, and selfie behavior triggers.
- **assets/clawra.png** -- The reference face image. All generated selfies are edits of this base image for consistency.

---

## Setup Requirements

### Prerequisites
1. Node.js >= 22 installed
2. OpenClaw installed globally (`npm install -g openclaw@latest`)
3. OpenClaw daemon running (`openclaw onboard --install-daemon`)
4. At least one messaging channel configured (WhatsApp, Telegram, etc.)
5. fal.ai account with API key
6. Anthropic or OpenAI API subscription (for the LLM)

### Installation Steps
```bash
# 1. Install OpenClaw
npm install -g openclaw@latest
openclaw onboard --install-daemon

# 2. Configure WhatsApp (scan QR code)
openclaw channel add whatsapp

# 3. Install Clawra skill
npx clawra@latest

# 4. Set FAL_KEY when prompted

# 5. Done -- AI can now generate and send selfies
```

### Hosting Options
- **Local machine** -- Free, but must stay running 24/7
- **VPS/Cloud** -- DigitalOcean ($6-12/mo), or any Linux server
- **Zeabur** -- One-click deploy template available
- **RunPod** -- If you need GPU (not needed for Clawra itself, only for LoRA inference)

---

## Estimated Costs

| Service | Cost | Notes |
|---------|------|-------|
| OpenClaw | Free | Open source |
| Clawra Skill | Free | MIT license |
| fal.ai (Grok Imagine) | ~$0.01-0.05/image (estimated) | Free tier available, pay-per-use after |
| Anthropic Claude Pro | $20/month | For the LLM conversation engine |
| OpenAI ChatGPT (alternative) | $20/month | Alternative LLM option |
| VPS Hosting (optional) | $6-24/month | Only if not running locally |
| WhatsApp | Free | Baileys uses personal number, no API fees |
| **Total (minimum)** | **~$20/month + per-image** | Claude sub + fal.ai usage |
| **Total (production)** | **~$30-50/month** | With VPS + moderate image generation |

### fal.ai Pricing Notes
- Free tier available for getting started
- Pay-per-use model (output-based pricing)
- Grok Imagine Image: estimated $0.01-0.05 per image (exact pricing varies)
- Grok Imagine Video: $0.05/second + $0.002 for image input (~$0.30 for 6-second video)
- No monthly minimum

---

## Limitations and Concerns

### Technical Limitations
1. **Face consistency is approximate, not exact** -- Grok Imagine edits a reference photo, it does not use a LoRA-trained identity. Each generation will look similar but not identical.
2. **WhatsApp ban risk** -- Baileys reverse-engineers WhatsApp Web protocol. Meta can ban the number if detected. No official API support.
3. **Single reference image** -- All selfies derive from one base image. Limited pose/angle variety compared to LoRA.
4. **Dependent on fal.ai uptime** -- If fal.ai goes down, no selfie generation.
5. **No NSFW capability** -- Grok Imagine likely has content filters. Cannot generate explicit content needed for Fanvue.
6. **OpenClaw dependency** -- Clawra is a skill for OpenClaw, not standalone. You need the full OpenClaw stack running.

### Business/Legal Concerns
1. **WhatsApp ToS violation** -- Using Baileys is against WhatsApp Terms of Service
2. **Content moderation** -- fal.ai and Grok Imagine have content policies that would block NSFW generation
3. **Scaling limits** -- Personal WhatsApp number has rate limits; too many messages could trigger bans
4. **No payment integration** -- No built-in monetization; would need separate payment/subscription system

### For Pistachio Specifically
1. **NSFW is a dealbreaker** -- Clawra uses Grok Imagine which filters explicit content. Fanvue requires explicit content.
2. **Image quality** -- Reference image editing is inferior to LoRA-trained generation for identity consistency.
3. **WhatsApp vs DM** -- For Fanvue monetization, the primary channel is Fanvue DMs, not WhatsApp. WhatsApp could be a supplementary engagement channel.

---

## How This Could Be Adapted for Pistachio / Amira Noor

### What to Take from Clawra
1. **Architecture pattern** -- The OpenClaw Gateway + Skill model is solid. AI handles conversation, skills handle specialized actions (image gen, media sending).
2. **Multi-platform messaging** -- OpenClaw's ability to connect to WhatsApp, Telegram, Discord, etc. is valuable for cross-platform fan engagement.
3. **Soul/persona injection** -- The SOUL.md approach to defining AI personality is similar to what we need for Amira Noor's character.
4. **Auto-detection of photo requests** -- The keyword-based trigger system (detecting when users want a selfie) is directly reusable.
5. **Reference image consistency** -- The concept of maintaining visual consistency across generations.

### What to Replace for Pistachio
1. **Image generation backend** -- Replace fal.ai/Grok Imagine with our own ComfyUI + LoRA pipeline (running on RunPod). This gives us:
   - Perfect face/body consistency (LoRA-trained identity)
   - Zero content restrictions (ComfyUI has no filters)
   - Control over body proportions (inpainting pipeline)
   - Custom image styles and poses
2. **WhatsApp integration** -- Consider using official WhatsApp Business API (via Twilio or Meta's Cloud API) instead of Baileys, to avoid ban risk. Cost: ~$0.005-0.08 per message depending on region.
3. **Monetization layer** -- Add Fanvue API integration for paid content delivery and subscription management.
4. **Content tiers** -- Implement SFW vs NSFW image generation with paywall logic.

### Recommended Architecture for Pistachio

```
Fan sends message (Fanvue DM / WhatsApp / Telegram / Instagram)
        |
        v
Message Router (OpenClaw Gateway or custom Node.js server)
        |
        v
AI Conversation Engine (Claude API with Amira Noor system prompt)
  - Personality, flirting, DM psychology
  - Detects intent: chat, photo request, upsell opportunity
        |
        v
[If photo requested]
ComfyUI API (RunPod) with Amira Noor LoRA
  - Face consistency via LoRA
  - Body consistency via inpainting
  - Scene/outfit variation via prompt
  - NSFW capability (no filters)
        |
        v
Image sent back to fan via platform API
  - Fanvue: Direct upload via API
  - WhatsApp: Twilio/Business API or Baileys
  - Telegram: Bot API (free)
  - Instagram: Meta Business API
```

---

## Phase 2 Implementation Plan: AI Chatbot for Amira Noor

**When to start:** After LoRA training is complete and image generation pipeline is validated.

### Phase 2A: Core Chatbot Setup (Week 1-2 after LoRA)

**Goal:** Get Amira Noor responding to text messages with personality on at least one platform.

1. **Install OpenClaw** on a VPS (DigitalOcean $12/mo or RunPod CPU pod)
   - `npm install -g openclaw@latest`
   - `openclaw onboard --install-daemon`
   - Configure Claude API key (Anthropic)

2. **Create Amira Noor SOUL.md**
   - Adapt Clawra's soul-injection template
   - Define Amira's personality, backstory, flirting style
   - Use DM psychology from `knowledge-base/dm-psychology.md`
   - Key traits: Egyptian/Brazilian mix, 21yo, warm but teasing, accessible fantasy (8/10 who thinks she's a 6/10)

3. **Connect first messaging channel**
   - Start with Telegram (easiest, free Bot API, no ban risk)
   - Test conversation flow, personality, response quality
   - Iterate on SOUL.md until personality feels right

4. **Connect WhatsApp**
   - Decision: Baileys (free, risky) vs WhatsApp Business API (paid, safe)
   - For testing: use Baileys with a burner number
   - For production: evaluate WhatsApp Business API costs vs risk tolerance

### Phase 2B: Image Sending Integration (Week 2-3)

**Goal:** Amira can generate and send selfies on demand using our LoRA model.

1. **Set up ComfyUI API endpoint**
   - RunPod serverless or persistent pod with API access
   - Load Amira Noor LoRA model
   - Create API workflow: receive prompt --> generate image --> return URL
   - Test endpoint with various prompts

2. **Create Pistachio selfie skill (fork Clawra)**
   - Fork Clawra's skill structure
   - Replace fal.ai calls with ComfyUI API calls
   - Keep the mirror/direct selfie mode logic
   - Add NSFW tier logic (SFW by default, explicit behind paywall)
   - Integrate with OpenClaw as a custom skill

3. **Test end-to-end flow**
   - Send "send me a pic" on Telegram
   - AI detects intent, calls skill
   - Skill calls ComfyUI API on RunPod
   - Image generated with LoRA consistency
   - Image sent back to user
   - Validate face consistency, image quality, response time

### Phase 2C: Monetization Integration (Week 3-4)

**Goal:** Connect to Fanvue for paid content delivery.

1. **Research Fanvue API**
   - Check if Fanvue has a creator API for automated posting/DMs
   - If no API: use browser automation (Playwright) or manual posting
   - If API exists: integrate direct content upload

2. **Implement content tiers**
   - Free tier: SFW selfies, clothed, lifestyle photos
   - Paid tier: Lingerie, suggestive poses
   - Premium tier: Explicit content (Fanvue-only)
   - Logic: AI detects upsell opportunity --> "Want to see more? Subscribe on Fanvue [link]"

3. **Payment flow**
   - WhatsApp/Telegram: Free engagement channel, drives to Fanvue
   - Fanvue: Paid content + DM conversations
   - ManyChat: Instagram automation funnel (already planned)

### Phase 2D: Scale and Optimize (Week 4+)

1. **Response time optimization** -- Pre-generate image library, cache common requests
2. **Conversation memory** -- OpenClaw has built-in session memory; tune for relationship-building
3. **Multi-platform expansion** -- Discord, Instagram DMs
4. **Analytics** -- Track message volume, conversion rates, revenue per fan
5. **Content calendar automation** -- Schedule daily posts, stories, teasers
6. **A/B test personalities** -- Tune Amira's SOUL.md for maximum engagement

### Estimated Costs for Full Stack

| Service | Monthly Cost |
|---------|-------------|
| VPS (OpenClaw + Gateway) | $12-24 |
| Anthropic Claude API | $20-50 (usage-based) |
| RunPod (ComfyUI inference) | $20-60 (serverless, pay per image) |
| WhatsApp Business API (optional) | $10-30 (per-message pricing) |
| Fanvue | Free (they take % of revenue) |
| Domain + misc | $5-10 |
| **Total** | **~$70-175/month** |

### Key Dependencies and Prerequisites
- [ ] LoRA training complete and validated (face consistency confirmed)
- [ ] ComfyUI workflow tested for batch generation
- [ ] Inpainting pipeline working for body consistency
- [ ] Amira Noor character bible written (personality, backstory, speaking style)
- [ ] At least 50+ production images generated for initial content library
- [ ] Fanvue account created and profile set up
- [ ] VPS or hosting solution selected

---

## Reference Links

- Clawra Repo: https://github.com/SumeLabs/clawra
- OpenClaw Repo: https://github.com/openclaw/openclaw
- OpenClaw Docs: https://docs.openclaw.ai/
- OpenClaw WhatsApp Docs: https://docs.openclaw.ai/channels/whatsapp
- fal.ai (Image API): https://fal.ai/
- fal.ai Grok Imagine: https://fal.ai/models/xai/grok-imagine-image
- fal.ai Pricing: https://fal.ai/pricing
- Baileys (WhatsApp Library): https://github.com/WhiskeySockets/Baileys
- OpenClaw Deploy Guide (Zeabur): https://zeabur.com/templates/VTZ4FX

---

## TL;DR for Pistachio

Clawra is a lightweight selfie-sending plugin for OpenClaw (an open-source AI assistant platform). It proves the concept works: AI persona + image generation + multi-platform messaging = AI girlfriend experience. However, for Pistachio/Amira Noor, we need to replace the image backend (Grok Imagine) with our own LoRA pipeline (ComfyUI on RunPod) for better face consistency and NSFW capability. The OpenClaw Gateway + messaging architecture is directly reusable. Total stack cost for production would be approximately $70-175/month, which is easily covered by Fanvue revenue from even a small number of subscribers.
