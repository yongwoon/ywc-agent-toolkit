# 000068-020-domain-ablation-paired-trials — Implementation Checklist

## Prerequisites

- [ ] `000067-020` 머지 완료 — 단일 실행과 상태 enum 이 존재한다
- [ ] `docs/skill-agent-eval/claude/spike-2026-07-22.md` 의 `--disable-slash-commands` 실측(`$0` 단락)을 확인했다

## Allowed Edit Scope

`scripts/ablation.py`, `scripts/test_ablation.py` 신규 2파일과 `references/trigger-eval-method.md` 의 은퇴 절차 절. runner 와 score.py 는 건드리지 않는다.

## Stop Conditions

- without-arm 을 slash 호출로 구성하게 되면 **중단** — `$0` 단락으로 두 팔이 비대칭이 된다
- 사람 승인 없이 은퇴가 확정되는 경로가 생기면 중단

## Hardening Gate

- [ ] RED 먼저: 6쌍 중 2쌍에 `ERROR` 를 주입했을 때 `INCONCLUSIVE` 가 나오는 테스트
- [ ] 사람 승인 플래그 없이는 `CANDIDATE_FOR_REVIEW` 를 넘어설 수 없음을 테스트로 증명

## Implementation Steps

- [ ] `ablation.py` 에 `run_pair(case, trial_idx) -> dict` 작성 — with-arm 은 `/name` 명시 호출, without-arm 은 **동일한 자연어 프롬프트** + `--disable-slash-commands`
- [ ] `run_suite(case, trials=6) -> dict` 작성 — 쌍 단위 집계. 한 팔이 `ERROR`/`SKIPPED_UNAVAILABLE` 이면 그 쌍을 제외하고 `paired_valid` 감소
- [ ] `paired_valid < 6` 이면 결과를 `INCONCLUSIVE` 로 확정하고 은퇴 판정에 쓰지 않는다 (AC18)
- [ ] `CANDIDATE_FOR_REVIEW` 조건 구현: without 팔의 실패가 with 팔보다 **1회 이하**로 많고 양쪽 비용 근거가 완비된 경우에만 (AC11)
- [ ] 최종 은퇴는 사람 승인 없이는 불가 — 코드가 승인 플래그를 요구하도록 작성
- [ ] 리포트에 **로드된 skill 수**를 기록 (§AC2″ — 귀속 한계를 드러내는 필수 항목)
- [ ] 시작 시 예상 dispatch 수와 비용(`trials × 2 × cases × $0.54`)을 stderr 출력 후 중단 기회 제공
- [ ] `references/trigger-eval-method.md` 의 `## Retired Items` 에 은퇴 절차와 `retired: true` 보존을 연결
- [ ] `test_ablation.py` 작성: 6쌍 정상, 2쌍 ERROR → INCONCLUSIVE, 비용 미완비 → INCONCLUSIVE, 승인 없이 은퇴 불가

## Task Verify

- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_ablation.py` 통과
- [ ] fake adapter 6쌍 실행이 pass rate·차이·비용을 모두 보고

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] 실제 CLI 호출은 이 task 의 자동 검증에 포함하지 않는다 (비용) — `test.md` 의 수동 절차로 1회만 확인
