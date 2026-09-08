# Mine Review History

Merge 済み PR の Bot Review Comment を限定された範囲で一括調査し、繰り返す欠陥 Class を確認付きの review-learning 候補として提示する Codex Skill です。`--limit` または `--since` が必要で、再発数は異なる PR 数で数えます。解決と後続修正、または理由付きの人間の却下が確認できない証拠は除外します。

ローカルの永続書き込みは `$ywc-review-learnings --mode update --source mining` に委譲し、共有カタログは Maintainer 提案だけを出力します。

詳細は [SKILL.md](./SKILL.md) を参照してください。
