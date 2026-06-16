# Question-First Gate

Use this gate before implementation, generation, or subagent dispatch that writes code.

## Purpose

The cheapest defect to fix is the one that never reaches code. Before writing files, surface ambiguity whose wrong answer would force a rewrite.

## Gate

Before any code-producing step:

1. Read the spec, task, Spec Reference, and immediate ownership context.
2. Enumerate genuinely ambiguous decisions.
3. If none exist, proceed. If any exist, return `NEEDS_CONTEXT` with the questions listed.

## Genuine Ambiguity

| Must ask | Do not ask |
|---|---|
| Public interface shape, return type, error model | Local variable name |
| Data field consumed by other tasks | Internal helper split |
| Naming that conflicts with existing repo names | Comment style |
| Library choice when multiple installed options exist | Lint-fixable formatting |
| Documented edge behavior missing from the spec | Whether to inline a small helper |
| Auth or permission boundary | Test file granularity |

If a repository file can answer the question, read it first. This gate is for unresolved ambiguity, not skipped discovery.

## Question Format

```text
NEEDS_CONTEXT

Before implementation, the following decisions need clarification:

1. <decision point>
   Options seen in repo / spec:
     a) <option A> - <where it appears>
     b) <option B> - <where it appears>
   Why this matters: <consequence of getting it wrong>
```

Ask only questions whose answers would change the implementation.
