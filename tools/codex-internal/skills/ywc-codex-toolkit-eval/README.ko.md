# ywc-codex-toolkit-eval

이 Repository의 Codex `ywc-*` Skill과 Codex custom Agent 품질을 평가하는 내부 관리 Skill입니다. `inventory_gate.py`로 구조 증거를 모으고, `score.py`로 mechanical axes를 채점한 뒤, 0-4 rubric 기반 judgment pass로 최종 grade와 개선 backlog를 만듭니다.

이 Skill은 배포 대상이 아닙니다. `tools/codex-internal/skills/ywc-codex-toolkit-eval/` 아래에만 두고, `codex/skills/` 또는 `.codex-plugin/skills/`에 포함하지 않습니다.

## 사용 방법

```bash
$ywc-codex-toolkit-eval --target all
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## 출력

- `docs/skill-agent-eval/codex/reports/` — Codex 평가 report
- `docs/skill-agent-eval/codex/scoreboard.md` — rolling scoreboard
- `evals/history.mechanical.json` — reviewed mechanical baseline

## 관련 Skill

- `ywc-skill-author` — Codex Skill 구조와 authoring rule의 출처
- `.claude/skills/ywc-toolkit-eval` — Claude Code Skill/Agent 평가용 별도 Skill
