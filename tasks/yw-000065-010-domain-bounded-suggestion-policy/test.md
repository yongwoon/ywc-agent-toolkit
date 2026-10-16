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

## Implementation Evidence

- Baseline `c0e773d6`. Pre-implementation confidence scorer 94 PROCEED: exact approved scope 95, existing owner/preview architecture 95, primary source/test evidence 90, reuse 95, duplicated-prompt root cause 96. No surviving Question-First ambiguity.
- AC-6/7, FR-5/6, FM-6/7: three grouped source fixtures RED before source edits, GREEN after, with scenarios for no/default/apply/defer/residual/new blocking/malformed evidence and approved/unapproved/stale/escaping/preview-only behavior. These are source expectations, not live model trials. Existing preview negative evals retained.
- Interface: spec-ready owns single Suggestion allowance; planner/agentic consume policy without changing closed Result/artifact authority. Task-generator retains approval/identity/containment/consume-only and preview-only write boundaries.
- Quality Gate N/A. Unit RUN source predicates; integration RUN source/package/temp installs via validate.sh; security RUN approval/identity source negatives only; mock/performance N/A no runtime service/budget. Build/typecheck N/A Markdown/stdlib. Full five-axis critical review required.
- Locale updates limited to spec-ready's changed default. Other owned READMEs contain no contradictory Suggestion policy and retain valid invocation usage. No release, Claude Code, dependency or checkpoint-schema changes.
