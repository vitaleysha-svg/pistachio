# Session Learnings - Pistachio Project

## Technical Insights

### RunPod
- **Use official templates** - Don't use pytorch template for ComfyUI. Use the "ComfyUI" template directly to avoid port exposure issues.
- **Persistent storage** - Everything in `/workspace` survives pod stops. Custom nodes, models, images - all safe.
- **Cost structure**:
  - Running: ~$0.60/hr (RTX 4090)
  - Stopped (idle disk): $0.014/hr ($0.33/day)
  - Only pay for GPU when running
- **First boot takes 5-15 min** - Template downloads models and sets up environment

### ComfyUI
- **ComfyUI Manager** - Built into the template, use it to install custom nodes (no terminal needed)
- **Nodes vs Models** - Custom nodes are CODE (how to process). Models are WEIGHTS (the AI brain). Need both.
- **Key nodes for face consistency**:
  - ComfyUI-InstantID (ID 43) - face locking
  - ComfyUI_IPAdapter_plus (ID 3, by Matteo) - style/face transfer

### Face Consistency Pipeline
- **InstantID** = instant face copying from 1 reference (82-92% consistency)
- **LoRA training** = learned face from 15-30 images (95-98% consistency)
- **Start with InstantID** - faster, good enough for Month 1
- **LoRA is optimization** - only if InstantID isn't consistent enough

### Workflow Understanding
1. Midjourney creates the initial "look" (done once)
2. ComfyUI + InstantID generates all future content
3. One reference face image → unlimited consistent variations
4. Time per image: ~30 seconds once workflow is built

## Process Insights

### Realistic Timelines
- "Hours to form the body correctly" - Cousin was right
- First setup session: tech installation (~1 hour)
- Workflow dialing: 2-4 hours of tweaking across sessions
- After dialed: 50 images in 30-45 minutes

### Cost Breakdown (Month 1)
| Item | Cost |
|------|------|
| Midjourney | $30/month |
| RunPod | ~$5-20/month |
| ManyChat | Free to start |
| Fanvue | Free (20% cut) |
| **Total** | **~$35-50** |

## Deferred Tasks

### Life OS Interview Session
**Priority:** After Pistachio tech setup complete
**What:** Full interview to fill in Life OS context files
**Files to fill:**
- `context/goals.md`
- `context/patterns.md`
- Identity statements in `CLAUDE.md`
**Approach:** Deep interview on who Vitaley is, what drives him, behavioral patterns, energy drains, motivations. Save everything to context files.

---
*Last updated: 2026-02-06*
