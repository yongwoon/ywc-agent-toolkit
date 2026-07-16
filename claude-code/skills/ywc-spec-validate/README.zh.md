<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-spec-validate

一个规范审查代理技能，用于在编写规范之后、运行任务生成器之前验证规范质量。

## 使用方法

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md --tasks tasks/
```

> 同时传入 `--tasks <dir>` 会在任务生成后增加一次 Cross-Artifact（Analyze）校验 — 验证每个 spec 需求都被某个任务覆盖，且没有孤立任务。

## 审查维度

| 维度         | 审查内容                                                                 |
| ------------ | ------------------------------------------------------------------------ |
| 完整性       | 缺少必要项（错误处理、边界情况、分页等）                                 |
| 一致性       | 文档间的术语/格式/数据结构不匹配                                         |
| 可行性       | 是否可以用当前技术栈实现                                                 |
| 代码兼容性   | 与现有数据库 Schema 和 API 路由模式的冲突                                |

## 执行代理

进入阶段 1 之前会先校验 `--spec` 路径：如果文件不存在，立即以 `BLOCKED` 状态终止执行，并报告缺失的路径。

### 阶段 1 — 并行分析（Sonnet × 4）

每个 Subagent 会接收 Step 1 收集的 Project Context 和 spec 文本，并返回：
- **Confirmed findings** — 维度标签、严重程度（Critical / Warning / Suggestion）、文件:行号、描述及改进建议
- **Advisor candidates** — 存在两种合理解释的 Findings（包含具体选择及其后果，每项 ≤100 行）

| Subagent | 负责维度 |
|---|---|
| Completeness Subagent | 完整性 |
| Consistency Subagent | 一致性 |
| Feasibility Subagent | 可行性 |
| Code Compatibility Subagent | 代码兼容性 |

**Aggregate（Step 4b）**：按 `{文件}:{行号}` 合并并去重 Findings。Advisor candidates 数量上限为 `advisor_budget`（默认 2），优先保留 Critical 而非 Warning；被舍弃的候选会记录在报告中。

### 阶段 2 — Advisor（Opus，最多 2 次）

仅针对存在歧义的 Findings，由 Opus Advisor 提供判断。可通过 `--advisor-budget <n>` 控制每次调用的 escalation 次数；`--advisor-budget 0` 时禁用 escalation，并将该 Finding 报告为普通 Suggestion（用于 orchestrator 的成本控制）。

## 输出格式

按严重程度分类的问题（严重 / 警告 / 建议），每项附带文件:行号引用和改进建议。

## 触发条件

本技能的触发条件定义在 [SKILL.md](./SKILL.md) 的 `description` 字段中。

## 本地化版本

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
