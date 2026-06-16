# 000007-020-test-trigger-coverage - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000007-010-infra-score-cli-contract` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within the trigger reference, tracked trigger fixture, and focused evaluator tests listed in `README.md`.
- [ ] Do not edit README locale files or `SKILL.md`; leave user-facing surface alignment for the downstream docs task.

## Stop Conditions

- [ ] Stop if trigger fixture updates require creating new ignored files under `evals/` rather than editing tracked `trigger-cases.json`.
- [ ] Stop if broad catalog fixture expansion becomes necessary to pass tests; report that the task has exceeded its spec.
- [ ] Stop if adding a runtime helper to `score.py` would change mechanical scoring output.

## Implementation Steps

- [ ] Correct trigger reference terminology.
  - [ ] Change title and mapping section in `trigger-eval-method.md` from `S1 / A2` to `S1 / A1`.
  - [ ] Replace `agent-rubric.md (A2)` references with `agent-rubric.md (A1)`.
  - [ ] Replace Claude auto-trigger wording with Codex metadata activation wording while keeping description-only judging.
- [ ] Strengthen `trigger-cases.json` for `ywc-codex-toolkit-eval`.
  - [ ] Add realistic collision cases where `ywc-codex-toolkit-eval` is the impostor and another skill should win.
  - [ ] Keep the existing three positive evaluator cases valid.
  - [ ] Validate JSON formatting with `python3 -m json.tool`.
- [ ] Add deterministic coverage tests.
  - [ ] Add coverage counting for positive and impostor/collision counts.
  - [ ] Assert `ywc-codex-toolkit-eval` has at least 3 positives and 2 impostor/collision cases.
  - [ ] Report broad catalog under-coverage in a deterministic data structure without failing every under-covered sibling.
- [ ] Run focused verification.
  - [ ] Run `test_score.py`.
  - [ ] Run the no-stale-trigger-wording `rg` assertion.
  - [ ] Confirm no new untracked ignored eval files are required.

## Task Verify

- [ ] `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] `! rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`
- [ ] `python3 -m json.tool tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json >/dev/null`

## Verification

- [ ] Focused unit tests pass.
- [ ] Trigger fixture JSON is valid.
- [ ] The implementation does not make full catalog fixture expansion a hidden blocker.
