# yk-000001-100-domain-pr-worktrees — Implementation Checklist

## Prerequisites
- [ ] yk-000001-070-domain-operational-safety is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-worktrees/`
- [ ] `codex/skills/ywc-handle-pr-reviews/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/pr-worktrees.json`
- [ ] `tests/codex_issue69_behavior_test.py`
- [ ] `tests/fixtures/codex-issue69/upstream-behavior/pr-worktrees/`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Implement existing-branch producer contract before consumer wiring: mutually exclusive base flag, exact local/origin refs and distinct absent/network/checked-out/dirty/locked outcomes.
  - [ ] Apply this behavior in `codex/skills/ywc-worktrees/`, `codex/skills/ywc-handle-pr-reviews/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Require positive pinned same-repository open PR number and allowlisted check-ref-format head; clean canonical in-place/reused/created worktrees use exact fetch and fast-forward only; ahead/diverged blocks.
  - [ ] Apply this behavior in `codex/skills/ywc-worktrees/`, `codex/skills/ywc-handle-pr-reviews/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Recheck cwd/root/branch before every read/edit/API/commit/push/CI; one cwd reentry per invocation, then BLOCKED. Push only HEAD:refs/heads/$H.
  - [ ] Apply this behavior in `codex/skills/ywc-worktrees/`, `codex/skills/ywc-handle-pr-reviews/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Stop mutations on required command failure and report existing side effects; cleanup guidance applies only to created worktrees with branch preservation; keep audit classifications.
  - [ ] Apply this behavior in `codex/skills/ywc-worktrees/`, `codex/skills/ywc-handle-pr-reviews/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/pr-worktrees.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.
- [ ] Exercise the existing executable seams.
  - [ ] Extend `tests/codex_issue69_behavior_test.py` and the owned behavior fixture directory; invoke affected existing helpers in temporary Git/fake subprocess environments.
  - [ ] Keep descriptive Markdown traces separate from extracted runnable recipe evidence; do not add a production dispatcher.

## Acceptance Criteria
- [ ] Existing-branch producer and pinned PR worktree consumer match the explicit expected results in test.md.
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
