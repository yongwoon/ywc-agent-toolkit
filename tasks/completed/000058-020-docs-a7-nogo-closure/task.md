# 000058-020-docs-a7-nogo-closure — Implementation Checklist

> **실행 조건**: `000057-020`의 report가 **NO-GO** (AC9 게이트 실패) 또는 **`INCONCLUSIVE`** (pooled `floor_rate > 0.25`)를 기록한 경우에만. GO면 `000058-010`을 대신 실행한다.

## Prerequisites

- [ ] `000057-020-test-pilot-dispatch-report`가 완료·merge되었다.
- [ ] report의 판정이 NO-GO 또는 `INCONCLUSIVE`임을 확인했다.

## Allowed Edit Scope

- [ ] `docs/ywc-plans/prune-report-rationalization-defense.md`의 결론 섹션만 쓴다.
- [ ] AC10의 다섯 파일(`ywc-skill-author/SKILL.md`, `claude-code/skills/CLAUDE.md`, `skill-rubric.md`, `score.py`, `test_score.py`) 중 **어느 것도 편집하지 않는다**.

## Stop Conditions

- [ ] "증거는 없지만 quota를 좀 완화해두자"는 생각이 들면 멈춘다 — AC10이 금지한다.
- [ ] `INCONCLUSIVE` run을 통과시키려고 ceiling(0.25)을 조정하고 싶어지면 멈춘다.
- [ ] null 결과를 "실패"나 "재시도 필요"로 적고 싶어지면 멈추고 사양의 표현을 확인한다.

## Implementation Steps

- [ ] report의 판정이 **어느 쪽인지** 확정한다:
  - `VALID` + 게이트 실패 → **결론이 나왔다**: corpus는 load-bearing임이 입증되었다.
  - `INCONCLUSIVE` → **결론이 나오지 않았다**: harness가 측정되었을 뿐이다.
- [ ] 게이트 실패인 경우: report에 **"quota not shown to manufacture padding"** 을 확정 기록하고, per-stratum inert 비율과 Fisher p-value를 근거로 인용한다. 이것이 정당하고 내구성 있는 결과임을 명시한다.
- [ ] `INCONCLUSIVE`인 경우: pooled `floor_rate`를 기록하고 "측정된 것은 corpus가 아니라 harness"임을 명시한다. 재실행을 위한 harness 분산 축소 방안(더 제약된 시나리오, 낮은 sampling temperature)을 기록한다.
- [ ] FR-4를 **미출시**로 닫는다고 report에 기록한다. 다섯 사본은 그대로 남는다.
- [ ] FR-5의 enforcement 모드가 **advisory**로 확정됨을 기록한다 (`000059-040`이 이것을 읽는다).
- [ ] 이 spec이 여전히 전달한 것을 열거한다: report, 두 script(`000055-020`), A8 수정(`000055-040`), README 동기화(`000055-030`), Deletion Test 절차(`000056-010`).

## Task Verify

- [ ] report에 최종 결론이 있고, 게이트 실패와 `INCONCLUSIVE`가 구별되어 서술되어 있다
- [ ] `git diff --name-only`가 report 외의 파일을 보이지 않는다
- [ ] `grep -n 'at least 5' claude-code/skills/ywc-skill-author/SKILL.md` → A7 quota가 **그대로 살아 있다**
- [ ] report에 ceiling 조정에 대한 서술이 없다

## Verification

- [ ] `bash scripts/validate.sh` 통과.
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과 (A7 게이트가 그대로 살아 있으므로 당연히 통과해야 한다) (AC13).
- [ ] `for d in claude-code/skills/ywc-*/; do bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh "$d" || echo "FAILED: $d"; done` → `FAILED:` 없음.
