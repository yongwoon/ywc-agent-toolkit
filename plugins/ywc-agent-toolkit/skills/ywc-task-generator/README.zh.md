<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Task Generator Skill

此 Codex Skill 将规范转换为依赖安全、可审查的实现任务。

它不仅适用于普通任务分解，还适用于可能通过 `git worktree` 和独立 Codex 或 Codex 会话并行运行的任务集。

## 使用方法

### 基本用法

提供规范并要求 Skill 生成任务：

```text
/task-generator [规范内容]
```

也可以要求精炼现有任务集：

```text
/task-generator refine docs/spec.md for parallel worktree execution.
```

### 语言选项

Skill 支持韩语、日语和英语输出。

| 语言 | 示例 |
|----------|---------|
| 韩语 | `Output in Korean.` |
| 日语 | `日本語でタスクを生成してください。` |
| 英语 | `Generate tasks in English.` |

如果用户未指定语言，Skill 会询问。

韩语和日语输出中，技术术语保留英文。

### 粒度模式选项

Skill 支持两种任务粒度模式，并**始终询问应用哪种模式** — 没有默认静默选择。

| 模式   | 大小指南               | 优化目标                                            |
|--------|------------------------|-----------------------------------------------------|
| human  | 约 10 个文件 / 约 300 行代码   | 每 PR 人工审查                                 |
| llm    | 约 25 个文件 / 约 800 行代码   | 在隔离 worktree 中的单 LLM 代理会话    |

安全不变量（DB 迁移分离、库引入分离、阶段硬门控、任务后可构建性）在两种模式下均相同适用。完整规范请参见 [references/granularity-modes.md](./references/granularity-modes.md)。

## 输出结构

### 任务目录

```text
tasks/
├── 000001-010-db-create-user-table/
│   ├── README.md
│   ├── task.md
│   └── test.md
├── 000001-020-api-user-registration/
│   ├── README.md
│   └── task.md
└── dependency-graph.md
```

### 任务命名

```text
[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
```

- `PHASE`：6 位数字，依赖阶段（为多年项目增长预留空间）
- `SEQUENCE`：3 位数字，以 10 为步长递增
- `CATEGORY`：`lib` | `db` | `api` | `domain` | `worker` | `ui` | `test` | `refactor` | `infra`

### 任务完成

完成并合并后：

```text
mv tasks/000001-010-db-create-user-table tasks/completed/000001-010-db-create-user-table
```

## 核心原则

| 原则 | 描述 |
|-----------|-------------|
| 可审查性 | 每个任务应可在约 1 小时内完成审查 |
| 依赖安全 | 无前向依赖；每个任务在其位置可实现 |
| DB 迁移分离 | 数据库迁移必须是独立任务 |
| 库引入分离 | 新库和框架必须隔离 |
| 单一关注点 | 一个任务应代表一个主要关注点 |
| 并行安全 | 任务应包含足够的元数据用于隔离 worktree 执行 |

## 并行 Worktree 操作

当任务可能并行执行时，生成的任务集应包含操作元数据。

### 每个任务所需的元数据

每个 `README.md` 应包含：

- `Spec Reference` — 主要来源（PRD / 技术设计链接）、摘要（2–5 句方向说明）和范围外（来自规范）的护栏。没有规范的维护任务应明确记录 `N/A — no external spec` 而非省略此部分。
- `Ownership`
- `Shared Surfaces`
- `Conflicts With`
- `Parallelizable After`
- `Task Verify`

> `Primary Sources` 中的外部 URL（Notion、Confluence、Figma 等）需要项目级策略。默认仅限项目相对路径；`sequential-executor` 将所选策略存储在 `Codex approval settings or the project-local policy file` 的 `taskExecutor.externalSpecUrls` 下。

### Ownership 与 Key Files 的区别

- `Key Files` 是预期的触及预测
- `Ownership` 是实际的操作边界
- 如果两者不同，以 `Ownership` 为准

### 依赖图调度

`tasks/dependency-graph.md` 是执行顺序的唯一真相来源。
当预计并行工作时，包含描述以下内容的 `Parallel Execution Notes`：

- 初始就绪集
- 每个合并边界后变为可运行的任务
- 被冲突而非依赖顺序阻塞的任务

### 推荐的提示补充

对于并行友好的输出，明确请求：

```text
- 为每个任务提供并行执行元数据
- Ownership 作为操作边界
- Conflicts With 用于共享合同、模式或配置
- dependency-graph.md 中的并行执行说明
```

## 示例提示

```text
/task-generator break down this specification into implementation tasks.

Requirements:
- Output in Korean.
- Assume tasks may be executed in parallel via git worktrees and separate Codex sessions.
- For every task README, include Ownership, Shared Surfaces, Conflicts With, Parallelizable After, and Task Verify.
- Ownership must be an operating boundary, not just a summary of expected files.
- In dependency-graph.md, include Parallel Execution Notes.

Specification:
[PASTE SPEC HERE]
```

## 触发关键词

此 Skill 适用于以下请求：

- `task generation`（任务生成）
- `task breakdown`（任务分解）
- `spec to tasks`（规范转任务）
- `refine existing tasks`（精炼现有任务）
- `parallel worktree tasks`（并行 worktree 任务）
