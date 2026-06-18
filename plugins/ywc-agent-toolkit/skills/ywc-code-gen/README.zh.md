<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-code-gen

一个用于同时跨多个层生成代码的技能。并行运行后端、前端和 QA 代理。

## 用法

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
```

## 执行代理

| 代理                   | 输出                                     |
| ----------------------- | ------------------------------------------ |
| 后端代理 (sonnet)  | API 路由、服务、数据库迁移           |
| 前端代理 (sonnet) | UI 组件、查询 Hook、状态管理 |
| QA 代理 (sonnet)       | 单元测试、集成测试、E2E 场景  |

## Contract 和 TDD baseline

在运行 worker 之前，本技能会准备共享的 Contract Snapshot，让后端、前端和 QA 使用同一组公共契约。改变行为的生成默认采用 test-first；`--tdd` 会启用更严格的 RED/GREEN/REFACTOR checkpoint commit。

## 与 sequential-executor 的关系

- **sequential-executor**：顺序执行（适用于有依赖关系的任务）
- **/ywc-code-gen**：独立层并行生成（当 SDK/API/Web 需要同时运行时）
- 两者互补使用

## 触发方式

本技能的触发条件定义在 [SKILL.md](./SKILL.md) 的 `description` 字段中。

## 本地化版本

- [英文](./README.en.md)
- [日文](./README.ja.md)
- [韩文](./README.ko.md)
