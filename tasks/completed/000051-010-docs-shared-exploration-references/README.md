# 000051-010-docs-shared-exploration-references

## Purpose
Fable-inspired exploration 규칙의 공통 기반을 추가한다. `Unknown Matrix`와 `Implementation Notes`를 shared reference로 정의해 이후 skill별 wiring이 중복 없이 같은 의미를 참조하도록 만든다.

## Scope
- `codex/skills/references/unknown-matrix.md` 신규 작성
- `codex/skills/references/implementation-notes.md` 신규 작성
- 두 reference가 기존 evidence-first / scope discipline과 충돌하지 않도록 공용 원칙에 맞춰 서술

## Spec Reference

### Primary Sources
- `docs/ywc-plans/fable-inspired-codex-exploration.md#functional-requirements` — FR1, FR6의 공통 reference 요구사항
- `docs/ywc-plans/fable-inspired-codex-exploration.md#iteration-1-amendments` — implementation-notes surface와 operative decision

### Summary
이 task는 후속 skill 수정의 기반이 되는 shared reference 2개를 만든다. 하나는 discovery/planning 단계의 blind-spot surfacing 규칙을 담고, 다른 하나는 implementation 과정에서 기록해야 할 non-obvious decision의 범위를 정의한다. 이후 skill들은 이 문서를 링크만 하고 의미를 재정의하지 않는다.

### Out of Scope (from spec)
- 개별 skill의 workflow hook 추가 — 후속 task에서 처리
- `agents/openai.yaml` sync — 후속 task에서 각 skill 변경과 함께 처리
- plugin sync / 전체 validation — 후속 infra task에서 처리

## Dependencies

### Depends On
- (None — if this is a root task)

### Depended By
- `000051-020-docs-discovery-skill-exploration-hooks` — discovery 계열 skill이 참조할 shared reference가 필요함
- `000051-030-docs-execution-skill-implementation-notes` — code/executor 계열 skill이 참조할 shared reference가 필요함
- `000051-040-docs-skill-author-exploration-rules` — skill-author가 future rule에서 참조할 shared guidance가 필요함

## Key Files
- `codex/skills/references/unknown-matrix.md` — discovery/planning blind-spot surfacing reference
- `codex/skills/references/implementation-notes.md` — implementation-time decision capture reference

## Notes
- `unknown-matrix.md`는 imagination을 허용하는 문서가 아니라 unknown-surfacing 절차를 operational하게 요약해야 한다.
- `implementation-notes.md`는 새 artifact를 강제하지 않고, 기존 completion/report surface에 붙이는 경량 규칙이어야 한다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/references/unknown-matrix.md`
- `codex/skills/references/implementation-notes.md`

### Shared Surfaces
- `codex/skills/references/**` shared bundle guidance
- Exploration / implementation-notes terminology reused by downstream skills

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n "Known Knowns|Unknown Unknowns|Implementation Notes|unexpected constraints|rejected alternatives" codex/skills/references/unknown-matrix.md codex/skills/references/implementation-notes.md`

## Out of Scope
- 개별 skill의 `SKILL.md`, `agents/openai.yaml`, README locale 수정
- validation command / plugin sync 변경
