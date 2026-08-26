# 000068-020-domain-ablation-paired-trials

## Purpose

with/without ablation 을 6회 paired 로 실행하고 은퇴 근거를 만든다. **노선 N1 에서 귀속을 주장할 수 있는 유일한 수단**이다.

## Scope

- 명시 플래그(`--suite expensive` 등)에서만 활성화
- with-arm: `claude -p "/<skill> <prompt>"` / without-arm: 동일 프롬프트 + `--disable-slash-commands`
- 6회 paired trial, pass rate 와 불확실성 표기
- 혼합 상태 집계 규칙 (AC18)
- `CANDIDATE_FOR_REVIEW` 판정과 **사람 승인** (AC11), fixture 존속 (AC12)

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-skill-eval-runner.md` — §AC2″ (귀속 한계), AC10/AC11 (ablation·은퇴), AC12 (fixture 존속), AC18 (혼합 상태), §NFR1″ (비용)
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` `## Retired Items`

### Summary

N1 에서 귀속은 **with/without 차이로만** 주장한다. with-arm 은 `/name` 명시 호출이라 대상 skill 실행은 보장되고, without-arm 은 모든 skill 이 꺼진다. 따라서 측정 대상은 "대상 skill 의 지시가 모델의 기본 행동보다 나은가" 이며 이는 가이드 §4 의 ablation 과 일치한다. 잔여 위험은 with-arm 중 형제 skill 의 개입이며, 리포트가 **로드된 skill 수를 함께 기록**해 한계를 드러낸다.

### Out of Scope (from spec)

- 평가 결과만으로 자동 은퇴 — 사람 승인 없이는 `CANDIDATE_FOR_REVIEW` 를 넘지 않는다
- CI 에서의 ablation 실행 — local manual 전용

## Criticality

`normal` — 자격증명을 다루지 않는다(N1 은 기존 구독 세션 사용). 다만 은퇴 판정은 되돌리기 어려운 결정이므로 사람 승인 게이트를 코드로 강제한다.

## Dependencies

### Depends On

- `000067-020-domain-eval-runner-workspace-boundary` — 단일 실행 기반
- `000067-010-infra-fixture-v2-schema-verifier-registry` — v2 fixture 입력

### Depended By

- `000069-010-infra-eval-ci-two-tier-docs` — ablation 절차를 문서화하고 CI 에서 제외함을 명시

## Key Files

- `.claude/skills/ywc-toolkit-eval/scripts/ablation.py` (신규)
- `.claude/skills/ywc-toolkit-eval/scripts/test_ablation.py` (신규)
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` (은퇴 절차 연결)

## Notes

- **without-arm 은 반드시 자연어 프롬프트**로 수행한다. slash 호출에 `--disable-slash-commands` 를 걸면 `Unknown command` 로 **$0 에 단락**되어 두 팔이 비대칭이 된다 (spike 실측).
- 케이스당 예상 비용 `6 × 2 × $0.54 ≈ $6.5`. 대상 케이스를 소수로 엄선한다.
- 은퇴해도 fixture 는 `retired: true` 로 남긴다 — 회귀 감시용.

## Hardening Evidence

### Test Feedback Path

- RED-first target: `.claude/skills/ywc-toolkit-eval/scripts/test_ablation.py`

### Interface Contract

- Contract: paired trial 집합 → 은퇴 판정
- Inputs: case 집합, trial 수(기본 6), adapter
- Outputs: arm 별 pass rate, 차이, 비용, 판정(`CANDIDATE_FOR_REVIEW` | `INCONCLUSIVE`)
- Error model: 한 팔의 `ERROR`/`SKIPPED_UNAVAILABLE`, `paired_valid < 6`, 비용 근거 불완전
- Impacted tests: 6쌍 fake adapter, 2쌍 ERROR 주입, 비용 미완비 케이스

### Critical Surface Review

- Review requirement: 표준 리뷰 + **은퇴 판정 경로 전량 리뷰** — 사람 승인 없이 은퇴가 확정될 수 없음을 코드로 확인한다.

### Data Integrity Hardening

- Trigger surface: 반복 실행 집계
- Atomic / locking strategy: trial 마다 독립 run id·workspace (`000067-020` 계약 재사용)
- Transaction boundary: 쌍 단위 — 한 팔이 무효면 그 쌍 전체를 집계에서 제외
- Idempotency guard: 시도별 고유 run id
- Required tests: `paired_valid` 감소 시 `INCONCLUSIVE`, 사람 승인 없이 은퇴 불가

## Parallel Execution Metadata

### Ownership

- `.claude/skills/ywc-toolkit-eval/scripts/ablation.py`
- `.claude/skills/ywc-toolkit-eval/scripts/test_ablation.py`
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` (은퇴 절차 절만)

### Shared Surfaces

- runner 결과 스키마 (`000067-020` 소유 — 재정의 금지)
- `trigger-eval-method.md` — `000069-010` 도 문서 갱신에서 접근 가능

### Conflicts With

- `000068-010-domain-s3-reliability-wiring` — 병렬 실행하지 않는다. 둘 다 `references/` 문서를 건드린다

### Parallelizable After

- `000067-020-domain-eval-runner-workspace-boundary`

### Task Verify

- `python3 .claude/skills/ywc-toolkit-eval/scripts/test_ablation.py`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/ablation.py --adapter fake --trials 6 --case <id>`

## Out of Scope

- 자동 은퇴 실행, CI 연결, S3 밴드 산출
