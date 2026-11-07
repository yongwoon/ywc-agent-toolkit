<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-finish-branch

一个 Codex 技能，可在一次调用中将功能分支提交到基础分支。它包括标记 PR 就绪、CI 等待 + Bot 评审轮询、合并（PR 或本地）、合并后验证、标记任务完成和本地分支清理。

## 概述

从 `ywc-sequential-executor` 和 `ywc-parallel-executor` 之前分别内联的交付逻辑中提取的单一职责。给定一个功能分支用于一个已通过验证的任务，此技能将其一直带到"完成"状态。

### 主要特性

- **单一位置的模式分发**：`normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **合并后的硬网关**：通过 `git log -1 --format="%s"` 确认合并实际运行
- **强制执行完成定义**：将任务目录移动到 `<tasks-dir>/completed/`，带验证网关
- **Bot 评审轮询兼容**：`--bot-action sequential|parallel` 与调用者的 CI 策略匹配
- **工作树路径模式**：`--worktree-path <path>` 使用 `git -C <path>` 限制交付命令的范围，而创建/删除由调用者保留
- **PR 语言透传**：`--pr-lang en|ja|ko|zh|es` 构建 `[<TASK_NUMBER>] <translated-slug>` 标题，并将相同值作为 `--lang <pr-lang>` 传递给 `ywc-create-pr`，保持机器标识符不变

## 使用

### 默认值（基于 PR）

```
$ywc-finish-branch --mode normal-pr --branch feature/yk-000001-010-db-create-users \
  --task-name yk-000001-010-db-create-users --base-branch develop
```

现有未加前缀的（`000001-010-...`）和旧版数字（`001010-...`）任务名称保持有效，并使用其原始全名进行移动。

### 本地合并

```
$ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### 范围模式，延迟推送

```
$ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### PR 语言

```
$ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop --pr-lang zh
```

支持的值：`en`、`ja`、`ko`、`zh`、`es`。

### 工作树路径模式

```
$ywc-finish-branch --mode local-merge --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --worktree-path ../worktree-run
```

### 自然语言触发器

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## 模式比较

| 模式 | PR | CI 等待 | 合并 | 标记完成 | 清理 |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | 是（委托给 `ywc-create-pr`） | 是 | `gh pr merge --delete-branch` | 是 | `git branch -d` |
| `local-merge` | 否 | 否 | `git merge --no-ff` + 推送 | 是 | 是 |
| `draft` | 是 | 否 | 否 | 否 | 否 |
| `skip-ci-wait` | 是（标记就绪） | 否 | 否 | 否 | 否 |
| `per-task-pr` | 是 | 否 | 否 | 否 | 否 |

## 前提条件

- 已安装并认证 `gh` CLI（基于 PR 的模式）
- 工作树清洁
- 调用者已通过其验证网关（lint / typecheck / test）
- 在 `Codex 批准设置或项目本地策略文件` 中配置了预授权（参见 `references/local-merge-permissions.md`）

## 使用的工具

`Bash`、`Read`、`Grep`、Task（委托给 `ywc-create-pr` / `ywc-handle-pr-reviews`）

## 集成

- **上游**：`ywc-sequential-executor`（替换其第 5–8 步）、`ywc-parallel-executor`（替换合并 + 标记完成的第 4e–4f 部分）
- **内部委托**：`ywc-create-pr`（第 2 步）、`ywc-handle-pr-reviews`（第 4 步 bot 轮询循环）

## 操作安全

远程删除分别通过这些防护：分支允许列表加 `git check-ref-format "refs/heads/$branch"`、单个固定的 `origin` 推送 URL、通过 `env -u GH_HOST gh` 限定主机的存储库（及其父级 fork）、确切的远程提示、对预期基础和当前提示的无条件合并 PR 检查，以及作为最后检查的零个开放 PR 计数，以及确切提示租期删除。在开放 PR 检查和删除之间仍然存在短暂的竞争窗口。
