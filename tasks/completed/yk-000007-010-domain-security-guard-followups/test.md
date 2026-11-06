# yk-000007-010-domain-security-guard-followups — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Unresolvable base
**Steps:**
1. In a temp repo with a committed `AKIA…` line, run `scan-secrets.sh --committed no-such-branch`

**Expected Result:**
- stderr names the base; exit 2; no `OK` line

### Scenario 2: Option-like base
**Steps:**
1. Run `scan-secrets.sh --committed --output=x`

**Expected Result:**
- exit 2 before any `git diff` runs

### Scenario 3: Committed secret vs valid base
**Steps:**
1. Commit an `AKIA…` line on a branch off `main`, run `scan-secrets.sh --committed main`

**Expected Result:**
- `SECRET DETECTED`; exit 1

### Scenario 4: Security tests are gated
**Steps:**
1. Temporarily break `test_retro_safety.py` (e.g. `assert False`) and run `bash scripts/validate.sh`

**Expected Result:**
- `ERROR: ... test suite failed` and non-zero exit; revert afterwards

### Scenario 5: Branch names with shell metacharacters
**Steps:**
1. Read the finish-branch remote deletion guard and pr-conflict-resolution for `a$(id)` and `-x`

**Expected Result:**
- Both are rejected by the allowlist before any git command; `check-ref-format` runs only afterwards
