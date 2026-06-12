# Advisor Escalation Policy (Pattern A)

> Referenced from: SKILL.md → Execution Cycle → Advisor Escalation Policy
> Related: [advisor-pattern.md](../../references/advisor-pattern.md) — the shared advisor pattern reference shared across all ywc-* skills
> Read this when: encountering one of the five escalation conditions below during the Execution Cycle, OR planning the budget for an upcoming range invocation.

## Pattern overview

This skill runs the full Execution Cycle on a single inherited-model executor. For a small number of **decision points** where a wrong judgment is expensive to undo, the executor may request one higher-capability advisor pass using the Codex delegation mechanism available in the current session. If no delegation tool is available, run the same advisor checklist inline and record the fallback. This follows **Pattern A** from the shared advisor-pattern reference — escalation inside a single subagent, with frontier judgment applied only where it actually matters.

The goal is **not** to use high-capability reasoning for everything. The goal is to reserve advisor reasoning for the few decisions where:
- the cost of being wrong is high (irreversibility),
- the right answer is genuinely ambiguous (not just unfamiliar), and
- the trigger is objective enough that the executor can recognize the situation without already knowing the answer.

## Budget

Up to **3 advisor escalations per invocation** (applies to single-task and range execution alike). Unused budget is good. Exceeding the budget requires an explicit justification in the Completion Report.

## Escalation conditions

Each must satisfy all three properties from `advisor-pattern.md` §5 (objective trigger, irreversibility, ambiguity):

### 1. Spec Reference conflict (Step 1b)

`task.md` and the linked Primary Source disagree on a specific requirement, and both readings would produce valid-looking code. The advisor chooses which reading wins and provides a one-line rationale.

**Why escalate**: implementing the wrong reading produces code that compiles, passes tests, and ships — but is semantically wrong against the spec. Detecting this later requires a human spec review and a rewrite.

### 2. Verification first failure with unclear cause (Step 4)

The full project test suite fails in a module **outside** the task's declared Ownership, and it is not obvious whether the task caused the regression (shared state, shared types, runtime wiring) or whether the test was already flaky. Escalate **before the second fix attempt** so the attempt targets the right layer.

**Why escalate**: blindly fixing the wrong layer (test vs. implementation, shared vs. local) burns the 2-attempt fix budget and triggers a stop without progress.

### 3. Merge conflict strategy (Step 6a, `--local-merge` mode)

`git merge` reports a non-trivial conflict in a file the task did not directly modify. The advisor suggests a resolution strategy before any edits happen. Do **not** auto-resolve.

**Why escalate**: auto-resolving a conflict in code the task does not own can silently overwrite another contributor's change. The advisor's verdict gives a defensible reason for the resolution choice.

### 4. CI first failure with ambiguous category (Step 6, normal mode)

CI fails and the failure category is not obviously "my code": infrastructure, environment variables, timing, and flake are all plausible. The advisor helps classify before the fix attempt.

**Why escalate**: spending fix attempts on a CI infrastructure issue (which the executor cannot fix) wastes budget and frustrates the user. Classification first, fix second.

### 5. Stop Condition borderline (Step 3)

A `task.md` Stop Condition is borderline, and proceeding would lock in a choice that is expensive to undo (wrong table schema, wrong API contract, published PR). The advisor confirms whether to halt or continue.

**Why escalate**: Stop Conditions exist precisely to prevent expensive irreversible mistakes. A borderline Stop Condition is the highest-leverage place to apply frontier judgment.

## Context payload rules (critical for cost discipline)

Pattern A's cost savings come from keeping the advisor payload small. If you forward the entire task state, you have effectively replaced your inherited-model executor with an advisor executor — defeating the entire pattern.

- **Forward only the decision point**: the specific Step, the evidence (failing test output, diff excerpt, spec excerpt), and the binding constraint. Target ≤100 lines of payload.
- **Do NOT forward**: the full task README, the full spec, the full repository state, or prior Execution Cycle turns.
- **Advisor returns a short verdict** (≤200 words) containing the recommended action and a one-line rationale. The advisor pass does not run tools; the parent executor continues with the advice.

## Explicit non-goals

Do **not** escalate for these — they fail at least one of the three required properties:

| Anti-pattern | Why it fails |
|---|---|
| General uncertainty or "gut feel" | No objective trigger |
| Every verification failure | Only the first ambiguous one passes the ambiguity gate |
| Routine merge conflicts in declared Ownership | Reversible — the executor can resolve without expensive consequences |
| Stylistic decisions, commit message wording, PR title phrasing | Reversible and low-stakes |
| Pausing to confirm Non-Stop Execution Principle compliance | Escalation is part of the current task's cycle, not a between-task pause |

## Reporting

Report escalations at the end: the Completion Report must note which Steps triggered advisor calls and what each verdict recommended, so the user can audit the decision trail. This audit log is the basis for refining the escalation conditions over time.
