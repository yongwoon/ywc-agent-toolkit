# Merge Dependabot Skill

Dependabot が作成した Pull Request を安全に一括 Merge する Codex Skill です。

## 概要

Dependabot PR を検出し、事前の安全確認を行ったうえで、PR 番号の昇順で順次処理します。

### 主な機能

- Dependabot PR をまとめて検出して Merge
- Security 関連 PR のみを対象にする Mode を提供
- Dockerfile Base Image 変更、Major Version 更新、CI Status を事前確認
- 可能な場合は Conflict 解決を試行
- 処理後に Summary Report を生成

## 使用方法

```text
/merge-dependabot
/merge-dependabot security
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## 前提条件

- `gh` CLI のインストールと認証が完了していること
- Repository に対する Merge 権限を持っていること
- Dependabot PR が存在していること

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
