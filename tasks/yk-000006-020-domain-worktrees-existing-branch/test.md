# yk-000006-020-domain-worktrees-existing-branch — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Hostile branch name
**Steps:**
1. Read the validation for `-x`, `a..b`, `a b`, `;rm`

**Expected Result:**
- Each yields `invalid branch name`, exit 1, before any git call

### Scenario 2: Flag exclusivity
**Steps:**
1. Pass both `--existing-branch` and `--base-branch`; then neither

**Expected Result:**
- Both cases exit 1 with a usage error

### Scenario 3: Origin-only branch
**Steps:**
1. Follow the flow for a branch present only on origin

**Expected Result:**
- A tracking branch is created and checked out
