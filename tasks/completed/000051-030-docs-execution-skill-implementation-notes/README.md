# 000051-030-docs-execution-skill-implementation-notes

## Purpose
Code generation / executor 계열 skill에 `implementation notes` convention을 연결한다. 구현 중 드러난 non-obvious decision이 기존 completion/report surface에 남도록 `ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`를 정렬한다.

## Scope
- `ywc-code-gen/SKILL.md` 및 필요 시 `prompts/implementer-base.md` 수정
- `ywc-sequential-executor/SKILL.md` 수정
- `ywc-parallel-executor/SKILL.md` 수정
- 위 3개 skill의 `agents/openai.yaml` sync
- 위 3개 skill의 locale README stale 여부 반영
- executor 두 개의 500-line cap 유지

## Spec Reference

### Primary Sources
- `docs/ywc-plans/fable-inspired-codex-exploration.md#functional-requirements` — FR6, FR7, FR8
- `docs/ywc-plans/fable-inspired-codex-exploration.md#iteration-1-amendments` — implementation-notes canonical surface, executor 500-line-cap safety, metadata/locale sync
- `codex/skills/references/implementation-notes.md` — shared convention definition

### Summary
이 task는 implementation-time decision capture를 code/executor 계열에 붙인다. 중요한 제약은 새 artifact를 만들지 않고 기존 completion/report surface를 재사용하는 것, 그리고 `ywc-sequential-executor` / `ywc-parallel-executor`가 500줄 상한을 넘지 않는 것이다. 따라서 append-only 문구 추가보다 no-net-growth replacement 또는 static-content extraction이 우선이다.

### Out of Scope (from spec)
- discovery/planning 계열 unknown-surfacing hook — `000051-020-docs-discovery-skill-exploration-hooks`
- `ywc-skill-author` future rule 정리 — `000051-040-docs-skill-author-exploration-rules`
- repository-wide validation / plugin sync — `000052-010-infra-fable-exploration-validation`

## Dependencies

### Depends On
- `000051-010-docs-shared-exploration-references` — `implementation-notes.md` reference가 먼저 존재해야 함

### Depended By
- `000052-010-infra-fable-exploration-validation` — execution skill edits, metadata sync, line-cap safety를 최종 검증함

## Key Files
- `codex/skills/ywc-code-gen/SKILL.md`
- `codex/skills/ywc-code-gen/prompts/implementer-base.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- 각 skill의 `agents/openai.yaml`
- 각 skill의 README locale files

## Notes
- `ywc-code-gen`은 `Implementation Notes`를 final output section으로 추가하는 편이 가장 자연스럽다.
- executor 둘은 새 file/log를 만들지 않고 existing completion report / per-task summary surface에 note를 싣는다.
- line-count check는 task verify에 반드시 포함한다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-code-gen/**`
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`

### Shared Surfaces
- `codex/skills/references/implementation-notes.md`
- Executor output/report vocabulary
- `agents/openai.yaml` skill chip metadata

### Conflicts With
- `(None identified)`

### Parallelizable After
- `000051-010-docs-shared-exploration-references`

### Task Verify
- `rg -n "Implementation Notes|implementation-notes" codex/skills/ywc-code-gen codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
- `wc -l codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`

## Out of Scope
- discovery/planning skill wiring
- `ywc-skill-author` rule changes
- plugin sync / final validation task
