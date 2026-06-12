# Release PR List

Release PR に含まれる PR 一覧を抽出し、Author ごとに整理して PR Description を更新する Codex Skill です。

## 概要

`develop` → `main` のような Release PR を作成する際に、Commit Headline から PR 番号を抽出し、Author 情報を引いて `## PR LIST` セクションを書き換えます。

### 主な機能

- Commit Headline の `#<number>` パターンから PR 番号を抽出
- PR を Author Login ごとにまとめ、アルファベット順に整列
- 実行時に PR ごとの Summary を併記するか Userに確認し、同意した場合のみ PR Title をもとに 1 行要約を各 entry へ付加
- `## PR LIST` 以外の既存 Description を保持
- 複数回実行しても同じセクションのみ更新

## 使用方法

```text
/release-pr-list 301
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## 前提条件

- `gh` CLI のインストールと認証が完了していること
- Release PR がすでに作成されていること

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
