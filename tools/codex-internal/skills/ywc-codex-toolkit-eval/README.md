# ywc-codex-toolkit-eval

이 Repository 의 Codex `ywc-*` Skill 과 Codex custom Agent 품질을 평가하는 내부 관리 Skill 입니다. 0-5 rubric 으로 채점하고, scorecard 와 개선 backlog 를 만들어 evaluate -> improve -> re-evaluate cycle 을 구동합니다.

이 Skill 은 배포 대상이 아닙니다. `tools/codex-internal/skills/ywc-codex-toolkit-eval/` 아래에만 두고, `codex/skills/` 또는 `.codex-plugin/skills/` 에 포함하지 않습니다.

## 사용 방법

```bash
$ywc-codex-toolkit-eval --mode full --target all
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## 출력

- `evals/scorecard.md` — Codex Skill/Agent 별 score 와 우선순위 backlog.
- `evals/history.json` — append-only trend history.

## 관련 Skill

- `ywc-skill-author` — 구조와 authoring rule 의 출처.
- `.claude/skills/ywc-toolkit-eval` — Claude Code Skill/Agent 평가용 별도 skill.
