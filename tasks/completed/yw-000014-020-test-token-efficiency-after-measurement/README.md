# yw-000014-020-test-token-efficiency-after-measurement

## Purpose

Close the loop this spec opened: measure the after-state against the `yw-000012-010` baseline
(FR10/AC12), run the mechanical and behavioral verification tiers (FR11/AC10/AC11), and run the
full final-validation checklist (AC8, AC9, AC14).

## Scope

- Mechanical tier: `score.py --target claude-code/skills --format json` over the 12 modified
  skills, compared against `yw-000012-010`'s recorded baseline — must be no lower (AC10).
- `ywc-sequential-executor` default-path composite size (body + references actually read) —
  compared against the recorded ~23,000-token baseline, must be strictly lower (AC12).
- Behavioral tier: `runner.py` over the 5 fixture-backed skills named in Iteration 1 Amendment
  A1.2 (`ywc-auth-implement`, `ywc-commit`, `ywc-create-pr`, `ywc-sequential-executor`,
  `ywc-task-generator`), recorded `s3_source: "runner"`. Remaining 7 skills recorded
  `(read-only)`, not counted as behavioral evidence (AC11).
- Final validation: `bash scripts/validate.sh` (AC8), `validate-skill.sh` per each of the 12
  modified skill dirs (AC9), `git diff --name-only -- codex/ plugins/` empty (AC14).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR10, FR11, AC8, AC9, AC10, AC11, AC12, AC14
- `tasks/completed/yw-000012-010-test-token-baseline-measurement/task.md` — the recorded before-baseline (once archived)

### Summary

This is the completion-proof task. FR10 requires an after/before comparison; FR11 requires both
verification tiers with `s3_source` recorded per item so measured and read-only evidence are
never merged. AC10–AC12, AC14 are all verified here as the final gate before this spec is
considered fully implemented.

**Known gap to verify at implementation time**: this session's own investigation of
`.claude/skills/ywc-toolkit-eval/scripts/runner.py:57-58` found `FIXTURE_ROOT` resolves to
`.claude/skills/ywc-toolkit-eval/evals/fixtures/`, which currently holds only 2 generic
meta-fixtures unrelated to the 47 target skills — not a per-target-skill `evals/fixtures/`
directory. The 5 named skills currently carry only a legacy `evals/evals.json`
(prompt + expected_output pairs), not the v2 fixture-schema JSON `runner.py --case <id>`
consumes. Before claiming `s3_source: "runner"` evidence for AC11, verify whether
runner-consumable fixtures exist or need authoring from the existing `evals.json` content.

### Out of Scope (from spec)

- Any further implementation change — this task is verification-only. If a check fails, report
  it; do not silently patch upstream tasks' work to make this task pass.

## Criticality

`normal` — read-only verification and reporting.

## Dependencies

### Depends On

- `yw-000014-010` — the amended `CLAUDE.md` must be in place before quoting it in the final report

### Depended By

- (None — terminal task)

## Key Files

- (None — this task writes no source files beyond its own task.md Implementation Notes)

## Notes

If AC11's 5 named skills genuinely lack runner-consumable fixtures and authoring them is out of
this task's budget, fall back to the spec's own explicit degradation clause: record
`(read-only)` and do not count that skill as behavioral evidence, rather than fabricating a
`PASS`. This is not a stop condition — it's the spec's documented fallback path.

## Parallel Execution Metadata

### Ownership

- (None — read-only; writes only to its own task.md Implementation Notes)

### Owned Interface

- (None — no public interface owned)

### Shared Surfaces

- (None identified)

### Conflicts With

- (None identified)

### Parallelizable After

- `yw-000014-010`

### Task Verify

- `bash scripts/validate.sh`
- `for d in ywc-auth-implement ywc-commit ywc-create-pr ywc-setup-language ywc-spec-writer ywc-task-generator ywc-docker-isolate ywc-handle-pr-reviews ywc-finish-branch ywc-merge-dependabot ywc-parallel-executor ywc-sequential-executor; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/$d; done`
- `git diff --name-only -- codex/ plugins/` (must produce no output)
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --ci`

## Out of Scope

- Fixing any upstream task's shortfall — report it as a finding, since this batch's tasks are already merged by the time this task runs.
