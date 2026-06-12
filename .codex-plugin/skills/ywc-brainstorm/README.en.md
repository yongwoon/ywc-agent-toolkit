# ywc-brainstorm

A Socratic-dialogue skill that turns a rough idea into an approved design before any implementation work begins.

## What It Does

Enforces the Hard Gate:

> **NO IMPLEMENTATION SKILL, SPEC DRAFTING, OR CODE WRITING UNTIL A DESIGN IS PRESENTED AND THE USER HAS APPROVED IT.**

A 6-step dialogue workflow:

1. **Step 1 — Explore project context** — Read affected-area `CLAUDE.md`, `docs/`, and recent commits to prevent stale assumptions.
2. **Step 2 — Detect "too big for one design"** — If the request spans multiple independent subsystems, STOP and decompose first.
3. **Step 3 — Ask clarifying questions one at a time** — Surface the four anchors (What / Why / Out of Scope / Done When), one question per message.
4. **Step 4 — Propose 2–3 approaches with trade-offs** — Lead with the recommendation; show the alternatives explicitly.
5. **Step 5 — Present the design and get approval** — Present in sections; confirm each before the final approval gate.
6. **Step 6 — Handoff to `ywc-plan`** — Pass the anchors and the chosen approach as explicit input.

The skill never branches directly into `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, or any executor — its terminal state is always invoking `ywc-plan`.

## When It Triggers

- The user says "idea", "brainstorm", "let's build", "アイディア", "구상", and similar.
- Intent is unclear or the implementation could go several ways.
- The request appears to span multiple subsystems.
- `ywc-plan` Step 1 delegates the clarification dialogue here.

## When NOT to Use

- The request already specifies file paths and acceptance criteria → use `ywc-plan` directly
- Validating an existing spec → `ywc-spec-validate`
- Choosing between libraries or frameworks → `ywc-tech-research` first
- Implementation-time questions → `ywc-code-gen`

## References

Full workflow and Rationalization Defense are in [SKILL.md](./SKILL.md). Underlying discipline is adapted from `superpowers:brainstorming`, tightened to hand off to `ywc-plan`.

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
