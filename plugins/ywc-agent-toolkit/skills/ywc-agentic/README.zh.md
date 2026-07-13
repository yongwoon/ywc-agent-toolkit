# ywc-agentic

将高层目标自动编排到 `ywc-*` pipeline 中，完成计划、执行、评估和再次迭代，直到代码实现通过验证。

仅当 user 明确要求 autonomous end-to-end lifecycle delivery 时使用。generic planning 应路由到 `ywc-plan`，ordinary direct change 应路由到 implementation workflow。

当你希望 Codex 自主推进整个交付流程，而不是手动控制每个阶段时使用。

`--pr-lang en|ja|ko|zh|es` 会原样转发给 executor。只有用户明确要求或 shared YWC language policy resolve task/spec language 时，才向 `ywc-task-generator` 转发 `--lang en|ja|ko|zh|es`；否则不传 `--lang`，由 downstream skill 必要时询问。
