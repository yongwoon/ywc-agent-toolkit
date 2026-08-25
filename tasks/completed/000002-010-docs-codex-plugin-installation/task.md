# 000002-010-docs-codex-plugin-installation — Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000001-010-infra-codex-plugin-package-layout` is completed (merged).
- [ ] `000001-020-infra-codex-plugin-validation` is completed (merged).
- [ ] `.codex-plugin/plugin.json` has `"skills": "./skills/"`.
- [ ] `bash scripts/validate.sh` passes.

## Allowed Edit Scope

- [ ] Stay within root README/localized README documentation.
- [ ] If docs need to contradict implementation behavior, stop and report the drift.

## Stop Conditions

- [ ] Stop if Codex marketplace availability is unknown and wording would imply official availability.
- [ ] Stop if translation tooling changes files outside root README locales unexpectedly.
- [ ] Stop if README instructions require a command that cannot be verified or sourced.

## Implementation Steps

- [ ] Update `README.md` Installation.
  - [ ] Add Codex CLI plugin install guidance using `/plugins`.
  - [ ] Add Codex App install guidance using sidebar Plugins flow.
  - [ ] Keep bash install as fallback.
  - [ ] Use conservative wording until official marketplace listing is confirmed.
- [ ] Align documentation with actual package layout.
  - [ ] Mention `.codex-plugin/plugin.json` only as repository packaging metadata, not as a manual user edit target.
  - [ ] Avoid saying `scripts/install.sh --codex` uses plugin metadata.
  - [ ] Preserve existing Claude Code plugin marketplace section.
- [ ] Decide and apply translation policy.
  - [ ] Either update `README.ko.md`, `README.ja.md`, `README.es.md`, and `README.zh.md` in the same PR.
  - [ ] Or explicitly defer localization and include `bash scripts/translate.sh --dry-run` evidence in PR notes.
- [ ] Verify docs.
  - [ ] Run translation dry-run.
  - [ ] Run local validation and install list.
  - [ ] Confirm Markdown links and commands render clearly.

## Task Verify

- [ ] `bash scripts/translate.sh --dry-run`
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list`
- [ ] `rg -n "Codex CLI|Codex App|/plugins|bash script" README.md`

## Verification

- [ ] Structure validation passes: `bash scripts/validate.sh`
- [ ] Install listing works: `bash scripts/install.sh --list`
- [ ] Translation dry-run completes: `bash scripts/translate.sh --dry-run`

