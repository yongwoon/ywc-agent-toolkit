---
name: ywc-brainstorm
description: >-
  (ywc) Use when the user has a rough idea or "let's build X" framing and
  intent is not yet pinned down. Clarifies purpose, constraints, success
  criteria, and 2-3 approaches before handing off to ywc-plan. Triggers:
  "아이디어", "brainstorm", "let's build", "アイディア", "ブレスト",
  "ywc-brainstorm". Do not use for an already-clear request (use ywc-plan),
  spec validation (use ywc-spec-validate), library/framework comparison (use
  ywc-tech-research), or implementation-time questions (use ywc-code-gen).
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
| "This existing-code problem I found isn't part of the request, so I won't mention it" | Ignoring it doesn't make it disappear — the new work lands on top of it either way. If it genuinely blocks or shapes the surface being changed (a file too large to extend safely, a boundary the new work must cross), fold a *targeted* improvement into the design's "Where it lives." If it merely lives nearby but doesn't block this round, name it once and route it to Out of Scope — never silently drop it, and never expand the design into an unrelated refactor. |
| "The user only wants approach A, I'll skip proposing alternatives" | Always propose 2–3 approaches with trade-offs. The user often *thinks* they want A but, when shown B and C, picks something else. Even if A wins, the explicit trade-off makes the design defensible during review. Lead with the recommendation, but show the alternatives. |
| "The request is too big for one design, I'll start anyway and split later" | If the request describes multiple independent subsystems ("a platform with X, Y, Z, and analytics"), STOP and decompose first. Each subsystem gets its own brainstorm → plan → spec cycle. Starting before decomposition produces a spec the user does not actually want and tasks that have to be re-cut. |
| "I'll skip the visible 'design presented' step and just start a `ywc-plan`" | The handoff to `ywc-plan` carries the approved design as input. Without an explicit approval step, `ywc-plan` has nothing concrete to operate on and will re-ask the same anchors — duplicating work, frustrating the user, and breaking the contract that each skill has a single responsibility. |
| "User wants to keep iterating in this session, I'll just keep brainstorming" | Once the design is approved, this skill terminates. Continuing to iterate inside the brainstorm scope reopens settled questions. If the user genuinely needs to change direction, end this skill, return to `ywc-brainstorm` for the *new* idea, and produce a new design doc. |
| "Every section already got a 'looks right' from the user in Step 5, so a self-review pass is redundant" | Per-section approval checks each piece in isolation as it is presented; contradictions between two independently-approved sections (a "Where it lives" that touches a service "Failure modes" never accounts for) only surface once the design is read as a whole. Step 5.5 is that whole-design pass — cheap to run, and it catches what per-section approval structurally cannot. |

**Violating the letter of these rules is violating the spirit.** The hard gate exists because every implementation skill is downstream of "the user said yes to this design."

## When to Use

Use when **any** of these apply:

- The user describes a goal, problem, or feature in their own words rather than a precise spec
- The intent could be implemented multiple ways and the trade-offs matter
- The request mentions external constraints (deadline, stakeholder, compliance, budget) that should shape design
- The scope is genuinely ambiguous (the user says "small thing" but the request touches multiple modules)

Do **not** use when:

- The request already specifies behavior, files, and acceptance criteria precisely → go to `ywc-plan` directly
- The destination is already known and the remaining work is deterministic multi-session discovery tracking → use `ywc-wayfinder`
- The user is validating an existing spec document → use `ywc-spec-validate`
- The decision is between specific libraries or frameworks → use `ywc-tech-research` first, return after
- The user is asking an implementation-time question ("how do I add this prop") → use `ywc-code-gen`

## Workflow

The skill is a 6-step dialogue. Steps 1–2 are pre-flight; Steps 3–5 are the conversation; Step 5.5 is a self-review pass; Step 6 is the handoff.

### Step 1: Explore project context

Before the first question, read enough to ground the conversation in current state:

- `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, `docs/architecture/` (if present) — convention and constraint
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

Before presenting the recommendation, run a quick blind-spot pass with [../references/unknown-matrix.md](../references/unknown-matrix.md) and surface any assumptions that are still worth validating. Keep the term internal; present them as concrete follow-up questions or caveats, not as "Unknown Matrix" jargon. Carry unresolved assumptions and their validation follow-ups into the Step 6 handoff and preserve them in the downstream plan's risk / follow-up language.

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

### Step 5.5: Self-review the design

Before drafting the Step 6 handoff, look at the approved design with fresh eyes and check four things:

1. **Placeholder scan** — any "TBD", "TODO", or vague requirement left in the anchors or design sections? Fix it now.
2. **Internal consistency** — does "Where it lives" match what "What we're building" describes? Does any section contradict another?
3. **Scope check** — does this still fit one `ywc-plan` cycle, or did the conversation drift into a second subsystem that Step 2 should have caught?
4. **Ambiguity check** — could any anchor be read two different ways? If so, pick one reading and make it explicit rather than carrying the ambiguity into the handoff.

Fix issues inline — no need to re-run the full per-section approval loop for a self-review fix. Only go back to the user if a fix changes the substance of something they already approved.

### Step 6: Handoff to ywc-plan

When approved, surface the handoff:

```text
✅ Design approved.
Next: $ywc-plan with the following intent

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

- [ ] Step 1 read the relevant `AGENTS.md` / `CODEX.md` / `CLAUDE.md`, `docs/`, and recent commits in the affected area
- [ ] Step 2 confirmed the request is scoped to one subsystem (or decomposed if not)
- [ ] All four anchors (What / Why / Out of Scope / Done When) have explicit one-sentence answers
- [ ] Step 4 presented at least 2 alternative approaches with explicit trade-offs — not just the recommended one
- [ ] Step 4 surfaced blind-spot assumptions worth validating before handoff
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
| [references/question-cookbook.md](references/question-cookbook.md) | Picking the right shape of question (multiple choice / open / scope check / constraint surface) for each anchor |
| [../references/question-first-gate.md](../references/question-first-gate.md) | Deciding whether the request is concrete enough to skip directly to `ywc-plan` |
| [../references/unknown-matrix.md](../references/unknown-matrix.md) | Running a blind-spot pass before recommending an approach or handing off to `ywc-plan` |
