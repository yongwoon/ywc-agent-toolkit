# ywc-agentic (Agentic Orchestrator)

A Skill that takes a single natural-language goal and autonomously orchestrates the existing `ywc-*` skills through to code implementation. Via a **Plan → Execute → Evaluate → Repeat** loop, it re-plans until the `ywc-impl-review` evaluation passes or a user-defined iteration ceiling is reached.

```text
User → Goal → Agent [Plan → Execute → Evaluate → Repeat] → Result
```

## Usage

```text
/ywc-agentic "Implement user authentication API"          # Natural-language goal
/ywc-agentic --goal "Add search feature" --max-iterations 5  # Set iteration ceiling
/ywc-agentic "Implement payment module" --executor parallel  # Force an executor
/ywc-agentic "Refactoring work" --resume                  # Resume from existing tasks/
/ywc-agentic "Goal" --dry-run                             # Print phase plan only
```

## Options

| Option                 | Description                                                                    |
| ---------------------- | ------------------------------------------------------------------------------ |
| `<goal>`               | Natural-language description of the goal to achieve (positional, required)     |
| `--goal <text>`        | Alternative to the positional `<goal>` (positional wins if both are given)     |
| `--max-iterations <n>` | Maximum loop iterations (default: 3, a safety valve never raised autonomously) |
| `--executor <mode>`    | Force an executor: sequential / parallel / auto (default: auto)                |
| `--tasks-dir <path>`   | Directory for task directories and agentic-log.md (default: tasks/)            |
| `--resume`             | Skip the Plan Phase and resume from existing tasks/                            |
| `--dry-run`            | Print the phase plan only; invoke no skills                                    |
| `--terse`              | Minimal output (phase headers and final report only)                           |
| `--pr-lang <lang>`     | PR title/description language (default: auto, inferred from CLAUDE.md)         |

## Execution Flow

1. Receive and validate the goal
2. Detect project context → decide Resume / Full Mode
3. Plan Phase — invoke `ywc-plan` (`--update-spec` on Re-plan)
4. Task Phase — invoke `ywc-task-generator` (Medium/Large only)
5. Execute Phase — run executor with `--local-merge` (Small Path uses `ywc-code-gen`)
6. Evaluate Phase — `ywc-impl-review --git-range` against the original spec
7. Loop Control — Pass exits / Fail re-plans / partial-completion report at the ceiling
8. Iteration Log — append to `tasks/agentic-log.md`
9. Completion Report

## Small Path vs. Medium/Large Path

| Path              | Condition                                 | Execution                                             |
| ----------------- | ----------------------------------------- | ----------------------------------------------------- |
| Small Path        | `ywc-plan` returns a Small verdict        | `ywc-code-gen` directly (no Task Phase or executor)   |
| Medium/Large Path | `ywc-plan` returns a Medium/Large verdict | `ywc-spec-validate` → `ywc-task-generator` → executor |

## Orchestrated Skills

`ywc-plan` · `ywc-spec-validate` · `ywc-task-generator` · `ywc-sequential-executor` / `ywc-parallel-executor` · `ywc-impl-review` · `ywc-code-gen`

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
