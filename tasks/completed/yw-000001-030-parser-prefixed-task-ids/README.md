# yw-000001-030-parser-prefixed-task-ids

## Purpose
Extend machine parsers to consume initials-prefixed task IDs without weakening legacy parsing or completion detection.

## Scope
Update the dependency-graph compactor, PR-title parser, and focused parser fixtures for prefixed full/short IDs and legacy compatibility.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#acceptance-criteria` — AC6 and AC7
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#fr-5-extend-machine-parsers-without-weakening-completion-logic` — parser requirements

### Summary
The compactor and PR-title builder must recognize the new initials-prefixed grammar while retaining numeric and unprefixed formats. Completion remains an exact `— done` suffix match; headings such as `— Done prerequisites` must not compact.

### Out of Scope (from spec)
- Generator allocation — handled by `yw-000002-010-task-generator-initials-allocation`.
- Executor and documentation consumers — handled by `yw-000002-020-consumer-legacy-compatibility`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000001-010-config-initials-writer` — establishes the preceding foundation phase.

### Depended By
- `yw-000002-010-task-generator-initials-allocation` — depends on parsers accepting emitted IDs.
- `yw-000002-020-consumer-legacy-compatibility` — uses parser-compatible IDs in executor and finish-branch contracts.
- `yw-000003-010-eval-bundle-validation` — validates final parser and bundle parity.

## Key Files
- `codex/skills/ywc-task-generator/scripts/compact-dependency-graph.py`
- `codex/skills/ywc-finish-branch/scripts/build-pr-title.py`
- Focused parser fixtures/evals

## Notes
Preserve existing parser fallbacks and output interface, including `TASK_NUMBER`/`SLUG_EN` behavior.

## Hardening Evidence
### Test Feedback Path
- RED-first target: compactor and PR-title parser fixtures for prefixed and legacy IDs.

### Interface Contract
- Contract: parser inputs and `build-pr-title.py` output fields.
- Inputs: prefixed, unprefixed, legacy full/short task names.
- Outputs: same compaction decisions and `TASK_NUMBER`/`SLUG_EN` fields.
- Error model: existing fallback behavior preserved.
- Impacted tests: focused Python fixtures.

### Critical Surface Review
- Review requirement: N/A — parser-only compatibility change.

### Data Integrity Hardening
- Trigger surface: N/A — read-only parser behavior.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A — parser fixtures cover behavior.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-task-generator/scripts/compact-dependency-graph.py`
- `codex/skills/ywc-finish-branch/scripts/build-pr-title.py`
- Focused parser fixtures

### Shared Surfaces
- Task ID grammar
- Dependency graph completion markers
- PR title parser output fields

### Conflicts With
- `yw-000002-020-consumer-legacy-compatibility` — shared task ID compatibility documentation and fixtures.

### Parallelizable After
- `yw-000001-010-config-initials-writer`

### Task Verify
- Run compactor fixtures for prefixed/legacy full and short IDs.
- Run the exact `— Done prerequisites` regression fixture.
- Run PR-title parser fixtures and compare output fields with legacy cases.

## Out of Scope
- Task directory generation and executor scheduling changes.
