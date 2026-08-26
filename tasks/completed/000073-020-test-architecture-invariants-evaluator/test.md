# 000073-020-test-architecture-invariants-evaluator — Manual Test Plan

## Preconditions
- [ ] `000073-010-domain-architecture-invariants-contract` is merged.
- [ ] Python 3 is available.

## Test Scenarios

### Scenario 1: Valid and invalid manifest contracts
**Steps:**
1. Run `python3 tests/architecture_invariants_test.py`.
2. Review valid, malformed, duplicate, dangling, invalid-glob, and unknown-field cases.

**Expected Result:**
- Valid contracts reach the expected mode result; invalid contracts return `NEEDS_CONTEXT` without process launches.

### Scenario 2: Evidence-bound audit
**Steps:**
1. Run the audit fixture cases with complete and partial coverage.
2. Review allow/forbid and aggregate precedence assertions.

**Expected Result:**
- Only normalized edge evidence can produce `MAINTAINED` or `VIOLATED`; incomplete evidence never produces `MAINTAINED`.

### Scenario 3: No arbitrary execution
**Steps:**
1. Run executable-field and process-launch instrumentation cases.
2. Inspect the recorded launch counter.

**Expected Result:**
- All executable/verifier-like fields are rejected and the child-process launch count remains zero.
