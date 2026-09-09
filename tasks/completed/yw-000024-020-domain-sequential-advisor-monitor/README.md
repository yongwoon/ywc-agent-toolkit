# yw-000024-020-domain-sequential-advisor-monitor

## Purpose
Add bounded monitoring and honest unavailable fallbacks for sequential advisor calls without changing advisor budgets or task lifecycle ownership.

## Scope
Update the sequential executor and its advisor evals for 300-second monitoring, successful-dispatch-only monitoring, and condition-specific evidence-based fallback.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#functional-requirements` — FR-1 and FR-3
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#acceptance-criteria` — AC4

### Summary
Successful advisor spawns use the shared monitoring contract and a bounded 300-second sequence. The existing three-call budget, delivery ownership, and stop rules remain authoritative; unavailable advisors follow the named fallback for spec conflict, ambiguous verification failure, borderline stop condition, or Pattern C plan review, without auto-redispatch.

### Out of Scope (from spec)
- Shared monitoring reference — handled by `yw-000023-010-docs-subagent-async-monitoring-contract`
- Parallel worker monitoring — handled by `yw-000024-010-domain-parallel-monitor-gate`
- Review-worker output — handled by `yw-000024-030-domain-review-monitor-output`
- Generated package sync — handled by `yw-000025-010-infra-codex-package-validation`

## Criticality
critical

## Dependencies

### Depends On
- `yw-000023-010-docs-subagent-async-monitoring-contract` — provides bounded advisor monitoring and quiescence rules

### Depended By
- `yw-000025-010-infra-codex-package-validation` — validates source and package parity

## Key Files
- `codex/skills/ywc-sequential-executor/SKILL.md` — advisor monitoring reference and fallback table
- `codex/skills/ywc-sequential-executor/evals/evals.json` — advisor unavailable scenario

## Notes
- Monitoring does not create a fourth advisor call or alter task-state/worktree lifecycle.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `codex/skills/ywc-sequential-executor/evals/evals.json` and `codex/skills/ywc-sequential-executor/scripts/test-transition-safety.py`
- RED-first target: add advisor-unavailable fallback eval coverage before finalizing the executor reference.

### Interface Contract
- Contract: advisor monitor/fallback handoff
- Owner task: `yw-000024-020-domain-sequential-advisor-monitor`
- Canonical signature: successful advisor target + condition + evidence → named unavailable fallback or attributable terminal result
- Consumers: sequential executor delivery and stop-rule paths
- Implementation opacity: consumers preserve the existing budget and do not redispatch based on internal monitoring details
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: advisor target, elapsed time, terminal evidence, condition category
- Outputs: advisor result or owner-specific fallback
- Error model: unavailable is non-terminal until bounded/quiescent; no auto-redispatch
- Impacted tests: `bash scripts/run-codex-skill-contract-evals.sh`

### Critical Surface Review
- Review requirement: `ywc-impl-review`

### Data Integrity Hardening
- Trigger surface: retryable collaboration calls and advisor budget state
- Atomic / locking strategy: equivalent serialized guard — consume one existing slot and one bounded escalation per target
- Transaction boundary: advisor dispatch through fallback decision; no task-state mutation
- Idempotency guard: existing three-call budget plus one monitor request/interrupt bound
- Required tests: advisor unavailable fallback and no-fourth-call scenario

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/evals/evals.json`

### Shared Surfaces
- `codex/skills/references/subagent-async-monitoring.md` — read-only dependency
- `codex/skills/ywc-sequential-executor/references/advisor-escalation.md` — existing budget and fallback semantics

### Conflicts With
- `yw-000024-010-domain-parallel-monitor-gate` and `yw-000024-030-domain-review-monitor-output` only if they attempt to modify the shared reference

### Parallelizable After
- `yw-000023-010-docs-subagent-async-monitoring-contract`

### Task Verify
- `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-sequential-executor/evals/evals.json", "utf8"))'`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
- Changing the advisor budget, delivery owner, task state, worktrees, or branch lifecycle.
