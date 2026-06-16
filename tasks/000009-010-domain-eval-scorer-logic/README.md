# 000009-010-domain-eval-scorer-logic

## Purpose
`ywc-toolkit-eval` 의 결정론적 채점기(`score.py`) 로직 결함 6건을 수정하고, 변경된 기계 축 점수를 CI 기준선에 원자적으로 재기준선화한다. 리뷰에서 식별된 High 2건(FR2·FR3)과 Medium 2건(FR4·FR6), Low 1건(FR10), 그리고 커버리지 게이트(FR1b)를 한 단위로 처리한다.

## Scope
- FR2: `--ci` 와 `--item` 동시 사용 차단(기준선 부분 덮어쓰기 방지)
- FR3: A5 상수 `4 if model` → 역할↔티어 휴리스틱(Amendment A1 의 12-에이전트 표 고정)
- FR4: A7 Rationalization Defense 행 카운트를 **데이터 행 ≥5** 의미로 교정
- FR6: collision 면제 판정을 `Do not use for` 절 기준으로 좁힘
- FR10: `_unresolved_sibling_pointers` 를 skill + agent 루트 양쪽으로 해석
- FR1b: `signals.coverage` 게이트(축 dict 미오염, CI 스키마 불변)
- 변경 직후 `evals/history.mechanical.json` 재기준선화(FR3/FR4 와 동일 커밋 — Amendment A3)

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-eval-improvements.md` — FR1b, FR2, FR3, FR4, FR6, FR10, FR12(재기준선 부분), `## Iteration 1 Amendments` A1·A2·A3
### Summary
score.py 의 기계 축(S2·S5·A5) 값에 영향을 주는 로직 변경(FR3·FR4·FR10)과 무영향 변경(FR2·FR6·FR1b)을 함께 적용한 뒤, 같은 커밋에서 기준선을 재생성한다. A5 는 현재 12개 에이전트 전부 4→5 로 상승하므로 CI 회귀(하락)는 발생하지 않는다(Amendment A3).
### Out of Scope (from spec)
- 룹릭 산문/문서 갱신(→ 000009-030), 단위 테스트(→ 000009-020), 케이스 작성(→ 000009-040)
- 2-tier 아키텍처·축·가중치 변경 없음

## Dependencies
### Depends On
- (없음) — 본 배치의 기반 태스크
### Depended By
- `000009-020-test-eval-scorer-unit-tests` — 신규 함수/분기(FR2 가드, A5 밴드, 행 카운트, 절 면제, 에이전트 포인터)를 검증
- `000009-030-docs-rubric-skill-alignment` — 룹릭/SKILL 의 임계값 숫자가 구현과 일치해야 함(A7=5, S2 하위집합, 인자 소유)
- `000009-040-test-trigger-cases-authoring` — `signals.coverage` 게이트가 작성된 케이스를 검증
- `000009-050-infra-final-verification` — 최종 교차 검증

## Key Files
- `.claude/skills/ywc-toolkit-eval/scripts/score.py` (수정)
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (재생성)

## Notes
- **선례 재사용:** Codex 형제 `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py` 가 커버리지/인벤토리 게이트의 검증된 구현이다. FR1b 설계 시 참고하되, 포팅이 아니라 본 스킬 스키마에 맞춰 `signals.coverage` 로 구현한다.
- **A5 권위 표(Amendment A1):** architect/root-cause/critic → Opus, doc-writer/포매팅 → Haiku, 그 외(security 정적분석 포함) → Sonnet. 현 카탈로그 12개는 전부 매치=5.
- **원자성(Amendment A3):** A5/A7 로직과 기준선 재생성은 반드시 동일 커밋. 분리 시 -010 PR 의 CI 가 적색이 될 수 있다.

## Out of Scope
- 판정(judgment) 축(S1·S3·S6·A1·A2·A6) 계산 — 변경 없음(여전히 judge 가 채움)
- 룹릭 마크다운 텍스트 — 000009-030 소유

## Parallel Execution Metadata
- **Ownership:** `.claude/skills/ywc-toolkit-eval/scripts/score.py`, `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- **Shared Surfaces:** `history.mechanical.json`(CI `validate.yml` 이 읽음), `trigger-cases.json` 스키마(040 와 공유), SKILL/룹릭의 임계값 숫자(030 과 의미적 공유 — 030 이 본 태스크 구현값을 따라야 함)
- **Conflicts With:** (None identified) — 020/030/040 와 파일 비중첩
- **Parallelizable After:** (없음 — 기반 태스크)
- **Task Verify:**
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` → 50항목 무오류
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci --item ywc-commit` → 비정상 종료 + 기준선 미변경(FR2)
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` → 회귀 없음 PASS, 50-key 유지
