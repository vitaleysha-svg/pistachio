# Pistachio Project - Comprehensive Self-Audit Report

**Date:** 2026-02-10
**Auditor Perspective:** Senior ML/Software Engineer (fresh eyes)
**Scope:** Full codebase review - CLAUDE.md, knowledge base, scripts, workflows, session history

---

## Executive Summary

The Pistachio project has a solid technical foundation and has achieved real results (LoRA trained, ComfyUI pipeline working, face consistency validated). But it is suffering from **knowledge system bloat** and **structural disorganization** that are actively degrading Claude's session-to-session performance. The core problem is not Claude getting dumber -- it is Claude drowning in context.

CLAUDE.md is approximately 480 lines. Session-learnings.md is 367 lines. PROGRESS.md is 240 lines. The operations manual is 1,869 lines. And Claude is expected to internalize all of this before responding to the first message. This is the equivalent of handing a new hire a 3,000-page employee handbook and expecting them to memorize it before their first task.

The system has accumulated wisdom, but it has not been distilled. The result: repeated mistakes, context overflow, and a user who has to remind Claude of things that should be automatic.

---

## 1. CLAUDE.md Effectiveness

### 1.1 Is CLAUDE.md Bloated?

**Yes. Significantly.**

CLAUDE.md is ~480 lines and contains:
- Life OS identity/personality system (~60 lines)
- Session Start Protocol (~30 lines)
- Auto-Save Protocol (~20 lines)
- Overnight Agent Task (~10 lines)
- Ralph Loop / Task Breakdown references (~30 lines)
- Workflow Decision Tree (~15 lines)
- 12 Core Principles (Elon 5-Step, Peter Thiel, Copy What's Validated, Bottleneck-Clearing, CoS Task Intake, etc.) (~100 lines)
- Quality Standards (~15 lines)
- Capabilities/Work Sessions/Pattern Recognition (~40 lines)
- Conversation Examples (~30 lines)
- File Operations (~5 lines)
- Language Monitoring (~15 lines)
- What NOT To Do (~10 lines)
- Context Recovery Protocol (~25 lines)
- Ralph Workflow Integration (~10 lines)
- Skills System documentation (~30 lines)
- Quick Reference (~10 lines)
- **Learned Mistakes: 8 entries (~155 lines)**

The Learned Mistakes section alone is a third of the file and growing. This is by design ("this section compounds"), but the execution is self-defeating. Every new session loads all 155 lines of mistake context before doing any work.

### 1.2 Conflicting Rules

Several rules conflict or create decision paralysis:

**Conflict 1: Workflow Decision Tree vs. Actual User Behavior**
The tree says: Coding 3+ steps -> Ralph Loop. Analysis -> Interview-First -> CoS Task Intake.
In practice, the user says "fix this" or "do that" and expects immediate action. The tree adds cognitive overhead that Claude has been explicitly told to skip ("Code/answer first, explanations only when asked" -- session-learnings.md). The decision tree is a legacy artifact from when the system was more theoretical.

**Conflict 2: "NEVER accept a task without running Elon's 5 steps first" vs. "User wants the code/answer first"**
These are directly contradictory. The user has explicitly said they want immediate execution, not a framework analysis of every request.

**Conflict 3: "Always know the current time" (run `date` at start of EVERY message) vs. Context efficiency**
Running `date` before every single response is wasteful tool-call overhead. It should be session-start only, not per-message.

**Conflict 4: Multiple overlapping decision frameworks**
Elon's 5 Steps, Peter Thiel's One Thing, Bottleneck-Clearing Framework, CoS Task Intake, Interview-First, Ralph Loop -- these are six different "apply before every task" frameworks. No human could run all six. Claude certainly cannot hold all six in working memory while also doing useful work.

### 1.3 Are Learned Mistakes Actually Being Followed?

**Partially. The pattern of repetition is clear:**

- **Mistake #6 (incremental fixes)** documents a pattern that happened on 2026-02-10. But session-learnings.md already documented "Offered band-aid fix instead of permanent solution" from 2026-02-09. The same pattern was documented twice because the first documentation did not prevent recurrence.

- **Mistake #8 (web terminal paste issues)** was documented on 2026-02-10. But session-learnings.md shows "Jupyter notebooks bypass terminal paste issues" was learned on 2026-02-07 -- three days earlier. The knowledge existed; it was not applied.

- **Mistake #7 (dismissing warnings)** is a generic AI reasoning failure, not something a rule can prevent. You cannot rule-patch judgment. This type of mistake requires structural changes (like a mandatory checklist), not another line in CLAUDE.md.

**Root cause:** The Learned Mistakes section has become a changelog, not a system of prevention. Writing down "don't do X" does not prevent X if the context window is too bloated to surface the rule at the right moment.

### 1.4 What Rules Are Missing?

1. **Dependency version lockfile pattern**: When a working set of Python dependencies is found, save it as a `requirements-pinned.txt` file on the pod, not just in documentation. The machine should enforce compatibility, not a markdown file.

2. **Pre-flight check for pod operations**: Before giving any command to run on the pod, verify: (a) Is it a single line? If not, create a script. (b) Are all dependencies pinned? (c) Is this a known-working command from the playbook?

3. **"Stop and research" trigger**: When an error occurs that involves a version, dependency, or compatibility issue, STOP. Do not suggest a fix until the full dependency graph is understood. This was documented as Mistake #6 but framed as a behavioral rule rather than a structural gate.

4. **Context budget rule**: CLAUDE.md should state the maximum number of files Claude should read at session start. Currently the Session Start Protocol says to read 5+ files. If each is 200+ lines, that is 1,000+ lines of context consumed before any work begins.

### 1.5 The Workflow Decision Tree

**Verdict: Remove it.**

The decision tree (Ralph vs Interview-First vs CoS) has never been the bottleneck. The user's tasks are clear. They say "train the LoRA" or "fix ComfyUI." They do not need Claude to route through a decision tree. The tree served a purpose during initial system design but is now dead weight that adds ~15 lines of always-on context.

---

## 2. Knowledge Base Quality

### 2.1 File Inventory

The knowledge-base directory contains 16 files:
- `face-consistency.md` (397 lines) -- actively maintained, accurate
- `runpod-automation-playbook.md` (509 lines) -- comprehensive, recent
- `video-animation-tools.md` (1,211 lines) -- exhaustive research document
- `white-label-playbook.md` (282 lines) -- partially stale
- `image-gen-workflow.md` (144 lines) -- stale (last updated 2026-02-03)
- `prompt-reverse-engineering.md` (266 lines) -- useful but contains stale Playwright section
- `clawra-ai-girlfriend-research.md` -- research artifact
- `content-strategy.md` -- not read, likely duplicates ops manual
- `dm-psychology.md` -- not read, likely duplicates ops manual
- `funnel-playbook.md` -- not read, likely duplicates ops manual
- `pipeline-workflow.md` -- not read, likely duplicates ops manual
- `prompt-iterations.md` -- not read
- `prompts-library.md` -- not read, likely duplicates ops manual
- `revenue-projections.md` -- not read
- `SESSION-LEARNINGS.md` -- DUPLICATE of context/session-learnings.md (different case)
- `video-gen-workflow.md` -- not read, likely overlaps video-animation-tools.md

### 2.2 Duplication Analysis

**Critical duplication detected:**

1. **Session learnings exist in THREE places:**
   - `context/session-learnings.md` (367 lines) -- the active file
   - `knowledge-base/SESSION-LEARNINGS.md` -- duplicate (different case)
   - CLAUDE.md Learned Mistakes section (~155 lines) -- partial duplicate

2. **Face consistency information in at least FOUR places:**
   - `knowledge-base/face-consistency.md` (397 lines)
   - `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` Section 6 (~150 lines)
   - `knowledge-base/white-label-playbook.md` (overlapping settings/troubleshooting)
   - `PROGRESS.md` (working combo settings documented inline)

3. **RunPod pod setup information in THREE places:**
   - `knowledge-base/runpod-automation-playbook.md` (509 lines)
   - `knowledge-base/face-consistency.md` "RunPod Pod Startup Fix Chain" section (~115 lines)
   - `knowledge-base/white-label-playbook.md` RunPod troubleshooting section

4. **MJ body terms documented in TWO places:**
   - `knowledge-base/white-label-playbook.md`
   - `knowledge-base/image-gen-workflow.md`

5. **MJ Editor workflow documented in TWO places:**
   - `knowledge-base/white-label-playbook.md`
   - `knowledge-base/image-gen-workflow.md`

6. **Video generation information potentially in THREE places:**
   - `knowledge-base/video-animation-tools.md` (1,211 lines)
   - `knowledge-base/video-gen-workflow.md`
   - `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` Section 7

7. **The Operations Manual (1,869 lines) duplicates almost everything:**
   - It contains its own version of face consistency, video generation, platform setup, content strategy, DM scripts, revenue model, prompts library, and MJ settings.
   - Much of it is now outdated (still references Wan2.1 instead of Wan2.2, original MJ prompts without --oref, pre-LoRA workflow).

### 2.3 Staleness

**Stale files:**

| File | Last Updated | Issue |
|------|-------------|-------|
| `image-gen-workflow.md` | 2026-02-03 | References Wan2.1, pre-LoRA workflow. Missing --oref documentation. |
| `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` | 2026-02-03 | Still references Wan2.1, pre-LoRA, pre-RunPod setup. 1,869 lines of increasingly outdated information. |
| `white-label-playbook.md` | 2026-02-08 | Pod ID references old pod (h0r68bqsw0lepy). Some troubleshooting superseded by runpod-automation-playbook.md. |
| `prompt-reverse-engineering.md` | Unknown | Contains Playwright automation section for MJ, which was explicitly ruled out (ban risk). |
| `context/projects/pistachio/context.md` | Pre-2026-02-06 | References "Nano Banana" tool, Wan2.1, path `/Users/mateuszjez/Desktop/pistachio/tools/Wan2.1/` (Matt's machine, not relevant). Status says "Images: Test images in Nano Banana showing promise" -- this is weeks out of date. |

### 2.4 Gaps

**What should be documented but is not:**

1. **A single `requirements-pinned.txt`** for the kohya sd-scripts environment. The working versions (transformers==4.38.2, diffusers==0.25.1, huggingface_hub==0.21.4) are documented in markdown but not as an installable file.

2. **ComfyUI workflow JSON files** -- The actual .json workflow files are referenced but not version-controlled in the repo. If the pod dies, the workflow is lost unless the user has a local copy. These should be in `tools/workflows/`.

3. **LoRA quality evaluation criteria** -- Training is done, but there is no documented process for evaluating LoRA output quality. What makes a "good" LoRA? What does overfitting look like? What does underfitting look like? How to compare checkpoint 500 vs 1000 vs 1500?

4. **Image prep pipeline** -- The captioning approach is hardcoded in train_lora.py as generic captions ("amiranoor, a young woman, photorealistic"). A senior ML engineer would note that caption quality dramatically affects LoRA output quality. There is no documentation on captioning best practices specific to this use case.

5. **Inpainting workflow** -- User explicitly asked for step-by-step inpainting walkthrough. Not yet documented anywhere.

6. **Wan2.2 setup on the pod** -- Next step per PROGRESS.md. No playbook exists yet.

### 2.5 Organization

**Verdict: Scattered and overlapping.**

There are effectively three "source of truth" layers:
1. `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` -- The "bible" (1,869 lines, increasingly stale)
2. `knowledge-base/` files -- Domain-specific reference (16 files, some redundant)
3. `context/session-learnings.md` -- The living memory

The operations manual was useful at project inception but has become a liability. It is too long to read, too stale to trust, and too redundant with the knowledge base files that supersede it. It is 1,869 lines of context that Claude should never load.

---

## 3. Performance Degradation Analysis

### 3.1 Patterns of Failure

Analyzing all documented mistakes and session learnings, five distinct failure patterns emerge:

**Pattern 1: "Fix One Thing, Break Another" (Cascading Dependency Failures)**
- Occurrences: 2026-02-10 (dependency pinning), 2026-02-10 (conflicting training flags)
- Root cause: Not understanding the full system before modifying a part of it
- This is the most expensive pattern because each iteration wastes user time AND erodes trust

**Pattern 2: "Known Issue, Unknown to Claude" (Not Applying Past Learnings)**
- Occurrences: 2026-02-10 (web terminal paste -- known since 02-07), 2026-02-09 (band-aid fix -- after prior session established permanent fix rule)
- Root cause: The knowledge exists in files but Claude's context window cannot hold everything. At 480 lines of CLAUDE.md + 367 lines of session-learnings + whatever else is loaded, the critical rule is buried.

**Pattern 3: "Reactive, Not Proactive" (User Has to Ask for Permanent Fixes)**
- Occurrences: 2026-02-09 (custom nodes re-install), 2026-02-10 (startup script evolution)
- Root cause: Claude defaults to solving the immediate symptom rather than the systemic cause. This is a fundamental LLM behavior pattern -- respond to the stated problem, not the unstated pattern.

**Pattern 4: "Optimism Bias on Warnings" (Dismissing Non-Error Signals)**
- Occurrences: 2026-02-10 (frontend version warning dismissed as cosmetic)
- Root cause: LLMs are trained to be helpful and to minimize alarm. Warnings feel like noise. This requires structural intervention (a rule that says "investigate all warnings first").

**Pattern 5: "Context Overwhelm Leading to Protocol Skip"**
- Occurrences: 2026-02-06 (skipped session start protocol), 2026-02-06 (didn't use Ralph Loop), 2026-02-06 (blew context with parallel reads)
- Root cause: Too many protocols to follow at session start. The system demands reading 5+ files and applying 12+ principles before the first response. When context is tight, something gets dropped.

### 3.2 Why Does Claude Keep Making the Same Mistakes?

Three structural reasons:

**1. Rules are documented but not enforced.**
Writing "NEVER give multi-line commands for web terminal" in a markdown file does not prevent it. The rule competes with hundreds of other rules for attention in the context window. By contrast, a structural solution (a skill or pre-flight script that reformats commands into .py files) would enforce the behavior without relying on Claude "remembering."

**2. The knowledge base is too large to load, too important to skip.**
Session-learnings.md (367 lines) contains genuinely critical operational knowledge. But loading it in full means 367 lines of context spent before any work begins. The solution is not "read more" or "read less" -- it is to restructure the information so the critical rules are unavoidable and the details are on-demand.

**3. Learned Mistakes are framed as behavioral corrections, not structural changes.**
Every mistake entry says "Rule: Do X instead of Y." But the rule is just words. What is needed is a structural change: a checklist, a script, a skill, a template. Rules tell Claude what to think. Structure constrains what Claude can do.

### 3.3 Is Context Bloat Causing Performance Issues?

**Absolutely. This is the primary cause of degradation.**

Let us estimate the context budget for a typical session start:

| Item | Lines | Always Loaded? |
|------|-------|---------------|
| CLAUDE.md | ~480 | Yes (system context) |
| Session Start Protocol reads | | |
| - context/goals.md | ~107 | Blank template -- still loaded |
| - context/patterns.md | ~216 | Blank template -- still loaded |
| - Today's daily log | ~50-100 | If exists |
| - PROGRESS.md | ~240 | Yes (recovery file) |
| - context/session-learnings.md | ~367 | Yes (per skill autoLoad) |
| Session-learning skill (autoLoad) | ~61 | Yes |
| **Total before first task** | **~1,521-1,571** | |

Claude Code's context window is finite. Loading ~1,500 lines of context before doing anything leaves limited room for the actual work. Add in tool call results, file reads for the task, and conversation history, and you are pushing against the ceiling within the first few exchanges.

**The most damaging items:**
- `context/goals.md` (107 lines of BLANK TEMPLATE) -- This is 107 lines of `[FILL IN]` placeholders consuming context every session. The Life OS interview has never been done. This file should not be loaded until it is populated.
- `context/patterns.md` (216 lines of BLANK TEMPLATE with examples) -- Same problem. 216 lines of generic framework with zero personalized data.
- CLAUDE.md Learned Mistakes section (155 lines) -- Growing every session. Will eventually be 50% of CLAUDE.md.

### 3.4 Structural Changes That Would Fix This

1. **Split CLAUDE.md into a lean core (<150 lines) + on-demand skills.** Move all frameworks (Elon 5-Step, Peter Thiel, Bottleneck-Clearing, etc.) into a skill. Move Learned Mistakes into session-learnings.md (where they belong). Move conversation examples out entirely.

2. **Create a "RunPod Operations" skill** that loads only when working on the pod. This consolidates runpod-automation-playbook.md, face-consistency.md's pod section, and white-label-playbook.md's troubleshooting.

3. **Create a "Pre-Flight Checklist" skill for pod commands** that structurally prevents the terminal paste issue by reformatting any multi-line command into a script file.

4. **Delete or archive the operations manual.** It is 1,869 lines of increasingly outdated information that competes with the knowledge base for truth.

5. **Remove blank template files from the session start protocol.** goals.md and patterns.md should only be loaded if they contain actual data.

---

## 4. Technical Workflow Issues

### 4.1 LoRA Training Pipeline

**What works:**
- `train_lora.py` is a solid, self-contained script. It handles dependency installation, image prep, sd-scripts setup, training, and deployment in one file. This is good engineering.
- `retrain_lora_v2.py` improves on v1 with duplicate detection, varied captions, and text encoder training. The progression shows learning.
- `parameter_sweep.py` is the right approach for evaluating LoRA quality -- programmatic A/B testing via ComfyUI API.

**What could be better:**

1. **Captioning is too generic.** Both train_lora.py and retrain_lora_v2.py use basic captions like "amiranoor, a young woman, photorealistic." A senior ML engineer would use a captioning model (BLIP-2, Florence-2, or CogVLM) to generate detailed, per-image captions that describe the actual content of each image. The trigger word gets prepended, and the model learns to associate "amiranoor" with the consistent features across varied descriptions. Generic captions teach the model that "amiranoor" = "a young woman" which is weak signal.

2. **No validation split.** All images are used for training. There is no holdout set for evaluating overfitting. Even a simple 80/20 split with visual inspection of holdout prompts would catch overfitting early.

3. **Duplicate detection is naive.** retrain_lora_v2.py deduplicates by file size only. Two different images that happen to be the same file size would be falsely deduplicated. Perceptual hashing (imagehash library) would be more robust.

4. **No regularization images.** Training without regularization/class images can cause the model to associate ALL features of the training images with the trigger word, not just the face. Adding 200-500 generic SDXL-generated images of women as regularization helps the model learn what is unique about "amiranoor" vs. generic.

5. **The `--cache_text_encoder_outputs` flag in train_lora.py is redundant** with `--network_train_unet_only` and was documented as a mistake (#mistake in session-learnings). The script should be cleaned up to remove it.

6. **No training metrics logging.** The training script runs but produces no loss curves, no evaluation metrics. Adding TensorBoard logging (`--logging_dir`) would give visibility into training dynamics.

### 4.2 ComfyUI Automation

**What exists:**
- `parameter_sweep.py` -- excellent start for programmatic generation via ComfyUI API
- Manual workflow loading via JSON files

**What is missing:**

1. **Workflow version control.** The ComfyUI workflow JSON files are not in the git repo. They should be saved in `tools/workflows/` with descriptive names (e.g., `instantid-faceid-v2.json`, `lora-test.json`, `inpainting.json`).

2. **Batch generation script.** The parameter_sweep.py is built for A/B testing. A separate `batch_generate.py` should exist that takes a CSV/JSON of prompts and generates images unattended. This was identified in runpod-automation-playbook.md as "Future Automation Opportunity #3" but not built.

3. **ComfyUI health check in startup.sh.** The startup script does not verify that ComfyUI is actually responding on port 8188 after restart. It should poll the `/system_stats` endpoint and report success/failure.

4. **No workflow API wrapper.** For the chatbot integration (Clawra/OpenClaw), a FastAPI wrapper around ComfyUI is needed. This was documented as "Future Automation Opportunity #4" but not built.

### 4.3 RunPod Pod Management

**What works:**
- startup.sh is comprehensive (db permissions, frontend update, custom nodes, ComfyUI restart)
- post_start.sh hook is correctly configured
- The pattern of "one master startup script" is correct

**What needs improvement:**

1. **No health monitoring.** If ComfyUI crashes mid-generation, there is no watchdog to restart it. A simple `while true; do ... done` wrapper or systemd-style supervisor would prevent silent failures.

2. **No pod state verification script.** A script that checks: Is ComfyUI running? Are all custom nodes loaded? Are all models present? Is the LoRA deployed? This would eliminate the "start a session, discover something is broken" pattern.

3. **Model downloads are not idempotent.** The download notebooks re-download everything even if models exist. They should check for existence and skip.

4. **No pod snapshot/template.** Documented as a future opportunity but not done. This would eliminate ALL setup time for new pods.

5. **The old migration pod (h0r68bqsw0lepy) is still documented as needing termination** in PROGRESS.md. If it has not been terminated, it is burning $0.24/day in idle storage. This is a small but symbolic example of documented-but-not-executed actions.

### 4.4 Dependency Management

**Current state:** Dependencies are pinned in documentation and in the training scripts. This is better than nothing but fragile.

**What would prevent dependency hell permanently:**

1. **A `requirements-pinned.txt` file on the pod** at `/workspace/requirements-pinned.txt` that is `pip install -r`'d by startup.sh. If the file exists, dependencies are always correct after every restart.

2. **A Docker-based approach.** RunPod supports custom Docker images. Baking the entire environment (Python deps, custom nodes, models) into a Docker image means zero setup time and zero dependency drift. This is the correct long-term solution.

3. **At minimum, add `pip install transformers==4.38.2 diffusers==0.25.1 huggingface_hub==0.21.4` to startup.sh.** Currently startup.sh does not pin these critical training dependencies. If a `pip install --upgrade` somewhere in the chain pulls a newer version, training breaks silently.

---

## 5. Missing Skills/Knowledge

### 5.1 Skills That Should Be Created

**Priority 1: `runpod-operations` skill**
- Consolidates all RunPod knowledge (startup, troubleshooting, pod management)
- Loads only when the user mentions RunPod, pod, ComfyUI, or training
- Includes the pre-flight checklist for commands (single-line only, or create script)
- Replaces the need to read runpod-automation-playbook.md + face-consistency.md's pod section + white-label-playbook.md's troubleshooting

**Priority 2: `lora-training` skill**
- LoRA training best practices for SDXL
- Pinned dependency versions
- Training parameter reference (what each flag does, what to change for different goals)
- Quality evaluation guide (overfitting signs, underfitting signs, how to compare checkpoints)
- Captioning best practices
- Regularization image guidance

**Priority 3: `comfyui-api` skill**
- How to programmatically interact with ComfyUI
- Workflow building via API
- Batch generation patterns
- How to build an API wrapper for chatbot integration

**Priority 4: `image-evaluation` skill**
- How to evaluate AI-generated image quality
- Face consistency scoring methodology
- Comparison framework (A/B testing with fixed seeds)
- What to look for: skin texture, face structure, body proportions, lighting consistency

### 5.2 Domain Knowledge Gaps

**Things a senior ML engineer would know that are not documented:**

1. **LoRA training dynamics:** Learning rate scheduling, warmup effects, the relationship between network_dim and output quality, when to use network_alpha = dim vs dim/2, how repeats interact with epochs. The current approach works but is not understood deeply enough to troubleshoot or optimize.

2. **SDXL architecture specifics:** Why UNet-only training works well (SDXL's dual text encoder architecture makes TE training tricky), what the CLIP-G and CLIP-L encoders do differently, why resolution bucketing matters.

3. **Regularization/class images:** Not mentioned anywhere in the knowledge base. This is a standard LoRA training technique that significantly improves output quality by preventing style collapse.

4. **DreamBooth vs LoRA trade-offs:** The project jumped straight to LoRA. No analysis of whether DreamBooth, Textual Inversion, or other fine-tuning approaches would be better for this specific use case (consistent face/body from limited training data).

5. **Inference optimization:** Running SDXL + InstantID + IP-Adapter + LoRA simultaneously is VRAM-intensive. Techniques like model offloading, attention slicing, and tiled VAE decoding are not documented. These matter for batch generation.

6. **Video model VRAM management:** Wan2.2 14B requires 24GB VRAM. If it is to run on the same pod as ComfyUI + SDXL + InstantID, VRAM management and model swapping strategies need to be documented.

### 5.3 Missing Automation Scripts

| Script | Purpose | Priority |
|--------|---------|----------|
| `pod_health_check.py` | Verify all pod components are working (ComfyUI, models, nodes, LoRA) | High |
| `batch_generate.py` | Generate images from a prompt list via ComfyUI API | High |
| `auto_caption.py` | Use BLIP-2 or Florence-2 to generate training captions | High |
| `requirements-pinned.txt` | Pinned dependency file for pod startup | High |
| `workflow_export.py` | Export current ComfyUI workflow to JSON for version control | Medium |
| `image_dedup.py` | Perceptual hash-based image deduplication | Medium |
| `lora_eval.py` | Generate a standard set of test prompts with a LoRA and organize results | Medium |
| `wan22_setup.py` | One-click Wan2.2 installation on the pod | Medium |
| `comfyui_api_wrapper.py` | FastAPI wrapper for chatbot integration | Low (until chatbot phase) |

---

## 6. Recommendations (Prioritized by Impact)

### Tier 1: Do Immediately (Highest Impact on Performance)

**R1. Gut CLAUDE.md to under 150 lines.**

Remove:
- All 12 framework descriptions (Elon 5-Step, Peter Thiel, Bottleneck-Clearing, CoS Task Intake, etc.) -> Move to a `frameworks` skill
- Learned Mistakes section (155 lines) -> Merge into session-learnings.md, which is the canonical location
- Conversation examples (30 lines) -> Delete entirely
- Quality Standards (15 lines) -> Redundant with session-learnings preferences
- Capabilities section (40 lines) -> Claude knows what it can do
- Language Monitoring (15 lines) -> Move to a skill
- Skills System documentation (30 lines) -> Claude knows the skills system
- Workflow Decision Tree (15 lines) -> Delete; it adds overhead without value

Keep:
- Identity (who Claude is to this user): ~10 lines
- Session Start Protocol (simplified): ~10 lines
- Auto-Save Protocol: ~10 lines
- Core Principles (distilled to top 3-4): ~20 lines
- Context Recovery Protocol: ~15 lines
- What NOT To Do (distilled): ~10 lines
- File locations reference: ~10 lines
- A single line pointing to session-learnings.md as the canonical learning file

**Estimated reduction: 480 lines -> ~100 lines. This alone recovers 380 lines of context for every session.**

**R2. Stop loading blank template files at session start.**

`context/goals.md` is 107 lines of `[FILL IN]`. `context/patterns.md` is 216 lines of generic framework with zero user data. Loading these costs 323 lines of context and provides zero value.

Change the Session Start Protocol to: "Read goals.md and patterns.md ONLY if they contain actual user data (not templates). Check the first 5 lines -- if they contain `[FILL IN]`, skip."

**Estimated recovery: 323 lines of context per session.**

**R3. Consolidate session learnings into ONE canonical file.**

Currently:
- CLAUDE.md Learned Mistakes (~155 lines)
- context/session-learnings.md (~367 lines)
- knowledge-base/SESSION-LEARNINGS.md (duplicate)

Consolidate to: `context/session-learnings.md` ONLY. Delete the knowledge-base duplicate. Remove the Learned Mistakes section from CLAUDE.md entirely.

Then restructure session-learnings.md into two sections:
- **CRITICAL RULES (top of file, ~30 lines):** The 5-8 most important rules distilled to one line each. Example: "NEVER paste multi-line commands in web terminal. Always create a .py or .sh file."
- **FULL HISTORY (below, append-only):** The detailed entries with dates, context, and examples.

Claude reads the CRITICAL RULES section every session (~30 lines). The FULL HISTORY is reference material, loaded only when troubleshooting.

**R4. Archive the Operations Manual.**

Rename `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` to `archive/OPERATIONS-MANUAL-v1-2026-02-03.md`. It is 1,869 lines of increasingly stale information. The knowledge base files have superseded it. Keeping it accessible but out of the way prevents accidental loading and removes the "stale truth" problem.

### Tier 2: Do This Week (High Impact on Workflow)

**R5. Create a `requirements-pinned.txt` and add it to startup.sh.**

Contents:
```
transformers==4.38.2
diffusers==0.25.1
huggingface_hub==0.21.4
accelerate
safetensors
bitsandbytes
insightface
onnxruntime-gpu
```

Add to startup.sh: `pip install -r /workspace/requirements-pinned.txt -q`

This permanently prevents dependency hell on every pod restart.

**R6. Create `pod_health_check.py`.**

A script that verifies:
- ComfyUI is responding on port 8188
- All required custom nodes are loaded (query /object_info)
- All required models exist (checkpoint, InstantID, IP-Adapter, LoRA)
- Database is writable
- Prints a clear PASS/FAIL report

Run this after every pod start/restart. Takes dependency on "is everything working" from human observation to automated verification.

**R7. Version-control ComfyUI workflow JSON files.**

Save all working workflows to `tools/workflows/` in the git repo:
- `instantid-faceid-v2.json` -- The current working face consistency workflow
- `lora-test.json` -- Basic LoRA testing workflow
- `parameter-sweep.json` -- The sweep workflow

These are critical assets that would be lost if the pod dies.

**R8. Create `batch_generate.py`.**

Extend parameter_sweep.py into a general-purpose batch generation script that reads prompts from a file and generates images unattended. This is the core of the production pipeline.

**R9. Clean up train_lora.py.**

- Remove `--cache_text_encoder_outputs` (documented conflict with UNet-only training)
- Add BLIP-2/Florence-2 auto-captioning as an option (fall back to template captions if captioning model not available)
- Add TensorBoard logging
- Add a simple quality check at the end (generate 3 test images with the trained LoRA and save them alongside the model)

### Tier 3: Do When Ready (Medium Impact, Builds Foundation)

**R10. Create the `runpod-operations` skill.**

Consolidate:
- runpod-automation-playbook.md (the good parts)
- face-consistency.md's pod section
- white-label-playbook.md's troubleshooting
- All pod-specific rules from session-learnings.md

Into a single skill at `.claude/skills/runpod-operations/SKILL.md` that loads when pod work is mentioned.

**R11. Create the `lora-training` skill.**

Contents:
- Pinned dependencies and why
- Training parameters reference with explanations
- VRAM budget table for different configurations
- Captioning best practices
- Quality evaluation checklist
- Common failure modes and fixes

**R12. De-duplicate the knowledge base.**

Map every piece of information to ONE canonical location:
- Face consistency: `knowledge-base/face-consistency.md`
- RunPod operations: `.claude/skills/runpod-operations/SKILL.md`
- MJ body terms + Editor: `knowledge-base/image-gen-workflow.md`
- Session learnings: `context/session-learnings.md`
- Business strategy: `context/business-ideas.md`

Delete or archive everything that is redundant.

**R13. Run the Life OS Interview.**

`context/goals.md` and `context/patterns.md` are blank. They have been blank since project creation. These files are LOADED EVERY SESSION but contain no data. Either fill them in (via the deferred interview task in PROGRESS.md) or stop loading them. The current state is the worst of both worlds: wasted context for zero benefit.

**R14. Build a ComfyUI watchdog.**

A simple process supervisor that:
- Monitors ComfyUI process health
- Restarts it if it crashes
- Logs crash events for debugging

This prevents silent failures during unattended batch generation.

### Tier 4: Future (Sets Up Scaling)

**R15. Create a custom RunPod Docker template.**

Bake the entire environment (ComfyUI, custom nodes, models, pinned deps, startup script) into a Docker image. Deploy new pods with zero setup time. This is the path to multi-persona scaling.

**R16. Build the Wan2.2 setup playbook.**

Before starting video generation, document the full setup process the same way runpod-automation-playbook.md documents image generation. Include VRAM management (can Wan2.2 and SDXL + InstantID coexist?), model downloads, workflow setup.

**R17. Build the chatbot API wrapper.**

When ready for the Clawra/OpenClaw integration, build a FastAPI wrapper around ComfyUI's API endpoints. This is the bridge between subscriber requests and image generation.

---

## Summary: Root Cause and Fix

**Root Cause of Performance Degradation:**

Claude's performance has degraded because the knowledge management system has grown organically without pruning. Information is duplicated across 20+ files. CLAUDE.md has become a catch-all for rules, frameworks, and mistakes. Context files that should contain user data are blank templates that still get loaded. The result is that Claude starts every session with ~1,500 lines of context consumed before doing any useful work, and much of that context is redundant, stale, or empty.

**The Fix in One Sentence:**

Cut CLAUDE.md from 480 to 100 lines, stop loading blank templates, consolidate learnings into one file with a 30-line executive summary at the top, archive the 1,869-line operations manual, and move domain knowledge into on-demand skills.

**Expected Impact:**

Recovering ~1,200+ lines of context budget per session will give Claude significantly more room for actual work, reduce the chance of missing critical rules, and eliminate the "I told you this already" pattern that frustrates the user.

---

## Appendix: File-by-File Disposition

| File | Action | Reason |
|------|--------|--------|
| `CLAUDE.md` | REWRITE (gut to ~100 lines) | Too bloated, conflicting rules, growing Learned Mistakes |
| `PROGRESS.md` | KEEP (trim stale sections) | Active state tracker, useful |
| `context/session-learnings.md` | RESTRUCTURE (critical rules at top) | Canonical learning file, needs priority hierarchy |
| `context/goals.md` | SKIP until populated | 107 lines of blank template, wastes context |
| `context/patterns.md` | SKIP until populated | 216 lines of blank template, wastes context |
| `context/projects/pistachio/context.md` | UPDATE | References stale tools, paths, and status |
| `PISTACHIO-COMPLETE-OPERATIONS-MANUAL.md` | ARCHIVE | 1,869 lines, increasingly stale, superseded by KB |
| `knowledge-base/face-consistency.md` | KEEP (remove pod section to skill) | Good reference, but pod info should be in its own skill |
| `knowledge-base/runpod-automation-playbook.md` | MOVE to skill | Best consolidated in a runpod-operations skill |
| `knowledge-base/video-animation-tools.md` | KEEP as reference | Comprehensive research, 1,211 lines but loaded on-demand |
| `knowledge-base/white-label-playbook.md` | DE-DUPLICATE | Overlaps with face-consistency and runpod playbook |
| `knowledge-base/image-gen-workflow.md` | UPDATE | Stale (2026-02-03), missing --oref, missing LoRA workflow |
| `knowledge-base/prompt-reverse-engineering.md` | UPDATE (remove Playwright section) | Contains ruled-out MJ automation approach |
| `knowledge-base/SESSION-LEARNINGS.md` | DELETE | Duplicate of context/session-learnings.md |
| `.claude/skills/ralph-workflow/SKILL.md` | KEEP | Good on-demand skill, well-structured |
| `.claude/skills/last30days/SKILL.md` | KEEP | Useful research skill |
| `.claude/skills/session-learning/SKILL.md` | KEEP (review autoLoad) | autoLoad: true means it loads every session -- may not be needed if session-learnings.md is already in the protocol |
| `train_lora.py` | CLEAN UP (remove conflicting flags) | Working but has technical debt |
| `retrain_lora_v2.py` | KEEP | Good v2 iteration |
| `fix_and_start.py` | KEEP | Useful one-click pod repair |
| `parameter_sweep.py` | KEEP (extend to batch_generate.py) | Good foundation for production pipeline |

---

*Report generated 2026-02-10. This document should itself be treated as a snapshot -- its recommendations should be executed, not just read.*
