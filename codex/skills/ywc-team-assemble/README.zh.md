# ywc-team-assemble

当用户明确要求 specialist team、subagent delegation 或 parallel agent work 时使用的 Codex skill。

## 使用场景

- 用户明确要求组建 team、委派给 agents 或 parallel 执行。
- 工作至少包含两个独立 workstream。
- write scope 可以分离，并且 parent agent 可以 review 和整合结果。

不要用于简单问题、单文件编辑或严格顺序执行的工作。

## 包含文件

- `SKILL.md` — team assembly workflow
- `agents/openai.yaml` — Codex metadata
- `references/prompt-templates.md` — explorer、worker、reviewer prompt template
- `evals/evals.json` — role isolation、Claim/Evidence、cap 和 privacy contract evals

## Context Safety

Team prompt 会在 projection 前验证有界 Claims 和 cited evidence。Independent reviewer 只能接收 scope 与 artifact path；dependent role 只能接收 Claims 及其引用的 artifact。peer conclusion/recommendation、transcript、raw content、uncited artifact、invalid 或 over-cap Claim 都会被拒绝。
