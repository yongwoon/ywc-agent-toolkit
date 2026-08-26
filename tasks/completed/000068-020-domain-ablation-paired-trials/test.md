# 000068-020-domain-ablation-paired-trials — Manual Test Plan

실제 비용이 발생하므로 **1 케이스만** 수동 확인한다.

## 1. 실제 ablation 1 케이스

**Steps**
1. 비용이 작은 skill 로 case 1건을 고른다
2. `python3 .claude/skills/ywc-toolkit-eval/scripts/ablation.py --suite expensive --trials 6 --case <id>` 실행
3. 시작 시 출력되는 예상 비용을 확인하고 진행한다

**Expected Result**
- 12회 dispatch(6쌍 × 2팔)가 실행된다
- with/without pass rate 와 차이, 총비용이 보고된다
- 판정이 `CANDIDATE_FOR_REVIEW` 또는 `INCONCLUSIVE` 중 하나이며, **자동으로 은퇴가 확정되지 않는다**
- 리포트에 로드된 skill 수가 기록된다

## 2. without-arm 이 $0 로 단락되지 않는지

**Steps**
1. 위 실행의 without-arm 개별 비용을 확인한다

**Expected Result**
- without-arm 비용이 **0 이 아니다** — 0 이면 slash 호출로 잘못 구성된 것이므로 즉시 수정한다
