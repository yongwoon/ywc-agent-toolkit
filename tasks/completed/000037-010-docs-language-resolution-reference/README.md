# 000037-010-docs-language-resolution-reference

## Purpose

언어 resolution 의 canonical source 를 만든다. 새 shared reference `claude-code/skills/references/language-resolution.md` 를 작성하고, `claude-code/skills/CLAUDE.md` 에 이를 문서화하는 `## Language Resolution` 섹션을 추가한다. 이후 모든 consumer skill 이 이 한 곳을 참조해 동일하게 언어를 해석한다.

## Scope

- **포함**: `references/language-resolution.md` 신규 작성(precedence chain, `## Language Policy` 섹션 format, code list, main-context resolution 규칙, back-compat 규칙); `CLAUDE.md` 에 `## Language Resolution` 문서화 섹션 추가.
- 이 task 는 foundation 이며 이후 phase 의 모든 task 가 이 file 을 link 한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/ywc-language-setup.md` — FR2, FR9, Iteration 1 Amendments A1/A2/A5, AC12, Data Model/Contract 섹션.

### Summary
Shared-reference 규약(`pr-bot-polling.md` 등)은 세 site — reference file, per-skill pointer, `CLAUDE.md` 문서화 섹션 — 에서 integrate 된다. 이 task 는 그중 reference file 과 `CLAUDE.md` 섹션(site 1, 3)을 만든다. resolution 은 main skill context 에서 수행하고, subagent 가 독립 해석해야 하면 두 CLAUDE.md 를 명시적으로 Read 한다(A2). canonical `## Language Policy` 는 기존 older cue 보다 우선하되 부재 시 기존 fallback 을 보존한다(A5, AC10).

### Out of Scope (from spec)
- Consumer skill 본문 수정(000038-020 / 000038-030 담당).
- 새 setup skill 작성(000038-010 담당).
- Session/대화 언어, 전용 JSON config, Codex 런타임.

## Criticality
`normal` — 보안 민감 surface 아님. Spec 에 Critical Surfaces 선언 없음.

## Dependencies

### Depends On
- (없음) — foundation task.

### Depended By
- `000038-010-docs-ywc-setup-language-skill` — 새 skill 이 이 reference 를 link.
- `000038-020-docs-wire-doc-generator-consumers` — consumer 가 이 reference 를 pointer 로 참조.
- `000038-030-docs-wire-git-artifact-consumers` — 동일.
- `000039-010-infra-validate-language-setup` — 최종 검증.

## Key Files
- `claude-code/skills/references/language-resolution.md` (신규)
- `claude-code/skills/CLAUDE.md` (`## Language Resolution` 섹션 추가)

## Notes
- Precedence chain: `--lang flag > project CLAUDE.md ## Language Policy > user ~/.claude/CLAUDE.md ## Language Policy > 각 skill 의 기존 fallback`. 마지막 rung 은 hardcoded `en` 이 아니라 "각 consumer 의 기존 fallback" 이어야 AC10(회귀 없음)이 성립.
- `CLAUDE.md` 섹션은 기존 4개 shared-ref 섹션(Bot Polling / PR Conflict / HTML Output / Schema Guide)의 "referenced-not-inlined" 방식을 따른다 — precedence chain 을 CLAUDE.md 안에 다시 쓰지 않는다.

## Out of Scope
- 실제 consumer wiring, 새 skill 작성, CI 실행.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/references/language-resolution.md`, `claude-code/skills/CLAUDE.md`.
- **Shared Surfaces**: `claude-code/skills/CLAUDE.md` (이 task 만 편집) — 다른 어떤 task 도 이 파일을 만지지 않는다.
- **Conflicts With**: (None identified)
- **Parallelizable After**: (없음 — 최초 실행 가능)
- **Task Verify**:
  - `test -f claude-code/skills/references/language-resolution.md`
  - `grep -q "## Language Resolution" claude-code/skills/CLAUDE.md`
  - `grep -q "ywc-task-generator" claude-code/skills/CLAUDE.md && grep -q "ywc-commit" claude-code/skills/CLAUDE.md` (consumer list 존재 확인)
