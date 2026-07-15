---
name: ywc-wayfinder
description: >-
  (ywc) Use when a large or uncertain change needs multi-session discovery with
  a deterministic local map and exactly one active ticket before planning or
  implementation. Triggers: "wayfinder", "길찾기", "discovery map", "multi-session
  discovery", "탐색 ticket", "経路整理", "探索マップ", "ywc-wayfinder". Do not use
  for ordinary planning (use ywc-plan), idea clarification (use ywc-brainstorm),
  direct implementation, or tracker/database writes outside the local Markdown
  map.
---

# ywc-wayfinder

**Announce at start:** "I'm using the ywc-wayfinder skill to manage a deterministic local discovery map with one active ticket."

This skill manages a local Markdown map for large or uncertain discovery work.
It does not implement code, does not write to external trackers, and resolves
at most one active ticket per session before routing the next step.

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "This looks fuzzy, I'll just start coding and document later" | Wayfinder exists for fuzzy, multi-session discovery. If uncertainty is still material, coding first hides the unresolved decisions instead of shrinking them. |
| "I'll keep two active tickets open so I can explore faster" | Exactly one active ticket is the contract. Multiple active tickets destroy resume safety and make terminal status ambiguous. |
| "The map is only a note, I can rewrite history when resuming" | The map is the local source of truth. Resume must preserve ticket state, evidence, and next context exactly enough for the next session to continue deterministically. |
| "If everything is resolved, I'll still append a summary ticket" | Terminal maps do not write. When all tickets are resolved, return `DONE` without mutating the map. |
| "Deferred or blocked tickets can still be marked done if the route is obvious" | Deferred or blocked terminal state is `NEEDS_CONTEXT`, not `DONE`. A route idea is not the same as resolved context. |
| "This can replace normal planning now that the map exists" | Wayfinder is for discovery, not ordinary planning. Once the route is clear, hand off to `ywc-plan`, `ywc-tech-research`, or another downstream skill. |

## Workflow

1. **Qualify the request**
   - Use this skill only when the request is large, uncertain, or likely to span multiple sessions.
   - If the request is ordinary planning or a single-session design discussion, route to `ywc-plan` or `ywc-brainstorm` instead.

2. **Resolve the map path**
   - The canonical artifact is `docs/ywc-plans/<slug>-wayfinder.md`.
   - If the map does not exist, create it with the canonical fields from [references/map-ticket-contract.md](references/map-ticket-contract.md).
   - If the map exists, validate its structure before using it.

3. **Enforce one active ticket**
   - The map may contain many tickets, but only one may be marked active.
   - If zero active tickets remain and unresolved work still exists, return `NEEDS_CONTEXT`.
   - If more than one active ticket exists, return `NEEDS_CONTEXT` without writing.

4. **Work one ticket**
   - Update only the active ticket's evidence, route, and next-context fields.
   - Route unresolved implementation work onward; do not implement it here.
   - If the active ticket is invalid, stale, or contradicts the map state, return `NEEDS_CONTEXT` without writing.

5. **Handle terminal states**
   - If all tickets are resolved, return `DONE` and do not write the map again.
   - If the best terminal state is deferred or blocked, return `NEEDS_CONTEXT` and do not write.

6. **Route onward**
   - Use `ywc-plan` for a clarified implementation plan.
   - Use `ywc-tech-research` when the ticket is blocked on external technical comparison.
   - Use `ywc-task-generator` only after a downstream planning/spec path produces a finalized spec.

## Output Format

```text
Map: docs/ywc-plans/<slug>-wayfinder.md
Ticket: <ticket-id>
Route: <next skill or stop reason>
Completion Status: DONE | NEEDS_CONTEXT
```

## Validation

- `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-wayfinder`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/validate.sh`

## Integration

- **Upstream:** Large ambiguous requests, resumed discovery sessions, or downstream skills that need a local discovery handoff.
- **Downstream:** `ywc-plan`, `ywc-tech-research`, `ywc-spec-ready`, or another planning/research skill once the route is clear.
- **Never downstream directly to implementation:** Executors and code-generation skills require a clearer contract than a discovery ticket provides.
