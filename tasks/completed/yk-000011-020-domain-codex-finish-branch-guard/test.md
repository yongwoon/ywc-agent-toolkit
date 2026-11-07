# yk-000011-020-domain-codex-finish-branch-guard — Manual Test Plan

## Preconditions

- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Push URL differs

**Steps:**

1. Walk the Codex guard with `remote.origin.pushurl` pointing elsewhere

**Expected Result:**

- `NEEDS_CONTEXT`, zero deletions

### Scenario 2: Fork of a fork

**Steps:**

1. Walk the guard where origin's parent is itself a fork

**Expected Result:**

- `NEEDS_CONTEXT`

### Scenario 3: Order regression

**Steps:**

1. Move the open-PR step above the merged check in a scratch copy and run the contract test

**Expected Result:**

- the new order test fails
