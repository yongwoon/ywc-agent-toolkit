# 000057-020-test-pilot-dispatch-report — Manual Test Plan

## T1 — resume가 실제로 중복을 만들지 않는다 (AC7)

**Steps**
1. 첫 세션에서 후보 10개를 처리해 report에 기록한다.
2. run을 강제로 중단한다.
3. 재시작한다.

**Expected Result**
- 이미 기록된 10개 key가 **재dispatch되지 않는다** (dispatch 로그로 확인).
- report에 중복 행이 **0개**.
- 후보 목록(표본 우주)이 재추출되지 않고 `000057-010`이 쓴 것을 그대로 읽는다.

## T2 — 세션 상한이 지켜진다

**Steps**
1. 한 세션에서 dispatch 수를 센다.

**Expected Result**
- 세션당 dispatch ≤ **60** (후보 10개 × 6).
- 전체 run이 약 8세션에 걸친다.

## T3 — blind가 유지된다

**Steps**
1. 임의의 세션에서 dispatch prompt 6개를 덤프한다.

**Expected Result**
- variant 정체, deletion test, authoring rule 언급이 **없다**.
- 6개 prompt가 body를 제외하면 동일하다.
- 각 subagent가 artifact **경로**만 반환한다.

## T4 — 계산 순서 (floor → ceiling → label)

**Steps**
1. 라벨이 report에 처음 나타나는 시점을 확인한다.

**Expected Result**
- 480개 within 비교가 모두 모이고 `floor_rate`가 계산되고 ceiling이 판정된 **뒤에** 첫 라벨이 나타난다.
- ceiling 판정 이전에 붙은 라벨이 **0개**.

## T5 — INCONCLUSIVE 경로 (AC5a)

**Steps**
1. `floor_rate > 0.25`가 실제로 나온 경우(또는 가상 시나리오로) report 종결 절차를 따라간다.

**Expected Result**
- 80개 후보 전부 `indeterminate`.
- `inert` / `load-bearing` 라벨이 **0개**.
- report가 "측정된 것은 corpus가 아니라 harness"임을 명시한다.
- 증거 게이트가 통과 불가로 닫힌다 → `000058-020` (NO-GO) 경로로 간다.
- ceiling을 0.25보다 높게 조정한 흔적이 **없다**.

## T6 — 증거 게이트 (AC9)

**Steps**
1. per-stratum inert 비율과 Fisher exact p-value를 확인한다.

**Expected Result**
- GO 판정은 `p < 0.05` **AND** Stratum B inert 비율 > Stratum A일 때만 나온다.
- 둘 중 하나라도 실패하면 NO-GO이며, report가 그것을 "quota가 padding을 만든다는 것이 입증되지 않았다"로 기록한다 (실패한 run이 아님).

## T7 — 아무것도 삭제되지 않았다 (AC2)

**Steps**
1. `git diff <base>..HEAD -- 'claude-code/skills/ywc-*/SKILL.md'`

**Expected Result**
- Rationalization Defense 섹션 안쪽에 떨어지는 `^-` 삭제 줄이 **0개**.
- 실제로는 `claude-code/` 아래 diff 자체가 비어 있어야 한다.
