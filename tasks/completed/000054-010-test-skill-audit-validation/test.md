# 000054-010-test-skill-audit-validation — Manual Test Plan

## Preconditions

- [ ] Both Phase 000053 tasks are merged.
- [ ] Run from repository root with Bash, `rg`, and `cmp` available.

## Test Scenarios

### Scenario 1: Valid audit

**Steps:**
1. Run the Claude Code-root audit with Codex counterpart.
2. Capture stdout and exit status.

**Expected Result:**
- Exit status is 0 regardless of advisory findings.
- Six headings appear in contract order; empty sections say `none`.
- No file changes occur.

### Scenario 2: Invalid audit input

**Steps:**
1. Run audit with `--near-line-cap 0`.
2. Capture stderr and exit status.

**Expected Result:**
- Exit status is 2 with concise input error.
- No successful report is presented.

### Scenario 3: Parity and trigger routing

**Steps:**
1. Run `cmp -s` on both audit scripts.
2. Compare descriptions against explicit autonomous lifecycle, generic plan, and direct-change requests.

**Expected Result:**
- Script comparison exits 0.
- Only explicit autonomous lifecycle wording routes to `ywc-agentic`.

### Scenario 4: Close-out

**Steps:**
1. Run `bash scripts/validate.sh`.
2. Choose a pruning pilot without editing it.

**Expected Result:**
- Validation passes.
- Recommendation has audit/deletion-test evidence and performs no pruning.
