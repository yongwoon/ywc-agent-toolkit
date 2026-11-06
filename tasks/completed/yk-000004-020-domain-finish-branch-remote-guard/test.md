# yk-000004-020-domain-finish-branch-remote-guard — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Open PR on the branch
**Steps:**
1. Read the guard for a branch with an open PR

**Expected Result:**
- Deletion is refused; the skill stops and reports

### Scenario 2: `gh` failure
**Steps:**
1. Read the guard when `gh pr list` fails or returns unparsable output

**Expected Result:**
- Result is `BLOCKED` or `NEEDS_CONTEXT`, never 'safe to delete'

### Scenario 3: Hostile branch name
**Steps:**
1. Read the guard with a name like `--force` or `a b`

**Expected Result:**
- `git check-ref-format --branch` fails; no command is built
