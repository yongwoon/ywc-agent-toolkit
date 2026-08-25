# 000027-030-refactor-executor-health-sweeps — Manual Test Plan

## Preconditions
- [ ] `000027-020-refactor-pr-health-handler` is merged.

## Test Scenarios

### Scenario 1: No bot comments still triggers health sweep
**Steps:**
1. Read the PR lifecycle sections in `codex/skills/ywc-parallel-executor/SKILL.md`.
2. Read the draft/range PR sections in `codex/skills/ywc-sequential-executor/SKILL.md`.

**Expected Result:**
- Both executors instruct the agent to run `ywc-handle-pr-reviews` even when bot comment count is zero.
- CI status and merge-readiness are named as required gates.

### Scenario 2: Long sequential range survives compaction
**Steps:**
1. Read the compaction guidance in `codex/skills/ywc-sequential-executor/SKILL.md`.
2. Confirm the durable records named in the instructions.

**Expected Result:**
- The executor keeps one-line task status digests in working context.
- `.ywc-run-state.json` and task artifacts are treated as durable source of truth.
