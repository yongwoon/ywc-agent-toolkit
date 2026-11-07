# Merge Dependabot Skill

> **ユーザー起動専用 Skill** — `/ywc-merge-dependabot` で直接実行します。モデルは自動的に選択せず(`disable-model-invocation: true`)、他の Skill が Skill tool 経由で呼び出すこともできません。

Dependabot が作成した Pull Request を安全に一括 Merge する Claude Code Skill です。

## 概要

Dependabot PR を検出し、事前の安全確認を行ったうえで、PR 番号の昇順で順次処理します。

### 主な機能

- Dependabot PR をまとめて検出して Merge
- Security 関連 PR のみを対象にする Mode を提供
- Dockerfile Base Image 変更、Major Version 更新、CI Status を事前確認
- Conflict 時は `@dependabot rebase` Comment を 1 回だけ投稿して Dependabot の rebase を待機。Major Version 更新は常に Skip して人手 Review に回す
- Parallel-auto は Base Branch に required status check が確認できた PR のみ `--auto` に登録 (Base Branch 名は事前に検証)。Queue は bounded chunk で polling し、30 分の deadline 経過後に残った PR のみ stalled と報告
- **Parallel-auto mode**: lockfile ecosystem ごとに PR を grouping し、GitHub auto-merge queue に直列化を委譲することで大量 PR の wall-clock 時間を短縮
- 処理後に Summary Report を生成

## 使用方法

```text
/ywc-merge-dependabot                          # 全 PR を sequential 処理
/ywc-merge-dependabot security                 # Security PR のみ sequential 処理
/ywc-merge-dependabot parallel-auto            # 全 PR を ecosystem-grouped auto-merge
/ywc-merge-dependabot security parallel-auto   # Security PR のみ ecosystem-grouped auto-merge
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
