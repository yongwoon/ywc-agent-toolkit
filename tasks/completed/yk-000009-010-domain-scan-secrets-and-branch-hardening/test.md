# yk-000009-010-domain-scan-secrets-and-branch-hardening — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Flag order
**Steps:**
1. In a temp repo with a committed `AKIA…` line on a branch off `main`, run `scan-secrets.sh --committed main --staged`, then `--staged --committed main`

**Expected Result:**
- Both exit 1 with `SECRET DETECTED`

### Scenario 2: git failure in Phase 1/2
**Steps:**
1. Put a `git` shim on PATH that fails `git status` (then one that fails `git diff --cached`) and run `scan-secrets.sh --staged`

**Expected Result:**
- Exit 2, no `OK` line

### Scenario 3: Parallel base refresh
**Steps:**
1. Read `ywc-parallel-executor/SKILL.md` Step 4e (a) step 4

**Expected Result:**
- `BASE` / `BRANCH` validated per C2 and quoted; `git -C "<worktree-path>"`; no `../worktree-<task-name>`
