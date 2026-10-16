# yw-000063-010-domain-event-monitoring — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Attributable completion with another outstanding worker

**Steps:**
1. Deliver a captured-target terminal notification while another target remains outstanding; inspect event processing and query accounting.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

The immediate redundant query may be skipped; outstanding timing continues and final closure still requires complete reconciliation.

### Scenario 2: Ambiguous and late events

**Steps:**
1. Exercise malformed, status-less, wrong-target, ambiguous events, API errors, and completion during escalation.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Ambiguity triggers reconciliation; missing roster entries never count as completion; a valid late terminal event takes precedence.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
