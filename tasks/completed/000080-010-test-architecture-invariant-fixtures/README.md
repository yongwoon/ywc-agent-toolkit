# 000080-010-test-architecture-invariant-fixtures

## Purpose
Add deterministic evaluator evidence for the architecture-invariants safety contract.

## Scope
- Add valid, malformed/unsafe, and no-manifest fixture cases using the existing V2 schema.
- Prove validation-only behavior and that unsafe verifier input cannot execute.
- Change `codex/skills/ywc-architecture-invariants/SKILL.md` only if a fixture exposes a real contract defect.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#acceptance-criteria` — AC1 and AC6 define the required evidence and schema boundary.
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#existing-constraints-touched` — architecture skill and evaluator ownership constraints.

### Summary
The evaluator must demonstrate valid architecture validation, safe rejection of malformed or unsafe input, and the documented no-manifest fallback. Fixtures must use only the existing validator, fake runner, and registry-owned verifier contract. The current skill contract remains authoritative unless the evidence identifies a concrete defect.

### Out of Scope (from spec)
- Infrastructure skill fixtures — handled by `000080-020-test-iac-design-safety-fixtures` and `000080-030-test-infra-routing-fixtures`.
- Live-adapter evaluation, new execution mechanisms, and mechanical baseline changes — handled by neither this task nor this batch.

## Criticality
critical

## Dependencies

### Depends On
- (None — root task.)

### Depended By
- `000081-010-infra-eval-rescore-report` — needs the completed architecture fixture evidence and passing targeted checks.

## Key Files
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-architecture-invariants/**` — architecture fixture manifests and inputs.
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py` — extend only if the existing contract cannot express AC1 safely.
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py` — extend only for a missing shared boundary regression.
- `codex/skills/ywc-architecture-invariants/SKILL.md` — conditional smallest contract correction only.

## Notes
- Keep fixture files under their fixture root and declare dependencies explicitly.
- Do not add commands, shell, environment, network, timeout, or arbitrary executable fields to fixture data.
- Do not edit shared evaluator files while `000080-020` or `000080-030` is active; stop and report if required.

## Hardening Evidence

### Test Feedback Path
- RED-first target: add or extend the architecture fixture assertion before production skill edits.
- Existing coverage: `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py` and targeted `runner.py` execution.

### Interface Contract
- Contract: existing V2 fixture schema and `bundle.validate` verifier registry.
- Inputs: JSON fixture manifest plus contained fixture files.
- Outputs: validator/runner status and bounded evidence checks.
- Error model: deterministic `FixtureValidationError`, `FAIL`, or documented no-manifest fallback.
- Impacted tests: `test_fixture_validator.py`, `test_runner.py`, targeted fixture command.

### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review for unsafe-input and execution-boundary changes.

### Data Integrity Hardening
- Trigger surface: N/A — read-only fixture and evaluator evidence.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-architecture-invariants/**`
- `codex/skills/ywc-architecture-invariants/SKILL.md` only for an evidence-driven contract fix.

### Shared Surfaces
- V2 fixture schema and verifier registry.
- `.codex/skills/ywc-codex-toolkit-eval/scripts/test_*.py` only if a shared regression is unavoidable.

### Conflicts With
- `000080-020-test-iac-design-safety-fixtures` — shared evaluator test files if extension is required.
- `000080-030-test-infra-routing-fixtures` — shared evaluator test files if extension is required.

### Parallelizable After
- Root task — no predecessor required.

### Task Verify
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`

## Out of Scope
- Changes to the evaluator schema or runner architecture unless the existing contract demonstrably cannot express the required safety assertion.
- Report, scoreboard, or baseline updates.
