# 000009-030-docs-rubric-skill-alignment

## Purpose
구현(-010)과 문서/룹릭의 드리프트를 제거한다. A7 임계값, S2 범위의 정직한 표기, 카탈로그 수치, 인자 소유 계층, determinism 문구, 내부 전용 로케일 면제를 정렬한다(FR4 텍스트·FR5·FR7·FR8·FR9·FR11).

## Scope
- FR4: `references/skill-rubric.md` 의 A7 문구를 "데이터 행 ≥5" 로, SKILL/ywc-skill-author 참조와 동일 숫자
- FR5: S2 를 "A1–A14 준수율" → "기계 점검 가능한 10개 하위집합" 으로 정직화, in/out 규칙 명시
- FR7: 카탈로그 수치 36→38 skills / 12 agents(또는 count-agnostic), 예시 scorecard 를 illustrative 로 라벨
- FR8: Arguments 표를 `score.py` 플래그 vs 스킬/오케스트레이터 인자(`--mode`/`--advisor-budget`)로 분리
- FR9: `references/trigger-eval-method.md:75` 의 `Math.random()` 표현을 런타임 중립 문구로
- FR11: SKILL.md 에 내부 전용·로케일 세트 면제 1줄 명시

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-eval-improvements.md` — FR4, FR5, FR7, FR8, FR9, FR11
### Summary
숫자·범위 주장이 -010 구현과 정확히 일치해야 한다. 특히 A7=5 데이터 행, S2 하위집합 정의는 코드와 글자 단위로 합의되어야 한다.
### Out of Scope (from spec)
- score.py 로직 변경(소유 -010)
- 케이스 데이터(소유 -040)

## Dependencies
### Depends On
- `000009-010-domain-eval-scorer-logic` — 구현된 임계값/하위집합을 그대로 문서가 따라야 함
### Depended By
- `000009-050-infra-final-verification`

## Key Files
- `.claude/skills/ywc-toolkit-eval/SKILL.md`
- `.claude/skills/ywc-toolkit-eval/README.md`
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md`
- (해당 시) `.claude/skills/ywc-toolkit-eval/references/agent-rubric.md`

## Notes
- SKILL.md ≤500줄 유지(현 158줄). 장문 신설 금지.
- markdownlint 통과 필요(README*.md).

## Out of Scope
- 코드·테스트·케이스 파일

## Parallel Execution Metadata
- **Ownership:** `.claude/skills/ywc-toolkit-eval/SKILL.md`, `.claude/skills/ywc-toolkit-eval/README.md`, `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`, `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md`, `.claude/skills/ywc-toolkit-eval/references/agent-rubric.md`
- **Shared Surfaces:** SKILL/룹릭의 임계값 숫자(-010 구현과 의미적 일치 필요)
- **Conflicts With:** (None identified) — score.py/케이스 파일 비중첩
- **Parallelizable After:** `000009-010` 머지 후 020·040 과 병렬 가능
- **Task Verify:** `npx --yes markdownlint-cli2 ".claude/skills/ywc-toolkit-eval/README*.md"` (또는 프로젝트 markdownlint 워크플로 기준), 및 룹릭↔코드 숫자 수기 대조
