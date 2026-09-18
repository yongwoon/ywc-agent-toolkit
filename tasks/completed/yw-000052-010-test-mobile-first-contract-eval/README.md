# yw-000052-010-test-mobile-first-contract-eval

## Purpose
Lock the mobile-first contract with deterministic source checks across the shared reference, five consumers, reviewer directive, and eval record.

## Scope
Extend `scripts/run-codex-skill-contract-evals.sh` with `check_mobile_first_ui_contract`. The check must validate trigger, `min-width` order, exception, and no-retrofit semantics and reject missing or inconsistent consumers.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md#quality-gate-contract`
- `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md#functional-requirements`

### Summary
The deterministic runner is the outcome oracle for source-contract consistency. It must inspect the shared reference, plan/scaffold/task-generator/sequential/parallel skill files, the TypeScript reviewer TOML, and its eval record. It also invokes the existing agent-eval checker in the verification sequence.

### Out of Scope (from spec)
- Policy and consumer implementation — handled by earlier tasks.
- Plugin synchronization and final full validation — handled by `yw-000053-010-infra-mobile-first-distribution`.

## Criticality
normal — deterministic validation script only.

## Dependencies

### Depends On
- `yw-000051-010-docs-mobile-first-consumers` — provides finalized skill consumers.
- `yw-000051-020-docs-mobile-first-reviewer` — provides finalized reviewer directive and eval record.

### Depended By
- `yw-000053-010-infra-mobile-first-distribution` — requires the source contract check before sync and final validation.

## Key Files
- `scripts/run-codex-skill-contract-evals.sh`

## Notes
Use explicit token/relationship checks rather than relying on ad hoc `rg` diagnostics as verification evidence.

## Hardening Evidence

### Test Feedback Path
- RED-first target: `bash scripts/run-codex-skill-contract-evals.sh` against missing/inconsistent policy tokens.
- Existing coverage: current JSON-shape and contract checks in the same runner.

### Interface Contract
- Contract: `check_mobile_first_ui_contract`
- Owner task: `yw-000052-010-test-mobile-first-contract-eval`
- Canonical signature: `repository source tree -> pass/fail deterministic contract result`
- Consumers: `yw-000053-010-infra-mobile-first-distribution`
- Implementation opacity: distribution task trusts the checker result and does not duplicate its assertions.
- Mismatch action: `NEEDS_CONTEXT`

### Critical Surface Review
- Review requirement: `N/A — validation-only script`

### Data Integrity Hardening
- Trigger surface: `N/A — read-only validation`
- Atomic / locking strategy: `N/A`
- Transaction boundary: `N/A`
- Idempotency guard: `N/A`
- Required tests: `N/A`

## Parallel Execution Metadata

### Ownership
- `scripts/run-codex-skill-contract-evals.sh`

### Shared Surfaces
- All five named Codex skill consumers, reviewer TOML, and eval JSON.

### Conflicts With
- `(None identified — all consumer edits are complete before this task starts.)`

### Parallelizable After
- `yw-000051-010-docs-mobile-first-consumers`
- `yw-000051-020-docs-mobile-first-reviewer`

### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/check-codex-agent-evals.sh`
- `git diff --check`

## Out of Scope
Do not modify policy prose, consumer skills, reviewer TOML/eval content, generated plugin output, or Claude Code surfaces.
