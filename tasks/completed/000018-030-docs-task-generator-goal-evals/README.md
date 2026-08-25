# 000018-030-docs-task-generator-goal-evals

## Purpose

`ywc-task-generator`가 검증 가능한 성공 기준을 강제하도록 보강하고(Karpathy 원칙 4 후반부), 그 출력 변경을 객관적 회귀로 잡는 eval을 추가한다.

## Scope

- FR-4: Task Verify가 태스크별 검증 가능 단언을 갖도록 Final Validation 체크 + Rationalization 행; per-task Acceptance Criteria 하위절; Notes에 Assumptions 필드.
- FR-12: `ywc-task-generator/evals/evals.json`에 위 산출(verifiable Task Verify + AC + Assumptions)을 단언하는 회귀 케이스 ≥1개. 불가 시 구현 노트에 사유.
- README locale set 동기화(§A7 — task-generator 출력 형식 변경).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §FR-4
- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §Iteration 1 Amendments §A2 (FR-12 + AC16)
- `claude-code/skills/ywc-task-generator/SKILL.md:289,309,322-324,379` — Task Verify / Final Validation
- `claude-code/skills/ywc-task-generator/evals/` — 기존 eval 구조(편집 전 형식 확인)
- `docs/ywc-plans/codex-karpathy-guideline-integration.md` FR-3/FR-6 — 선례

### Summary

Task Verify가 "전역 게이트만은 피하라"고만 하던 것을, 태스크 동작이 없으면 실패하는 태스크별 단언을 *강제*하도록 올린다. per-task Acceptance Criteria(When/does/observable-as)와 분해 시 Assumptions 기록을 추가한다. 이 출력 변경을 eval 회귀로 고정한다.

### Out of Scope (from spec)

- task.md.template의 간결 구조 해체 — 필드만 추가
- ywc-sequential-executor evals(FR-12 대칭 노트)는 000018-050 담당

## Dependencies

### Depends On

- `000018-010-docs-principles-foundation` — Goal-Driven Execution 표준 원칙 이름

### Depended By

- `000019-010-infra-karpathy-validation` — 최종 검증(AC5/AC16)

## Key Files

- `claude-code/skills/ywc-task-generator/SKILL.md` — Final Validation 체크 + Rationalization + AC 하위절 + Assumptions
- `claude-code/skills/ywc-task-generator/evals/evals.json` — 회귀 케이스
- `claude-code/skills/ywc-task-generator/README.md`/`README.ko.md`/`README.en.md`/`README.ja.md`

## Notes

- evals.json 편집 전 기존 케이스 형식을 반드시 읽고 따른다.
- 객관적 eval이 불가하면 구현 노트에 사유 기록(AC16 충족).

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-task-generator/**`

### Shared Surfaces

- `공유 SoT: principles.md` (읽기 전용 인용)

### Conflicts With

- (None identified)

### Parallelizable After

- `000018-010-docs-principles-foundation`

### Task Verify

- `rg -n "Acceptance Criteria|Assumptions|verifiable" claude-code/skills/ywc-task-generator/SKILL.md`
- `rg -n "Task Verify|Acceptance|Assumptions" claude-code/skills/ywc-task-generator/evals/evals.json` 또는 구현 노트의 불가 사유
- `bash scripts/validate.sh`

## Out of Scope

- 다른 skill의 eval 추가
- task 생성 알고리즘 자체 변경
