# Retrospective Skill (ywc-retro)

> **ユーザー起動専用 Skill** — `/ywc-retro` で直接実行します。モデルは自動的に選択せず(`disable-model-invocation: true`)、他の Skill が Skill tool 経由で呼び出すこともできません。

Coding session を振り返り、次回の実行から Agent がより良く作業できるよう **環境**(navigation pointer、automated check、coding standard、steering file、tooling、情報アクセス)の改善候補を重要度 (High / Medium / Low) 順に提案する Claude Code Skill です。`mattpocock/skills` の `retro` をベースにしています。

## 概要

- Session の primary source(会話、tool call)を直接読み、根拠を引用
- 7 つのカテゴリで候補を収集: Navigation / Automated checks / Coding standards / Steering files / Tool economy / No-ops / Information access
- 候補は 3 つの lens subagent (judgment / tooling / divergent、`sonnet`) が並列に収集し、clean context の synthesizer (`opus`) が却下理由付きで絞り込む — 振り返り対象である parent session の self-review bias を避けるためで、実行ごとに subagent 4 回分のコストがかかる
- **機械的な違反はルールではなく check に**: 固定パターン・禁止 API・import 形式の違反は lint rule、pre-commit hook、CI job として提案し、判断を要するものだけを文書化された standard として提案
- pre-commit hook も CI もない repo は、それ自体を finding として報告
- 結果を提示する前に credential・token・個人情報を `<REDACTED>` に置換
- 提案のみで適用はしない — 採用するかはユーザーが決定

## 使い方

```text
/ywc-retro
/ywc-retro 昨日 ywc-agentic を実行した session
```

## オプション Reference

- **呼び出し**: `/ywc-retro`
- **入力**: 対象 session (省略時は現在の session)

Flag なし。

## 関連 Skill

- `ywc-skill-author` — Skill の指示が原因の候補のフォローアップ、および振り返りが参照する Writing Levers の出典
- `ywc-review-learnings` — Project 単位の review の好みを蓄積
- `ywc-incident-postmortem` — Production 障害の振り返り (この Skill は Agent session の振り返り)
