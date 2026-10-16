# yw-000065-020-domain-impact-security-evidence — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Localized Impact

**Steps:**
1. Prepare behavior-change and docs-only PR bodies using an existing diff and repository template.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Behavior changes get concise localized scope/Before/After; docs-only bodies omit Impact; no duplicate broad diff fetch occurs.

### Scenario 2: Overlapping security scenarios

**Steps:**
1. Generate cases for authenticated upload with overlapping input/path/authorization triggers.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Each triggered lens has a negative-path test; duplicate scenarios and unconditional PR-body fetching are absent.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
