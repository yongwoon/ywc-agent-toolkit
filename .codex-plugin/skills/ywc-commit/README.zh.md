<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Commit Skill（ywc-commit）

一个 Codex Skill，用于安全地暂存、提交当前会话的更改，并可选择性地推送。

## 概述

此 Skill 自动处理以下事项：

- 仅选择与会话相关的文件进行暂存
- 将逻辑上不同的更改拆分为独立的提交
- 从 `git log` 学习项目的提交风格（`type/scope/message`）并一致应用
- 报告所有已创建提交的简洁摘要

## 使用方法

使用自然语言或斜杠命令请求：

```text
/ywc-commit
```

```text
commit and push
```

```text
commit only the authentication-related files
```

也支持韩语短语：`커밋 해줘`、`커밋푸쉬 ㄱㄱ`、`지금까지 한 작업 커밋`。

## 核心规则

| 规则 | 详情 |
| --- | --- |
| 仅暂存与会话相关的文件 | 仅限本次对话中创建、修改或讨论的文件 |
| 按逻辑单元拆分提交 | 一个提交 = 一个目的 |
| 仅在明确请求时推送 | 由"push"、"푸쉬"、"올려줘"或等效词触发 |
| 禁止使用 `--no-verify` | 修复 hook 失败或报告它们——绝不绕过 |
| 禁止使用 `git add .` | 始终通过明确路径暂存文件 |
| 提交到 main/master 前需确认 | 几乎总是错误的——先询问 |
| 排除密钥和构建产物 | 跳过 `.env*`、`dist/`、`build/`，除非是有意添加的 |
| 默认不添加工具特定的共同作者 trailer | 仅在仓库约定或用户明确要求时包含 |

## 工作流程

```text
第 1 步：评估当前状态
  └─ git status, git diff, git log（学习风格），检查分支

第 2 步：分类已更改的文件
  └─ IN（与会话相关）/ UNKNOWN（来源不明）/ OUT（无关）
  └─ 如发现 UNKNOWN/OUT 文件，向用户展示分类表并获得批准

第 3 步：拆分为逻辑提交
  └─ 为逻辑上不同的更改规划独立提交
  └─ 必要时使用 git add -p 进行 hunk 级别的暂存
  └─ 向用户展示计划的提交（文件 + 草稿消息）并获得批准

第 4 步：编写提交消息
  └─ 从 git log 学习项目风格并准确应用
  └─ 仅在仓库约定或用户要求时包含共同作者 trailer

第 5 步：暂存并提交
  └─ 通过明确路径暂存 → 验证 diff → 使用 heredoc 提交

第 6 步：验证结果
  └─ 检查 git log 和 git status，查找缺失的提交或意外更改

第 7 步：推送（仅在请求时）
  └─ 默认推送；如果没有设置 upstream，使用 -u 标志
  └─ 仅在明确请求时强制推送
```

## 提交消息格式

与项目现有的 `git log` 风格匹配。通用格式：

```text
<type>(<scope>): <summary>

<body — 仅在需要时>
```

**常用类型**（仅使用此仓库已使用的类型）：
`feat`、`fix`、`refactor`、`perf`、`chore`、`docs`、`test`

**Scope**：从 `git log` 模式派生（包名、模块名等）。当更改跨越多个领域时省略。

默认不添加 `Co-Authored-By` trailer。仅当近期提交历史一致使用 AI 共同作者 trailer 或用户明确要求时才添加。如果仓库没有约定且用户要求，使用 `Co-Authored-By: Claude <noreply@anthropic.com>`。

## 报告格式

所有提交完成后：

```text
✅ 已创建 N 个提交 [+ 已推送]
  1. <hash> <type>(<scope>): <summary>
  2. <hash> <type>(<scope>): <summary>
排除的文件：<如有则列出，否则省略>
```

## 错误处理

| 情况 | 行为 |
| --- | --- |
| 发现 UNKNOWN 文件 | 向用户展示分类表并等待批准 |
| Hook 失败 | 绝不使用 `--no-verify`；报告根本原因并停止 |
| 直接提交到 main/master | 先请求用户确认 |
| 非快进推送被拒绝 | 解释情况并提供选项；仅在明确请求时强制推送 |
| 发现密钥或产物文件 | 通知用户并从提交中排除 |

## 集成

此 Skill 与以下 Skill 配合使用：

- **ywc-create-pr** — 在第 3 步内部调用，当需要在创建 PR 前提交未暂存的更改时
- **ywc-sequential-executor** — 可在任务执行的提交步骤中引用

## 示例提示

```text
/ywc-commit
commit and push
commit only the authentication-related files
```
