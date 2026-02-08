# Pistachio Pipeline: Complete Content Creation Workflow

> Full process from face creation to Instagram/TikTok posts.
> Updated: 2026-02-07

---

## Step 1: Create the Face (Midjourney) - ONE TIME

- Open Midjourney, prompt for the character face
- Generate batches of 4, iterate until "the one" (the hero image)
- Use Vary (Subtle/Strong) to refine
- Save the final hero image - this is the character's DNA
- **Time:** 1-3 hours | **Cost:** Midjourney $10-30/mo

## Step 2: Generate Image Variations (ComfyUI + InstantID) - ONGOING

- Load hero image into ComfyUI
- InstantID locks the face across all outputs
- img2img mode: feed hero + change prompt for scenarios
- Denoise controls variation: 0.35 (subtle) → 0.65 (significant)
- Batch generate scenarios: coffee shop, beach, gym, home, night out, etc.
- **Time:** 30-90 sec/image, 20 images in 15-30 min | **Cost:** FREE (local GPU)

### Current Settings (Phase 1 Fix)
- InstantID weight: 0.75
- CFG: 4.0
- Steps: 35
- Sampler: DPM++ 2M Karras
- Resolution: 1016x1280
- end_at: 0.90

## Step 3: Generate Videos - ONGOING

### Option A: WAN 2.2 in ComfyUI (Free, Local)
- Take generated image → WAN 2.2 Image-to-Video workflow
- Prompt the motion: "woman picks up coffee, smiles, slight head tilt"
- Generates 3-5 second clips
- Stitch clips in CapCut for full videos
- **Time:** 2-5 min/clip | **Cost:** FREE | **Needs:** 8GB+ VRAM

### Option B: Cloud AI Video Tools (Paid, Easier)
| Tool | Cost | Best For |
|------|------|----------|
| Kling AI | $6.99-33/mo | Best quality/price. 5-10 sec clips |
| Runway Gen-4 | $12-95/mo | Highest quality cinematic video |
| HeyGen | $29/mo | Talking head videos (lip sync) - critical for TikTok |
| Hedra | Free tier | Budget lip sync alternative |

## Step 4: Voice (For Talking Videos)
- ElevenLabs ($5-22/mo): AI voice generation from text
- Workflow: Script → ElevenLabs audio → HeyGen + face image → Talking video
- Alternative: HeyGen has built-in voice options

## Step 5: Edit & Post (CapCut)
- Import images + video clips into CapCut
- Assemble 15-60 second videos
- Add: text overlays, captions, transitions, music
- Export 9:16 vertical, 1080x1920
- Post to Instagram Reels + TikTok
- **Time:** 15-30 min per finished post | **Cost:** Free or $7.99/mo Pro

---

## Monthly Cost Breakdown

| Tool | Cost | Required? |
|------|------|-----------|
| Midjourney Standard | $30/mo | Yes (first month, then optional) |
| ComfyUI | FREE | Yes |
| Kling AI Standard | $6.99/mo | Yes (or WAN 2.2 free) |
| HeyGen Creator | $29/mo | Yes for TikTok talking heads |
| ElevenLabs Starter | $5/mo | Yes if using HeyGen |
| CapCut Pro | $7.99/mo | Optional |
| **TOTAL** | **~$79/mo** | |

**Budget:** Midjourney Basic ($10) + free tools = ~$10/mo
**Pro:** Full stack + Runway = ~$140/mo

## Weekly Production Schedule (Once Dialed In)

| Task | Time | Output |
|------|------|--------|
| Generate 20 images | 30 min | Week's image content |
| Generate 10 video clips | 30-60 min | Week's video raw material |
| Edit 1 post | 15-30 min | 1 finished post |
| **Weekly total** | **3-4 hours** | **7-10 posts** |

## The Pipeline Flow

```
ONCE: Midjourney → Hero Face

WEEKLY BATCH:
Hero Face → ComfyUI + InstantID → 20 scenario images
Best images → WAN 2.2 / Kling → 10 video clips
Script → ElevenLabs → Audio → HeyGen → Talking head

DAILY:
Images + Clips → CapCut → 15-60 sec video → Instagram + TikTok
```

---

## Reminders
- Playwright is installed for future browser automation (scraping, posting, etc.)
- WAN 2.2 can run in ComfyUI on 8GB+ VRAM (GGUF models for low VRAM)
- Face consistency must hit 9/10 before launching accounts
- Stockpile 30+ content pieces before going live
- Stealth phase: no Fanvue link initially, build audience first

---

*Sources: ComfyUI docs, NextDiffusion tutorials, CivitAI guides, Apatero blog*
