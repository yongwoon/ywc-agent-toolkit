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

## Implementation Evidence

- Baseline: `6cf73667`; Python stdlib and Markdown contracts. AC-2/FR-2/FM-2: six source/fixture scenarios under `tests/fixtures/codex-issue69/spec-review-availability/` failed before source edits, passed after. Assertions cover direct fallback once, degraded provenance, possibly-live/API failure, missing identity, escalation completion and no-delegation inline.
- Interface: captured dispatch target + bounded status/summary/findings; canonical monitor supplies quiescence evidence; parent owns fallback and aggregation. No callable signature or state schema added.
- Quality Gate: N/A — no quality gate contract. Unit RUN focused source/fixture runner; integration RUN temporary package/install checks in validate.sh; mock service N/A (no runtime API code), performance N/A (no budget/claim), security N/A (no runtime input boundary introduced).
- Typecheck/build N/A (Markdown/stdlb repository). Bash syntax and whitespace checks apply. Evidence is source assertion / fixture expectation, not live model behavior. A real spec-review availability observation was not measured; optional live-evidence gap retained.
- Key Files reason: owned locale additions describe changed availability behavior, generated copies preserve packaging. Test evidence is maintained here as required by Task Verify.
