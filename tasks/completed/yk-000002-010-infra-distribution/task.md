# yk-000002-010-infra-distribution — Implementation Checklist

## Prerequisites
- [ ] yk-000001-010-domain-model-hints is merged and its documented contract is available.
- [ ] yk-000001-020-domain-analyst-modes is merged and its documented contract is available.
- [ ] yk-000001-030-domain-authoring-feedback is merged and its documented contract is available.
- [ ] yk-000001-040-domain-session-retro is merged and its documented contract is available.
- [ ] yk-000001-050-domain-session-handoff is merged and its documented contract is available.
- [ ] yk-000001-060-domain-review-defects is merged and its documented contract is available.
- [ ] yk-000001-070-domain-operational-safety is merged and its documented contract is available.
- [ ] yk-000001-080-domain-mission-anchor is merged and its documented contract is available.
- [ ] yk-000001-090-domain-infra-evidence is merged and its documented contract is available.
- [ ] yk-000001-100-domain-pr-worktrees is merged and its documented contract is available.
- [ ] yk-000001-110-domain-convergence-callers is merged and its documented contract is available.
- [ ] yk-000001-120-domain-pr-body is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `README.es.md`, `README.ja.md`, `README.ko.md`, `README.md`, `README.zh.md`
- [ ] `codex/README.md`
- [ ] `codex/agents/README.md`
- [ ] `plugins/ywc-agent-toolkit/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/distribution.json`
- [ ] `tests/codex_issue69_behavior_test.py`
- [ ] `tests/fixtures/codex-issue69/upstream-behavior/distribution/`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Update repository skill catalogs, agent documentation, locales and actual counts for the completed source bundle; regenerate plugin from source.
  - [ ] Apply this behavior in `codex/README.md`, `codex/agents/README.md`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Verify unique numeric skill eval IDs with source_id provenance and nonempty agent expectations. Run contract, behavior, installation and validation gates.
  - [ ] Apply this behavior in `codex/README.md`, `codex/agents/README.md`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Test selected new skills and agent-only installs with temporary CODEX_HOME; distinguish source assertions, expected traces, extracted runnable recipes, existing helper execution and live evidence. Record unavailable live execution as UNVERIFIED.
  - [ ] Apply this behavior in `codex/README.md`, `codex/agents/README.md`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/distribution.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Catalog counts/locales, generated plugin and temporary installs match the explicit expected results in test.md.
- [ ] Every scenario in test.md has positive/refusal evidence and a negative control for required source clauses.
- [ ] Existing source contracts and owned locale/eval metadata remain valid; unexecuted live behavior is recorded as UNVERIFIED.

## Task Verify
- [ ] `git diff --check`
- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `python3 tests/codex_issue69_behavior_test.py`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/install.sh --list --codex-agents`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] `git diff --check`
- [ ] `bash scripts/validate.sh` (required before PR).
- [ ] No application build/typecheck exists for this Markdown/Bash distribution; validate bundle structure and relevant evaluators.
