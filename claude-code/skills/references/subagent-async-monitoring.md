# Subagent Async Monitoring Contract

Use this when an orchestrating skill dispatches a **concurrent batch** of subagents via the `Agent` tool (a wave in `ywc-parallel-executor`, the 5-way Phase 1 fan-out or the 20-way Step 4.5 verifier fan-out in `ywc-impl-review`, or a bounded single Opus advisor dispatch). This contract exists because a concurrently-dispatched subagent's completion notification can arrive out of order or late — treating notification order or count alone as a proxy for completion has previously caused a completed subagent to be mistaken for still-pending.

## Unique Dispatch Labeling

Every subagent dispatched as part of a concurrent batch must be given a name that deterministically maps back to what it was dispatched for — task name for `ywc-parallel-executor`, `<aspect>-<verifier-index>` for `ywc-impl-review`'s verifier fan-out. Never a generic or reused label across a batch.

## Full-Roster Reconciliation

Before treating a batch as complete, the orchestrator must reconcile the full expected roster (the set of names it dispatched) against the set of names it has received a terminal status for — via the orchestrating session's agent-roster-listing capability, where the runtime provides one, or otherwise the batch's own tracked state (a checklist of dispatched names ticked off as each terminal status arrives). Never infer completion from notification arrival order or count alone.

Reconciliation must be safe to invoke repeatedly against the same state: a duplicate terminal-status notification for an already-reconciled name is a no-op, never treated as a second batch member.

## Waiting for Completion

Dispatching a batch — including a single bounded dispatch such as `ywc-sequential-executor`'s Opus advisor call — is asynchronous, but waiting on it is not something the orchestrator implements with its own timer. **End the turn after dispatching and let the harness `<task-notification>` arrive**, or let the user resuming the session serve as the reconciliation trigger. Do not call `ScheduleWakeup` to wait on a dispatched subagent — that tool is `/loop`-dynamic-pacing only, and using it here injects an unrelated `/loop` prompt into the session; the same applies to `Monitor` (it observes shell/WebSocket streams, not the `Agent` tool), a foreground `sleep` in `Bash` (blocked by the harness), or any other active polling/scheduling mechanism. The turn boundary is the waiting primitive — what makes completion detection reliable is the Full-Roster Reconciliation that runs when the turn resumes, not a timer that fires while it is suspended.

The Threshold table below still matters: it defines the elapsed-time bands `## Bounded Escalation on Stall` measures against once a signal — a `<task-notification>` or the user resuming the session — actually arrives. Elapsed time is computed from the dispatch's wall-clock time to the current signal's wall-clock time, not from any timer this contract arms.

| Batch size | Soft-check interval | Hard escalation threshold |
|---|---|---|
| 1 (single bounded dispatch, e.g. one Opus advisor call) | 480s | 900s |
| 2–4 concurrent subagents | 480s | 900s |
| 5+ concurrent subagents (e.g. impl-review Phase 1, Step 4.5) | 300s | 600s |

There is no fallback to cancel: with waiting done at the turn boundary, nothing is armed while the batch runs. If every dispatch in a batch goes silent and no signal ever arrives, the turn stays ended and control sits with the user — a visible, recoverable state — rather than a synthetic timer manufacturing activity the session cannot act on. Do not engineer around it.

## Bounded Escalation on Stall

If the hard escalation threshold is reached and full-roster reconciliation still shows one or more names without a terminal status, treat it as the batch-level equivalent of `BLOCKED` per [subagent-status-actions.md](./subagent-status-actions.md). Do not keep waiting indefinitely. Do not silently re-dispatch. Surface which named subagent(s) are unaccounted for.

## Known Limitations

This contract mitigates but does not eliminate notification races: a subagent whose process exits without ever emitting a terminal status is indistinguishable from one that is merely slow, right up until a signal arrives and elapsed time is found to cross the hard escalation threshold. If no signal ever arrives, that comparison never runs at all — per `## Waiting for Completion`, the turn simply stays ended, so this is a detection gap, not just a delay: an exited-without-status subagent in a batch that otherwise goes fully silent can leave the batch permanently unescalated rather than merely slow to escalate.
