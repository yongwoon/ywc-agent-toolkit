<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-agentic (Agentic Orchestrator)

一个 Skill，接收单一的自然语言目标，并自主编排现有的 `ywc-*` skills 直至完成代码实现。通过 **Plan → Execute → Evaluate → Repeat** 循环，它会不断重新规划，直到 `ywc-impl-review` 评估通过或达到用户定义的迭代上限。

仅当 user 明确要求 autonomous end-to-end lifecycle delivery 时使用。generic planning 应路由到 `ywc-plan`，ordinary direct change 应路由到 implementation workflow。

```text
User → Goal → Agent [Plan → Execute → Evaluate → Repeat] → Result
```

## 使用方法

```text
/ywc-agentic "Implement user authentication API"          # 自然语言目标
/ywc-agentic --goal "Add search feature" --max-iterations 5  # 设置迭代上限
/ywc-agentic "Implement payment module" --executor parallel  # 强制指定 executor
/ywc-agentic "Refactoring work" --resume                  # 从现有 tasks/ 恢复
/ywc-agentic "Goal" --dry-run                             # 仅打印 phase 计划
```

## 选项

| 选项                   | 描述                                                                            |
| ---------------------- | ------------------------------------------------------------------------------ |
| `<goal>`               | 要实现的目标的自然语言描述（位置参数，必填）                                     |
| `--goal <text>`        | 位置参数 `<goal>` 的替代形式（若两者都提供，位置参数优先）                       |
| `--max-iterations <n>` | 最大循环迭代次数（默认：3，这是一个绝不会自主提高的安全阀）                       |
| `--executor <mode>`    | 强制指定 executor：sequential / parallel / auto（默认：auto）                    |
| `--tasks-dir <path>`   | task 目录和 agentic-log.md 的所在目录（默认：tasks/）                            |
| `--resume`             | 跳过 Plan Phase 并从现有 tasks/ 恢复                                             |
| `--dry-run`            | 仅打印 phase 计划；不调用任何 skill                                              |
| `--terse`              | 最小化输出（仅 phase 标题和最终报告）                                            |
| `--pr-lang <lang>`     | PR 标题/描述语言（默认：auto，从 CLAUDE.md 推断）                                |

## 执行流程

1. 接收并验证目标
2. 检测项目 context → 决定 Resume / Full Mode
3. Plan Phase — 调用 `ywc-plan`（Re-plan 时使用 `--update-spec`）
4. Task Phase — 调用 `ywc-task-generator`（仅 Medium/Large）
5. Execute Phase — 使用 `--local-merge` 运行 executor（Small Path 使用 `ywc-code-gen`）
6. Evaluate Phase — 针对原始 spec 执行 `ywc-impl-review --git-range`
7. Loop Control — Pass 退出 / Fail 重新规划 / 到达上限时输出部分完成报告
8. Iteration Log — 追加到 `tasks/agentic-log.md`
9. Completion Report

## Small Path 与 Medium/Large Path

| Path              | 条件                                       | 执行方式                                              |
| ----------------- | ----------------------------------------- | ----------------------------------------------------- |
| Small Path        | `ywc-plan` 返回 Small 判定                 | 直接使用 `ywc-code-gen`（无 Task Phase 或 executor）  |
| Medium/Large Path | `ywc-plan` 返回 Medium/Large 判定          | `ywc-spec-validate` → `ywc-task-generator` → executor |

## 被编排的 Skills

`ywc-plan` · `ywc-spec-validate` · `ywc-task-generator` · `ywc-sequential-executor` / `ywc-parallel-executor` · `ywc-impl-review` · `ywc-code-gen`

## 触发

此 Skill 的触发条件定义在 [SKILL.md](./SKILL.md) 的 `description` 字段中。

## 本地化版本

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
