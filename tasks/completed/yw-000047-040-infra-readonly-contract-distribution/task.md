# yw-000047-040-infra-readonly-contract-distribution — Implementation Checklist

## Prerequisites
- [ ] `yw-000046-020-infra-readonly-contract-validator` is completed and merged.
- [ ] `yw-000046-030-test-installed-readonly-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Run the existing sync and validation commands from the repository root.
- [ ] Allow generated output only under `plugins/ywc-agent-toolkit/skills/`; stop before hand-editing generated files or changing unrelated files.

## Stop Conditions
- [ ] Stop if synchronization produces unrelated generated changes.
- [ ] Stop if source validation or installed smoke coverage fails.
- [ ] Stop if the generated reference does not match the source after one source-first sync.

## Hardening Gate
- [ ] Classify as generated-file-only distribution maintenance.
- [ ] Use predecessor validation and smoke-test results as existing coverage; sync-first is the named exception to RED-first production edits.
- [ ] Record source/generated parity as the cross-task interface contract.
- [ ] Data Integrity Hardening: N/A — no mutable runtime state.
- [ ] Critical review: N/A — not a critical surface.

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root without editing the generated package first.
  - Confirm the generated `subagent-status-actions.md` carries the source reference change.
  - Confirm no unrelated generated package files changed.
- [ ] Run final source/package and installation checks: `bash scripts/validate.sh`, `bash tests/install-codex-agents-test.sh`, and the two Codex `--list` install checks from the spec.
- [ ] Review `git diff --stat` and `git diff --check`; report any unexpected source or generated changes instead of broadening scope.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`.
- [ ] `bash scripts/validate.sh`.
- [ ] `bash tests/install-codex-agents-test.sh`.
- [ ] `bash scripts/install.sh --list --codex`.
- [ ] `bash scripts/install.sh --list --codex-agents`.
- [ ] `git diff --check`.

## Verification
- [ ] Repository has no project lint, typecheck, unit-test, integration-test, or build command; final validation is covered by the commands above.

