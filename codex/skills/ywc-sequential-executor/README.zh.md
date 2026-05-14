<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Sequential Executor Skill（ywc-sequential-executor）

此 Codex Skill 执行由 ywc-task-generator Skill 生成的任务。它将从创建分支到实现、提交、创建 PR、CI 验证、合并和本地同步的完整开发生命周期自动化。

支持单任务执行和顺序范围执行。

## 使用方法

### 基本用法

执行单个任务：

```text
/ywc-sequential-executor 000001-010-db-create-users-table
```

也可以通过阶段+序列前缀指定：

```text
/ywc-sequential-executor 000001-010
```

### 范围执行

在循环中顺序执行连续任务：

```text
/ywc-sequential-executor 000001-010..000002-030
```

### 自动检测下一个任务

未指定任务时，Skill 分析依赖图并选择下一个可执行任务：

```text
/ywc-sequential-executor
```

### 选项

| 选项 | 描述 | 示例 |
|--------|-------------|---------|
| `--pr-lang <lang>` | PR 标题/描述语言 | `--pr-lang ja` |
| `--tasks-dir <path>` | 任务目录路径（默认：`tasks/`） | `--tasks-dir ./docs/tasks` |
| `--skip-ci-wait` | 跳过 CI 等待和自动合并（仅创建 PR） | |
| `--draft` | 创建草稿 PR，跳过合并 | |
| `--local-merge` | 完全跳过 PR — 将功能分支本地合并到基础分支并推送（步骤 4 验证仍运行） | |
| `--base-branch <branch>` | 基础分支覆盖（默认：自动检测） | `--base-branch develop` |
| `--dry-run` | 显示执行计划（任务顺序、依赖、模式）但不实际执行 | |

> `--local-merge`、`--draft` 和 `--skip-ci-wait` 互斥。如果传入多个，Skill 会停止并询问您的意图。
> `--local-merge` **不运行远程 CI**，因此合并的唯一安全网是步骤 4 中的本地验证（lint/typecheck/test）。敏感变更请避免使用。

## 执行周期

对于每个任务，按顺序执行以下步骤。**在范围模式下，完整周期（步骤 1 → 步骤 8）对每个任务重复执行。每个任务有其独立的功能分支。**

### 范围模式下的每任务分支生命周期

**普通模式（PR 流程）：**

```text
每个任务：检出基础 → 拉取 → 创建功能分支 → 实现 → PR → CI → 合并 → 重复
```

**`--local-merge` 模式：**

```text
每个任务：检出基础 → 拉取 → 创建功能分支 → 实现 → 本地合并 → 推送 → 重复
```

**`--draft` / `--skip-ci-wait` 模式：**

```text
每个任务：从前一个功能分支分叉（链式分支）→ 实现 → 草稿 PR → 重复
```

### 步骤详情

```text
步骤 1：依赖验证与规范加载
  └─ 验证所有依赖任务存在于 tasks/completed/ 中
  └─ 加载 README.md 的规范引用（主要来源 / 摘要 / 范围外）
  └─ 外部 URL 遵循 Codex approval settings or the project-local policy file 中的 taskExecutor.externalSpecUrls 策略

步骤 2：分支创建（每个任务运行 — 范围模式下从不跳过）
  └─ （普通/local-merge）git checkout <base> && git pull && git checkout -b feature/<task-name>
  └─ （范围+draft/skip-ci-wait）从前一个功能分支分叉（链式分支）

步骤 3：实现
  └─ 按照 task.md 实现步骤进行，在逻辑边界处提交

步骤 4：任务验证
  └─ 运行任务验证命令和 lint/typecheck/test

步骤 5：创建 PR
  └─ 调用 create-pr Skill（包含安全检查、CI 推送前验证）
  └─ （--local-merge）跳过 — 不创建 PR

步骤 6：CI 验证与合并
  └─ gh pr checks --watch → gh pr merge --delete-branch
  └─ （--local-merge）git checkout base → git merge --no-ff feature/<task> → git push → git branch -d

步骤 7：本地同步
  └─ git checkout <base-branch> && git pull origin <base-branch>

步骤 8：标记完成
  └─ mv tasks/<task-name> tasks/completed/<task-name> → 提交
  └─ --local-merge 范围：每个任务完成后立即推送
  └─ 普通 PR 范围：最后一个任务完成后统一推送

步骤 9：下一个任务（范围模式）
  └─ 如果还有任务，返回步骤 1 并重复完整周期（包含步骤 2）
```

## PR 语言

未指定 `--pr-lang` 时，语言按以下优先级检测：

1. **CLAUDE.md** — 检查语言指令（如 `Git commits: Japanese`）
2. **AGENTS.md** — 检查语言偏好
3. **最近 PR 历史** — 检测主要语言
4. **回退** — 英语

## 错误处理

| 情况 | 行为 |
|-----------|----------|
| CI 失败 | 最多 2 次修复尝试，然后通知用户 |
| 合并冲突 | 停止并要求用户手动解决 |
| CI 超时（>30 分钟） | 报告状态并询问用户是否继续 |
| 依赖未满足 | 列出未完成的依赖并停止 |
| 任务未找到 | 显示可用任务 |

## 集成

此 Skill 与以下配合工作：

- **ywc-task-generator** — 任务生成（上游）
- **create-pr** — PR 创建（在步骤 5 中调用）

## 示例提示

### 单任务执行（日语 PR）

```text
/ywc-sequential-executor 000001-010-db-create-users-table --pr-lang ja
```

### 全范围执行

```text
/ywc-sequential-executor 000001-010..000003-020 --pr-lang ja
```

### 仅草稿 PR（不合并）

```text
/ywc-sequential-executor 000001-010..000002-030 --draft --pr-lang ko
```

### 无 PR 的本地合并

```text
/ywc-sequential-executor 000001-010-db-create-users-table --local-merge
```

步骤 4 lint/typecheck/test 仍会运行。成功后，功能分支通过 `git merge --no-ff` 合并到基础分支并推送。

## 触发条件

此 Skill 的触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。
