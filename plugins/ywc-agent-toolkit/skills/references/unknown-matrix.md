# Unknown Matrix

> Shared reference document. Linked from discovery and planning skills that need
> to surface blind spots before requirements harden into implementation work.

## Purpose

Use this reference when the request is broad enough that the dangerous failure
mode is not a missing answer, but a missing question.

The matrix exists to expose hidden uncertainty early without loosening evidence,
scope, or safety discipline. It is a discovery aid, not a license to invent.

## The Four Quadrants

| Quadrant | Operational meaning | Typical action |
|---|---|---|
| **Known Knowns** | Requirements, constraints, and precedents already verified from the repo or the spec | State them explicitly so downstream skills do not re-decide them |
| **Known Unknowns** | Missing decisions you already know you need | Ask the smallest blocking question or route to the right discovery skill |
| **Unknown Knowns** | Assumptions so familiar that nobody wrote them down | Surface them as candidate assumptions and verify them against code, docs, or the user |
| **Unknown Unknowns** | Risk areas not considered at all yet | Run a brief blind-spot pass to identify what else could change the plan |

## When to Use

Use the matrix when any of these apply:

- The user has a strong preference, but the repo evidence for that preference is weak
- The request could be satisfied several ways and the trade-off is not yet grounded
- The codebase investigation surfaced adjacent constraints, but not enough to form a direct implementation question
- A recommendation or plan feels "obvious" too early

Do not use it when:

- The next step is already blocked by a concrete missing decision that should become `NEEDS_CONTEXT`
- The repo or spec already answers the question
- The task is in execution mode and the remaining uncertainty is local implementation detail only

## Prompt Pattern

Use a short pass, not a long essay:

```text
Before locking the plan, surface:
1. Known knowns — what is already verified
2. Known unknowns — what still needs a decision
3. Unknown knowns — what we may be assuming without saying
4. Unknown unknowns — what we may not have considered at all

Keep the list operational. Prefer repository evidence over memory.
Turn implementation-blocking ambiguity into direct questions.
```

## Guardrails

- Verified repository or specification evidence outranks intuition.
- A surfaced unknown is not automatically a blocker.
- If an unknown would change implementation shape, interface shape, ownership, or dependency order, escalate it explicitly.
- If an unknown is interesting but not decision-shaping, record it as a note instead of reopening scope.
- Do not expand the matrix into a brainstorming exercise once the right next question is already known.

## Output Discipline

Good output is short and concrete:

- 2–5 verified known knowns
- 1–3 real known unknowns
- 1–2 candidate hidden assumptions worth checking
- 0–2 blind spots that could materially alter the plan

If nothing new is surfaced, say so and continue. The goal is better question
selection, not mandatory uncertainty theater.
