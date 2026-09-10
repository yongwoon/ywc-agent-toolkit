# ADR-0001: Isolate wave delivery behind a Hardener-gated integration branch, except for `--per-task-pr`

**Status:** Accepted
**Date:** 2026-09-10
**Provenance:** `ywc-plan` Step 3.5 (`docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.architecture-verdict.md`), plan `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md`
**Scope:** `claude-code/skills/ywc-parallel-executor/`, `codex/skills/ywc-parallel-executor/`

## Context

`ywc-parallel-executor`'s wave-boundary mutation gate (Hardener, Step 4e.5) ran *after* every task in the wave had already been merged into the base branch. Hardener needs the wave's merged diff to see cross-task interaction defects — a gap only visible once the tasks are combined — so it could only run post-merge. The consequence: an `enforced`-tier `BLOCKED` verdict from Hardener could no longer prevent anything from reaching base. The gate existed but had no blocking authority at the moment it mattered.

The codex root had the identical defect, plus a pre-existing, unrelated bug: its wave-boundary aggregation step (`4e.5`) was headed and numbered as if it ran *after* delivery, while its own prose already said "Before delivery, aggregate…" — a numbering/placement contradiction independent of the isolation question, fixed alongside this decision (see Consequences).

The remedy considered was a temporary **wave integration branch** (`wave-int/<N>`): merge wave tasks there instead of directly into base, run Hardener against it, and promote to base only on a passing verdict. The open question the architecture verdict resolved was not "should we do this" but whether the integration-branch model should apply **uniformly** across `ywc-parallel-executor`'s four delivery modes (`--local-merge`, `--draft`, `--aggregate-pr`, `--per-task-pr`), or whether one mode should deliberately diverge — and by what principled rule, not by per-mode enumeration.

## Decision

We will route `--local-merge`, `--draft`, and `--aggregate-pr` wave delivery through a Hardener-gated integration branch, `wave-int/<N>`, created only when the wave contains at least one task with a declared Quality Gate Contract. `--per-task-pr` is **permanently excluded** from this isolation and keeps today's direct-to-base ordering.

The governing rule, verbatim from the architecture advisor: *an isolation branch can only protect state whose point-of-no-return sits after the gate.* For the three isolated modes, the point-of-no-return is end-of-run (`--draft`/`--aggregate-pr`) or a re-pushable local base (`--local-merge`) — both after the Hardener gate. For `--per-task-pr`, the point-of-no-return is `gh pr merge --delete-branch`, reached once per task, **inside** the wave — no branch topology can move a per-task irreversibility boundary behind a wave boundary. This is a timing property, not a topology one. Under `--per-task-pr`, the wave-boundary check still runs but stays reporting-only and may never return `BLOCKED` even under an `enforced` contract; blocking authority for that mode lives entirely at Step 4c.5, which already runs per-task before PR creation.

A new promotion step, labeled `4e.6` in both roots, runs after Hardener and before worktree cleanup: on a non-blocking verdict it fast-forwards base to `wave-int/<N>` and stamps `wave-complete`; on a blocking verdict it leaves base untouched, preserves the integration branch and every task worktree, and skips cleanup for the wave. **`wave-complete`'s meaning changes from "wave finished" to "wave promoted"** for any wave that created an integration branch — a fully contract-less wave, or any `--per-task-pr` wave, keeps today's meaning unchanged.

## Alternatives Considered

- **Option B — Uniform isolation, including `--per-task-pr`** — rejected. Retargeting each task's PR base to `wave-int/<N>` requires a second `wave-int → base` PR per wave: a full extra CI + bot-review cycle, and the project's required-checks / branch-protection rules are configured against the real base, not `wave-int/*`. Per-task PRs would no longer be reviewed against the branch they actually merge into. This is a rebuild of `--aggregate-pr` under a different flag name, not a genuine simplification, and it destroys the exact signal `--per-task-pr` exists to buy: bot review, CI, and branch protection evaluated against the real base.
- **Option C — Severity-scoped isolation (isolate only `enforced` contracts)** — rejected. Two branch topologies selected at runtime by contract severity is a modest cost saving on advisory-tier waves, but it means resume logic must first determine which topology a given wave used before it can even interpret checkpoint state — a strict increase in state-machine complexity for a marginal benefit.

## Consequences

**A future reader must not "fix" the `--per-task-pr` carve-out by making it uniform.** This is a permanent, deliberate exclusion, not an oversight or a temporary gap in feature parity. Retargeting `--per-task-pr` to `wave-int/<N>` (Option B) is unsound, not merely more expensive — it removes the real-base bot review, CI, and branch-protection evaluation that mode exists to provide. Any change proposing to unify the four modes' delivery topology must re-litigate this ADR explicitly, not silently override it as a refactor.

`wave-complete` now means two different things depending on whether a wave created an integration branch: "wave promoted" for a contract-bearing wave under an isolated mode, "wave finished" (unchanged) for a contract-less wave or any `--per-task-pr` wave. Any future code or prose reading `wave-complete` must account for both meanings rather than assuming the pre-ADR uniform semantics.

The codex root's pre-existing `4e.5` numbering/placement contradiction (prose said "before delivery", heading position implied after) is corrected as part of this change — the wave-boundary aggregation now sits, in both text and number, after the per-task delivery loop and before `4e.6` promotion, matching its own stated intent. This was a bug fix bundled with this decision, not a new divergence between the two roots.

Base-branch fast-forward can fail if base advances during the wave; the promotion step handles this by merging base into `wave-int/<N>` (never rebasing) and re-running Hardener before retrying, bounded by a two-counter attempt limit (a fresh Mutation Loop Cap per dispatch, and a separate `promotion_retry_count` capped at 2 for live-lock). Any future change to base-advance handling during promotion must preserve this bound rather than retrying unboundedly.
