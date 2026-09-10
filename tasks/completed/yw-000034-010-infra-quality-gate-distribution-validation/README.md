# yw-000034-010-infra-quality-gate-distribution-validation

## Purpose
Synchronize the generated Codex marketplace package and run the complete quality-gate validation hard gate.

## Scope
Update only necessary Codex localized READMEs/catalog surfaces, regenerate `plugins/ywc-agent-toolkit/skills/`, verify source/package parity, run contract evals, installer tests, and repository validation.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-7-codex-catalog-and-generated-package-release`
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#outcome-oracle`
- `scripts/sync-codex-plugin.sh`
- `scripts/validate.sh`
### Summary
This is the final hard gate after all source consumers are complete. The generated marketplace package is derived from `codex/skills/`, must match source, and must expose both workers in the installed catalog. Validation must cover all AC1–AC7 and report no unresolved boundary, packet, status, or evidence failures.
### Out of Scope (from spec)
- New feature behavior or late source implementation.
- Claude Code bundle changes and generic evaluation-harness changes.

## Criticality
critical

## Dependencies
### Depends On
- `yw-000033-010-domain-sequential-quality-gate`
- `yw-000033-020-domain-parallel-quality-gate`
- `yw-000033-030-domain-review-quality-evidence`
### Depended By
- (None — final validation task)

## Key Files
- `plugins/ywc-agent-toolkit/skills/**` — generated package output.
- Necessary Codex localized READMEs/catalog files.
- Existing validation/install scripts and fixtures only if targeted assertions are required.

## Notes
Never edit generated package source first. Use the repository sync script. Do not add a parallel structural validator.

## Hardening Evidence
### Test Feedback Path
- RED-first target: `bash scripts/run-codex-skill-contract-evals.sh`, installer test, and `bash scripts/validate.sh` before final sync.
### Interface Contract
- Contract: Codex source bundle → generated marketplace package
- Owner task: this task
- Canonical signature: source tree + sync script → byte-current generated package and passing validation
- Consumers: release/installation workflow
- Implementation opacity: downstream release consumers use generated output only after validation.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: manual full implementation review plus `ywc-impl-review`.
### Data Integrity Hardening
- Trigger surface: generated artifact replacement
- Atomic / locking strategy: sync script replacement semantics
- Transaction boundary: complete source-to-package sync before validation
- Idempotency guard: repeatable sync and byte-current comparison
- Required tests: repeat sync, installer enumeration, validation failure on stale output.

## Parallel Execution Metadata
### Ownership
- `plugins/ywc-agent-toolkit/skills/**`
- Necessary Codex README/catalog and targeted validation fixture surfaces.
### Shared Surfaces
- Entire generated Codex package.
- `scripts/validate.sh` and contract eval runner.
### Conflicts With
- All Phase `yw-000033` tasks — this task starts only after their merge.
### Parallelizable After
- `yw-000033-010-domain-sequential-quality-gate`
- `yw-000033-020-domain-parallel-quality-gate`
- `yw-000033-030-domain-review-quality-evidence`
### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash tests/install-codex-agents-test.sh`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/validate.sh`

## Out of Scope
Late behavioral changes, Claude Code files, generic eval harness, CRAP/mutation dependencies, and delivery actions beyond validation/reporting.
