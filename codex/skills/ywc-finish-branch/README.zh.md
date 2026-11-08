<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-finish-branch

一个Codex技能，可在单个调用中将功能分支交付到其基础分支。它涵盖标记PR就绪、CI等待+机器人审查轮询、合并（PR或本地）、合并后验证、标记任务完成和本地分支清理。

## 概述

从`ywc-sequential-executor`和`ywc-parallel-executor`之前分别内联的交付逻辑中进行单一责任提取。给定一个具有通过验证的功能分支的任务，此技能将其一直带到"完成"。

### 关键特性

- **一个地方的模式分派**：`normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **合并后的硬门**：通过`git log -1 --format="%s"`确认合并实际运行
- **完成定义已强制**：将任务目录移至`<tasks-dir>/completed/`并进行验证门
- **机器人审查轮询兼容**：`--bot-action sequential|parallel`与调用者的CI策略匹配
- **工作树路径模式**：`--worktree-path <path>`使用`git -C <path>`确定交付命令范围，同时创建/删除保持与调用者一致
- **PR语言直通**：`--pr-lang en|ja|ko|zh|es`构建`[<TASK_NUMBER>] <translated-slug>`标题，并将相同值作为`--lang <pr-lang>`传递给`ywc-create-pr`，保持机器标识符不变

## 使用

### 默认（基于PR）

```
$ywc-finish-branch --mode normal-pr --branch feature/yk-000001-010-db-create-users \
  --task-name yk-000001-010-db-create-users --base-branch develop
```

现有的无前缀（`000001-010-...`）和旧版数字（`001010-...`）任务名称保持有效，并使用其原始完整名称移动。

### 本地合并

```
$ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### 带延迟推送的范围模式

```
$ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### PR语言

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

### 自然语言触发

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## 模式比较

| 模式 | PR | CI等待 | 合并 | 标记完成 | 清理 |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | 是（委托给`ywc-create-pr`） | 是 | `gh pr merge --delete-branch` | 是 | `git branch -d` |
| `local-merge` | 否 | 否 | `git merge --no-ff` + 推送 | 是 | 是 |
| `draft` | 是 | 否 | 否 | 否 | 否 |
| `skip-ci-wait` | 是（标记就绪） | 否 | 否 | 否 | 否 |
| `per-task-pr` | 是 | 否 | 否 | 否 | 否 |

## 前提条件

- 安装了`gh` CLI并已认证（基于PR的模式）
- 清洁的工作树
- 调用者已通过其验证门（lint / typecheck / test）
- 在`Codex批准设置或项目本地政策文件`中配置的预授权（见`references/local-merge-permissions.md`）

## 使用的工具

`Bash`、`Read`、`Grep`、Task（委托给`ywc-create-pr` / `ywc-handle-pr-reviews`）

## 集成

- **上游**：`ywc-sequential-executor`（替换其步骤5–8）、`ywc-parallel-executor`（替换步骤4e–4f的合并+标记完成部分）
- **内部委托**：`ywc-create-pr`（步骤2）、`ywc-handle-pr-reviews`（步骤4机器人轮询循环）

## 操作安全

远程删除通过这些防护的顺序进行：分支允许列表加`git check-ref-format "refs/heads/$branch"`、单个固定的`origin`推送URL、通过`env -u GH_HOST gh`进行的主机资格限定的存储库绑定（及其用于复刻的父库）、精确的远程提示、对预期基础和当前提示的无条件合并PR检查、作为最后一个检查的零个开放PR计数，以及精确提示租赁删除。在开放PR检查和删除之间仍存在短竞争窗口。
