# yw-000035-060-domain-sequential-executor-quality-gate

## Purpose
Insert the opt-in Cleaner (CRAP gate) and Hardener (Mutation gate) steps into the claude-code sequential executor, dispatching to the pre-existing `ywc-refactor-cleaner` / `ywc-qa-engineer` agents, between the existing Implementation and Task Verification steps.

## Scope
Insert `### Step 3.5: Cleaner (CRAP gate)` and `### Step 3.6: Hardener (Mutation gate)` into `claude-code/skills/ywc-sequential-executor/SKILL.md` between the existing `### Step 3: Implementation` and `### Step 4: Task Verification`. Create `claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md` with the full dispatch procedure.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-3-ywc-sequential-executor--step-35-cleaner--step-36-hardener` — FR-3 (claude-code half only; codex half already delivered by `yw-000033-010-domain-sequential-quality-gate`)
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC3, AC11
- `claude-code/skills/references/quality-gates.md` (created by `yw-000035-010`) — canonical thresholds/vocabulary this task links, never restates

### Summary
Each subsection dispatches to the pre-existing agent as a separate Task-tool invocation from the Step 3 implementer — never self-approved. Both point to the new `quality-gate-steps.md` for the full procedure: Cleaner runs first; Hardener runs only if Cleaner does not block; Hardener is capped at 3 rounds; a dispatch failure routes to `DONE_WITH_CONCERNS`, never `BLOCKED`; unresolved Mutation survivors after the cap forward unchanged to Step 4.5 (Implementation Review). Both steps state the `N/A — no quality gate contract` skip behavior per AC11.

### Out of Scope (from spec)
- The codex sequential-executor gate — already delivered by `yw-000033-010-domain-sequential-quality-gate`.
- `ywc-parallel-executor` and `ywc-impl-review` insertions — `yw-000035-070` and `yw-000035-080`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000035-010-docs-quality-gate-contract-claude` — provides `claude-code/skills/references/quality-gates.md`, which the new Step 3.5/3.6 and `quality-gate-steps.md` link via `> **Action required**: Read [...]`. Landing this task before `yw-000035-010` merges would leave a dangling reference (per the spec's own Edge Cases ordering rule).

### Depended By
- (None identified)

## Key Files
- `claude-code/skills/ywc-sequential-executor/SKILL.md` — insert two new `###` step subsections.
- `claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md` — new reference file (create).

## Notes
No new claude-code agent file is created (AC6) — this task only adds dispatch instructions targeting the two pre-existing agents by name.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-sequential-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`

### Owned Interface
(None — no public interface owned; this is a skill prompt and its reference doc, not a code module with a signature other tasks call.)

### Shared Surfaces
- `claude-code/skills/references/quality-gates.md` — read-only reference; this task does not modify it, only links it.

### Conflicts With
- (None identified — `yw-000035-070` and `yw-000035-080` edit different skill directories)

### Parallelizable After
- `yw-000035-010-docs-quality-gate-contract-claude`

### Task Verify
- `grep -n "^### Step 3: Implementation\|^### Step 3.5: Cleaner\|^### Step 3.6: Hardener\|^### Step 4: Task Verification" claude-code/skills/ywc-sequential-executor/SKILL.md` — confirm line-number order matches heading order above.
- `test -f claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`
- `grep -q "Action required" claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`
- `grep -q "Rationalization Defense" claude-code/skills/ywc-sequential-executor/references/quality-gate-steps.md`
- `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-sequential-executor/SKILL.md`
- `bash scripts/validate.sh`

## Out of Scope
- Any codex-side sequential-executor change.
- Creating a new agent file.
