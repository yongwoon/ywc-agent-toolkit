# yw-000065-010-domain-bounded-suggestion-policy — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: One bounded Suggestion pass

**Steps:**
1. Exercise default, explicit apply/defer, residual Suggestions and a revalidation that introduces a Warning.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Default attempts one pass; defer skips amendment; residual advisory findings cause no policy loop; blocking findings cannot hand off as ready.

### Scenario 2: Approval reuse and stale identity

**Steps:**
1. Consume a matching approved preview; repeat with unapproved, changed digest/revision and escaping paths, then preview-only.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Only the matching approved preview consumes without duplicate confirmation; unsafe/stale inputs gain no authority and preview-only writes no tasks.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.
