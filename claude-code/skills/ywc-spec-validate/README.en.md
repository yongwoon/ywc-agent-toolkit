# ywc-spec-validate

A Spec Reviewer Agent Skill that validates specification quality after writing specs and before running the task-generator.

## Usage

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md --tasks tasks/
```

> Passing `--tasks <dir>` adds a Cross-Artifact (Analyze) pass once tasks exist — it verifies every spec requirement is covered by a task and no task is orphaned.

## Review Dimensions

| Dimension          | What is reviewed                                                      |
| ------------------ | --------------------------------------------------------------------- |
| Completeness       | Missing required items (Error Handling, Edge Cases, Pagination, etc.) |
| Consistency        | Terminology/format/data structure mismatches across documents         |
| Feasibility        | Whether it can be implemented with the current stack                  |
| Code compatibility | Conflicts with existing DB Schema and API Route patterns              |
| Simplicity         | Abstraction, configurability, or generality the stated scope does not yet require (over-engineering) — surfaced as a Warning within the Feasibility pass |

## Execution Agent

### Phase 1 — Parallel Analysis (Sonnet × 4)

| Subagent | Dimension |
|---|---|
| Completeness Subagent | Completeness |
| Consistency Subagent | Consistency |
| Feasibility Subagent | Feasibility |
| Code Compatibility Subagent | Code Compatibility |

### Phase 2 — Advisor (Opus, up to 2 calls)

Opus Advisor provides judgment for ambiguous findings only. `--advisor-budget <n>` controls the per-invocation escalation count; `--advisor-budget 0` disables escalation and reports those findings as normal Suggestions (for orchestrator cost guarding).

## Output Format

Issues classified by severity (Critical / Warning / Suggestion), each with file:line references and improvement suggestions.

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
