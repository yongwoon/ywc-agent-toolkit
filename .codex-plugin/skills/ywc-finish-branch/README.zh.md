<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-finish-branch

一个 Codex Skill，通过单次调用将 Feature 分支交付到基础分支。涵盖标记 PR 为可审查状态、CI 等待 + Bot 审查轮询、合并（PR 或本地）、合并后验证、标记任务完成以及本地分支清理。

## 概述

这是从 `ywc-sequential-executor` 和 `ywc-parallel-executor` 之前分别内联的交付逻辑中提取出的单一职责组件。给定一个通过验证的 Feature 分支对应的任务，此 Skill 将其带到"完成"状态。

### 主要特性

- **单一位置的模式调度**：`normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **合并后硬性关卡**：通过 `git log -1 --format="%s"` 确认合并实际执行
- **强制执行完成定义**：将任务目录移动到 `<tasks-dir>/completed/` 并设有验证关卡
- **兼容 Bot 审查轮询**：`--bot-action sequential|parallel` 与调用者的 CI 策略匹配
- **Worktree 无关**：将 worktree 生命周期留给并行执行器，保持清晰的职责边界

## 使用方法

### 默认（基于 PR）

```
/ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop
```

### 本地合并

```
/ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### 延迟推送的范围模式

```
/ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### 自然语言触发词

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## 模式对比

| 模式 | PR | CI 等待 | 合并 | 标记完成 | 清理 |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | 是（委托给 `ywc-create-pr`） | 是 | `gh pr merge --delete-branch` | 是 | `git branch -d` |
| `local-merge` | 否 | 否 | `git merge --no-ff` + push | 是 | 是 |
| `draft` | 是 | 否 | 否 | 否 | 否 |
| `skip-ci-wait` | 是（标记为就绪） | 否 | 否 | 否 | 否 |
| `per-task-pr` | 是 | 否 | 否 | 否 | 否 |

## 前提条件

- `gh` CLI 已安装并完成身份验证（基于 PR 的模式）
- 干净的工作树
- 调用者已通过其验证关卡（lint / typecheck / test）
- 在 `Codex approval settings or the project-local policy file` 中配置了预授权（参见 `references/local-merge-permissions.md`）

## 使用的工具

`Bash`、`Read`、`Grep`、Task（委托给 `ywc-create-pr` / `ywc-handle-pr-reviews`）

## 集成

- **上游**：`ywc-sequential-executor`（替换其步骤 5–8）、`ywc-parallel-executor`（替换步骤 4e–4f 的合并 + 标记完成部分）
- **内部委托**：`ywc-create-pr`（步骤 2）、`ywc-handle-pr-reviews`（步骤 4 Bot 轮询循环）
