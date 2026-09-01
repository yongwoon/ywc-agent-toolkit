# Task: 000038-010-docs-ywc-setup-language-skill

## Prerequisites
- [ ] `000037-010-docs-language-resolution-reference` 완료(`references/language-resolution.md` 존재).

## Allowed Edit Scope
- `claude-code/skills/ywc-setup-language/**` (신규 디렉토리 전체)
- 그 외 파일 편집 금지(consumer skill, CLAUDE.md, 다른 reference 금지).

## Stop Conditions
- `ywc-skill-author` 가 요구하는 canonical 구조를 이 스킬에 적용할 수 없으면 중단하고 보고.
- setup 이 `~/.claude/CLAUDE.md` 를 건드리는 방식(OQ2)이 프로젝트 stateful-file 규약과 충돌하면 중단하고 보고.

## Implementation Steps
- [ ] **`ywc-skill-author` 를 먼저 invoke** 해 `ywc-setup-language` 골격을 생성(NFR3).
- [ ] `SKILL.md` 작성:
  - [ ] frontmatter: `(ywc) Use when…` 로 시작, `Do not use for…` anti-trigger 로 종료, multilingual trigger 포함.
  - [ ] `**Announce at start:**` 라인.
  - [ ] Arguments: 위치 인자 `<code|full-name>`, `--user`, `--show`.
  - [ ] 동작: 대상 CLAUDE.md(기본 project, `--user` 시 `~/.claude/CLAUDE.md`)의 `## Language Policy` 섹션 create-or-replace(멱등, AC3/EC6); 대상 부재 시 delimited 섹션만 담아 생성(EC5); full-name → code 정규화(EC3).
  - [ ] `--show`: write 없이 resolved 언어 + source rung(project/user/none) 보고(AC4).
  - [ ] `> **Action required**: Read [../references/language-resolution.md]` directive 로 resolution 규칙 참조(inline 금지).
  - [ ] ≥5행 Rationalization Defense table(도메인 특화).
- [ ] README locale set 작성: `README.md`(Korean), `README.en.md`, `README.ja.md`, `README.ko.md`(Tier 1); `scripts/translate.sh` 로 `README.zh.md`/`README.es.md`(Tier 2) 생성.

## Task Verify
- [ ] `test -f claude-code/skills/ywc-setup-language/SKILL.md`
- [ ] `for l in "" .en .ja .ko .zh .es; do test -f claude-code/skills/ywc-setup-language/README$l.md; done`
- [ ] `grep -q "language-resolution.md" claude-code/skills/ywc-setup-language/SKILL.md`
- [ ] `grep -qE "^description:.*\\(ywc\\) Use when" claude-code/skills/ywc-setup-language/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` — 새 skill 이 frontmatter + Tier 1 README locale + Codex 아닌 CC 규칙 통과.
- [ ] `bash scripts/install.sh --list --cc | grep ywc-setup-language` — 목록 노출.
