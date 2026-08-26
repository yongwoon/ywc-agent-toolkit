# 000056-010-refactor-skill-author-deletion-test — Manual Test Plan

절차와 rubric은 산문이므로 단위 테스트가 없다. 대신 **스모크 후보 1개**로 절차를 끝까지 걸어보고, 각 단계의 관찰 가능한 계약을 확인한다. 이 test는 라벨을 report에 기록하지 않는다 — 그것은 `000057-020`의 일이다.

## T1 — blind dispatch가 실제로 blind한가

**Steps**
1. 임의의 skill에서 후보 1개를 골라 `build-variant.sh`로 variant를 만든다.
2. 절차대로 6개 subagent를 dispatch한다.
3. 6개 dispatch prompt를 전부 덤프해 읽는다.

**Expected Result**
- 어떤 prompt에도 "deletion test", "variant", "original", "deleted", "Rationalization Defense", authoring rule(A1–A14) 언급이 없다.
- 6개 prompt가 시나리오 텍스트에서 서로 구별되지 않는다 (body만 다르다).
- 각 subagent가 artifact **경로**를 반환하고 artifact 본문을 반환하지 않는다.

## T2 — 동등성 rubric이 양방향으로 작동한다

**Steps**
1. 표현만 다르고 행동이 같은 두 출력을 rubric으로 판정한다.
2. 파일 하나를 더 건드리거나 게이트 하나를 덜 강제한 두 출력을 rubric으로 판정한다.

**Expected Result**
- 1번은 **동등**(불일치 아님).
- 2번은 **불일치**.
- rubric이 두 판정 각각에 대해 인용 가능한 근거 문장을 갖는다.

## T3 — 문턱 T가 꼬리 경계다 (평균이 아니다)

**Steps**
1. `floor_rate`를 0.00 / 0.05 / 0.10 / 0.15 / 0.20 / 0.25로 넣고 문서화된 `T` 계산을 수행한다.

**Expected Result**
- `T`가 각각 **0 / 2 / 3 / 3 / 4 / 4**를 낸다 (사양 AC5 표와 일치).
- `floor(floor_rate × 9)`(평균 공식)를 썼다면 0/0/0/1/1/2가 나온다 — 이 값이 나오면 **실패**다.

## T4 — validity ceiling이 run을 멈춘다

**Steps**
1. `floor_rate = 0.30`을 가정하고 절차를 따라간다.

**Expected Result**
- run이 `INCONCLUSIVE`로 판정된다.
- 80개 후보 전부 `indeterminate`가 되고 어떤 후보도 `inert`/`load-bearing`을 받지 못한다.
- 증거 게이트(AC9)가 통과 불가로 표시된다.
- 절차 어디에도 "ceiling을 낮춰서 통과시킨다"는 우회로가 없다.

## T5 — 층화 추출 프레임이 실현 가능하다

**Steps**
1. `enumerate-rd-rows.sh`를 46개 skill 전체에 돌려 Stratum A(위치 1–4)와 B(위치 5+) pool 크기를 센다.

**Expected Result**
- Stratum A pool = **184행**, Stratum B pool = **235행**.
- 46개 skill 전부가 각 stratum에 최소 1행을 갖는다 (즉 skill 당 1행 제약으로 40+40 추출이 가능하다).

## T6 — keyed resume가 중복을 만들지 않는다

**Steps**
1. report에 후보 key 몇 개를 미리 기록해둔다.
2. 절차의 resume 검사를 그 상태에서 실행한다.

**Expected Result**
- 이미 기록된 key는 **재dispatch되지 않는다**.
- 중복 report 행이 **0개**다.
