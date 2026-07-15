# Map and Ticket Contract

This file defines the deterministic local artifact used by `ywc-wayfinder`.

## Canonical Path

- `docs/ywc-plans/<slug>-wayfinder.md`

The path is project-relative and lives beside other planning artifacts so it can
be reviewed, resumed, and handed off without hidden state.

## Required Map Sections

Every map must include these top-level sections:

1. `# <slug> Wayfinder Map`
2. `## Destination`
3. `## Fog`
4. `## Local Status`
5. `## Tickets`
6. `## Evidence Log`
7. `## Next Context`

## Required Ticket Fields

Each ticket entry must record:

- `Ticket ID`
- `Question`
- `Status`
- `Route`
- `Evidence`
- `Next Context`

## One Active Ticket Rule

- Exactly one ticket may be `active`.
- Resolved tickets are historical context only.
- Deferred and blocked tickets are terminal unresolved states.
- Zero active tickets with unresolved work means the map is incomplete and must
  return `NEEDS_CONTEXT`.
- More than one active ticket is invalid and must return `NEEDS_CONTEXT`
  without writing.

## Allowed Ticket Status Values

- `active`
- `resolved`
- `deferred`
- `blocked`

Any other status is invalid.

## Terminal Behavior

- If every ticket is `resolved`, return `DONE` and do not write the map.
- If the terminal state is `deferred` or `blocked`, return `NEEDS_CONTEXT` and
  do not write the map.
- Invalid ticket structure or resume state also returns `NEEDS_CONTEXT` without
  writing.

## Write Discipline

- Creation may write the initial map.
- Resume may update only the active ticket and related evidence fields.
- Terminal evaluation does not append a final summary write.
- The skill never writes to an external tracker, database, or issue system.

## Route Semantics

- `ywc-plan` — route when discovery clarified the implementation path.
- `ywc-tech-research` — route when external technical comparison is still
  required.
- `ywc-spec-ready` — route when a spec exists but is not yet task-generator
  ready.
- `NEEDS_CONTEXT` — stop when ambiguity is still blocking deterministic routing.
