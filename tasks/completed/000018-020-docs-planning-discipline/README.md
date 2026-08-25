# 000018-020-docs-planning-discipline

## Purpose

planning 클러스터 skill에 Karpathy 원칙 1(복수 해석 제시)과 원칙 2(과설계 탐지)를 심는다. spec-validate는 과잉을 잡는 단순성 차원을, ywc-plan/ywc-spec-writer는 의도 모호성 시 복수 해석 제시 규율을 얻는다.

## Scope

- FR-2: `ywc-spec-validate/SKILL.md`에 Simplicity 검토 초점 + Rationalization 행.
- FR-3: `ywc-plan/SKILL.md`에 의도 모호성 Rationalization 행 + Step 1 모순-중단 1줄; `ywc-spec-writer/SKILL.md` non-negotiable rules에 Open Questions 양해석 기록 1줄.
- 사용자 표면 동작이 바뀌는 3개 skill의 README locale set 동기화(§A7).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §FR-2, §FR-3
- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §A7 (README-sync 필요 목록: spec-validate, ywc-plan, ywc-spec-writer 포함)
- `claude-code/skills/ywc-spec-validate/SKILL.md:23-24` — 4차원 표/Rationalization (보존)
- `claude-code/skills/ywc-plan/SKILL.md:29,135` — default-Medium(규모 전용, 보존)
- `claude-code/skills/ywc-spec-writer/SKILL.md:146,158,165` — non-negotiable rules / Open Questions

### Summary

spec-validate의 기존 4차원(completeness/consistency/feasibility/compatibility)과 advisor 메커니즘은 그대로 두고 Simplicity 검토 초점만 보강한다. plan/spec-writer의 default-Medium 규칙은 *규모* 모호성 전용이므로 변경하지 않고, *의도* 모호성에 대한 복수 해석 제시 규율을 별도로 추가한다.

### Out of Scope (from spec)

- spec-validate Phase 1 4-subagent fan-out 구조 변경 — Simplicity는 기존 차원에 접힘
- task-generator/code-gen의 단순성 처리 — 각각 000018-030/040 담당

## Dependencies

### Depends On

- `000018-010-docs-principles-foundation` — Assumption & Ambiguity / Goal-Driven 표준 원칙 이름

### Depended By

- `000019-010-infra-karpathy-validation` — 최종 검증(AC3/AC4)

## Key Files

- `claude-code/skills/ywc-spec-validate/SKILL.md` — Simplicity 차원
- `claude-code/skills/ywc-plan/SKILL.md` — 복수 해석 Rationalization + Step 1 줄
- `claude-code/skills/ywc-spec-writer/SKILL.md` — Open Questions 양해석 줄
- 위 3개 skill의 `README.md`/`README.ko.md`/`README.en.md`/`README.ja.md`

## Notes

- §A7: 세 skill 모두 사용자 표면 산출물에 영향 → README 동기화 필요.
- spec-writer의 Open Questions 기록은 사용자 표면 산출물(spec)에 영향하므로 README 포함.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-spec-validate/**`
- `claude-code/skills/ywc-plan/**`
- `claude-code/skills/ywc-spec-writer/**`

### Shared Surfaces

- `공유 SoT: principles.md` (읽기 전용 인용; 편집은 000018-010)

### Conflicts With

- (None identified) — 다른 Phase 000018 태스크와 disjoint Ownership

### Parallelizable After

- `000018-010-docs-principles-foundation`

### Task Verify

- `rg -n "Simplicity|over-engineer|speculative" claude-code/skills/ywc-spec-validate/SKILL.md`
- `rg -n "interpretation|두 해석|복수 해석" claude-code/skills/ywc-plan/SKILL.md`
- `rg -n "Open Questions" claude-code/skills/ywc-spec-writer/SKILL.md`
- `bash scripts/validate.sh`

## Out of Scope

- spec-validate에 5번째 병렬 subagent 추가(차원에 접어 비용 유지)
- default-Medium(규모) 규칙 수정
