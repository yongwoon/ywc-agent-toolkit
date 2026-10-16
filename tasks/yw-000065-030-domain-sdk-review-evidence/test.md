# yw-000065-030-domain-sdk-review-evidence — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Verified inheritance

**Steps:**
1. Review a fixture with version-matching SDK source/error-reference evidence.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

A finding identifies the inspected version and supporting primary evidence.

### Scenario 2: Unsupported SDK assertion

**Steps:**
1. Review an inline comment unsupported by source, or evidence for the wrong SDK version.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

The result exposes uncertainty rather than claiming verified inheritance.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
