# yw-000033-020-domain-parallel-quality-gate

## Purpose
Insert bounded quality gates into parallel task waves with safe worktree preservation and deterministic aggregation.

## Scope
Run Cleaner per eligible task before wave delivery, run Hardener only after Cleaner permits it, aggregate mutation evidence at the wave boundary, and preserve blocked worktrees/branches.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-5-parallel-executor-gate`
- `codex/skills/references/quality-gates.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
### Summary
Parallel execution must apply the same bounded worker semantics as sequential execution without allowing one task’s DONE to mask another task’s concern. Cleaner is task-local, Hardener follows only an allowed Cleaner result, and mutation aggregation waits for a safe wave boundary.
### Out of Scope (from spec)
- Sequential lifecycle — `yw-000033-010-domain-sequential-quality-gate`.
- Review evidence and final packaging — later tasks.

## Criticality
critical

## Dependencies
### Depends On
- `yw-000032-010-domain-plan-scaffold-quality-declaration`
- `yw-000032-020-domain-task-quality-gate-packet`
- `yw-000032-030-infra-quality-gate-workers`
### Depended By
- `yw-000034-010-infra-quality-gate-distribution-validation`

## Key Files
- `codex/skills/ywc-parallel-executor/SKILL.md`
- Parallel executor references/evals.

## Notes
Preserve existing rerouting, triage, worktree, and wave-delivery semantics for N/A/report-only paths.

## Hardening Evidence
### Test Feedback Path
- RED-first target: parallel executor evals for per-task Cleaner, wave Hardener, preservation, and precedence.
### Interface Contract
- Contract: task packet set → wave aggregate status/evidence
- Owner task: this task
- Canonical signature: eligible task packets + worker results → wave status with retained concerns
- Consumers: completion reporting and implementation review
- Implementation opacity: consumers trust sanitized wave evidence.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: manual full implementation review plus `ywc-impl-review`.
### Data Integrity Hardening
- Trigger surface: retryable parallel dispatch and shared wave state
- Atomic / locking strategy: isolated task worktrees plus wave-boundary aggregation
- Transaction boundary: each worker attempt and final wave aggregation
- Idempotency guard: task identity plus one Cleaner/conditional Hardener dispatch
- Required tests: preserved blocked worktree and concern precedence.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-parallel-executor/**`
### Shared Surfaces
- Wave status and completion evidence.
- `codex/skills/references/quality-gates.md`.
### Conflicts With
- `yw-000033-010-domain-sequential-quality-gate` — shared semantic contract only; separate files.
### Parallelizable After
- All Phase `yw-000032` tasks.
### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `rg -n "quality gate|Cleaner|Hardener|wave|BLOCKED|NEEDS_CONTEXT|DONE_WITH_CONCERNS|worktree" codex/skills/ywc-parallel-executor`

## Out of Scope
Sequential executor, worker TOML, implementation review, and generated package release.
