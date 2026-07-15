# ywc-wayfinder

A discovery Skill for large or uncertain changes that need a deterministic local map across multiple sessions. It keeps exactly one active ticket in a Markdown map and routes the next step instead of implementing code.

## Use Cases

- Too much unresolved context for ordinary planning
- Discovery that must resume across multiple sessions
- A local, reviewable handoff without external tracker writes

## Core Contract

- Canonical map path: `docs/ywc-plans/<slug>-wayfinder.md`
- Exactly one active ticket
- Terminal resolved state returns `DONE` with no final write
- Terminal deferred or blocked state returns `NEEDS_CONTEXT` with no final write
