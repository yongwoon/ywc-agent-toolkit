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

## Implementation Evidence

- Baseline `67e08599`: seven source fixtures RED (5 failures/2 absent-reference errors), GREEN after atomic producer/consumer edits. Added ten negative report fixtures (non-DONE/absent/malformed/contradictory/mismatched at both boundaries), expected zero downstream calls, plus source-order assertions that each gate follows its call before the next boundary. These are fixture expectations/source checks, not a live call trace.
- Interface: existing task-generator Status plus call-attributed spec/preview identity, coverage counts and unresolved IDs; no planner/ready Result or checkpoint/handoff schema extension. Consumer returns unchanged attributable failure or BLOCKED invalid evidence, preserves artifacts, and authorizes no repair execution.
- Ruling: owned output reference did not exist, so created it from existing inline Step 11 and linked it. Owned README template mapping is required by task checklist though not listed separately in Key Files.
- Quality Gate N/A. Unit RUN source/placement fixtures; integration RUN package/temp install via validate.sh; security RUN source approval/identity negatives only; mock/performance N/A no runtime API/budget. Build/typecheck N/A Markdown/stdlib. Existing locale invocation usage remains accurate; required metadata/locales preserved.

- Final verification: focused/contract runners, full validate.sh in commit hook (description partitions, agent/temporary install checks), install list and whitespace checks passed. All five review lanes completed; Devex capacity failure retried once after quiescence. QA predicate gaps closed by producer/consumer/wiring assertions; five in-memory clause deletion probes now fail. No live call trace is claimed.
- Review decision confidence (not a retrospective pre-implementation claim): scope 95 exact Ownership; architecture 94 existing owners/protocols; evidence 90 current source/tests with live limits explicit; reuse 95 existing gates/runner; root cause 94 absent coverage handoff confirmed. Deterministic scorer applied to these review-readiness scores.
- Review Risk high for execution-authority gating; full bounded five-axis inspection; no human approval decision required. No Use Case postconditions supplied; no app test result status inferred.
