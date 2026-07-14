<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-code-gen

一个用于同时跨多个层生成代码的技能。并行运行后端、前端和 QA 代理。

## 用法

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"

# 生成后在 Step 8 一并运行 /ywc-impl-review（fix cycle 仅 1 次）
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## Step 8 审查契约

`--review` 会在 Step 8 运行 `/ywc-impl-review`，审查 staged、unstaged、untracked 以及被删除的生成改动，无需创建仅用于审查的 commit（`--tdd` 会在每个 checkpoint 提交 commit 并清空 working tree，此时审查目标改为 `--git-range <pre-generation-sha>..HEAD`）。生成前 working tree 必须干净。

**即使不加 `--review`**，只要生成文件命中 critical path（auth、payment、crypto、PII、external input），就会强制运行 `/ywc-impl-review` 和 `/ywc-security-audit`（与 `ywc-sequential-executor` 相同的契约）。**两个** review 的 Critical/High finding 都会进入这一次 fix cycle；任一方返回 `BLOCKED`/`NEEDS_CONTEXT` 时会直接传播该状态。本 Skill 无 merge 权限，因此该 gate 是 advisory 而非 blocking — 残留的 finding 只会将状态降级为 `DONE_WITH_CONCERNS`，不会丢弃生成的代码。

Verification Gate 通过 `git diff --stat` 确认只改动了 spec 指定的文件（diff scope），Confidence Gate 的 Minimalism 维度会让过度复杂的代码失败（working ≠ minimal）。Step 6.5 还会把生成期间遇到的 spec↔reality 差异记录到 `implementation-notes.md`，在差异属于 material 时建议执行 `ywc-plan --update-spec` 重新规划。

## 执行代理

| 代理                   | 输出                                     |
| ----------------------- | ------------------------------------------ |
| 后端代理 (sonnet)  | API 路由、服务、数据库迁移           |
| 前端代理 (sonnet) | UI 组件、查询 Hook、状态管理 |
| QA 代理 (sonnet)       | 单元测试、集成测试、E2E 场景  |

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
