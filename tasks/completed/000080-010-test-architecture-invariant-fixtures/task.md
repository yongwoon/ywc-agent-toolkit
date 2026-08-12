# 000080-010-test-architecture-invariant-fixtures — Implementation Checklist

## Prerequisites
- [ ] Confirm the working tree changes in the spec/report are preserved.
- [ ] Confirm no other task is editing the shared evaluator test or registry files.

## Allowed Edit Scope
- [ ] Stay within the declared architecture fixture subtree.
- [ ] Edit the architecture skill or shared evaluator tests only when a fixture proves the existing contract is insufficient; stop and report first.

## Stop Conditions
- [ ] Stop if the required behavior cannot be expressed with the existing V2 schema and registry-owned verifiers.
- [ ] Stop if the fixture needs arbitrary execution, network access, credentials, or a path outside its fixture root.
- [ ] Stop if a shared validator, runner, or verifier change is required while another fixture task owns that surface.

## Hardening Gate
- [ ] Classify this as security-sensitive evaluator contract coverage.
- [ ] Add the failing/negative assertion before any conditional skill contract edit.
- [ ] Record the V2 fixture interface: manifest inputs, bounded checks, status/error outputs, and impacted tests.
- [ ] Data Integrity Hardening: N/A — read-only fixture/evaluator work.
- [ ] Require full implementation review or `ywc-impl-review` before completion.

## Implementation Steps
- [ ] Inspect `codex/skills/ywc-architecture-invariants/SKILL.md` and existing evaluator fixture patterns.
- [ ] Create contained fixture roots for one valid architecture case and assert the expected validation evidence.
- [ ] Create malformed/unsafe input coverage and assert rejection without executing verifier-supplied data.
- [ ] Create a no-manifest case and assert the documented `N/A — no architecture contract` fallback.
- [ ] Add only the smallest owning-skill correction if a fixture exposes an actual contract defect; otherwise leave the skill unchanged.
- [ ] Keep target skill and dependency lists explicit and run the fixture validator before the targeted runner checks.

## Task Verify
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`

## Verification
- [ ] Lint/structure passes (`bash scripts/validate.sh`)
- [ ] Typecheck: N/A — repository has no typecheck command
- [ ] Unit tests pass (the targeted Python test commands above)
- [ ] Integration tests: N/A — no live integration is permitted
- [ ] Build: N/A — repository has no application build

## Implementation Notes

