---
name: ywc-brainstorm
description: >-
  (ywc) Use when the user has a rough idea, a half-formed feature request, or
  "let's build X" framing and intent has not yet been pinned down. Surfaces
  purpose, constraints, success criteria, and 2–3 alternative approaches
  through one-question-at-a-time Socratic dialogue before any implementation
  begins, then hands off to ywc-plan. Triggers: "아이디어", "구상",
  "어떻게 만들지", "이런 거 만들고 싶은데", "brainstorm", "let's build",
  "discuss this idea", "어떻게 시작", "ideate", "explore", "feature 구상",
  "アイディア", "どう作る", "ブレスト", "ywc-brainstorm". Do not use for an
  already-clear request (go straight to ywc-plan), validating an existing
  spec (use ywc-spec-validate), choosing between libraries or frameworks
  (use ywc-tech-research), or implementation-time questions (use
  ywc-code-gen).
category: discipline
phase: pre-plan
requires: []
---

# ywc-brainstorm

**Announce at start:** "I'm using the ywc-brainstorm skill to surface intent, constraints, and 2–3 alternative approaches before any implementation work begins."

This skill is the entry point for any "I have an idea — let's build something" interaction. It exists because every implementation skill (`ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`) assumes the request is *understood*. When that assumption breaks, the implementation ships the wrong thing, and the spec / task / code work all has to be redone. The cost of one brainstorming session is 10–30 minutes; the cost of skipping it is a full re-plan iteration through `ywc-plan` → `ywc-spec-validate` → `ywc-task-generator` → code, measured in hours per iteration. Adapted from `superpowers:brainstorming`, tightened to hand off to `ywc-plan` rather than implementation.

## The Hard Gate

```text
NO IMPLEMENTATION SKILL, SPEC DRAFTING, OR CODE WRITING UNTIL A DESIGN IS
PRESENTED AND THE USER HAS APPROVED IT.
```

This applies to **every** request, regardless of perceived simplicity. The design can be short (a few sentences for genuinely small changes), but it must be surfaced and the user must explicitly approve before the workflow proceeds.

The terminal state of this skill is **invoking `ywc-plan`** with the approved intent in hand. Do not jump to `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, or any executor.

## Rationalization Defense

When tempted to bypass the gate, check this table first:

| Excuse | Reality |
|---|---|
| "This is too simple to need a design" | "Simple" is where unexamined assumptions cause the most rework. Every project goes through the gate. The design can be short — but it must be presented and approved. |
| "The user said 'just build it', I'll skip the questions" | "Just build it" is a request for speed, not a waiver on understanding. Confirm the four anchors (What, Why, Out of Scope, Done When) in one consolidated question. The user agrees to the design, and the implementation downstream stays on rails. |
| "I'll ask all the questions at once to save turns" | One question at a time is non-negotiable. Multi-question dumps produce shallow answers (the user picks the easiest one) and miss the assumption you most needed to surface. Use multiple choice when it speeds the answer, but keep to one topic per turn. |
| "I know the codebase, I don't need Step 1 (context exploration)" | Familiarity is the failure mode. The "I know this" agent reuses a stale mental model and proposes a design that conflicts with a constraint added last week. Always check current files, recent commits, and any `docs/ywc-plans/` or `docs/specification/` entries in the same area. |
| "The user only wants approach A, I'll skip proposing alternatives" | Always propose 2–3 approaches with trade-offs. The user often *thinks* they want A but, when shown B and C, picks something else. Even if A wins, the explicit trade-off makes the design defensible during review. Lead with the recommendation, but show the alternatives. |
| "The request is too big for one design, I'll start anyway and split later" | If the request describes multiple independent subsystems ("a platform with X, Y, Z, and analytics"), STOP and decompose first. Each subsystem gets its own brainstorm → plan → spec cycle. Starting before decomposition produces a spec the user does not actually want and tasks that have to be re-cut. |
| "I'll skip the visible 'design presented' step and just start a `ywc-plan`" | The handoff to `ywc-plan` carries the approved design as input. Without an explicit approval step, `ywc-plan` has nothing concrete to operate on and will re-ask the same anchors — duplicating work, frustrating the user, and breaking the contract that each skill has a single responsibility. |
| "User wants to keep iterating in this session, I'll just keep brainstorming" | Once the design is approved, this skill terminates. Continuing to iterate inside the brainstorm scope reopens settled questions. If the user genuinely needs to change direction, end this skill, return to `ywc-brainstorm` for the *new* idea, and produce a new design doc. |

**Violating the letter of these rules is violating the spirit.** The hard gate exists because every implementation skill is downstream of "the user said yes to this design."

## When to Use

Use when **any** of these apply:

- The user describes a goal, problem, or feature in their own words rather than a precise spec
- The intent could be implemented multiple ways and the trade-offs matter
- The request mentions external constraints (deadline, stakeholder, compliance, budget) that should shape design
- The scope is genuinely ambiguous (the user says "small thing" but the request touches multiple modules)

Do **not** use when:

- The request already specifies behavior, files, and acceptance criteria precisely → go to `ywc-plan` directly
- The user is validating an existing spec document → use `ywc-spec-validate`
- The decision is between specific libraries or frameworks → use `ywc-tech-research` first, return after
- The user is asking an implementation-time question ("how do I add this prop") → use `ywc-code-gen`

## Workflow

The skill is a 6-step dialogue. Steps 1–2 are pre-flight; Steps 3–5 are the conversation; Step 6 is the handoff.

### Step 1: Explore project context

Before the first question, read enough to ground the conversation in current state:

- `CLAUDE.md`, `AGENTS.md`, `docs/architecture/` (if present) — convention and constraint
- `docs/ywc-plans/` or `docs/specification/` for any in-flight design in the same area
- Recent commits on the affected surface (`git log --oneline -20 -- <area>`)
- The exact files the user named, if any

The point is not to read the whole repo — it is to avoid asking questions whose answers are already in the codebase, and to detect collisions with in-flight work.

### Step 2: Detect "too big for one design"

If the user's request describes multiple independent subsystems (e.g., "a platform with auth, chat, billing, and analytics"), STOP before any questions.

Surface the situation:

> "This request covers <N> independent subsystems: <list>. Each needs its own design → plan → implementation cycle, otherwise the spec becomes too broad to validate. Would you like to (a) pick the first subsystem to brainstorm now, or (b) talk through how to decompose first?"

Resume only after the scope is narrowed to one subsystem.

### Step 3: Ask clarifying questions — one at a time

Use **one question per message**. Prefer multiple-choice phrasing when possible — it makes the answer cheaper for the user and forces you to surface the actual options.

Cover the four anchors (the same anchors `ywc-plan` will need downstream — collecting them here means `ywc-plan` does not have to re-ask):

| Anchor | Sample question |
|---|---|
| **What** | "What concrete behavior changes? Is the user-facing surface a new screen, a modified action, an API addition, or something else?" |
| **Why** | "What problem does this solve? Is it a user complaint, a metric we are trying to move, a compliance requirement, or a cleanup?" |
| **Out of Scope** | "What might look related but is explicitly out of scope for this round? (Anything you are deferring even though it is in the same area.)" |
| **Done When** | "How will we know this is done? What observable outcome counts as success?" |

If the initial request already answers one of these, do not re-ask — confirm in one sentence and move to the next.

### Step 4: Propose 2–3 approaches with trade-offs

Once intent is clear, present 2 or 3 approaches in conversational prose. For each: one-sentence summary, the trade-offs, and an explicit "fits this case because…" or "less fit because…".

Lead with your recommendation. Make the recommendation defensible from the anchors collected in Step 3, not from generic best-practice talk.

If the user has a strong preference already, still present the alternatives — the explicit trade-off is what makes the choice defensible during `ywc-spec-validate` and later review.

### Step 5: Present the design and get approval

Present the design in sections sized to their complexity. Cover at minimum:

- **What we're building** (the chosen approach, in one paragraph)
- **Where it lives** (concrete file paths, modules, or services touched)
- **Data shape** (if any) — entity / DTO / contract, just enough to disambiguate the approach
- **Failure modes** (what can go wrong, what we do about each)
- **Out of Scope** (verbatim from Step 3)

After each section, confirm understanding: "Does that match what you have in mind?"

After the last section, ask explicitly: "Should I hand this off to `ywc-plan` to produce the full plan / spec?"

This is the approval gate. Until the user says yes, do not advance.

### Step 6: Handoff to ywc-plan

When approved, surface the handoff:

```text
✅ Design approved.
Next: /ywc-plan with the following intent

What: <one paragraph>
Why: <one paragraph>
Out of Scope: <bullet list>
Done When: <bullet list>
Recommended approach: <one paragraph; alternatives noted as "ruled out because …">

(Detailed sections from Step 5 follow as context for ywc-plan.)
```

Never proceed to `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, or any executor from this skill. The contract is: brainstorm produces an approved design; `ywc-plan` decides Small vs. Medium/Large and routes accordingly.

## Output Format

The skill emits no committed file by itself — the design lives in the conversation history and the handoff message. `ywc-plan`, when invoked next, will write the `plan.md` (Small) or `docs/ywc-plans/<slug>.md` (Medium/Large).

If the conversation runs long enough that the design needs a checkpoint, optionally write a draft to `docs/ywc-plans/_brainstorm-<slug>.md` (the `_brainstorm-` prefix marks it as pre-plan, not yet a spec). This is optional — most sessions can hand off directly without an intermediate file.

## Integration

- **Upstream callers:** User invocation; `ywc-plan` Step 1 (when an idea arrives via `ywc-plan` but has not yet been understood — `ywc-plan` delegates the clarification dialogue here).
- **Downstream:** `ywc-plan` (always). Never `ywc-code-gen`, `ywc-spec-writer`, or any executor directly.
- **Pairs with:** `ywc-tech-research` (when the design hinges on a library / framework choice — pause this skill, run `ywc-tech-research`, then return), `ywc-product-review` (when the design needs business framing beyond what the user gave).

## Validation Checklist

Before handing off, verify:

- [ ] Step 1 read the relevant `CLAUDE.md`, `docs/`, and recent commits in the affected area
- [ ] Step 2 confirmed the request is scoped to one subsystem (or decomposed if not)
- [ ] All four anchors (What / Why / Out of Scope / Done When) have explicit one-sentence answers
- [ ] Step 4 presented at least 2 alternative approaches with explicit trade-offs — not just the recommended one
- [ ] Step 5 surfaced the design in sections and received explicit per-section confirmation
- [ ] The user said "yes" (or equivalent) to the handoff prompt, not just to the recommendation
- [ ] The handoff message includes the four anchors verbatim, not summarized
- [ ] No implementation skill, spec drafting, or code edit happened during this dialogue

## Common Mistakes

- **Combining the "approach" presentation and the "design" presentation into a single message.** The approach is the *what* you would do; the design is the *how*. The user needs to approve the approach before the design is worth presenting. Separate them into Steps 4 and 5.
- **Asking the question and the multiple-choice options together with the user's likely answer pre-filled.** Pre-filling collapses the option space — the user nods, and the assumption you most needed to surface is buried. Ask the question; let the user pick.
- **Treating a "go ahead" mid-conversation as the final approval.** "Go ahead with that direction" approves the *approach*; it does not approve the *design*. Always ask the final handoff question explicitly.
- **Skipping the four-anchor confirmation because "the request already had them."** Re-state each anchor in your own words and ask "is that right?" — the user's wording and yours may diverge, and that divergence is the most common source of "this is not what I asked for" downstream.

## References

| Reference | Use when |
|---|---|
| [references/question-cookbook.md](references/question-cookbook.md) | Picking the right shape of question (multiple choice / open / scope check / constraint surface) for each anchor |
| [../references/question-first-gate.md](../references/question-first-gate.md) | Deciding whether the request is concrete enough to skip directly to `ywc-plan` |
