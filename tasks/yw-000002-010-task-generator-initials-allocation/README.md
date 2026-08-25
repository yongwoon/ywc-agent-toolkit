# yw-000002-010-task-generator-initials-allocation

## Purpose
Make new task generation collision-resistant across linked worktrees by resolving collaborator initials and atomically reserving initials-scoped PHASEs.

## Scope
Update the task-generator contract and references for explicit/configured/interactive initials resolution, linked-worktree scanning, scoped numbering, shared Git reservation refs, and deterministic conflict handling.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#acceptance-criteria` — naming, scanning, and reservation requirements
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#fr-2-derive-initials-safely` — resolution behavior
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#fr-3-allocate-initials-scoped-phases` — allocation behavior

### Summary
The generator must resolve a validated initials namespace before touching task artifacts. Prefixed IDs are scoped to that namespace while legacy IDs remain readable but do not advance it. Candidate PHASEs must include the resolved graph, active/completed tasks, and corresponding task paths in linked worktrees, then use an atomic common-Git reservation before writing directories.

### Out of Scope (from spec)
- Config writer implementation — handled by `yw-000001-010-config-initials-writer`.
- Parser/consumer updates — handled by Phase `yw-000002` tasks.
- Remote coordination across separate clones and task migration — excluded by the spec.

## Criticality
critical

## Dependencies
### Depends On
- `yw-000001-010-config-initials-writer` — provides the persisted config writer and validation contract.
- `yw-000001-030-parser-prefixed-task-ids` — makes emitted prefixed IDs readable by core parsers.

### Depended By
- `yw-000002-020-consumer-legacy-compatibility` — consumes generator/reference semantics.

## Key Files
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/collaborator-initials.md`
- `codex/skills/ywc-task-generator/references/*.md` where naming/allocation examples change
- `tasks/dependency-graph.md`

## Notes
Use the repository common Git directory for reservations so linked worktrees share the ledger. Reservations remain consumed after crashes; bounded retry failures must not create task directories.

## Hardening Evidence
### Test Feedback Path
- RED-first target: generator contract fixtures for missing initials, scoped scans, linked worktrees, and reservation races.

### Interface Contract
- Contract: generator input resolution and task ID output.
- Inputs: explicit initials or project/user config; repository-relative tasks directory.
- Outputs: validated initials, prefixed task IDs, or `NEEDS_CONTEXT` before artifact writes.
- Error model: invalid initials, unsafe task path, inaccessible source, and bounded reservation conflict.
- Impacted tests: task-generator evals and linked-worktree/concurrency fixtures.

### Critical Surface Review
- Review requirement: `ywc-impl-review` for duplicate-sensitive allocation.

### Data Integrity Hardening
- Trigger surface: duplicate-sensitive side effect and shared mutable Git metadata.
- Atomic / locking strategy: common-Git exclusive generator lock plus compare-and-create reservation ref.
- Transaction boundary: scan, reserve candidate, then create the complete task batch and graph update.
- Idempotency guard: durable reservation ref consumes each initials/PHASE once.
- Required tests: concurrent same-initials generators, retry collision, crash-after-reservation behavior.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-task-generator/**`
- Generator allocation contract and task ID naming rules

### Shared Surfaces
- `tasks/dependency-graph.md`
- `.codex/ywc.json` resolution contract
- Common Git reservation refs

### Conflicts With
- `yw-000001-030-parser-prefixed-task-ids` and `yw-000002-020-consumer-legacy-compatibility` — both update task ID consumer semantics.

### Parallelizable After
- `yw-000001-010-config-initials-writer`
- `yw-000001-030-parser-prefixed-task-ids`

### Task Verify
- Run task-generator contract fixtures for explicit/configured/missing initials.
- Run linked-worktree and concurrent reservation fixtures in temporary repositories.
- Confirm legacy task IDs remain readable and no task artifacts are written on `NEEDS_CONTEXT`.

## Out of Scope
- Parser implementation and generated marketplace synchronization.
