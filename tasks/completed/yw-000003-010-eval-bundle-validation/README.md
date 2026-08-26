# yw-000003-010-eval-bundle-validation

## Purpose
Finalize the Codex-only initials support across documentation/evals and verify source-to-marketplace parity and repository health.

## Scope
Update affected Codex localized READMEs, `agents/openai.yaml`, eval fixtures, synchronize generated marketplace output, and run final validation.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#acceptance-criteria` — AC9 and AC10
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#fr-6-keep-codex-distribution-synchronized` — source/generated parity

### Summary
The source tree is authoritative; generated marketplace output must be refreshed only through `bash scripts/sync-codex-plugin.sh`. Final evidence must cover shell/Python syntax, config and parser fixtures, task-generator contracts, install scanning, validation, and source/generated parity. Existing user deletions under `docs/ywc-plans/` must remain untouched.

### Out of Scope (from spec)
- Feature implementation in setup, generator, parsers, or consumers — handled by predecessor tasks.
- Claude Code distribution and unrelated documentation changes — excluded by the spec.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000001-030-parser-prefixed-task-ids` — parser implementation and fixtures.
- `yw-000002-020-consumer-legacy-compatibility` — consumer/documentation updates.

### Depended By
- (None — final hard gate)

## Key Files
- Generated marketplace output produced by `scripts/sync-codex-plugin.sh`
- Generated marketplace output produced by `scripts/sync-codex-plugin.sh`
- `tasks/dependency-graph.md`

## Notes
Do not hand-edit generated output. Verify only intended Codex files changed and preserve the pre-existing deleted plan files.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: repository validation, install scan, and changed-skill eval fixtures.
- Named exception: parity-only generated files are verified by sync/diff checks rather than independent tests.

### Interface Contract
- Contract: source-to-generated Codex bundle parity and eval metadata.
- Inputs: finalized source skills/references/scripts/evals.
- Outputs: identical generated marketplace copies and passing repository validation.
- Error model: sync or validation failure blocks completion.
- Impacted tests: `scripts/validate.sh`, install list, targeted evals.

### Critical Surface Review
- Review requirement: N/A — final validation and generated documentation.

### Data Integrity Hardening
- Trigger surface: N/A — generated/documentation-only finalization.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- Generated marketplace output only through `scripts/sync-codex-plugin.sh`
- Generated marketplace output only through `scripts/sync-codex-plugin.sh`
- `tasks/dependency-graph.md` batch entry

### Shared Surfaces
- Source/generated bundle parity
- Repository validation scripts

### Conflicts With
- All predecessor tasks — final hard gate must run after their merged changes.

### Parallelizable After
- `yw-000002-010-task-generator-initials-allocation`
- `yw-000002-020-consumer-legacy-compatibility`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/install.sh --list`
- `bash scripts/validate.sh`
- Source/generated parity diff check and `git diff --stat` review.

## Out of Scope
- Any implementation changes to setup, generator, parser, or executor behavior.
