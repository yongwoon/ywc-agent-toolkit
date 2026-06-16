<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# UI/UX Review - 混合代码与实时 UI 审计工具

一个 Codex Skill，通过结合静态代码分析和基于 available browser tooling 的实时 UI 探索，从 UI/UX 视角审计项目，并生成优先级 Markdown 报告。

## 概述

此 Skill 回答"我们应该首先改进哪里的 UX？"这一问题，所有发现均有证据支撑。每个问题都引用权威启发法（Nielsen 10 / WCAG 2.2 AA / Material 3 / Apple HIG / 内部设计系统）。

### 主要特性

- 混合审查：静态代码分析 + 实时 UI 探索
- 重点领域：信息架构、视觉设计
- 四级严重程度输出：Critical / High / Medium / Low
- 每条发现包含位置和启发法引用
- 通过 available browser tooling 无障碍树快照实现高效 token 使用

## 使用方法

```text
Review the UI/UX of http://localhost:3000 — focus on the dashboard.
```

```text
Audit usability and Information Architecture of the settings flow.
```

自然语言触发条件在 [SKILL.md](./SKILL.md) 中定义。

## 参考资料

- 领域检查清单和启发法引用存储在 [`references/`](./references) 下
- 报告模板存储在 [`assets/`](./assets) 下
- 工作流和触发短语在 [SKILL.md](./SKILL.md) 中定义

## 实时 UI 工具

此 Skill 优先使用 available browser tooling 进行检查类任务（无障碍树快照、Lighthouse 审计、计算样式、截图）。仅在需要多步骤交互自动化时才使用 Playwright MCP。

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语（摘要）](./README.ko.md)
