# 000057-020-test-pilot-dispatch-report — Implementation Checklist

## Prerequisites

- [ ] `000057-010-test-pilot-sample-frame`이 완료·merge되었다.
- [ ] report header에 부모 audit SHA와 80개 후보 목록, 후보별 시나리오가 이미 기록되어 있다.
- [ ] `deletion-test-rubric.md`를 읽었다.

## Allowed Edit Scope

- [ ] `docs/ywc-plans/prune-report-rationalization-defense.md` 에 **append만** 한다. 기존 header/후보 목록을 수정하지 않는다.
- [ ] `claude-code/skills/**`는 읽기 전용. variant는 `build-variant.sh`가 temp path에만 쓴다.

## Stop Conditions

- [ ] variant가 불일치했다는 이유로 후보를 재실행하고 싶어지면 **멈춘다** — 금지 사항이다.
- [ ] 라벨을 원하는 쪽으로 옮기려고 표본을 바꾸고 싶어지면 멈춘다.
- [ ] pooled `floor_rate > 0.25`가 나오면 **라벨을 하나도 붙이지 말고** `INCONCLUSIVE`로 report를 닫는다. ceiling을 낮추지 않는다.
- [ ] subagent가 artifact 본문을 반환하기 시작하면 멈추고 §3.5 계약을 복구한다.

## Implementation Steps

- [ ] 세션마다 report를 읽어 이미 기록된 후보 key를 수집하고, 그 key는 **재dispatch하지 않는다** (AC7).
- [ ] 미처리 후보에 대해 `build-variant.sh`로 variant를 만든다 (손 편집 금지).
- [ ] 후보당 **blind 3+3 dispatch**: 원본 body 3개, 삭제 body 3개, 동일 시나리오. 어느 subagent에게도 variant 정체·deletion test 존재·authoring rule을 알리지 않는다. 각자 artifact **경로만** 반환.
- [ ] 세션당 dispatch 상한 **60**을 지킨다 (후보 10개/세션). 세션 경계는 resume point다.
- [ ] 후보당 비교 수행: within-variant 6쌍(원본 3 + 삭제 3), cross-variant 9쌍(3×3). 동등성은 rubric이 판정한다.
- [ ] 후보 행을 report에 append: 6개 artifact 경로, within 불일치(0–6), cross 불일치(0–9), 시나리오, stratum, (라벨은 아직 비워둔다).
- [ ] **480개 within-variant 비교가 모두 모인 뒤** pooled floor를 계산한다: `floor_rate = (전체 within 불일치 합) / (6 × 80)`.
- [ ] **ceiling 검사** (AC5a): `floor_rate > 0.25` → run은 `INCONCLUSIVE`. 80개 전부 `indeterminate`, report에 "측정된 것은 corpus가 아니라 harness"라고 명시, 증거 게이트 통과 불가로 닫는다. 여기서 종료한다.
- [ ] `VALID`인 경우 문턱 계산: `T` = `X ~ Binomial(9, floor_rate)`에 대해 `P(X ≤ t) ≥ 0.95`인 최소 `t`. **평균 공식(`floor(floor_rate × 9)`)을 쓰지 않는다.**
- [ ] 라벨 부여: cross ≤ `T` → `inert` (경계 포함), > `T` → `load-bearing`, 6개 run 중 BLOCKED/NEEDS_CONTEXT 있음 → `indeterminate`.
- [ ] per-stratum inert 비율과 **two-sided Fisher exact p-value**를 계산해 기록한다.
- [ ] 증거 게이트 판정 기록 (AC9): `p < 0.05` **AND** Stratum B의 inert 비율 > Stratum A. 통과면 GO, 아니면 NO-GO.
- [ ] null 결과인 경우 "quota가 padding을 만든다는 것이 입증되지 않았다"로 명시 기록한다 — 실패한 run이 아니다.

## Task Verify

- [ ] report의 라벨 행 == 80, 각 행에 artifact 경로 **정확히 6개**
- [ ] pooled `floor_rate`와 ceiling 판정(`VALID`/`INCONCLUSIVE`)이 기록되어 있다
- [ ] `VALID`인 경우 `T`가 사양 AC5 표(0.00→0, 0.05→2, 0.10→3, 0.15→3, 0.20→4, 0.25→4)와 일치하는 방식으로 계산되었다
- [ ] `VALID`인 경우 per-stratum inert 비율과 Fisher exact p-value, GO/NO-GO 판정이 기록되어 있다
- [ ] run 중단 후 재시작 → 재dispatch 0건, 중복 행 0건
- [ ] 라벨은 있는데 artifact 경로가 6개 미만인 행이 **0개**

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (AC13).
- [ ] `git diff --name-only`가 report 외의 파일을 보이지 않는다 (AC2).
- [ ] report가 `inert` 라벨을 삭제 허가로 취급하는 문장을 단 하나도 담고 있지 않다.
