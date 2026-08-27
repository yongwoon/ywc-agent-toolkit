# yw-000009-010-infra-codex-package-sync

## Purpose
Synchronize the authoritative Codex skill source into the generated marketplace package and prove bundle parity.

## Scope
Run the repository sync script after the source test task, verify the generated test copy byte-for-byte, run install listing and repository validation, and confirm the final diff stays within the specification boundary.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr223-review-artifact-test-hardening.md#acceptance-criteria` — AC6–AC8 define validation, parity, and scope requirements.
- `docs/ywc-plans/20260826-codex-pr223-review-artifact-test-hardening.md#global-constraints` — `codex/skills/` is authoritative and `plugins/` is generated.
- `codex/AGENTS.md#build-test-and-development-commands` — sync, install-list, and validation commands.

### Summary
This is a mechanical packaging hard gate after the source-side test is complete. `bash scripts/sync-codex-plugin.sh` regenerates the marketplace tree; the generated test must match the source test byte-for-byte, and the install listing plus validation script must pass. No generated file is edited independently.

### Out of Scope (from spec)
- Source test implementation — `yw-000008-010-test-collector-contract-harness`.
- Claude files, Nitpick parser/producer, `raw_fallback`, and collector production behavior.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000008-010-test-collector-contract-harness` — provides the finalized authoritative source test to package.

### Depended By
- (None — terminal hard gate for this spec)

## Key Files
- `plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/**` — generated marketplace output.

## Notes
- Treat `codex/skills/` as the only source of truth.
- The sync may update more generated files; inspect the diff and stop if unrelated production or Claude content changes.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: `bash scripts/validate.sh` plus the focused source test from `yw-000008-010`.

### Interface Contract
- Contract: source-to-marketplace generated bundle parity.
- Inputs: `codex/skills/**` and `scripts/sync-codex-plugin.sh`.
- Outputs: matching generated skill files under `plugins/ywc-agent-toolkit/skills/**`.
- Error model: sync failure or validation/parity mismatch blocks completion.
- Impacted tests: parity `diff`, install listing, and `scripts/validate.sh`.

### Critical Surface Review
- Review requirement: N/A — generated packaging and validation only.

### Data Integrity Hardening
- Trigger surface: N/A — generated-file synchronization only.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/**` generated output only.
- `scripts/sync-codex-plugin.sh` execution and validation evidence; do not modify the script.

### Shared Surfaces
- Codex source/package parity
- Repository-wide validation and install listing

### Conflicts With
- Any task independently editing `plugins/ywc-agent-toolkit/**`.
- Any task changing `codex/skills/ywc-handle-pr-reviews/**` after Phase `yw-000008`.

### Parallelizable After
- `yw-000008-010-test-collector-contract-harness`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `diff -u codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`
- `bash scripts/install.sh --list --codex`
- `bash scripts/validate.sh`

## Out of Scope
- Editing generated output by hand.
- Modifying the source collector, source test, Claude tree, or any Nitpick-related behavior.
