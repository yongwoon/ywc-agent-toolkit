# Parallel Execution Metadata Rules

These rules apply when tasks may be executed via `git worktree`, Codex, or other isolated worker setups.

## Ownership Is a Contract

- Every task must declare **Ownership** in its `README.md`.
- Ownership must be specific enough to serve as an edit boundary for the implementer or agent.
- Prefer concrete file paths, path globs, modules, or named contracts.
- If two tasks are likely to modify the same area, either split the tasks further or declare an explicit conflict.
- **Key Files is a forecast; Ownership is an operational boundary.** When they differ, Ownership takes precedence.

### Good examples

- `sdk/src/runtime/**`
- `api/src/routes/metrics.ts`
- `Database schema: auto_target_registry`
- `OpenAPI contract: /api/v1/metrics`

### Bad examples

- `backend`
- `frontend related files`
- `any files required for this task`

## Shared Surfaces Must Be Declared

If a task touches a shared boundary, it must be listed in **Shared Surfaces**.

Common shared surfaces:

- Database schema
- API / OpenAPI contracts
- Event payload schema
- Shared types
- Workspace-level configuration
- CI / lint / build configuration

Even without direct file overlap, overlapping Shared Surfaces indicate potential conflicts.

## Conflicts With Must Be Explicit

- Tasks that should not run in parallel — even if dependencies allow it — must be declared in **Conflicts With**.
- Declare conflicts when Ownership or Shared Surfaces overlap.
- If no known conflicts exist, write `(None identified)`.

## Parallelizable After Is Operational

- `Depends On` is the logical precondition.
- `Parallelizable After` is the minimum merged baseline for safely starting isolated execution.
- Often the same as `Depends On`, but may be narrower or operationally more specific.

## Task Verify Must Be Task-Specific

- Every task must have exact commands that prove completion.
- Do not list only project-wide gates unless truly required.
- Prefer task-focused verification: targeted tests, filtered builds, package-scoped checks, endpoint-specific validations.

## Dependency Graph Must Support Scheduling

`tasks/dependency-graph.md` maintains the single source of truth for execution order.

When parallel execution is expected, add a **Parallel Execution Notes** section describing:

- Which root tasks can start together.
- Which tasks become runnable after each merge boundary.
- Which tasks are blocked by conflicts rather than dependency order.

This section is for scheduling purposes — not for verbose design explanations.
