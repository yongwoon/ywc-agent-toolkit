# 000078-010-docs-impl-review-bounded-payload-noninteractive — Manual Test Plan

spec의 NFR Verification/Testability는 이 change set에 자동 테스트 harness가 없음을 명시한다. 구조적 항목은 `task.md` 의 grep으로 기계 확인하고, 아래 3건은 육안 확인한다.

## T1 — `--non-interactive` 실행에서 prompt가 열리지 않는다 (AC4)

**Steps**

1. 이 task의 변경이 반영된 상태에서 `/ywc-impl-review --non-interactive` 를 임의의 소규모 diff 대상으로 1회 실행한다.
2. 실행 transcript에서 `AskUserQuestion` tool 호출 횟수를 센다.
3. 생성된 report의 Step 7 해당 구간을 확인한다.

**Expected Result**

- `AskUserQuestion` 호출 **0회**.
- report에 `### Learning candidates (not promoted — non-interactive)` block이 존재한다.
- block의 각 행이 고정 field 순서를 따른다: `[<aspect>] Occurrences in this review: <n> — <summary> (severity: <값>) — would promote to <target file> as <learning type>`.
- 후보가 0건이면 block 안에 `(none)` 이 출력되고, block 자체가 생략되지 않는다.
- `docs/review-learnings.md` 와 `claude-code/skills/references/recurring-defects.md` 가 실행 전후로 **변경되지 않는다** (`git status` 로 확인).

## T2 — flag 없는 실행이 기존 동작을 유지한다 (AC5 / AC8)

**Steps**

1. 동일 대상에 대해 flag 없이 `/ywc-impl-review` 를 1회 실행한다.
2. Step 0의 learnings 주입 여부를 T1 실행과 비교한다.
3. Step 7에서 승격 offer가 열리는지 확인한다.

**Expected Result**

- Step 0의 learnings 주입 결과가 T1과 **동일**하다 (`--non-interactive` 는 loading에 영향을 주지 않는다).
- Step 7에서 기존대로 승격 offer가 열린다.
- `Learning candidates (not promoted — non-interactive)` block은 출력되지 않는다.

## T3 — `--non-interactive` + `--skip-learnings` 조합 (Edge Case)

**Steps**

1. 두 flag를 동시에 지정해 1회 실행한다.

**Expected Result**

- Step 0 loading과 Step 7 모두 skip된다.
- report에 loading skip 사실만 기록되고, `Learning candidates (not promoted — non-interactive)` block은 출력되지 않는다 (수집 근거가 없으므로).
- 두 flag 조합이 `flag conflict` 로 처리되지 않는다.
