# Agent Rubric — 0–5 Banding per Axis

Codex custom agents (`codex/agents/ywc-*.toml`) are evaluated on a **different** axis set than skills: an agent has no README locale set, but it has sandbox permissions, a model assignment, and a `Status:` output contract that skills lack.

| Axis | Weight | Tier |
|---|---|---|
| A1 Role-boundary clarity | 20 | judgment |
| A2 Dispatch accuracy | 25 | mixed |
| A3 Sandbox minimality | 15 | mechanical |
| A4 Output-contract compliance | 15 | mechanical |
| A5 Model-tier appropriateness | 15 | mixed |
| A6 System-prompt quality | 10 | judgment |

Total weight = 100. Item total = Σ(axis_score / 5 × weight).

## A1 — Role-Boundary Clarity (weight 20)

Judgment. Is the agent's responsibility crisp and non-overlapping with sibling agents and with the skill-level reviewers it may be dispatched from?

| Score | Band |
|---|---|
| 5 | Single responsibility, one sentence; clearly distinct from every sibling and from the skill-side reviewers (e.g., `ywc-typescript-reviewer` vs the generic Design subagent in `ywc-impl-review`). |
| 4 | Distinct, but the description's scope sentence is broader than the body actually delivers. |
| 3 | Overlaps one sibling's responsibility; a dispatcher could pick either. |
| 2 | Two agents would plausibly be dispatched for the same finding category. |
| 1 | Responsibility stated only by example, not by boundary. |
| 0 | Redundant with a sibling, or scope is "general helper" with no boundary. |

## A2 — Dispatch Accuracy (weight 25)

Highest-weight agent axis — the agent analog of skill S1. Will the orchestrator (or `ywc-impl-review`'s Tier-2 dispatch logic) select this agent at the right moment and not at the wrong one? Mechanical collision sub-signal + judged precision over the agent cases in `evals/trigger-cases.json`.

| Score | Band |
|---|---|
| 5 | `description` enumerates concrete dispatch triggers AND explicit "Do not use for" exclusions; no overlap with sibling agents' trigger surface. |
| 4 | Triggers clear, one exclusion missing. |
| 3 | Triggers present but one collision with a sibling agent unresolved. |
| 2 | Triggers vague ("for code tasks"); dispatcher must guess. |
| 1 | No exclusions; high collision risk across multiple siblings. |
| 0 | Description does not state when to dispatch. |

Mechanical sub-signal: caps A2 at 3 if `score.py` finds a description n-gram overlap with a sibling agent above threshold and neither names the other as an exclusion.

## A3 — Sandbox Minimality (weight 15)

Mechanical. Least privilege. Parse the Codex agent's `sandbox_mode`.

| Score | Band |
|---|---|
| 5 | Uses `sandbox_mode = "read-only"` for reviewer/advisor/analyst roles. |
| 4 | Uses a broader sandbox with a clear, role-specific justification in `developer_instructions`. |
| 3 | Sandbox is broader than necessary but the body forbids writes. |
| 2 | Sandbox is broader than necessary and no write boundary is stated. |
| 1 | Sandbox allows broad mutation for a narrow review/advisor role. |
| 0 | Missing sandbox declaration or a reviewer/analyst can write with no boundary. |

Heuristic: current repository policy requires Codex agents to keep `sandbox_mode = "read-only"`.

## A4 — Output-Contract Compliance (weight 15)

Mechanical (presence) + judgment (adherence). Codex agents MUST define the `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` contract plus a `Next action:` when the caller must apply or inspect something.

| Score | Band |
|---|---|
| 5 | Output contract includes an inline `Status:` block with the four states (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT) and a parseable `Next action:`. |
| 4 | Contract defined, one state or `Next action:` under-specified. |
| 3 | Output shape implied by an example but not stated as a contract. |
| 2 | Free-form output; caller must parse prose. |
| 1 | Output format contradicts the caller's expectation. |
| 0 | Codex agent missing the `Status:` contract entirely. |

## A5 — Model-Tier Appropriateness (weight 15)

Mechanical heuristic + judgment. Is the agent on the right model for its cognitive load? Frontier judgment (architecture, root-cause, security boundary) → Opus; standard implementation/review → Sonnet; mechanical enumeration (coverage counting, formatting) → Haiku.

| Score | Band |
|---|---|
| 5 | Model assignment matches the role's reasoning demand and is justified where non-obvious. |
| 4 | Reasonable assignment, justification absent. |
| 3 | Over-provisioned (Opus for mechanical work) — correct output, wasted cost. |
| 2 | Under-provisioned (Haiku for architecture judgment) — quality risk. |
| 1 | Assignment contradicts the role (mechanical agent on Opus AND judgment agent on Haiku in the same catalog). |
| 0 | No model declared where the harness needs one. |

## A6 — System-Prompt Quality (weight 10)

Judgment. Persona clarity, anti-rationalization coverage, vague-language density.

| Score | Band |
|---|---|
| 5 | Persona unambiguous; the prompt pre-empts the rationalizations the role would actually make; zero un-thresholded vague language. |
| 4 | Strong prompt, one vague phrase. |
| 3 | Clear role but no anti-rationalization guardrails. |
| 2 | Generic helper tone; relies on the model's defaults. |
| 1 | Internally inconsistent instructions. |
| 0 | Prompt does not establish the role. |
