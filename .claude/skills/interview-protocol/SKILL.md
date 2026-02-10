---
name: interview-protocol
description: Interview-first protocol for ambiguous requests before planning or implementation.
---

# Interview Protocol Skill

## When To Use
Use this before planning if the request is ambiguous, high-impact, or missing success criteria.

## Objective
Turn vague requests into executable specs with minimal back-and-forth.

## Question Sequence
1. Outcome: what must be true when this is done?
2. Scope: what is in and out for this pass?
3. Constraints: deadlines, dependencies, environment limits.
4. Quality bar: how will we verify success?
5. Failure cost: what happens if this is wrong?

## AskUserQuestion Pattern
- Keep questions short and mutually exclusive when possible.
- Ask one blocking question at a time.
- Offer a recommended default option first.
- Convert answers into explicit implementation criteria.

## Conversation Examples
- "Do you want a quick patch or a durable rebuild? Recommended: durable rebuild."
- "Should this optimize for speed or quality first? Recommended: quality first if reruns are expensive."
- "Is compatibility with current workflow mandatory? Recommended: yes unless migration is approved."

## Completion Criteria
Do not start coding until the output, scope, constraints, and verification signal are explicit.
