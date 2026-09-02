# yw-000016-010-test-scaffold-contract-evals

## Purpose
Add machine-readable Codex contract fixtures proving the new conditional research and approval-gated reference-refresh behavior.

## Scope
Append two cases to the established `evals.json` schema while preserving all four existing fixtures and avoiding any expectation of silent edits.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr6--codex-contract-coverage-and-packaging` — fixture shape and coverage
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#ac10` — acceptance criteria for both cases

### Summary
One fixture exercises a large or contested scaffold request and asserts conditional research/delta handling. The other asks to refresh `go.md` and asserts target inference, additive proposal, and approval stop. The existing JSON schema and fixtures remain unchanged.

### Out of Scope (from spec)
- Source skill and reference implementation — handled by Phase 000015 tasks.
- Plugin synchronization and final repository validation — handled by `yw-000017-010-infra-scaffold-sync-validation`.

## Dependencies
### Depends On
- `yw-000015-010-domain-scaffold-routing` — defines the modes and status behavior under test.
- `yw-000015-020-refactor-scaffold-reference-enrichment` — defines the reference targets and terms under test.

### Depended By
- `yw-000017-010-infra-scaffold-sync-validation` — runs structural validation after the fixture update.

## Key Files
- `codex/skills/ywc-project-scaffold/evals/evals.json` — two appended contract cases.

## Notes
Use the existing `prompt` / `expected_output` / `files` shape; optional expectation arrays must match the repository harness schema if used.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-project-scaffold/evals/evals.json`

### Shared Surfaces
- Codex contract-eval JSON schema and `ywc-project-scaffold` output vocabulary.

### Conflicts With
- `(None identified)`

### Parallelizable After
- `yw-000015-010-domain-scaffold-routing`
- `yw-000015-020-refactor-scaffold-reference-enrichment`

### Task Verify
- `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Do not alter existing fixture prompts, add a new eval mechanism, or edit source skill/reference files.
