# yw-000035-050-refactor-cleaner-boundary-note

## Purpose
Keep `ywc-refactor-cleaner`'s written Boundaries contract in sync with the new CRAP-gate dispatch responsibility it will receive from `yw-000035-060` and `yw-000035-070`, without expanding its deletion authority.

## Scope
Add exactly one sentence to `claude-code/agents/ywc-refactor-cleaner.md`'s `## Boundaries` section. No other file changes.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-8-claude-code-cleanerhardener-dispatch--reuse-existing-agents-no-new-files` — FR-8, Correction (iteration 1)

### Summary
`ywc-refactor-cleaner.md`'s Boundaries currently read "SAFE-tier dead-code deletion only." The CRAP gate's read-only complexity measurement is a distinct activity outside that written scope. Add exactly one sentence: "May also perform read-only complexity measurement (e.g. CRAP-gate greps via Bash) and report findings; deletion authority remains SAFE-tier only." `ywc-qa-engineer.md` is explicitly **not** modified — Mutation-gate work is ordinary test authoring already inside its existing Boundaries. No new claude-code agent file is created (AC6).

**Spec gap for user awareness**: this FR has no dedicated Acceptance Criterion in the port spec (AC1–AC11 cover FR-1 through FR-7 and FR-9/FR-10, but no AC explicitly verifies the `ywc-refactor-cleaner.md` Boundaries sentence). This was not treated as a no-AC speculative requirement to route to Open Questions — the spec author's own iteration-1 Amendment Log entry gives a specific, well-justified rationale (Opus advisor verdict that CRAP-gate measurement is genuinely outside the persona's written scope), so it is implemented normally. Flagging the missing AC as a residual spec-completeness gap, not a task-generator omission.

### Out of Scope (from spec)
- `claude-code/agents/ywc-qa-engineer.md` — explicitly unmodified per FR-8.
- Any new claude-code agent file — AC6 requires zero new files.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- (None identified — `yw-000035-060`/`yw-000035-070` dispatch to the pre-existing agent by name; they do not read this file's content, only its file path)

## Key Files
- `claude-code/agents/ywc-refactor-cleaner.md` — one sentence added to `## Boundaries`.

## Notes
This is the narrowest possible change: one sentence, one file. Do not touch Mission, Success Criteria, or Return Contract sections.

## Parallel Execution Metadata

### Ownership
- `claude-code/agents/ywc-refactor-cleaner.md`

### Owned Interface
(None — no public interface owned; this is a persona/prompt file, not a code module.)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `grep -q "May also perform read-only complexity measurement" claude-code/agents/ywc-refactor-cleaner.md`
- `grep -c "^## " claude-code/agents/ywc-refactor-cleaner.md` unchanged from pre-task count (no section added/removed, only a sentence within `## Boundaries`)
- `! git diff --name-only | grep -q "ywc-qa-engineer.md"` (confirm this file was not touched)
- `bash scripts/validate.sh`

## Out of Scope
- Any Mission, Success Criteria, or Return Contract change in `ywc-refactor-cleaner.md`.
- `ywc-qa-engineer.md`.
