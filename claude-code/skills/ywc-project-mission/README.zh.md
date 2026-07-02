<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-project-mission

一个将项目持久的 Mission / North-Star、可衡量的 Success Criteria 和 Out-of-Scope 非目标持久化到 `docs/project-mission.md` 的 skill——这是一个已提交的、runtime 无关的 Markdown 文件。它遵循与 `ywc-review-learnings` 相同的 stateful-file 架构：`ywc-plan` 在澄清任何新请求之前加载此文件，因此每个 planning session 都由同一个 north-star 来框定，而不是每次都从头重新推导。

关键理念是：与功能上线后即被丢弃的一次性 plan 不同，Mission 记录了超越任何单个功能的*持久*意图。每个条目都带有其出处和日期，因此读者可以区分当前的承诺和已放弃的方向。

## 支持的模式

- **read**——加载 Mission 以框定 planning（通常由 `ywc-plan` 调用）
- **update**——从已确认的来源捕获或修订 Mission / Success Criteria / 非目标
- **list**——显示当前的 Mission
- **curate**——弃用陈旧或被取代的条目（绝不硬删除）

## 何时使用

- 当你想在项目级别持久化由一次 brainstorm 产生的 Mission（What+Why）和 Success Criteria（Done When）时
- 当你希望 `ywc-plan` 从同一个 Mission 来框定其问题和 Acceptance Criteria，而不是每个 session 都重新推导 north-star 时
- 当你想显式记录持久的非目标（"这个项目永远不会做 X"）时
- 当你想通过将 `@docs/project-mission.md` 添加到 CLAUDE.md 让 LLM 自动理解项目 Mission 时

## 使用方法

```bash
/ywc-project-mission
```

或通过自然语言触发：

> "Remember this project's mission"
> "Capture the success criteria"
> "What is the current project mission?"

## 输入

- （可选）`--mode read|update|list|curate`——强制指定一个模式（省略时自动检测）
- （可选）`--source brainstorm|plan`——update 模式中 Mission/criterion 的出处（默认 `brainstorm`）
- （可选）`--output <path>`——mission 文件路径（默认 `docs/project-mission.md`）
- （可选）`--dry-run`——显示 CHANGESET 而不写入

## 输出

- `docs/project-mission.md`——Mission / North-Star、Success Criteria 表（`ID | Criterion | Source | Added | Status`）、Out of Scope、一个自动维护的 Change Log
- update 时：呈现一个 ADD / MODIFY / DEPRECATE CHANGESET，仅写入已确认的条目，打印一个 `Mission updated` 确认块
- 首次创建文件时：仅打印一次 `@docs/project-mission.md` CLAUDE.md 激活提示
- 幂等重新运行：空的 CHANGESET → 不写入文件，不更新日期

## 相关 Skill

- `ywc-brainstorm`——Step 6 Handoff 提供通过 `update --source brainstorm` 持久化 Mission（What+Why）和 Success Criteria（Done When）的选项（opt-in）
- `ywc-plan`——Step 1 以 read 模式加载 Mission 以框定问题并播种 Acceptance Criteria
- `ywc-review-learnings`——相同的按项目 stateful-file 架构（read/update/list/curate，用户确认的写入），不同的领域（持久意图 vs review 偏好）
- `ywc-ubiquitous-language`——管理领域*词汇*；此 skill 存储领域*意图*（不要混淆二者）
