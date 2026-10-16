# yw-000064-010-domain-conditional-omission-lenses — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Conditional applicability

**Steps:**
1. Review a UI spec, authenticated-upload spec, and unrelated documentation spec using the same rubric.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Only triggered lenses apply; missing applicable observable requirements are reported without fabricated requirements.

### Scenario 2: Installed references and legacy compatibility

**Steps:**
1. Inspect installed lens links in the temporary install exercised by validate.sh; review a legacy spec without Failure Modes.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Both references resolve and absence of the legacy section alone is not a failure.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
