# 000051-020-docs-discovery-skill-exploration-hooks

## Purpose
Discovery / planning 계열 skill에 Fable-inspired unknown surfacing hook를 연결한다. `ywc-brainstorm`, `ywc-plan`, `ywc-tech-research`, `ywc-onboard-repo`가 언제 `unknown-matrix.md`를 읽고 어떻게 결과를 output surface에 반영하는지 명시한다.

## Scope
- `ywc-brainstorm/SKILL.md` blind-spot pass hook
- `ywc-plan/SKILL.md` investigation / design-assumption hook
- `ywc-tech-research/SKILL.md` `Unknowns Surfaced` output section 추가
- `ywc-onboard-repo/SKILL.md` unknown-but-worth-verifying repository question surface 추가
- 위 4개 skill의 `agents/openai.yaml` sync
- 위 4개 skill의 locale README stale 여부 반영

## Spec Reference

### Primary Sources
- `docs/ywc-plans/fable-inspired-codex-exploration.md#functional-requirements` — FR2, FR3, FR4, FR5
- `docs/ywc-plans/fable-inspired-codex-exploration.md#iteration-1-amendments` — Unknown Matrix visibility, `Unknowns Surfaced` section placement, metadata/locale sync
- `codex/skills/references/unknown-matrix.md` — 새 shared discovery reference

### Summary
이 task는 discovery 계열 4개 skill에 exploration hook를 추가한다. 핵심은 speculative freedom을 높이는 것이 아니라, ambiguity가 implementation question으로 굳기 전에 blind spot을 체계적으로 surface하는 것이다. `ywc-tech-research`는 output shape까지 바꾸므로 report 구조와 status semantics를 함께 맞춘다.

### Out of Scope (from spec)
- code/executor 계열 implementation-notes wiring — `000051-030-docs-execution-skill-implementation-notes`
- `ywc-skill-author` future rule update — `000051-040-docs-skill-author-exploration-rules`
- plugin sync / 전체 validation — `000052-010-infra-fable-exploration-validation`

## Dependencies

### Depends On
- `000051-010-docs-shared-exploration-references` — `unknown-matrix.md` reference가 먼저 존재해야 함

### Depended By
- `000052-010-infra-fable-exploration-validation` — discovery skill edits와 metadata/readme sync 결과를 최종 검증함

## Key Files
- `codex/skills/ywc-brainstorm/SKILL.md`
- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-tech-research/SKILL.md`
- `codex/skills/ywc-onboard-repo/SKILL.md`
- `codex/skills/ywc-brainstorm/agents/openai.yaml`
- `codex/skills/ywc-plan/agents/openai.yaml`
- `codex/skills/ywc-tech-research/agents/openai.yaml`
- `codex/skills/ywc-onboard-repo/agents/openai.yaml`
- 해당 skill들의 README locale files

## Notes
- `ywc-brainstorm`는 Unknown Matrix 용어를 기본적으로 internal guidance로 유지한다.
- `ywc-tech-research`는 `### Unknowns Surfaced`를 `Project-Specific Considerations`와 `References` 사이에 둔다.
- README locale은 behavior/usage text가 바뀐 skill만 수정한다. 존재하는 `README.zh.md` / `README.es.md`도 동기화 대상이다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-brainstorm/**`
- `codex/skills/ywc-plan/**`
- `codex/skills/ywc-tech-research/**`
- `codex/skills/ywc-onboard-repo/**`

### Shared Surfaces
- `codex/skills/references/unknown-matrix.md`
- Skill chip metadata semantics in `agents/openai.yaml`
- Locale README behavior descriptions

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000051-010-docs-shared-exploration-references`

### Task Verify
- `rg -n "unknown-matrix|Unknowns Surfaced|blind-spot|unknown but high-value" codex/skills/ywc-brainstorm codex/skills/ywc-plan codex/skills/ywc-tech-research codex/skills/ywc-onboard-repo`

## Out of Scope
- `ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-skill-author` edits
- shared reference 신규 작성
- plugin package sync
