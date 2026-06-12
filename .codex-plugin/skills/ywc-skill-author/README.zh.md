<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-skill-author

一个用于编写新 ywc-* 技能并重构现有技能的**元技能**。它将从分析 18 个生产级 ywc-* 技能中提炼出的规范规则（Frontmatter 格式、理性化防御、多语言触发器、渐进式披露等）编码化，使 LLM 自动遵循该标准。

## 使用场景

- 从零开始编写全新的 ywc-* 技能。
- 重构现有 ywc-* 技能的 frontmatter、正文章节或参考文档。
- 对照规范规则集审计 18 个 ywc-* 技能。

## 调用方式

```bash
/ywc-skill-author
```

或通过自然语言：

> "Create a new ywc skill"
> "Audit my ywc skill against the rules"
> "Upgrade ywc skill structure"

## 输入

- 新技能：技能目的和主要触发场景。
- 审计：目标技能目录的路径。

## 输出

- 遵循标准结构的 SKILL.md（Frontmatter + 理性化防御 + 工作流 + 验证清单）。
- 适当情况下的补充 `references/` 文件。
- 完整的 README 语言集合（`README.md`、`README.en.md`、`README.ja.md`、`README.ko.md`）。

## 核心规则

本技能强制执行的标准包括：

- **必选规则**：Frontmatter / 正文 / 文件系统（A1–A13）。
- **推荐规则**：情境性指南（B1–B7）。
- **格式约定**：韩语散文配英语技术术语、多语言触发器等。
- **反模式**：工作流摘要式描述、桩代码、`@` 交叉引用及类似陷阱。

完整规范请参阅 `SKILL.md` 及 `references/` 下的四份参考文档。

## 相关技能

- `ywc-task-generator` — 采用相同的多语言策略和参考文档提取模式。
- 所有 ywc-* 技能 — 必须遵守此处定义的规则。

## 参考文档

- `references/skill-template.md` — 新技能的起始模板。
- `references/rationalization-defense-cookbook.md` — 编写理性化防御表格的指南。
- `references/description-anti-patterns.md` — 描述字段中应避免的反模式。
- `references/cross-skill-graph.md` — 18 个 ywc-* 技能的依赖关系和交叉引用图。
