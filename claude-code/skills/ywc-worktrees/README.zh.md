<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-worktrees

Git worktree 生命周期管理 Skill。worktree 优先级解析（`.worktrees/` > CLAUDE.md `worktree_root` > `--root` fallback）的单一事实来源，由 `ywc-parallel-executor` 和 `ywc-finish-branch` 调用。

## 模式

- `--mode resolve` — 打印 worktree 将落地的路径（无副作用）
- `--mode create` — 运行 `git worktree add` 并验证注册
- `--mode audit` — 检测陈旧 / 泄漏 / 缺失的 worktree（Pre-flight 或 wave-end）
- `--mode prune` — merge 后清理（`git worktree remove` + 删除本地 branch + `git worktree prune` + 验证）。传入 `--keep-branch` 以仅移除 worktree 并保留本地 branch（例如为稍后的 trunk PR 保留一个 integration branch）。

关于完整的参数表和优先级解析链，请参见 [SKILL.md](./SKILL.md)。

## 捆绑脚本

| Script | Purpose |
|---|---|
| `scripts/audit-worktrees.sh` | `--mode audit` 的核心审计逻辑 |
| `scripts/cleanup-worktree.sh` | `--mode prune` 的核心清理和 branch 删除逻辑 |

两个脚本均通过 `git mv` 从 `ywc-parallel-executor/scripts/` 移动而来，以保留其 commit 历史。

## 设计来源

改编自 [superpowers / using-git-worktrees](https://github.com/anthropic-experimental/superpowers) Skill——优先级解析链和四模式接口遵循该模式。本项目的自包含 runtime 策略意味着引用 superpowers skill 仅为设计意图；它在 runtime **不会**被调度。

## 集成

- **upstream**：[`ywc-parallel-executor`](../ywc-parallel-executor/)（Pre-flight audit、Step 4 逐 task create、Step 4g prune），[`ywc-finish-branch`](../ywc-finish-branch/)（Step 5 / 8 清理）
- **downstream**：无（leaf-operation skill）

## 3-Root 同步

本 Skill 向所有三个 skill root（claude-code、codex-skill、pi-skills）交付相同的内容，因为 worktree 管理是通用功能。它**不在** `is_diverged()` 中。
