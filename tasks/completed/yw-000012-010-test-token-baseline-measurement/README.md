# yw-000012-010-test-token-baseline-measurement

## Purpose

Capture the pre-change measurement baseline this spec's later verification (AC10, AC12) depends
on, before any of FR1–FR9's edits land. `AC10` requires the post-change mechanical score to be
"no lower than the recorded pre-change baseline"; `AC12` requires `ywc-sequential-executor`'s
activation cost to be reported as a before/after number. Neither is provable without a number
captured now, prior to any script or `SKILL.md` edit.

## Scope

Read-only measurement, no source edits:

- `wc -c` on `SKILL.md` for each of the 12 skills this spec modifies.
- For `ywc-sequential-executor` specifically: identify which references its **default,
  no-flag** execution path reads (the composite the spec measures at ~23,000 tokens — body +
  eagerly-read references for branches like `--non-interactive`, `--aggregate-pr`,
  external-URL prompts that a default run never enters), and record `wc -c` for each.
- Run the mechanical tier of `ywc-toolkit-eval` over `claude-code/skills` and record the
  per-skill score for each of the 12 modified skills.
- Record all numbers in this task's own `task.md` Implementation Notes — later tasks
  (`yw-000014-020`) read them back from `tasks/completed/yw-000012-010-.../task.md` once this
  task is merged.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR10, FR11, AC10, AC12
- `docs/ywc-plans/20260901-claude-skill-token-efficiency.spec-ready-log.md` — validation history (DONE, gate 92)

### Summary

The spec's Purpose section states the eager-loading problem: a single `ywc-sequential-executor`
invocation pays "16,590 tokens of body + ~6,600 tokens of eagerly-read references ≈ 23,000
tokens before the first task begins." FR10 requires recording this (and the other 11 skills'
sizes) before any edit; FR11 requires the mechanical `score.py` baseline over all 12 modified
skills. This task performs both recordings and stops — it makes no code or doc changes.

### Out of Scope (from spec)

- The after-measurement and behavioral comparison — handled by `yw-000014-020`.
- Any script or `SKILL.md` edit — handled by `yw-000012-020`, `yw-000012-030`,
  `yw-000013-010`, `yw-000013-020`, `yw-000014-010`.

## Criticality

`normal` — read-only measurement task; touches no security-sensitive surface.

## Dependencies

### Depends On

- (None — root task, must run before any other task in this batch)

### Depended By

- `yw-000012-020` — needs this baseline captured before `resolve-language.sh` lands
- `yw-000012-030` — needs this baseline captured before `resolve-initials.sh` lands
- `yw-000014-020` — reads the recorded numbers back for the before/after comparison (AC12)

## Key Files

- (None — this task writes no source files; its only output is its own `task.md`
  Implementation Notes)

## Notes

The 12 skills are the union of the 6 language-resolution consumers (FR5) and the 8 skills FR7
touches, minus 2 overlaps (`ywc-auth-implement`, `ywc-create-pr` appear in both sets):
`ywc-auth-implement`, `ywc-commit`, `ywc-create-pr`, `ywc-setup-language`, `ywc-spec-writer`,
`ywc-task-generator`, `ywc-docker-isolate`, `ywc-handle-pr-reviews`, `ywc-finish-branch`,
`ywc-merge-dependabot`, `ywc-parallel-executor`, `ywc-sequential-executor`.

## Parallel Execution Metadata

### Ownership

- (None — read-only; the only write this task makes is to its own `task.md`
  Implementation Notes)

### Owned Interface

- (None — no public interface owned)

### Shared Surfaces

- (None identified)

### Conflicts With

- (None identified — read-only, no file writes outside its own task directory)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
- `wc -c claude-code/skills/ywc-auth-implement/SKILL.md claude-code/skills/ywc-commit/SKILL.md claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-setup-language/SKILL.md claude-code/skills/ywc-spec-writer/SKILL.md claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-docker-isolate/SKILL.md claude-code/skills/ywc-handle-pr-reviews/SKILL.md claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/ywc-merge-dependabot/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md`

## Out of Scope

- Interpreting whether the baseline is "good" or "bad" — this task only records numbers.
- Any edit to a script, `SKILL.md`, or `CLAUDE.md`.
