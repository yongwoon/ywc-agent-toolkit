# yk-000006-030-domain-handle-pr-reviews-worktree — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Non-numeric PR number
**Steps:**
1. Read Step 1.5 for PR `12;rm`

**Expected Result:**
- `BLOCKED: PR number must be numeric`

### Scenario 2: Fork PR
**Steps:**
1. Follow Step 1.5 when `isCrossRepository` is true

**Expected Result:**
- `BLOCKED`; no worktree is created

### Scenario 3: Prune advice
**Steps:**
1. Read Step 9

**Expected Result:**
- `--keep-branch` is explicit so the PR head branch survives

### Scenario 4: Worktree creation path
**Steps:**
1. Search the skill for `git worktree add`

**Expected Result:**
- Zero hits; creation goes through `ywc-worktrees` only
