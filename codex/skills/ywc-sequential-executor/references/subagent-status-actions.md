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

## Claim/Evidence Contract

`Claims` is an optional, bounded field in a dependent subagent's status payload.
It is evidence for the returned status, not a second status or a replacement for
the artifact written by the subagent.

```text
Claims:
  - Statement: <one bounded factual statement>
    Evidence: <project-relative/path.md:line or project-relative/artifact.md>
```

The contract is closed and rejects a payload rather than guessing or partially
repairing it:

- `Claims` contains at most **three** claim objects. An omitted field means no
  claims; an empty list is allowed only when the caller explicitly requested no
  claims.
- Each claim has exactly `Statement` and `Evidence`. `Statement` is required,
  factual, and at most 1,024 characters. `Evidence` is required and is either a
  project-relative `file:line` citation (with a positive decimal line number)
  or a project-relative artifact path. `Evidence` is at most 4,096 characters.
  A path is not evidence when it is absolute, escapes with `..`, uses a URI, or
  is only an unlabelled prose reference.
- The payload remains bounded by the base return contract: `Summary` is one
  sentence of at most 200 characters; `Concerns` is at most 10 lines;
  `Blocker` is at most 5 lines; and `Missing context` is at most 10 bullets.
  Claims do not carry generated source, full findings, full diffs, or a second
  copy of an artifact.
- A cap, shape, statement, or evidence violation is rejected as `BLOCKED`.
  The rejection may name only the field and bounded rule, for example
  `BLOCKED — claim contract rejected: Claims exceeds three items` or
  `BLOCKED — claim contract rejected: Evidence is not a project-relative
  file:line citation or artifact path`. Never echo the rejected value.

### Privacy rejection

Validation walks the complete payload recursively before any role projection.
It rejects the payload as `BLOCKED` if any object key, including a nested key,
is one of these fields or a normalized key containing one of these forbidden
tokens:
`transcript`, `chain_of_thought`, `generated_source`, `full_diff`,
`raw_tool_output`, `raw_response`, or `tool_output`. Normalization is
case-insensitive and ignores separators, so `raw-response`, `chainOfThought`,
and `tool_output_text` are rejected as equivalent raw-content fields. The
rejection diagnostic names only the offending field name and rule; it never
includes the field value, transcript, tool output, or a raw response.

This rule applies to `Claims`, `Evidence`, `Concerns`, `Blocker`, artifacts'
metadata, and any wrapper object supplied to a role. A privacy rejection is
terminal for that payload: do not redact, summarize, forward, or retry the same
payload unchanged.

### Role boundaries

Role projections are allowlists, not invitations to copy the source payload:

| Role | May receive | Must not receive |
|---|---|---|
| Independent reviewer | `Included scope`, `Excluded scope`, and `Artifacts` (paths only) | `Claims`, peer conclusions, peer recommendations, transcript, or any raw content |
| Dependent role | `Claims` and the cited artifact paths only | peer transcript, uncited artifacts, peer conclusions, peer recommendations, or raw content |

An independent reviewer forms its finding independently; another reviewer's
claim or conclusion is not context for that review. A dependent role may read a
cited artifact, but may not infer or receive additional context from the
producer's conversation. If a required citation or artifact is unavailable,
return `NEEDS_CONTEXT` with the missing path/citation rather than forwarding
the producer payload.

### Hardening/evaluation targets

The downstream context-safety evaluation owns executable fixtures for the
following RED-first cases: more than three claims, missing evidence, invalid
`file:line`/artifact paths, independent-role isolation, dependent-role
allowlisting, and every forbidden privacy field including nested and equivalent
spellings. This reference is the canonical contract those fixtures cite.

## PR Language Context

Language preferences are task context, not a completion status. Preserve any caller-supplied `--pr-lang` value when re-dispatching a task or delegating to downstream PR creation.

Do not translate branch names, task names, file paths, command output, or status tokens while carrying that context. Only human-facing PR title/body prose follows the selected language.
