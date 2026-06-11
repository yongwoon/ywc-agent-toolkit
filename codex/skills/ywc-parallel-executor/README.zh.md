<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-parallel-executor（并行执行器）

一个使用 Agent 并行执行由 task-generator 生成的任务的 Skill。分析 dependency-graph.md 以在 Git Worktree 隔离下执行基于 Wave 的并行执行。

## 使用方法

```text
/ywc-parallel-executor 000001-010-db-create-events           # 单个任务
/ywc-parallel-executor 000001-010..000002-040                # 范围（并行）
/ywc-parallel-executor --all                                 # 执行全部
/ywc-parallel-executor 000001-010..000002-040 --review       # 并行 + 自动审查
/ywc-parallel-executor 000001-010..000002-040 --local-merge  # 本地合并，无 PR
/ywc-parallel-executor 000001-010..000002-040 --draft        # 创建草稿 PR
```

## 选项

| 选项 | 描述 |
|------|------|
| `--tasks-dir <path>` | 任务目录路径（默认：tasks/） |
| `--review` | 每个任务完成后自动运行 `ywc-impl-review`（可组合） |
| `--local-merge` | 无 PR，仅推送到基础分支（默认行为） |
| `--draft` | 所有任务完成后创建草稿 PR |
| `--per-task-pr` | 每个任务创建独立 PR |

## 执行流程

1. 解析 dependency-graph.md
2. 规划 Wave（拓扑排序）
3. 按 Wave 执行：创建 Worktree → 并行 Agent 执行 → 合并 → 删除 Worktree

## 任务 → Agent 自动映射

| 类别 | Agent |
|------|-------|
| db, api, domain, lib, worker | Backend Agent (sonnet) |
| ui | Frontend Agent (sonnet) |
| test | QA Agent (sonnet) |
| infra | DevOps Agent (sonnet) |
| refactor | Reviewer Agent (opus) |

使用 Agent Hint 覆盖：
```markdown
## Parallel Execution Metadata
- Agent Hint: frontend
```

## 与 sequential-executor 的比较

| 场景 | 推荐工具 |
|------|---------|
| 小范围（1-3 个任务） | sequential-executor |
| 强顺序依赖 | sequential-executor |
| 大范围（4+ 个任务） | /ywc-parallel-executor |
| 可并行任务较多 | /ywc-parallel-executor |

## 触发条件

此 Skill 的触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。

## 本地化版本

- [英语](./README.en.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
