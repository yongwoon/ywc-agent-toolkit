# yw-000035-070-domain-parallel-executor-quality-gate

## Purpose
Insert bounded per-task Cleaner and wave-boundary Hardener gates into the claude-code parallel executor, and extend its Category → `subagent_type` table with Cleaner/Hardener columns.

## Scope
Insert `**4c.5. Cleaner (CRAP gate, per-task)**` after existing 4c content, before 4d; insert `**4e.5. Hardener (Mutation gate, wave boundary)**` after existing 4e content, before 4g; extend the Step 3 Category table with `Cleaner` and `Hardener` columns. All in `claude-code/skills/ywc-parallel-executor/SKILL.md` only.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-4-ywc-parallel-executor--step-4c5-cleaner-per-task--step-4e5-hardener-wave-boundary` — FR-4 (claude-code half only; codex half already delivered by `yw-000033-020-domain-parallel-quality-gate`)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC4, AC5, AC11
- `claude-code/skills/references/quality-gates.md` (created by `yw-000035-010`) — canonical thresholds/vocabulary

### Summary
4c.5 runs per-task (fast, parallel-safe), dispatching to `ywc-refactor-cleaner`; 4e.5 runs once against the wave's merged diff (cross-task interaction gaps only surface post-merge), dispatching to `ywc-qa-engineer`. Both follow the dispatch-failure → `DONE_WITH_CONCERNS`-never-`BLOCKED` rule from FR-3. 4c.5 records `gate_state` in the per-task subagent return payload; 4e.5 records it in the wave-level Completion Report — never in `.ywc-run-state.json`. The Category table (5 rows, verified) gains Cleaner/Hardener columns pointing to `ywc-refactor-cleaner`/`ywc-qa-engineer` for every code-producing category row, matching FR-3's agent reuse (no new agents). Both steps link `quality-gates.md`, never restate thresholds, and state the contract-absent fallback per AC11.

**Implementation note carried forward**: unlike `yw-000035-060` (which creates a dedicated `quality-gate-steps.md`), this task inlines its procedure directly in `SKILL.md` at 4c.5/4e.5 with pointers to `quality-gates.md`, rather than depending on `yw-000035-060`'s new reference file — the two tasks have no dependency edge between them (both depend only on `yw-000035-010`) and must remain independently completable in any order.

### Out of Scope (from spec)
- The codex parallel-executor gate — already delivered by `yw-000033-020-domain-parallel-quality-gate`.
- `ywc-sequential-executor` and `ywc-impl-review` insertions — `yw-000035-060` and `yw-000035-080`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000035-010-docs-quality-gate-contract-claude` — provides `claude-code/skills/references/quality-gates.md`, which 4c.5/4e.5 link.

### Depended By
- (None identified)

## Key Files
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — insert two new bolded step subsections plus two new table columns.

## Notes
Does not depend on `yw-000035-060` — the two dependent tasks are siblings under `yw-000035-010`, not chained to each other, so they can run in parallel worktrees.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-parallel-executor/SKILL.md`

### Owned Interface
(None — no public interface owned.)

### Shared Surfaces
- `claude-code/skills/references/quality-gates.md` — read-only reference; not modified by this task.

### Conflicts With
- (None identified — `yw-000035-060` and `yw-000035-080` edit different skill directories)

### Parallelizable After
- `yw-000035-010-docs-quality-gate-contract-claude`

### Task Verify
- `grep -n "^\*\*4c\.\|^\*\*4c\.5\.\|^\*\*4d\.\|^\*\*4e\.\|^\*\*4e\.5\.\|^\*\*4g\." claude-code/skills/ywc-parallel-executor/SKILL.md` — confirm ascending line-number order
- `grep -n "^| Category" claude-code/skills/ywc-parallel-executor/SKILL.md` then confirm the table header row includes `Cleaner` and `Hardener`
- `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-parallel-executor/SKILL.md`
- `bash scripts/validate.sh`

## Out of Scope
- Any codex-side parallel-executor change.
- Creating a new agent file or a new reference file (procedure is inlined in SKILL.md).
