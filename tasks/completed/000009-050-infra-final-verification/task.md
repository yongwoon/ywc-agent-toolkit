# 000009-050-infra-final-verification — 구현 체크리스트

## Prerequisites
- [ ] `000009-010`,`-020`,`-030`,`-040` 모두 완료/머지

## Allowed Edit Scope
- (없음) — 검증 전용. 결함 발견 시 해당 태스크로 회부, 본 태스크에서 수정 금지

## Stop Conditions
- `--ci` 가 회귀를 보고하거나 A5 에 5 미만이 있으면 중단·해당 태스크로 회부

## Implementation Steps
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` → 50항목 무오류, agents A5 전원 5
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` 커버리지 요약 "0 items below minimum"
- [ ] `python3 -m unittest discover -s .claude/skills/ywc-toolkit-eval/scripts -p 'test_score.py'` 전부 통과
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` PASS(무회귀), `git diff .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` 가 A5 4→5 외 하락 없음
- [ ] `bash scripts/validate.sh` 통과
- [ ] markdownlint(README*.md) 통과

## Task Verify
- [ ] 위 6개 단계 전부 PASS

## Verification
- [ ] 전체 스위트 green, 회귀 0
