# yk-000008-050-docs-low-followups — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: PR worktree at pre-flight
**Steps:**
1. Leave a `.worktrees/pr-12` from handle-pr-reviews and read parallel Pre-flight item 5

**Expected Result:**
- the run stops and points to ywc-handle-pr-reviews; nothing is deleted

### Scenario 2: Counts
**Steps:**
1. Compare root CLAUDE.md counts with `ls -d` of each skill/agent root

**Expected Result:**
- all four match
