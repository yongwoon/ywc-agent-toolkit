# yw-000047-040-infra-readonly-contract-distribution

## Purpose
Synchronize the generated Codex marketplace reference from the validated source and perform the final source/package freshness checks for the inline return contract.

## Scope
- Run the source-first Codex plugin synchronization script.
- Retain only the generated marketplace reference change related to the shared status contract.
- Run final validation and diff checks after both Phase `000046` tasks pass.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#fr-5-generated-package-synchronization` — source-first sync behavior.
- `docs/ywc-plans/20260917-codex-readonly-agent-inline-contract.md#ac6--distribution-parity` — generated package acceptance criterion.

### Summary
The Codex source tree is authoritative and the marketplace package is generated. After the source contract, validator, and installed smoke test are complete, run `bash scripts/sync-codex-plugin.sh` and verify that the generated `subagent-status-actions.md` matches its source. Do not hand-edit generated files first or broaden the change into unrelated package updates.

### Out of Scope (from spec)
- Source agent/reference wording — handled by `yw-000045-010-docs-readonly-inline-contract-source`.
- Validator — handled by `yw-000046-020-infra-readonly-contract-validator`.
- Installed smoke test — handled by `yw-000046-030-test-installed-readonly-contract`.
- Claude-side distribution, release/version files, and upstream repository changes.

## Criticality
normal

## Dependencies

### Depends On
- `yw-000046-020-infra-readonly-contract-validator` — source validator passes.
- `yw-000046-030-test-installed-readonly-contract` — installed parity passes.

### Depended By
- (None — final task in this batch)

## Key Files
- `scripts/sync-codex-plugin.sh` — execute source-to-generated synchronization.
- `plugins/ywc-agent-toolkit/skills/references/subagent-status-actions.md` — generated output expected to change.
- `scripts/validate.sh` — final freshness and structure oracle.

## Notes
Run synchronization from the repository root and inspect `git diff --stat`/`git diff --check`; retain only the generated marketplace reference change required by the source edit.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `bash scripts/validate.sh` plus `bash tests/install-codex-agents-test.sh` from predecessor tasks.
- Named exception: generated-file-only sync; source-first synchronization and final freshness validation replace RED-first production evidence.

### Interface Contract
- Contract: source/generated reference parity.
- Owner task: `yw-000047-040-infra-readonly-contract-distribution`.
- Canonical signature: `codex/skills/references/subagent-status-actions.md` → byte/content-equivalent generated marketplace counterpart.
- Consumers: marketplace distribution and final repository validation.
- Implementation opacity: generated files are never hand-edited before synchronization.
- Mismatch action: return `NEEDS_CONTEXT` if sync produces unrelated changes or source/package parity cannot be established.

### Data Integrity Hardening
- Trigger: N/A — generated distribution files only; no runtime data or mutable service state.

### Critical Surface Review
- N/A — not a critical surface under the spec's criticality rules.

## Out of Scope
No source contract edits, new installer behavior, runtime agent changes, release metadata, or unrelated generated-package refresh.

## Parallel Execution Metadata
- **Ownership:** `plugins/ywc-agent-toolkit/skills/references/subagent-status-actions.md` as generated output and source-to-package synchronization commands.
- **Shared Surfaces:** Source/generated Codex skill reference parity; repository validation output.
- **Conflicts With:** All earlier tasks; this is the final hard-gate task.
- **Parallelizable After:** Merged completion of `yw-000046-020-infra-readonly-contract-validator` and `yw-000046-030-test-installed-readonly-contract`.
- **Task Verify:** `bash scripts/sync-codex-plugin.sh`; `bash scripts/validate.sh`; `git diff --check`; `git diff --stat`.

