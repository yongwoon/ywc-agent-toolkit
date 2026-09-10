# Sequential Quality-Gate Steps

> **Action required**: Read [../../references/quality-gates.md](../../references/quality-gates.md). This procedure is only the sequential-executor handoff; it does not replace the canonical contract.

## Procedure

1. Resolve the task packet after normal Step 4 verification and before optional implementation review or delivery.
2. If the packet is absent, record exactly `N/A — no quality gate contract` and continue the existing lifecycle. Do not emit placeholder fields or dispatch a worker.
3. For `report-only`, retain sanitized evidence and gaps without dispatching Cleaner or Hardener.
4. For `advisory` or `enforced`, validate the complete packet, immutable approved command IDs and digests, repository-relative bounded evidence paths, and both production and test/fixture Ownership symbol sets. Invalid or incomplete input is `NEEDS_CONTEXT` with no edit.
5. Dispatch one Cleaner only when complexity is above the caller-approved threshold. Cleaner is production-only and must return sanitized pre/post baseline-test evidence and changed paths. A threshold pass is a legitimate skip.
6. Dispatch one Hardener only after a legitimate Cleaner skip or Cleaner `DONE`/`DONE_WITH_CONCERNS`, and only when sanitized mutation evidence shows remaining work. Hardener is test/fixture-only, is capped at three attempts, and forwards all residual survivors without an equivalence claim.
7. Do not dispatch Hardener after Cleaner `BLOCKED` or `NEEDS_CONTEXT`. Neither worker has staging, commit, push, PR, merge, delivery, or delegation authority.
8. Aggregate each gate and the lifecycle monotonically using `BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`. Preserve all sanitized evidence and residual survivors; later `DONE` cannot mask an earlier stronger status.

## Status routing before delivery

Route the aggregate quality-gate status before entering optional implementation review or `ywc-finish-branch` delivery:

- `BLOCKED`: do not dispatch review or delivery. Preserve the task branch, any in-progress merge state, the Step 4.5 checkpoint, and sanitized blocker/residual evidence for recovery.
- `NEEDS_CONTEXT`: do not dispatch review or delivery. Preserve the task branch and recovery checkpoint; provide the missing context and revalidate the same immutable packet and exact Ownership before re-dispatching.
- `DONE_WITH_CONCERNS`: read the contract concerns. Resolve correctness or scope concerns and re-dispatch the affected gate before review or delivery; observation-level concerns may proceed only when recorded in the Completion Report with sanitized evidence and residuals retained.
- `DONE`: continue to optional review, then delivery, subject to the existing review and finish-branch status gates.

Quality-gate routing is authoritative for this stage: no later review or delivery result may convert a blocked or context-incomplete gate into delivery eligibility.

## Retry and idempotency

The executor performs at most one Cleaner dispatch and at most one conditional Hardener dispatch per task. A recovery attempt revalidates the same immutable packet and Ownership; it does not broaden paths, replace command identities/digests, replay a completed worker, or bypass the ordering gate. Hardener uses at most three approved attempts within its single dispatch.

## Completion evidence

The Completion Report carries only the contract state, aggregate/worker statuses, sanitized evidence paths, changed-path checks, and residual survivors. Never forward raw commands, raw output, transcripts, credentials, secrets, or full diffs.

## Rationalization Defense

| Excuse | Reality |
|---|---|
| “The task has a quality contract, so missing fields can be inferred.” | Missing, contradictory, unauthorized, or unbounded packet data is `NEEDS_CONTEXT`; dispatch does not begin. |
| “Hardener can run while Cleaner is blocked.” | Cleaner `BLOCKED` or `NEEDS_CONTEXT` forbids Hardener dispatch. |
| “The last worker returned DONE, so the task is clean.” | Aggregation is monotonic; `BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`, and earlier concerns remain. |
| “A retry can broaden the worker’s scope.” | Retries bind to the same exact Ownership paths and symbols; scope expansion is `NEEDS_CONTEXT`. |
