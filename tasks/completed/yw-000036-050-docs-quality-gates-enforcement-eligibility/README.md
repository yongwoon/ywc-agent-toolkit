# yw-000036-050-docs-quality-gates-enforcement-eligibility

## Purpose
Record the enforcement-eligibility rule — a delivery mode whose point-of-no-return precedes a gate may not declare `enforced` at that gate — in both roots' `quality-gates.md`, plus the `--per-task-pr` reporting-only channel note, so `yw-000036-030`/`yw-000036-040` can link it instead of restating it.

## Scope
- `claude-code/skills/references/quality-gates.md`: add the enforcement-eligibility rule in this file's own idiom (its severity vocabulary is `gate_state`, §9); add that under `--per-task-pr` the wave-boundary result is a plain descriptive note in the wave's Completion Report, never assigned to `gate_state`.
- `codex/skills/references/quality-gates.md`: add the same rule in this file's own idiom (its `report-only`/`advisory`/`enforced` three-tier model, §2); add that under `--per-task-pr` the wave-boundary result is never promoted into `contract_state`.
- No other file. Do not reconcile the two files' broader divergence (parent-spec open question, explicitly out of scope for this task).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#fr-8-enforcement-eligibility-rule-in-both-quality-gatesmd-files-and-the---per-task-pr-reporting-channel` — FR-8, including the corrected Iteration-3 wording naming each root's own field (`gate_state` vs. `contract_state`) rather than treating `gate_state` as shared vocabulary
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#acceptance-criteria` — AC10
- `claude-code/skills/references/quality-gates.md` §7 "Contract-Absent Fallback", §9 "gate_state Sentinel Vocabulary"
- `codex/skills/references/quality-gates.md` §2 "Contract states", §9 "No-contract path and downstream citation"
- `docs/ywc-plans/20260910-quality-gate-contract-port.md` (parent spec, FR-4) — `gate_state` never written to `.ywc-run-state.json` (not relevant to this file, which is prose-only, but the vocabulary discipline still applies: do not conflate `gate_state` and `contract_state` as one shared term)

### Summary
Both `quality-gates.md` files already have a place this rule slots into: claude-code's §9 severity vocabulary, codex's existing three-tier `report-only`/`advisory`/`enforced` model at §2. This task adds one rule to each, in each file's own words, and records that `--per-task-pr`'s wave-boundary cross-task check still runs (reporting only) but its result never becomes a `gate_state` value (claude-code) or a `contract_state` value (codex) — it's a plain note in the Completion Report only, per the spec's Option C decision (avoiding a synchronized new-sentinel change across two independently-maintained files).

### Out of Scope (from spec)
- Reconciling the codex three-tier model with claude-code's `gate_state` vocabulary more broadly — parent spec's still-open question, this task adds one rule to each in its own idiom and stops there.
- Any change to `ywc-parallel-executor/SKILL.md` in either root — those link this rule, they don't restate it (`yw-000036-030`, `yw-000036-040`).

## Criticality
`normal` — reference documentation only.

## Dependencies

### Depends On
- (None — this task has no code/schema dependency; it documents a standalone rule.)

### Depended By
- `yw-000036-030-domain-parallel-executor-hardener-isolation-claude` — links this file's rule via `> **Action required**: Read [...]` rather than restating it.
- `yw-000036-040-domain-parallel-executor-hardener-isolation-codex` — same, codex side.

## Key Files
- `claude-code/skills/references/quality-gates.md` — new rule paragraph, `--per-task-pr` note.
- `codex/skills/references/quality-gates.md` — new rule paragraph, `--per-task-pr` note.

## Notes
- Write the rule once per file, in that file's own words — do not copy-paste the same paragraph between the two files (Global Constraint: independently maintained, never a shared file).
- Name each root's own field explicitly (`gate_state` in claude-code, `contract_state` in codex) — never use `gate_state` as if it were shared vocabulary across both roots (Amendment Log Iteration 3, Critical #2).

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/references/quality-gates.md`
- `codex/skills/references/quality-gates.md`

### Owned Interface
- (None — no public interface owned.)

### Shared Surfaces
- (None identified — this task is the sole owner of both files for the duration of this batch.)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `grep -n "point-of-no-return" claude-code/skills/references/quality-gates.md` — confirm the rule appears.
- `grep -n "point-of-no-return" codex/skills/references/quality-gates.md` — confirm the rule appears.
- `grep -n "gate_state" claude-code/skills/references/quality-gates.md` and confirm the `--per-task-pr` note explicitly says the wave-boundary result is never assigned to it.
- `grep -n "contract_state" codex/skills/references/quality-gates.md` and confirm the equivalent note for that file's field.
- `bash scripts/validate.sh`

## Out of Scope
- Any change to either `ywc-parallel-executor/SKILL.md`.
- Merging or reconciling the two files' broader structural divergence.
