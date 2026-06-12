<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-spec-validate

一个规范审查代理技能，用于在编写规范之后、运行任务生成器之前验证规范质量。

## 使用方法

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
```

## 审查维度

| 维度         | 审查内容                                                                 |
| ------------ | ------------------------------------------------------------------------ |
| 完整性       | 缺少必要项（错误处理、边界情况、分页等）                                 |
| 一致性       | 文档间的术语/格式/数据结构不匹配                                         |
| 可行性       | 是否可以用当前技术栈实现                                                 |
| 代码兼容性   | 与现有数据库 Schema 和 API 路由模式的冲突                                |

## 执行代理

- **规范审查代理**（claude-opus-4-20250514）

## 输出格式

按严重程度分类的问题（严重 / 警告 / 建议），每项附带文件:行号引用和改进建议。

## 触发条件

本技能的触发条件定义在 [SKILL.md](./SKILL.md) 的 `description` 字段中。

## 本地化版本

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
