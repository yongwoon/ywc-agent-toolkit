# yk-000001-070-domain-operational-safety — Implementation Checklist

## Prerequisites
- [ ] yk-000001-060-domain-review-defects is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-finish-branch/`
- [ ] `codex/skills/ywc-parallel-executor/`
- [ ] `codex/skills/ywc-merge-dependabot/`
- [ ] `codex/skills/ywc-security-audit/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json`
- [ ] `tests/codex_issue69_behavior_test.py`
- [ ] `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Gate remote deletion on valid branch and successful parsed empty open-PR query; merged evidence must bind intended base and current remote tip.
  - [ ] Apply this behavior in `codex/skills/ywc-finish-branch/`, `codex/skills/ywc-parallel-executor/`, `codex/skills/ywc-merge-dependabot/`, `codex/skills/ywc-security-audit/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Block all nonzero isolation setup results including 127 before any worker; preserve already conforming behavior.
  - [ ] Apply this behavior in `codex/skills/ywc-finish-branch/`, `codex/skills/ywc-parallel-executor/`, `codex/skills/ywc-merge-dependabot/`, `codex/skills/ywc-security-audit/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Detect Dockerfile FROM changes and preserve one total 1800-second polling deadline across chunks; timeout is not success.
  - [ ] Apply this behavior in `codex/skills/ywc-finish-branch/`, `codex/skills/ywc-parallel-executor/`, `codex/skills/ywc-merge-dependabot/`, `codex/skills/ywc-security-audit/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Use prompt-injection severity row conditions, retaining item 2 no-downgrade; add explicit-invocation preference for merge-dependabot.
  - [ ] Apply this behavior in `codex/skills/ywc-finish-branch/`, `codex/skills/ywc-parallel-executor/`, `codex/skills/ywc-merge-dependabot/`, `codex/skills/ywc-security-audit/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.
- [ ] Exercise the existing executable seams.
  - [ ] Create `tests/codex_issue69_behavior_test.py` and the owned behavior fixture directory; invoke affected existing helpers in temporary Git/fake subprocess environments.
  - [ ] Keep descriptive Markdown traces separate from extracted runnable recipe evidence; do not add a production dispatcher.

## Acceptance Criteria
- [ ] Remote deletion, isolation setup, polling deadline and severity row guards match the explicit expected results in test.md.
- [ ] Every scenario in test.md has positive/refusal evidence and a negative control for required source clauses.
- [ ] Existing source contracts and owned locale/eval metadata remain valid; unexecuted live behavior is recorded as UNVERIFIED.

## Task Verify
- [ ] `git diff --check`
- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `python3 tests/codex_issue69_behavior_test.py`

## Verification
- [ ] `git diff --check`
- [ ] `bash scripts/validate.sh` (required before PR).
- [ ] No application build/typecheck exists for this Markdown/Bash distribution; validate bundle structure and relevant evaluators.
