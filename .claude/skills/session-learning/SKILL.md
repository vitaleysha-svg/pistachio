---
name: session-learning
description: Compounding learning system. Tracks mistakes, corrections, preferences, and what works. Read at session start, update during/after every session. Never repeat a documented mistake. Always apply documented preferences.
autoLoad: true
---

# Session Learning System

## Purpose

This skill makes Claude smarter every session. It reads accumulated learnings, applies them automatically, and adds new ones as they emerge. Knowledge compounds daily.

## On Every Session Start (Non-Negotiable)

Read `context/session-learnings.md` BEFORE doing any work. Apply everything in it. This file IS your memory of what the user likes, hates, and how they work.

## During Every Session

Watch for these signals and log them IMMEDIATELY to `context/session-learnings.md`:

### 1. Mistakes (User corrects you)
- User says "no", "wrong", "that's not right", "I said X not Y"
- User undoes or reverts something you did
- User re-explains something you should have gotten the first time
- **Log:** What you did wrong, what the correct approach was, the rule going forward

### 2. Corrections (User adjusts your output)
- User asks you to change format, length, tone, detail level
- User says "too long", "too short", "more detail", "less fluff"
- User modifies your approach mid-task
- **Log:** What you produced, what they wanted instead, the preference rule

### 3. What Works (User approves or shows enthusiasm)
- User says "yes", "perfect", "exactly", "love it", "this is good"
- User uses your output without changes
- User asks for more of the same approach
- **Log:** What you did, why it worked, replicate this pattern

### 4. What Doesn't Work (User rejects approach)
- User skips or ignores your suggestion
- User says "I don't need that", "skip this", "not now"
- User shows frustration with an approach
- **Log:** What you did, why it didn't land, avoid this pattern

### 5. Preferences (Implicit or explicit)
- How they want things formatted
- How much detail they want
- What tone resonates
- What tools/approaches they prefer
- How they make decisions
- **Log:** The preference, the context, apply always

## Rules

1. NEVER repeat a documented mistake
2. ALWAYS apply documented preferences without being reminded
3. Add learnings the MOMENT they happen, not at end of session
4. Be specific - "user doesn't like long responses" is useless. "User wants scripts capped at 20 seconds, sweet spot 15-20, never over 25" is useful.
5. Date every entry so patterns over time are visible
6. This file only grows. Never delete entries. The whole point is compounding.
