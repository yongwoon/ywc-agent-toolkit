# yk-000010-040-domain-finish-branch-guard-review — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Fork PR same head
**Steps:**
1. Walk the guard with an open fork PR whose head name equals the local branch

**Expected Result:**
- remote deletion does not run

### Scenario 2: Moved tip
**Steps:**
1. Walk the guard where the remote tip differs from the merged PR's headRefOid

**Expected Result:**
- stop and report

### Scenario 3: Origin is a fork with a single remote
**Steps:**
1. Walk the guard where `git remote` lists only `origin`, `origin` is a fork (`isFork: true`), and an open PR from this head exists only on the parent repository

**Expected Result:**
- the `--repo "$parent"` open-PR check prints a non-zero count; zero deletions; the PR number is reported

### Scenario 4: ls-remote tail match
**Steps:**
1. Walk the guard where `git ls-remote origin "refs/heads/$branch"` prints both `refs/heads/$branch` and `refs/heads/x/refs/heads/$branch` with different SHAs

**Expected Result:**
- `tip` is taken only from the exact `refs/heads/$branch` line; the other line is ignored

### Scenario 5: Push after the tip read
**Steps:**
1. Walk the guard where a new commit lands on the remote branch after step 3 reads `tip`

**Expected Result:**
- the lease-delete is rejected (non-zero exit) → `BLOCKED`; the branch and the new commit survive
