# Create PR

変更を Commit し、リポジトリの PR Template に従って Draft PR を作成する Codex Skill です。

## 概要

Feature Branch での作業完了後、Commit 作成から Draft PR 作成までの流れを自動化します。

### 主な機能

- `develop` → `main` → `master` の順で Base Branch を自動判定
- `.env`、`*.key`、`*.pem` などの機密ファイルを Security Check
- push 前に lint、format、typecheck、test などの CI Check を実行
- `.github/pull_request_template.md` があれば自動適用
- すべての PR を Draft で作成

## 使用方法

```text
/create-pr
/create-pr main
/create-pr --skip-ci-check
/create-pr main --skip-ci-check
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## 前提条件

- `gh` CLI のインストールと認証が完了していること
- Git Repository の Feature Branch で作業していること

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
