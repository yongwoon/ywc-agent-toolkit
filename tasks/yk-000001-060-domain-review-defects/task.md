# yk-000001-060-domain-review-defects — Implementation Checklist

## Prerequisites
- [ ] Confirm the specification and repository baseline; no predecessor task is required.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-impl-review/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/review-defects.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Add A-005 checkout credentials, A-006 unawaited/boolean Promise, A-007 discarded errors with provenance and severity rationale; preserve existing catalog.
  - [ ] Apply this behavior in `codex/skills/ywc-impl-review/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Use only installed stack-appropriate changed-file linters: ruff S110/BLE001/B904, zizmor artipacked/unpinned-uses, TypeScript Promise rules and Go errcheck; report unavailable tools.
  - [ ] Apply this behavior in `codex/skills/ywc-impl-review/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Require verify-before-surface for every linter hit; do not install tools or change lint configuration.
  - [ ] Apply this behavior in `codex/skills/ywc-impl-review/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/review-defects.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] A-005–007 and installed targeted-linter evidence match the explicit expected results in test.md.
- [ ] Every scenario in test.md has positive/refusal evidence and a negative control for required source clauses.
- [ ] Existing source contracts and owned locale/eval metadata remain valid; unexecuted live behavior is recorded as UNVERIFIED.

## Task Verify
- [ ] `git diff --check`
- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] `git diff --check`
- [ ] `bash scripts/validate.sh` (required before PR).
- [ ] No application build/typecheck exists for this Markdown/Bash distribution; validate bundle structure and relevant evaluators.
