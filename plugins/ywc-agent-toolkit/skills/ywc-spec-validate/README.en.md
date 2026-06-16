# ywc-spec-validate

A Spec Reviewer Agent Skill that validates specification quality after writing specs and before running the task-generator.

## Usage

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
/ywc-spec-validate --spec docs/ywc-plans/example.md --advisor-budget 0
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

## Advisor Budget

`--advisor-budget <n>` sets the Phase 2 advisor budget for this invocation. Omitted uses the default `2`; `0` disables advisor escalation. The report header includes `Phase 2 advisor calls used: X of N (...)` and `Advisor budget status: available | disabled | exhausted | advisor-required | not-reported`.

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
