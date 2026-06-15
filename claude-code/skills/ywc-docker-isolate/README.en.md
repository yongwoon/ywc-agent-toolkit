# ywc-docker-isolate

Eliminates the Docker container host-port collision ("port is already
allocated") that arises during parallel Git worktree development. Each worktree
derives a unique host-port block **deterministically** from its task name, so
multiple worktrees can run independent Docker stacks simultaneously.

## Core behavior

- **per-worktree namespacing**: `COMPOSE_PROJECT_NAME = ywc-<sanitized-task>` plus
  `port = 20000 + (hash(task) % 100) * 100 + var_index`.
- **original immutable (NFR-1)**: writes only a worktree-local env-file managed
  block and the `.ywc-docker-ports` persist file; never mutates the committed
  compose / env-file.
- **deterministic (AC2)**: re-runs read back `.ywc-docker-ports` for identical
  ports and run a cross-platform live-check that fails loud on a squatter.

## Modes

| Mode | Action | Key args | Exit |
|---|---|---|---|
| `setup` | derive port block + write env-file/persist | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | `down --volumes` for this worktree's stack only | `--task-name`\|`--project-name` `--worktree-path` `[--keep-volumes]` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | report residual stacks (stdout non-empty) | `--expect t1,t2` `[--prune]` | always 0 |

## ywc-parallel-executor integration points

- **Pre-flight**: `audit --expect <wave tasks>` — abort the run if residual.
- **Step 4a** (per task): `setup` — exit 1 → task BLOCKED, worktree preserved.
- **Step 4g** (before `cleanup-worktree.sh`): `teardown` — preserved worktrees skip it.

## Example

```bash
# Apply port isolation to a task worktree
bash scripts/setup-docker-ports.sh --task-name feat-a --worktree-path /path/wt-a

# Tear down the worktree stack (including volumes)
bash scripts/teardown-docker.sh --task-name feat-a --worktree-path /path/wt-a

# Audit for residual stacks
bash scripts/audit-docker-stacks.sh --expect feat-a,feat-b
```

## References

- [references/port-allocation.md](references/port-allocation.md) — hash formula, sort rule, salt chain, determinism guarantee
- [references/preconditions.md](references/preconditions.md) — compose detection, env-var limits, platform tools, precedence
