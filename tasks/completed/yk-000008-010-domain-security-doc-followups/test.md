# yk-000008-010-domain-security-doc-followups — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Exit 2 wording
**Steps:**
1. Read ywc-create-pr Step 3

**Expected Result:**
- exit 2 names the invalid/unresolvable `--committed` base case

### Scenario 2: Local-merge quoting
**Steps:**
1. Read finish-branch Step 5 local-merge block

**Expected Result:**
- no unquoted `<base-branch>` / `feature/<task-name>` on a git command line
