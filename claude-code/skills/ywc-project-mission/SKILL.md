---
name: ywc-project-mission
description: >-
  (ywc) Use when capturing, reading, or curating a project's durable Mission /
  North-Star, measurable Success Criteria, and Out-of-Scope non-goals — the
  stable "why this project exists" memory that frames every planning session
  (the stateful-file pattern, runtime-agnostic, committed Markdown). Triggers:
  "프로젝트 미션 정리", "project mission", "미션 작성", "north star 정의",
  "success criteria 정리", "프로젝트 목표 영속화", "이 프로젝트 미션 기억해둬",
  "プロジェクトミッション", "mission persistence", "remember the project mission",
  "capture project goals". Do not use for domain vocabulary / ubiquitous language
  (use ywc-ubiquitous-language), for accumulated code-review preferences
  (use ywc-review-learnings), for a single feature's implementation plan
  (use ywc-plan), or for spec-level review (use ywc-spec-validate).
---

# ywc-project-mission

**Announce at start:** "I'm using the ywc-project-mission skill to read or update the project's durable mission, success criteria, and non-goals."

This skill produces or maintains `docs/project-mission.md` — a per-project, accumulating record of the project's **durable** intent: the Mission / North-Star (why the project exists), the measurable Success Criteria (what "done" looks like at the project level), and the Out-of-Scope non-goals (what the project deliberately will not do). It is the stateful-file sibling of `ywc-review-learnings`: instead of a one-off plan that is discarded after a feature ships, the mission lives as a committed, human-editable Markdown file that `ywc-plan` loads before clarifying any new request, so every planning session is framed by the same north-star rather than re-derived from scratch.

It operates in four modes: **read** (load the mission to frame planning), **update** (capture or revise mission / criteria / non-goals from a confirmed source), **list** (display the current mission), and **curate** (deprecate stale or superseded entries). Each entry records its provenance and date, so a future reader (or LLM) can tell a current commitment from an abandoned one.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Write the mission I inferred from the code — confirmation is overhead" | An unconfirmed mission silently frames *every* future planning session on this project. The mission is a durable commitment, not a guess; always present the ADD / MODIFY / DEPRECATE CHANGESET for one confirmation round before writing. |
| "This success criterion is obvious — skip the measurable form" | A non-measurable criterion ("be fast", "be usable") cannot seed an Acceptance Criterion downstream and cannot tell `ywc-plan` whether a plan satisfies it. Every Success Criterion must be an observable, checkable done-condition. |
| "The new mission statement contradicts the old one — keep both" | Two contradictory mission statements make planning non-deterministic. Newest-wins: deprecate the old entry with `~~strikethrough~~` + a superseded-by note, never silently delete — the history of *why* the direction changed is itself signal. |
| "Re-running `update` is harmless — just bump the date" | A spurious `<!-- updated -->` bump on an identical file produces noise in `git log` and falsely signals the mission moved. An `update` with an empty CHANGESET must be a no-op: no file write, no date bump. |
| "Record a feature-level task here so it's not forgotten" | The mission file is for *durable* project intent, not the current sprint's task list. A transient task pollutes the north-star and ages into stale noise; route feature work to `ywc-plan` / the task system, and reserve this file for commitments that outlive any single feature. |
| "Drop the provenance — the entry speaks for itself" | Without provenance (`brainstorm` / `plan <ref>`) a reader cannot trace a criterion back to where it was agreed, so a stale entry can never be confidently retired. Record the source and date on every entry. |
| "Print the `@docs/project-mission.md` activation prompt on every update so the user sees it" | Repeating the CLAUDE.md activation reminder on each incremental update is noise. Print it **only** on first file creation — that is the one moment the reference does not yet exist. |

**Violating the letter of these rules is violating the spirit.** A mission file full of unconfirmed, non-measurable, or undated entries frames every future planning session with noise instead of signal — the opposite of its purpose.

## Arguments

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| `--mode` | `--mode read\|update\|list\|curate` | auto-detect | Force a specific mode (see Mode Detection below) |
| `--source` | `--source brainstorm\|plan` | `brainstorm` | Where a new mission/criterion comes from in `update` mode — `brainstorm` (a `ywc-brainstorm` handoff) or `plan` (a finalized `ywc-plan` success criterion). Recorded as provenance |
| `--output` | `--output <path>` | `docs/project-mission.md` | Mission file path |
| `--dry-run` | flag | off | Show the proposed CHANGESET without writing to disk |

### Mode Detection (when `--mode` is omitted)

| Condition | Auto-selected mode |
|---|---|
| Invoked by `ywc-plan` to frame a request, file exists | `read` |
| User is stating durable intent ("the mission is…", "success means…", "we will never…") | `update` |
| File absent, user wants to start a mission | `update` (creates the file with the first entry) |
| User asks "what is the project mission?" | `list` |

## Workflow

### Mode: read — Load the Mission to Frame Planning

Invoked before planning (typically by `ywc-plan` Step 1).

1. **Read the file.** If `docs/project-mission.md` is absent, return an empty mission and say so — never block planning on a missing mission file (NFR2 no-block invariant).
2. **Emit a compact mission block** in the [Mission block format](#output-format): the Mission / North-Star line, the active Success Criteria (skip `deprecated`), and the Out-of-Scope non-goals. Keep it tight — target ≤ ~25 lines (NFR1); a mission block that floods context degrades the planning it is meant to frame.

### Mode: update — Capture or Revise the Mission

1. **Read the existing file** in full (or note its absence to create it). Parse the current Mission, Success Criteria, and Out-of-Scope entries.
2. **Gather the candidate** from the declared `--source`. Mission statements must be durable (outlive any single feature); Success Criteria must be **measurable** (an observable done-condition); Out-of-Scope entries must name the non-goal and the reason.
3. **Classify against the existing file.** If a similar entry already exists, treat the candidate as a `MODIFY`, not a duplicate `ADD`. A candidate that contradicts an active entry is a `DEPRECATE` (old) + `ADD` (new), newest-wins.
4. **Build the CHANGESET** for user confirmation: `ADD` / `MODIFY` / `DEPRECATE` lists, each showing its provenance and date. Do not write any entry the user has not confirmed.
5. **Idempotency gate (AC15 / NFR3).** If the confirmed CHANGESET is empty — the candidate content is identical to what the file already holds — **make no write**: do not touch the file, do not bump `<!-- updated: DATE -->`. Report "mission unchanged" and stop.
6. **Apply and echo.** Write confirmed changes, update the `<!-- updated: DATE -->` header, append a `## Change Log` row, and print a `Mission updated` confirmation block listing exactly what changed.
7. **CLAUDE.md activation prompt (first creation only).** The *first* time the file is created (it did not exist before this run), print the activation reminder so the mission actually reaches future planning:
   ```text
   ★ To activate this mission, add the following line to your CLAUDE.md so every
     planning session (and every LLM session) loads it automatically:
       @docs/project-mission.md
   ```
   Print it only on first creation, not on every incremental update.

### Mode: list — Display the Current Mission

Print the active mission, Success Criteria, and Out-of-Scope non-goals. Show deprecated entries only when explicitly asked. Useful before planning to sanity-check the north-star the planner will apply.

### Mode: curate — Deprecate Stale / Superseded Entries

1. Read the file. Identify candidates: contradictory pairs, Success Criteria that no longer reflect the project, or entries the user reports as abandoned.
2. Present a `DEPRECATE` list with the reason for each. On confirmation, mark with `~~strikethrough~~` and a `> deprecated YYYY-MM-DD: <reason / superseded-by #ID>` note. Never hard-delete — the history of *why* a direction was abandoned is itself a learning.

## Output Format

The full mission-file specification (field rules, deprecation grammar, provenance grammar) is in [references/mission-format.md](references/mission-format.md).

**`docs/project-mission.md` (file) summary:**

```markdown
# Project Mission — [Project Name]

<!-- updated: YYYY-MM-DD -->

## Mission / North-Star
- <durable one-paragraph statement of what the project is and why>  (brainstorm, 2026-06-23)

## Success Criteria
| ID | Criterion (measurable) | Source | Added | Status |
|----|------------------------|--------|-------|--------|
| S001 | <observable done condition> | brainstorm / plan <ref> | 2026-06-23 | active |

## Out of Scope (durable non-goals)
- <non-goal> — <reason>  (2026-06-23)

## Change Log
| Date | Change | Source |
|------|--------|--------|
| 2026-06-23 | Created mission + S001 | brainstorm |
```

**Mission block (read-mode emission, injected into planning):**

```text
## Project Mission
North-Star: <durable one-paragraph statement>.
Success Criteria (2 active):
  [S001] <observable done condition>. (brainstorm, 2026-06-23)
  [S002] <observable done condition>. (plan #14, 2026-06-20)
Out of Scope: <non-goal>; <non-goal>.
```

**`Mission updated` confirmation (update-mode emission):**

```text
✦ Mission updated (1 ADD, 0 MODIFY, 1 DEPRECATE)
  + S004 [Success Criterion] — Median plan-to-first-task time under 10 minutes.
        source: plan #21, 2026-06-23
  ~ S002 deprecated — superseded by S004 (re-scoped from p95 to median).
```

## Validation

Before declaring complete:

- [ ] The Mission / North-Star statement is durable (outlives any single feature), not a feature description
- [ ] Every active Success Criterion is measurable (an observable done-condition), not a vague aspiration
- [ ] Every entry carries a `Source` (provenance) and a date (`Added` / inline `YYYY-MM-DD`)
- [ ] No two **active** entries contradict each other (the older was deprecated, not left to coexist)
- [ ] The user confirmed the CHANGESET before any write (no inferred-and-written entries)
- [ ] An `update` with no new content made no write and no `<!-- updated -->` bump (idempotency)
- [ ] `docs/project-mission.md` is parseable Markdown with no broken table rows
- [ ] `<!-- updated: DATE -->` header reflects today's date (on a real write only)
- [ ] A `Mission updated` confirmation was printed for update mode
- [ ] On first file creation, the `@docs/project-mission.md` CLAUDE.md activation prompt was printed once

## Common Mistakes

- **Writing an inferred mission without confirmation** — the single most damaging failure. An unconfirmed mission frames every future planning session; always confirm the CHANGESET first.
- **Non-measurable success criteria** — "be fast" cannot seed an Acceptance Criterion or tell the planner whether a plan satisfies it. Make every criterion observable.
- **Spurious date bumps** — re-running `update` on an identical file must be a no-op, not a fresh `<!-- updated -->` line.
- **Storing feature tasks as mission entries** — the mission is durable project intent, not the current sprint. Route transient work to `ywc-plan`.
- **Hard-deleting a superseded entry** — the reviewer/planner loses the record of why the direction changed. Deprecate with `~~strikethrough~~`, never delete.

## Integration

- **Upstream**: `ywc-brainstorm` (Step 6 Handoff offers to persist Mission + Success Criteria via `update --source brainstorm`), `ywc-plan` (Step 1 calls this skill in `read` mode to frame clarifying questions and seed Acceptance Criteria; may offer an `update --source plan` when a plan finalizes new durable criteria).
- **Downstream**: `ywc-plan` consumes the read-mode Mission block; the file is also a natural `@docs/project-mission.md` reference in `CLAUDE.md`.
- **Pairs with**: `ywc-review-learnings` — same per-project stateful-file architecture (read/update/list/curate, user-confirmed writes, first-creation activation prompt), different content domain (durable project intent vs review preferences).
- **Do not confuse with**: `ywc-ubiquitous-language` (shared domain *vocabulary*, modes new/extract/update) — this skill stores the durable *intent*, not the term glossary.
