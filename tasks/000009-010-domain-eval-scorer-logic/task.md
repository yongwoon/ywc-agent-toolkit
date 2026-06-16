# 000009-010-domain-eval-scorer-logic — 구현 체크리스트

## Prerequisites
- [ ] (없음) 기반 태스크

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/scripts/score.py`
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (마지막 단계 재생성)
- 그 외 파일 수정 금지(룹릭/SKILL/README/테스트/케이스는 다른 태스크 소유)

## Stop Conditions
- A5 휴리스틱 적용 후 현 12개 에이전트 중 하나라도 A5 ≠ 5 가 나오면 중단·보고(권위 표와 불일치 = 구현 버그)
- `--ci` 가 회귀(하락)를 보고하면 중단·보고(A7 변경으로 S2 하락 가능 — 재기준선 단계 누락 여부 확인)
- 커버리지 표기가 `axes` dict 에 비정수로 들어가면 중단(FR1b 는 `signals` 전용)

## Implementation Steps
- [ ] FR2: `main()` 에서 `args.ci and args.item` 이면 stderr 에 1줄 오류 출력 후 `return 2`, `ci_gate`/`HISTORY_MECH` 쓰기 이전에 차단 (`score.py:393-400` 영역)
- [ ] FR3: `score_agent` 의 `a5 = 4 if model else 0`(`:271`) 를 역할→기대티어 추론 + 선언 model 대조 밴딩으로 교체. 키워드 매핑 상수를 모듈 상단에 정의하고 `references/agent-rubric.md` §A5 를 가리키는 주석 추가. `signals["model_expected"]` 방출
- [ ] FR4: A7 체크(`:136-137`)를 Rationalization Defense 표의 **데이터 행 수**(전체 표 라인 − 헤더 − 구분자) ≥5 로 변경
- [ ] FR6: `find_collisions`(`:104`)의 `b not in ad`/`a not in bd` 를 "`Do not use for` 절 내 형제 언급" 판정으로 교체(현 카탈로그 40건 전부 영문 절)
- [ ] FR10: `_unresolved_sibling_pointers`(`:220-226`)가 `SKILL_ROOTS` + `AGENT_ROOTS`(파일형 `claude-code/agents/ywc-<name>.md`) 양쪽 해석
- [ ] FR1b: `trigger-cases.json` 로드 → 항목별 `{positives, collisions, sufficient}`(≥3/≥2) 계산하여 `signals["coverage"]` 에만 기록(S1/A2 는 `axes` 에서 계속 `null`). 카탈로그 요약에 "N items below minimum" 출력
- [ ] 재기준선(Amendment A3): 위 변경 후 `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 로 `history.mechanical.json` 재생성, diff 가 A5 4→5(상승만) 및 의도된 S2 변화로 한정됨을 확인하고 같은 커밋에 포함

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` 무오류, A5 signals 에 `model_expected` 존재
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci --item ywc-commit` 비정상 종료 + `git diff --stat .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` 무변경
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` PASS(회귀 없음)

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('.claude/skills/ywc-toolkit-eval/scripts/score.py').read_text())"` 구문 OK(stdlib only 유지)
