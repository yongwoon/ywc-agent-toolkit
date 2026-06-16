# ywc-docker-isolate

병렬 Git Worktree 개발 시 발생하는 Docker container host port 충돌
("port is already allocated")을 제거하는 skill 입니다. 각 worktree 가 자신의 task
명에서 **결정론적으로** 고유 host port block 을 도출하여, 여러 worktree 가 각자
독립된 Docker stack 으로 동시에 동작할 수 있게 합니다.

## 핵심 동작

- **per-worktree namespacing**: `COMPOSE_PROJECT_NAME = ywc-<sanitized-task>` +
  `port = 20000 + (hash(task) % 100) * 100 + var_index` 로 고유 port 를 도출합니다.
- **원본 불변(NFR-1)**: worktree-local env-file 의 managed block 과
  `.ywc-docker-ports` persist 파일에만 기록하며, commit 된 compose / env-file 은
  절대 수정하지 않습니다.
- **결정론(AC2)**: 재실행은 `.ywc-docker-ports` read-back 으로 동일 port 를
  보장하고, 반환 전 cross-platform live-check 로 squatter 점유를 fail-loud 합니다.

## Mode

| Mode | 동작 | 주요 인자 | Exit |
|---|---|---|---|
| `setup` | port block 도출 + env-file/persist 작성 | `--task-name` `--worktree-path` | 0=격리/no-op, 1=hardcoded/충돌/corrupt/squatter |
| `teardown` | 해당 worktree stack 만 `down --volumes` | `--task-name`\|`--project-name` `--worktree-path` `[--keep-volumes]` | 0=정리, 1=LEAKED/SANITIZE_ERROR |
| `audit` | 잔존 stack 보고 (stdout non-empty 판별) | `--expect t1,t2` `[--prune]` | 항상 0 |

## ywc-parallel-executor 통합 위치

- **Pre-flight**: `audit --expect <wave tasks>` — 잔존 시 run abort.
- **Step 4a**(per task): `setup` — exit 1 → task BLOCKED + worktree 보존.
- **Step 4g**(`cleanup-worktree.sh` 직전): `teardown` — preserved worktree 는 skip.

## 예시

```bash
# task worktree 에 port 격리 적용
bash scripts/setup-docker-ports.sh --task-name feat-a --worktree-path /path/wt-a

# worktree stack 정리 (volume 포함)
bash scripts/teardown-docker.sh --task-name feat-a --worktree-path /path/wt-a

# 잔존 stack 점검
bash scripts/audit-docker-stacks.sh --expect feat-a,feat-b
```

## References

- [references/port-allocation.md](references/port-allocation.md) — port 도출 공식·정렬·salt chain·결정론 보장
- [references/preconditions.md](references/preconditions.md) — compose 탐지·env-var 한계·플랫폼 도구·우선순위
