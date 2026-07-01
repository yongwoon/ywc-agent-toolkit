# Agent Rubric — 0–5 Banding per Axis

Claude Code custom agents (`claude-code/agents/ywc-*.md`) are evaluated on a **different** axis set than skills: an agent has no README locale set, but it has a tool grant, a model assignment, and a return contract that skills lack. Codex TOML agents are evaluated separately by `.codex/skills/ywc-codex-toolkit-eval`.

| Axis | Weight | Tier |
|---|---|---|
| A1 Role-boundary clarity | 20 | judgment |
| A2 Dispatch accuracy | 25 | mixed |
| A3 Tool-grant minimality | 15 | mechanical |
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

## A3 — Tool-Grant Minimality (weight 15)

Mechanical. Least privilege. Parse the agent's tool grant.

| Score | Band |
|---|---|
| 5 | Grants exactly the tools the role needs. Read-only reviewers (`*-reviewer`, `*-analyst`, `*-engineer` in audit role) hold no `Write`/`Edit`/`Bash`-mutate. |
| 4 | One broader-than-needed grant with a plausible justification in the body. |
| 3 | A read-only-by-name agent holds `Edit` or `Write` but does not use it. |
| 2 | Holds mutating tools unrelated to its stated role. |
| 1 | Grants `*` (all tools) for a narrow role. |
| 0 | A reviewer/analyst agent can write to the repo with no contract forbidding it. |

Heuristic: if the agent name or description contains `review`, `audit`, `analyst`, or "read-only", the presence of `Write`/`Edit`/`NotebookEdit` in the grant drops A3 to ≤3.

Mechanical default (`score.py`, `a3_tool_band`): `*` → 1; a read-only-by-role agent holding any mutating tool → 3; **every other bounded, explicit grant → 5**. An implementer agent (coder / worker) legitimately needs `Write`/`Edit`/`Bash`, so a bounded mutating grant on a non-read-only role is minimal-for-role and scores 5 — it is NOT capped at 4. The mechanical tier cannot distinguish "exactly needed" (5) from "one tool broader than needed" (4) without role knowledge; it defaults to 5 and the judgment tier demotes to 4 only when it identifies a specific unused/extraneous tool.

## A4 — Output-Contract Compliance (weight 15)

Mechanical (presence) + judgment (adherence). Claude Code agents should define a clear, parseable output shape or explicitly reference the canonical return contract.

| Score | Band |
|---|---|
| 5 | Output contract follows the canonical Return Contract — a clear inline shape or an explicit reference to `claude-code/skills/references/subagent-status-actions.md §3.5`. An inline-invented incompatible format does not qualify. |
| 4 | Contract defined, one state or `Next action:` under-specified. |
| 3 | Output shape implied by an example but not stated as a contract. |
| 2 | Free-form output; caller must parse prose. |
| 1 | Output format contradicts the caller's expectation. |
| 0 | No output contract: no Status block, no canonical reference, and no contract defined. |

## A5 — Model-Tier Appropriateness (weight 15)

Mechanical heuristic + judgment. Is the agent on the right model for its cognitive load? The mechanical heuristic (`score.py`, FR3) infers the expected tier from role keywords in the agent **name**: frontier judgment (`architect`, `root-cause`, `critic`) → Opus; documentation / formatting / mechanical enumeration (`doc-writer`, `documentation`, `formatting`, `mechanical`, `enumeration`) → Haiku; **everything else — including `security`, `reviewer`, `coder`, `engineer` — → Sonnet**. Security review in this toolkit is static analysis on Sonnet by design and is NOT an Opus-expected role. Mechanical bands: declared == expected → 5; over-provisioned → 3; under-provisioned → 2; model present but tier unrecognized → 4; no model → 0. The judgment tier may refine within these.

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
