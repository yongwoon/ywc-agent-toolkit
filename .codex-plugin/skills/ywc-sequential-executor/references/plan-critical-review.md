# Plan Critical Review (Pattern C, range mode)

> Reference for the optional upfront plan review used by `ywc-sequential-executor` when running a range of tasks. Linked from the SKILL.md "Plan Critical Review" section.

## 1. Why This Exists

The standard Pre-flight checks the **environment** (clean working tree, gh auth, tasks directory present). It does not check the **plan**: missing tasks, contradictory specifications, ordering issues, or dependency-graph errors that only surface mid-range when a task fails for reasons unrelated to its own implementation.

A wrong plan is the most expensive failure mode in range mode, because the cost compounds: every subsequent task either inherits the broken assumption or has to be re-run after the plan is fixed. A 1-time upfront advisor call (Pattern C from [../../references/advisor-pattern.md](../../references/advisor-pattern.md)) is cheaper than the rework forced by a plan defect discovered at task 7 of 12.

This is the same shape `ywc-parallel-executor` already uses for its **Wave Planning Advisor** — a single upfront advisor call before worktree creation begins. Sequential adopts the same pattern for the same reason: the damage is expensive to undo once branches and commits exist.

## 2. When to Invoke

**Skip the review** for any of these:
- Single-task invocation (no range).
- Range size of **2 tasks or fewer**.
- Auto-detect mode (`$ywc-sequential-executor` with no specifier) when only one task is eligible.
- The plan was generated within the same session by `ywc-task-generator` followed immediately by this skill — the generator already validates dependency-graph correctness, and a re-review duplicates work.

**Invoke the review** when **all three** of the following hold:
1. Range size is **3 tasks or more**.
2. The plan was either (a) generated in a prior session, or (b) modified by hand since `ywc-task-generator` produced it.
3. At least one of:
   - Any task in the range has Spec Reference URLs marked for fetching.
   - The range crosses a Phase boundary (Phase X end + Phase Y begin).
   - First-pass dependency check shows any task with **3+ Depends On entries**.
   - Any task's `Stop Conditions` block is non-trivial (more than the boilerplate "verification fails after 2 attempts" pattern).

If the conditions are not met, skip the review silently and proceed to Task Resolution. Do not log "skipped" in the Completion Report; it is not a discrepancy.

## 3. How to Invoke

Spawn one higher-capability advisor subagent. Payload (≤200 lines total):

- **Dependency-graph excerpt** — task names + `Depends On` + `Conflicts With` + Phase numbers, in topological order. Do not forward full task READMEs.
- **First-and-last task summaries** — Goal + Ownership + Spec Reference Primary Sources (path-only) for the first task in the range and the last task in the range. Skip the middle tasks unless their Goal or Ownership is unusual.
- **Stop Condition collisions** — list any task in the range whose Stop Condition references another task in the range; otherwise omit.

Ask the advisor for three things:

1. **Plan correctness verdict** — is the dependency graph consistent (no cycle, no missing predecessor) and are the Spec Reference paths reachable?
2. **Order risk** — is there a task in the range that should run first based on shared types or schema dependencies the topological sort missed?
3. **Range cohesion** — does the range form a coherent unit, or should the user split it into two invocations (e.g., a Phase X batch followed by a Phase Y batch with a manual checkpoint)?

## 4. Budget

This counts as **one** of the 3 advisor calls in the skill's `advisor_budget`. It is upfront and one-shot — no mid-range escalation extends it. If the advisor returns "reconsider with refinements", report the refinements to the user and stop; do not auto-apply the refinements and do not start the range.

The Pattern A per-step budget of 3 still applies to the rest of the run; the Plan Critical Review consumes 1 of those 3 when it runs. If a range run hits the per-step budget after this review fires, that is a signal of plan-level fragility — surface it in the Completion Report as a `DONE_WITH_CONCERNS` even if all tasks completed.

## 5. Advisor Output Format (≤300 words)

The advisor returns a verdict in this shape:

```
PLAN VERDICT: <proceed | reconsider with refinements>

CORRECTNESS: <one line — graph consistent or specific defect named>
ORDER RISK: <one line — none, or specific reordering needed and why>
RANGE COHESION: <one line — coherent, or split recommendation with the boundary task>

[If "reconsider with refinements":]
REFINEMENTS:
1. <concrete change to the plan, named in terms the user can apply>
2. <next change>
```

The verdict must lead with `PLAN VERDICT:` on its own line so the orchestrator can dispatch on the value without parsing prose. Refinements must be actionable — "consider whether the order is right" is not a refinement; "swap task 000003-020 and 000003-030 because the latter creates the type the former imports" is.

## 6. What This Review Does Not Cover

- **Code-level review** — that is `ywc-impl-review`'s job, after implementation completes.
- **Spec quality** — that is `ywc-spec-validate`'s job, before tasks are generated.
- **Per-step decisions during execution** — those are Pattern A escalations, governed by [advisor-escalation.md](./advisor-escalation.md).

The Plan Critical Review only validates that the plan is coherent enough to start. It does not predict every failure that will happen during execution; it catches the failures that are visible from the plan alone.

## 7. Failure Modes to Avoid

| Anti-pattern | Why bad | Replace with |
|---|---|---|
| Forwarding full task READMEs to the advisor | Burns tokens; the dependency graph + Goal lines are sufficient | Send the structured payload defined in §3 |
| Auto-applying advisor refinements | The advisor cannot validate that its refinements match the user's intent | Surface refinements; let the user decide |
| Skipping the review for borderline cases ("only 3 tasks, probably fine") | The 3-task floor is the trigger, not the boundary; if invocation conditions hold, run it | Run the review when the conditions match, even if the range feels small |
| Running the review during auto-detect mode | Auto-detect picks one ready task, not a range; there is no plan to review | Skip silently in auto-detect mode |
