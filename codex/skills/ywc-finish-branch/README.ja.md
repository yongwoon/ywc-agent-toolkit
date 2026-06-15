# ywc-finish-branch

Feature Branch を Base Branch に deliver する Codex Skill です。Mark-PR-ready、CI Wait + Bot Review Polling、Merge (PR または Local)、Post-Merge Verification、Mark Task Complete、Local Branch Cleanup を 1 回の呼び出しで処理します。

## Overview

`ywc-sequential-executor` と `ywc-parallel-executor` がそれぞれ inline で持っていた delivery ロジックを切り出した単一責任 Skill です。1 つの Feature Branch、1 つの Task に対し、verification 完了時点から「done」状態までの全フローを担当します。

### 主な特徴

- **Mode 分岐の一元化**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Post-merge Hard Gate**: `git log -1 --format="%s"` で merge の実行を検証
- **Mark Task Complete の Definition of Done を強制**: `<tasks-dir>/completed/` への移動を verification 含めて実施
- **Bot Review Polling 互換**: `--bot-action sequential|parallel` で caller の CI 戦略に合わせて挙動を切替
- **Worktree-path mode**: `--worktree-path <path>` で sequential run-level worktree 内の delivery を `git -C <path>` 기준にし、作成/削除は caller が保持

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

### Worktree path mode

```
/ywc-finish-branch --mode local-merge --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --worktree-path ../worktree-run
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
- Pre-authorization 設定済み (`Codex approval settings or the project-local policy file` — `references/local-merge-permissions.md` 参照)

## 使用 Tool

`Bash`, `Read`, `Grep`, Task (`ywc-create-pr` / `ywc-handle-pr-reviews` への委譲)

## 呼び出し関係

- **Upstream**: `ywc-sequential-executor` (Steps 5–8 を委譲), `ywc-parallel-executor` (Step 4e–4f の一部を委譲)
- **Internal delegation**: `ywc-create-pr` (Step 2), `ywc-handle-pr-reviews` (Step 4 の bot polling ループ内)
