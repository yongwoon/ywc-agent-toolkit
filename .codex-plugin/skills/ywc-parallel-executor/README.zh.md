<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-parallel-executor

本文档介绍 Codex `ywc-parallel-executor` workflow。权威的 trigger 条件、anti-trigger、执行步骤和输出格式以 [SKILL.md](./SKILL.md) 为准。

## 本地化版本

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.md)
- [한국어 full](./README.ko.md)
- [Español](./README.es.md)

## 何时使用

- 用户输入此 skill 的 trigger phrase 或等价的自然语言请求。
- Codex 在执行前需要遵循 skill 专用 workflow 和 validation criteria。
- 其他 `ywc-*` skill 将此 skill 作为 upstream 或 downstream step 引用。

## 使用方法

```bash
$ywc-parallel-executor
```

支持的 option 和 mode 请遵循 [SKILL.md](./SKILL.md) 的 Arguments 或 Workflow section。

## Delivery Modes

| Mode | 行为 |
|---|---|
| `--local-merge` | 将每个 task 本地 merge 到 base branch 并立即 push。不创建 PR。 |
| `--draft` | 通过本地 merge 累积 task 更改，并在最后创建一个 aggregate draft PR。 |
| `--per-task-pr` | 对每个 task 创建 PR、等待 CI、处理 bot review、刷新到最新 base、merge PR、同步 base，并 Mark Complete。 |

在 `--per-task-pr` 中，同一 wave 里的前一个 task 可能会推进 base branch。因此 merge 前 executor 会检查 PR branch 是否包含最新 base；如果没有，就把 base merge 到 worktree branch，push 后重新验证 CI。Base refresh conflict 会报告为 `BLOCKED`，不会只凭旧 head SHA 的 CI 结果 merge PR。

## 输出

此 skill 遵循 [SKILL.md](./SKILL.md) 中定义的 report、artifact 和 status format。如果 skill 输出 Completion Status，请保持 `DONE`、`DONE_WITH_CONCERNS`、`BLOCKED` 和 `NEEDS_CONTEXT` 的含义。
