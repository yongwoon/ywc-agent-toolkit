<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Project Scaffold - 目录结构生成器

一个 Claude Code Skill，通过组合语言、框架、架构模式、协议和项目规模，以 Markdown 格式生成合适的项目目录结构。

## 概述

此 Skill 适用于开始新项目时，需要为所选技术栈决定如何组织目录结构的场景。

### 主要特性

- 支持语言、框架、协议和架构的组合条件
- 为小型、中型和大型项目提供不同的结构
- 解释每个目录的作用及其存在的原因
- 反映 SaaS、电商、聊天等领域特性

## 使用方法

```text
/ywc-project-scaffold FastAPI + Clean Architecture, medium scale
/ywc-project-scaffold Go + gRPC + DDD, large scale, e-commerce
```

自然语言触发条件在 [SKILL.md](./SKILL.md) 中定义。

## 参考资料

- 框架和语言参考存储在 [`references/`](./references) 下
- 触发规则和详细工作流在 [SKILL.md](./SKILL.md) 中定义

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
