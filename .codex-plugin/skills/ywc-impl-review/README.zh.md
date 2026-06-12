<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-impl-review

一个 Skill，在实现完成后创建 PR 前执行全面的实现合规性验证。并行运行 3 个 Agent（Reviewer + Security + QA）。

## 使用方法

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
```

## 执行 Agent

| Agent | 验证范围 |
| --------------------- | ----------------------------------------------------------------------- |
| Reviewer Agent (opus) | 实现与规范的差距、代码质量、模式一致性 |
| Security Agent (opus) | OWASP Top 10、缺失的认证/授权、输入验证 |
| QA Agent (sonnet) | 测试覆盖率分析、缺失测试用例建议 |

## 输出格式

集成报告——Aggregator 合并 3 个 Agent 的结果，按严重程度分类，提供优先级修复建议。

## 触发条件

此 Skill 的触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。

## 本地化版本

- [英语](./README.en.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
