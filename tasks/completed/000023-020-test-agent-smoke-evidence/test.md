# 000023-020-test-agent-smoke-evidence — Manual Test Plan

## Preconditions
- [ ] `000023-010-infra-agent-smoke-harness` is merged.
- [ ] The current worktree has access to the seven Codex custom agents in `codex/agents/*.toml`.
- [ ] `agent_smoke.py` runs locally with Python standard library only.

## Test Scenarios

### Scenario 1: Happy-path fixture output validates
**Steps:**
1. Select one happy-path fixture for a language reviewer.
2. Confirm its captured output file contains fixture metadata and `Status: DONE` or `Status: DONE_WITH_CONCERNS` as declared.
3. Run the full `agent_smoke.py` command from `task.md`.

**Expected Result:**
- The command exits 0.
- The selected case appears in the per-agent/case summary as passing.

### Scenario 2: Missing evidence remains explicit
**Steps:**
1. Select the fixture whose `expected_status` is `NEEDS_CONTEXT`.
2. Confirm its captured output explains the missing bounded evidence without asking to run tools or inspect live files.
3. Run the full `agent_smoke.py` command.

**Expected Result:**
- The command exits 0.
- The output contains the exact `Status: NEEDS_CONTEXT` line and expected signal text.

### Scenario 3: Read-only discipline is enforced
**Steps:**
1. Select the read-only discipline fixture.
2. Inspect its `forbidden_signals` values.
3. Search the captured output for those forbidden signals.
4. Run the full `agent_smoke.py` command.

**Expected Result:**
- No forbidden signal appears in the captured output.
- The command exits 0 and reports the case as passing.
