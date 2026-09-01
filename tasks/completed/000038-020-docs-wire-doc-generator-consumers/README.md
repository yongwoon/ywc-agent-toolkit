# 000038-020-docs-wire-doc-generator-consumers

## Purpose

문서 생성 consumer skill 3종(`ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`)이 각자의 bespoke 언어 추론 prose 대신 shared `references/language-resolution.md` 를 참조하도록 wiring 한다. user-global CLAUDE.md 까지 확인하고 project-over-user precedence 를 준수하며, 각 skill 의 기존 fallback(회귀 없음)을 보존한다.

## Scope

- **포함**: `ywc-task-generator` / `ywc-spec-writer` / `ywc-plan` 의 SKILL.md 에서 언어 해석 부분을 `> **Action required**: Read [language-resolution.md]` pointer 로 교체; user-global CLAUDE.md 확인 + precedence 준수; spec-writer 는 resolved code 를 `init-spec-structure.sh <lang>` 로 전달(A4).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/ywc-language-setup.md` — FR3(task-generator), FR4(spec-writer + A4 script 인자), FR5(plan), AC5, AC8, AC9, AC10, EC8, Amendment A4/A5.

### Summary
세 skill 은 현재 서로 다른 CLAUDE.md cue 를 서로 다른 default 로 읽는다(task-generator: "Language Policy section or Documentation Writing Guidelines", default `en`, SKILL.md:43,:129 / spec-writer: "declared primary documentation language", default `ko`, SKILL.md:90 / plan: Step 2 always-read "language policy", SKILL.md:98). 이를 canonical resolution pointer 로 통일하되, canonical `## Language Policy` 부재 시 기존 looser cue 를 hardcoded default 이전 fallback 으로 허용해 AC10 을 보존한다(A5). spec-writer 는 resolved code 를 `init-spec-structure.sh <lang>`(SKILL.md:108) 첫 위치 인자로 전달해야 scaffold 도 올바른 언어로 생성된다(A4).

### Out of Scope (from spec)
- `ywc-create-pr` / `ywc-commit` wiring(000038-030).
- resolution 규칙 정의(000037-010).

## Criticality
`normal`.

## Dependencies

### Depends On
- `000037-010-docs-language-resolution-reference` — pointer 대상 reference 존재.

### Depended By
- `000039-010-infra-validate-language-setup` — 최종 검증.

## Key Files
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-plan/SKILL.md`

## Notes
- **EC8/A2**: resolution 은 main skill context 에서 수행. task-generator 처럼 subagent fan-out 하는 skill 은 main-context 에서 1회 해석 후 resolved code 를 subagent payload 로 전달 — subagent 가 auto-load 에 의존하지 않도록 명시.
- 각 skill 의 기존 `references/language-policy.md`(locale writing 규칙)는 그대로 유지 — 이 task 는 "어떤 언어인가" 의 해석 경로만 통일한다.
- fallback 보존이 핵심: 정책 부재 시 task-generator 는 여전히 `en`+infer-then-ask, spec-writer 는 여전히 `ko`.

## Out of Scope
- git-artifact consumer, 새 skill, CLAUDE.md 문서화 섹션.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-task-generator/SKILL.md`, `claude-code/skills/ywc-spec-writer/SKILL.md`, `claude-code/skills/ywc-plan/SKILL.md`.
- **Shared Surfaces**: `references/language-resolution.md` 의 계약(읽기 전용 참조) — 000037-010 이 소유.
- **Conflicts With**: (None identified) — 000038-030 과 disjoint SKILL.md set.
- **Parallelizable After**: `000037-010-docs-language-resolution-reference`
- **Task Verify**:
  - `grep -q "language-resolution.md" claude-code/skills/ywc-task-generator/SKILL.md`
  - `grep -q "language-resolution.md" claude-code/skills/ywc-spec-writer/SKILL.md`
  - `grep -q "language-resolution.md" claude-code/skills/ywc-plan/SKILL.md`
  - `grep -q "init-spec-structure.sh" claude-code/skills/ywc-spec-writer/SKILL.md` (resolved lang 전달 문맥 유지 확인)
