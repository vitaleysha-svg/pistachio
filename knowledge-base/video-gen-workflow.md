# Video Generation Workflow

> Using Wan2.1 for AI influencer video content.

## Why Wan2.1

- **SOTA Performance:** Outperforms all other open-source video models
- **Consumer GPU Compatible:** 1.3B model needs only 8.19 GB VRAM
- **Open Source:** Full control, no API costs for generation
- **Multi-Task:** Text-to-video, image-to-video, video editing

## Model Options

| Model | Resolution | VRAM | Use Case |
|-------|-----------|------|----------|
| T2V-1.3B | 480P | 8.19 GB | Consumer GPU, quick iterations |
| T2V-14B | 720P | ~40 GB | High quality, cloud GPU |
| I2V-14B | 720P | ~40 GB | Animate still images |
| VACE-14B | 720P | ~40 GB | Edit existing videos |

## Installation

**Repository:** https://github.com/Wan-Video/Wan2.1
**Local Clone:** `/Users/mateuszjez/Desktop/pistachio/tools/Wan2.1/`

```bash
# Requirements
Python 3.10+
PyTorch >= 2.4.0
CUDA compatible GPU (8GB+ VRAM for 1.3B model)

# Install
cd /Users/mateuszjez/Desktop/pistachio/tools/Wan2.1
pip install -r requirements.txt

# Download models via HuggingFace
# (See repo README for exact commands)
```

## Workflow for Pistachio

### Image-to-Video (I2V)

**Best for:** Animating our generated portraits
**Input:** Static AI-generated image from Nano Banana
**Output:** 5-second video with subtle movement

**Workflow:**
1. Generate portrait with Nano Banana (face consistent)
2. Feed to Wan2.1 I2V model
3. Generate subtle animation (hair movement, blinking, breathing)
4. Export for IG Reels/Stories

### Text-to-Video (T2V)

**Best for:** Creating content variations
**Input:** Text prompt describing scene
**Output:** Short video clip

**Use Cases:**
- "Gaming girl reacting to screen, messy bedroom"
- "Woman typing on phone, dim lighting"
- "Candid selfie recording"

## Quality Considerations

### What Works
- Subtle movements (breathing, blinking, hair)
- Consistent lighting
- Simple backgrounds
- Short clips (3-5 seconds)

### What to Avoid
- Complex motion
- Multiple subjects
- Rapid scene changes
- Long durations (quality degrades)

## Integration with Image Gen

```
Nano Banana (image) → Wan2.1 I2V (animate) → ElevenLabs (voice) → Final Edit
```

## Cost Analysis

| Approach | Cost | Speed | Quality |
|----------|------|-------|---------|
| Wan2.1 Local (RTX 4090) | Electricity only | ~4 min/5sec clip | SOTA |
| Wan2.1 Cloud GPU | ~$0.50-1/video | ~4 min | SOTA |
| Runway/Pika API | $15-50/month | Faster | Good |

**Recommendation:** Start with Runway for speed, transition to Wan2.1 for scale/cost.

## Alternatives Considered

| Tool | Pros | Cons |
|------|------|------|
| Runway | Fast, easy | Expensive at scale |
| Pika | Good quality | Limited control |
| Chinese tools (KLM) | Free | Quality variable |
| **Wan2.1** | Best quality, free | Requires GPU |

---

*This file is updated by the Pistachio CoS autonomous agent.*
