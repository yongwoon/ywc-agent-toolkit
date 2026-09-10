# Quality Gate Steps — Sequential Executor

> **Action required**: Read [../../references/quality-gates.md]. This document describes the operational workflow for Cleaner and Hardener dispatch within the executor; the canonical contract, thresholds, roles, and state vocabulary are defined in the shared reference above.

## Ordering and Dispatch Flow

Quality gates run in strict order after implementation (Step 3) completes:

1. **Step 3.5: Cleaner (CRAP gate)** — Dispatched first, independently of Hardener. Attempts complexity reduction when diff-measured CRAP exceeds the task's threshold (default ≤ 8). Returns `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED`.

2. **Step 3.6: Hardener (Mutation gate)** — Dispatched only if Cleaner does not return a blocking result. Attempts to raise mutation score when surviving mutants remain after Cleaner passes. Runs up to three approved attempts per task.

If Cleaner returns `BLOCKED` (enforced contract mode), skip Step 3.6 entirely and route to verification failure; do not dispatch Hardener.

## Mutation Loop Cap and Survivor Forwarding

Hardener may make at most three approved attempts per task or execution wave. After the third attempt:

- **Incomplete mutation coverage**: Report every residual survivor — a mutant not killed by the test suite — with its bounded evidence reference.
- **Forward to Implementation Review**: All survivors from round 3 forward unchanged to Step 4.5 (Implementation Review), never silently drop them. The reviewer, not the executor or Hardener, decides whether survivors are acceptable.
- **No claim of success on survivors**: A third-round attempt with survivors remaining is still evidence of incomplete mutation coverage. The task records `gate_state: "fail — severity <advisory|enforced>"` even if all three attempts completed successfully.

Surviving mutants after round 3 are raised as concerns in the final Completion Report; the reviewer has full context to distinguish a true equivalent mutant from one representing incomplete test coverage.

## Dispatch-Failure Handling

If a dispatch to `ywc-refactor-cleaner` (Step 3.5) or `ywc-qa-engineer` (Step 3.6) fails before the worker can attempt the gate:

- **Status routing**: Route to `DONE_WITH_CONCERNS`, never `BLOCKED`. The gate did not block the task, but the failed dispatch is recorded as evidence of a system-level constraint.
- **gate_state record**: Set `gate_state: "not run — dispatch failed"` in the task's completion record.
- **Proceed to Step 4**: Continue verification and delivery normally. The failed dispatch is a concern for the Completion Report, not a step blocker.

## Rationalization Defense

When tempted to skip a gate or redefine its scope, check this table first:

| Excuse | Reality |
|---|---|
| "CRAP gate says a function is logically one unit" | Decomposition or a registered exclusion-list entry are the only two paths past the gate. A "logical unit" that exceeds the complexity threshold is a hidden risk; the gate exists precisely because naming a unit "logical" does not prove it is testable or maintainable. |
| "Mutation gate says the test suite is incomplete, but we ran all the tests we wrote" | "All the tests we wrote" is not the same as "all the tests this code needs." Hardener discovers surviving mutants that your test suite missed. Kill them or escalate the survivors as a concern. |
| "Cleaner says refactoring is needed, but I wrote the simplest code possible" | Simplest-possible code and low-complexity code are not the same thing. Code can be simple in intent but complex in control flow (nested conditions, nested loops, exception paths). Simplify the control flow or argue for an exclusion. |
| "We'll skip the gate for this task and add it to the next one" | Quality gates are not deferrals. Deferring a gate leaves the current task's risk unaddressed. If a gate blocks, resolve it in the current task or escalate to human review — do not postpone. |
| "Hardener's 3-round limit is arbitrary; we should run more attempts" | The 3-round cap is not arbitrary — it prevents infinite mutation-chasing and enforces escalation to human review. After round 3, survivors become a concern for the reviewer, not a signal to keep trying. |

## Contract-Absent Fallback

When a task or plan declares no quality gate contract (the sentinel `N/A — no quality gate contract` in its spec), Steps 3.5 and 3.6 are skipped entirely and the task proceeds directly from Step 3 implementation to Step 4 verification. No dispatch, no tool invocation, no evidence gathering — a clean no-op. The absence of a contract is a legitimate choice, not a failure.
