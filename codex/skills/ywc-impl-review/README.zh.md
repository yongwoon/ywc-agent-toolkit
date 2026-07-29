<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-impl-review

一个 Skill，在实现完成后创建 PR 前执行全面的实现合规性验证。并行运行 Phase 1 的 5 个 Agent（Architecture / Design / Devex / Security / QA — 其中 4 个使用 Sonnet，1 个使用 Haiku），并将存在歧义的 finding 上报至 Phase 2 Opus Advisor。

## 使用方法

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --base main
```

`--working-tree` 无需创建 commit，即可审查 staged、unstaged 和 untracked 的 source 改动。`--base <ref>` 审查 `git merge-base <ref> HEAD` 到 `HEAD` 的范围，并报告 supplied ref 和 resolved merge-base。`--git-range A..B` 仍是显式的双端点比较。四种 target mode 中必须且只能指定一种，彼此互斥。

## 执行 Agent

| Agent | 验证范围 |
| --------------------- | ----------------------------------------------------------------------- |
| Architecture (sonnet) | Module 边界、Layering、Dependency 方向、结构性规范符合性 |
| Design (sonnet) | API/Interface 设计、Naming、Signature、Error Model、Contract 规范符合性 |
| Devex (sonnet) | 可读性、Error Message、Logging、Documentation、Debuggability |
| Security (sonnet) | OWASP Top 10 分析 |
| QA (haiku) | Test Coverage 缺口、缺失的 Test Case |

Phase 2（opus）——仅对上述 5 个 Agent 中存在歧义的 finding 进行升级复审（Budget：默认 5 次，可通过 `--advisor-budget` 调整，共享）。

## 输出格式

集成报告——Aggregator 合并 Phase 1 的 finding 与 Phase 2 Advisor 的判定，按严重程度分类，提供优先级修复建议。每条 finding 均带有 `[P1]`/`[P2]` marker，标示其 Phase 1/Phase 2 出处。

## 触发条件

此 Skill 的触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。

## 本地化版本

- [英语](./README.en.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
- [中文](./README.zh.md)
- [西班牙语](./README.es.md)
