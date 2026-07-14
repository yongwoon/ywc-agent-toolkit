<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-code-gen

一个用于同时跨多个层生成代码的技能。并行运行后端、前端和 QA 代理。

## 用法

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## 执行代理

| 代理                   | 输出                                     |
| ----------------------- | ------------------------------------------ |
| 后端代理 (sonnet)  | API 路由、服务、数据库迁移           |
| 前端代理 (sonnet) | UI 组件、查询 Hook、状态管理 |
| QA 代理 (sonnet)       | 单元测试、集成测试、E2E 场景  |

## Contract 和 TDD baseline

在运行 worker 之前，本技能会准备共享的 Contract Snapshot，让后端、前端和 QA 使用同一组公共契约。改变行为的生成默认采用 test-first；`--tdd` 会启用更严格的 RED/GREEN/REFACTOR checkpoint commit。

## 可选实现审查

使用 `--review` 会在生成结果通过验证和 Confidence Gate 后运行 `ywc-impl-review`。它无需创建仅用于审查的 commit，即可审查 staged、unstaged、untracked 以及被删除的生成改动（`--tdd` 会在每个 checkpoint 提交 commit 并清空 working tree，此时审查目标改为 `--git-range <pre-generation-sha>..HEAD`）。开始前 working tree 必须干净；Critical/High 问题可修复一次并重新审查，未解决的疑虑会保留在结果中。

**即使不加 `--review`**，只要生成文件命中 critical path（auth、payment、crypto、PII、external input），就会强制运行 `ywc-impl-review` 和 `ywc-security-audit`（与 `ywc-sequential-executor` 相同的契约）。**两个** review 的 Critical/High finding 都会进入这一次 fix cycle；任一方返回 `BLOCKED`/`NEEDS_CONTEXT` 时不会报告成功，而是直接传播该状态。本 Skill 无 merge 权限，因此该 gate 是 advisory 而非 blocking — 残留的 finding 只会将状态降级为 `DONE_WITH_CONCERNS`，不会丢弃生成的代码。

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
