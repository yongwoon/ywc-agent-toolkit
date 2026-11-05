## Spec Review Result: 20261105-claude-upstream-issue-69-port.md (iteration 4)

### Summary
- Critical: 0, Warning: 14, Suggestion: 14
- Gate: PROCEED (90) — Scope clarity 90, Root cause 95; no Critical findings
- Phase 2 advisor calls used: 0 of 2 (none)

### Critical Issues
None.

### Warning Issues
1. [spec:134] consistency:fr5-claudemd-order — CLAUDE.md row says B1→B2→B3 vs global B1→B3→B2.
2. [spec:135] consistency:history-json-task-set — history.mechanical.json row omits C2/C3 and pre-B3 tasks.
3. [spec:116,192,212] consistency:baseline-regen-stale — AC17 / Existing Constraints / Failure Modes still say "baseline 재생성", contradicting B3.
4. [spec:5] consistency:header-aux-scope — header task list omits B2 (and C2/C3) for toolkit-eval path.
5. [spec:44-46,52,69-71] completeness:scope-without-ac — A6 extra hunks, A7 brainstorm/horizontal-slicing rows, A8 code-gen, C2 mutual exclusion lack AC or review-only label.
6. [spec:69; claude-code/agents/README*.md:35,39] completeness:agents-readme-catalog — C1 description changes vs agent catalog rows.
7. [spec:64,171-174] completeness:b4-security-surface — B4 scripts take PR numbers/branch input; not in Critical Surfaces, no validation AC.
8. [spec:72,189] completeness:c3-step9-prune-absent — local Step 9 has no prune text; C3 adds new text.
9. [score.py:447-454] compat:a14-new-refs-unlinked — new references (feedback-loop.md, retro lenses) must be named in SKILL.md body.
10. [scripts/validate.sh:739-749] compat:reference-link-resolution — `../references/` links inside ported reference files resolve skill-locally and fail.
11. [score.py:457-462] compat:s4-small-ref — feedback-loop.md needs ≥30 lines.
12. [spec:52] feasibility:a8-batch-oversize — split A8.
13. [spec:148] feasibility:nfr1-extraction-unowned — extraction has no owning sub-item/target file.
14. [spec:69-70] feasibility:c1-trigger-cases-churn — local-eval-only rewrite in completion condition.

### Suggestions
1. [spec:56,63,64] consistency:validate-sh-two-tasks — validate.sh (A8,B4) and merge-dependabot README (B3,B4) not in FR5 table.
2. [spec:63,192] consistency:trigger-cases-lines — 42 hit lines; unify citation.
3. [spec:211] consistency:a3-failure-status — "BLOCKED 또는 NEEDS_CONTEXT".
4. [spec:65,204] consistency:user-invoked-readme — B5 README lacks user-invoked blockquote.
5. [spec:243] consistency:gate-score — self-assessed band figure.
6. [spec:64,56] completeness:exec-bit — preserve mode 755 or invoke via interpreter.
7. [spec:43] completeness:create-pr-snapshot-extras — note unported extras.
8. [spec:41] completeness:finish-branch-mark-task-complete — Out of Scope note.
9. [scripts/validate.sh:752-771] compat:schedulewakeup-scan — ported files must not contain `ScheduleWakeup(`.
10. [spec NFR1] compat:nfr1-counts — awk vs score.py counting differs by 2.
11. [spec:65] feasibility:retro-tune-description — snapshot retro cites `tune description` mode absent locally.
12. [spec:70] feasibility:existing-branch-arg-shape — flag vs value; required-argument rule change.
13. [spec:35] feasibility:t0-scratchpad-lifetime — scratchpad not visible to later sessions.
14. [spec:101-112] [unverifiable-ac] AC8, AC9, AC10, AC11, AC12, AC14, AC14b, AC14c are not single-grep checks.

### Completion Status
DONE
