# Question-First Gate

> Shared reference document. Linked from any `ywc-*` skill that performs implementation, generation, or review work where silent guessing would compound across subsequent steps.

## 1. Purpose

The cheapest defect to fix is the one that never makes it into code. The Question-First Gate exists to surface ambiguity **before** the implementer commits to a direction. A 30-second clarification round costs orders of magnitude less than a re-implementation forced by a wrong assumption.

This gate complements [confidence-gate.md](./confidence-gate.md) (which evaluates output quality) and the Advisor Pattern (which escalates expensive decisions). Question-First runs **earliest** — before any code is written.

## 2. The Gate

Before any code-producing step (Step 3 of `ywc-sequential-executor`, Phase 1 of `ywc-code-gen`, Step 4b of `ywc-parallel-executor`, or any subagent dispatch that writes code), the executor or subagent must do exactly two things:

1. **Read the spec and the immediate context** — task spec, Spec Reference Primary Sources, the files inside the declared Ownership.
2. **Enumerate genuinely ambiguous decisions** — decisions whose wrong answer would force a rewrite, not stylistic choices that can be flipped later.

If the enumeration is empty, proceed. If non-empty, **stop and return `NEEDS_CONTEXT`** with the questions listed.

## 3. What Counts as a Genuine Ambiguity

| Genuine ambiguity (must ask) | Stylistic choice (do not ask) |
|---|---|
| Public interface shape (function signature, return type, error model) | Local variable name |
| Data model field that other tasks will read | Internal helper structure |
| Naming that already exists elsewhere in the repo | Comment style |
| Library or framework choice (when more than one is installed) | Lint-fixable formatting |
| Behavior under a documented edge case the spec did not cover | Whether to inline a one-liner |
| Auth/permission boundary (who is allowed to call this) | Test file split granularity |

**Heuristic**: if you can answer the question by reading a file in the repo, do so first. Question-First is for ambiguity that is not resolved by reading.

## 4. Anti-Patterns

These are common ways the gate fails to do its job. The skill must avoid each.

| Anti-pattern | Why bad | Replace with |
|---|---|---|
| "Inferring from neighboring tasks" | Compounds error across the sequence; if the neighbor was wrong, every subsequent task is wrong | Stop and ask — the neighbor's choice may not have been validated either |
| Asking for stylistic preferences | Wastes the user's time; the answer changes nothing of substance | Decide locally and proceed |
| Bundling 10 questions into one round | Overwhelms the user and dilutes signal | Ask only the questions whose answers would change the implementation; defer the rest |
| Asking after writing code | Defeats the purpose of the gate; the cost is already sunk | Ask before any commit, even before the first file write |
| Skipping the gate "because the task seems clear" | The most expensive failures are the ones that looked clear and were not | Run the enumeration step every time; an empty list is a fine answer |

## 5. Question Format

When returning `NEEDS_CONTEXT`, structure the questions so the user can answer with minimal back-and-forth:

```
NEEDS_CONTEXT

Before implementation, the following decisions need clarification:

1. <decision point in one phrase>
   Options seen in repo / spec:
     a) <option A> — <where it appears>
     b) <option B> — <where it appears>
   Why this matters: <consequence of getting it wrong>

2. <next decision point>
   ...
```

Do not bury questions inside prose. Do not ask open-ended questions ("how should this work?"). Each question must offer the alternatives the executor already considered, so the user is approving a choice rather than designing from scratch.

## 6. When the Gate Does Not Apply

The gate is for code-producing or design-producing steps. It does **not** apply to:

- Read-only review skills (`ywc-impl-review`, `ywc-security-audit`) — these report findings, not designs.
- Mechanical bookkeeping steps (moving a task to `completed/`, creating a feature branch).
- Verification steps (running tests, lint, build).

For those steps, follow [principles.md](./principles.md) §6 (Failure Discipline) instead.

## 7. Cost of the Gate

The gate adds one round-trip in the worst case. It removes one rewrite cycle when it triggers. The break-even point is well below 1 — if even 5% of tasks would have hit a rewrite without the gate, the gate pays for itself across the rest.

The gate is therefore a default-on discipline, not an opt-in feature. Skipping it is the exception that requires justification, not the other way around.
