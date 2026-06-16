# 000009-020-test-eval-scorer-unit-tests

## Purpose
score.py 의 룹릭↔구현 정합을 회귀로부터 보호하는 stdlib 단위 테스트(`test_score.py`)를 신설한다(FR12).

## Scope
- FR2 가드, FR3 A5 밴드(매치=5 / Opus-on-mechanical=3 / Haiku-on-architecture=2), FR4 데이터 행 카운트, FR6 절 면제, FR10 에이전트 포인터를 합성 픽스처로 검증
- `python3 -m unittest` 로 실행 가능

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-eval-improvements.md` — FR12, Amendment A1(A5 합성 픽스처 기대값), API/CLI Contract 표
### Summary
현 카탈로그는 A5 가 전부 5(차별화 미발생)이므로, 변별력 증명을 위해 Opus-on-mechanical·Haiku-on-architecture 합성 에이전트 픽스처로 3·2 를 검증한다.
### Out of Scope (from spec)
- 판정 축 테스트(모델 호출 필요) 제외 — 기계 축만

## Dependencies
### Depends On
- `000009-010-domain-eval-scorer-logic` — 테스트 대상 함수/분기 제공
### Depended By
- `000009-050-infra-final-verification`

## Key Files
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (신규)

## Notes
- 선례: Codex 형제의 `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py` 구조 참고 가능(포팅 아님).
- stdlib `unittest` 만 사용. score.py 의 헬퍼를 import 하여 직접 호출.

## Out of Scope
- score.py 로직 수정(소유는 -010)

## Parallel Execution Metadata
- **Ownership:** `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`
- **Shared Surfaces:** score.py 의 공개 함수 시그니처(-010 이 확정)
- **Conflicts With:** (None identified)
- **Parallelizable After:** `000009-010` 머지 후 030·040 과 병렬 가능
- **Task Verify:** `python3 -m unittest discover -s .claude/skills/ywc-toolkit-eval/scripts -p 'test_score.py'`
