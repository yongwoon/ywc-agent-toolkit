# yw-000022-010-infra-impl-review-package-validation

## Purpose

Synchronize the finished authoritative Codex skill into its generated marketplace mirror and prove source, package, eval, and repository validation integrity.

## Scope

- Run source checks, synchronize `plugins/ywc-agent-toolkit/skills/ywc-impl-review/`, and prove parity.
- Confirm that no `codex/agents/*.toml` file changes as part of the feature.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#verification` — required commands and evidence.
- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#acceptance-criteria` — AC7 package-integrity requirement.

### Summary

The marketplace package is generated exclusively from `codex/skills/` after all source SKILL, eval, and README changes are complete. This task runs the named JSON, contract-eval, synchronization, parity, and structural-validation gates, then verifies custom agents stayed untouched.

### Out of Scope (from spec)

- Source workflow changes — handled by `yw-000021-010-domain-impl-review-verification-contract`.
- Eval fixture changes — handled by `yw-000021-020-test-impl-review-verification-evals`.
- Locale README edits — handled by `yw-000021-030-docs-impl-review-localized-flow`.
- Any custom-agent implementation or TOML modification — excluded by the specification.

## Criticality

normal

## Dependencies

### Depends On

- `yw-000021-010-domain-impl-review-verification-contract` — finalized source SKILL behavior.
- `yw-000021-020-test-impl-review-verification-evals` — finalized source eval fixture.
- `yw-000021-030-docs-impl-review-localized-flow` — finalized source README locales.

### Depended By

- (None — terminal task for this task set.)

## Key Files

- `plugins/ywc-agent-toolkit/skills/ywc-impl-review/**` — generated mirror updated by the sync script.

## Notes

Run synchronization only after all Phase 21 changes are merged. Do not hand-edit generated content. `contract_state: N/A — no architecture contract`.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `jq empty codex/skills/ywc-impl-review/evals/evals.json`, `bash scripts/run-codex-skill-contract-evals.sh`, and `bash scripts/validate.sh`.

### Interface Contract

- Contract: Source-to-marketplace generated package parity.
- Owner task: `yw-000022-010-infra-impl-review-package-validation`.
- Canonical signature: `codex/skills/ywc-impl-review/** -> plugins/ywc-agent-toolkit/skills/ywc-impl-review/**`.
- Consumers: marketplace package users and repository validation.
- Implementation opacity: use `bash scripts/sync-codex-plugin.sh`; do not manually reconstruct generated files.
- Mismatch action: `NEEDS_CONTEXT`.
- Inputs: merged authoritative source skill directory.
- Outputs: byte-equivalent generated skill directory.
- Error model: source/package mismatch or validation failure blocks completion.
- Impacted tests: `diff -qr codex/skills/ywc-impl-review plugins/ywc-agent-toolkit/skills/ywc-impl-review`; `bash scripts/validate.sh`.

### Critical Surface Review

- Review requirement: N/A — generated-distribution and validation task.

### Data Integrity Hardening

- Trigger surface: N/A — generated-distribution task.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `plugins/ywc-agent-toolkit/skills/ywc-impl-review/**` generated only through `bash scripts/sync-codex-plugin.sh`.

### Shared Surfaces

- Source-to-plugin sync contract.
- Repository-wide structural validation in `scripts/validate.sh`.

### Conflicts With

- `yw-000021-010-domain-impl-review-verification-contract` — source must be complete before sync.
- `yw-000021-020-test-impl-review-verification-evals` — source fixture must be complete before sync.
- `yw-000021-030-docs-impl-review-localized-flow` — source locales must be complete before sync.

### Parallelizable After

- `yw-000021-010-domain-impl-review-verification-contract`
- `yw-000021-020-test-impl-review-verification-evals`
- `yw-000021-030-docs-impl-review-localized-flow`

### Task Verify

- `jq empty codex/skills/ywc-impl-review/evals/evals.json`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/sync-codex-plugin.sh`
- `diff -qr codex/skills/ywc-impl-review plugins/ywc-agent-toolkit/skills/ywc-impl-review`
- `bash scripts/validate.sh`
- `git diff -- codex/agents/*.toml`

## Out of Scope

Do not edit authoritative `codex/skills/ywc-impl-review` source files or any `codex/agents/*.toml` file; report source defects to their owning Phase 21 task.
