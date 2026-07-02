<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-docker-isolate

## 概览

`ywc-docker-isolate` 在并行 Git worktree 开发期间防止 Docker compose host port 冲突。每个 worktree 会根据 task name 推导确定性的 host port block 和 `COMPOSE_PROJECT_NAME`，然后只写入 worktree-local `.env` managed block 和 `.ywc-docker-ports` persist file。

## 何时使用

| 情况 | 使用 |
|---|---|
| 多个 Git worktrees 运行各自的 Docker compose stacks | Yes |
| `ywc-parallel-executor` 创建和清理 task worktrees | Yes |
| `ywc-sequential-executor` 不使用 worktrees、一次运行一个 task | No |
| 非 Docker local process ports 或 devcontainer isolation | No |

## Modes

| Mode | Action | Key args | Exit |
|---|---|---|---|
| `setup` | 推导 port block，并写入 env-file/persist data | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | 对 scoped worktree stack 执行 `down --volumes` | `--task-name` 或 `--project-name`, `--worktree-path` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | 报告 residual stacks | `--expect t1,t2` `[--prune]` | 总是 0；stdout 非空表示存在 residuals |

## Integration

本 Skill 作为 `ywc-parallel-executor` 的 pointer-level hooks 使用。

- planning 后：`audit --expect <selected tasks>`
- Step 4a verification 后：`setup --task-name <task> --worktree-path <worktree>`
- Step 4g cleanup 前：`teardown --task-name <task> --worktree-path <worktree>`

## Verification

```bash
bash -n codex/skills/ywc-docker-isolate/scripts/*.sh
bash scripts/validate.sh
find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort
```

算法见 [references/port-allocation.md](references/port-allocation.md)，检测规则见 [references/preconditions.md](references/preconditions.md)。
