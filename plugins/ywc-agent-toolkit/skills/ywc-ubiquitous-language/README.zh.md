<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-ubiquitous-language

一个用于创建和维护项目通用语言文档的 Skill — 这是一个共享领域词汇表，使开发者、领域专家和 LLM 在规范术语使用上保持一致。生成并管理 `docs/ubiquitous-language.md`。

支持三种模式：**new**（通过访谈从头创建）、**extract**（从现有代码库中发现术语）和 **update**（对现有文档进行增量修订）。

## 使用场景

- 在新项目开始时创建共享领域词汇表
- 分析现有代码库，将隐式领域术语正式化为文档
- 添加新功能后更新词汇表
- 通过 CLAUDE.md 中的 `@docs/ubiquitous-language.md` 让 LLM 自动访问项目词汇

## 使用方法

```bash
/ywc-ubiquitous-language
```

或通过自然语言：

> "Create a ubiquitous language document"
> "Extract domain terms from the codebase"
> "Update our ubiquitous language"
> "Create a domain glossary"

### 模式自动检测

| 条件 | 自动选择的模式 |
|-----------|------------------|
| `docs/ubiquitous-language.md` 存在 | `update` |
| 文件不存在 + 找到源文件（`src/`、`app/` 等） | `extract` |
| 文件不存在 + 无源文件 | `new` |

使用 `--mode new|extract|update` 覆盖。

## 输入

- （可选）领域描述 — "This is a B2B e-commerce platform"
- （可选）`--mode new|extract|update` — 强制指定模式
- （可选）`--context <name>` — 限定到单个限界上下文
- （可选）`--ddd` — 添加 DDD 类型列（Entity / Value Object / Aggregate / Domain Event / Policy）
- （可选）`--output <path>` — 输出文件路径（默认：`docs/ubiquitous-language.md`）

## 输出

- `docs/ubiquitous-language.md` — 按限界上下文组织的术语表
- 完成后：打印提示以将 `@docs/ubiquitous-language.md` 添加到 CLAUDE.md

## 输出示例

```markdown
# Ubiquitous Language — ShopBot

<!-- updated: 2026-05-02 -->

## Bounded Contexts

| Context | Responsibility |
|---------|---------------|
| Order   | Order lifecycle from placement through fulfillment |

---

## Order

| Term      | Korean    | Definition                                          | Synonyms to Avoid |
|-----------|-----------|-----------------------------------------------------|------------------|
| Order     | 주문      | A confirmed request by a Customer to purchase items | Cart, Purchase    |
| OrderItem | 주문 항목 | A single product-quantity pair within an Order      | LineItem, CartItem |
```

## 相关 Skills

- `ywc-plan` — 在编写规范前建立词汇时一起使用
- `ywc-project-docs` — 管理整体 docs/ 目录结构（上游）
- `ywc-spec-validate` — 检查规范术语是否与通用语言匹配
- `ywc-task-generator` — 下游：建立词汇后分解工作
- `ywc-code-gen` — 在代码生成过程中应用词汇表中的规范命名
