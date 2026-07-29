---
name: ywc-adr
description: >-
  (ywc) Use when capturing, reading, listing, or curating (deprecating) a
  project's Architecture Decision Records — durable records of a
  hard-to-reverse architectural choice and the trade-off reasoning behind
  it. Triggers: "ADR 작성", "아키텍처 결정 기록해줘", "이 결정 ADR 로
  남겨줘", "architecture decision record", "record this decision", "curate
  an ADR", "deprecate ADR", "ADR-0004 정리해줘", "アーキテクチャ決定記録",
  "ADR作成". Do not use for durable project intent (use ywc-project-mission),
  review preferences (use ywc-review-learnings), domain vocabulary (use
  ywc-ubiquitous-language), or the planning process itself (use ywc-plan).
---

# ywc-adr

**Announce at start:** "I'm using the ywc-adr skill to capture, read, or list the project's Architecture Decision Records."

This skill produces or maintains `docs/adr/NNNN-<slug>.md` — one immutable-ish Markdown file per architectural decision, in the standard Nygard ADR shape (Context / Decision / Alternatives Considered / Consequences). It is the stateful-file sibling of `ywc-review-learnings` and `ywc-project-mission`: instead of a Step 3.5 verdict that lives only in one plan's `architecture-verdict.md`, a decision that clears the offer criteria below becomes a committed, human-readable record any future session can cite by a stable ID (`ADR-0007`) instead of re-deriving the reasoning or re-litigating a settled trade-off.

It operates in four modes: **new** (capture a fresh decision, optionally superseding an old one), **read** (load a compact block of active ADRs to frame planning or review), **list** (display all ADRs and their status), and **curate** (mark an ADR `Deprecated` when its context vanished without a formal successor). Each ADR carries its own date and provenance, so a future reader can tell an operative constraint from an abandoned one.

**One deliberate deviation from the family:** unlike `docs/review-learnings.md` or `docs/project-mission.md`, this skill does **not** print a `@docs/adr/` `CLAUDE.md` activation prompt. A single compact file is cheap to preload into every session; an unbounded directory of ADRs is not — most are irrelevant to any given request. ADRs are read on demand, filtered by `--target`, by whichever skill needs them (see Integration).

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "This decision seems obviously right, no alternatives to record" | An ADR without alternatives cannot tell a future reader why the "obvious" path wasn't taken instead — and the decisions worth recording are exactly the ones that will stop looking obvious in a year. If there is genuinely only one option, the decision fails the offer criteria below and should not become an ADR at all. |
| "The decision changed, I'll edit the old ADR's Decision section directly" | ADRs are point-in-time records; editing one rewrites history a future reader relies on ("why didn't they just do X" only has an answer if X's rejection is still on record). Write a new ADR and mark the old one `Superseded by ADR-NNNN` instead. |
| "Every Medium/Large `ywc-plan` run should offer to record an ADR" | Offering on every run trains the user to click through without reading, which turns a durable record into noise nobody trusts. Gate the offer on all three of hard-to-reverse, surprising-without-context, and a real trade-off between genuine alternatives — the same three-part test `ywc-plan` Step 3.5 already exists to answer. |
| "Skip Alternatives Considered, we already know we won't reconsider" | The reader who needs Alternatives most is the one two years from now asking why the team didn't just do the simpler thing. Without it, the ADR reads as an assertion, not a decision. |
| "Preload every ADR into CLAUDE.md the way review-learnings does" | Unlike a single compact file, a directory of ADRs grows unbounded and most entries are irrelevant to any one request. Read on demand, filtered by `--target`, per this skill's read mode — never blanket-preload. |
| "The decision clearly meets the offer criteria, I'll write the ADR without asking" | Meeting the offer criteria only justifies making the offer, not skipping confirmation. Every write in this family goes through a user-confirmed CHANGESET (`ADD` / `SUPERSEDE` / `DEPRECATE`) — this skill has no exception. |
| "`curate` found no direct successor, I'll leave the old ADR Accepted since deprecating loses information" | An ADR that no longer reflects the codebase but still reads `Accepted` misleads a future reader into applying a dead constraint. Mark it `Deprecated` with the reason — never hard-delete, but never leave it silently stale either. |

**Violating the letter of these rules is violating the spirit.** A directory of unconfirmed, alternative-less, or silently-stale ADRs teaches future sessions the wrong constraints — worse than having no ADRs at all, because it reads as authoritative.

## Arguments

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| `--mode` | `--mode new\|read\|list\|curate` | auto-detect | Force a specific mode (see Mode Detection below) |
| `--supersedes` | `--supersedes <ADR-NNNN>` | — | With `new` mode, the ADR this decision replaces. Flips the named ADR's status to `Superseded by ADR-<new-id>` in the same CHANGESET |
| `--target` | `--target <path\|area>` | all ADRs | With `read` mode, filter to ADRs whose recorded `Scope` field (see below) overlaps the given path or area |
| `--source` | `--source plan\|manual` | `manual` | Where the candidate decision comes from — `plan` (a `ywc-plan` Step 3.5 verdict) or `manual` (a decision stated directly in conversation). Recorded as provenance |
| `--output` | `--output <dir>` | `docs/adr/` | ADR directory |
| `--dry-run` | flag | off | Show the proposed CHANGESET without writing to disk |

### Mode Detection (when `--mode` is omitted)

| Condition | Auto-selected mode |
|---|---|
| Invoked by `ywc-plan` Step 3.5 or another skill to frame a decision, `docs/adr/` exists | `read` |
| User is stating a decision just made ("we decided to…", "ADR 로 남겨줘", "record this as an ADR") | `new` |
| Directory absent, user wants to start recording decisions | `new` (creates `docs/adr/` with ADR-0001) |
| User asks "what ADRs exist?" / "무슨 결정들이 기록돼 있어?" | `list` |
| User asks to clean up stale or superseded ADRs | `curate` |

## Workflow

### Mode: new — Capture a Decision

1. **Check the offer criteria** before proceeding. Record an ADR only when **all three** hold — otherwise this is normal project work, not a decision worth a durable record:
   - **Hard to reverse** — the cost of changing course later is meaningful (a data model shape, a module boundary, a sync-vs-async choice a dozen call sites will depend on).
   - **Surprising without context** — a future reader would reasonably ask "why did they do it this way?"
   - **Result of a real trade-off** — genuine alternatives existed and one was picked over the others for stated reasons.

   If any of the three is missing, say so and skip — do not write an ADR for a decision with no real alternative or no real cost to reversing.

2. **Gather the candidate.** From `--source plan`, take the framed decision, the trade-off table, and the chosen direction from the `ywc-plan` Step 3.5 verdict (`architecture-verdict.md` or equivalent). From `--source manual`, extract the decision, its context, and the alternatives from the conversation — ask for any of the four fields (Context / Decision / Alternatives / Consequences) that are missing rather than inventing them. Also record a **Scope** — the path or area this decision governs (e.g. `api/billing/`, `frontend`, or `repo-wide` if it applies everywhere) — asking for it if it isn't evident from context. `read --target` matches against this field (see [references/adr-format.md](references/adr-format.md) for the matching rule).

3. **Assign the next ID.** Read `docs/adr/` (if present) and pick the next zero-padded 4-digit sequence number (`0001`, `0002`, …). If the directory is absent, this is `0001` and creates the directory.

4. **Build the CHANGESET** for user confirmation:
   - `ADD` — the new ADR's Title, Scope, Context, Decision, Alternatives Considered, and Consequences, in full.
   - `SUPERSEDE` (only with `--supersedes`) — the old ADR's status line change to `Superseded by ADR-<new-id>`.

   Do not write anything the user has not confirmed.

5. **Apply and echo.** Write the confirmed ADR to `docs/adr/NNNN-<slug>.md` using the format in [references/adr-format.md](references/adr-format.md). If superseding, update only the old ADR's status line (never its Context / Decision / Consequences body — see Rationalization Defense). Print an `ADR recorded` confirmation block naming the new ID and, if applicable, the superseded ID.

### Mode: read — Load Applicable ADRs

Invoked before planning or review (typically by `ywc-plan` Step 2, or `ywc-onboard-repo`).

1. **Read the directory.** If `docs/adr/` is absent, return an empty set and say so — never block planning or review on a missing ADR directory.
2. **Filter.** Include an ADR if `--target` is omitted, or if the ADR's recorded `Scope` overlaps the given path/area per the matching rule in [references/adr-format.md](references/adr-format.md) (prefix/substring match; a `Scope` of `repo-wide` always matches; an ADR with no `Scope` recorded is treated as `repo-wide`). Skip `Deprecated` and `Superseded` entries unless the caller explicitly asks for history.
3. **Emit a compact block** — one line per active ADR: ID, Title, and a one-sentence gist of the Decision. Keep it tight; a caller drowning in ADR text plans worse, not better. The full Context / Alternatives / Consequences are available on request by reading the specific file.

### Mode: list — Display All ADRs

Print every ADR's ID, Title, Status, and Date, sorted by ID. Optionally filter by `--target`. Useful before starting `new` mode to confirm the next ID and check for a near-duplicate decision already on record.

### Mode: curate — Deprecate Stale ADRs

1. Read `docs/adr/`. Identify candidates: an ADR whose Decision no longer matches the codebase and has no formal successor, or one the user reports as abandoned.
2. Present a `DEPRECATE` list with the reason for each. On confirmation, change only the status line to `Deprecated: <reason>, <date>` — never edit or delete the Context / Decision / Consequences body, and never hard-delete the file. Print an `ADR curated` confirmation block naming each deprecated ID and its reason.

## Output Format

The full per-ADR template (all four sections, the status-line grammar, and worked examples) is in [references/adr-format.md](references/adr-format.md).

**`docs/adr/0007-async-webhook-delivery.md` (file) summary:**

```markdown
# ADR-0007: Deliver webhooks asynchronously via a queue

**Status:** Accepted
**Date:** 2026-07-29
**Provenance:** ywc-plan Step 3.5 (architecture-verdict.md), plan `docs/ywc-plans/webhook-delivery.md`
**Scope:** `api/webhooks/`

## Context
<the forces at play: why synchronous delivery was the starting assumption, what broke it>

## Decision
<what was decided, as an action: "We will deliver webhooks through a durable queue, not inline in the request handler.">

## Alternatives Considered
<synchronous delivery with a timeout — rejected because X; a third-party delivery service — rejected because Y>

## Consequences
<what becomes easier/harder; what future work must respect this — e.g. "any new webhook type must publish to the same queue topic">
```

**Read-mode emission (injected into the caller):**

```text
## Applicable ADRs (2)
[ADR-0007] Deliver webhooks asynchronously via a queue — Accepted, 2026-07-29
[ADR-0003] Use Postgres row-level locking for the booking table — Accepted, 2026-05-14
```

**`ADR recorded` confirmation (new-mode emission):**

```text
✦ ADR recorded
  + ADR-0008 — Split the reporting service out of the monolith
        provenance: ywc-plan Step 3.5, plan docs/ywc-plans/reporting-split.md
  ~ ADR-0002 superseded — see ADR-0008
```

**`ADR curated` confirmation (curate-mode emission):**

```text
✦ ADR curated
  ~ ADR-0004 deprecated — reason: migrated off the custom job queue to a managed service months ago, no formal successor ADR was written
```

## Validation

Before declaring complete:

- [ ] Every recorded ADR passed all three offer criteria (hard to reverse, surprising, real trade-off)
- [ ] Every ADR has a non-empty Alternatives Considered section naming at least one genuine rejected option
- [ ] Every ADR has a `Status` of exactly `Accepted`, `Deprecated: <reason>, <date>`, or `Superseded by ADR-<id>`
- [ ] A `SUPERSEDE` never rewrote the old ADR's Context / Decision / Consequences body — only its status line
- [ ] The user confirmed the CHANGESET before any write (no inferred-and-written ADRs)
- [ ] `docs/adr/NNNN-<slug>.md` filenames use a contiguous, zero-padded 4-digit sequence with no gaps or reused IDs
- [ ] No `@docs/adr/` CLAUDE.md activation prompt was printed (deliberate deviation — see the skill summary)
- [ ] An `ADR recorded` confirmation was printed for `new` mode; an `ADR curated` confirmation was printed for `curate` mode

## Common Mistakes

- **Recording a decision with no real alternative** — the single most common failure. If there was only ever one viable path, this is not an ADR-worthy decision; skip it.
- **Editing an old ADR's body instead of superseding it** — destroys the historical record of why the earlier direction was chosen, which is often exactly what a later "why don't we just revert" conversation needs.
- **Treating an unconfirmed, obviously-qualifying decision as pre-approved** — meeting the offer criteria justifies the offer, never the write.
- **Blanket-preloading ADRs into CLAUDE.md** — defeats the reason this skill uses on-demand `read` mode instead of the family's usual `@`-activation prompt.

## Integration

- **Upstream**: `ywc-plan` Step 3.5 (Architectural Advisor Gate) — offers `new --source plan` once the gate's verdict clears the three-part test; Step 2 (Investigate the Codebase) calls `read` (best-effort) so a plan does not silently contradict a non-deprecated ADR.
- **Downstream**: `ywc-onboard-repo` and future planning sessions are natural consumers of `read` / `list` for an unfamiliar or evolving repo — no code change required on their side to benefit, since absence is a clean no-op.
- **Pairs with**: `ywc-review-learnings`, `ywc-project-mission` — same stateful-file family (user-confirmed CHANGESET, no-block invariant), different content domain (point-in-time architectural decisions vs. accumulating review preferences vs. durable project intent) and different storage shape (one immutable file per decision vs. one accumulating file).
- **Do not confuse with**: `ywc-architect` — the read-only advisor that *produces* the trade-off judgment this skill records; `ywc-architect` has no Write tool and never persists its own verdict.
