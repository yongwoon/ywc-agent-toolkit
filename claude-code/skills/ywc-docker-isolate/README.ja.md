# ywc-docker-isolate

並列 Git Worktree 開発で発生する Docker container host port 衝突
("port is already allocated") を解消する skill です。各 worktree が自身の task
名から **決定論的に** 固有の host port block を導出し、複数の worktree が
それぞれ独立した Docker stack で同時に動作できるようにします。

## 主な動作

- **per-worktree namespacing**: `COMPOSE_PROJECT_NAME = ywc-<sanitized-task>` と
  `port = 20000 + (hash(task) % 100) * 100 + var_index`。
- **original immutable (NFR-1)**: worktree-local env-file の managed block と
  `.ywc-docker-ports` persist file にのみ記録し、commit 済みの compose /
  env-file は決して変更しません。
- **determinism (AC2)**: 再実行は `.ywc-docker-ports` の read-back で同一 port を
  保証し、返却前に cross-platform live-check で squatter 占有を fail-loud します。

## Mode

| Mode | 動作 | 主な引数 | Exit |
|---|---|---|---|
| `setup` | port block 導出 + env-file/persist 書き込み | `--task-name` `--worktree-path` | 0=分離/no-op, 1=hardcoded/衝突/corrupt/squatter |
| `teardown` | 当該 worktree stack のみ `down --volumes` | `--task-name`\|`--project-name` `--worktree-path` `[--keep-volumes]` | 0=整理, 1=LEAKED/SANITIZE_ERROR |
| `audit` | 残存 stack 報告 (stdout non-empty で判定) | `--expect t1,t2` `[--prune]` | 常に 0 |

## ywc-parallel-executor 統合ポイント

- **Pre-flight**: `audit --expect <wave tasks>` — 残存時は run abort。
- **Step 4a**(per task): `setup` — exit 1 → task BLOCKED + worktree 保持。
- **Step 4g**(`cleanup-worktree.sh` 直前): `teardown` — preserved worktree は skip。

## 例

```bash
# task worktree に port 分離を適用
bash scripts/setup-docker-ports.sh --task-name feat-a --worktree-path /path/wt-a

# worktree stack を整理 (volume 含む)
bash scripts/teardown-docker.sh --task-name feat-a --worktree-path /path/wt-a

# 残存 stack を点検
bash scripts/audit-docker-stacks.sh --expect feat-a,feat-b
```

## References

- [references/port-allocation.md](references/port-allocation.md) — port 導出公式・ソート・salt chain・determinism 保証
- [references/preconditions.md](references/preconditions.md) — compose 検出・env-var 制限・platform tool・優先順位
