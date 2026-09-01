# Task: 000037-010-docs-language-resolution-reference

## Prerequisites
- [ ] (없음 — foundation task)

## Allowed Edit Scope
- `claude-code/skills/references/language-resolution.md` (신규)
- `claude-code/skills/CLAUDE.md` (`## Language Resolution` 섹션 추가만)
- 그 외 파일 편집 금지.

## Stop Conditions
- `CLAUDE.md` 의 기존 섹션 구조를 재배치해야 할 것 같으면 중단하고 보고(추가만 허용).
- precedence 규칙이 spec(A5)과 충돌하는 기존 CLAUDE.md 언어 규정을 발견하면 중단하고 보고.

## Implementation Steps
- [ ] `claude-code/skills/references/language-resolution.md` 생성. 다음을 포함:
  - [ ] Precedence chain: `--lang flag > project CLAUDE.md ## Language Policy > user ~/.claude/CLAUDE.md ## Language Policy > 각 skill 의 기존 fallback` (마지막 rung 은 hardcoded `en` 금지).
  - [ ] canonical `## Language Policy` 섹션 format (Output language code + Applies-to + English-preserved token 규칙) — spec 의 Data Model/Contract 블록 전재.
  - [ ] code list `ko|ja|en|es|zh` + full-name mapping(`korean`→`ko` 등).
  - [ ] main-context resolution 규칙(A2): resolution 은 main skill context 에서 수행; subagent 가 독립 해석해야 하면 `~/.claude/CLAUDE.md` 와 project `CLAUDE.md` 를 명시적으로 Read; 권장 pattern 은 main-context orchestrator 가 1회 해석 후 resolved code 를 payload 로 전달.
  - [ ] back-compat 규칙(A5): canonical `## Language Policy` 우선; 부재 시 skill 의 기존 looser cue(task-generator 의 "Documentation Writing Guidelines", spec-writer 의 "primary documentation language") 를 hardcoded default 이전 fallback 으로 허용 → AC10 보존.
  - [ ] English-preserved token: conventional-commit `type:` prefix, PR-title `[task-id]`/prefix, technical terms.
- [ ] `claude-code/skills/CLAUDE.md` 에 `## Language Resolution` 섹션 추가(기존 4개 shared-ref 섹션 뒤, 동일 style):
  - [ ] `references/language-resolution.md` 를 canonical source 로 명시.
  - [ ] consumer skill 나열: `ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`, `ywc-create-pr`, `ywc-commit`.
  - [ ] no-block invariant(NFR1) 명시.
  - [ ] referenced-not-inlined 규칙 준수(precedence chain 을 CLAUDE.md 안에 재기술하지 않음).

## Task Verify
- [ ] `test -f claude-code/skills/references/language-resolution.md`
- [ ] `grep -q "## Language Resolution" claude-code/skills/CLAUDE.md`
- [ ] `grep -qE "ywc-task-generator.*ywc-commit|ywc-commit" claude-code/skills/CLAUDE.md`

## Verification
- [ ] `bash scripts/validate.sh` 통과(구조/shellcheck 무변경 확인).
- [ ] markdownlint 대상 파일이면 lint 통과.
