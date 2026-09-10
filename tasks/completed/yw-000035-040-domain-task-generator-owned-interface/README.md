# yw-000035-040-domain-task-generator-owned-interface

## Purpose
Give the claude-code task-generator's README template an `Owned Interface` field distinct from the broader `Ownership` field, so generated tasks can declare the specific public interface other tasks may trust without reading the implementation.

## Scope
Insert a `### Owned Interface` subsection immediately after `### Ownership` in `claude-code/skills/ywc-task-generator/references/README.md.template` only.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-7-ywc-task-generator-readme-template--owned-interface-field` — FR-7 (claude-code half only)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC9

### Summary
Wording per spec: "Public interface this task confirms and owns; other tasks trust this signature and do not read the implementation," with a `(None — no public interface owned)` sentinel and an explanatory `<!-- NOTE: ... -->` comment (matching the template's existing NOTE-comment style) distinguishing it from the broader `Ownership` field.

**Unverified assumption carried into this task**: re-verification during investigation found `codex/skills/ywc-task-generator/references/README.md.template` has `### Ownership` and `### Shared Surfaces` but **no** `Owned Interface` heading either — the codex half of FR-7 also appears incomplete, despite the prior `yw-000032-020-domain-task-quality-gate-packet` task's Scope mentioning a "conditional Quality Gate Contract/Owned Interface section." This task does not fix the codex side (out of Ownership) — flag as a residual gap.

### Out of Scope (from spec)
- `codex/skills/ywc-task-generator/references/README.md.template` — belongs to the (apparently still-incomplete) codex batch.
- `## Criticality` section gap in this same template — explicitly Out of Scope per the port spec (unrelated pre-existing gap).

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- (None identified)

## Key Files
- `claude-code/skills/ywc-task-generator/references/README.md.template` — insert one new `###` subsection.

## Notes
`claude-code/skills/ywc-task-generator/references/dependency-graph.md.template` was checked and contains no Ownership/Owned Interface references — no change needed there.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-task-generator/references/README.md.template`

### Owned Interface
(None — no public interface owned; this task edits a documentation template, not a code module.)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `grep -n "^### Owned Interface" claude-code/skills/ywc-task-generator/references/README.md.template`
- Line-number check: `### Owned Interface` immediately follows `### Ownership` and precedes `### Shared Surfaces`.
- `grep -q "None — no public interface owned" claude-code/skills/ywc-task-generator/references/README.md.template`
- `bash scripts/validate.sh`

## Out of Scope
- `codex/skills/ywc-task-generator/references/README.md.template`.
- `## Criticality` section addition (unrelated, pre-existing gap, explicitly out of scope per the port spec).
