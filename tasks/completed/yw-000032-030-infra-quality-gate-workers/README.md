# yw-000032-030-infra-quality-gate-workers

## Purpose
Add the two bounded write-enabled Codex workers and enforce their sandbox and edit-boundary contracts.

## Scope
Create Cleaner and Hardener TOML agents, update the Codex agent catalog, allow `workspace-write` only for these exact workers, and add agent/evaluator coverage for scope violations, unavailable tools, residuals, and no-delivery authority.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-3-two-bounded-write-agents`
- `codex/skills/references/quality-gates.md`
- `codex/agents/README.md`
### Summary
Cleaner may edit only task-owned production code for behavior-preserving complexity reduction. Hardener may edit only task-owned tests/fixtures for assertion hardening, with at most three approved attempts. Both agents must redact raw execution data and have no staging, commit, push, PR, merge, or delivery authority.
### Out of Scope (from spec)
- Executor dispatch and aggregation — `yw-000033-010` and `yw-000033-020`.
- Runtime CRAP or mutation tooling dependency in user projects.

## Criticality
critical

## Dependencies
### Depends On
- `yw-000031-010-docs-quality-gate-contract` — canonical worker contract.
### Depended By
- `yw-000033-010-domain-sequential-quality-gate` — dispatches Cleaner/Hardener.
- `yw-000033-020-domain-parallel-quality-gate` — dispatches Cleaner/Hardener.
- `yw-000034-010-infra-quality-gate-distribution-validation` — validates agent installation and catalog.

## Key Files
- `codex/agents/ywc-complexity-cleaner.toml`
- `codex/agents/ywc-test-hardener.toml`
- `codex/agents/README.md`
- `scripts/validate.sh`
- `tests/install-codex-agents-test.sh`
- Agent contract eval fixtures.

## Notes
The existing validator currently requires read-only for all agents; narrow the exception to the two exact filenames while retaining model and reasoning constraints.

## Hardening Evidence
### Test Feedback Path
- RED-first target: agent contract evals and `tests/install-codex-agents-test.sh`.
### Interface Contract
- Contract: bounded worker packet → sanitized terminal result
- Owner task: this task
- Canonical signature: packet with exact Ownership/IDs/digests → status, sanitized evidence, changed paths, residuals
- Consumers: sequential and parallel executors
- Implementation opacity: executors do not authorize edits beyond the packet.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: manual full implementation review plus `ywc-impl-review`.
### Data Integrity Hardening
- Trigger surface: shared mutable workspace edits
- Atomic / locking strategy: task-owned isolated worktree boundary
- Transaction boundary: one worker attempt, with no delivery operation
- Idempotency guard: attempt cap and no-delivery restriction
- Required tests: out-of-ownership edit, duplicate attempt, unavailable tool.

## Parallel Execution Metadata
### Ownership
- `codex/agents/ywc-complexity-cleaner.toml`
- `codex/agents/ywc-test-hardener.toml`
- `codex/agents/README.md`
- Agent validation/install/eval surfaces.
### Shared Surfaces
- `scripts/validate.sh` — global agent sandbox rule.
- `codex/agents/README.md` — catalog.
### Conflicts With
- (None identified)
### Parallelizable After
- `yw-000031-010-docs-quality-gate-contract`
### Task Verify
- `bash tests/install-codex-agents-test.sh`
- `bash scripts/validate.sh`

## Out of Scope
Executor routing, mutation/complexity tool implementation, generated package sync, and Claude Code agents.
