# 000068-010-domain-s3-reliability-wiring — Implementation Checklist

## Prerequisites

- [ ] `000067-020` 머지 완료 — runner 가 per-case 상태를 낸다
- [ ] `SKILL.md:113-114` 의 기존 S1/A2 unmeasured 문언을 확인했다 (같은 문언을 재사용한다)

## Allowed Edit Scope

`SKILL.md`, `references/skill-rubric.md`, `references/scorecard-format.md`, `score.py` 의 **history 기록부만**, `test_score.py`. **`score.py` 의 axes 계산식은 한 줄도 건드리지 않는다.**

## Stop Conditions

- `axes.S3` 에 숫자를 넣어야 한다고 판단되면 **중단하고 보고** — AC7 위반이며 CI 를 비결정적으로 만든다
- `·` 와 `?` 를 하나로 합치자는 판단이 들면 중단 — 두 상태는 해소 방법이 다르다

## Hardening Gate

- [ ] RED 먼저: `prose_lint` 때와 같은 방식으로, S3 를 오염시켜도 `axes` 가 바이트 동일함을 증명하는 테스트
- [ ] `score.py --ci` 실행 후 `history.mechanical.json` 에 git diff 가 없음을 확인

## Implementation Steps

- [ ] `references/skill-rubric.md` 의 S3 절을 reliability 밴드표로 교체하고, 채택 trial 수에서 **도달 불가한 밴드를 명시** (AC9)
- [ ] 같은 절에 fixture 미보유 시 독해 기반 fallback 을 `(read-only)` 태그와 함께 유지한다고 기술
- [ ] `SKILL.md:115` Behavioral judge 항목을 교체 — fixture 가 있으면 runner reliability, 없으면 `(read-only)` fallback (AC16)
- [ ] `references/scorecard-format.md` 에 범례 추가: `?` = fixture 부재로 측정 불가, `·` = 판단 tier 미실행, `Total` = `—` 조건
- [ ] `SKILL.md` `## Output Format` 의 예시 표에도 **동일 범례** 반영 (§AC17′ — 한쪽만 고치면 모순)
- [ ] `score.py` 의 history 기록부에 규칙 구현: 미측정 축이 있는 항목은 `items.<name> = null`, run row 에 `unmeasured[]` 와 `measured` 기록, `mean_total`/`below_threshold` 는 측정 완료 항목만으로 산출
- [ ] `score.py` 에 `s3_source: "runner" | "read-only"` 기록 추가 — 두 출처의 4점은 같은 측정이 아니다
- [ ] `test_score.py` 에 추가: 미측정 항목의 총점이 `null`, `mean_total` 이 해당 항목 제외, S3 오염 시 axes 불변

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` 통과
- [ ] `score.py --ci` exit 0 **그리고** `git diff --exit-code` 로 baseline 무변경 확인

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] `SKILL.md` 본문 500줄 이하 유지 (A8)
