---
name: ywc-brainstorm
description: >-
  (ywc) Use when the user has a rough idea, half-formed feature request, or
  "let's build X" framing and intent isn't pinned down yet. Surfaces purpose,
  constraints, success criteria, and 2-3 alternatives via Socratic dialogue
  before implementation, hands off to ywc-plan. Triggers: "아이디어", "구상",
  "어떻게 만들지", "만들고 싶은데", "brainstorm", "discuss this idea", "ideate",
  "アイディア", "どう作る", "ブレスト", "ywc-brainstorm". Do not use for an
  already-clear request (use ywc-plan), validating an existing spec (use
  ywc-spec-validate), choosing libraries/frameworks (use ywc-tech-research),
  or implementation-time questions (use ywc-code-gen).
category: discipline
phase: pre-plan
requires: []
---

# ywc-brainstorm

**Announce at start:** "I'm using the ywc-brainstorm skill to surface intent, constraints, and 2–3 alternative approaches before any implementation work begins."

Clarify the request before planning. Hand the approved design to `ywc-plan`, never directly to implementation.

## The Hard Gate

```text
NO IMPLEMENTATION SKILL, SPEC DRAFTING, OR CODE WRITING UNTIL A DESIGN IS
PRESENTED AND THE USER HAS APPROVED IT.
```

This applies to **every** request, regardless of perceived simplicity. The design can be short (a few sentences for genuinely small changes), but it must be surfaced and the user must explicitly approve before the workflow proceeds.

**Disposable prototypes are exempt.** For design-heavy requests, generating throwaway HTML mockups (Step 4) to surface the user's visual taste is *exploration*, not implementation — the gate blocks production code, spec drafting, and executor handoff, not disposable artifacts written to the `_brainstorm-<slug>/` scratch directory and discarded once the direction is chosen.

The terminal state of this skill is **invoking `ywc-plan`** with the approved intent in hand. Do not jump to `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, or any executor.

## Non-negotiables

- Explore current context; include only existing-code improvements that directly shape this work.
- Decompose independent subsystems before asking detailed questions.
- Ask one question at a time, present 2–3 approaches, and get approval for both the chosen approach and the detailed design.
- Use disposable visual prototypes only when visual comparison would clarify a decision; never treat them as production code.
- Do not treat a request for speed, familiarity with the codebase, or apparent simplicity as an exception to the hard gate.

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

The skill is a 6-step dialogue. Steps 1–2 are pre-flight; Steps 3–5 are the conversation; Step 5.5 is a self-review pass; Step 6 is the handoff.

### Step 1: Explore project context

Before the first question, read enough to ground the conversation in current state:

- `CLAUDE.md`, `AGENTS.md`, `docs/architecture/` (if present) — convention and constraint
- `docs/ywc-plans/` or `docs/specification/` for any in-flight design in the same area
- Recent commits on the affected surface (`git log --oneline -20 -- <area>`)
- The exact files the user named, if any

The point is not to read the whole repo — it is to avoid asking questions whose answers are already in the codebase, and to detect collisions with in-flight work.

If this exploration surfaces an existing problem that affects the work at hand — a file that has grown too large, an unclear module boundary, a tangled responsibility the new work must cross — fold a *targeted* improvement into the design's "Where it lives" (Step 5). Do not propose unrelated refactoring that merely lives nearby; anything not blocking the current work is named once and routed to Step 3's Out of Scope, not built into the design.

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

#### Design-heavy requests: divergent visual prototypes

When the request is design-centric — a new user-facing screen, a visual redesign, a landing page, or a component whose *look and feel* is the point — prose approaches cannot surface the user's visual taste (the "Unknown Knowns" they would never write into a spec). In that case, **additionally** generate 2–4 deliberately divergent HTML mockups and let the user react to them before Step 5.

Read [references/divergent-prototypes.md](references/divergent-prototypes.md) for how divergent to make them, the self-contained single-file rules, where to write them, and how to run the reaction. The mockups are throwaway *exploration* artifacts under `docs/ywc-plans/_brainstorm-<slug>/prototypes/` — never carried into production; only the chosen direction feeds the Step 5 design.

After presenting the approaches — and getting a visual reaction when applicable — ask which approach to use as the basis for the detailed design. Do not begin Step 4.5 or Step 5 until the user confirms it.

### Step 4.5: Blind-spot pass (the Unknown Matrix)

Before presenting the design, run one explicit pass against the four quadrants of the Unknown Matrix. The point is to surface what neither you nor the user has said out loud — the left column is already in hand, so the two right-hand quadrants are the whole reason for this step:

| Quadrant | Question | What to do with it |
|---|---|---|
| Known Knowns | "What do I already know I want, and what has Step 1 already verified?" | Two sources: the four anchors (confirmed user *intent*) **and** the requirements / constraints verified from the repo or spec in Step 1. Confirm the Step 1 repo/spec constraints are stated explicitly in the design before handoff — do not assume the four anchors alone cover them. |
| Known Unknowns | "What do I know I haven't figured out?" | Ask if it could change scope, an interface, data shape, permissions, or Done When; otherwise record it as a risk or follow-up. |
| Unknown Knowns | "What is so obvious to the user they never said it?" (implicit convention, house style, taste) | Surface as a one-line confirmation question before Step 5. |
| Unknown Unknowns | "What has nobody considered at all?" | Name the risk in the design's Failure Modes. |

Ask at most 1–2 confirmation questions for the highest-risk Unknown Knowns. Resolve any uncertainty that could change scope, an interface, data shape, permissions, or Done When before Step 5; record only non-blocking risks as Failure Modes. See [references/question-cookbook.md](references/question-cookbook.md) "Blind spots" for question shapes.

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

### Step 5.5: Self-review the design

Before drafting the Step 6 handoff, look at the approved design with fresh eyes and check four things:

1. **Placeholder scan** — any "TBD", "TODO", or vague requirement left in the anchors or design sections? Fix it now.
2. **Internal consistency** — does "Where it lives" match what "What we're building" describes? Does any section contradict another?
3. **Scope check** — does this still fit one `ywc-plan` cycle, or did the conversation drift into a second subsystem that Step 2 should have caught?
4. **Ambiguity check** — clarify only wording that does not change the approved substance. If an interpretation could change scope, behavior, an interface, data shape, permissions, or Done When, return to Step 3 and ask the user.

Fix issues inline — no need to re-run the full per-section approval loop for a self-review fix. Only go back to the user if a fix changes the substance of something they already approved.

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

**Optional: persist the mission.** After surfacing the handoff, offer once to persist the durable part of this design to the project mission file:

```text
Persist this to docs/project-mission.md? (Mission = What + Why, Success Criteria = Done When)
→ /ywc-project-mission --mode update --source brainstorm   [y / skip]
```

If the user accepts, invoke `ywc-project-mission --mode update --source brainstorm`, mapping **What+Why** to the Mission / North-Star and each **Done When** item to a measurable Success Criterion; `ywc-project-mission`'s own CHANGESET confirmation gate still applies. If the user declines (or does not respond), it is a **clean no-op** — never write the mission file without acceptance, and never block the handoff on it. Only the *durable* anchors belong in the mission; a feature-specific Done-When is for `ywc-plan`, not the mission file.

Never proceed to `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, or any executor from this skill. The contract is: brainstorm produces an approved design; `ywc-plan` decides Small vs. Medium/Large and routes accordingly.

## Output Format

The skill emits no committed file by itself — the design lives in the conversation history and the handoff message. `ywc-plan`, when invoked next, will write the `plan.md` (Small) or `docs/ywc-plans/<slug>.md` (Medium/Large).

If the conversation runs long enough that the design needs a checkpoint, optionally write a draft to `docs/ywc-plans/_brainstorm-<slug>.md` (the `_brainstorm-` prefix marks it as pre-plan, not yet a spec). This is optional — most sessions can hand off directly without an intermediate file.

## Integration

- **Upstream callers:** User invocation; `ywc-plan` Step 1 (when an idea arrives via `ywc-plan` but has not yet been understood — `ywc-plan` delegates the clarification dialogue here).
- **Downstream:** `ywc-plan` (always). Never `ywc-code-gen`, `ywc-spec-writer`, or any executor directly.
- **Optional persistence:** `ywc-project-mission` (Step 6 — opt-in offer to persist the durable Mission (What+Why) + Success Criteria (Done When) via `update --source brainstorm`; declining is a clean no-op, the handoff never blocks on it).
- **Pairs with:** `ywc-tech-research` (when the design hinges on a library / framework choice — pause this skill, run `ywc-tech-research`, then return), `ywc-product-review` (when the design needs business framing beyond what the user gave).

## Validation Checklist

Before handing off, verify:

- [ ] Step 1 read the relevant `CLAUDE.md`, `docs/`, and recent commits in the affected area
- [ ] Step 2 confirmed the request is scoped to one subsystem (or decomposed if not)
- [ ] All four anchors (What / Why / Out of Scope / Done When) have explicit one-sentence answers
- [ ] Step 4 presented at least 2 alternative approaches with explicit trade-offs — not just the recommended one
- [ ] For a design-heavy request, Step 4 generated ≥2 divergent HTML mockups (in `_brainstorm-<slug>/prototypes/`) and the user reacted before Step 5
- [ ] Step 4.5 blind-spot pass ran — Unknown Knowns surfaced as confirmation questions, Unknown Unknowns recorded as Failure Modes
- [ ] Step 5 surfaced the design in sections and received explicit per-section confirmation
- [ ] Step 5.5 self-review passed — placeholder scan, internal consistency, scope check, and ambiguity check all clear before the handoff was drafted
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
| [references/question-cookbook.md](references/question-cookbook.md) | Picking the right shape of question (multiple choice / open / scope check / constraint surface) for each anchor, and the Step 4.5 blind-spot ("Unknown Matrix") question shapes |
| [references/divergent-prototypes.md](references/divergent-prototypes.md) | Generating 2–4 divergent, disposable HTML mockups for a design-heavy request (Step 4) to surface the user's visual taste |
| [../references/question-first-gate.md](../references/question-first-gate.md) | Deciding whether the request is concrete enough to skip directly to `ywc-plan` |
