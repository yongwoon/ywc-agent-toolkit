# yw-000002-020-consumer-legacy-compatibility

## Purpose
Align all Codex task consumers and task-generation documentation with prefixed IDs while preserving existing task references and directories.

## Scope
Update sequential/parallel executor parsing contracts, finish-branch and task-generator references/templates, examples, and compatibility eval expectations.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#acceptance-criteria` — AC3, AC6, and AC9
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#fr-4-preserve-numbering-and-dependency-semantics` — consumer compatibility

### Summary
Every consumer that selects, displays, references, or moves tasks must accept both prefixed and legacy forms. New examples and templates should teach the prefixed form, while existing task directories and dependency references remain unchanged. This task does not change the execution-order source of truth.

### Out of Scope (from spec)
- Core parser regex changes — handled by `yw-000001-030-parser-prefixed-task-ids`.
- Generated marketplace sync and final validation — handled by `yw-000003-010-eval-bundle-validation`.
- Claude Code consumers and task migration — excluded by the spec.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000001-030-parser-prefixed-task-ids` — supplies parser compatibility behavior.
- `yw-000002-010-task-generator-initials-allocation` — supplies finalized allocation behavior.

### Depended By
- `yw-000003-010-eval-bundle-validation` — validates the complete source and generated bundle.

## Key Files
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`
- `codex/skills/ywc-finish-branch/**`
- `codex/skills/ywc-task-generator/references/dependency-graph.md.template`
- `codex/skills/ywc-task-generator/references/execution-convention.md`
- Affected README/eval files

## Notes
Do not rename or migrate existing numeric/unprefixed task directories. Keep task IDs, paths, commands, and stable keys in English.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: executor contract evals and finish-branch parser fixtures.
- Named exception: documentation-heavy consumer alignment uses targeted contract scans where no executable fixture exists.

### Interface Contract
- Contract: accepted task-name/reference grammar for range selection, dependency graph, completion moves, and PR titles.
- Inputs: prefixed or legacy task names and ranges.
- Outputs: unchanged execution and completion semantics.
- Error model: existing invalid-range and missing-task errors.
- Impacted tests: executor and finish-branch evals.

### Critical Surface Review
- Review requirement: N/A — compatibility/documentation consumer updates.

### Data Integrity Hardening
- Trigger surface: N/A — no new writes or state transitions.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`
- `codex/skills/ywc-finish-branch/**`
- Shared task-generator references and examples

### Shared Surfaces
- Task ID grammar
- Dependency graph and range-selection contracts
- Completion move and PR title interfaces

### Conflicts With
- `yw-000001-030-parser-prefixed-task-ids` — shared compatibility fixtures and ID grammar.

### Parallelizable After
- `yw-000002-010-task-generator-initials-allocation`

### Task Verify
- Run sequential and parallel executor contract evals for prefixed and legacy ranges.
- Run finish-branch completion-move and PR-title compatibility checks.
- Scan updated templates/examples for prefixed output and preserved legacy references.

## Out of Scope
- Source parser implementation and generated marketplace files.
