# Handoff Skill (ywc-handoff)

> **ユーザー起動専用 Skill** — `/ywc-handoff` で直接実行します。モデルは自動的に選択せず(`disable-model-invocation: true`)、他の Skill が Skill tool 経由で呼び出すこともできません。

現在の会話を、新しい Agent session が引き継げる handoff 文書に圧縮する Claude Code Skill です。`mattpocock/skills` の `handoff` をベースにしています。

## 概要

- Goal / State / Decisions / Dead ends / Next step / Waiting on user / References / Suggested skills の 8 セクションで作成
- State の各 thread は `gh pr view` / `git branch` で確認した status tag を 1 つ付けて始め、確認できない場合は `[unverified]` と理由を記録
- Waiting on user にはユーザーだけが下せる判断のみを call / pick / evidence / risk で記録 (なければ `N/A — nothing waits on the user`)
- Spec、plan、ADR、issue、commit、diff など既存の成果物は **コピーせず path・URL で参照**
- API key、password、token、個人情報はファイルに書き込む **前に** `<REDACTED>` に置換 (本文、code block、log、URL、ファイル名、task 名すべて)
- 保存先は OS の一時 Directory (`${TMPDIR:-/tmp}`) — canonical path が repository の外にある場合のみ保存し、`mktemp` で新規ファイルを作成して mode `0600` を確認

## 使い方

```text
/ywc-handoff
/ywc-handoff 次の session では PR review 対応のみ進める
```

## オプション Reference

- **呼び出し**: `/ywc-handoff`
- **入力**: 次の session の用途 (任意) — 指定すると各セクションをその用途に合わせて作成

Flag なし。
