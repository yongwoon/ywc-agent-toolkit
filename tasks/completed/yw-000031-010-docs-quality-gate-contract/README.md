# yw-000031-010-docs-quality-gate-contract

## Purpose
Create the canonical Codex Quality Gate Contract reference used by every producer, worker, executor, and reviewer.

## Scope
Define contract states, bounded packet fields, evidence redaction, dispatch eligibility, thresholds, retry caps, gate ordering, and status precedence. Register the shared reference wherever repository guidance requires shared Codex references.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#quality-gate-contract`
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-1-shared-contract-and-planning-declaration`
### Summary
The reference is the single source of truth for opt-in quality-gate semantics. It must preserve the exact no-contract sentinel and must never authorize raw executable commands, raw output, or delivery actions. Downstream tasks cite this contract rather than copying divergent state tables.
### Out of Scope (from spec)
- Planner, scaffold, task-generator, agent, executor, review, and packaging edits — handled by later tasks in this batch.
- Claude Code changes and runtime tooling dependencies — excluded by the spec.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)
### Depended By
- `yw-000032-010-domain-plan-scaffold-quality-declaration` — consumes canonical declaration rules.
- `yw-000032-020-domain-task-quality-gate-packet` — consumes packet and redaction rules.
- `yw-000032-030-infra-quality-gate-workers` — consumes worker boundaries and terminal rules.
- `yw-000033-010-domain-sequential-quality-gate` — consumes routing and aggregation rules.
- `yw-000033-020-domain-parallel-quality-gate` — consumes routing and aggregation rules.
- `yw-000033-030-domain-review-quality-evidence` — consumes evidence-boundary rules.

## Key Files
- `codex/skills/references/quality-gates.md` — canonical contract reference.

## Notes
No database migration, library introduction, or external API is involved. The reference must make `N/A — no quality gate contract` a valid compatibility state.

## Hardening Evidence
### Test Feedback Path
- `(N/A — docs-only contract reference; verify with targeted searches and downstream contract evals.)`
### Interface Contract
- Contract: Quality Gate Contract packet and status precedence
- Owner task: `yw-000031-010-docs-quality-gate-contract`
- Canonical signature: bounded metadata packet → Cleaner/Hardener/executor/reviewer decisions
- Consumers: Phase `yw-000032` and `yw-000033` tasks
- Implementation opacity: consumers trust the reference fields and do not invent alternate states
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: `ywc-impl-review` via the final validation task
### Data Integrity Hardening
- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `codex/skills/references/quality-gates.md`
### Shared Surfaces
- `codex/skills/references/quality-gates.md` — downstream consumers cite this file.
### Conflicts With
- (None identified — downstream tasks depend on this task.)
### Parallelizable After
- (Root task — no predecessor required)
### Task Verify
- `rg -n "report-only|advisory|enforced|NEEDS_CONTEXT|N/A — no quality gate contract|DONE_WITH_CONCERNS|BLOCKED" codex/skills/references/quality-gates.md`

## Out of Scope
All consumer implementation, worker TOML, generated package, and eval changes.
