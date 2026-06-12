# Subagent Status Actions

Use this when an orchestrating skill receives `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT` from a delegated subagent or child skill.

## Status Responses

| Returned status | Orchestrator response |
|---|---|
| `DONE` | Integrate the result. Do not redo validation the subagent already performed. |
| `DONE_WITH_CONCERNS` | Read the concerns. Correctness or scope concerns must be resolved before integration; observation-level concerns may be carried into the final report. |
| `NEEDS_CONTEXT` | Provide the missing context and re-dispatch the same subagent with the same model class. Context is the cheapest fix. |
| `BLOCKED` | Apply the triage below before surfacing to the user. |

## Return Payload Contract

When a subagent emits its status, the **payload returned to the orchestrator must be lean**. The orchestrator's main context is finite and is shared across the entire skill chain; a verbose return from a single fan-out subagent can push the main context past its budget within one or two waves.

The canonical return shape:

| Field | Limit | Required when |
|---|---|---|
| Status | one of `DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT` | always |
| Summary | 1 sentence, ≤ 200 chars | always |
| Artifacts | file path(s) only | work produced output |
| Concerns | ≤ 10 lines total | `DONE_WITH_CONCERNS` |
| Blocker | ≤ 5 lines | `BLOCKED` (feeds the triage below) |
| Missing context | bullet list, ≤ 10 items | `NEEDS_CONTEXT` |

**The return MUST NOT contain:**

- Generated source code (write to file, return the path)
- Full review findings, security audits, or analysis outputs (write to file)
- Verbose chain-of-thought or "I considered X, Y, Z before deciding ..."
- Re-stated prompt content — the orchestrator already has it
- Multi-screen tables — paginate by writing to a file and returning the path

**Why this contract exists**: fan-out skills (e.g., `ywc-code-gen`, `ywc-impl-review`, `ywc-parallel-executor`, `ywc-spec-validate`) dispatch 3+ subagents per phase. Without a payload cap, three verbose returns of ~2 KB each = 6 KB of inline payload **per phase**, and the orchestrator continues running for several more steps. Two phases of fan-out plus a 5-layer skill chain (e.g., `ywc-sequential-executor` → `ywc-finish-branch` → `ywc-create-pr` → `ywc-commit` → `ywc-ubiquitous-language`) saturates the context window before the work completes.

**Enforcement**: every fan-out skill must inject the following directive **verbatim** into each subagent prompt (alongside the existing Completeness and Tool-Error-Recovery directives):

> **Return-payload contract**: Reply with `Status | 1-line summary | artifact paths | (Concerns ≤ 10 lines | Blocker ≤ 5 lines | Missing-context bullets)`. Do not return generated code, full findings, full diffs, restated prompt content, or chain-of-thought. Write those to files and return the paths. The orchestrator will read the files only when it needs to.

## BLOCKED Triage

1. **Context problem**: provide the missing context and re-dispatch with the same model class.
2. **Reasoning problem**: re-dispatch once with a stronger model if available.
3. **Scope problem**: decompose into smaller pieces and re-aggregate.
4. **Plan problem**: the blocker reveals the plan itself is wrong (impossible requirement, missing prerequisite, contradictory specification). Surface to the user — **in a structured form, not a bare halt**. The surface message must contain:
   1. **What was attempted** — one line per triage step (1, 2, 3) already tried and what each returned
   2. **Blocker (verbatim)** — the subagent's BLOCKED text, quoted exactly; reference the offending plan line if identifiable
   3. **Proposed default action** — the orchestrator's best-guess next step that would make progress (e.g., "skip requirement R and proceed with remaining tasks", "ask the spec author to clarify line N"). The user can accept, reject, or replace this

   Do not retry the subagent. Do not silently work around. But also do not emit a generic "halted, awaiting input" — that wastes a round-trip on a problem the orchestrator already understood well enough to triage. The structured surface lets the user respond with a single confirmation in the common case.

Do not retry the same input unchanged. Change the context, model class, scope, or plan before another dispatch.

## Aggregating Status

All `DONE` -> `DONE`. Observation-level concerns -> `DONE_WITH_CONCERNS`. Resolved correctness concerns -> `DONE`. Unresolved `BLOCKED` -> `BLOCKED`. Unresolved `NEEDS_CONTEXT` -> `NEEDS_CONTEXT`.
