# yw-000064-030-domain-task-coverage-gate — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Unmapped requirement or justified in-scope deferral

**Steps:**
1. Generate from fixtures separately omitting an AC, FR and Failure Modes row; repeat with a documented in-scope deferral.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Each ID appears in the coverage report and status is not clean DONE; no requirement is silently made out of scope.

### Scenario 2: Both downstream boundaries

**Steps:**
1. Return non-DONE, absent, malformed, contradictory or identity-mismatched coverage after preview and after consume.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Unresolved preview causes zero consume calls; unresolved consume causes zero executor calls; attributable statuses propagate and invalid evidence blocks.

### Scenario 3: Interface and verification mapping

**Steps:**
1. Consume an incompatible declared signature, then review existing tests through a documented mapping.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Mismatch includes producer/consumer evidence; valid documented test mapping is accepted without invented legacy signatures.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
