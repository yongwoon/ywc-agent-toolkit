# ywc-spec-validate

A Spec Reviewer Agent Skill that validates specification quality after writing specs and before running the task-generator.

## Usage

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
```

## Review Dimensions

| Dimension          | What is reviewed                                                      |
| ------------------ | --------------------------------------------------------------------- |
| Completeness       | Missing required items (Error Handling, Edge Cases, Pagination, etc.) |
| Consistency        | Terminology/format/data structure mismatches across documents         |
| Feasibility        | Whether it can be implemented with the current stack                  |
| Code compatibility | Conflicts with existing DB Schema and API Route patterns              |

## Execution Agent

- **Spec Reviewer Agent** (claude-opus-4-20250514)

## Output Format

Issues classified by severity (Critical / Warning / Suggestion), each with file:line references and improvement suggestions.

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
