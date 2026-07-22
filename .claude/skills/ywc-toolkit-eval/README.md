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

## 운영 절차 (CI 2계층)

평가는 **CI 1계층 + 로컬 수동 1계층**으로 나뉜다. 원래 설계는 3계층이었으나 가운데 계층(scheduled live)이 구조적으로 불가능하다.

### 계층 1 — PR CI (자동, 무료)

`.github/workflows/validate.yml` 의 `skill-eval-schema` job 이 PR 마다 실행된다. **모델을 한 번도 호출하지 않는다.**

- v2 fixture 가 스키마를 만족하는가 (`fixture_schema.validate_case`)
- 선언된 경로가 `fixture_root` 밖으로 나가지 않는가 (`normalize_manifest`)
- runner / ablation 이 fake adapter 로 정상 동작하는가
- `score.py --ci` 기계적 회귀 게이트 (`validate-skills` job)

이 계층이 보장하는 것은 **평가 장치가 온전하다**는 것이지 스킬이 실제로 잘 동작한다는 것이 아니다. 그 둘을 혼동하면 CI 초록불을 품질 근거로 오독하게 된다.

### 계층 2 — 로컬 수동 (사람, 유료)

live 평가와 ablation 은 개발자 머신에서 릴리스 주기마다 사람이 돌린다.

```bash
# 단일 케이스 실행 (fake 는 무료, claude 는 dispatch 당 약 $0.54)
python3 .claude/skills/ywc-toolkit-eval/scripts/runner.py --adapter fake --case <fixture-id>

# with/without ablation — 케이스당 6 trial × 2 arm ≈ $6.50
python3 .claude/skills/ywc-toolkit-eval/scripts/ablation.py \
  --case <fixture-id> --suite expensive --adapter claude --loaded-skill-count <n>
```

`--suite expensive` 는 실수로 돈을 쓰지 않게 하는 명시적 opt-in 이다. 대상 케이스는 소수로 엄선한다. 은퇴 판정 절차는 `references/trigger-eval-method.md` 의 `## Retired Items` 를 따른다 — 사람 승인 없이는 은퇴가 확정되지 않는다.

### 왜 CI 에서 live 평가를 하지 않는가

**할 수 없기 때문이다.** `claude -p` dispatch 는 개발자 머신의 구독 세션 인증에 의존하는데 GitHub Actions 러너에는 그 세션이 없다. 대안인 `ANTHROPIC_API_KEY` 는 프로젝트 방침상 배제되어 있고, `--bare` 모드는 OAuth 와 keychain 을 읽지 않으므로 구독 인증 자체가 성립하지 않는다.

이는 축소이지 결함이 아니다. 평가는 "매 PR 마다 자동으로 도는 것"이 아니라 **릴리스 주기마다 사람이 로컬에서 수행하는 활동**으로 정의된다. `.github/workflows/` 에 live 평가 job 을 추가하지 않는다 — 추가할 자격증명이 없다.

## 관련

- `ywc-skill-author` — S2 sub-rubric 의 출처(규칙). 이 Skill 은 준수율을 채점만 함
- `.codex/skills/ywc-codex-toolkit-eval` — Codex Skill/Agent 전용 평가
- `ywc-impl-review` — application 코드를 리뷰. 이 Skill 은 toolkit 자체를 평가
- `scripts/validate.sh` — 이진 구조 게이트. 이 Skill 은 그 위의 graded layer
