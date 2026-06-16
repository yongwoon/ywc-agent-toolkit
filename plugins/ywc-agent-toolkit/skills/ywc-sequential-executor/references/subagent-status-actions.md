# Subagent Status Actions

Use this when an orchestrating skill receives `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT` from a delegated subagent or child skill.

## Status Responses

| Returned status | Orchestrator response |
|---|---|
| `DONE` | Integrate the result. Do not redo validation the subagent already performed. |
| `DONE_WITH_CONCERNS` | Read the concerns. Correctness or scope concerns must be resolved before integration; observation-level concerns may be carried into the final report. |
| `NEEDS_CONTEXT` | Provide the missing context and re-dispatch the same subagent with the same model class. Context is the cheapest fix. |
| `BLOCKED` | Apply the triage below before surfacing to the user. |

## BLOCKED Triage

1. **Context problem**: provide the missing context and re-dispatch with the same model class.
2. **Reasoning problem**: re-dispatch once with a stronger model if available.
3. **Scope problem**: decompose into smaller pieces and re-aggregate.
4. **Plan problem**: surface to the user. Do not retry around an impossible or contradictory plan.

Do not retry the same input unchanged. Change the context, model class, scope, or plan before another dispatch.

## Aggregating Status

All `DONE` -> `DONE`. Observation-level concerns -> `DONE_WITH_CONCERNS`. Resolved correctness concerns -> `DONE`. Unresolved `BLOCKED` -> `BLOCKED`. Unresolved `NEEDS_CONTEXT` -> `NEEDS_CONTEXT`.
