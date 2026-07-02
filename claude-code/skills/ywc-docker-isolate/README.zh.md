<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-docker-isolate

消除在并行 Git worktree 开发期间出现的 Docker Container 主机端口冲突
（"port is already allocated"）。每个 worktree 都会**确定性地**从其
task 名称派生出唯一的主机端口块，因此多个 worktree 可以同时运行独立的
Docker stack。

## 核心行为

- **per-worktree namespacing**：`COMPOSE_PROJECT_NAME = ywc-<sanitized-task>` 加上
  `port = 20000 + (hash(task) % 100) * 100 + var_index`。
- **原始文件不可变（NFR-1）**：只写入一个 worktree 本地的 env-file 托管
  块和 `.ywc-docker-ports` 持久化文件；绝不修改已提交的
  compose / env-file。
- **确定性（AC2）**：重新运行时读回 `.ywc-docker-ports` 以获得相同的
  端口，并运行跨平台的实时检查，在有占用者时高声失败。

## Modes

| Mode | 动作 | 关键参数 | Exit |
|---|---|---|---|
| `setup` | 派生端口块 + 写入 env-file/持久化文件 | `--task-name` `--worktree-path` | 0=isolated/no-op, 1=hardcoded/collision/corrupt/squatter |
| `teardown` | 仅对此 worktree 的 stack 执行 `down --volumes` | `--task-name`\|`--project-name` `--worktree-path` `[--keep-volumes]` | 0=cleaned, 1=LEAKED/SANITIZE_ERROR |
| `audit` | 报告残留 stack（stdout 非空） | `--expect t1,t2` `[--prune]` | always 0 |

## ywc-parallel-executor 集成点

- **Pre-flight**：`audit --expect <wave tasks>` — 若有残留则中止运行。
- **Step 4a**（每个 task）：`setup` — exit 1 → task BLOCKED，worktree 保留。
- **Step 4g**（在 `cleanup-worktree.sh` 之前）：`teardown` — 被保留的 worktree 会跳过。

## 示例

```bash
# 对 task worktree 应用端口隔离
bash scripts/setup-docker-ports.sh --task-name feat-a --worktree-path /path/wt-a

# 拆除 worktree stack（包括 volumes）
bash scripts/teardown-docker.sh --task-name feat-a --worktree-path /path/wt-a

# 审计残留 stack
bash scripts/audit-docker-stacks.sh --expect feat-a,feat-b
```

## 参考

- [references/port-allocation.md](references/port-allocation.md) — hash 公式、排序规则、salt chain、确定性保证
- [references/preconditions.md](references/preconditions.md) — compose 检测、env-var 限制、平台工具、优先级
