# yw-000035-090-domain-quality-gate-codex-gaps

## Purpose
Close two codex-side completeness gaps discovered while generating the `yw-000035` claude-code batch: two headings that the prior codex-only `yw-000032-010` and `yw-000032-020` tasks were expected to add (per their own Scope text) are, on inspection, still missing from the codex files they were supposed to touch. This task finishes that codex-side work so the port spec's AC2.5 (both roots) and AC9 (both roots) are actually satisfied, not just assumed satisfied.

## Scope
- Add `## Quality Gate Contract` and `## Module Boundaries` sections to `codex/skills/ywc-plan/references/spec-template.md`, positioned after the file's `## Existing Constraints Touched`-equivalent heading and before its `## Acceptance Criteria`-equivalent heading (mirror the claude-code placement done in `yw-000035-020`, adapted to this file's own heading sequence and language idiom — Korean prose where the codex file body is already Korean, per `claude-code/skills/CLAUDE.md` §"Codex-skill: Maintained Independently").
- Add a `### Owned Interface` subsection immediately after `### Ownership` in `codex/skills/ywc-task-generator/references/README.md.template`, matching the field order and wording intent of the claude-code version added in `yw-000035-040`, in the codex template's own idiom.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-2-ywc-plan-spec-templatemd--author-net-new-quality-gate-contract--module-boundaries-sections` — FR-2 (codex half)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-7-ywc-task-generator-readme-template--owned-interface-field` — FR-7 (codex half)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC2.5, AC9, AC11
- `tasks/yw-000032-010-domain-plan-scaffold-quality-declaration/README.md` — the prior task whose Key Files listed `codex/skills/ywc-plan/references/spec-template.md` but whose delivered content, verified by direct grep during `yw-000035` generation, does not contain the two target headings
- `tasks/yw-000032-020-domain-task-quality-gate-packet/README.md` — the prior task whose Key Files listed `codex/skills/ywc-task-generator/references/README.md.template` but whose delivered content does not contain an `Owned Interface` heading

### Summary
The `yw-000032-010`/`yw-000032-020` codex batch's own Key Files sections named these two files as edit targets, but a direct read of the current file contents (performed while generating `yw-000035`) shows the specific headings this spec's AC2.5 and AC9 require are absent. This is either because those tasks have not been executed yet, or were executed with narrower scope than their README implied — this task does not need to resolve which; it only needs to leave both files in the state the port spec's acceptance criteria require. If `yw-000032-010`/`yw-000032-020` are executed first and happen to add these headings as part of their own work, this task becomes a no-op verification rather than a fresh edit — re-check current file state before editing.

### Out of Scope (from spec)
- The claude-code-side equivalents of both headings — already handled by `yw-000035-020` (spec-template) and `yw-000035-040` (Owned Interface).
- Any other content inside `codex/skills/ywc-plan/references/spec-template.md` or `codex/skills/ywc-task-generator/references/README.md.template` beyond the two named headings.
- Re-running or re-scoping `yw-000032-010`/`yw-000032-020` themselves.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000032-010-domain-plan-scaffold-quality-declaration` — establishes the codex `ywc-plan` quality-gate declaration surface this task's `## Quality Gate Contract` / `## Module Boundaries` sections sit alongside.
- `yw-000032-020-domain-task-quality-gate-packet` — establishes the codex `ywc-task-generator` quality-gate packet surface this task's `### Owned Interface` section sits alongside.

### Depended By
- (None — this is a completeness fix with no further downstream consumer inside this port)

## Key Files
- `codex/skills/ywc-plan/references/spec-template.md` — add two headings.
- `codex/skills/ywc-task-generator/references/README.md.template` — add one heading.

## Notes
Both gaps were discovered, not invented — this task exists because a direct grep during `yw-000035` task generation showed the headings absent, contradicting what the prior tasks' Scope text implied. Before editing, re-run the same grep to confirm the gap still exists (the prior tasks may have since been executed and could have already closed it), and treat a clean grep as "already satisfied, task is a no-op verification" rather than forcing a duplicate edit.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-plan/references/spec-template.md`
- `codex/skills/ywc-task-generator/references/README.md.template`

### Owned Interface
(None — no public interface owned; these are documentation/template sections, not a code module with a signature other tasks call.)

### Shared Surfaces
- (None identified — these two files are not concurrently edited by any other task in this batch; `yw-000032-010`/`yw-000032-020` own the surrounding files but this task's Ownership is scoped to the two specific headings only.)

### Conflicts With
- `yw-000032-010-domain-plan-scaffold-quality-declaration` — do not run in parallel; if that task is executed concurrently it may also touch `codex/skills/ywc-plan/references/spec-template.md`.
- `yw-000032-020-domain-task-quality-gate-packet` — do not run in parallel; same reasoning for `codex/skills/ywc-task-generator/references/README.md.template`.

### Parallelizable After
- `yw-000032-010-domain-plan-scaffold-quality-declaration`
- `yw-000032-020-domain-task-quality-gate-packet`

### Task Verify
- `grep -q "Quality Gate Contract" codex/skills/ywc-plan/references/spec-template.md`
- `grep -q "Module Boundaries" codex/skills/ywc-plan/references/spec-template.md`
- `grep -q "Owned Interface" codex/skills/ywc-task-generator/references/README.md.template`
- `bash scripts/validate.sh`

## Out of Scope
- Any change to the claude-code-side spec-template.md or README.md.template (already done in `yw-000035-020` / `yw-000035-040`).
- Re-verifying or re-scoping any other Key File listed by `yw-000032-010` / `yw-000032-020`.
