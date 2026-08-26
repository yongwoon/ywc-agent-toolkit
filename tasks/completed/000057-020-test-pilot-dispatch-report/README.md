# 000057-020-test-pilot-dispatch-report

## Purpose

파일럿을 실제로 돌린다. 고정된 80개 후보에 대해 blind 3+3 dispatch를 수행하고(총 **480 dispatch**), pooled noise floor와 validity ceiling을 계산하고, 라벨을 붙이고, per-stratum inert 비율과 Fisher exact p-value를 report에 확정 기록한다. 이 task의 산출물이 `000058`의 GO/NO-GO를 결정한다.

## Scope

- 80후보 × 6 dispatch = **480 dispatch**, 세션당 상한 **60** — run은 약 8세션에 걸치며 세션 경계는 restart가 아니라 resume point다.
- pooled noise floor 계산 (480 within-variant 비교) 및 ceiling 판정 (`VALID` / `INCONCLUSIVE`).
- 라벨 부여 (`inert` / `load-bearing` / `indeterminate`) + 후보당 artifact 경로 6개 기록.
- 증거 게이트 (AC9): per-stratum inert 비율 + two-sided Fisher exact p-value.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-3-run-the-pilot`
- `docs/ywc-plans/skill-pruning-pilot.md` AC5, AC5a, AC7, AC9
- `docs/ywc-plans/skill-pruning-pilot.md#fr-1-...` 5–8단계
- `claude-code/skills/ywc-skill-author/references/deletion-test-rubric.md` (`000056-010` 산출물)

### Summary

**계산 순서가 곧 안전장치다.** floor를 먼저 pooling하고, ceiling을 검사하고, **그 다음에** 라벨을 붙인다. 순서를 뒤집으면 `INCONCLUSIVE`인 run에서 이미 라벨이 나와버린다.

**Ceiling (AC5a)**: pooled `floor_rate > 0.25`면 run은 `INCONCLUSIVE`다. 80개 전부 `indeterminate`이 되고, report는 측정된 것이 corpus가 아니라 **harness**임을 명시한다. 올바른 대응은 harness 분산을 줄이고(더 제약된 시나리오, 낮은 sampling temperature) 재실행하는 것이다. **run을 "성공"시키려고 ceiling을 낮추지 마라.** 0.25인 이유는 오차 예산이 아니라 **분리 가능성(separability)** 이다 — 그 위에서는 귀무의 퍼짐이 0–9 범위 대부분을 덮어 어떤 현실적 load-bearing 신호도 잡음과 구별되지 않는다. 이것은 Type II(검정력) 한계이지 Type I 한계가 아니다.

**증거 게이트 (AC9)**: `p < 0.05` **그리고** Stratum B의 inert 비율이 Stratum A를 초과할 때만 통과. 검정력은 n=40/group, 진짜 35 포인트 격차에 대해 exact enumeration으로 **85.8 – 93.5 %**로 계산되어 있다. **null 결과는 실패한 run이 아니라 "quota가 padding을 만든다는 것이 입증되지 않았다"는 정당하고 내구성 있는 결과**이며, 그 경우 FR-4는 출시되지 않는다.

### Out of Scope (from spec)

- **어떤 행도 삭제하지 않는다** (AC2). 이 파일럿의 유일한 write는 report다.
- A7 quota 변경 (`000058-010`이 게이트 통과 시에만 수행)
- `invocation:` tier (000059 트랙)
- **불일치했다는 이유로 후보 재실행** — 금지. 그것은 테스트를 항상 통과하는 테스트로 바꾼다.

## Criticality

`normal` — 파일을 쓰는 대상이 report 하나뿐이다. 다만 **이 task의 산출물이 `000058-010`의 critical surface 변경을 정당화하는 유일한 증거**이므로, 통계 계산은 사양의 공식과 축자 대조해야 한다.

## Dependencies

### Depends On

- `000057-010-test-pilot-sample-frame` — 고정된 80후보 목록, 시나리오, 부모 audit SHA.
- `000056-010-refactor-skill-author-deletion-test` — dispatch 절차, rubric, floor/ceiling/labeling 규칙.

### Depended By

- `000058-010-infra-retire-a7-quota` — GO 경로. AC9 게이트 통과가 전제.
- `000058-020-docs-a7-nogo-closure` — NO-GO 경로. 게이트 실패 또는 `INCONCLUSIVE`가 전제.
- `000059-040-infra-invocation-tier-validator` — FR-5의 enforcement 모드(hard-fail vs advisory)가 이 게이트 결과에 달려 있다.

## Key Files

- `docs/ywc-plans/prune-report-rationalization-defense.md` (append-only)

## Notes

- **append-only, 단일 writer.** label 생산 단계는 skill을 가로질러 fan-out할 수 있지만 report에 쓰는 것은 orchestrator뿐이다. subagent는 artifact 경로만 반환한다 (§3.5) — 이것 없이는 80후보 sweep이 첫 wave에서 orchestrator context를 포화시킨다.
- **resume는 key 기반이다** (AC7). dispatch 전에 report가 이미 그 key를 가지고 있는지 확인하고 있으면 건너뛴다. run을 중간에 죽였다가 재시작해도 이미 기록된 후보는 **0개** 재dispatch되고 중복 행은 **0개**여야 한다.
- 라벨은 있는데 artifact 경로가 6개 미만인 행은 **결함**이다.
- floor가 0으로 나오면(모든 within-variant 쌍이 일치) 귀무가 degenerate하고 `T = 0`이며, *어떤* cross-variant 불일치든 `load-bearing`이 된다. 잡음 없는 harness에서는 관측된 차이가 모두 삭제에 귀속되므로 이것이 옳다.
- **`inert` 라벨은 집계 대조(AC9)를 위한 증거이지 그 행을 지워도 된다는 허가가 아니다.** 하류의 pruning 변경은 사람이 리뷰하며 건드리는 행마다 재검증해야 한다.

## Out of Scope

- skill 파일 편집
- 규칙 변경

## Parallel Execution Metadata

### Ownership

- `docs/ywc-plans/prune-report-rationalization-defense.md` (append-only, 단일 writer)

### Shared Surfaces

- `claude-code/skills/**` — read-only. variant는 temp path.

### Conflicts With

- `000057-010-test-pilot-sample-frame` — 같은 report 파일. 010 완료 후 시작.

### Parallelizable After

- `000057-010-test-pilot-sample-frame`

### Task Verify

- report에 80개 라벨 행이 있고, 각 행이 artifact 경로 **6개**, within 불일치 수(0–6), cross 불일치 수(0–9), 적용된 문턱 `T`, 시나리오, stratum(A/B), 라벨을 가진다
- pooled `floor_rate`와 ceiling 판정(`VALID`/`INCONCLUSIVE`)이 기록되어 있다
- `VALID`인 경우: per-stratum inert 비율과 two-sided Fisher exact p-value가 기록되어 있다
- run을 중단 후 재시작하면 재dispatch 0건, 중복 행 0건 (AC7)
- `git diff -- claude-code/` 가 비어 있다 (AC2)
