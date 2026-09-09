# Subagent Async Monitoring Contract

This reference is the shared authority for asynchronous subagent identity,
liveness, escalation, and quiescence. It applies to implementation workers,
sequential advisors, and read-only Phase 1 review workers. It defines how a
caller proves that a target is terminal; it does not redefine terminal status
meaning, task-state ownership, worktree ownership, or delivery policy.

Terminal status interpretation remains owned by
[`subagent-status-actions.md`](./subagent-status-actions.md). Consumers must
cite this document rather than copy its algorithm.

## 1. Identity and dispatch capture

Before dispatch, retain the caller's source label for task state, worktree,
report, and delivery operations. After a successful `spawn_agent` response,
accept a returned canonical `task_name` only when it is present, parseable, and
attributable to that dispatch. Record the mapping:

```text
source task name -> returned canonical task_name
```

Use the returned canonical target for `list_agents`, `wait_agent`,
`send_message`, and `interrupt_agent`. Never invent a target from an agent ID,
requested label, array position, or a missing response. A successful spawn with
no usable canonical target is outside the active roster and follows the
caller's existing failed-dispatch path.

## 2. Event-first, full-roster reconciliation

The monitor is event-first but roster-complete:

1. Process every delivered, attributable, parseable terminal payload before
   consulting roster state.
2. Reconcile every outstanding canonical target with the complete
   `list_agents` result, not only targets named in the latest notification.
3. Treat `wait_agent` wakeups, timeouts, and user steering as reconciliation
   points.
4. Keep monitoring while any target lacks attributable terminal evidence.
5. A missing roster entry is not terminal evidence and never proves `DONE`.

An attributable terminal payload wins when it arrives during escalation. A late
terminal payload after a preserved failure is retained as recovery evidence and
does not silently reverse the source-task transition.

## 3. Bounded heartbeat and escalation

Heartbeats are no longer than 60 seconds. Every target receives at most one
status request and one interrupt during escalation. There is no automatic
redispatch.

### Implementation and review workers

At 600 seconds after successful dispatch, if no attributable terminal payload
exists:

1. send one status request to the returned canonical target;
2. at the next heartbeat of no more than 60 seconds, interrupt only if the
   target is still non-terminal;
3. wait and perform one final reconciliation for no more than 60 seconds.

Only a proven-quiescent target may enter the existing preserved-failure path.
If the target may still be live, the caller must block cleanup, next-wave
dispatch, normal report or review aggregation, Completion Report, and `DONE`.

### Sequential advisors

At 300 seconds after successful advisor dispatch, apply the same bounded
request/heartbeat-interrupt/final-reconciliation sequence. The caller consumes
one existing advisor slot and applies its owner-specific unavailable fallback;
this sequence never creates a fourth advisor call or changes task-state or
worktree ownership.

## 4. Quiescence and API failure

`unavailable` means the bounded sequence ended without attributable terminal
evidence and with sufficient evidence that the target is quiescent. It is not a
success result. The caller must surface the lane/target, elapsed time, roster
state, and raw-evidence category and apply the consumer's degraded outcome.

If a monitoring API call fails, process already delivered events, retain raw
evidence, and interrupt each known live target at most once. Do not claim
quiescence from an incomplete roster or a notification timeout. If quiescence
cannot be proved, classify the target as possibly live and block lifecycle
actions until a later attributable terminal event or a verified quiescent state
is available.

## 5. Consumer boundaries

- `ywc-parallel-executor` retains source task names for state/worktree/report
  operations and uses returned targets only for collaboration operations.
- `ywc-sequential-executor` retains its three-call advisor budget and named
  fallback ownership.
- `ywc-impl-review` treats Phase 1 reviewer output as read-only inline evidence
  and applies possibly-live blocking before quiescent-unavailable concerns,
  then normal aggregation.

None of these consumers may introduce CLI polling, persisted resume state, or
new terminal-status semantics through this reference.

## 6. Scenario matrix

| Scenario | Required outcome |
|---|---|
| Usable canonical target returned | Record source-to-target mapping and monitor returned target. |
| Missing or malformed canonical target | Exclude from active roster; use existing failed-dispatch handling. |
| Terminal event before reconciliation | Process event first; do not preserve failure. |
| Missing roster entry | Keep non-terminal; never infer `DONE`. |
| Silent implementation/review worker at 600 seconds | One request, one conditional interrupt, one final reconciliation. |
| Silent advisor at 300 seconds | Same bounded sequence; consume existing slot and use named fallback. |
| Target finishes during escalation | Attributable parseable terminal payload wins. |
| Target remains possibly live | Block cleanup, next wave, ordinary report/aggregation, Completion Report, and `DONE`. |
| Quiescent target without terminal payload | Surface `unavailable` with evidence; consumer may return concerns, not success. |
| Monitoring API failure | Retain raw evidence; interrupt known live targets once; block if quiescence is unproved. |
| Late terminal evidence after preserved failure | Retain recovery evidence; do not reverse source-task state silently. |
| All review lanes answer cleanly | Continue existing Phase 2 selection, confidence gate, and report flow. |

The affected consumer evals are the executable regression surface for these
scenarios. Any consumer-specific status mapping belongs in that consumer and
in the terminal-status authority, not here.
