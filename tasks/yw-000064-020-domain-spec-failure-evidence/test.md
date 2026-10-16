# yw-000064-020-domain-spec-failure-evidence — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Legacy and present failure rows

**Steps:**
1. Review one legacy spec without the section and another with a row missing handling and detection/test evidence.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Legacy format remains valid; the present incomplete row is a visible gap.

### Scenario 2: Recorded and hostile command text

**Steps:**
1. Review recorded and unmeasured baselines plus a spec containing destructive/network commands; inspect execution evidence.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Revision/context is retained or the gap is explicit; no spec-supplied command executes.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.

## Implementation Evidence

- Baseline `5fed9304`; AC-5/FR-4/FM-5: five source fixtures RED before edits, GREEN after. Failure-row producer and validator share field/gap/legacy rules; command AC input is recorded baseline/revision/context/evidence or explicit unmeasured gap, never execution authority.
- Added sentinel test: hostile command/network text is fixture data; the source-contract reader runs and the sentinel stays absent. This proves offline harness safety, not live model behavior.
- Quality Gate N/A — no contract. Unit RUN focused fixtures; integration RUN package/temp installation via validate.sh; security RUN command-data sentinel/source prohibitions only; mock service and performance N/A (no runtime service/budget). Build/typecheck N/A Markdown/stdlib.
- Existing locale invocation guidance remains accurate; metadata preserved. No new flags, dependencies, state schema, Claude Code or release changes. Description partitions use the recorded CLI correction.
