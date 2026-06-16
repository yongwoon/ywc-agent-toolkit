# ywc-docker-isolate

## Overview

`ywc-docker-isolate` は、並列 Git worktree 開発中の Docker compose host port 衝突("port is already allocated")を防ぐ Codex skill です。各 worktree は task name から決定論的な host port block と `COMPOSE_PROJECT_NAME` を導出し、worktree-local `.env` managed block と `.ywc-docker-ports` persist file だけに書き込みます。

## When To Use

| 状況 | 使用 |
|---|---|
| 複数の Git worktree がそれぞれ Docker compose stack を実行する | Yes |
| `ywc-parallel-executor` が task worktree を作成・削除する | Yes |
| `ywc-sequential-executor` が worktree なしで 1 task ずつ実行する | No |
| Docker 以外の local process port や devcontainer isolation | No |

## Modes

| Mode | 動作 | 主な引数 | Exit |
|---|---|---|---|
| `setup` | port block を導出し env-file/persist data を書き込む | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | 対象 worktree stack に `down --volumes` を実行する | `--task-name` または `--project-name`, `--worktree-path` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | residual stack を報告する | `--expect t1,t2` `[--prune]` | 常に 0、stdout non-empty が residual signal |

## Integration

この skill は `ywc-parallel-executor` の pointer-level hook として使用します。

- planning 後: `audit --expect <selected tasks>`
- Step 4a verification 後: `setup --task-name <task> --worktree-path <worktree>`
- Step 4g cleanup 直前: `teardown --task-name <task> --worktree-path <worktree>`

## Verification

```bash
bash -n codex/skills/ywc-docker-isolate/scripts/*.sh
bash scripts/validate.sh
find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort
```

Algorithm は [references/port-allocation.md](references/port-allocation.md)、detection rule は [references/preconditions.md](references/preconditions.md) を参照してください。
