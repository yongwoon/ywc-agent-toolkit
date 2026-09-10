# yw-000033-010-domain-sequential-quality-gate

## Purpose
Insert the opt-in Cleaner → Hardener gate into the sequential executor while preserving the existing no-contract lifecycle.

## Scope
Resolve the task packet after normal verification, dispatch only eligible workers, aggregate terminal states with canonical precedence, retain sanitized evidence/residuals, and place the gate before optional review/delivery.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-4-sequential-executor-gate`
- `codex/skills/references/quality-gates.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
### Summary
The sequential executor runs quality gates only for a valid eligible packet. Cleaner precedes Hardener, Hardener is skipped after a disallowed Cleaner result, and a later DONE cannot erase an earlier concern. N/A and report-only retain the current path.
### Out of Scope (from spec)
- Parallel wave lifecycle — `yw-000033-020-domain-parallel-quality-gate`.
- Review evidence consumption — `yw-000033-030-domain-review-quality-evidence`.

## Criticality
critical

## Dependencies
### Depends On
- `yw-000032-010-domain-plan-scaffold-quality-declaration`
- `yw-000032-020-domain-task-quality-gate-packet`
- `yw-000032-030-infra-quality-gate-workers`
### Depended By
- `yw-000034-010-infra-quality-gate-distribution-validation` — final eval and validation gate.

## Key Files
- `codex/skills/ywc-sequential-executor/SKILL.md`
- Sequential executor references/evals.

## Notes
Do not execute raw project commands from the packet; use immutable approved identities/digests and sanitized evidence paths only.

## Hardening Evidence
### Test Feedback Path
- RED-first target: sequential executor contract evals for no-contract, concern precedence, missing packet, and blocked enforced gate.
### Interface Contract
- Contract: task packet → sequential completion status/evidence
- Owner task: this task
- Canonical signature: valid packet + normal verification → aggregate status and sanitized evidence
- Consumers: implementation review and completion reporting
- Implementation opacity: consumers rely on the aggregate and do not re-run the gate.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: manual full implementation review plus `ywc-impl-review`.
### Data Integrity Hardening
- Trigger surface: retryable worker dispatch and duplicate-sensitive completion status
- Atomic / locking strategy: single sequential lifecycle and immutable packet binding
- Transaction boundary: gate stage before review/delivery
- Idempotency guard: one Cleaner then conditional Hardener per task
- Required tests: duplicate dispatch prevention and earlier-concern retention.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-sequential-executor/**`
### Shared Surfaces
- Completion Report status/evidence contract.
- `codex/skills/references/quality-gates.md`.
### Conflicts With
- `yw-000033-020-domain-parallel-quality-gate` — shared semantic contract only; do not edit the same files.
### Parallelizable After
- All Phase `yw-000032` tasks.
### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `rg -n "quality gate|Cleaner|Hardener|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED|Completion Report" codex/skills/ywc-sequential-executor`

## Out of Scope
Parallel execution, worker TOML definitions, implementation-review rules, and package sync.
