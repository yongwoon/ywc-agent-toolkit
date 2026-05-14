# Task Execution Convention

This document covers rules that apply **after task generation**, during the task **execution** phase. These rules are followed by the skill or person executing the tasks.

## Task Completion Handling

When a task is completed, move its directory to `tasks/completed/`:

```bash
# Example
mv tasks/000001-010-db-create-user-table tasks/completed/000001-010-db-create-user-table
```

Purpose of this convention:
- Looking at `tasks/` shows only incomplete tasks, providing an immediate view of current progress
- Looking at `tasks/completed/` provides a history of completed tasks
- Completion status is clearly distinguished by directory location, making it easy for automation (CI, scripts, agents)

**Directory structure after completion:**

```text
tasks/
├── dependency-graph.md
├── completed/
│   ├── 000001-010-db-create-user-table/
│   └── 000001-020-lib-setup-bcrypt/
├── 000001-030-domain-user-entity/
│   ├── README.md
│   └── task.md
└── 000002-010-api-user-registration/
    ├── README.md
    └── task.md
```

## Notes

- The `tasks/completed/` directory is created automatically when the first task is completed (not at task generation time)
- `dependency-graph.md` is never moved — it always stays at the `tasks/` root
- Do not modify the README.md or task.md of completed tasks (preserve execution history)
