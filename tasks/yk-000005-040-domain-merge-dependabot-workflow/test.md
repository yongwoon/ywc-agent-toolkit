# yk-000005-040-domain-merge-dependabot-workflow — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Hostile base branch name
**Steps:**
1. Feed `--x`, `a/../b`, and `a b` as `baseRefName` to the documented validation step

**Expected Result:**
- All rejected as 'cannot confirm'; PR excluded from `--auto`

### Scenario 2: Base branch without required checks
**Steps:**
1. Follow the SKILL.md flow for such a branch

**Expected Result:**
- `--auto` is not used

### Scenario 3: Polling deadline
**Steps:**
1. Run the stubbed polling test

**Expected Result:**
- Chunk ends at `chunk_deadline`; 'stalled' only after the overall deadline
