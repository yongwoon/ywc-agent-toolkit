# Advisor Pattern

> Shared reference document. Linked from any `ywc-*` skill that wants to use a bounded high-capability review step without running the whole workflow on the most expensive model.

## 1. Purpose

The Advisor Pattern combines a normal executor with a short, focused frontier-model consultation only at decision points where judgment materially changes the outcome.

Use it when a skill can do most work mechanically, but a small number of decisions are expensive to get wrong: security severity, architecture direction, task phase boundaries, or ambiguous specification conflicts.

## 2. Core Shape

```text
Phase 1: Executor
  - gathers evidence
  - applies deterministic rules
  - produces draft findings or a draft plan
  - marks only the ambiguous high-impact items

Phase 2: Advisor
  - receives only the marked item plus minimal evidence
  - decides severity, strategy, or correctness
  - returns a short verdict
```

The advisor input should contain only:

- the decision being asked
- the evidence collected by the executor
- the constraints that bound the decision

Do not forward whole repositories, full transcripts, or unrelated findings. This is a cost-and-focus rule, not a redaction control. If secrets or PII need removal, redact before Phase 1 sees them.

## 3. Advisor Output Size

An advisor verdict is short by contract. The observed ceiling is **typically under 500 words**: a confirmed severity or decision, a one-line rationale, and a "confirmed" or "adjusted" marker. A skill MAY set a tighter operational cap (for example 200 words) for its own dispatches.

If a genuinely complex candidate needs more room, a skill may invoke an override: exceed the cap and justify the overrun in the final report's budget section (see §6). The default expectation remains a terse verdict — large advisor returns saturate the orchestrator's context and defeat the bounded-payload contract.

## 4. Patterns

### Pattern A: Escalation Inside One Executor

Use when one long-running executor has one or two risky decision points.

- Run the workflow in one executor.
- At the named decision point, spawn one short advisor subagent.
- Continue only after incorporating the advisor verdict.

Suggested budget: 0-3 advisor calls.

### Pattern B: Two-Phase Review

Use when multiple reviewers can find mostly mechanical issues, with only some findings needing judgment.

- Phase 1: run reviewers in parallel.
- Aggregate candidate-for-advisor findings.
- Phase 2: send each candidate to a short advisor pass.
- Merge confirmed or adjusted findings into the final report.

Suggested budget: 0-5 advisor calls, capped by finding ambiguity rather than file count.

### Pattern C: Up-Front Planning Advisor

Use when the first decomposition decision shapes all later work.

- Run exactly one advisor pass at the start to produce or critique the plan.
- Execute the resulting plan with normal executors.
- Do not keep re-invoking the advisor unless the skill explicitly documents a new trigger.

Suggested budget: exactly 1 advisor call.

## 5. Escalation Criteria

An advisor escalation is allowed only when all three conditions are true:

1. Objective trigger: the executor can tell the condition applies without another judgment call.
2. Irreversibility: the wrong decision is expensive to undo.
3. Ambiguity: more than one reasonable interpretation of the evidence exists.

Good examples:

- a Critical or High security finding has indirect evidence
- a task phase boundary could cascade through many generated tasks
- a verification failure could be caused by the change or by unrelated shared state
- a spec clause is internally consistent but conflicts with linked architecture docs

Avoid escalating for style preferences, large files, vague uncertainty, or every security-related finding.

## 6. Reporting

The final report should state:

- which Advisor Pattern was used
- how many advisor calls were made
- which decisions were confirmed or adjusted
- any budget overrun and why it was necessary

## 7. Integration Checklist

- [ ] The skill names Pattern A, B, or C.
- [ ] The skill defines objective escalation triggers.
- [ ] Advisor input context is bounded to the decision.
- [ ] The skill documents an advisor-call budget.
- [ ] The final report distinguishes executor-only results from advisor-adjusted results.
