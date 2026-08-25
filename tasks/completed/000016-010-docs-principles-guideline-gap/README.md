# 000016-010-docs-principles-guideline-gap

## Purpose
`codex/skills/references/principles.md`에 Karpathy guideline 검토에서 발견된 공통 gap을 반영한다. 이 task는 다른 skill/agent task가 공유할 용어와 원칙을 먼저 고정한다.

## Scope
- `Assumption & Ambiguity Discipline` section 추가
- `Goal-Driven Execution` section 추가
- 기존 Evidence, Scope, Failure discipline과 충돌하지 않도록 짧은 operational rule로 통합
- 새 `karpathy-*` skill을 만들지 않는 boundary 확인

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#fr-1-strengthen-shared-principles` — shared principles 요구사항
- `docs/ywc-plans/codex-karpathy-guideline-integration.md#acceptance-criteria` — AC1, AC2 검증 기준
- `codex/skills/references/principles.md` — 수정 대상 source of truth

### Summary
이 task는 Codex skill 전반에 적용되는 원칙 문서에 추측 금지, ambiguity 처리, goal-driven done 판단을 추가한다. 다른 task가 각 skill/agent에 세부 지침을 넣기 전에 shared vocabulary를 먼저 안정화한다. 문서는 manifesto가 아니라 기존 스타일에 맞는 짧은 rule set이어야 한다.

### Out of Scope (from spec)
- `ywc-code-gen` worker prompt 변경 — handled by `000016-020-docs-code-gen-worker-discipline`
- `ywc-task-generator` template 변경 — handled by `000016-030-docs-task-template-goal-verification`
- `ywc-skill-author` guidance 변경 — handled by `000016-040-docs-skill-author-future-proofing`
- `codex/agents/*.toml` 변경 — handled by `000016-050-docs-custom-agent-bounded-evidence`
- generated plugin sync/validation — handled by `000017-010-infra-codex-karpathy-validation`

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000016-020-docs-code-gen-worker-discipline` — shared assumption/scope wording를 worker prompt에 맞춰 반영
- `000016-030-docs-task-template-goal-verification` — goal-driven execution vocabulary를 task template에 맞춰 반영
- `000016-040-docs-skill-author-future-proofing` — Rationalization Defense authoring rule에 shared vocabulary 반영
- `000016-050-docs-custom-agent-bounded-evidence` — agent bounded-evidence wording 정렬
- `000017-010-infra-codex-karpathy-validation` — final sync/validation

## Key Files
- `codex/skills/references/principles.md` — shared Codex principles source

## Notes
- 기존 hierarchy를 교체하지 말고, 누락된 operational discipline만 추가한다.
- 외부 guideline 문장을 그대로 복사하지 않는다.
- 새 skill 또는 새 agent를 만들지 않는다.

## Parallel Execution Metadata

### Ownership
- `codex/skills/references/principles.md`

### Shared Surfaces
- Shared reference contract: `codex/skills/references/principles.md`

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n "Assumption|Ambiguity|Goal-Driven|NEEDS_CONTEXT|success criteria" codex/skills/references/principles.md`
- `test ! -d codex/skills/karpathy-guidelines`
- `test ! -d claude-code/skills/karpathy-guidelines`

## Out of Scope
- Editing any `codex/skills/ywc-*` skill body or prompt.
- Editing `codex/agents/*.toml`.
- Editing generated plugin package manually.
