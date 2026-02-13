# Session Learnings

## CRITICAL RULES (Read First)
1. Read goals, patterns, session learnings, and progress before first action.
2. For 3+ step work, use structured task loop before coding.
3. Keep main context lean; avoid bulk long-file reads in one pass.
4. Keep CLAUDE.md compact; move heavy guidance into skills.
5. Treat warnings as possible root causes until disproved.
6. Prefer permanent fixes over temporary patches.
7. Use pinned dependency sets for training/tooling environments.
8. Avoid copy-paste multiline terminal commands; provide scripts.
9. Save screenshots and external artifacts immediately.
10. Save decisions and plan changes to persistent project files.
11. Log new user preferences the moment they appear.
12. Log mistakes with trigger plus prevention rule immediately.
13. Verify ad/data recommendations against current metrics before advising.
14. Use exact business routing: Pistachio vs RedLine Gen vs BMV.
15. Ask when routing is ambiguous; do not guess.
16. Keep scripts practical, uploadable, and self-contained.
17. Include immediate fix plus long-term prevention in incident responses.
18. Always define expected outcome for every proposed action.
19. Prioritize one highest-value task until complete.
20. Keep production instructions step-by-step and executable.
21. For LoRA quality, use detailed per-image captions with trigger token.
22. For LoRA identity, include regularization images in training.
23. Validate training flag compatibility before launch.
24. Keep startup automation as single source of truth.
25. Keep backup and recovery artifacts versioned and reproducible.
26. Do not fabricate image/text readings when visibility is unclear.
27. Use measured numbers in performance recommendations.
28. Archive historical learnings; keep active rules concise.
29. Update this critical section when a pattern proves durable.
30. Never repeat a documented mistake.
31. At 5% context remaining, STOP all work and save full state to PROGRESS.md before auto-compact.
32. Pod migrations lose pip packages and authorized_keys — startup script must reinstall everything.
33. Always run Python scripts with `-u` flag on pod for unbuffered output in logs.
34. FaceID similarity ceiling is ~0.52 max. InstantID + LoRA reaches 0.73.
35. User wants reusable ComfyUI workflow files (.json) they can load in the UI — always export winning configs.
36. Generated images must vary in pose/angle — don't use same composition across all prompts.
37. Auto-run quality checks (InsightFace similarity + face detection) on every generation batch.
38. User preference: research on BlackHat, Reddit, CivitAI for real-world techniques.

## Historical Archive (On-Demand)
Detailed historical notes moved to `context/archive/session-learnings-history.md`.
Load the archive only when debugging nuanced past decisions.
