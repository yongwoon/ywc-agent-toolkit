# yk-000001-120-domain-pr-body — Implementation Checklist

## Prerequisites
- [ ] Confirm the specification and repository baseline; no predecessor task is required.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-create-pr/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/pr-body.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Write Changes by feature with supported what/location/intent; preserve template sections and update Step 7 skip.
  - [ ] Apply this behavior in `codex/skills/ywc-create-pr/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add Method+Path API table only for endpoint addition/deletion or request/response/auth/status changes, including auth/schema-only changes bound to a route; exclude internal refactors.
  - [ ] Apply this behavior in `codex/skills/ywc-create-pr/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Order deleted/changed/new rows; omit host/token/query values; place after Impact or body/Design Background fallback; cover template/update/language cases.
  - [ ] Apply this behavior in `codex/skills/ywc-create-pr/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/pr-body.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Feature Changes and conditional API table match the explicit expected results in test.md.
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
