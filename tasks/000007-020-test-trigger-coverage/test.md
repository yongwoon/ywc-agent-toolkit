# 000007-020-test-trigger-coverage - Test Plan

## Preconditions

- [ ] `000007-010-infra-score-cli-contract` is merged.
- [ ] Trigger fixture updates are complete.

## Test Scenarios

### Scenario 1: Trigger reference is Codex-aligned

**Steps:**
1. Run `rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`.

**Expected Result:**
- Command returns no matches.
- The document uses `S1 / A1` for skill/agent activation mapping.

### Scenario 2: Evaluator target coverage meets minimum

**Steps:**
1. Run `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`.

**Expected Result:**
- Coverage test passes for `ywc-codex-toolkit-eval`.
- Failure messages, if any, name missing positive and impostor/collision counts.

### Scenario 3: Fixture remains valid JSON

**Steps:**
1. Run `python3 -m json.tool tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json >/dev/null`.

**Expected Result:**
- Command exits 0.
