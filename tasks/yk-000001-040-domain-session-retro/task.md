# yk-000001-040-domain-session-retro — Implementation Checklist

## Prerequisites
- [ ] yk-000001-030-domain-authoring-feedback is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/skills/ywc-retro/agents/openai.yaml`
- [ ] `codex/skills/ywc-retro/`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/session-retro.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Port the frozen #345 Codex retro skill with Tier 1 locales, openai.yaml and numeric eval IDs preserving upstream source_id.
  - [ ] Apply this behavior in `codex/skills/ywc-retro/agents/openai.yaml`, `codex/skills/ywc-retro/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Cover Navigation, Automated checks, Coding standards, Steering files, Tool economy, No-ops, Information access; deduplicate evidence occurrences and sort by priority, occurrence count, first occurrence, input order.
  - [ ] Apply this behavior in `codex/skills/ywc-retro/agents/openai.yaml`, `codex/skills/ywc-retro/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Use supplied conversation/attachments only; include priority rationale, category, redacted evidence, proposed change and established owner or explicit Unassigned; empty evidence yields no candidates.
  - [ ] Apply this behavior in `codex/skills/ywc-retro/agents/openai.yaml`, `codex/skills/ywc-retro/`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/session-retro.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Retro categories, ranking, evidence and owner rules match the explicit expected results in test.md.
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
