# Task: 000040-010-docs-codex-language-resolution-reference

## Prerequisites

- [ ] (None — root foundation task)

## Allowed Edit Scope

- [ ] Edit only `codex/skills/references/language-resolution.md`.
- [ ] If any consumer skill must change to make the reference meaningful, stop and leave that for Phase `000041`.

## Stop Conditions

- [ ] Stop if project guidance already contains a conflicting Codex-wide language resolution reference.
- [ ] Stop if the policy requires session default storage; session scope is explicitly out of scope.
- [ ] Stop if implementation would need a script or runtime parser instead of Markdown instructions.

## Hardening Gate

- [ ] Classify this task as docs-only.
- [ ] Record named exception: no RED-first test; use targeted grep and `bash scripts/validate.sh`.
- [ ] Record shared contract: `language-resolution.md` defines resolution order and config semantics for downstream skills.
- [ ] Data Integrity fields are N/A.
- [ ] Critical surface review is N/A.

## Implementation Steps

- [ ] Create `codex/skills/references/language-resolution.md`.
  - [ ] Define precedence exactly: explicit `--lang` > project `.codex/ywc.json` > project guidance `AGENTS.md` / `CODEX.md` / `CLAUDE.md` > user `~/.codex/ywc.json` > ask user.
  - [ ] State there is no skill-level output-language default.
  - [ ] Define project/user config shape as `{ "lang": "<ko|ja|en|zh|es>" }`.
  - [ ] Define malformed JSON, missing `lang`, and unsupported values as unresolved tiers that fall through.
- [ ] Add supported language and alias policy.
  - [ ] Canonical codes: `ko`, `ja`, `en`, `zh`, `es`.
  - [ ] Existing aliases: `korean`, `japanese`, `english`, `chinese`, `spanish`, `한국어`, `日本語`, `中文`, `espanol`, `español`; preserve `kr` as backward-compatible input where already documented, normalize to `ko`.
  - [ ] `zh` / `chinese` means Simplified Chinese unless explicitly stated otherwise.
- [ ] Add output writing policy.
  - [ ] Human prose follows resolved language.
  - [ ] Machine-facing surfaces stay English: commands, file paths, YAML/JSON keys, code, task IDs, section contract terms, branch names, labels.
  - [ ] Conversation language follows the user and does not override artifact language.

## Task Verify

- [ ] `test -f codex/skills/references/language-resolution.md`
- [ ] `grep -q ".codex/ywc.json" codex/skills/references/language-resolution.md`
- [ ] `grep -q "~/.codex/ywc.json" codex/skills/references/language-resolution.md`
- [ ] `grep -q "ko.*ja.*en.*zh.*es" codex/skills/references/language-resolution.md`

## Verification

- [ ] `bash scripts/validate.sh`
