# Project Scaffold - Directory Structure Generator

言語、Framework、Architecture Pattern、Protocol、Project 規模を組み合わせて、適切な Directory 構造を Markdown で生成する Codex Skill です。

## 概要

新しいプロジェクトを始める際に、選択した Stack に合う Directory 構造を整理するための Skill です。

### 主な機能

- 言語、Framework、Protocol、Architecture の複合条件に対応
- Small、Medium、Large 規模ごとの構造を提示
- 各 Directory の役割と配置理由を説明
- SaaS、E-commerce、Chat などの Domain 特性を反映

## 使用方法

```text
/project-scaffold FastAPI + Clean Architecture, medium scale
/project-scaffold Go + gRPC + DDD, large scale, e-commerce
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## Reference

- Framework と言語ごとの Reference は [`references/`](./references) にあります
- Trigger 条件と詳細 Workflow は [SKILL.md](./SKILL.md) にあります

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
