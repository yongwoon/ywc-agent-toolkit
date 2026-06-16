# 000009-020-test-eval-scorer-unit-tests — 구현 체크리스트

## Prerequisites
- [ ] `000009-010` 완료(score.py 신규 로직 머지)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (신규)만

## Stop Conditions
- 테스트가 -010 구현의 실제 버그를 드러내면 중단·보고(테스트를 약화시키지 말 것)

## Implementation Steps
- [ ] `test_score.py` 생성, `score` 모듈 import(경로 조정 포함)
- [ ] FR2: `--ci`+`--item` 조합이 비정상 종료하고 `HISTORY_MECH` 미기록임을 임시 baseline 픽스처로 검증
- [ ] FR3: 합성 에이전트 dict 로 밴드 검증 — (architect, opus)=5, (security, sonnet)=5, (doc-writer, haiku)=5, (mechanical-role, opus)=3, (architecture-role, haiku)=2, (no model)=0
- [ ] FR4: 데이터 행 4개=실패, 5개=통과 표 문자열로 A7 검증
- [ ] FR6: 형제를 `Do not use for` 절에 둔 경우 면제, 협력 문장에만 둔 경우 collision 유지 검증
- [ ] FR10: `use ywc-<agent>`(실존 에이전트) 포인터가 미플래그됨을 검증

## Task Verify
- [ ] `python3 -m unittest discover -s .claude/skills/ywc-toolkit-eval/scripts -p 'test_score.py'` 전부 통과

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] 신규 의존성 없음(stdlib only)
