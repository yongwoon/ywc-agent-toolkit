# yk-000001-020-domain-analyst-modes — Implementation Checklist

## Prerequisites
- [ ] yk-000001-010-domain-model-hints is merged and its documented contract is available.

## Allowed Edit Scope
- [ ] `codex/agents/README.md`
- [ ] `codex/skills/ywc-debug-rootcause/`
- [ ] `codex/skills/ywc-incident-postmortem/`
- [ ] `codex/skills/ywc-confidence-gate/`
- [ ] `codex/agents/ywc-root-cause-analyst.toml`
- [ ] `codex/agents/evals/evals.json`
- [ ] `tests/fixtures/codex-issue69/upstream-adoption/analyst-modes.json`
- [ ] Stop before editing any path outside README Ownership.

## Stop Conditions
- [ ] Stop on missing prerequisite, ownership spill, ambiguous frozen-source provenance, contract mismatch or failed required verification.

## Hardening Gate
- [ ] Record baseline and RED-first focused fixture evidence or a named exception before source changes.
- [ ] Record cross-task input/output/status contracts from the spec; require NEEDS_CONTEXT on mismatch.
- [ ] Apply Data Integrity Hardening to triggered writes/retries and require full review for critical surfaces.

## Implementation Steps
- [ ] Update the analyst TOML and all three callers atomically: debug_hypotheses, incident_five_whys, confidence_root_cause; missing/unknown/mismatched pairs return NEEDS_CONTEXT.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-debug-rootcause/`, `codex/skills/ywc-incident-postmortem/`, `codex/skills/ywc-confidence-gate/`, `codex/agents/ywc-root-cause-analyst.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Record minimal feedback catches/misses; rank 3–5 falsifiable debug candidates and change one variable per experiment. Preserve incident 5 Whys and confidence evidence for/against one cause.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-debug-rootcause/`, `codex/skills/ywc-incident-postmortem/`, `codex/skills/ywc-confidence-gate/`, `codex/agents/ywc-root-cause-analyst.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Stop after three failed fixes; permit a fourth debug attempt only with both evidence-linked Fix #4 signal and Next fix worth attempting fields.
  - [ ] Apply this behavior in `codex/agents/README.md`, `codex/skills/ywc-debug-rootcause/`, `codex/skills/ywc-incident-postmortem/`, `codex/skills/ywc-confidence-gate/`, `codex/agents/ywc-root-cause-analyst.toml`, `codex/agents/evals/evals.json`.
  - [ ] Check the corresponding expected/refusal cases in `test.md`; retain existing gates and public contracts.
- [ ] Add focused source-contract evidence.
  - [ ] Create `tests/fixtures/codex-issue69/upstream-adoption/analyst-modes.json` with unique id, requirements, source checks, required clauses and forbidden clauses following the existing fixture schema.
  - [ ] Run `python3 tests/codex_issue69_contract_test.py`; the runner auto-discovers this fixture. Remove each required clause in a temporary copy to prove its negative control.

## Acceptance Criteria
- [ ] Three caller/mode pairs and bounded diagnostic feedback match the explicit expected results in test.md.
- [ ] Every scenario in test.md has positive/refusal evidence and a negative control for required source clauses.
- [ ] Existing source contracts and owned locale/eval metadata remain valid; unexecuted live behavior is recorded as UNVERIFIED.

## Task Verify
- [ ] `git diff --check`
- [ ] `python3 tests/codex_issue69_contract_test.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/check-codex-agent-evals.sh`

## Verification
- [ ] `git diff --check`
- [ ] `bash scripts/validate.sh` (required before PR).
- [ ] No application build/typecheck exists for this Markdown/Bash distribution; validate bundle structure and relevant evaluators.
