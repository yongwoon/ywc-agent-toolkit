# yk-000012-010-domain-codex-merge-dependabot-parity — Manual Test Plan

## Preconditions

- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: No required checks on base

**Steps:**

1. Follow Codex 3b for a base without required checks

**Expected Result:**

- the PR never gets `--auto`; it is handled in Stage 3

### Scenario 2: Head moves before merge

**Steps:**

1. Push to the Dependabot branch between the CI check and the merge

**Expected Result:**

- the pinned merge is refused; no unverified head lands

### Scenario 3: Resume after crash

**Steps:**

1. Resume a run whose PR merged during the crash window

**Expected Result:**

- recorded as Merged, not restarted or Failed
