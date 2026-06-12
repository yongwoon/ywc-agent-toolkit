# ywc-confidence-gate

A pre-implementation discipline skill that forces an explicit 5-dimension confidence score and surfaces a PROCEED / REVIEW / STOP decision before any implementation tool is invoked.

## What It Does

Enforces the Iron Law:

> **NO IMPLEMENTATION WITHOUT AN EXPLICIT CONFIDENCE SCORE AND BAND DECISION**

Scores 5 dimensions (each 0–100), takes the weighted sum, and maps to a band.

| Dimension | Weight | One-sentence test |
|---|---|---|
| Scope clarity | 25% | Can you state in-scope and out-of-scope each in one sentence without vague terms? |
| Architecture compliance | 25% | Does the planned change follow existing structure / naming / abstractions? |
| Evidence quality | 20% | Are claims backed by primary sources (code, official docs, test output)? |
| Reuse verified | 15% | Have you searched for existing utilities and ruled out each with a reason? |
| Root cause identified | 15% | Bug: do you name the cause, not the symptom? Greenfield: the underlying need, not the surface request? |

| Band | Aggregate | Action |
|---|---|---|
| **PROCEED** | ≥ 90 | Begin implementation; carry the score into the executor report |
| **REVIEW** | 70–89 | Present 1–3 alternatives or open questions; raise the weakest dimension first |
| **STOP** | < 70 | Do not begin; surface weak dimensions and route back to upstream skill |

**Single-dim `< 50` override**: the aggregate sets a tentative band, then any single dimension scoring below 50 drops it by one level (PROCEED → REVIEW, REVIEW → STOP) — always one level, never a jump straight to STOP, and a dimension at exactly 50 does not trigger it. Prevents a strong dimension from masking a fatal weakness.

## When It Triggers

- User says "ready to implement", "should I proceed", "confidence check", "確信度チェック", "구현 시작해도 돼".
- Boundary entry of `ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-agentic`.
- After `ywc-plan` Scale assessment, just before downstream handoff.
- Before any commit with material architectural impact.

## When NOT to Use

- Post-implementation verification → `ywc-verify-done` (the symmetric gate using the same rubric)
- Spec quality review → `ywc-spec-validate`
- Implementation review score → `ywc-impl-review` (also uses this rubric — scores comparable)
- Intent clarification → `ywc-brainstorm`

## References

Full workflow and anti-patterns are in [SKILL.md](./SKILL.md). The canonical rubric definition is the shared reference [../references/confidence-gate.md](../references/confidence-gate.md). The skill draws from ECC's confidence-check pattern and SuperClaude's PM Agent rubric.

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
