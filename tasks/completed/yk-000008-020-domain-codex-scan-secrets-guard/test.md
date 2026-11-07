# yk-000008-020-domain-codex-scan-secrets-guard — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Unresolvable base (Codex)
**Steps:**
1. In a temp repo with a committed `AKIA…` line run the Codex script with `--committed no-such-branch`

**Expected Result:**
- exit 2, no `OK` line

### Scenario 2: Mutation
**Steps:**
1. Remove any one guard from the Codex script

**Expected Result:**
- the Codex test suite fails
