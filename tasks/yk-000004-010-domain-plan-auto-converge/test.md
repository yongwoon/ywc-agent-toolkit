# yk-000004-010-domain-plan-auto-converge — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Medium spec, default invocation
**Steps:**
1. Read `ywc-plan/SKILL.md` Step 5 for a Medium spec

**Expected Result:**
- Step 5 calls `/ywc-spec-ready --spec <path>` with no question

### Scenario 2: `--no-converge` / `--non-interactive`
**Steps:**
1. Search Step 5 and the Arguments table for both flags

**Expected Result:**
- Both skip the auto-run; `--non-interactive` states the caller owns the next step

### Scenario 3: Re-plan Mode
**Steps:**
1. Follow Step 4c with `--update-spec` to its last step

**Expected Result:**
- Step 7 prints `Spec amended` and stops; Step 5 is not reached

### Scenario 4: Non-DONE spec-ready result
**Steps:**
1. Read the failure handling text after the auto-run

**Expected Result:**
- Completion Report surfaced verbatim; no retry or auto-fix
