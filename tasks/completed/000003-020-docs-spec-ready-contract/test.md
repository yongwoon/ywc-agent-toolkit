# 000003-020-docs-spec-ready-contract - Manual Test Plan

## Preconditions

- [ ] `ywc-spec-ready` package exists.
- [ ] `ywc-spec-validate` documentation includes advisor budget contract.

## Test Scenarios

### Scenario 1: readiness handoff is documented but not executed

**Steps:**
1. Inspect `codex/skills/ywc-spec-ready/SKILL.md`.
2. Search for `ywc-task-generator <spec-path>`.
3. Confirm the text says the command is printed only after `DONE`.

**Expected Result:**
- `ywc-spec-ready` clearly stops at handoff and does not claim to invoke `ywc-task-generator`.

### Scenario 2: advisor budget contract is consumer-readable

**Steps:**
1. Run `rg -n -- "--advisor-budget|Advisor budget status|advisor_budget_status" codex/skills/ywc-spec-validate/SKILL.md`.
2. Inspect the matched report-header and Programmatic Consumer Policy text.

**Expected Result:**
- The allowed budget statuses are documented.
- Machine consumers have a normalized `advisor_budget_status` key.

### Scenario 3: agentic routing remains deferred

**Steps:**
1. Run `rg -n "ywc-spec-ready" codex/skills/ywc-agentic/SKILL.md || true`.
2. Inspect every match if any exist.

**Expected Result:**
- No match appears, or every match is explicitly labeled deferred/follow-up rather than current routing.
