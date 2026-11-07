# yk-000010-060-test-reviewer-trigger-coverage — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Coverage report
**Steps:**
1. Run `score.py --ci`

**Expected Result:**
- no unexplained below-minimum item; exempt items are named with a reason

### Scenario 2: No fabricated sources
**Steps:**
1. Inspect new trigger cases

**Expected Result:**
- every new case's source is a real session trace or user prompt
