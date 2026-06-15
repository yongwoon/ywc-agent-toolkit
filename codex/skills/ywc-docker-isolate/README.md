# ywc-docker-isolate

## Overview

병렬 Git Worktree 개발에서 발생하는 Docker container host port 충돌("port is already allocated")을 제거하는 Codex skill입니다. 각 worktree는 task name에서 결정론적 host port block과 `COMPOSE_PROJECT_NAME`을 도출하고, worktree-local `.env` managed block 및 `.ywc-docker-ports` persist file에만 기록합니다.

## When To Use

| 상황 | 사용 여부 |
|---|---|
| 여러 Git worktree가 각자 Docker compose stack을 실행함 | 사용 |
| `ywc-parallel-executor`가 task별 worktree를 만들고 정리함 | 사용 |
| worktree 없이 `ywc-sequential-executor`가 한 task씩 실행함 | 사용하지 않음 |
| Docker 외 local process port, devcontainer 격리 | 사용하지 않음 |

## Modes

| Mode | 동작 | 주요 인자 | Exit |
|---|---|---|---|
| `setup` | port block 도출 + env-file/persist 작성 | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | 해당 worktree stack만 `down --volumes` | `--task-name` 또는 `--project-name`, `--worktree-path` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | residual stack 보고 | `--expect t1,t2` `[--prune]` | 항상 0, stdout non-empty가 residual signal |

## Integration

`ywc-parallel-executor`에서 pointer-level hook으로 사용합니다.

- Pre-flight 이후: `audit --expect <selected tasks>`
- Step 4a 이후: `setup --task-name <task> --worktree-path <worktree>`
- Step 4g cleanup 직전: `teardown --task-name <task> --worktree-path <worktree>`

## Verification

```bash
bash -n codex/skills/ywc-docker-isolate/scripts/*.sh
bash scripts/validate.sh
find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort
```

자세한 algorithm은 [references/port-allocation.md](references/port-allocation.md), precondition은 [references/preconditions.md](references/preconditions.md)를 참조합니다.
