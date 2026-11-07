# yk-000008-040-test-trigger-cases-grounding — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Verbatim trigger
**Steps:**
1. Search impl-review-expected prompts for impl-review trigger phrases

**Expected Result:**
- zero hits

### Scenario 2: Collision grounding
**Steps:**
1. For each 7b23a3bf collision case, read the expected item's `Do not use for` clause

**Expected Result:**
- it names the impostor, and the prompt's real winner is `expected`
