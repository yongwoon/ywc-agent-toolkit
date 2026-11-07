# yk-000010-010-domain-scan-secrets-hunk-filter — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: `++` content line
**Steps:**
1. Stage a file whose added line is `++key=AKIA…` and run `--staged`

**Expected Result:**
- exit 1, the secret is reported

### Scenario 2: Headers still skipped
**Steps:**
1. Stage a new file whose path contains `AKIA`-like text

**Expected Result:**
- the `+++ b/<path>` header is not scanned as content
