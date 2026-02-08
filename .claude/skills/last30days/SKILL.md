---
name: last30days
description: Research any topic across Reddit, X, CivitAI, GitHub, and the web from the last 30 days. Synthesizes community consensus into actionable findings. No API keys needed - uses Claude Code's built-in WebSearch.
---

# /last30days - Real-Time Community Research Skill

> Inspired by [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill). Rebuilt to use Claude Code's built-in WebSearch - zero API keys required.

## How to Invoke

```
/last30days [topic]
/last30days [topic] for [specific tool/context]
```

**Examples:**
```
/last30days InstantID ComfyUI photorealistic face consistency
/last30days AI influencer face consistency best settings 2026
/last30days LoRA training SDXL best practices
/last30days Fanvue marketing strategies
```

---

## Workflow (What Claude Does When Invoked)

### Step 1: Parse Intent

Extract from the user's query:
- **TOPIC**: The subject to research (e.g., "InstantID settings")
- **CONTEXT**: Where findings will be applied (e.g., "ComfyUI workflow")
- **TIMEFRAME**: Default last 30 days, but can be specified

### Step 2: Multi-Source Research

Run **parallel WebSearch queries** across these sources (4-6 searches minimum):

| Source | Search Template | Why |
|--------|----------------|-----|
| Reddit | `site:reddit.com [topic] [current year]` | Real practitioner discussions, upvote-validated |
| Reddit focused | `site:reddit.com r/StableDiffusion [topic]` | SD-specific community |
| CivitAI | `site:civitai.com [topic]` | Model/workflow community, tested configs |
| GitHub | `site:github.com [topic] issues OR discussions` | Bug reports, real configs, developer solutions |
| X/Twitter | `[topic] site:x.com OR site:twitter.com [current year]` | Real-time tips from AI creators |
| General | `[topic] best settings [current year]` | Blogs, tutorials, guides |

**Rules:**
- Always include current year in queries to get recent results
- Run at least 4 searches in parallel
- Use WebFetch on the 3-5 most promising URLs to get full content
- Prioritize sources with engagement metrics (upvotes, likes, stars)

### Step 3: Synthesize Findings

After research, organize into:

1. **Community Consensus** - What most people agree works
2. **Contrarian Takes** - Minority opinions worth noting
3. **Specific Settings/Values** - Exact numbers people report working
4. **Common Mistakes** - What people say NOT to do
5. **Pro Tips** - Advanced techniques from experienced users

**Weight sources by credibility:**
- High: Reddit posts with 50+ upvotes, GitHub issues with maintainer responses, CivitAI guides with 100+ downloads
- Medium: Blog posts with specific benchmarks, X posts from verified creators
- Low: Generic tutorials, posts with no engagement, outdated info

### Step 4: Present Results

Format output as:

```markdown
## /last30days: [TOPIC]
*Researched [DATE] across Reddit, CivitAI, GitHub, X*

### Community Consensus (What Most People Agree On)
- [Finding 1] (Source: [platform], [engagement])
- [Finding 2]
- ...

### Specific Settings That Work
| Setting | Recommended Value | Source |
|---------|------------------|--------|
| ... | ... | ... |

### Common Mistakes to Avoid
- [Mistake 1] - [Why it's bad]
- ...

### Pro Tips (From Experienced Users)
- [Tip 1] (Source: [user/post])
- ...

### Contrarian Takes (Worth Testing)
- [Take 1] - [Why some disagree]
- ...

### Sources Consulted
- [URL 1] - [brief description] ([engagement])
- [URL 2] - ...
```

### Step 5: Offer Follow-Up

After presenting research:
- Ask if user wants deeper dive on any finding
- Offer to generate copy-paste-ready prompts/configs based on findings
- Offer to save findings to a knowledge base file

---

## Key Rules

1. **Never use pre-existing knowledge as primary source** - WebSearch first, then add context
2. **Always cite sources** - Every finding should trace back to a URL
3. **Engagement metrics matter** - A 500-upvote Reddit post > a random blog
4. **Recency matters** - 2026 post > 2024 post (AI tools change fast)
5. **Don't summarize before researching** - Research first, synthesize second
6. **Use WebFetch for depth** - Don't just read search snippets, fetch full pages for the best results
7. **Parallel searches** - Run all WebSearch calls in parallel for speed
8. **No API keys needed** - This skill uses only Claude Code's built-in WebSearch and WebFetch tools

---

## Integration with Pistachio

When used for Pistachio project topics, automatically offer to update relevant knowledge base files:
- `knowledge-base/face-consistency.md` - Face/InstantID findings
- `knowledge-base/prompt-reverse-engineering.md` - Prompt engineering findings
- `knowledge-base/image-gen-workflow.md` - Workflow findings
- `knowledge-base/content-strategy.md` - Marketing/growth findings
- `knowledge-base/white-label-playbook.md` - Tool/settings documentation
