# 000038-010-docs-ywc-setup-language-skill

## Purpose

새 skill `ywc-setup-language` 를 작성한다. project 또는 user 단위 `CLAUDE.md` 의 `## Language Policy` 섹션을 멱등하게 write/update 하고, `--show` read 모드를 제공한다. 프로젝트 규칙에 따라 **`ywc-skill-author` 를 먼저 invoke** 해 canonical frontmatter/구조/README locale set 을 갖춘다.

## Scope

- **포함**: `claude-code/skills/ywc-setup-language/` 신규 디렉토리 — `SKILL.md`, README locale set(`.md`/`.en`/`.ja`/`.ko` Tier 1 + 생성된 `.zh`/`.es` Tier 2).
- setup 동작: 위치 인자 = 언어 코드/full-name; `--user`(→ `~/.claude/CLAUDE.md`, 기본은 project `CLAUDE.md`); `--show`(write 없이 resolved 언어와 source rung 보고); 멱등 in-place 갱신.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/ywc-language-setup.md` — FR1, FR8, NFR3, AC1–AC4, AC11, OQ1(skill 이름), OQ2(user-global 생성 시 확인 방식), EC5/EC6.

### Summary
`ywc-setup-language <code> [--user] [--show]` 는 canonical `## Language Policy` 섹션을 올바른 CLAUDE.md 에 생성/갱신한다. 대상 CLAUDE.md 부재 시(특히 `--user`) delimited 섹션만 담아 생성한다(EC5). 재실행은 append 가 아니라 in-place replace(AC3, EC6). resolution 규칙 자체는 000037-010 의 `language-resolution.md` 를 `> **Action required**: Read` directive 로 참조한다.

### Out of Scope (from spec)
- consumer skill 수정(000038-020/030).
- resolution 규칙 본문 정의(000037-010 이 소유).

## Criticality
`normal` — 보안 민감 surface 아님.

## Dependencies

### Depends On
- `000037-010-docs-language-resolution-reference` — skill 본문이 `language-resolution.md` 를 참조하고 canonical `## Language Policy` format 을 write.

### Depended By
- `000039-010-infra-validate-language-setup` — 구조/README locale set CI 검증.

## Key Files
- `claude-code/skills/ywc-setup-language/SKILL.md` (신규)
- `claude-code/skills/ywc-setup-language/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` (신규, Tier 1)
- `claude-code/skills/ywc-setup-language/README.zh.md` / `README.es.md` (신규, 생성된 Tier 2 — `scripts/translate.sh`)

## Notes
- **NFR3 준수**: 새 `ywc-*` skill 이므로 반드시 `ywc-skill-author` 를 먼저 invoke(frontmatter `(ywc) Use when… / Do not use for…`, multilingual triggers, `**Announce at start:**`, ≥5행 Rationalization Defense).
- **OQ1**: 이름은 `ywc-setup-language` 로 확정(넓은 `ywc-setup` 는 scope creep 위험). 변경 시 이 task 안에서 결정.
- **OQ2**: `--user` 로 `~/.claude/CLAUDE.md` write 시 `@`-activation 없이 delimited 섹션 write + 1줄 confirmation(권장). author 시 확정.
- README.md 는 Korean, `README.[locale].md` 는 해당 locale, 그 외 파일은 English(프로젝트 규칙).

## Out of Scope
- consumer wiring, resolution 규칙 정의, CI 실행.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-setup-language/**` (신규 디렉토리 전체).
- **Shared Surfaces**: 없음 — 신규 디렉토리라 기존 파일과 겹치지 않음.
- **Conflicts With**: (None identified)
- **Parallelizable After**: `000037-010-docs-language-resolution-reference`
- **Task Verify**:
  - `test -f claude-code/skills/ywc-setup-language/SKILL.md`
  - `for l in "" .en .ja .ko .zh .es; do test -f claude-code/skills/ywc-setup-language/README$l.md || echo "missing README$l"; done`
  - `grep -q "language-resolution.md" claude-code/skills/ywc-setup-language/SKILL.md`
