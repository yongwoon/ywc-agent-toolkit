# Handle PR Reviews

PR Review Comment を確認し、必要な修正を反映したうえで各 Thread に返信する Claude Code Skill です。

## 概要

PR Review 後の反復作業を自動化します。明確な修正依頼はそのまま反映し、判断が必要な Comment はユーザー確認に回します。

PR を「対応」するとは、単に Comment へ返信することではなく PR を **Mergeable** な状態にすることです。そのため **3 つの独立した Gate** —（1）Review Comment、（2）CI Status、（3）Merge-readiness（Conflict）— を **毎回の実行で** すべて確認します。Comment が 0 件でも CI が Red だったり base と Conflict することがあるため、CI・Conflict Gate は Skip しません。

### 主な機能

- Comment を修正依頼、論点あり、質問、処理済みに分類
- 同じファイルの Comment をまとめて処理
- Reviewer の言語に合わせて返信文を作成
- 既に処理済みまたは返信済みの Comment は Skip
- Comment 処理後に CI 失敗と base Conflict を確認し、PR を Mergeable な状態で締める（Comment が 0 件でも両 Gate は常に実行）

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
