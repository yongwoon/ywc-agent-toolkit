# 000009-030-docs-rubric-skill-alignment — 구현 체크리스트

## Prerequisites
- [ ] `000009-010` 완료(임계값/하위집합 확정)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/SKILL.md`, `.claude/skills/ywc-toolkit-eval/README.md`, `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`, `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md`, `.claude/skills/ywc-toolkit-eval/references/agent-rubric.md`

## Stop Conditions
- 문서 숫자가 -010 구현값과 다르면 중단·보고(코드가 진실의 원천)

## Implementation Steps
- [ ] FR4: `references/skill-rubric.md:42` "≥5 table rows" 를 "데이터 행 ≥5(헤더·구분자 제외)" 로 명확화, SKILL.md A7 참조 동일화
- [ ] FR5: `references/skill-rubric.md` S2 섹션과 `SKILL.md:61` 표기를 "기계 점검 10개 하위집합"으로, 점검 10개 규칙 열거 + A5/A10/A12/A13 비기계 범위 명시
- [ ] FR7: `SKILL.md`(16/123 영역)·`README.md` 수치 38 skills/12 agents 로 갱신, Output Format 예시에 "(illustrative)" 라벨
- [ ] FR8: `SKILL.md` Arguments 표를 score.py 플래그(`--target/--item/--format/--ci`)와 오케스트레이터 인자(`--mode/--advisor-budget`, 스크립트 미전달)로 분리
- [ ] FR9: `references/trigger-eval-method.md:75` 문구를 런타임 중립("비결정 샘플링 미사용; judge 최선 매치, 동률은 나열 순")으로 교체
- [ ] FR11: `SKILL.md` 에 ".claude/skills/ 내부 전용·en/ja/ko 로케일 면제" 1줄 추가

## Task Verify
- [ ] 룹릭/SKILL 의 A7=5, S2 하위집합 표기가 score.py 와 일치(수기 대조)
- [ ] `grep -c 'Math.random' .claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` == 0
- [ ] `SKILL.md` ≤500줄: `awk 'END{exit (NR>500)}' .claude/skills/ywc-toolkit-eval/SKILL.md`

## Verification
- [ ] markdownlint 통과(README*.md)
- [ ] `bash scripts/validate.sh` 통과
