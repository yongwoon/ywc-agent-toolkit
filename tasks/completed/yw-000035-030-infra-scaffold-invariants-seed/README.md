# yw-000035-030-infra-scaffold-invariants-seed

## Purpose
Give the codex `ywc-project-scaffold` skill an optional step to draft an advisory Architecture Invariants manifest from the layer structure it just proposed, reusing the already-implemented codex `ywc-architecture-invariants --mode draft` interface.

## Scope
Add a new "6. Architecture Invariants Seed" step to `codex/skills/ywc-project-scaffold/SKILL.md` only, immediately after the existing "5. Extras" step and before "## Output Rules". Do not touch `claude-code/skills/ywc-project-scaffold/SKILL.md` — claude-code has no `ywc-architecture-invariants` skill to call into.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#fr-6-ywc-project-scaffold--architecture-invariants-seed-codex-only` — FR-6
- `docs/ywc-plans/20260910-quality-gate-contract-port.md#acceptance-criteria` — AC8
- `codex/skills/ywc-architecture-invariants/SKILL.md` — existing `--mode draft` interface this step calls into

### Summary
For `new-project-plan` mode only, after the tree/explanation step, offer `ywc-architecture-invariants --mode draft --proposal <path> --output <path> --approve-write` to draft a fenced-YAML/JSON manifest from the proposed layer structure. Never written to disk without approval, `enforcement: advisory` always, skipped entirely (no manifest emitted) when the structure yields no forbidden edges. This is a deliberate claude-code/codex divergence: `develop-with-llm` wires both runtimes because both have the underlying skill; this repo's claude-code root does not, so only codex gets this step. This FR is unrelated to CRAP/Mutation gates and was not covered by the prior codex-only quality-gate batch (confirmed absent via grep across `docs/ywc-plans/20260910-codex-quality-gate-contract.md` and the `yw-000032-010` task files).

### Out of Scope (from spec)
- `claude-code/skills/ywc-project-scaffold/SKILL.md` — explicitly excluded by AC8; must remain unmodified.
- Creating a claude-code `ywc-architecture-invariants` skill — a separate, larger scope decision (spec's Open Questions), not this task.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- (None identified — no other task in this batch reads this file)

## Key Files
- `codex/skills/ywc-project-scaffold/SKILL.md` — insert one new numbered step.

## Notes
Verify at task completion, not just at start, that `claude-code/skills/ywc-project-scaffold/SKILL.md` has zero new "architecture-invariants" references — this is the explicit negative assertion AC8 requires.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-project-scaffold/SKILL.md`

### Owned Interface
(None — no public interface owned; this task calls an existing interface (`ywc-architecture-invariants --mode draft`), it does not define a new one.)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `grep -n "Architecture Invariants Seed" codex/skills/ywc-project-scaffold/SKILL.md`
- `grep -q "ywc-architecture-invariants --mode draft" codex/skills/ywc-project-scaffold/SKILL.md`
- `! grep -q "architecture-invariants" claude-code/skills/ywc-project-scaffold/SKILL.md` (must find zero matches)
- `bash scripts/validate.sh`

## Out of Scope
- Any claude-code-side scaffold change.
- Any change to `codex/skills/ywc-architecture-invariants/SKILL.md` itself — this task only calls the existing interface.
