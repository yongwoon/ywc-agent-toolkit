# ywc-toolkit-eval

Claude Code `ywc-*` Skill 과 Claude Code Agent 품질을 **등급(0~5, 가중 100점)으로 채점**하고, `평가 → 점수 → 우선순위 → 개선 → 재평가` 사이클을 구동하는 Meta Skill 입니다. `ywc-skill-author` 가 제작 시점의 **이진 규칙**을 정의한다면, 이 Skill 은 이미 존재하는 Claude Code Skill/Agent 의 **graded scorecard** 를 만들어 약한 항목부터 고치게 합니다. Codex Skill/Agent 평가는 `.codex/skills/ywc-codex-toolkit-eval` 이 담당합니다.

## 평가 항목

### Skill 6축

| 축 | 가중치 | 내용 |
| --- | --- | --- |
| S1 Activation 정확도 | 30 | Trigger precision/recall + sibling 충돌 |
| S2 구조 Compliance | 15 | ywc-skill-author A1~A14 중 기계 점검 가능한 10개 하위집합 준수율 (A5/A10/A12/A13 제외) |
| S3 Behavioral 효능 | 20 | SKILL.md 만 따라도 의도한 산출물이 나오는가 |
| S4 토큰 경제성 | 10 | Tier-1 leanness, 본문 ≤500, Tier-3 추출 적정 |
| S5 일관성/무결성 | 15 | README locale, pointer resolve, dangling ref |
| S6 카탈로그 적합성 | 10 | sibling 중복/공백 |

### Agent 6축

| 축 | 가중치 | 내용 |
| --- | --- | --- |
| A1 역할 경계 명확성 | 20 | 책임이 crisp 하고 비중복인가 |
| A2 Dispatch 정확도 | 25 | orchestrator 가 올바른 상황에 선택하는가 |
| A3 Tool 최소권한 | 15 | 읽기전용 reviewer 가 mutating tool 미보유 |
| A4 Output contract | 15 | Status/Next-action 형식 정의·준수 |
| A5 Model tier 적합성 | 15 | Opus/Sonnet/Haiku fit |
| A6 System prompt 품질 | 10 | persona 명확성, anti-rationalization |

## 2-Tier 채점

| Tier | 방식 | CI |
| --- | --- | --- |
| Mechanical | `scripts/score.py` (결정론적) | 회귀 시 차단 |
| Judgment | Agent judge pass | on-demand, 비차단 |

## 사용 방법

```bash
# 전체 평가 + 개선 우선순위
/ywc-toolkit-eval --mode full --target all

# 구조만 빠르게 (스크립트)
python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --format markdown

# CI 회귀 게이트
python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci
```

또는 자연어로 호출:

> "toolkit skill들 품질 평가하고 점수 매겨줘"

Codex 쪽을 평가하려면 `ywc-codex-toolkit-eval`을 사용합니다.

## 출력

- `evals/scorecard.md` — Skill/Agent 별 축점수 + 총점 + 우선순위 backlog
- `evals/history.json` — 날짜별 총점 (추세)

## 관련

- `ywc-skill-author` — S2 sub-rubric 의 출처(규칙). 이 Skill 은 준수율을 채점만 함
- `.codex/skills/ywc-codex-toolkit-eval` — Codex Skill/Agent 전용 평가
- `ywc-impl-review` — application 코드를 리뷰. 이 Skill 은 toolkit 자체를 평가
- `scripts/validate.sh` — 이진 구조 게이트. 이 Skill 은 그 위의 graded layer
