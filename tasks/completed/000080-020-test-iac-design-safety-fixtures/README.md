# 000080-020-test-iac-design-safety-fixtures

## Purpose
Add deterministic evidence for IaC authoring and infrastructure-design safety boundaries.

## Scope
- Cover missing-design clarification, validate/plan-only behavior, design artifact creation, and downstream handoff.
- Use separate fixture cases for `ywc-iac-author` and `ywc-infra-design`.
- Apply only evidence-driven contract fixes in the owning skill directories.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#acceptance-criteria` — AC2, AC3, and AC6.
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#existing-constraints-touched` — IaC author and infrastructure-design contracts.

### Summary
Fixtures must prove that IaC authoring asks for missing design evidence, stops at validation/planning, and preserves review handoff without apply. Infrastructure design must produce a design artifact and handoff without authoring Terraform in the same pass. All evidence runs through the existing offline fixture contract.

### Out of Scope (from spec)
- Architecture-invariants fixtures — handled by `000080-010-test-architecture-invariant-fixtures`.
- Optimization/review routing fixtures — handled by `000080-030-test-infra-routing-fixtures`.
- Live adapters, cloud credentials, Terraform execution, and mechanical baseline updates — out of scope for this batch.

## Criticality
critical

## Dependencies

### Depends On
- (None — root task.)

### Depended By
- `000081-010-infra-eval-rescore-report` — needs the IaC/design fixture results before scoring and reporting.

## Key Files
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-iac-author/**`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-infra-design/**`
- `codex/skills/ywc-iac-author/SKILL.md` and `codex/skills/ywc-infra-design/SKILL.md` — conditional contract fixes only.

## Notes
- Fixture assertions describe expected output only; they must not introduce `argv`, shell, environment, network, timeout, or executable fields.
- Keep each target's fixture subtree independently runnable.
- Stop before editing shared validator/runner/registry files; coordinate through a follow-up task if needed.

## Hardening Evidence

### Test Feedback Path
- RED-first target: target-specific fixture assertions for missing design, no-apply, and design-only handoff.
- Existing coverage: `test_fixture_validator.py`, `test_runner.py`, and the fake mocked suite.

### Interface Contract
- Contract: existing V2 fixture schema, fake runner, and registry-owned verifier boundary.
- Inputs: contained JSON manifests and target skill/dependency names.
- Outputs: clarification/status evidence, declared artifact checks, and no-apply/review-handoff signals.
- Error model: deterministic validation failure or `NEEDS_CONTEXT`/bounded evaluator status.
- Impacted tests: targeted fixture validation and runner checks.

### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review for no-apply and infrastructure safety boundaries.

### Data Integrity Hardening
- Trigger surface: N/A — read-only fixture/evaluator work.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-iac-author/**`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-infra-design/**`
- The two named `codex/skills/**/SKILL.md` files only for evidence-driven fixes.

### Shared Surfaces
- V2 fixture schema and fake runner.
- Registry-owned verifier names.

### Conflicts With
- `000080-010-test-architecture-invariant-fixtures` and `000080-030-test-infra-routing-fixtures` if shared evaluator framework files need edits.

### Parallelizable After
- Root task — no predecessor required.

### Task Verify
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`

## Out of Scope
- Live Terraform or cloud-provider operations.
- Shared evaluator framework redesign.
- Scoreboard/report edits.
