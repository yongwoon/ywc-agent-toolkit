# 000038-030-docs-wire-git-artifact-consumers

## Purpose

Git artifact consumer 2종(`ywc-create-pr`, `ywc-commit`)이 shared `references/language-resolution.md` 로 언어를 해석하도록 wiring 한다. create-pr 은 정책 존재 시 별도 언어 prompt 를 skip 하고 옵션을 5개 언어로 넓히며, commit 은 message 설명부에 언어 해석을 새로 도입한다. prefix/type/기술용어는 영어 유지.

## Scope

- **포함**: `ywc-create-pr` Step 0 에 resolution 추가(정책 있으면 `AskUserQuestion` skip, 없으면 현행 prompt 유지 + 옵션을 `ko|ja|en|es|zh` 로 확대); `ywc-commit` 에 resolution step 추가(설명부 언어 결정, `type:` prefix·기술용어 영어 유지).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/ywc-language-setup.md` — FR6(create-pr), FR7(commit), AC6, AC7, EC4, EC7.

### Summary
`ywc-create-pr` 는 현재 `--lang` 없으면 English/Japanese/Korean 3개만 제시하는 `AskUserQuestion` 을 띄우고 CLAUDE.md 추론이 전혀 없다(SKILL.md:52). FR6: prompt 이전에 resolution 을 수행해 정책이 있으면 그 언어로 제목·본문을 쓰고 prompt 를 skip; 없을 때만 prompt(옵션 5개로 확대). `--title` 이 주어지면 제목은 verbatim 유지, 정책은 본문 언어만 지배(EC4). `ywc-commit` 은 언어 개념이 아예 없으므로(SKILL.md) FR7 로 message 설명부 언어 해석을 새로 추가하되 `type:` prefix·기술용어는 영어 유지; 위임 chain(finish-branch→create-pr→commit)에서도 read-only·멱등이라 중복 prompt 없음(EC7, prompt 자체 없음).

### Out of Scope (from spec)
- 문서 생성 consumer wiring(000038-020).
- PR 제목 `[task-id]`/prefix 를 비영어로 바꾸기(영어 유지).

## Criticality
`normal` — PR/commit 텍스트 생성. 보안 민감 surface 아님.

## Dependencies

### Depends On
- `000037-010-docs-language-resolution-reference` — pointer 대상 reference 존재.

### Depended By
- `000039-010-infra-validate-language-setup` — 최종 검증.

## Key Files
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-commit/SKILL.md`

## Notes
- create-pr: 정책 부재 시 현행 prompt 동작 보존(AC10). 옵션 확대는 일관성(누락된 `es`/`zh` 추가).
- commit: 설명부(description)만 언어 지배. `feat:`/`fix:` 등 conventional type prefix 와 whitelist 기술용어는 항상 영어.
- 두 skill 모두 resolution 규칙은 inline 하지 말고 `> **Action required**: Read` directive 로 참조.

## Out of Scope
- 문서 생성 consumer, 새 skill, CLAUDE.md 섹션.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-create-pr/SKILL.md`, `claude-code/skills/ywc-commit/SKILL.md`.
- **Shared Surfaces**: `references/language-resolution.md` 계약(읽기 전용) — 000037-010 소유.
- **Conflicts With**: (None identified) — 000038-020 과 disjoint SKILL.md set.
- **Parallelizable After**: `000037-010-docs-language-resolution-reference`
- **Task Verify**:
  - `grep -q "language-resolution.md" claude-code/skills/ywc-create-pr/SKILL.md`
  - `grep -q "language-resolution.md" claude-code/skills/ywc-commit/SKILL.md`
