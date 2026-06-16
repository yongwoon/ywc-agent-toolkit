# 000007-010-infra-score-cli-contract - Test Plan

## Preconditions

- [ ] Repository is at the project root.
- [ ] Task implementation is complete.
- [ ] No downstream docs task has changed README examples yet.

## Test Scenarios

### Scenario 1: Mechanical mode is backward compatible

**Steps:**
1. Run `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --format json`.
2. Run `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format json`.

**Expected Result:**
- Both commands exit 0.
- Both payloads report `"mode": "mechanical"`.
- The same skill paths are present in `roots.codex/skills`.

### Scenario 2: Missing item fails clearly

**Steps:**
1. Run `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown`.

**Expected Result:**
- Command exits non-zero.
- stderr contains `no-such-skill`.
- stderr contains `codex/skills`.

### Scenario 3: Targeted item still works

**Steps:**
1. Run `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json`.

**Expected Result:**
- Command exits 0.
- JSON contains exactly one item under `roots.codex/skills`.
- The item name is `ywc-plan`.
