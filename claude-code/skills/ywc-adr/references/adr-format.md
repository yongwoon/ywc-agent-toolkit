# ADR File Format

Full specification for a `docs/adr/NNNN-<slug>.md` file. Referenced from `SKILL.md` Output Format.

## File naming

`docs/adr/NNNN-<slug>.md` — `NNNN` is a zero-padded 4-digit sequence starting at `0001`, contiguous, never reused even after an ADR is deprecated or superseded. `<slug>` is a short kebab-case summary of the Decision (not the Context), e.g. `0007-async-webhook-delivery.md`.

## Template

```markdown
# ADR-NNNN: <Title — the decision, stated as a short noun phrase>

**Status:** Accepted <!-- | Deprecated: <reason>, <date> | Superseded by ADR-MMMM -->
**Date:** YYYY-MM-DD
**Provenance:** <ywc-plan Step 3.5, plan <path> | manual, conversation>
**Scope:** <path|area this decision governs, e.g. `api/billing/`, `frontend` | `repo-wide`>

## Context

<The forces at play that made this a real decision rather than an obvious step:
constraints, prior state, what changed to force the choice. Written so a reader
with none of the current conversation's context can understand why a decision
was needed at all.>

## Decision

<What was decided, stated as an action the team commits to: "We will X." One or
two sentences — the elaboration belongs in Consequences, not here.>

## Alternatives Considered

<Every genuine alternative that was on the table, and why each was rejected.
At least one entry; a single "we also considered nothing else" line does not
satisfy this — if there was truly no alternative, the decision does not meet
the offer criteria and should not have become an ADR (see SKILL.md
Rationalization Defense).>

- **<Alternative A>** — rejected because <reason>
- **<Alternative B>** — rejected because <reason>

## Consequences

<What becomes easier or harder as a direct result of this decision. Include any
constraint future work must respect — e.g. "any new X must follow pattern Y" —
so a later session can tell whether a proposed change conflicts with this ADR.>
```

## Scope field and `--target` matching

`Scope` records the path or area this decision governs, so `read --target <path|area>` can decide which ADRs are relevant without loading every file. Matching rule:

- A `Scope` of `repo-wide` always matches any `--target`.
- Otherwise, the ADR matches when `--target` and `Scope` overlap as strings: `--target` is a prefix of `Scope`, `Scope` is a prefix of `--target`, or one contains the other (e.g. `--target api/billing` matches a `Scope` of `api/billing/`, and `--target api` matches a `Scope` of `api/billing/` too).
- An ADR written before this field existed, or with `Scope` omitted, is treated as `Scope: repo-wide` — never silently excluded from a `--target` filter for lack of a recorded scope.

## Status grammar

| Status line | Meaning |
|---|---|
| `**Status:** Accepted` | Currently operative; future work should respect the Decision and Consequences |
| `**Status:** Deprecated: <reason>, <date>` | No longer operative, and no specific ADR replaced it — the context that motivated it no longer holds |
| `**Status:** Superseded by ADR-MMMM` | Replaced by a specific later decision; read ADR-MMMM for the current direction |

A `curate` or `new --supersedes` write changes **only** this line — the Context / Decision / Alternatives Considered / Consequences body is never edited after the ADR is written. This is what makes an ADR a reliable historical record: a reader two years from now sees exactly what was decided and why, even after the decision itself has been superseded.

## Worked example

```markdown
# ADR-0007: Deliver webhooks asynchronously via a queue

**Status:** Accepted
**Date:** 2026-07-29
**Provenance:** ywc-plan Step 3.5 (architecture-verdict.md), plan docs/ywc-plans/webhook-delivery.md
**Scope:** api/webhooks/

## Context

The webhook delivery endpoint currently calls the subscriber's URL synchronously
inside the request handler that triggers the event. As subscriber count grew,
p95 latency on the triggering request climbed past 4s because it now waits on
the slowest subscriber. A single slow or down subscriber degrades the
triggering user's request, which has nothing to do with webhook delivery.

## Decision

We will deliver webhooks through a durable queue (existing `jobs` infrastructure)
instead of inline in the request handler. The triggering request enqueues a
delivery job and returns immediately; a worker pool performs the HTTP call with
retry and backoff.

## Alternatives Considered

- **Synchronous delivery with a short timeout** — rejected because a timeout
  still couples the triggering request's latency to subscriber health, and a
  short timeout increases false-negative delivery failures for slow-but-healthy
  subscribers.
- **Third-party webhook delivery service (e.g. Svix)** — rejected because it
  introduces a new paid dependency and an external data-egress path for
  customer event payloads that the current compliance review has not covered;
  revisit if in-house queue delivery proves insufficient at higher volume.

## Consequences

Triggering requests no longer block on subscriber latency; delivery failures
are now asynchronous and surfaced via the existing job-failure dashboard
instead of an inline error. Any new event type that needs webhook delivery
must publish to the same `webhook-delivery` job topic rather than calling
subscribers directly — a direct call from a new code path silently reintroduces
the coupling this ADR removed.
```
