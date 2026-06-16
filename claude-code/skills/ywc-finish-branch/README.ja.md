# ywc-finish-branch

Feature Branch を Base Branch に deliver する Claude Code Skill です。Mark-PR-ready、CI Wait + Bot Review Polling、Merge (PR または Local)、Post-Merge Verification、Mark Task Complete、Local Branch Cleanup を 1 回の呼び出しで処理します。

## Overview

`ywc-sequential-executor` と `ywc-parallel-executor` がそれぞれ inline で持っていた delivery ロジックを切り出した単一責任 Skill です。1 つの Feature Branch、1 つの Task に対し、verification 完了時点から「done」状態までの全フローを担当します。

### 主な特徴

- **Mode 分岐の一元化**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Post-merge Hard Gate**: `git log -1 --format="%s"` で merge の実行を検証
- **Mark Task Complete の Definition of Done を強制**: `<tasks-dir>/completed/` への移動を verification 含めて実施
- **Bot Review Polling 互換**: `--bot-action sequential|parallel` で caller の CI 戦略に合わせて挙動を切替
- **Worktree lifecycle 非関与、ただし worktree 内動作は対応**: worktree の生成/削除は caller 責任だが、`--worktree-path <path>` を渡すと Steps 1・5–8 のすべての git コマンドを `git -C <path>` で実行し、`ywc-sequential-executor --worktree` が作成した run worktree の中で delivery 可能 (delivery の意味は不変、working dir のみ変更)

## 使い方

### 基本 (PR-based)

```
/ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop
```

### Local Merge

```
/ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### Range mode で push を遅延

```
/ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### 自然言語トリガー

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## Mode 比較

| Mode | PR | CI 待機 | Merge | Mark Complete | Cleanup |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | yes (`ywc-create-pr` に委譲) | yes | `gh pr merge --delete-branch` | yes | `git branch -d` |
| `local-merge` | no | no | `git merge --no-ff` + push | yes | yes |
| `draft` | yes | no | no | no | no |
| `skip-ci-wait` | yes (mark ready) | no | no | no | no |
| `per-task-pr` | yes | no | no | no | no |

## 前提条件

- `gh` CLI のインストールと認証 (PR-based モード)
- Working tree が clean
- caller が verification gate (lint / typecheck / test) を通過済み
- Pre-authorization 設定済み (`.claude/settings.local.json` — `references/local-merge-permissions.md` 参照)

## 使用 Tool

`Bash`, `Read`, `Grep`, Task (`ywc-create-pr` / `ywc-handle-pr-reviews` への委譲)

## 呼び出し関係

- **Upstream**: `ywc-sequential-executor` (Steps 5–8 を委譲), `ywc-parallel-executor` (Step 4e–4f の一部を委譲)
- **Internal delegation**: `ywc-create-pr` (Step 2), `ywc-handle-pr-reviews` (Step 4 の bot polling ループ内)
