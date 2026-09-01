# Task: 000041-040-docs-catalog-language-setup

## Prerequisites

- [ ] `000040-010-docs-codex-language-resolution-reference` is completed.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/README.md` and root `README*.md`.
- [ ] Do not edit skill behavior files or generated plugin files.

## Stop Conditions

- [ ] Stop if root README localization policy is unclear or would require regenerating translations outside project workflow.
- [ ] Stop if adding `ywc-setup` to root docs would imply Claude Code support.

## Hardening Gate

- [ ] Classify this task as docs-only catalog update.
- [ ] Record named exception: no RED-first test; use grep and validation.
- [ ] Record interface contract: docs expose examples and resolution order.
- [ ] Data Integrity fields are N/A.
- [ ] Critical surface review is N/A.

## Implementation Steps

- [ ] Update `codex/skills/README.md`.
  - [ ] Add `ywc-setup` to skill list.
  - [ ] Add routing row for output language defaults.
  - [ ] Include examples: `ywc-setup --scope project --lang ko`, `ywc-setup --scope user --lang ja`.
  - [ ] Summarize resolution order and session exclusion.
- [ ] Update root `README*.md` only where appropriate.
  - [ ] Add Codex-only `ywc-setup` mention.
  - [ ] Avoid changing Claude Code skill tables unless they explicitly list Codex-only skills.
  - [ ] Keep localized README text consistent with existing locale style.
- [ ] Ensure docs point to Codex scope and do not claim Claude Code parity.

## Task Verify

- [ ] `grep -q "ywc-setup" codex/skills/README.md`
- [ ] `grep -q ".codex/ywc.json" codex/skills/README.md`
- [ ] `grep -q "~/.codex/ywc.json" codex/skills/README.md`
- [ ] `grep -q "session" codex/skills/README.md`

## Verification

- [ ] `bash scripts/validate.sh`
