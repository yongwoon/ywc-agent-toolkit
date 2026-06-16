# Handle PR Reviews

PR Review Comment を確認し、必要な修正を反映したうえで各 Thread に返信する Codex Skill です。

## 概要

PR Review 後の反復作業を自動化します。明確な修正依頼はそのまま反映し、判断が必要な Comment はユーザー確認に回します。

### 主な機能

- Comment を修正依頼、論点あり、質問、処理済みに分類
- 同じファイルの Comment をまとめて処理
- Reviewer の言語に合わせて返信文を作成
- 既に処理済みまたは返信済みの Comment は Skip

## 使用方法

```text
/handle-pr-reviews
/handle-pr-reviews 123
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## 前提条件

- `gh` CLI のインストールと認証が完了していること
- PR が存在する Branch で実行すること

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
