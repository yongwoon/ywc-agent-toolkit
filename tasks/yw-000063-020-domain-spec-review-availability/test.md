# yw-000063-020-domain-spec-review-availability — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Quiescent unavailable dimension

**Steps:**
1. Supply complete quiescence evidence for an unavailable reviewer and inspect parent aggregation.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Exactly one parent review covers that dimension; provenance is degraded and no worker result is invented.

### Scenario 2: Possibly-live or unidentified lane

**Steps:**
1. Supply a possibly-live lane, failed dispatch, missing identity, or monitoring API error; attempt aggregation.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Ordinary aggregation and downstream handoff are blocked when liveness remains unresolved; failed dispatch and unidentified targets cannot masquerade as quiescent absence.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
