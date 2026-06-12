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
