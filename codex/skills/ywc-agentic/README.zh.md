# ywc-agentic

将高层目标自动编排到 `ywc-*` pipeline 中，完成计划、执行、评估和再次迭代，直到代码实现通过验证。

当你希望 Codex 自主推进整个交付流程，而不是手动控制每个阶段时使用。

`--pr-lang en|ja|ko|zh|es` 会原样转发给 executor，用于 PR 标题/正文语言。只有当用户或 project guidance 明确要求 task/spec 语言时，才向 `ywc-task-generator` 转发 `--lang en|ja|ko|zh|es`；否则保持不传 `--lang` 的既有行为。
