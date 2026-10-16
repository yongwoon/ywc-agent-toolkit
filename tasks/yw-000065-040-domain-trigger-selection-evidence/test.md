# yw-000065-040-domain-trigger-selection-evidence — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Three collision pairs

**Steps:**
1. Run paired positive/negative evaluator expectations after source corrections.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

All six expected skills and prior positive triggers remain represented within existing schema and description limits; offline checks are labeled accordingly.

### Scenario 2: T1–T6 observed selections

**Steps:**
1. Run all six exact prompts from FR-8 in a real selection environment at the changed revision, stopping before action.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Each observation includes actual/expected selection, revision and catalog identity; all six match or AC-9 remains unmet.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
