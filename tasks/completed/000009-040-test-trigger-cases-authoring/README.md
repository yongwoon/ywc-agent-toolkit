# 000009-040-test-trigger-cases-authoring

## Purpose
활성화 정확도(S1 30% / A2 25%)의 측정 가능성을 확보하기 위해, 50개 항목(38 skills + 12 agents) 전체에 대한 트리거 케이스를 작성한다(FR1a). 항목별 positive ≥3, collision ≥2.

## Scope
- `evals/trigger-cases.json` 를 항목별 최소 케이스(≥3 pos, ≥2 collision)로 확장, 페어형 collision 규약 준수
- 충돌 위험 큰 클러스터부터: reviewer 계열, executor 계열, PR 라이프사이클(commit/create-pr/finish-branch/handle-pr-reviews)
- 클러스터별 ≥1 negative

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-eval-improvements.md` — FR1a, Data Model(trigger-cases.json), Amendment A5(skills+agents 단일 파일)
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` — 케이스 분류·페어 규약
### Summary
같은 프롬프트가 owner 에는 positive, 인접 형제에는 collision+impostor 로 들어가는 페어 규약을 따른다. `expected`/`impostor` 는 skill 또는 agent 실명을 가리킬 수 있다(교차 루트).
### Out of Scope (from spec)
- 게이트 로직(소유 -010), 반자동 생성 워크플로(채택 안 함)

## Dependencies
### Depends On
- `000009-010-domain-eval-scorer-logic` — `signals.coverage` 게이트가 충족 여부를 검증
### Depended By
- `000009-050-infra-final-verification`

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (대폭 확장)

## Notes
- 커버리지는 `signals` 에만 영향 → `history.mechanical.json` 기준선 불변(재기준선 불필요).
- 50항목 전수 = 약 250+ 케이스. 클러스터 순서로 작성하되 누락 0 을 목표.

## Out of Scope
- 코드/문서/테스트 파일

## Parallel Execution Metadata
- **Ownership:** `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- **Shared Surfaces:** trigger-cases.json 스키마(-010 게이트가 소비)
- **Conflicts With:** (None identified)
- **Parallelizable After:** `000009-010` 머지 후 020·030 과 병렬 가능
- **Task Verify:** `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` 의 커버리지 요약이 "0 items below minimum"
