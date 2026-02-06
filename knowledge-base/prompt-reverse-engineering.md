# Prompt Reverse-Engineering System

> Turn any reference photo into precise MJ + ComfyUI prompts. Compound learning with every iteration.

---

## How It Works

1. **Input** - Screenshot/photo of a real person
2. **Decompose** - Break down every visual attribute into categories
3. **Map** - Convert attributes to prompt language (MJ syntax + ComfyUI params)
4. **Generate** - Run prompts, compare output to reference
5. **Iterate** - User feedback logged, prompts refined, patterns extracted
6. **Compound** - Learnings feed back into future decompositions

---

## Step 1: Visual Decomposition Framework

When given a reference image, decompose into ALL of these categories:

### Face Structure
- **Bone structure**: Round, oval, angular, heart-shaped, square jaw, high/low cheekbones
- **Eye shape**: Almond, round, hooded, monolid, deep-set, wide-set, close-set
- **Eye color**: Specific shade (dark brown, hazel, amber, etc.)
- **Nose**: Bridge width, tip shape (button, pointed, flat, aquiline)
- **Lips**: Full, thin, asymmetric, cupid's bow prominence
- **Jawline**: Defined, soft, V-line, square
- **Forehead**: High, low, wide, narrow
- **Distinctive features**: Dimples, beauty marks, freckles, diastema, scars

### Skin
- **Tone**: Specific shade (warm olive, golden tan, fair with warm undertones, etc.)
- **Texture**: Visible pores, smooth, matte, dewy, oily
- **Imperfections**: Blemishes, redness, sun spots, under-eye darkness
- **Makeup level**: None, minimal, full glam, specific products visible

### Hair
- **Type**: Straight, wavy, curly, coily, frizzy
- **Color**: Specific (jet black, dark brown with highlights, etc.)
- **Length**: Cropped, shoulder, mid-back, waist
- **Style**: Messy, styled, pulled back, bangs, parted where
- **Texture**: Silky, matte, shiny, dry, voluminous, flat

### Expression & Mood
- **Expression**: Neutral, smiling, bored, tired, contemplative, laughing, candid
- **Eye direction**: Camera, off-camera left/right, down, unfocused
- **Energy**: High, low, relaxed, tense, playful, serious
- **Authenticity cues**: Caught mid-action, posed, natural moment

### Body & Pose
- **Body type**: Slim, athletic, curvy, petite, tall
- **Pose**: Sitting, standing, lying down, leaning, specific position
- **Hands**: Visible, hidden, holding something, gesture
- **Posture**: Relaxed, upright, slouched, dynamic

### Clothing & Accessories
- **Style**: Casual, streetwear, loungewear, dressed up, specific pieces
- **Fit**: Oversized, fitted, cropped, layered
- **Colors**: Specific colors and patterns
- **Accessories**: Jewelry, glasses, hats, piercings
- **Fabric**: Cotton, silk, denim, knit (affects rendering)

### Environment
- **Setting**: Bedroom, cafe, outdoor, studio, bathroom, kitchen
- **Clutter level**: Clean, messy, lived-in, minimal
- **Props**: Specific objects visible (phone, drink, books, etc.)
- **Background**: Blurred, sharp, plain, detailed

### Camera & Technical
- **Framing**: Close-up, medium shot, full body, 3/4
- **Angle**: Eye level, slightly above, below, side profile, 3/4 turn
- **Lens estimate**: Wide (24-35mm), standard (50mm), portrait (85mm), telephoto (135mm+)
- **Depth of field**: Shallow (blurred bg), deep (everything sharp)
- **Distance**: Intimate (2-3ft), conversational (4-6ft), environmental (8ft+)

### Lighting
- **Direction**: Front, side (Rembrandt), back (rim), overhead, below
- **Quality**: Hard (sharp shadows), soft (diffused), mixed
- **Source**: Natural window, artificial lamp, golden hour, overcast, ring light
- **Color temperature**: Warm (tungsten, golden), cool (daylight, blue), mixed
- **Shadows**: Where they fall, how deep, fill level

### Aesthetic & Vibe
- **Overall mood**: Cozy, edgy, clean, gritty, ethereal, nostalgic
- **Color palette**: Warm tones, cool tones, muted, saturated, specific dominant colors
- **Film/digital feel**: Clean digital, film grain, vintage, modern
- **Reference style**: "Looks like X photographer" or "Y era aesthetic"

---

## Step 2: Attribute-to-Prompt Mapping

### Midjourney v7 Syntax

**Structure**: `[subject description], [imperfections], [expression], [clothing], [environment], [lighting], [camera], [style] --style raw --ar 4:5 --s [100-250]`

**Skin tone mapping:**
- Fair with warm undertones -> "fair warm-toned skin"
- Golden olive -> "golden olive complexion"
- Light brown -> "light caramel skin tone"
- Mixed Japanese/Brazilian -> "mixed Japanese-Brazilian ethnicity, warm golden-olive skin"

**Imperfection triggers (CRITICAL for realism):**
- "visible pores, slight skin texture"
- "subtle under-eye shadows"
- "natural skin imperfections"
- "asymmetrical features"
- "no retouching, raw skin texture"

**Expression mapping:**
- Bored -> "bored expression, half-lidded eyes"
- Candid -> "candid moment, caught mid-thought"
- Tired -> "slightly tired, relaxed expression"
- Natural -> "unstaged natural expression"

**Camera/lens mapping:**
- Close portrait -> "shot on Canon 5D Mark IV, 85mm f/1.4, shallow depth of field"
- Natural light -> "natural window light, soft diffused"
- Film look -> "Kodak Portra 400 film grain, warm tones"
- Candid feel -> "candid off-center framing"

**Parameters:**
- `--style raw` - ALWAYS for realism (reduces AI beautification)
- `--s 100-200` - Stylization range for realistic output
- `--ar 4:5` - Instagram portrait
- `--ar 9:16` - Story/TikTok
- `--q 2` - Higher quality

### ComfyUI Parameter Mapping

**InstantID settings:**
- `ip_adapter_weight`: 0.6-0.8 (face similarity, higher = more similar)
- `controlnet_conditioning_scale`: 0.8-1.0 (structural adherence)
- `start_step`: 0 (apply from beginning)
- `end_step`: 1.0 (apply through end)

**IP-Adapter FaceID settings:**
- `weight`: 0.7-0.85 (balance between reference and creativity)
- `weight_type`: "linear" or "ease in-out"
- `start_at`: 0.0
- `end_at`: 1.0

**Key models needed:**
- Base: SDXL or SD 1.5 realistic checkpoint
- Face: antelopev2 (InsightFace detection)
- InstantID: ip-adapter.bin + ControlNet model
- IP-Adapter: ip-adapter-faceid-plusv2_sdxl.bin

---

## Step 3: Prompt Assembly

### Template

```
[Ethnicity/age], [face structure], [skin description with imperfections],
[hair description], [expression], [clothing],
[pose] in [environment with specific details],
[lighting description], [camera/lens], [film stock/style],
[anti-beautification triggers]
--style raw --ar [ratio] --s [100-200]
```

### Example (Japanese/Brazilian persona)

```
Mixed Japanese-Brazilian woman, 21, oval face with soft jawline,
warm golden-olive skin with visible pores and slight under-eye shadows,
dark wavy hair past shoulders slightly messy and unstyled,
bored half-lidded expression looking at phone screen glow on face,
oversized vintage band t-shirt grey cotton,
sitting cross-legged on unmade bed with tangled charger cables and empty cans,
warm tungsten lamp lighting from left with cool phone screen fill,
shot on Canon 5D Mark IV 50mm f/1.4 shallow depth of field,
Kodak Portra 400 natural film grain, candid framing off-center,
no makeup no retouching visible skin texture asymmetrical features
--style raw --ar 4:5 --s 150
```

---

## Step 4: Iteration Protocol

After each generation:

1. **Compare**: Side-by-side reference vs output
2. **Score categories** (1-10): Face accuracy, skin tone, hair, expression, vibe, overall
3. **Identify gaps**: What's off? What's too perfect? What's wrong?
4. **Adjust**: Modify specific prompt segments
5. **Log**: Full entry in `knowledge-base/prompt-iterations.md`
6. **Extract pattern**: What worked becomes a reusable rule

---

## Playwright Automation Notes (Future)

### Goal
Claude autonomously runs this entire workflow via Playwright browser automation:
1. Open Midjourney (Discord or web app)
2. Paste generated prompt
3. Wait for generation
4. Screenshot the output
5. Compare to reference (visual analysis)
6. Auto-iterate if not matching
7. Download final images
8. Log everything

### Steps to Document (Manual First)
- [ ] How to navigate to MJ prompt input (Discord vs web)
- [ ] How to paste and submit a prompt
- [ ] How to wait for generation to complete
- [ ] How to upscale specific images (U1-U4)
- [ ] How to download the result
- [ ] How to open ComfyUI web interface
- [ ] How to load a workflow in ComfyUI
- [ ] How to upload reference face image
- [ ] How to queue a generation
- [ ] How to download ComfyUI output

### Automation Requirements
- Playwright installed locally or on RunPod
- Discord bot token OR MJ web app access
- ComfyUI API endpoint (RunPod pod URL)
- Screenshot comparison logic (Claude vision)

---

## MEAN Framework Integration

Every generated persona must pass the MEAN test:
- **M**emorable - Distinctive features that stand out
- **E**ngaging - Expression/vibe that draws people in
- **A**uthentically imperfect - Real skin, real mess, real life
- **N**ot generic - If she could be anyone, she's no one

Anti-patterns to catch:
- Too perfect skin = generic AI look
- Perfect symmetry = uncanny valley
- Studio lighting = feels fake
- Clean environment = no personality
- Professional pose = stock photo energy
