# yk-000001-110-domain-convergence-callers — Implementation Checklist

## Prerequisites
- [ ] yk-000001-030-domain-authoring-feedback is merged and its documented contract is available.
- [ ] yk-000001-100-domain-pr-worktrees is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-plan/`
- [ ] `codex/skills/ywc-auth-implement/`
- [ ] `codex/skills/ywc-agentic/`
- [ ] `codex/skills/ywc-skill-author/references/cross-skill-graph.md`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/convergence-callers.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Auto-run spec-ready once for new Medium/Large specifications; exclude no-converge, noninteractive, Small and Re-plan paths. Auth and agentic own their readiness and pass planner no-converge.
  - [ ] Apply this behavior in `codex/skills/ywc-plan/`, `codex/skills/ywc-auth-implement/`, `codex/skills/ywc-agentic/`, `codex/skills/ywc-skill-author/references/cross-skill-graph.md`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Preserve agentic artifact profile and Result/Status/Scale/Artifact authority in interactive/noninteractive paths; preserve spec-ready goal and Re-plan termination boundaries.
  - [ ] Apply this behavior in `codex/skills/ywc-plan/`, `codex/skills/ywc-auth-implement/`, `codex/skills/ywc-agentic/`, `codex/skills/ywc-skill-author/references/cross-skill-graph.md`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Inspect other callers for duplicate convergence and update cross-skill-graph for convergence and PR worktree boundaries.
  - [ ] Apply this behavior in `codex/skills/ywc-plan/`, `codex/skills/ywc-auth-implement/`, `codex/skills/ywc-agentic/`, `codex/skills/ywc-skill-author/references/cross-skill-graph.md`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/convergence-callers.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Single-owner convergence and artifact-profile preservation match the explicit expected results in test.md.
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
