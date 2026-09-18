# yw-000048-020-docs-granularity-readmes

## Purpose
Align the maintained public task-generator README guidance with the canonical expanded granularity contract.

## Scope
Update `codex/skills/ywc-task-generator/README.md` and only the locale README counterparts required by the repository translation workflow. Preserve the required Tier 1 and maintained Tier 2 file set while ensuring published guidance states the same human/LLM thresholds, one-feature limit, Ownership, Shared Surfaces, and invariant protections.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260918-codex-task-generator-granularity-expansion.md#FR-3`
- `codex/skills/ywc-task-generator/SKILL.md`

### Summary
The public README must not contradict the primary skill instructions. The default Korean README and any locale files marked as maintained for these strings should use the expanded values and guardrails. Translation scope is limited to the repository’s documented workflow.

### Out of Scope (from spec)
- Primary contract changes — handled by `yw-000048-010-docs-granularity-contract`.
- Eval fixtures — handled by `yw-000048-030-test-granularity-evals`.
- Generated marketplace mirror — handled by `yw-000049-010-infra-granularity-distribution`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000048-010-docs-granularity-contract` — provides canonical wording and thresholds.

### Depended By
- `yw-000049-010-infra-granularity-distribution` — syncs the finalized source documentation.

## Key Files
- `codex/skills/ywc-task-generator/README.md` — default public guidance.
- `codex/skills/ywc-task-generator/README.*.md` — maintained locale counterparts only.

## Notes
- Do not hand-edit generated plugin files.
- Do not update unrelated historical plans or locale strings outside the maintained granularity section.

## Hardening Evidence
### Test Feedback Path
- Named exception: documentation-only update; targeted searches and repository validation replace RED-first production tests.

### Interface Contract
- Contract: public granularity guidance.
- Owner task: `yw-000048-020-docs-granularity-readmes`.
- Canonical signature: README mode table and guardrails -> public user-facing explanation consistent with `SKILL.md`.
- Consumers: users and generated marketplace documentation.
- Implementation opacity: consumers trust the canonical source task and do not infer divergent thresholds.
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
- `codex/skills/ywc-task-generator/README.md`
- Maintained `codex/skills/ywc-task-generator/README.*.md` granularity sections.

### Shared Surfaces
- Public task-generator documentation contract.

### Conflicts With
- `yw-000048-010-docs-granularity-contract` — source wording must land first.

### Parallelizable After
- `yw-000048-010-docs-granularity-contract`

### Task Verify
- `rg -n '~15 files|~500 LOC|~35 files|~1,200 LOC' codex/skills/ywc-task-generator/README*.md`
- `! rg -n '~10 files|~300 LOC|~25 files|~800 LOC' codex/skills/ywc-task-generator/README*.md`
- `bash scripts/validate.sh`

## Out of Scope
- Source instruction wording, eval fixtures, generated plugin content, and unrelated translations.
