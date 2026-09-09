# yw-000021-020-test-impl-review-verification-evals

## Purpose

Encode the independent-verification and scope-guardrail behavior in the Codex skill contract-eval fixture. The scenarios keep the instruction-level orchestration contract mechanically reviewable.

## Scope

- Extend the `ywc-impl-review` eval fixture with focused assertions for AC1–AC5.
- Preserve the existing fixture schema and existing architecture-packet scenarios.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#acceptance-criteria` — AC1–AC5 required behavior.
- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#edge-cases` — threshold, cap, and error classifications.

### Summary

The fixture must assert empty and excessive scope refusals, blind verifier packets, the 20-call ordering/cap, every verification result class, and Phase 2 or `--no-advisor` routing. It is a behavioral documentation contract, not a runtime test fixture or a new verifier implementation.

### Out of Scope (from spec)

- Source workflow implementation — handled by `yw-000021-010-domain-impl-review-verification-contract`.
- README locale alignment — handled by `yw-000021-030-docs-impl-review-localized-flow`.
- Package synchronization — handled by `yw-000022-010-infra-impl-review-package-validation`.

## Criticality

normal

## Dependencies

### Depends On

- `yw-000021-010-domain-impl-review-verification-contract` — provides the finalized names, ordering, and report contract to encode.

### Depended By

- `yw-000022-010-infra-impl-review-package-validation` — validates the completed source eval fixture and mirrors it.

## Key Files

- `codex/skills/ywc-impl-review/evals/evals.json` — behavioral contract-eval fixture.

## Notes

Keep each scenario focused on observable orchestration behavior. Do not add custom-agent implementations, runtime fixtures, or a new evaluator script. `contract_state: N/A — no architecture contract`.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `codex/skills/ywc-impl-review/evals/evals.json` assertions for newly required tokens and expected behavior.
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh`.

### Interface Contract

- Contract: Implementation-review orchestration protocol.
- Owner task: `yw-000021-010-domain-impl-review-verification-contract`.
- Canonical signature: `selected target + Phase 1 findings -> scope decision, verification status, Phase 2 candidate priority, report fields`.
- Consumers: this eval fixture and `yw-000021-030-docs-impl-review-localized-flow`.
- Implementation opacity: verify the documented protocol rather than redefining it.
- Mismatch action: `NEEDS_CONTEXT`.
- Inputs: target-mode and verifier-outcome prompts.
- Outputs: expected bounded status and report/dispatch assertions.
- Error model: malformed verifier output maps to `verification-error`.
- Impacted tests: `bash scripts/run-codex-skill-contract-evals.sh`.

### Critical Surface Review

- Review requirement: N/A — test-fixture-only task.

### Data Integrity Hardening

- Trigger surface: N/A — test-fixture-only task.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-impl-review/evals/evals.json`

### Shared Surfaces

- Implementation-review orchestration protocol owned by `yw-000021-010-domain-impl-review-verification-contract`.
- JSON fixture schema enforced by `scripts/run-codex-skill-contract-evals.sh`.

### Conflicts With

- `yw-000021-010-domain-impl-review-verification-contract` — use the merged protocol terminology before editing assertions.
- `yw-000022-010-infra-impl-review-package-validation` — do not sync the plugin while this source fixture is in flight.

### Parallelizable After

- `yw-000021-010-domain-impl-review-verification-contract`

### Task Verify

- `jq empty codex/skills/ywc-impl-review/evals/evals.json`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope

Do not modify `SKILL.md`, README locales, generated plugin content, or the contract-eval runner.
