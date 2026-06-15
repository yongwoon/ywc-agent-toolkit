# ywc-docker-isolate

## Overview

`ywc-docker-isolate` prevents Docker compose host port collisions during parallel Git worktree development. Each worktree derives a deterministic host port block and `COMPOSE_PROJECT_NAME` from the task name, then writes only a worktree-local `.env` managed block and `.ywc-docker-ports` persist file.

## When To Use

| Situation | Use |
|---|---|
| Multiple Git worktrees run their own Docker compose stacks | Yes |
| `ywc-parallel-executor` creates and cleans up task worktrees | Yes |
| `ywc-sequential-executor` runs one task at a time without worktrees | No |
| Non-Docker local process ports or devcontainer isolation | No |

## Modes

| Mode | Action | Key args | Exit |
|---|---|---|---|
| `setup` | Derive port block and write env-file/persist data | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | Run `down --volumes` for the scoped worktree stack | `--task-name` or `--project-name`, `--worktree-path` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | Report residual stacks | `--expect t1,t2` `[--prune]` | Always 0; stdout non-empty signals residuals |

## Integration

This skill is used as pointer-level hooks from `ywc-parallel-executor`.

- After planning: `audit --expect <selected tasks>`
- After Step 4a verification: `setup --task-name <task> --worktree-path <worktree>`
- Before Step 4g cleanup: `teardown --task-name <task> --worktree-path <worktree>`

## Verification

```bash
bash -n codex/skills/ywc-docker-isolate/scripts/*.sh
bash scripts/validate.sh
find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort
```

See [references/port-allocation.md](references/port-allocation.md) for the algorithm and [references/preconditions.md](references/preconditions.md) for detection rules.
