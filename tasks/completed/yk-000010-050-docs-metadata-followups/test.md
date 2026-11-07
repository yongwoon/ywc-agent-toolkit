# yk-000010-050-docs-metadata-followups — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Description routing
**Steps:**
1. Run `score.py --ci`

**Expected Result:**
- no routing regression after the description is shortened

### Scenario 2: validate.sh
**Steps:**
1. Break one scan-secrets test locally and run validate.sh

**Expected Result:**
- it still reports the scan-secrets suite failure
