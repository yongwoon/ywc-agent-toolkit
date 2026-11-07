# yk-000010-020-domain-merge-dependabot-hardening — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Null head
**Steps:**
1. Stub `gh pr view` to return `null` for headRefOid and run `wait-dependabot-rebase.sh`

**Expected Result:**
- never `REBASED=1`

### Scenario 2: No required checks
**Steps:**
1. Follow SKILL.md for a base with no required checks

**Expected Result:**
- the PR is not labelled `Failed (CI not passing)`
