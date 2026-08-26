# 000068-010-domain-s3-reliability-wiring

## Purpose

S3(Behavioral efficacy)를 **독해 기반에서 실행 기반으로** 전환한다. runner 의 reliability 를 밴드로 환산하고, fixture 미보유 항목은 `"unmeasured"` 로 남긴다.

## Scope

- `reliability = passes / trials` → S3 밴드 매핑, 도달 불가 구간 명시
- fixture 미보유 → `"unmeasured"` (S1/A2 와 동일 규율)
- `SKILL.md` Behavioral judge 항목 교체 (AC16)
- 스코어카드 표기 규약 — `?`(측정 불가) vs `·`(판단 tier 미실행), `Total` 은 `—` (§AC17′)
- `history.json` 기록 규칙 — 미측정 항목은 `items.<name>: null` (§AC8′)

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-skill-eval-runner.md` — §AC8′ (총점 정직성), §AC17′ (양쪽 문서 표기), AC16 (judge 교체), AC9 (해상도)
- `.claude/skills/ywc-toolkit-eval/SKILL.md:113-115` — 기존 S1/A2 unmeasured 규율과 Behavioral judge 위치

### Summary

축 하나가 unmeasured 인 항목의 `/100` 총점은 만점이 80 인 점수이므로 숫자로 내보내지 않는다 — `items.<name>` 은 `null` 이고 `mean_total`/`below_threshold` 는 측정 완료 항목만으로 계산한다. 표기는 `·`(이번 run 에서 판단 tier 미실행)와 `?`(fixture 부재로 측정 불가)를 **반드시 구분**한다. 둘은 해소 방법이 다르다 — 전자는 `--mode full` 재실행, 후자는 fixture 백필.

### Out of Scope (from spec)

- `axes.S3` 를 숫자로 만드는 것 — AC7 이 금지한다. runner 결과는 scorecard/backlog 에만 반영
- ablation 집계 (`000068-020`)

## Criticality

`normal` — 보안 민감 표면을 다루지 않는다. 다만 AC7(CI 결정성 보존) 위반은 CI 를 LLM 비결정성에 종속시키므로 테스트로 강제한다.

## Dependencies

### Depends On

- `000067-020-domain-eval-runner-workspace-boundary` — reliability 의 입력이 되는 실행 결과를 제공

### Depended By

- `000069-010-infra-eval-ci-two-tier-docs` — 밴드표와 표기 규약을 문서화 대상으로 삼는다

## Key Files

- `.claude/skills/ywc-toolkit-eval/SKILL.md` (Behavioral judge 항목, Step 2 signal 나열)
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md` (S3 절 교체)
- `.claude/skills/ywc-toolkit-eval/references/scorecard-format.md` (표기 범례)
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` (history 기록 규칙)

## Notes

- **`axes.S3` 는 계속 `None`** 이다. `flatten_mech()` 가 non-null axes 만 baseline 에 저장하므로, 숫자를 넣는 순간 `--ci` 가 LLM 비결정성에 종속된다.
- `references/scorecard-format.md:68` 이 이미 "judgment tier's natural variance never trips the gate" 를 문서화하고 있다 — 재유도하지 말고 인용한다.
- 표기 규약은 `scorecard-format.md` 와 `SKILL.md` `## Output Format` **양쪽**에 반영해야 한다. 한쪽만 고치면 두 문서가 서로를 반박한다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (신규 케이스 추가)

### Interface Contract

- Contract: 실행 결과 → S3 값과 기록 형태
- Inputs: runner 의 per-case 상태 집합, fixture 보유 여부
- Outputs: S3 정수(0–5) 또는 문자열 `"unmeasured"`, `items.<name>` 값(숫자 또는 `null`)
- Error model: trials 0, 전 trial `ERROR`, fixture 부재
- Impacted tests: unmeasured 강제, 총점 null, mean_total 제외, axes 불변

### Critical Surface Review

- Review requirement: 표준 리뷰. 단 AC7 회귀 테스트는 필수 — S3 가 `axes`/baseline 에 진입하지 않음을 증명해야 한다.

### Data Integrity Hardening

- Trigger surface: `history.json` append
- Atomic / locking strategy: 해당 없음 (단일 프로세스 append)
- Transaction boundary: run row 1건 append, 기존 row 불변
- Idempotency guard: 회차당 1 row — 재실행이 기존 row 를 덮지 않는다
- Required tests: 기존 row 불변, 미측정 항목이 `mean_total` 에서 제외됨

## Parallel Execution Metadata

### Ownership

- `.claude/skills/ywc-toolkit-eval/SKILL.md`
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`
- `.claude/skills/ywc-toolkit-eval/references/scorecard-format.md`
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` (history 기록부 한정)
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`

### Shared Surfaces

- `SKILL.md` — `000069-010` 도 문서 갱신에서 접근할 수 있다
- `score.py` — axes 계산식은 건드리지 않지만 파일을 공유한다
- `history.json` 스키마

### Conflicts With

- `000069-010-infra-eval-ci-two-tier-docs` — `SKILL.md` 를 함께 건드릴 수 있으므로 병렬 실행하지 않는다

### Parallelizable After

- `000067-020-domain-eval-runner-workspace-boundary`

### Task Verify

- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 후 `git diff --exit-code .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

## Out of Scope

- ablation, 은퇴 판정, CI 변경
