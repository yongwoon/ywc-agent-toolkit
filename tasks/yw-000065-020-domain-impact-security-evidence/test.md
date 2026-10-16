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

## Implementation Evidence

- Baseline `b5fac41f`; predecessor merged/accepted. Confidence 95 PROCEED (scope96 architecture94 evidence92 reuse96 root95): exact FR-7 scope, existing diff/template/input modes and Stage2 lens reused; no signature invention or source ambiguity.
- AC-8/FR-7 E1: behavior/docs-only/localized-template and overlapping/untriggered/missing-reference source fixtures observed RED before production edits. These are offline source assertions, not live behavioral observations.
- Interfaces: create-pr reuses existing author-review evidence and resolved language/template; gen-testcase consumes shared spec-validator lens from installed sibling, returning NEEDS_CONTEXT when absent. No extra fetch/collection or publishing authorization.
- Quality Gate N/A. Unit source predicates RUN; integration source/package/temp-install RUN; security negative-path contracts RUN; mock/performance/build/typecheck N/A Markdown/stdlib with no runtime service. Existing localized README invocation descriptions remain accurate and contain no conflicting Impact/lens behavior. No unrelated locale churn.
- GREEN: 3 contract tests, contract runner, both description shards, agent evals and install list passed. Temporary installation of gen-testcase + spec-validate resolved the sibling lens byte-for-byte. First mechanical S7 check misclassified Markdown `../ywc-…` as slash command; explicit skills-root-relative reference removed ambiguity without changing reference authority or evaluator.
- Required full `validate.sh` passed via fresh precommit hook at `4ce326b4`; source/package checks, metadata and installed assets passed. Five-axis review found no findings. Parent clause-deletion probes killed observable-only and dedup-outcome removals; QA independently killed 22/22 asserted FR-7 clause deletions. No live behavior claimed. AC-8 and task-local AC-10 met; no deferred findings.
