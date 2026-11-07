# yk-000005-020-domain-user-invoked-skills — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Validator exception
**Steps:**
1. Run `validate-skill.sh` on `ywc-merge-dependabot`

**Expected Result:**
- No A2/A3/A4 failure

### Scenario 2: Non-user-invoked skill is still checked
**Steps:**
1. Temporarily remove 'Do not use for' from another skill's description and run `score.py`

**Expected Result:**
- The A3 axis drops (exception is not global); revert afterwards

### Scenario 3: Fixture cleanliness
**Steps:**
1. Grep `trigger-cases.json` for both skill names

**Expected Result:**
- Only 'user-invoked, not routed' mentions remain; schema test passes
