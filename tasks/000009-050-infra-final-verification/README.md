# 000009-050-infra-final-verification

## Purpose
전체 변경 머지 후 교차 검증: 50항목 무오류 채점, A5 전원 5, 커버리지 0 미달, CI 회귀 없음, validate.sh 통과(FR12 검증 부분, AC14).

## Scope
- `score.py --target all` / `--ci` / `test_score.py` / `validate.sh` / markdownlint 전 구동
- `history.mechanical.json` diff 가 A5 4→5(하락 없음)로 한정됨을 확인

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-eval-improvements.md` — FR12, AC14, Amendment A3
### Summary
읽기 검증 중심. 기준선 재생성은 -010 에서 이미 원자적으로 완료되었으므로, 본 태스크는 안정성(재실행 시 무회귀)을 확인한다.
### Out of Scope (from spec)
- 신규 scorecard 등급화 산출(검증 목적의 재구동만)

## Dependencies
### Depends On
- `000009-010-domain-eval-scorer-logic`
- `000009-020-test-eval-scorer-unit-tests`
- `000009-030-docs-rubric-skill-alignment`
- `000009-040-test-trigger-cases-authoring`
### Depended By
- (없음)

## Key Files
- (소스 수정 없음 — 검증 전용)

## Notes
- `--ci` 재구동이 무변경이어야 함(이미 재기준선됨). 변경 발생 시 -010 의 재기준선 누락 신호.

## Out of Scope
- 모든 소스/문서/케이스 편집

## Parallel Execution Metadata
- **Ownership:** (검증 전용 — 소스 미편집)
- **Shared Surfaces:** (없음)
- **Conflicts With:** (None identified)
- **Parallelizable After:** `000009-010`,`-020`,`-030`,`-040` 전부 머지 후
- **Task Verify:** 아래 Verification 전 항목 PASS
