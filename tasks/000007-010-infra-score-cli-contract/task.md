# 000007-010-infra-score-cli-contract - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] Spec is ready: `docs/ywc-plans/codex-toolkit-eval-improvements.md`
- [ ] No dependency task is required.

## Allowed Edit Scope

- [ ] Stay within `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py`
- [ ] Stay within `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] If README, `SKILL.md`, or fixture edits look necessary, stop and leave them for downstream tasks.

## Stop Conditions

- [ ] Stop if supporting `--mode mechanical` requires changing current mechanical score semantics.
- [ ] Stop if `--ci` or `--update-baseline` behavior changes unexpectedly.
- [ ] Stop if a missing item cannot be detected without breaking unfiltered empty-root output.
- [ ] Stop if changes require a non-standard-library Python dependency.

## Implementation Steps

- [ ] Update CLI mode parsing in `score.py`.
  - [ ] Add `--mode` to `parse_args()` with choices `mechanical`, `judge`, `full` and default `mechanical`.
  - [ ] Preserve existing output payload field `"mode": "mechanical"` for mechanical mode.
  - [ ] Add an explicit non-zero path for `judge` and `full` if real orchestration is not implemented.
- [ ] Add missing-item detection.
  - [ ] Detect when `args.item` is set and `evaluate()` returns zero matching assets across selected roots.
  - [ ] Print stderr that includes the missing item and target, for example `item not found: no-such-skill in codex/skills`.
  - [ ] Keep unfiltered empty-root rendering unchanged.
- [ ] Extend focused tests in `test_score.py`.
  - [ ] Add a test that `--mode mechanical` succeeds and returns mechanical output.
  - [ ] Add a test that unsupported `--mode judge` or `--mode full` exits non-zero if not implemented.
  - [ ] Add a test that `--item no-such-skill` exits non-zero and names the item.
  - [ ] Add a test that `--item ywc-example` returns exactly one skill in JSON.
- [ ] Re-run focused verification.
  - [ ] Run all task verify commands from `README.md`.
  - [ ] Confirm existing `--ci` still passes against the current repository baseline.

## Task Verify

- [ ] `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown`
- [ ] `! python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci`

## Verification

- [ ] Focused unit tests pass: `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] Mechanical regression gate passes: `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci`
- [ ] No new package manager, DB, API, or external service dependency was introduced.
