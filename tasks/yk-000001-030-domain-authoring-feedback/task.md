# yk-000001-030-domain-authoring-feedback — Implementation Checklist

## Prerequisites
- [ ] yk-000001-020-domain-analyst-modes is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-brainstorm/`
- [ ] `codex/skills/ywc-tdd-ritual/`
- [ ] `codex/skills/ywc-skill-author/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/authoring-feedback.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Inspect repository facts before asking one unresolved prerequisite question; retain approval gates.
  - [ ] Apply this behavior in `codex/skills/ywc-brainstorm/`, `codex/skills/ywc-tdd-ritual/`, `codex/skills/ywc-skill-author/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Record public-seam catches/misses and finish one behavior RED/GREEN/REFACTOR cycle before another; do not expose private helpers.
  - [ ] Apply this behavior in `codex/skills/ywc-brainstorm/`, `codex/skills/ywc-tdd-ritual/`, `codex/skills/ywc-skill-author/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add Writing Levers: remove no-ops, positive goals, conditions first, observable completion, canonical references.
  - [ ] Apply this behavior in `codex/skills/ywc-brainstorm/`, `codex/skills/ywc-tdd-ritual/`, `codex/skills/ywc-skill-author/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/authoring-feedback.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Repository-first questions, behavior TDD and Writing Levers match the explicit expected results in test.md.
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
