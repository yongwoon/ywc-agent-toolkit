# ywc-codex-toolkit-eval

この Repository の Codex `ywc-*` Skill と Codex custom Agent の品質を評価する内部管理 Skill です。`inventory_gate.py` で構造 evidence を集め、`score.py` で mechanical axes を採点し、0-4 rubric の judgment pass で最終 grade と改善 backlog を作ります。

この Skill は配布対象ではありません。`tools/codex-internal/skills/ywc-codex-toolkit-eval/` の下だけに置き、`codex/skills/` や `.codex-plugin/skills/` には含めません。

## 使い方

```bash
$ywc-codex-toolkit-eval --target all
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## 出力

- `docs/skill-agent-eval/codex/reports/` — Codex 評価 report
- `docs/skill-agent-eval/codex/scoreboard.md` — rolling scoreboard
- `evals/history.mechanical.json` — reviewed mechanical baseline

## 関連 Skill

- `ywc-skill-author` — Codex Skill 構造と authoring rule の出典
- `.claude/skills/ywc-toolkit-eval` — Claude Code Skill/Agent 評価用の別 Skill
