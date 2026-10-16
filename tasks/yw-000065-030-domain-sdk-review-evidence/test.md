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

## Implementation Evidence

- Baseline `b39a217c`, accepted predecessor. Confidence 95 PROCEED: scope96 architecture96 evidence93 reuse95 root96; existing Devex/error and verify-before-surface owners reused, exact FR-8 portion, no runtime SDK factual claim.
- AC-9/FR-8 SDK portion: three predetermined source scenarios (verified hierarchy, wrong version, unsupported comment) RED before edits, GREEN after. Version resolution and citation provenance plus actual throw/base/catch/wrapper trace required; unavailable primary evidence stays uncertainty. No new SDK install/network/execute phase. Routing/live selection acceptance remains final task.
- Interface is prose review evidence, not callable signature. Quality Gate N/A. Unit/source RUN, integration/package/temp-install RUN, security applicability N/A no new auth/SDK execution; mock/performance/build/typecheck N/A Markdown/stdlib. Existing locale usage descriptions remain accurate; internal methodology does not change invocation/output usage.
- GREEN: 3 focused tests, contract runner, both description shards, agent evals, install list and fresh full precommit `validate.sh` passed at `85aa0dba`; 61-item mechanical baseline passed. All 16 source-clause deletion probes killed. Five-axis review found no defects; no SDK runtime observation is claimed. AC-9 SDK portion and local AC-10 met; six routing observations remain with task65-040.
