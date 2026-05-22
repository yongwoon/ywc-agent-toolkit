---
name: ywc-confidence-gate
description: >-
  (ywc) Use before starting any non-trivial implementation, before invoking
  ywc-code-gen / ywc-sequential-executor / ywc-parallel-executor, or before
  committing to a design path with material rework cost. Scores readiness
  across five dimensions (scope clarity, architecture compliance, evidence
  quality, reuse verified, root cause identified) and gates the decision
  with PROCEED (≥90) / REVIEW (70–89) / STOP (<70). Triggers: "confidence
  check", "confidence gate", "ready to implement", "should I proceed",
  "is this ready", "준비 됐어", "구현 시작해도 돼", "confidence 점검",
  "착수 준비", "実装着手", "実装に進んで良いか", "確信度チェック",
  "ywc-confidence-gate". Do not use for completion verification (use
  ywc-verify-done — that gates the claim, this gates the start), spec
  quality review (use ywc-spec-validate), implementation review (use
  ywc-impl-review — that scores findings, this scores readiness), or
  brainstorming intent (use ywc-brainstorm).
category: discipline
phase: pre-implementation
requires: []
---

# ywc-confidence-gate

**Announce at start:** "I'm using the ywc-confidence-gate skill to score readiness across five dimensions before implementation begins."

This skill is the canonical pre-implementation gate. It exists because every implementation skill (`ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`) starts producing code immediately when invoked — and the cost of code produced from a half-understood spec is borne later by `ywc-impl-review`, CI, or production. A 5-minute confidence score catches the same defect classes that a 30-minute re-plan and a 2-hour debug session would catch — at a fraction of the cost.

The scoring rubric and band definitions are shared with `ywc-impl-review` and other downstream skills via [`../references/confidence-gate.md`](../references/confidence-gate.md). This skill does not redefine the rubric; it applies it at the pre-implementation entry point.

## The Iron Law

```text
NO IMPLEMENTATION WITHOUT AN EXPLICIT CONFIDENCE SCORE AND BAND DECISION
```

If the aggregate score is below 90 and the band is REVIEW or STOP, implementation does **not** begin until the weakest dimension has been raised (or the user has explicitly accepted the residual risk and the agent has surfaced what cannot be raised). "I'll figure it out as I go" is not a band decision — it is the failure mode this skill exists to prevent.

## Rationalization Defense

When tempted to skip the gate, check this table first:

| Excuse | Reality |
|---|---|
| "The user already approved the spec, that means PROCEED" | Spec approval is one signal among five (Scope clarity). Architecture compliance, evidence quality, reuse, and root cause are independent — a spec can be perfectly clear and still rest on an unverified architectural assumption. Score all five before deciding. |
| "I have high confidence overall — skipping the per-dimension scoring is fine" | "Overall" confidence is the failure mode. The point of the rubric is to surface the **weakest** dimension; aggregate-only scoring lets a strong dimension (e.g., scope clarity 95) mask a fatal weakness elsewhere (e.g., reuse verified 40 because no one searched the existing utils). The single-dim-below-50 rule is what catches these. |
| "Scoring is bureaucracy when the change is small" | A 5-minute gate on a 5-line change is fast. A 2-hour debug session on the same 5-line change because no one checked if a utility already exists is slow. The gate scales **down** for small changes (most dimensions score 95+ trivially), but it must still be executed and surfaced. |
| "I'll score after to validate that proceeding was right" | Scoring after the fact is rationalization, not evidence. The point is to score before the decision so the score *informs* it. Post-hoc scores always conveniently clear the threshold. |
| "Evidence quality dimension is hard to score precisely — I'll round up" | "Round up to clear the threshold" is the most common gate-defeating move. A dimension at 65 is REVIEW; rounding to 70 to PROCEED is a documented anti-pattern in the shared rubric (§7). Score honestly; if the band is REVIEW, present alternatives — that is the correct outcome. |
| "REVIEW band wastes time on questions the user already has answers to" | REVIEW band exists precisely to surface those answers explicitly so they bind the implementation. If the user has them in their head but they are not in the spec, the implementation will diverge. Present the 1–3 alternatives or open questions; the user clears them in seconds. |
| "STOP band is for catastrophic situations only" | STOP fires whenever aggregate < 70 *or* any required dimension < 70. It is not catastrophic — it is "the current evidence does not support starting; raise it first". Treat STOP as "go back to spec / research / context", not as "abandon project". |
| "If I report a sub-90 band, the user will think I'm being slow" | The opposite. Reporting a REVIEW band with the weakest dimension named saves the user the rework cycle they would otherwise pay for. The gate is a transparency mechanism — the alternative is opaque overconfidence that surfaces as broken CI hours later. |
| "I can skip the gate when running from inside another skill (e.g., ywc-agentic loop)" | Skill-to-skill delegation is the **most** dangerous entry point — the upstream context narrows what is in scope, and the downstream skill may not see the spec the user actually wrote. Always re-score at the boundary; do not inherit confidence from an upstream caller. |
| "The five dimensions don't apply to my type of work" | They are deliberately abstract so they apply across feature work, bug fixes, refactors, and infra. If a dimension feels not-applicable, score it generously (90+) — but score it. Removing a dimension defeats the comparability of scores across skills, which is the rubric's primary value. |

**Violating the letter of this discipline is violating the spirit.** The rubric is shared with downstream skills precisely so that scores remain comparable — a score from this skill must mean the same thing as a score from `ywc-impl-review`.

## The Five Dimensions

> Read [`../references/confidence-gate.md`](../references/confidence-gate.md) for the canonical rubric definition. The summary below is for quick reference; the reference file is the authoritative source.

| # | Dimension | Weight | One-sentence test |
|---|---|---|---|
| 1 | Scope clarity | 25% | "Can I state in one sentence what is in scope and one sentence what is out — without using vague terms like 'related cleanup' or 'and other improvements'?" |
| 2 | Architecture compliance | 25% | "Does the planned change follow existing structure / naming / abstractions, or am I introducing a new pattern? If new, was it discussed?" |
| 3 | Evidence quality | 20% | "Are the claims I am about to act on backed by primary sources (current file content, official docs, test output) or by inference / memory?" |
| 4 | Reuse verified | 15% | "Have I searched the codebase / package registry for existing utilities that solve this? Listed them and ruled each out with a reason?" |
| 5 | Root cause identified | 15% | "For a bug fix, do I name the underlying cause (not the symptom)? For greenfield work, do I name the underlying user need (not the surface request)?" |

Score each dimension 0–100. Aggregate is the weighted sum, rounded to the nearest integer.

## The Decision Bands

| Band | Aggregate score | Per-dim override | Action |
|---|---|---|---|
| **PROCEED** | ≥ 90 | All ≥ 50 | Begin implementation. Report the score in the completion summary or the executor's per-step report. |
| **REVIEW** | 70–89 | None < 50 | Present 1–3 alternatives or open questions before proceeding. Trigger the [Advisor Pattern](../references/advisor-pattern.md) for any dimension < 70. Do not begin implementation until at least the weakest dimension is raised or explicitly accepted. |
| **STOP** | < 70 | Any < 50 (forces this band even if aggregate ≥ 70) | Do not begin implementation. Report which dimensions are weak and what evidence would raise them. Hand back to `ywc-plan` (architecture / scope), `ywc-spec-validate` (evidence), `ywc-tech-research` (reuse), or `ywc-brainstorm` (root cause / user need). |

**Single-dim ≤ 50 rule**: even if aggregate would clear the threshold, a single dimension scoring at or below 50 drops the band by one level (PROCEED → REVIEW, REVIEW → STOP). This prevents one strong dimension from masking a fatal weakness.

## Workflow

### Step 1: Establish the work item

State in one sentence what is about to be implemented. If the sentence requires three or more clauses, the work item is too large — split it via `ywc-task-generator` before continuing.

### Step 2: Score each dimension explicitly

For each of the five dimensions, do **all** of the following:

1. Read the one-sentence test (above).
2. State the evidence supporting the current score in 1–2 lines — file paths, command outputs, doc references, or the absence of those.
3. Score 0–100. Be honest; rounding up is the defeating move.

Use [`references/pre-implementation-checklist.md`](references/pre-implementation-checklist.md) for the per-dimension probe questions.

### Step 3: Compute the aggregate

```text
aggregate = (scope × 0.25)
          + (architecture × 0.25)
          + (evidence × 0.20)
          + (reuse × 0.15)
          + (root_cause × 0.15)
```

Round to the nearest integer.

### Step 4: Apply the single-dim override

If any dimension scored ≤ 50, drop the band by one level. PROCEED becomes REVIEW; REVIEW becomes STOP.

### Step 5: Surface the report

Print the report in the canonical format below (this is the same shape `ywc-impl-review` uses for post-implementation confidence — by design, so scores stay comparable).

### Step 6: Act on the band

- **PROCEED**: invoke the implementation skill (`ywc-code-gen`, `ywc-sequential-executor`, etc.) immediately. Carry the score into the executor's per-step report.
- **REVIEW**: present 1–3 alternatives or open questions; wait for user response or trigger the Advisor Pattern for the weakest dimension. Do not begin implementation in this turn.
- **STOP**: surface the failing dimensions and route back to the appropriate upstream skill (see §Decision Bands above). Do not begin implementation.

## Output Format

```text
Confidence Gate Report
──────────────────────
Aggregate: <NN>/100 — <PROCEED | REVIEW | STOP>

  Scope clarity:           <NN>   <one-line evidence>
  Architecture compliance: <NN>   <one-line evidence>
  Evidence quality:        <NN>   <one-line evidence>
  Reuse verified:          <NN>   <one-line evidence>
  Root cause identified:   <NN>   <one-line evidence>

<If REVIEW or STOP:>
Weakest dimension: <name> (<NN>)
Why: <one or two sentences explaining what is missing>
What would raise it: <concrete evidence or action — file to read, command to run, question to ask>

<If REVIEW:>
Alternatives presented for user decision:
  A. <option> — trade-off
  B. <option> — trade-off
  (C. <option> — trade-off)

<If STOP:>
Routing: <ywc-plan | ywc-spec-validate | ywc-tech-research | ywc-brainstorm> — <why>
```

The "Weakest dimension" and "What would raise it" lines are **mandatory** whenever the band is REVIEW or STOP. They are the mechanism that turns the gate from a roadblock into a step-by-step path forward.

## Integration

- **Upstream callers**: user invocation; `ywc-plan` (after Scale assessment, before downstream handoff); `ywc-code-gen` (Step 0, before Reuse Gate); `ywc-sequential-executor` / `ywc-parallel-executor` (before per-task implementation begins, especially for tasks with no upstream `ywc-plan` evidence); `ywc-agentic` (per-iteration entry).
- **Downstream**: implementation skills proceed on PROCEED; user dialog or Advisor Pattern on REVIEW; `ywc-plan` / `ywc-spec-validate` / `ywc-tech-research` / `ywc-brainstorm` on STOP.
- **Pairs with**: `ywc-verify-done` (the symmetric **post**-implementation gate — that gates the claim, this gates the start); `ywc-impl-review` (uses the same rubric for post-review confidence — scores remain comparable across the two gates).

## Validation Checklist

Before reporting a PROCEED band and beginning implementation, verify:

- [ ] All five dimensions have explicit numeric scores (not "high", not "OK")
- [ ] Each dimension has a one-line evidence statement
- [ ] No dimension scored at or below 50
- [ ] Aggregate was computed with the rubric weights (25/25/20/15/15)
- [ ] The single-dim override was applied if any score ≤ 50
- [ ] The score and band are surfaced in the response **before** any implementation tool is invoked
- [ ] If REVIEW or STOP, no implementation skill was invoked in the same turn

## Common Mistakes

(Procedural failure modes specific to this skill. Behavioral rationalizations are in the table above — do not duplicate here.)

- **Scoring after the implementation already started in the same turn.** The report must appear before the first implementation tool call. Scoring after invokes the gate retroactively — at which point its primary value (preventing the call) is gone.
- **Reporting only the aggregate, not the per-dimension breakdown.** A single number hides the weakest dimension; that is exactly the information the user needs to act. Always print all five dimension scores.
- **Carrying an upstream skill's confidence forward instead of re-scoring.** Each skill boundary re-narrows the context. A PROCEED at `ywc-plan` does not automatically transfer to `ywc-code-gen`, because the code-gen step has its own dimensions to score (especially Reuse verified and Architecture compliance, which `ywc-plan` does not score as deeply).
- **Treating REVIEW as a soft STOP.** REVIEW is "proceed with explicit alternatives presented and one of them chosen". STOP is "do not proceed". Conflating them collapses three bands into two and defeats the rubric's resolution.
- **Adding a sixth dimension because "my work has a unique aspect".** The five dimensions are fixed across skills so scores remain comparable. Per-skill adjustments belong in the "required dimensions" profile (see `references/confidence-gate.md` §4), not in extra dimensions.

## References

| Reference | Use when |
|---|---|
| [../references/confidence-gate.md](../references/confidence-gate.md) | Authoritative rubric definition; per-skill required-dimension profiles; status mapping; anti-patterns |
| [references/pre-implementation-checklist.md](references/pre-implementation-checklist.md) | Per-dimension probe questions specific to the pre-implementation moment (this skill's distinct usage from the post-review usage in `ywc-impl-review`) |
| [../references/advisor-pattern.md](../references/advisor-pattern.md) | Escalating a weak dimension to Opus for a second opinion before changing the band |
| [../ywc-verify-done/SKILL.md](../ywc-verify-done/SKILL.md) | The symmetric post-implementation gate; both gates use the same rubric so the start-of-work and end-of-work scores are directly comparable |
