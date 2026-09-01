# yw-000014-020-test-token-efficiency-after-measurement — Implementation Checklist

## Prerequisites

- [ ] `yw-000014-010` is completed (merged) — `CLAUDE.md` amendment in place
- [ ] `tasks/completed/yw-000012-010-test-token-baseline-measurement/task.md` exists with the before-baseline recorded in its Implementation Notes

## Allowed Edit Scope

- [ ] This task edits no source files — its only write is to this file's Implementation Notes

## Stop Conditions

- [ ] Stop if the before-baseline from `yw-000012-010` cannot be found — do not fabricate a baseline to compare against
- [ ] Stop (do not fabricate) if AC11's runner-consumable fixtures genuinely don't exist for a named skill — record it `(read-only)` per the spec's own degradation clause instead

## Implementation Steps

- [ ] Re-run the mechanical tier and diff against the recorded before-baseline
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format json`
  - Confirm no per-skill score regressed for the 12 modified skills (AC10)
  - Re-measure `ywc-sequential-executor`'s default-path composite size and confirm it is strictly lower than the ~23,000-token baseline (AC12)
- [ ] Run the behavioral tier over the 5 fixture-backed skills
  - First verify whether `.claude/skills/ywc-toolkit-eval/evals/fixtures/` has a runner-consumable case for each of `ywc-auth-implement`, `ywc-commit`, `ywc-create-pr`, `ywc-sequential-executor`, `ywc-task-generator` — if not, this is a known gap (see README.md Notes); record `(read-only)` for whichever skill lacks one rather than blocking
  - For any skill with a usable fixture, run `python3 .claude/skills/ywc-toolkit-eval/scripts/runner.py --case <id>` before/after and confirm identical observable outcome, recorded `s3_source: "runner"`
- [ ] Run final validation: `scripts/validate.sh` (AC8), `validate-skill.sh` per each of the 12 modified skill dirs (AC9), `git diff --name-only -- codex/ plugins/` (AC14, must be empty)
- [ ] Regenerate and commit the `score.py --ci` baseline if scores legitimately changed, per `.github/workflows/validate.yml`'s own instruction comment
- [ ] Write the full before/after comparison as this spec's completion summary into this file's Implementation Notes

## Task Verify

- [ ] `bash scripts/validate.sh` exits 0
- [ ] `validate-skill.sh` exits 0 for all 12 modified skill dirs
- [ ] `git diff --name-only -- codex/ plugins/` produces no output
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --ci` exits 0

## Verification

- [ ] All items above pass; completion summary recorded in Implementation Notes

## Implementation Notes (optional)
