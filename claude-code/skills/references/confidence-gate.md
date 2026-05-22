# Confidence Gate for Claude Code Skills

> Shared reference document. Linked from any `ywc-*` skill that needs an objective, score-based decision boundary between "proceed", "present alternatives", and "stop and gather information".

## 1. Purpose

This document defines the **Confidence Gate** — a five-dimension scoring rubric that any `ywc-*` skill can use to convert a fuzzy judgment ("does this look ready?") into a numeric threshold ("is the aggregate confidence ≥ 80%?").

The gate exists to make three things explicit:

- **Why** a skill chose to proceed, escalate, or stop.
- **Which dimension** was weakest, so the user knows what to address next.
- **Where the threshold sits**, so different skills do not silently disagree about what "good enough" means.

This complements the [Advisor Pattern](./advisor-pattern.md): the Advisor Pattern decides *how* to escalate to Opus when judgment is needed; the Confidence Gate decides *whether* to escalate at all.

## 2. The Five Dimensions

The gate uses five weighted dimensions. Weights are fixed across skills so that scores from different skills remain comparable.

| # | Dimension | Weight | What it measures |
|---|-----------|--------|------------------|
| 1 | Scope clarity | 25% | The work to be done is bounded and unambiguous. No undefined terms, no "and other improvements". |
| 2 | Architecture compliance | 25% | The proposed change is consistent with existing structure, naming, and abstractions. No accidental new patterns. |
| 3 | Evidence quality | 20% | Claims are backed by primary sources (code, official docs, test output) rather than inference or memory. |
| 4 | Reuse verified | 15% | Existing utilities, libraries, and patterns have been searched. Nothing is being reimplemented unnecessarily. |
| 5 | Root cause identified | 15% | For diagnostic work, the underlying cause is named — not just the symptom. For greenfield work, the underlying user need is named — not just the surface request. |

Each dimension is scored from 0 to 100. The aggregate confidence is the weighted sum, rounded to the nearest integer.

## 3. Decision Bands

The aggregate score maps to one of three bands. Each band has a prescribed action.

| Band | Score | Action |
|------|-------|--------|
| **PROCEED** | ≥ 90 | Execute as planned. No advisor escalation required. Report the score in the completion summary. |
| **REVIEW** | 70 – 89 | Present 1-3 alternatives or open questions to the user before proceeding. Trigger the [Advisor Pattern](./advisor-pattern.md) for any dimension scoring < 70. |
| **STOP** | < 70 | Do not execute. Report which dimensions are weak and what evidence is needed to raise them. |

A single dimension scoring **below 50** drops the band by one level even if the aggregate would otherwise allow proceeding. This prevents one strong dimension from masking a fundamental gap in another.

## 4. Per-Skill Adoption Profile

Different skills weight different dimensions implicitly. The Confidence Gate keeps the weights uniform but lets each skill specify which dimensions are *required to score above 70*. A required dimension scoring below 70 forces STOP regardless of aggregate.

Recommended profiles for skills that adopt this gate:

| Skill | Required dimensions | Rationale |
|-------|---------------------|-----------|
| `ywc-spec-validate` | Scope clarity, Root cause | A spec with unclear scope or undefined user need cannot be reviewed meaningfully. |
| `ywc-code-gen` | Architecture compliance, Reuse verified | Code generation that reinvents existing utilities or violates structure produces costly cleanup. |
| `ywc-impl-review` | Evidence quality, Root cause | Review findings without primary evidence are opinions, not findings. |
| `ywc-security-audit` | Evidence quality, Root cause | A security finding without root cause cannot be remediated correctly. |
| `ywc-tech-research` | Evidence quality, Reuse verified | Research that ignores prior art or relies on inference fails its purpose. |

Skills that do not adopt the gate explicitly may still report a confidence score for transparency.

## 5. Integration with Completion Status

Skills that already emit `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` should map gate bands to status as follows:

| Gate band | Completion status |
|-----------|-------------------|
| PROCEED, then succeeded | DONE |
| PROCEED, then encountered non-blocking issues | DONE_WITH_CONCERNS |
| REVIEW (alternatives presented) | NEEDS_CONTEXT |
| STOP | BLOCKED |

This keeps the existing status protocol intact while adding a quantitative basis for the choice between DONE_WITH_CONCERNS and BLOCKED.

## 6. Reporting Format

When a skill reports its confidence, use the following compact format. It fits inside an executor completion report or an impl-review summary without inflating length.

```
Confidence: 84/100 — REVIEW
  Scope clarity:           90
  Architecture compliance: 85
  Evidence quality:        80
  Reuse verified:          70
  Root cause identified:   90

Weakest dimension: Reuse verified (70)
Action: Searched existing utils/ for similar helpers; found two candidates
        but neither matches the required signature. Proceeding with new
        implementation; flagging for reviewer attention.
```

The "Weakest dimension" and "Action" lines are mandatory whenever the band is REVIEW or STOP. They explain to the user what raising the score would require.

## 7. Anti-Patterns

The following defeat the purpose of the gate. Skills must not do them.

- **Scoring after the fact to justify a decision.** Score before deciding, not after.
- **Rounding all dimensions up to clear the threshold.** A dimension scoring 65 is REVIEW, not PROCEED. The gate is not aspirational.
- **Hiding the score from the user when it is below 90.** Always report the aggregate and the weakest dimension. Silent confidence is worse than no confidence.
- **Adding extra dimensions per skill.** The five dimensions and their weights are fixed. Per-skill variation belongs in the "required dimensions" profile, not in new dimensions.
- **Treating the gate as a substitute for the Advisor Pattern.** A REVIEW band still typically warrants an Opus advisor for the weakest dimension. The gate decides *whether* to escalate; the Advisor Pattern decides *how*.

## 8. Scope and Limits

The gate is a decision aid, not a guarantee. It helps a skill avoid two specific failure modes:

- **False confidence** — proceeding when a critical dimension is weak.
- **False caution** — blocking when the aggregate is strong and no single dimension is critically weak.

It does not replace human judgment for architectural calls, security trade-offs, or release timing. Skills that defer such calls to a human should report the gate score as evidence supporting the deferral, not as a substitute for it.
