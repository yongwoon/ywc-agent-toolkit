# yw-000048-010-docs-granularity-contract

## Purpose
Update the primary Codex `ywc-task-generator` contract so `human` and `llm` modes use the expanded, mode-aware granularity guidance without weakening safety invariants.

## Scope
Revise the primary `SKILL.md` reviewability, mode, Planning Advisor, and LLM naming rules. Update `references/granularity-modes.md` with the new thresholds, one-feature LLM bundling limit, exclusive Ownership, explicit Shared Surfaces, category splitting, and invariant rules. The repository has no separate `example-decomposition.md`; update the inline decomposition guidance and examples in the maintained source files instead.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260918-codex-task-generator-granularity-expansion.md#FR-1`
- `docs/ywc-plans/20260918-codex-task-generator-granularity-expansion.md#FR-2`

### Summary
The specification raises the advisory limits to `human: ~15 files / ~500 LOC` and `llm: ~35 files / ~1,200 LOC`. LLM bundling remains limited to one feature with exclusive Ownership and declared Shared Surfaces, while database migrations, library introductions, phase gates, buildability, and single-phase tasks remain invariant. The Planning Advisor must receive the selected mode and only its matching guideline.

### Out of Scope (from spec)
- Public README localization — handled by `yw-000048-020-docs-granularity-readmes`.
- Regression fixtures — handled by `yw-000048-030-test-granularity-evals`.
- Generated marketplace synchronization — handled by `yw-000049-010-infra-granularity-distribution`.
- `codex/agents/ywc-architect.toml` and unrelated Claude Code behavior.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000048-020-docs-granularity-readmes` — consumes the canonical thresholds and guardrails.
- `yw-000048-030-test-granularity-evals` — asserts the canonical instruction contract.
- `yw-000049-010-infra-granularity-distribution` — synchronizes and validates the finalized source.

## Key Files
- `codex/skills/ywc-task-generator/SKILL.md` — primary mode and advisor contract.
- `codex/skills/ywc-task-generator/references/granularity-modes.md` — detailed mode rules.

## Notes
- Keep `--mode` and `--granularity` semantics unchanged.
- Numeric thresholds are advisory and never authorize cross-feature bundling or invariant bundling.
- Preserve the one-advisor budget and unavailable-advisor fallback.

## Hardening Evidence
### Test Feedback Path
- Named exception: docs-only contract change; targeted repository searches and downstream contract fixtures provide replacement verification.

### Interface Contract
- Contract: `ywc-task-generator` granularity contract.
- Owner task: `yw-000048-010-docs-granularity-contract`.
- Canonical signature: selected mode plus matching advisory size guideline and invariant-aware bundling rules -> task decomposition guidance.
- Consumers: `yw-000048-020-docs-granularity-readmes`, `yw-000048-030-test-granularity-evals`, downstream task-generation sessions.
- Implementation opacity: consumers rely on this wording and do not invent alternate thresholds.
- Mismatch action: `NEEDS_CONTEXT`.

### Critical Surface Review
- Review requirement: N/A — documentation-only change.

### Data Integrity Hardening
- Trigger surface: N/A — docs-only task.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/granularity-modes.md`

### Shared Surfaces
- Task-generator instruction contract consumed by README and eval tasks.

### Conflicts With
- `yw-000048-020-docs-granularity-readmes` — until the canonical wording is merged.
- `yw-000048-030-test-granularity-evals` — until the canonical wording is merged.

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `rg -n '~15 files|~500 LOC|~35 files|~1,200 LOC|exclusive Ownership|Shared Surfaces|one feature' codex/skills/ywc-task-generator/SKILL.md codex/skills/ywc-task-generator/references/granularity-modes.md`
- `! rg -n '~10 files|~300 LOC|~25 files|~800 LOC' codex/skills/ywc-task-generator/SKILL.md codex/skills/ywc-task-generator/references/granularity-modes.md`
- `git diff --check`

## Out of Scope
- README locale maintenance, eval fixture authoring, package synchronization, and full validation.
