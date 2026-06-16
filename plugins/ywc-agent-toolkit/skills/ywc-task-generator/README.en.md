# Task Generator Skill

This Codex Skill converts a specification into dependency-safe, reviewable implementation tasks.

It is designed not only for ordinary task decomposition, but also for task sets that may later run in parallel through `git worktree` and separate Codex sessions.

## Usage

### Basic Usage

Provide a specification and ask the Skill to generate tasks:

```text
/task-generator [Specification content]
```

You can also ask it to refine an existing task set:

```text
/task-generator refine docs/spec.md for parallel worktree execution.
```

### Language Options

The Skill supports Korean, Japanese, and English output.

| Language | Example |
|----------|---------|
| Korean | `Output in Korean.` |
| Japanese | `日本語でタスクを生成してください。` |
| English | `Generate tasks in English.` |

If the user does not specify a language, the Skill asks.

For Korean and Japanese outputs, technical terms stay in English.

### Granularity Mode Options

The Skill supports two task granularity modes and **always asks which mode to apply** — there is no silent default.

| Mode   | Size guideline         | Optimized for                                       |
|--------|------------------------|-----------------------------------------------------|
| human  | ~10 files / ~300 LOC   | Per-PR human review                                 |
| llm    | ~25 files / ~800 LOC   | Single LLM agent session in an isolated worktree    |

Safety Invariants (DB migration separation, Library introduction separation, Phase hard gate, post-task buildability) apply identically in both modes. See [references/granularity-modes.md](./references/granularity-modes.md) for the full specification.

## Output Structure

### Task Directory

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

### Task Naming

```text
[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
```

- `PHASE`: 6 digits, dependency stage (reserves headroom for multi-year project growth)
- `SEQUENCE`: 3 digits, increments by 10
- `CATEGORY`: `lib` | `db` | `api` | `domain` | `worker` | `ui` | `test` | `refactor` | `infra`

### Task Completion

After completion and merge:

```text
mv tasks/000001-010-db-create-user-table tasks/completed/000001-010-db-create-user-table
```

## Core Principles

| Principle | Description |
|-----------|-------------|
| Reviewability | Each task should be reviewable within about 1 hour |
| Dependency Safety | No forward dependency; each task is implementable at its position |
| DB Migration Separation | Database migration must be its own task |
| Library Introduction Separation | New libraries and frameworks must be isolated |
| Single Concern | One task should represent one primary concern |
| Parallel Safety | Tasks should include enough metadata for isolated worktree execution |

## Parallel Worktree Operation

When tasks may be executed in parallel, the generated task set should include operational metadata.

### Required Metadata Per Task

Each `README.md` should include:

- `Spec Reference` — Primary Sources (links to PRD / tech design), Summary (2–5 sentence orientation), and Out of Scope (from spec) guardrail. Housekeeping tasks with no spec should explicitly record `N/A — no external spec` instead of omitting the section.
- `Ownership`
- `Shared Surfaces`
- `Conflicts With`
- `Parallelizable After`
- `Task Verify`

> External URLs in `Primary Sources` (Notion, Confluence, Figma, etc.) require a project-level policy. The default is project-relative paths only; `sequential-executor` stores the chosen policy in `Codex approval settings or the project-local policy file` under `taskExecutor.externalSpecUrls`.

### Ownership vs Key Files

- `Key Files` is an expected touch forecast
- `Ownership` is the actual operating boundary
- If they differ, treat `Ownership` as authoritative

### Dependency Graph Scheduling

`tasks/dependency-graph.md` stays the source of truth for execution order.  
When parallel work is expected, include `Parallel Execution Notes` describing:

- the initial ready set
- tasks that become runnable after each merge boundary
- tasks blocked by conflicts instead of dependency order

### Recommended Prompt Additions

For parallel-friendly output, explicitly request:

```text
- Parallel Execution Metadata for every task
- Ownership as an operating boundary
- Conflicts With for shared contracts, schema, or config
- Parallel Execution Notes in dependency-graph.md
```

## Example Prompt

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

## Trigger Keywords

This Skill fits requests such as:

- `task generation`
- `task breakdown`
- `spec to tasks`
- `refine existing tasks`
- `parallel worktree tasks`
