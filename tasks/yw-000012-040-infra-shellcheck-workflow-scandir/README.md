# yw-000012-040-infra-shellcheck-workflow-scandir

## Purpose

Close the CI-coverage gap the original spec assumed but didn't have: `.github/workflows/validate.yml`'s
ShellCheck step only scans `./scripts`, so the two new scripts under `claude-code/skills/` would
otherwise never be linted in CI.

## Scope

- Extend `.github/workflows/validate.yml`'s ShellCheck step to also scan `claude-code/skills`
  (second `scandir` entry or a matrix over both roots).
- Triage pre-existing shellcheck findings in the 4 shared shell scripts now newly in scope:
  `claude-code/skills/scripts/mark-complete.sh`, `poll-pr-reviews.sh`, `scan-stubs.sh`,
  `test-poll-pr-reviews.sh` — fix each finding, or suppress with an inline
  `# shellcheck disable=<code>` carrying a reason.
- `update-state.py` (the 5th file in that directory) is Python and stays outside shellcheck's
  scope in this change.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — Iteration 1 Amendment A1.1 (FR12, AC15, amended NFR1, amended AC8)
- `.github/workflows/validate.yml` — current ShellCheck step (`scandir: ./scripts`)

### Summary

The original spec's NFR1 claimed CI shellcheck coverage that doesn't exist — `scandir: ./scripts`
only covers the repo-root `scripts/` directory. This task adds `claude-code/skills` to that
scan so `resolve-language.sh` and `resolve-initials.sh` (added by `yw-000012-020` /
`yw-000012-030`) are actually linted, and triages whatever pre-existing findings surface in the
4 shared shell scripts now newly in scope. Per the spec's own words: "Silencing the whole new
scandir to make CI green is not acceptable."

### Out of Scope (from spec)

- `update-state.py` — Python, outside shellcheck's scope entirely.
- Any behavior change to the 4 shared scripts beyond what a shellcheck fix or a justified suppression requires.

## Criticality

`normal` — CI configuration change plus lint-only triage of existing scripts; no behavior change to production logic.

## Dependencies

### Depends On

- `yw-000012-020` — `resolve-language.sh` must exist to be scanned (AC15)
- `yw-000012-030` — `resolve-initials.sh` must exist to be scanned (AC15)

### Depended By

- `yw-000014-020` — final AC8 verification assumes this CI coverage is in place

## Key Files

- `.github/workflows/validate.yml` — extend ShellCheck `scandir`
- `claude-code/skills/scripts/mark-complete.sh` — triage only
- `claude-code/skills/scripts/poll-pr-reviews.sh` — triage only
- `claude-code/skills/scripts/scan-stubs.sh` — triage only
- `claude-code/skills/scripts/test-poll-pr-reviews.sh` — triage only

## Notes

A blanket `# shellcheck disable=` at the top of a file to silence everything is not acceptable
per the spec — each suppression must be inline, scoped to one finding, and carry a reason.

## Parallel Execution Metadata

### Ownership

- `.github/workflows/validate.yml`
- `claude-code/skills/scripts/mark-complete.sh`
- `claude-code/skills/scripts/poll-pr-reviews.sh`
- `claude-code/skills/scripts/scan-stubs.sh`
- `claude-code/skills/scripts/test-poll-pr-reviews.sh`

### Owned Interface

- (None — no public interface owned; CI config + lint triage only)

### Shared Surfaces

- CI workflow: `.github/workflows/validate.yml` (any future skill's script additions inherit this scandir)

### Conflicts With

- (None identified — no other task in this batch edits `.github/workflows/validate.yml` or these 4 scripts)

### Parallelizable After

- `yw-000012-020`, `yw-000012-030`

### Task Verify

- `shellcheck claude-code/skills/scripts/resolve-language.sh claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh`
- `shellcheck claude-code/skills/scripts/*.sh`

## Out of Scope

- Adding shellcheck coverage for any script outside `scripts/` and `claude-code/skills/` (e.g. `codex/`, `plugins/` — those trees are out of scope per the spec's AC14).
