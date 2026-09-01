# Task: 000041-010-docs-codex-ywc-setup-skill

## Prerequisites

- [ ] `000040-010-docs-codex-language-resolution-reference` is completed.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-setup/**`.
- [ ] Do not edit consumer skills, root docs, generated plugin package, or real config files.

## Stop Conditions

- [ ] Stop if `codex/skills/ywc-setup/SKILL.md` would need frontmatter fields beyond `name` and `description`.
- [ ] Stop if setup behavior would require a runtime parser/script rather than Markdown skill instructions.
- [ ] Stop if session default storage re-enters scope.

## Hardening Gate

- [ ] Classify this task as docs-only/new skill package.
- [ ] Record named exception: no RED-first test; use install/list and validation.
- [ ] Record interface contract: `ywc-setup --scope project|user --lang <code>`.
- [ ] Data Integrity fields are N/A.
- [ ] Critical surface review is N/A.

## Implementation Steps

- [ ] Create `codex/skills/ywc-setup/SKILL.md`.
  - [ ] Frontmatter only includes `name: ywc-setup` and `description: ...`.
  - [ ] Include triggers for `ywc-setup`, `setup ywc language`, `ywc 언어 설정`, `project language default`, `user language default`.
  - [ ] Include anti-triggers: not for Claude Code, not for session language, not for project docs generation.
  - [ ] Add announce line.
  - [ ] Link `../references/language-resolution.md` as the canonical resolution policy.
- [ ] Specify setup workflow.
  - [ ] Parse `--scope project|user` and ask if omitted.
  - [ ] Parse `--lang ko|ja|en|zh|es` plus documented aliases and ask if omitted.
  - [ ] For project scope, create/update `.codex/ywc.json`.
  - [ ] For user scope, create/update `~/.codex/ywc.json`.
  - [ ] Reject `--scope session` and do not write `.codex/tmp/ywc-session.json`.
- [ ] Create README files.
  - [ ] `README.md` Korean guide.
  - [ ] `README.en.md` English guide.
  - [ ] `README.ja.md` Japanese guide.
  - [ ] `README.ko.md` Korean locale mirror.
- [ ] Create `agents/openai.yaml`.
  - [ ] Include `interface.display_name`, `interface.short_description`, `interface.default_prompt`.

## Task Verify

- [ ] `test -f codex/skills/ywc-setup/SKILL.md`
- [ ] `test -f codex/skills/ywc-setup/agents/openai.yaml`
- [ ] `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-setup/$f; done`
- [ ] `grep -q ".codex/ywc.json" codex/skills/ywc-setup/SKILL.md`
- [ ] `grep -q "~/.codex/ywc.json" codex/skills/ywc-setup/SKILL.md`
- [ ] `grep -q "session" codex/skills/ywc-setup/SKILL.md`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex | grep -q ywc-setup`
