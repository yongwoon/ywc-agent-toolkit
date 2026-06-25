<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-plan

一个实现前规划 Skill，将粗略的想法转化为两种可执行产物之一：Small 路径的直接执行计划，或 Medium/Large 路径的规范文档。自动评估规模并路由到正确的下游 Skill。

## 使用场景

- 当用户说"为这个功能制定计划"
- 当还没有 Spec 或任务，用户不知道从哪里开始
- 当不清楚变更是 Small 的一次性编辑还是需要完整 Spec
- 当准备 `ywc-task-generator` 将消费的输入 Spec 时

## 使用方法

```bash
/ywc-plan "<粗略请求>"
```

或自然语言调用：

> "我想在个人资料页面添加通知偏好设置——制定一个计划。"

## 输入

- 自然语言变更请求（粗略想法、功能请求、变更描述）

## 输出

根据规模，输出以下之一：

| 规模 | 输出 |
|---|---|
| Small | `./plan.md` — 可直接执行的单 PR 计划 |
| Medium / Large | `docs/ywc-plans/<slug>.md` — `ywc-spec-validate` 和 `ywc-task-generator` 将消费的 Spec 文档 |

每条路径都会发出明确的交接消息，指名下一个 Skill。

## 流程

1. **澄清** — 向用户一次性询问四个锚点：做什么 / 为什么 / 不在范围内 / 何时完成
2. **调查** — 只读取必要文件：`CLAUDE.md`、`package.json`、`docs/architecture/` 等
3. **评估规模** — 从 Small / Medium / Large 中选择一个（模糊时默认为 Medium）
4. **分支** — Small 写 `plan.md`；Medium/Large 写 Spec 文档
5. **交接** — 明确打印下一个 Skill（执行是用户的决定，不是此 Skill 的）

## 安全不变量

以下任何一项会自动升级到 Medium 规模或更高：

- 数据库迁移 / 模式变更
- 引入新库 / 框架
- 向外部消费者暴露的新 API 合约
- 触及认证 / 授权逻辑
- 跨越 2+ 个模块的横切变更

## 相关 Skills

- `ywc-tech-research` — 技术选型未定时，在 `ywc-plan` 之前运行
- `ywc-product-review` — 产品/业务框架不清晰时，在 `ywc-plan` 之前运行
- `ywc-spec-ready` — Medium/Large 路径的自动收敛快捷方式（spec 起草后通过 opt-in 提示提供）
- `ywc-spec-validate` — Medium/Large 路径的手动下一步
- `ywc-task-generator` — 审查通过后将 Spec 分解为任务
- `ywc-code-gen` — Small 路径的直接执行选项
- `ywc-sequential-executor` / `ywc-parallel-executor` — 执行生成的任务

## 触发条件

触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。

## 本地化版本

- [韩语（默认）](./README.md)
- [日语](./README.ja.md)
