# yw-000061-010-docs-fastify-scaffold

## Purpose
ywc-project-scaffold JavaScript 참조에 Fastify Small/Medium/Large 구조를 추가한다 (Phase D).

## Scope
- `references/javascript.md` 의 Express.js (`:483`) 뒤에 Fastify 3 단계 섹션 + Key Points + TOC 링크 (FR-D1)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — `## Scope` Phase D, FR-D1, AC-9
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #251 의 claude-code 판 내용을 그대로 반영하고, 이 파일의 기존 heading 형식 (`### <Framework> <Size>`) 과 TOC 에 맞춘다.

### Out of Scope (from spec)
- (None — spec has no deferred items)

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- `yw-000060-010-docs-pr-review-impact` — Phase C 머지 base

### Depended By
- `yw-000062-010-docs-trigger-boundary-descriptions` — Phase D 머지 base
- `yw-000062-020-docs-model-hint-routing` — Phase D 머지 base
- `yw-000062-030-docs-ac-baseline` — Phase D 머지 base

## Key Files
- `claude-code/skills/ywc-project-scaffold/references/javascript.md`

## Notes
- Phase D 는 내용상 독립이지만 spec 의 A→E 순서 필수 규칙에 따라 직렬화한다.
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: haiku — M2 (Ownership 전부 `*.md`, category docs; Depended By 3 개이나 Owned Interface 없음으로 M1 불일치)

### Ownership
- `claude-code/skills/ywc-project-scaffold/references/javascript.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- (None identified)

### Conflicts With
- (None identified — Phase hard gate)

### Parallelizable After
- `yw-000060-010-docs-pr-review-impact`

### Task Verify
- `grep -c "^### Fastify" claude-code/skills/ywc-project-scaffold/references/javascript.md` → 3 + TOC 링크 존재 (AC-9)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- codex 측 javascript.md
