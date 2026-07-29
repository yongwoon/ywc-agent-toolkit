# ywc-implement

承認済みの単一の仕様またはチケットを直接実装する Codex Skill です。

`--spec <repo-relative-path>` または `--ticket <reference>` のどちらか一つだけを受け付けます。承認の証拠と受け入れ条件がなければ `NEEDS_CONTEXT` を返します。

クリーンなベースラインと feature branch を記録し、既存パターンを確認します。動作変更では TDD、focused check、全体検証、`ywc-impl-review` を順に実行し、レビュー後に conventional commit を作成します。PR 作成と force-push は行いません。
