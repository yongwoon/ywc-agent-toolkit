# Subagent Async Monitoring Contract

Use this when an orchestrating skill dispatches a **concurrent batch** of subagents via the `Agent` tool (a wave in `ywc-parallel-executor`, the 5-way Phase 1 fan-out or the 20-way Step 4.5 verifier fan-out in `ywc-impl-review`, or a bounded single Opus advisor dispatch). This contract exists because a concurrently-dispatched subagent's completion notification can arrive out of order or late — treating notification order or count alone as a proxy for completion has previously caused a completed subagent to be mistaken for still-pending.

This contract is not scoped to the consumers named above or to any closed list: it applies to **every batch of 2 or more concurrent `Agent` dispatches whose completion the same session then waits on**, regardless of which skill (or ad hoc, hand-constructed fan-out) initiated the batch. A skill author adding a new N-way parallel dispatch to a `SKILL.md` must cite this file at the dispatch point with an `Action required` callout that also carries the Release clause (see [Releasing Completed Named Agents](#releasing-completed-named-agents)) on the same physical line — `tests/named_agent_release_test.py` rejects a callout line without it. The consumer list in `claude-code/skills/CLAUDE.md` documents known citation sites; it is not the boundary of where this contract applies.

## Unique Dispatch Labeling

Every subagent dispatched as part of a concurrent batch must be given a name that deterministically maps back to what it was dispatched for — task name for `ywc-parallel-executor`, `<aspect>-<verifier-index>` for `ywc-impl-review`'s verifier fan-out. Never a generic or reused label across a batch.

## On Every Signal

Apply this sequence, in order, every time a signal arrives (a `<task-notification>`, or the user resuming the session):

1. Apply [Full-Roster Reconciliation](#full-roster-reconciliation).
2. Apply [Bounded Escalation on Stall](#bounded-escalation-on-stall).
3. If any dispatch is still unresolved, apply [Waiting for Completion](#waiting-for-completion) — end the turn; never arm a timer or a polling wakeup.
4. If the whole batch is resolved and its results are consumed, apply [Releasing Completed Named Agents](#releasing-completed-named-agents).

The sequence re-runs in full for the 2nd, 3rd, and every later signal a batch produces, not only the first — a dispatch that stalls midway through a batch must go through the same reconciliation and escalation check the next time a signal arrives.

## Full-Roster Reconciliation

Before treating a batch as complete, the orchestrator must reconcile the full expected roster (the set of names it dispatched) against the set of names it has received a terminal status for — via the orchestrating session's agent-roster-listing capability, where the runtime provides one, or otherwise the batch's own tracked state (a checklist of dispatched names ticked off as each terminal status arrives). Never infer completion from notification arrival order or count alone.

Reconciliation must be safe to invoke repeatedly against the same state: a duplicate terminal-status notification for an already-reconciled name is a no-op, never treated as a second batch member.

**When to re-query the roster.** The re-query is a fresh read of the session's agent roster (where the runtime provides a listing capability). A notification that already names the completing agent and reports a terminal status *is* the reconciliation for that one dispatch — a fresh query adds nothing, and repeating an identical query on every notification of a batch draining one dispatch at a time is the shape harness loop-detection flags as a loop.

| Situation | Re-query the roster? |
|---|---|
| Notification names the agent and reports a terminal status | No — the notification is already the reconciliation for that dispatch |
| Notification is ambiguous (no agent name, no terminal status, or its ordering against another near-simultaneous notification is unclear) | Yes |
| The batch reaches its expected completed count | Yes — one final query to confirm no dispatch was silently missed |
| Every single notification in a batch, regardless of content | No — this is the anti-pattern above, not extra safety |

This narrows *when a fresh query is required*, not the reconciliation duty itself: every outstanding dispatch stays tracked from its last known status, and the stall check in [Bounded Escalation on Stall](#bounded-escalation-on-stall) still runs on every signal against that tracked status.

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

**This check does not depend on whether the roster was re-queried on this signal.** On every signal, compare the dispatch time recorded for each outstanding dispatch (any dispatch whose last known status is not yet terminal) against the signal's wall-clock time — including dispatches no notification mentioned this turn. A dispatch that never sends its own notification is exactly the case this check exists for: other lanes' notifications keep arriving while one lane stays silent, and nothing else re-examines the silent lane's elapsed time.

If the hard escalation threshold is reached and full-roster reconciliation still shows one or more names without a terminal status, treat it as the batch-level equivalent of `BLOCKED` per [subagent-status-actions.md](./subagent-status-actions.md). Do not keep waiting indefinitely. Do not silently re-dispatch. Surface which named subagent(s) are unaccounted for.

## Releasing Completed Named Agents

A dispatch that carries a `name` (required above for any batch of 2+) is registered by the harness as an addressable teammate, not a fire-and-forget subagent. When its work ends it does **not** exit: it stays `idle` — running and addressable — until it is stopped or the session ends. This is intended harness behavior, not a stall and not something to escalate: the Bounded Escalation thresholds above apply only to `running` dispatches, and an `idle` named agent whose result was already delivered is finished work.

**Release step.** After the batch reaches its expected completed count (the final confirmation in [Full-Roster Reconciliation](#full-roster-reconciliation)) **and** every result has been consumed, call `TaskStop` once per named agent in that batch, passing its `name` as `task_id`. Do not release earlier: an agent whose result is not yet consumed must stay reachable.

- Release only agents from the current batch. Never stop an agent this session did not dispatch, and never stop one that is still `running`.
- A `TaskStop` failure on an agent that already exited is inconsequential (the goal is already met); do not retry or add a pre-check.
- Do not originate a `shutdown_request` for this: that protocol is a request the teammate may reject, and `TaskStop` by name is the documented direct stop for a named agent. Use `shutdown_request` only when the user asks for a graceful shutdown.
- If the session ends right after the batch, the release step may be skipped — team resources are cleaned up at session end.

Source: <https://code.claude.com/docs/en/agent-teams.md> (teammates stay running while idle; stopped by a shutdown request or `x` in in-process mode).

## Known Limitations

This contract mitigates but does not eliminate notification races: a subagent whose process exits without ever emitting a terminal status is indistinguishable from one that is merely slow, right up until a signal arrives and elapsed time is found to cross the hard escalation threshold. If no signal ever arrives, that comparison never runs at all — per `## Waiting for Completion`, the turn simply stays ended, so this is a detection gap, not just a delay: an exited-without-status subagent in a batch that otherwise goes fully silent can leave the batch permanently unescalated rather than merely slow to escalate.
