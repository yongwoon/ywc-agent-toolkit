# 000041-010-docs-codex-ywc-setup-skill

## Purpose

Codex 전용 `ywc-setup` skill 을 추가해 project 또는 user scope 의 기본 output language 를 설정할 수 있게 한다. 이 task 는 새 skill directory 전체와 Codex UI metadata 를 소유한다.

## Scope

- `codex/skills/ywc-setup/` 신규 directory 작성.
- `SKILL.md`, Tier 1 README files, `agents/openai.yaml` 추가.
- `--scope project|user`, `--lang ko|ja|en|zh|es`, `--scope session` rejection 동작 문서화.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-ywc-language-setup.md` — AC1-AC3, FR-1, FR-2, FR-3, Data Model, Edge Cases.

### Summary

`ywc-setup`은 `.codex/ywc.json` 또는 `~/.codex/ywc.json`에 `{ "lang": "<code>" }`를 쓰는 setup skill 이다. `--scope` 또는 `--lang` 이 빠진 경우 질문하고, alias 입력은 canonical code 로 normalize 한다. Session scope 는 의도적으로 지원하지 않으며 `.codex/tmp/ywc-session.json`을 만들지 않는다.

### Out of Scope (from spec)

- Shared resolution reference 작성 — `000040-010-docs-codex-language-resolution-reference`.
- 기존 consumer skill wiring — `000041-020`, `000041-030`.
- Catalog/root docs discoverability — `000041-040`.

## Dependencies

### Depends On

- `000040-010-docs-codex-language-resolution-reference` — `ywc-setup` 본문이 shared reference 를 link.

### Depended By

- `000042-010-infra-codex-language-setup-validation` — new skill structure, install list, validation 확인.

## Key Files

- `codex/skills/ywc-setup/SKILL.md`
- `codex/skills/ywc-setup/README.md`
- `codex/skills/ywc-setup/README.en.md`
- `codex/skills/ywc-setup/README.ja.md`
- `codex/skills/ywc-setup/README.ko.md`
- `codex/skills/ywc-setup/agents/openai.yaml`

## Notes

- Codex `SKILL.md` frontmatter 는 `name`과 `description`만 허용된다.
- Tier 2 README(`README.zh.md`, `README.es.md`)는 새 skill 에서 만들지 않아도 된다. 만들 경우 이후 유지 대상이 된다.
- `~/.codex/ywc.json` write 는 user scope 이므로 작업 전 path 를 명확히 보여주고, overwrite 가 아니라 `{ "lang": "<code>" }` shape 로 create/update 하도록 지시한다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only skill package; verification is install/list and repository validation.

### Interface Contract

- Contract: `ywc-setup --scope project|user --lang <code>`
- Inputs: scope, language code or alias
- Outputs: `.codex/ywc.json` or `~/.codex/ywc.json` with canonical `{ "lang": "<code>" }`
- Error model: unsupported scope/lang asks for correction; session scope rejected without write
- Impacted tests: `bash scripts/validate.sh`, `bash scripts/install.sh --list --codex`

### Critical Surface Review

- Review requirement: N/A — writes documented config files only; no secrets or runtime code.

### Data Integrity Hardening

- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-setup/**`

### Shared Surfaces

- Codex skill catalog metadata.
- Shared language resolution reference (read-only).

### Conflicts With

- (None identified)

### Parallelizable After

- `000040-010-docs-codex-language-resolution-reference`

### Task Verify

- `test -f codex/skills/ywc-setup/SKILL.md`
- `test -f codex/skills/ywc-setup/agents/openai.yaml`
- `for f in README.md README.en.md README.ja.md README.ko.md; do test -f codex/skills/ywc-setup/$f; done`
- `grep -q "scope project" codex/skills/ywc-setup/SKILL.md`
- `grep -q "scope user" codex/skills/ywc-setup/SKILL.md`
- `grep -q "session" codex/skills/ywc-setup/SKILL.md`

## Out of Scope

- Editing `scripts/install.sh` or `scripts/validate.sh`.
- Creating `.codex/ywc.json` in this repository as part of implementation.
- Adding Claude Code parity.
