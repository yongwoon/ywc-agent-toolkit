# yw-000048-030-test-granularity-evals

## Purpose
Add focused source-level regression fixtures that lock the expanded task-generator granularity contract.

## Scope
Append four valid entries to `codex/skills/ywc-task-generator/evals/evals.json`: an accepted LLM vertical slice, a rejected cross-feature bundle, a human category split, and mode-aware Planning Advisor behavior. Assertions must cover the new thresholds and reject superseded values without changing the generic runner.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260918-codex-task-generator-granularity-expansion.md#FR-4`
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/granularity-modes.md`

### Summary
The eval fixtures are the executable contract for the four behavior boundaries named in AC1–AC4. They must distinguish acceptable one-feature LLM bundling from cross-feature bundling, preserve human category splitting, and require the advisor payload to name the selected mode and matching guideline. The fixtures should remain source-level and preserve the existing eval schema.

### Out of Scope (from spec)
- Primary instruction edits — handled by `yw-000048-010-docs-granularity-contract`.
- Public README alignment — handled by `yw-000048-020-docs-granularity-readmes`.
- Generic runner changes unless an actual limitation is discovered.
- Generated package synchronization — handled by `yw-000049-010-infra-granularity-distribution`.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000048-010-docs-granularity-contract` — provides the source assertions and canonical wording.

### Depended By
- `yw-000049-010-infra-granularity-distribution` — runs the completed contract suite as a release gate.

## Key Files
- `codex/skills/ywc-task-generator/evals/evals.json` — four regression fixtures.

## Notes
- Preserve valid JSON and existing fixture ordering conventions.
- Do not add assertions for historical plans or generated files.

## Hardening Evidence
### Test Feedback Path
- RED-first target: the four new entries in `codex/skills/ywc-task-generator/evals/evals.json` should fail against the old thresholds before source updates are present.

### Interface Contract
- Contract: task-generator contract-eval fixture schema.
- Owner task: `yw-000048-030-test-granularity-evals`.
- Canonical signature: valid eval record with source assertions -> contract runner verdict.
- Consumers: `scripts/run-codex-skill-contract-evals.sh`, `yw-000049-010-infra-granularity-distribution`.
- Implementation opacity: the runner consumes schema-valid fixtures without requiring runner changes.
- Mismatch action: `NEEDS_CONTEXT`.

### Critical Surface Review
- Review requirement: N/A — source-level evaluation fixtures only.

### Data Integrity Hardening
- Trigger surface: N/A — test data only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-task-generator/evals/evals.json`

### Shared Surfaces
- Eval JSON schema and source-level task-generator contract paths.

### Conflicts With
- `yw-000048-010-docs-granularity-contract` — fixtures depend on finalized source wording.

### Parallelizable After
- `yw-000048-010-docs-granularity-contract`

### Task Verify
- `python3 -m json.tool codex/skills/ywc-task-generator/evals/evals.json >/dev/null`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `git diff --check`

## Out of Scope
- Generic runner implementation, README localization, source instruction edits, and generated package synchronization.
