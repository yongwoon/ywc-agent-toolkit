# ywc-codex-toolkit-eval

この Repository の Codex `ywc-*` Skill と Codex custom Agent を評価する内部管理 Skill です。0-5 の rubric で採点し、scorecard と改善 backlog を作成して evaluate -> improve -> re-evaluate の cycle を回します。

この Skill は配布対象ではありません。`tools/codex-internal/skills/ywc-codex-toolkit-eval/` にのみ配置し、`codex/skills/` や `.codex-plugin/skills/` には含めません。

## 使い方

```bash
$ywc-codex-toolkit-eval --mode full --target all
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## 出力

- `evals/scorecard.md` — Codex Skill/Agent ごとの score と優先順位付き backlog。
- `evals/history.json` — append-only の trend history。

## 関連 Skill

- `ywc-skill-author` — 構造と authoring rule の source。
- `.claude/skills/ywc-toolkit-eval` — Claude Code Skill/Agent 評価用の別 Skill。
