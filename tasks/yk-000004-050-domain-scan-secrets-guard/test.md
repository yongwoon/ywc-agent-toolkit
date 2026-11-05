# yk-000004-050-domain-scan-secrets-guard — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Run outside a work tree
**Steps:**
1. `cd $(mktemp -d)` and run `scan-secrets.sh --staged`

**Expected Result:**
- Exit code 2 with an explanatory message (not 0)

### Scenario 2: Run in a bare repo
**Steps:**
1. `git init --bare` in a temp dir, run the script there

**Expected Result:**
- Exit code 2

### Scenario 3: Hook environment
**Steps:**
1. Stage `scripts/validate.sh` and let the pre-commit hook run

**Expected Result:**
- New test passes; no inherited-git-env failure
