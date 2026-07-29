# ywc-adr

A skill for managing a project's Architecture Decision Records (ADRs). Records architectural decisions that are hard to reverse, surprising without context, and the result of a real trade-off — one immutable-ish file per decision at `docs/adr/NNNN-<slug>.md`. It belongs to the same stateful-file family as `ywc-review-learnings` / `ywc-project-mission`, but stores differently: instead of one accumulating file, each decision gets its own file.

Until now, the verdict `ywc-plan`'s Step 3.5 (Architectural Advisor Gate) produces has lived only inside that one plan's `architecture-verdict.md` and then disappeared. When a decision clears the three-part offer test (hard to reverse + surprising without context + real trade-off), this skill turns that verdict into a durable record any future session can cite by a stable ID (`ADR-0007`).

## Supported Modes

- **new** — capture a fresh decision (optionally superseding an existing ADR)
- **read** — load a compact summary of relevant ADRs to frame planning or review
- **list** — display all ADRs and their status
- **curate** — mark an ADR `Deprecated` when its context vanished without a formal successor

**One deliberate deviation from the family:** unlike `docs/review-learnings.md` or `docs/project-mission.md`, this skill does not print an `@docs/adr/` CLAUDE.md activation prompt. A single compact file is cheap to preload every session; an unbounded ADR directory is not, and most entries are irrelevant to any given request. ADRs are instead loaded on demand via `read` mode, filtered by `--target`.

## Usage Scenarios

- The `ywc-plan` Step 3.5 architecture verdict clears the three-part test, and you want to turn that judgment into a durable ADR
- A new decision reverses a past one, and you want the record of why the direction changed (supersede)
- Before drafting a new spec, you want to confirm it doesn't contradict an already-settled architectural decision
- You want to clean up an old ADR that no longer reflects the codebase

## How to Use

```bash
/ywc-adr
```

Or invoke with natural language:

> "Record this decision as an ADR"
> "무슨 ADR 들이 있어?"
> "Clean up ADR-0004, it's no longer valid"

## Input

- (optional) `--mode new|read|list|curate` — force a specific mode (auto-detected if omitted)
- (optional) `--supersedes <ADR-NNNN>` — with `new` mode, the existing ADR this decision replaces
- (optional) `--target <path|area>` — with `read` mode, filter to ADRs whose recorded `Scope` field overlaps this path or area (an ADR with no `Scope` recorded is treated as `repo-wide`)
- (optional) `--source plan|manual` — where the decision comes from (default `manual`)
- (optional) `--output <dir>` — ADR directory path (default: `docs/adr/`)
- (optional) `--dry-run` — show the CHANGESET without writing

## Output

- `docs/adr/NNNN-<slug>.md` — a file with Title / Status / Date / Provenance / Scope plus Context / Decision / Alternatives Considered / Consequences sections
- On `new`: an `ADR recorded` confirmation block naming the new (and, if applicable, superseded) ID
- On `curate`: an `ADR curated` confirmation block naming each deprecated ID and its reason
- No CLAUDE.md activation prompt is printed (intentional — see above)

## Sample Output

```markdown
# ADR-0007: Deliver webhooks asynchronously via a queue

**Status:** Accepted
**Date:** 2026-07-29
**Provenance:** ywc-plan Step 3.5, plan docs/ywc-plans/webhook-delivery.md

## Context
...

## Decision
We will deliver webhooks through a durable queue, not inline in the request handler.

## Alternatives Considered
- Synchronous delivery with a timeout — rejected because ...
- Third-party delivery service — rejected because ...

## Consequences
...
```

## Related Skills

- `ywc-plan` — Step 3.5 (Architectural Advisor Gate) offers this skill's `new --source plan` as an opt-in, and Step 2 calls `read` mode to confirm the plan doesn't contradict an existing ADR
- `ywc-architect` — the read-only advisor that produces the trade-off judgment this skill records; it never persists its own verdict
- `ywc-review-learnings` / `ywc-project-mission` — same stateful-file family (user-confirmed writes, no-block on absence), different content domain and storage shape
