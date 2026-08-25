# 000058-020-docs-a7-nogo-closure

> **조건부 task.** `000057-020`의 증거 게이트(AC9)가 **실패**했거나 run이 `INCONCLUSIVE`인 경우에만 실행한다. GO면 이 task 대신 `000058-010`을 실행한다.

## Purpose

null 결과를 **정당하고 내구성 있는 결론으로 확정 기록**하고 FR-4를 미출시로 닫는다. 사양은 이것을 실패한 run이 아니라고 명시한다 — 게이트가 실패하면 corpus는 *load-bearing임이 입증된 것*이고, 이는 inert임이 입증된 것과 똑같이 내구성 있는 결과다.

이 task가 존재하는 이유: 이 경로가 없으면 NO-GO 결과가 아무 곳에도 확정 기록되지 않고, AC13의 phase-말 검증이 돌지 않으며, 다음 사람이 몇 달 뒤 같은 480 dispatch를 다시 돌리게 된다.

## Scope

- report에 최종 결론을 확정 기록한다: **"quota가 padding을 만든다는 것이 입증되지 않았다"** (게이트 실패) 또는 **"harness가 측정되었을 뿐 corpus가 측정되지 않았다"** (`INCONCLUSIVE`).
- FR-4를 **미출시**로 닫는다. 다섯 사본 중 **어느 것도 건드리지 않는다** (AC10: "게이트가 실패하면 다섯 중 아무것도 건드리지 않는다").
- `INCONCLUSIVE`인 경우, 재실행에 필요한 harness 분산 축소 방안(더 제약된 시나리오, 낮은 sampling temperature)을 기록한다.
- AC13의 3종 게이트를 돌려 phase를 닫는다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-pruning-pilot.md#fr-4-conditionally-retire-the-a7-quota` — "If the gate fails, **nothing here ships**"
- `docs/ywc-plans/skill-pruning-pilot.md` AC9 (null 결과의 지위), AC5a (`INCONCLUSIVE`), AC10 (게이트 실패 시 다섯 사본 불변), AC13
- `docs/ywc-plans/skill-pruning-pilot.md#edge-cases` — "AC9's gate fails" 항목
- `docs/ywc-plans/prune-report-rationalization-defense.md` (`000057-020` 산출물)

### Summary

사양의 Edge Case가 이 경로를 정확히 규정한다: **AC9의 게이트가 실패하면 FR-4는 출시되지 않고, FR-5의 검사는 advisory-only로만 출시되며, 어떤 script도 건드리지 않는다.** 그리고 이 spec은 여전히 report, 두 script, FR-6의 A8 수정, FR-7의 README 동기화를 **전달한다** — 즉 spec 전체가 실패한 것이 아니다.

`INCONCLUSIVE`와 게이트 실패는 다르다:
- **게이트 실패** (`VALID`이지만 `p ≥ 0.05` 또는 B의 inert 비율이 A 이하): corpus에 대한 **결론이 나왔다** — quota가 padding을 만든다는 증거가 없다.
- **`INCONCLUSIVE`** (pooled `floor_rate > 0.25`): corpus에 대한 결론이 **나오지 않았다** — harness가 측정되었을 뿐이다. 재실행이 정당하다.

두 경우 모두 FR-4는 출시되지 않지만, report가 기록해야 할 문장은 다르다. 이 구분을 뭉개면 다음 사람이 "결론 없음"을 "quota는 문제없음"으로 오독한다.

### Out of Scope (from spec)

- **다섯 사본 중 어느 것도 수정하지 않는다** (AC10). A7 quota는 그대로 남는다.
- `INCONCLUSIVE`인 경우의 **재실행 자체** — 방안만 기록하고, 재실행은 새 승인 하에 `000057-020`을 다시 도는 것으로 처리한다.
- ceiling을 낮춰 run을 "성공"시키는 것 — 사양이 명시적으로 금지한다.

## Criticality

`normal` — 문서 전용. 코드도 CI 게이트도 건드리지 않는 것이 이 task의 요점이다.

## Dependencies

### Depends On

- `000057-020-test-pilot-dispatch-report` — NO-GO 또는 `INCONCLUSIVE` 판정이 이 task의 존재 조건이다.

### Depended By

- `000059-040-infra-invocation-tier-validator` — FR-5의 enforcement 모드가 **advisory**로 확정된다 (게이트가 통과하지 않았으므로).

## Key Files

- `docs/ywc-plans/prune-report-rationalization-defense.md` (결론 섹션 append)

## Notes

- **A7 quota를 "일단 완화해두자"는 유혹을 거부하라.** 증거가 없다는 것은 완화의 근거가 아니라 완화하지 않을 근거다. 사양의 원래 관찰: 46개 skill 중 **하한 아래는 0개이고 최솟값이 정확히 5** — 여유가 어디에도 없다. 증거 없이 하한을 내리면 다음 skill 저자가 그 여유를 padding으로 채운다.
- null 결과를 "실패"로 적지 마라. 사양의 표현을 쓴다: **"quota not shown to manufacture padding."**

## Out of Scope

- 코드·규칙·CI 변경 일체

## Parallel Execution Metadata

### Ownership

- `docs/ywc-plans/prune-report-rationalization-defense.md` — 결론 섹션만

### Shared Surfaces

- (없음 — 이 task는 report 외에 아무것도 쓰지 않는다.)

### Conflicts With

- `000058-010-infra-retire-a7-quota` — **상호 배타적.** 정확히 하나만 실행된다.

### Parallelizable After

- `000057-020-test-pilot-dispatch-report` (NO-GO 또는 INCONCLUSIVE 판정 포함)

### Task Verify

- report에 최종 결론이 확정 기록되어 있고, 게이트 실패와 `INCONCLUSIVE`가 **구별되어** 서술되어 있다
- AC10의 다섯 파일 어느 것도 변경되지 않았다
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (A7 게이트가 그대로 산다)
- report에 "ceiling을 낮춘다"는 서술이 없다
