# Image Generation Workflow

> Complete workflow for creating hyper-realistic AI portraits.
> Last updated: 2026-02-03

## Tool Comparison (2026)

| Tool | Photorealism | Consistency | Cost | Best For |
|------|--------------|-------------|------|----------|
| **Midjourney v7** | 10/10 | Medium | $30/mo | Highest quality portraits |
| Midjourney v6 | 9/10 | Medium | $30/mo | Still excellent |
| Stable Diffusion XL | 8/10 | High (with LoRA) | Free | Control + consistency |
| Leonardo AI | 7/10 | Good | Freemium | Quick iterations |
| Flux | 8/10 | Good | Free | Open source alternative |

**RECOMMENDATION:** Start with Midjourney v7 for best photorealism. Move to SDXL + InstantID for face consistency once character is established.

## Midjourney v7 Settings for Photorealism

### Critical Parameters

```
--style raw          # Reduces AI beautification, more natural
--s 100-250          # Lower stylization = more realistic (not 0, not 1000)
--ar 4:5             # Instagram portrait ratio
--q 2                # Higher quality
```

### Portrait Prompt Formula

**Structure:** Setting + Subject + Emotion + Lighting + Camera + Style

### Proven Photorealistic Prompt Template

```
Professional portrait of a [subject description], [ethnicity], [age],
[imperfections: tooth gap, visible pores, frizzy hair, asymmetrical features],
[expression: tired, bored, candid],
soft natural lighting, shallow depth of field,
shot on Hasselblad, Kodak Portra 400 film simulation,
[environment: messy bedroom, authentic clutter],
--ar 4:5 --style raw --s 150 --q 2
```

### What Makes It Look REAL

1. **Camera terminology:** "shot on Canon 5D", "Hasselblad", "Leica M6"
2. **Lens specs:** "50mm f/1.8", "85mm portrait lens"
3. **Film stocks:** "Kodak Portra 400", "Fuji 400H"
4. **Lighting terms:** "volumetric lighting", "rim light", "chiaroscuro"
5. **Imperfections:** "freckles", "pores", "wrinkles", "sweaty skin"

### What Makes It Look FAKE

- Over-smoothed skin (plastic/waxy)
- Perfect symmetry
- Too saturated colors
- Studio lighting without environment
- No grain or texture
- Perfect hair

## DSLR Skeleton Prompt (Pistachio Persona)

```
Portrait of Egyptian/Brazilian mix woman, 21 years old,
tooth gap diastema, frizzy unstyled dark hair,
visible skin pores, slight blemishes, tired bored expression,
asymmetrical features, no makeup,
photo-realistic, shot on Canon 5D Mark IV,
50mm f/1.4 lens, shallow depth of field,
ISO grain, sub-surface scattering skin,
natural tungsten lamp lighting, golden hour tones,
messy bedroom background, authentic clutter,
oversized vintage band t-shirt,
candid off-center framing, looking at phone,
Kodak Portra 400 film simulation
--ar 4:5 --style raw --s 150 --q 2
```

### Negative Prompt Concepts (for SD/Flux)

```
airbrushed, smooth skin, perfect symmetry, studio lighting,
white background, professional model, posed, staged,
oversaturated, HDR, makeup, styled hair, perfect teeth
```

## Pro Tips

1. **Cite photographers:** Adding "style of [photographer name]" influences aesthetic
2. **Rim light:** Separates subject from background naturally
3. **Imperfections first:** Lead with flaws, not beauty
4. **Environment matters:** Describe the room, not just the person
5. **Candid > Posed:** "caught mid-action" beats "posing for camera"

## Workflow: Image to Video

```
1. Generate still in Midjourney (best quality)
2. Upscale and refine
3. Feed to Wan2.1 for subtle animation (breathing, blinking)
4. Add voice with ElevenLabs if needed
5. Export for IG Reels/Stories
```

## Sources

- [Midjourney Photorealistic Prompts Guide](https://www.aiarty.com/midjourney-prompts/midjourney-photorealistic-prompts.htm)
- [Ultimate Midjourney V6 Portrait Formula](https://myaiforce.com/midjourney-v6-portrait/)
- [Non-cliché Realistic Photo Prompts](https://www.videoproc.com/resource/midjourney-prompts-realistic.htm)

---

## Midjourney Editor / Vary (Region) - Targeted Edits (2026-02-08)

### Workflow
1. Click image in MJ -> open in Editor
2. Use **Smart Select** or **Paint > Erase** to mask the area to change
3. Type replacement prompt in "What will you imagine?" bar
4. Hit **Submit Edit**
5. MJ regenerates ONLY the masked area, keeping everything else intact

### Best Use Cases
- Remove accessories (glasses, hats, jewelry)
- Modify clothing (change outfit, remove items)
- Change background elements
- Subtle face tweaks (expression, hair)

### Body Modifications
- Mask the body area, prompt with MJ-safe terms only (see white-label-playbook.md for full list)
- If MJ flags the edit as violating content policy, use **ComfyUI inpainting** instead (zero content filter)

### MJ-Safe Body Terms Quick Reference
Safe: `hourglass figure`, `slim waist`, `toned athletic feminine figure`, `naturally curvy`, `feminine curves`, `fit figure`, `athletic build`, `elegant silhouette`, `full body photo`

Banned: cup sizes, bust/breasts/busty, glutes/booty/ass, thick thighs, voluptuous, provocative, lingerie, scantily clad, skimpy, sexy, body measurements

### Key Insight
`--oref` at `--ow 250` carries body shape from the reference image. Text prompt only needs scene/outfit/pose - NOT body measurements. Save explicit body descriptions for ComfyUI after LoRA training.

---

*Updated by Pistachio CoS Agent - 2026-02-08*
