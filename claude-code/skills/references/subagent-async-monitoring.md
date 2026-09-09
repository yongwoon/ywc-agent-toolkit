# Subagent Async Monitoring Contract

Use this when an orchestrating skill dispatches a **concurrent batch** of subagents via the `Agent` tool (a wave in `ywc-parallel-executor`, the 5-way Phase 1 fan-out or the 20-way Step 4.5 verifier fan-out in `ywc-impl-review`, or a bounded single Opus advisor dispatch). This contract exists because a concurrently-dispatched subagent's completion notification can arrive out of order or late — treating notification order or count alone as a proxy for completion has previously caused a completed subagent to be mistaken for still-pending.

## Unique Dispatch Labeling

Every subagent dispatched as part of a concurrent batch must be given a name that deterministically maps back to what it was dispatched for — task name for `ywc-parallel-executor`, `<aspect>-<verifier-index>` for `ywc-impl-review`'s verifier fan-out. Never a generic or reused label across a batch.

## Full-Roster Reconciliation

Before treating a batch as complete, the orchestrator must reconcile the full expected roster (the set of names it dispatched) against the set of names it has received a terminal status for — via the orchestrating session's agent-roster-listing capability, where the runtime provides one, or otherwise the batch's own tracked state (a checklist of dispatched names ticked off as each terminal status arrives). Never infer completion from notification arrival order or count alone.

Reconciliation must be safe to invoke repeatedly against the same state: a duplicate terminal-status notification for an already-reconciled name is a no-op, never treated as a second batch member.

## Mandatory Fallback Wakeup

After dispatching any batch — including a single bounded dispatch such as `ywc-sequential-executor`'s Opus advisor call — the orchestrator sets an explicit bounded wait/check point — the orchestrating session's scheduled-recheck capability, where the runtime provides one, or otherwise a manual "check back after N seconds" discipline it holds itself to — rather than passively waiting on notifications alone.

| Batch size | Soft-check interval | Hard escalation threshold |
|---|---|---|
| 1 (single bounded dispatch, e.g. one Opus advisor call) | 480s | 900s |
| 2–4 concurrent subagents | 480s | 900s |
| 5+ concurrent subagents (e.g. impl-review Phase 1, Step 4.5) | 300s | 600s |

Cancel the fallback the instant full-roster reconciliation confirms every dispatched name has a terminal status — never let a stale fallback fire after the batch is already known complete.

## Bounded Escalation on Stall

If the hard escalation threshold is reached and full-roster reconciliation still shows one or more names without a terminal status, treat it as the batch-level equivalent of `BLOCKED` per [subagent-status-actions.md](./subagent-status-actions.md). Do not keep waiting indefinitely. Do not silently re-dispatch. Surface which named subagent(s) are unaccounted for.

## Known Limitations

This contract mitigates but does not eliminate notification races: a subagent whose process exits without ever emitting a terminal status is indistinguishable from one that is merely slow until the hard escalation threshold fires.
