# yw-000064-010-domain-conditional-omission-lenses — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Conditional applicability

**Steps:**
1. Review a UI spec, authenticated-upload spec, and unrelated documentation spec using the same rubric.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Only triggered lenses apply; missing applicable observable requirements are reported without fabricated requirements.

### Scenario 2: Installed references and legacy compatibility

**Steps:**
1. Inspect installed lens links in the temporary install exercised by validate.sh; review a legacy spec without Failure Modes.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Both references resolve and absence of the legacy section alone is not a failure.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.

## Implementation Evidence

- Baseline `fb9fa13d`. AC-3/FR-3/FM-3: four source/fixture cases (UI, auth/upload, unrelated documentation, legacy) failed before edits (2 failures, 2 missing-reference errors); then passed after definitions and consumer wiring. Removing the trigger eligibility or N/A/no-invention clauses fails the unrelated-surface case. These are source assertions / fixture expectations, not model behavior.
- Interface: trigger/source evidence -> applicable row or N/A with reason -> observable omission/evidence gap using existing dimension severity. No new callable or state/schema interface.
- Quality Gate N/A — no quality gate contract. Unit RUN source fixtures; integration RUN generated package/temp installed references via validate.sh; security RUN focused negative applicability and security-lens source assertions (not a runtime scanner); mock service N/A (no runtime boundary implementation); performance N/A (no budget/claim). Full five-axis review required by critical metadata.
- Build/typecheck N/A for Markdown contracts. Preserve metadata/locales and source-first package synchronization; no Claude Code or release edits. Existing localized usage stays accurate (no new flag or changed invocation); no gratuitous locale edits.
- Description verification uses `--paths a-m` and `--paths n-z` per recorded run ruling.

- Final verification: focused runner, contract eval runner, both description partitions and agent checks (through validate.sh), full `bash scripts/validate.sh` in commit hook, install list, `git diff --check` passed. Both lens files were additionally installed into temporary CODEX_HOME and compared byte-for-byte with source.
- All five review lanes DONE, no findings/candidates. Added row-level handling/eligibility assertions; three in-memory eligibility/N-A/no-invention deletion mutations are rejected. Security RUN is limited to this source-contract negative evidence; no runtime/model security assurance is claimed.
