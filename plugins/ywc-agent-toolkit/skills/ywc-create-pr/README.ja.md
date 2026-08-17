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
- `--lang` / `--language` で PR title/body prose を `en`、`ja`、`ko`、`zh`、`es` のいずれかにし、task ID、branch name、file path、command、label、明示的な `--title` 値はそのまま保持
- branch に対応する task の `## Spec Reference` を優先確認し、なければ `docs/ywc-plans/` 配下の plan を best-effort で検索して設計背景を PR 本文に追加

## 使用方法

```text
$ywc-create-pr
$ywc-create-pr main
$ywc-create-pr --skip-ci-check
$ywc-create-pr main --skip-ci-check
$ywc-create-pr --lang zh
$ywc-create-pr --language spanish
$ywc-create-pr --plan-doc docs/ywc-plans/20260814-small_example.md
$ywc-create-pr --no-plan-ref
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## 前提条件

- `gh` CLI のインストールと認証が完了していること
- Git Repository の Feature Branch で作業していること

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
- [Chinese (Simplified)](./README.zh.md)
- [Spanish](./README.es.md)
