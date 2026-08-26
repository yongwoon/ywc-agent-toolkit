# 000027-060-test-codex-parity-evals — Manual Test Plan

## Preconditions
- [ ] Eval fixture edits are complete.

## Test Scenarios

### Scenario 1: JSON fixtures remain valid
**Steps:**
1. Run `python3 -m json.tool codex/skills/ywc-project-docs/evals/evals.json >/dev/null`.
2. Run `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null`.

**Expected Result:**
- Both commands exit `0`.
- No JSON parse error is printed.

### Scenario 2: New parity prompts are discoverable
**Steps:**
1. Run `rg -n "docs/product|cross-reference|Axum|Layered Architecture|Rust" codex/skills/ywc-project-docs/evals/evals.json codex/skills/ywc-project-scaffold/evals/evals.json`.

**Expected Result:**
- Matches show the product routing / cross-reference fixture.
- Matches show the Rust + Axum + Layered Architecture fixture.
