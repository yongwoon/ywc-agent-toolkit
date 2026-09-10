# yw-000036-060-docs-adr-hardener-isolation

## Purpose
Record the permanent `--per-task-pr` carve-out and the changed meaning of `wave-complete` as an ADR, per the architecture verdict's `ADR Recommendation: yes`, using the repository's own `ywc-adr` skill and path convention.

## Scope
- One new ADR under `docs/adr/NNNN-<slug>.md`, authored via `ywc-adr --mode new`.
- Covers: the permanent carve-out of `--per-task-pr` from `enforced` wave gating; the changed meaning of `wave-complete` (wave finished → wave promoted); the rejected Option B (retargeting per-task PR bases) and why; the consequence that a future reader must not "fix" the carve-out by making it uniform.
- No skill file is touched by this task.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#fr-10-adr-for-the-carve-out-and-the-changed-checkpoint-meaning` — FR-10, including the resolved path-convention decision (`docs/adr/NNNN-<slug>.md`, not `docs/architecture/adr/`)
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md#acceptance-criteria` — AC13
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.architecture-verdict.md` — full verdict; primary source for Context/Decision/Alternatives/Consequences content (trade-off table, `--per-task-pr` specifics, branch-lineage reasoning, the three advisor-considered options)
- `yw-000036-030-domain-parallel-executor-hardener-isolation-claude`, `yw-000036-040-domain-parallel-executor-hardener-isolation-codex` — the merged implementations this ADR must describe accurately (final branch-name form, promotion-step label)

### Summary
Neither `docs/adr/`, `docs/architecture/adr/`, nor `docs/architecture/` exists in this repository yet, so this task creates the directory. Two conventions collided in the spec's investigation (`ywc-plan`'s own Step 3.5 names `docs/architecture/adr/`, but the `ywc-adr` skill this repository distributes names `docs/adr/NNNN-<slug>.md`) — the spec resolved this in favor of the repo's own distributed skill: use `docs/adr/NNNN-<slug>.md` and dogfood `ywc-adr --mode new` rather than hand-writing the file. The ADR content is drawn from the architecture verdict (already adjudicated, not re-litigated here) plus the actual settled values from `yw-000036-030`/`yw-000036-040` (branch-name form, promotion-step label) so it reflects what shipped, not just what was proposed.

### Out of Scope (from spec)
- Any change to the skill files themselves — those are `yw-000036-030`/`yw-000036-040`, already merged by the time this task runs.
- Re-litigating the architecture verdict's decision — this task records it, it does not re-decide it.
- Retargeting `--per-task-pr` PR bases (rejected Option B) — recorded in the ADR as rejected, never implemented.

## Criticality
`normal` — documentation only.

## Dependencies

### Depends On
- `yw-000036-030-domain-parallel-executor-hardener-isolation-claude` — supplies the final branch-name/promotion-step-label decisions to record accurately.
- `yw-000036-040-domain-parallel-executor-hardener-isolation-codex` — confirms the same decisions held across both roots.

### Depended By
- (None identified)

## Key Files
- `docs/adr/NNNN-<slug>.md` (new, e.g. `docs/adr/0001-wave-hardener-delivery-isolation.md` — exact number determined by `ywc-adr --mode new` at generation time; check for any ADR created by unrelated work between now and execution).

## Notes
- Dogfood `ywc-adr --mode new` rather than hand-writing — this both follows the spec's resolved path decision and exercises the skill this repo distributes.
- The ADR must explicitly warn a future reader against "fixing" the carve-out into uniformity (Option B was rejected as unsound, not merely more expensive) — this is the single most important Consequences-section sentence per FR-10.

## Parallel Execution Metadata

### Ownership
- `docs/adr/` (new directory and file)

### Owned Interface
- (None — no public interface owned.)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000036-030-domain-parallel-executor-hardener-isolation-claude`
- `yw-000036-040-domain-parallel-executor-hardener-isolation-codex`

### Task Verify
- `test -d docs/adr` — directory exists.
- `ls docs/adr/*.md` — exactly one new file for this ADR (or check for a naming collision with unrelated concurrent ADR work first).
- `grep -l "per-task-pr" docs/adr/*.md` — confirm the carve-out is named.
- `grep -c "^## " docs/adr/<the-new-file>.md` — confirm Context/Decision/Alternatives/Consequences sections are present (exact heading style follows `ywc-adr`'s own template).
- `bash scripts/validate.sh`

## Out of Scope
- Any skill file change.
- Any other ADR beyond this one.
