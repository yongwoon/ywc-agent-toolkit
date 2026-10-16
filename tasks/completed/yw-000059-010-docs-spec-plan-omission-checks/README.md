# yw-000059-010-docs-spec-plan-omission-checks

## Purpose
spec 작성·검증·분해 단계에서 누락을 줄이기 위해 UI/Interaction Omission Check, Failure Modes, spec coverage 검증을 추가하고 spec-ready 의 Suggestion 확인 질문을 자동 1회 pass 로 바꾼다 (Phase B).

## Scope
- `ywc-spec-validate` UI/Interaction Omission Check + `references/ui-qa-lenses.md` 신규 (FR-B1)
- `ywc-plan` + `spec-template.md` 의 `## Failure Modes`, `reuse`, prior-art seam (FR-B2)
- `ywc-task-generator` Step 11 Spec coverage / Interface consistency / Right-Sizing, `Unmapped spec items` 보고 (FR-B3)
- `ywc-spec-ready` Suggestion 자동 1회 pass (FR-B4)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — `## Scope` Phase B, FR-B1~FR-B4, AC-5/6/7/12(B3)/14, FM-4
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #257/#268/#266(spec-ready 부분) 을 반영한다. 이 저장소 task-generator 에는 preview 승인 단계와 `DONE_WITH_CONCERNS` 상태가 없으므로 미매핑 항목은 Step 11 결과 요약에 보고한다. spec-validate 의 UI check step 번호는 이 저장소 step 체계에 맞춘다.

### Out of Scope (from spec)
- #266 task-generator preview 부분 — 이 저장소에 해당 단계 없음
- #282 의 AC `Covers` 인용 / regression repair

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- `yw-000058-010-docs-named-agent-release` — Phase A 머지 base — `ywc-spec-validate/SKILL.md` 에 callout 이 이미 반영된 상태

### Depended By
- `yw-000060-010-docs-pr-review-impact` — Phase B 머지 base

## Key Files
- `claude-code/skills/ywc-spec-validate/SKILL.md`, `claude-code/skills/ywc-spec-validate/references/ui-qa-lenses.md` (신규)
- `claude-code/skills/ywc-plan/SKILL.md`, `claude-code/skills/ywc-plan/references/spec-template.md`
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-spec-ready/SKILL.md` (`:40`, `:85-95`, `:153`)

## Notes
- ywc-task-generator 는 463 줄 — 추가 후 500 줄 초과 시 상세는 `references/parallel-execution-metadata.md` 로 이동.
- spec-ready 의 자동 pass 후 새 Critical 이 생기면 handoff report 에 잔존 findings 를 표시 (FM-4).
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: haiku — M2 (Ownership 전부 `*.md`, category docs)

### Ownership
- `claude-code/skills/ywc-spec-validate/SKILL.md`
- `claude-code/skills/ywc-spec-validate/references/ui-qa-lenses.md`
- `claude-code/skills/ywc-plan/SKILL.md`
- `claude-code/skills/ywc-plan/references/spec-template.md`
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-task-generator/references/parallel-execution-metadata.md`
- `claude-code/skills/ywc-spec-ready/SKILL.md`

### Owned Interface
- `## Failure Modes` 표 형식 (`FM-n` / New path / Realistic failure / Covered by / User-visible?) — 이후 FR-E5 가 같은 template 위에서 작업

### Shared Surfaces
- `claude-code/skills/ywc-plan/references/spec-template.md` (Phase E `yw-000062-030` 과 공유)
- `claude-code/skills/ywc-spec-validate/SKILL.md` (Phase A, E 와 공유)

### Conflicts With
- (None identified — Phase hard gate)

### Parallelizable After
- `yw-000058-010-docs-named-agent-release`

### Task Verify
- `grep -c "Failure Modes" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-plan/references/spec-template.md` 각 ≥1 (AC-5)
- `grep -n "ask the user" claude-code/skills/ywc-spec-ready/SKILL.md` 에 Suggestion pass 질문 문구 없음 (AC-6)
- `test -f claude-code/skills/ywc-spec-validate/references/ui-qa-lenses.md` exit 0 + SKILL.md 상대 링크 (AC-7)
- `grep -c "Spec coverage\|Interface consistency" claude-code/skills/ywc-task-generator/SKILL.md` ≥1 (AC-12 B3)
- `grep -c "exactly one suggestion-focused" claude-code/skills/ywc-spec-ready/SKILL.md` ≥1 (AC-14)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- task-generator Model Hint (Phase E `yw-000062-020`)
- AC Baseline (Phase E `yw-000062-030`)
