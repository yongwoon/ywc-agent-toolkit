# yk-000011-010-domain-ci-gate-and-dependabot-lows — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Lookup failure
**Steps:**
1. Stub `gh api` to return 403 and run the 3a gate block

**Expected Result:**
- `Skipped (required checks unconfirmed)`, no merge, no fallback

### Scenario 2: New coverage gap
**Steps:**
1. In a scratch fixture copy, drop a reviewer's collision cases and run validate.sh's test_score step

**Expected Result:**
- the suite fails and validate.sh reports it
