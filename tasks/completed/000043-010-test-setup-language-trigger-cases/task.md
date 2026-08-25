# Task: setup-language 트리거 케이스 작성

## Prerequisites
- [ ] §OQ1′ 결정 완료: collision 형제 확정 또는 커버리지 규칙 예외 승인. **미결이면 Stop.**

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` 만.

## Stop Conditions
- OQ1(collision 형제)이 미결이면 착수하지 말고 보고.
- 신규 케이스 추가로 기존 형제(예: ywc-project-mission)의 collision 카운트가 의도치 않게 변동하면 보고.

## Implementation Steps
- [ ] `trigger-cases.json`의 기존 케이스 shape 확인: `{id, prompt, expected, kind, impostor?, note?}`.
- [ ] positive ≥3 추가 — ko/ja/en 혼합. 예: `setup-language-pos-1` "출력 언어 설정해줘"(ko),
      `setup-language-pos-2` "set the project output language"(en), `setup-language-pos-3` "出力言語を設定して"(ja),
      각 `expected: ywc-setup-language`, `kind: positive`.
- [ ] collision ≥2 추가 — §OQ1′에서 확정된 impostor 지목. 각 케이스는 `kind: collision`,
      `expected: <owner가 이겨야 하는 스킬>`, `impostor: <오작동 후보>`, `note:` 로 승자 근거 명시.
- [ ] JSON 유효성: `python3 -m json.tool .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json >/dev/null`.
- [ ] 중복 id 없음 확인.

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-setup-language --format json`
      출력의 `signals.coverage`가 `{"positives": >=3, "collisions": >=2, "sufficient": true}`.
- [ ] 전체 실행 `... --target claude-code/skills` 시 stderr "N items below minimum"에서 ywc-setup-language 사라짐.

## Verification
- [ ] `bash scripts/validate.sh` exit 0 (구조 회귀 없음).
- [ ] 참고: `validate.sh`는 eval 픽스처를 직접 검증하지 않으므로 FR1의 실질 게이트는 위 score.py coverage.
