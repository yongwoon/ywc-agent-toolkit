# ywc-project-mission

A skill that persists a project's durable Mission / North-Star, measurable Success Criteria, and Out-of-Scope non-goals to `docs/project-mission.md` — a committed, runtime-agnostic Markdown file. It follows the same stateful-file architecture as `ywc-review-learnings`: `ywc-plan` loads this file before clarifying any new request, so every planning session is framed by the same north-star instead of being re-derived from scratch.

The key idea: unlike a one-off plan that is discarded once a feature ships, the Mission records the *durable* intent that outlives any single feature. Each entry carries its provenance and date, so a reader can tell a current commitment from an abandoned direction.

## Supported Modes

- **read** — load the Mission to frame planning (typically called by `ywc-plan`)
- **update** — capture or revise Mission / Success Criteria / non-goals from a confirmed source
- **list** — display the current Mission
- **curate** — deprecate stale or superseded entries (never hard-delete)

## When to Use

- When you want to persist the Mission (What+Why) and Success Criteria (Done When) produced by a brainstorm at the project level
- When you want `ywc-plan` to frame its questions and Acceptance Criteria from the same Mission instead of re-deriving the north-star every session
- When you want to record durable non-goals ("this project will never do X") explicitly
- When you want LLMs to understand the project Mission automatically by adding `@docs/project-mission.md` to CLAUDE.md

## How to Use

```bash
/ywc-project-mission
```

Or trigger via natural language:

> "Remember this project's mission"
> "Capture the success criteria"
> "What is the current project mission?"

## Input

- (optional) `--mode read|update|list|curate` — force a mode (auto-detected if omitted)
- (optional) `--source brainstorm|plan` — provenance for a Mission/criterion in update mode (default `brainstorm`)
- (optional) `--output <path>` — mission file path (default `docs/project-mission.md`)
- (optional) `--dry-run` — show the CHANGESET without writing

## Output

- `docs/project-mission.md` — Mission / North-Star, Success Criteria table (`ID | Criterion | Source | Added | Status`), Out of Scope, an auto-maintained Change Log
- On update: present an ADD / MODIFY / DEPRECATE CHANGESET, write only confirmed entries, print a `Mission updated` confirmation block
- On first file creation: print the `@docs/project-mission.md` CLAUDE.md activation prompt exactly once
- Idempotent re-run: an empty CHANGESET → no file write, no date bump

## Related Skills

- `ywc-brainstorm` — Step 6 Handoff offers to persist the Mission (What+Why) and Success Criteria (Done When) via `update --source brainstorm` (opt-in)
- `ywc-plan` — Step 1 loads the Mission in read mode to frame questions and seed Acceptance Criteria
- `ywc-review-learnings` — same per-project stateful-file architecture (read/update/list/curate, user-confirmed writes), different domain (durable intent vs review preferences)
- `ywc-ubiquitous-language` — manages domain *vocabulary*; this skill stores domain *intent* (do not confuse the two)
