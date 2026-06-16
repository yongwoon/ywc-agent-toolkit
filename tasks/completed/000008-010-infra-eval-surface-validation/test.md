# 000008-010-infra-eval-surface-validation - Test Plan

## Preconditions

- [ ] `000007-010-infra-score-cli-contract` is merged.
- [ ] `000007-020-test-trigger-coverage` is merged.
- [ ] Documentation alignment is complete.

## Test Scenarios

### Scenario 1: README examples no longer advertise failing direct full mode

**Steps:**
1. Run `rg -n '\$ywc-codex-toolkit-eval --mode full' tools/codex-internal/skills/ywc-codex-toolkit-eval/README*.md`.

**Expected Result:**
- Command returns no matches unless direct full mode was genuinely implemented and verified.

### Scenario 2: Internal-only boundary holds

**Steps:**
1. Run `test ! -e codex/skills/ywc-codex-toolkit-eval`.
2. Run `test ! -e .codex-plugin/skills/ywc-codex-toolkit-eval`.

**Expected Result:**
- Both commands exit 0.

### Scenario 3: Final validation passes

**Steps:**
1. Run `bash scripts/validate.sh`.

**Expected Result:**
- Validation exits 0.
- Output ends with `All checks passed.`
