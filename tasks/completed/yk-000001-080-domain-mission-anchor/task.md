# yk-000001-080-domain-mission-anchor — Implementation Checklist

## Prerequisites
- [ ] Confirm the specification and repository baseline; no predecessor task is required.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-mission/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/mission-anchor.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Port full frozen #348 mission skill and mission-format reference, Tier 1 locales, metadata and evals.
  - [ ] Apply this behavior in `codex/skills/ywc-mission/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Support read/update/curate at docs/mission.md; read absence yields empty anchor. Read whole file and present exact ADD/MODIFY/DEPRECATE CHANGESET before confirmed nonempty writes.
  - [ ] Apply this behavior in `codex/skills/ywc-mission/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Keep one active mission, observable SC+rationale, RA reason, stable IDs/provenance/history and optional NG reason/CN rationale; anchors include active entries only. Empty/dry-run changes do not write or update dates; preserve deprecated history and offer steering activation guidance only.
  - [ ] Apply this behavior in `codex/skills/ywc-mission/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/mission-anchor.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Read/update/curate mission with stable NG/CN history match the explicit expected results in test.md.
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
