# yk-000001-090-domain-infra-evidence — Implementation Checklist

## Prerequisites
- [ ] yk-000001-080-domain-mission-anchor is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/agents/README.md`
- [ ] `codex/skills/ywc-infra-review/`
- [ ] `codex/agents/ywc-performance-engineer.toml`
- [ ] `codex/agents/evals/evals.json`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/infra-evidence.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Accept one-time evidence_type state_backend|apply_record|applied_commit, exact binding_target and applied yes/no without provider queries or extra required revision fields.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-infra-review/`, `codex/agents/ywc-performance-engineer.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Scoped-only missing/unbound/unapplied returns BLOCKED with no reviewers; valid binding with missing/truncated content returns NEEDS_CONTEXT.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-infra-review/`, `codex/agents/ywc-performance-engineer.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] For mixed input send identical eligible sets to all three lenses; exclude only ineligible scoped sets, never use them as fallback. Missing fresh or eligible content returns NEEDS_CONTEXT; preserve fresh-only/topology-only N/A headers and topology packets.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-infra-review/`, `codex/agents/ywc-performance-engineer.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Update performance agent to return bounded cost/risk alternatives inline; missing evidence returns NEEDS_CONTEXT; aggregator owns report files.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-infra-review/`, `codex/agents/ywc-performance-engineer.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/infra-evidence.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Eligible applied scope and bounded inline FinOps evidence match the explicit expected results in test.md.
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
