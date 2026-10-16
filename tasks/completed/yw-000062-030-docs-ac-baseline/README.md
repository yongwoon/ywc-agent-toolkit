# yw-000062-030-docs-ac-baseline

## Purpose
명령을 포함한 AC 가 변경 전 tree 에서 실제로 실행된 결과 (Baseline) 를 기록하도록 해 검증 불가능한 AC 를 줄인다 (Phase E, FR-E5).

## Scope
- ywc-plan Pass B 행 + Validation 항목, spec-template AC 형식, spec-validate Feasibility 의 Baseline 확인 (FR-E5)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — FR-E5, AC-11
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #282 중 Baseline 부분만 반영한다. spec-validate 는 plain read command allowlist 만 재실행하고, Baseline 부재 시 `missing-ac-baseline` Suggestion 으로 보고한다. 쓰기 명령은 절대 실행하지 않는다.

### Out of Scope (from spec)
- #282 criticality / SCS profile / initializer / AC Covers / spec-ready regression repair

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- `yw-000061-010-docs-fastify-scaffold` — Phase D 머지 base (Phase B 의 Failure Modes 반영 template 포함)

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/ywc-plan/SKILL.md` (Pass B `:273-283`, Validation)
- `claude-code/skills/ywc-plan/references/spec-template.md` (AC 형식)
- `claude-code/skills/ywc-spec-validate/SKILL.md` (Phase 1 Feasibility 행, Review Dimensions)

## Notes
- Phase B 가 수정한 같은 파일 위에서 작업 — Phase B 머지 확인 후 착수.
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: haiku — M2 (Ownership 전부 `*.md`, category docs)

### Ownership
- `claude-code/skills/ywc-plan/SKILL.md`
- `claude-code/skills/ywc-plan/references/spec-template.md`
- `claude-code/skills/ywc-spec-validate/SKILL.md`

### Owned Interface
- AC Baseline 표기 `Baseline: <exit code> — <one-line output>` / `Baseline: unrunnable — <reason>`

### Shared Surfaces
- `claude-code/skills/ywc-spec-validate/SKILL.md` (Phase A, B 와 공유)

### Conflicts With
- (None identified — 같은 phase 의 010 / 020 과 파일 겹침 없음)

### Parallelizable After
- `yw-000061-010-docs-fastify-scaffold`

### Task Verify
- `grep -n "Baseline:" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-plan/references/spec-template.md claude-code/skills/ywc-spec-validate/SKILL.md` → Pass B 행, Validation, template AC 형식, Feasibility 에 각각 존재 (AC-11)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- spec-ready 쪽 Baseline 처리
