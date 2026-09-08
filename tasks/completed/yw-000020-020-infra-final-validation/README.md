# yw-000020-020-infra-final-validation

## Purpose
Run the complete focused and repository validation suite for the Codex mine-review-history port.

## Scope
Verification only: shell syntax and helper tests, JSON parsing, contract evals, install lists, package sync/freshness, full structural validation, targeted boundary checks, and diff hygiene.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#verification`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#outcome-oracle`

### Summary
This task confirms the source and generated package satisfy the spec's quality threshold. It must not repair production behavior or alter catalog content; failures are reported back to the owning task.

### Out of Scope (from spec)
- Any source, fixture, catalog, or generated-package edits — those belong to prior tasks.
- Custom-agent catalog changes.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000020-010-docs-codex-catalog-distribution` — provides synchronized catalog and generated package.

### Depended By
- (None — terminal verification task)

## Key Files
- No intended file edits; command outputs and failures only.

## Notes
If a check fails, stop and report the exact owning task rather than broadening this verification task's scope.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: all commands in the spec Verification block.
- Named exception: verification-only task; no production edits.

### Critical Surface Review
- Review requirement: N/A — verification-only.

### Data Integrity Hardening
- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- Validation commands only; no source ownership.

### Shared Surfaces
- Repository validation status
- Source/package freshness

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000020-010-docs-codex-catalog-distribution`

### Task Verify
- `bash -n codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh`
- `bash codex/skills/ywc-mine-review-history/scripts/test_fetch_bulk_review_comments.sh`
- `python3 -m json.tool codex/skills/ywc-mine-review-history/evals/evals.json >/dev/null`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/install.sh --list --codex`
- `bash scripts/install.sh --list --codex-agents`
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `git diff --check`

## Out of Scope
- Fixing failures or changing any repository file.
