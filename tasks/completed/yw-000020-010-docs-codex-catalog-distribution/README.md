# yw-000020-010-docs-codex-catalog-distribution

## Purpose
Publish the completed source skill in the Codex catalog and synchronize the generated marketplace package.

## Scope
Add the skill-table and routing-guide rows, recalculate the Codex skill count in all required root README locales, run the source-to-package sync, and inspect generated file parity and executable modes. Keep custom-agent catalogs unchanged.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr4--eval-and-catalog-integration`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#ac6--distribution`
- `codex/AGENTS.md#project-structure--module-organization`

### Summary
This task handles distribution surfaces after source behavior and tests are complete. The Codex source remains authoritative; `bash scripts/sync-codex-plugin.sh` generates the marketplace package. Counts must be calculated from source directories, and no custom-agent TOML or README changes are allowed.

### Out of Scope (from spec)
- New skill behavior and tests — completed in Phase `yw-000019`.
- Final full validation — handled by `yw-000020-020-infra-final-validation`.
- Claude Code, upstream, changelog, release-version, or custom-agent changes.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000019-030-test-mine-review-history-contract` — provides validated source skill and fixtures.

### Depended By
- `yw-000020-020-infra-final-validation` — verifies the synchronized result.

## Key Files
- `codex/skills/README.md`
- `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, `README.es.md`
- `plugins/ywc-agent-toolkit/skills/**` — generated only by sync script

## Notes
Calculate the post-addition source count; do not assume the existing number. Run sync from source and preserve executable mode.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: `bash scripts/sync-codex-plugin.sh`, `bash scripts/install.sh --list --codex`, and package freshness checks in `scripts/validate.sh`.
- Named exception: documentation/generated-only change; command verification replaces RED-first production tests.

### Critical Surface Review
- Review requirement: N/A — catalog and generated distribution metadata only.

### Data Integrity Hardening
- Trigger surface: N/A — no runtime durable write.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: source-to-package sync is deterministic
- Required tests: package parity and executable-mode validation

## Parallel Execution Metadata
### Ownership
- `codex/skills/README.md`
- Root README locale files listed in Key Files
- Generated package output only through `scripts/sync-codex-plugin.sh`

### Shared Surfaces
- Codex source/package parity
- Root skill-count metadata

### Conflicts With
- `yw-000020-020-infra-final-validation` — validation must run after distribution edits.

### Parallelizable After
- `yw-000019-030-test-mine-review-history-contract`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/install.sh --list --codex`
- `git diff --check`

## Out of Scope
- Editing generated files by hand, custom agents, and implementation behavior.
