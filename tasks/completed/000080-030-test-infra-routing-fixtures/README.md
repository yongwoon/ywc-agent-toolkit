# 000080-030-test-infra-routing-fixtures

## Purpose
Add deterministic evidence for infrastructure optimization routing and review completeness.

## Scope
- Cover SAFE, CAUTION, and DANGER classification with remediation routing to IaC authoring and no auto-execution.
- Prove infrastructure review runs security, cost, and reliability lenses and blocks on Critical/High findings.
- Apply only evidence-driven contract fixes in the two owning skills.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#acceptance-criteria` — AC4, AC5, and AC6.
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#existing-constraints-touched` — optimization and review contracts.

### Summary
Optimization fixtures must make all three safety classifications observable and prove that remediation is routed to `ywc-iac-author` without automatic execution. Review fixtures must require all three review lenses and produce an explicit BLOCK recommendation for Critical/High findings. Assertions remain offline and registry-owned.

### Out of Scope (from spec)
- Architecture, IaC-author, and design fixtures — handled by `000080-010-test-architecture-invariant-fixtures` and `000080-020-test-iac-design-safety-fixtures`.
- Live adapters, cloud credentials, infrastructure changes, and baseline updates — out of scope for this batch.

## Criticality
critical

## Dependencies

### Depends On
- (None — root task.)

### Depended By
- `000081-010-infra-eval-rescore-report` — needs routing/review evidence before the final scorecard pass.

## Key Files
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-infra-optimize/**`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-infra-review/**`
- `codex/skills/ywc-infra-optimize/SKILL.md` and `codex/skills/ywc-infra-review/SKILL.md` — conditional contract fixes only.

## Notes
- Do not encode executable commands, shell, environment, network, timeout, or credential fields in fixtures.
- Keep optimization and review fixture cases independently diagnosable.
- Stop before editing shared evaluator framework files.

## Hardening Evidence

### Test Feedback Path
- RED-first target: target-specific classification and lens/blocking fixture assertions.
- Existing coverage: `test_fixture_validator.py`, `test_runner.py`, and the fake mocked suite.

### Interface Contract
- Contract: existing V2 fixture schema, target/dependency inventory, and registry-owned verifier checks.
- Inputs: contained manifests and bounded evidence packets.
- Outputs: classification, routing, lens-completeness, and BLOCK recommendation evidence.
- Error model: deterministic schema rejection or bounded evaluator failure.
- Impacted tests: targeted fixture validation and runner checks.

### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review for safety routing and blocking behavior.

### Data Integrity Hardening
- Trigger surface: N/A — read-only fixture/evaluator work.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-infra-optimize/**`
- `.codex/skills/ywc-codex-toolkit-eval/evals/fixtures/ywc-infra-review/**`
- The two named `codex/skills/**/SKILL.md` files only for evidence-driven fixes.

### Shared Surfaces
- V2 fixture schema, fake runner, and IaC-author routing contract.
- Registry-owned verifier names.

### Conflicts With
- `000080-010-test-architecture-invariant-fixtures` and `000080-020-test-iac-design-safety-fixtures` if shared evaluator framework files need edits.

### Parallelizable After
- Root task — no predecessor required.

### Task Verify
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`

## Out of Scope
- Automatic remediation or Terraform apply.
- Shared evaluator framework redesign.
- Scoreboard/report edits.
