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
