# Task: 000042-010-infra-codex-language-setup-validation

## Prerequisites

- [ ] `000041-010-docs-codex-ywc-setup-skill` is completed.
- [ ] `000041-020-docs-wire-artifact-language-consumers` is completed.
- [ ] `000041-030-docs-wire-pr-orchestration-consumers` is completed.
- [ ] `000041-040-docs-catalog-language-setup` is completed.

## Allowed Edit Scope

- [ ] Generated plugin files changed only by `bash scripts/sync-codex-plugin.sh`, if needed.
- [ ] Do not manually edit source skill files in this task except to revert accidental local validation artifacts.

## Stop Conditions

- [ ] Stop if `bash scripts/validate.sh` fails for a source issue owned by a predecessor task.
- [ ] Stop if generated plugin package requires manual edits.
- [ ] Stop if `ywc-setup` is absent from install list after source skill exists.

## Hardening Gate

- [ ] Classify this task as infra/package validation.
- [ ] Existing coverage: `bash scripts/validate.sh`.
- [ ] Record interface contract: Codex source package and generated plugin package are in sync.
- [ ] Data Integrity fields are N/A.
- [ ] Critical surface review is N/A.

## Implementation Steps

- [ ] Run generated package sync if source skill changes make plugin package stale.
  - [ ] Use `bash scripts/sync-codex-plugin.sh`.
  - [ ] Do not manually edit `plugins/ywc-agent-toolkit/skills/**`.
- [ ] Run full repository validation.
  - [ ] `bash scripts/validate.sh`
  - [ ] If it fails, classify failure by owning task and stop with that routing.
- [ ] Run install/list checks.
  - [ ] `bash scripts/install.sh --list --codex | grep -q ywc-setup`
  - [ ] Optionally verify isolated install: `CODEX_HOME="$(mktemp -d)" bash scripts/install.sh --codex ywc-setup`
- [ ] Run targeted language wiring search.
  - [ ] Confirm `language-resolution.md` is referenced by all touched consumer skills.
  - [ ] Confirm no touched language-sensitive skill still advertises `ko` or `en` as a skill default.
- [ ] Confirm documentation discoverability.
  - [ ] `grep -q "ywc-setup" codex/skills/README.md`
  - [ ] `grep -q ".codex/ywc.json" codex/skills/README.md`

## Task Verify

- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex | grep -q ywc-setup`
- [ ] `rg -n "language-resolution.md" codex/skills/ywc-task-generator codex/skills/ywc-spec-writer codex/skills/ywc-gen-testcase codex/skills/ywc-project-docs codex/skills/ywc-create-pr codex/skills/ywc-agentic codex/skills/ywc-finish-branch codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`

## Verification

- [ ] `bash scripts/validate.sh`
