<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-spec-ready (Spec Readiness Loop)

一个将 `ywc-plan` 产出的 spec 自动收敛到 `ywc-spec-validate` `DONE` 状态的 Skill。每次迭代运行 `ywc-spec-validate`；在 `DONE_WITH_CONCERNS` 时通过 `ywc-plan --update-spec` 追加一条修订并重新验证。到达 `DONE` 时打印 `ywc-task-generator` 交接内容并**停止**（它绝不会自动运行 task-generator）。

```text
spec ──> [ywc-spec-validate ──DONE_WITH_CONCERNS──> ywc-plan --update-spec]* ──DONE──> handoff
```

现有的 `ywc-agentic` loop 围绕 `ywc-impl-review`（code evaluation）运转，且只运行 `ywc-spec-validate` **一次**。此 Skill 填补了缺失的内层 loop —— **多迭代 spec 收敛**。

## Usage

```text
/ywc-spec-ready --spec docs/ywc-plans/feature.md                       # Default (max 5 iterations)
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-iterations 8    # Set iteration ceiling
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-advisor-calls 2 # Advisor cost guard
/ywc-spec-ready --spec docs/ywc-plans/feature.md --dry-run             # Print command sequence only
```

## Options

| Option                   | Description                                                       |
| ------------------------ | ---------------------------------------------------------------- |
| `--spec <path>`          | 要收敛的 spec 文件（必需，一个 `ywc-plan` output）。缺失 → `NEEDS_CONTEXT` |
| `--max-iterations <n>`   | Validation loop 上限（默认：5，绝不自主提高）  |
| `--max-advisor-calls <n>`| 所有迭代中的 Opus advisor 总预算（默认：4，成本保护） |
| `--log <path>`           | Append-only loop log（默认：`<spec-dir>/<slug>.spec-ready-log.md`） |
| `--dry-run`              | 仅打印计划的命令序列；不调用任何 sibling skill |
| `--lang <lang>`          | Report/handoff 语言（默认：auto，从 CLAUDE.md 推断） |
| `--focus <area>`         | 转发给 `ywc-spec-validate`                                  |
| `--format <fmt>`         | 转发给 `ywc-spec-validate`（markdown / html）               |
| `--terse`                | 最小化输出（仅 phase headers 和最终 report）         |

## Execution Flow

1. Pre-flight —— 验证 `--spec` 存在，推导 `<slug>`，处理 `--dry-run`
2. Iteration Loop —— `ywc-spec-validate` → Status Routing → （在 DONE_WITH_CONCERNS 时）guard check → `ywc-plan --update-spec` → log → 重复
3. Hard Stop —— 在 `BLOCKED` / `NEEDS_CONTEXT` / `SOCRATIC` / 无法解析时立即停止
4. Handoff —— 在 `DONE` 时，打印 `ywc-task-generator` 指引并停止
5. Completion Report —— 单一 report（最后一行是 Completion Status）

## Loop-prevention Guards

| Guard | Stop condition |
| --- | --- |
| Iteration cap | `iteration >= --max-iterations` 且 status ≠ DONE |
| Non-decreasing Criticals | Critical count 连续 2 次迭代增加或持平（signature overlap） |
| Repeated signature | 重新 plan 后，相同的 Critical signature 在连续迭代中再次出现 |
| Identical amendment scope | 新的 amendment scope 等于上一个（recursion guard） |

完整规则见 [references/convergence.md](references/convergence.md)，log schema 见 [references/loop-log.md](references/loop-log.md)。

## Triggering

此 Skill 的 trigger 条件定义在 [SKILL.md](./SKILL.md) 的 `description` 字段中。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
