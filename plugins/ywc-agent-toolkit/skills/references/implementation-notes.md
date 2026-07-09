# Implementation Notes

> Shared reference document. Linked from code-producing or executor skills that
> need a lightweight place to preserve non-obvious implementation decisions.

## Purpose

Implementation notes capture the small set of discoveries that materially shaped
 the final output but are easy to lose if the worker only reports "done."

This reference exists so those discoveries are preserved without turning every
task into a diary or a raw log dump.

## What Belongs Here

Record only decision-shaping findings such as:

- Unexpected constraints discovered during implementation
- An alternative considered and rejected because of repository reality
- An assumption that was verified or invalidated mid-flight
- A local workaround or boundary chosen to preserve scope or compatibility

## What Does Not Belong Here

Do not record:

- Routine progress updates
- Full command logs
- Evidence already shown elsewhere in the report
- Generic observations that did not affect the implementation
- Future roadmap ideas outside the task scope

## When Notes Are Required

Implementation notes are required only when a non-obvious decision materially
affected the final code, document, or executor behavior.

If the implementation followed the planned path with no meaningful deviations,
use `N/A — no implementation-shaping discoveries`.

## Output Surface

Do not create a new mandatory artifact just for these notes.

Prefer the skill's existing surface:

- Final report section
- Per-agent summary
- Completion summary
- Per-task completion note

The calling skill decides the exact location, but the note content must stay
short and operational.

## Suggested Shape

Use 1–3 bullets:

```text
Implementation Notes
- Constraint: <what was discovered>
- Decision: <what changed because of it>
- Verification: <how the team can confirm this was real>
```

If only one bullet is needed, keep only the most important point.

## Guardrails

- Notes supplement verification; they do not replace it.
- Notes do not authorize scope expansion.
- Notes do not justify speculative abstractions.
- If a note reveals a true blocker, return `BLOCKED` or `NEEDS_CONTEXT` instead of burying it in a summary.
