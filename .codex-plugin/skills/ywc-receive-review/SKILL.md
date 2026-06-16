---
name: ywc-receive-review
description: >-
  (ywc) Use when receiving code-review feedback (human reviewer comments,
  CodeRabbit, Codex Review, Claude Review, ChatGPT review, or any
  reviewer-shaped input) and about to respond or implement changes.
  Enforces technical verification before agreement, blocks performative
  acknowledgments ("You're absolutely right!", "Great point!", "Thanks!"),
  and requires clarification of unclear items before partial implementation.
  Triggers: "리뷰 받았어", "리뷰 코멘트", "리뷰 대응", "PR comment 처리",
  "review feedback", "received review", "respond to review", "address
  review comments", "リビュー対応", "レビュー受信", "コメント返信",
  "ywc-receive-review". Do not use for performing a code review yourself
  (use ywc-impl-review), creating a PR (use ywc-create-pr), or for the
  automation orchestration of fetching / replying to inline PR comments
  (use ywc-handle-pr-reviews — this skill is its attitude layer, the two
  compose).
---

# ywc-receive-review

**Announce at start:** "I'm using the ywc-receive-review skill to verify review feedback before responding — no performative agreement, no blind implementation."

This skill is the attitude layer for receiving code-review feedback. It exists because the default LLM behavior — agreeing eagerly to whatever the reviewer says and starting to implement — produces three failure modes the ywc workflow must avoid: (1) implementing a "fix" that breaks a deliberately-shaped behavior the reviewer did not know about; (2) blindly removing code the reviewer thought was unused but is actually called from a path they did not see; (3) burning trust by saying "You're absolutely right!" to a wrong suggestion and then quietly reverting. Adapted from `superpowers:receiving-code-review`, tightened to integrate as the attitude layer of `ywc-handle-pr-reviews` (which owns the *automation*; this skill owns the *judgment*).

## The Iron Law

```text
VERIFY BEFORE IMPLEMENTING. NO PERFORMATIVE AGREEMENT, EVER.
```

Receiving review feedback is **technical evaluation**, not emotional performance. Every item is a *suggestion to evaluate*, not an order to follow. The act of agreeing must be backed by a technical check; the act of disagreeing must be backed by technical reasoning.

## Rationalization Defense

When tempted to skip verification or to soften the response, check this table first:

| Excuse | Reality |
|---|---|
| "Saying 'You're right!' is polite — it doesn't change the technical outcome" | It changes two things: (1) it commits you to an implementation before you have verified the suggestion holds, which makes the post-verification correction expensive; (2) it teaches the reviewer (and any teammate reading the thread) that your agreements are not load-bearing. State the fix instead of the gratitude — actions speak. |
| "The reviewer is more senior, I should defer" | Authority is not a check against a codebase. A senior reviewer who has not opened the file in 6 months may suggest a change that broke something last week. Verify against current code; then defer with evidence, or push back with evidence. |
| "Pushing back feels confrontational — implementing is friendlier" | Friendlier today, hostile tomorrow when the implementation breaks production and someone has to figure out why a clearly-wrong suggestion was accepted without comment. Technical pushback **is** the courteous response — it preserves the reviewer's intent, your trust, and the codebase. |
| "I'll batch-acknowledge all 12 items and then implement them" | Items are often related. Partial understanding of one becomes partial implementation of another. Read all items, clarify unclear ones, **then** implement. Acknowledging without understanding is a worse failure than asking. |
| "The bot review is automated, no harm in agreeing reflexively" | The bot has no context for `// eslint-disable-next-line` next to a known-safe pattern, for the `as any` that documents a deliberate type erasure, for the `console.log` that was the user's manual debug tool. Bot suggestions need the same verification a human's would. |
| "If I push back and I'm wrong, I look incompetent" | If you defer and you are wrong, the codebase has a documented bug *and* the reviewer trusts that subsequent acceptances mean you checked. Both costs compound. Push back with technical reasoning; if you are wrong, the correction is one sentence: "Verified, you are right because <X>. Implementing." |
| "Saying 'Thanks for catching that!' shows I'm a team player" | The codebase does not record team-player points. It records the fix. Surface the fix; the team-player signal is implicit in the speed and accuracy of the action. |
| "The user is my human partner — I should not push back on them" | The human partner asks for pushback when the partner is wrong. Implementing a wrong instruction without surfacing the concern is the failure mode. Use technical reasoning, not defiance: "Before implementing, I want to flag that <X> appears to conflict with <Y>. Should I proceed, or revise?" |
| "Multiple reviewers gave contradicting suggestions — I'll pick whichever feels right" | Surface the contradiction and ask the human partner. Reviewers who disagree have not seen each other's comments; you have. The job is to surface, not to arbitrate. |
| "Asking for clarification slows the review down" | Implementing the wrong interpretation and then re-implementing it correctly is slower than asking once. Estimate: 1 question (~1 minute round-trip) beats a misimplementation (~30 minutes plus second review). |

**Violating the letter of this discipline is violating the spirit.** The codebase records what was implemented, not what was said. Every "You're absolutely right!" without a corresponding verified fix is a small lie that compounds.

## The Response Pattern

For every reviewer comment, execute these six steps in order. Skipping any step is the failure mode.

```text
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
```

| # | Step | What it produces |
|---|---|---|
| 1 | READ | The full feedback, read without reacting. No agreement, no disagreement, no implementation tool calls yet. |
| 2 | UNDERSTAND | Restate the technical requirement in your own words, or — if any part is unclear — ask before advancing. |
| 3 | VERIFY | Check the claim against the current codebase: open the file, run the failing test, grep for the alleged dead reference, read the cited line. |
| 4 | EVALUATE | Decide: does the suggestion hold for **this** codebase in **this** state? Consider compatibility, deliberate prior decisions, YAGNI, platform constraints. |
| 5 | RESPOND | Acknowledge with a fix sentence, or push back with technical reasoning. Forbidden: "You're absolutely right!", "Great point!", "Thanks!" |
| 6 | IMPLEMENT | One item at a time, test each, surface the verification block per `ywc-verify-done`. |

## Forbidden Acknowledgments

The following phrases are **never** acceptable in response to review feedback. They commit you to an implementation before verification (Step 3) and they teach the reviewer that your agreements are noise.

| Forbidden | Replace with |
|---|---|
| "You're absolutely right!" | State the fix: "Fixed — `<file:line>` now <behavior>." |
| "Great point!" | State the fix or the question: "Will fix; verifying <X> first." |
| "Excellent feedback!" | Drop entirely. State the action. |
| "Thanks for catching that!" | Drop entirely. The fix is the thanks. |
| "Thanks for the review!" (preamble) | Drop entirely. Get to the technical content. |
| "Let me implement that right now" (before Step 3) | "Verifying before implementing: <check>." |
| "Good catch!" | Drop entirely. State the action. |
| Any unsolicited gratitude expression | Drop entirely. Actions speak. |

A complete list of forbidden phrases (including paraphrases and tells) is in [`references/forbidden-acknowledgments.md`](references/forbidden-acknowledgments.md).

**If you catch yourself about to write "Thanks":** delete it. State the fix or the question instead.

## When to Push Back

Push back, with technical reasoning, when the suggestion meets any of these:

| Condition | Example |
|---|---|
| Breaks existing functionality | "Removing the legacy branch breaks pre-10.15 clients — verified in `userAgent.test.ts:24`. Drop pre-10.15 support, or keep the branch?" |
| Reviewer lacks full context | "The `console.log` is gated behind `DEBUG=auth`; removing it disables a documented debugging surface. Wrap in `if (process.env.DEBUG === 'auth')` removal, or keep?" |
| YAGNI violation | "Grepped the codebase — `metricsEndpoint` is not called. Remove rather than 'implement properly'?" |
| Technically incorrect for this stack | "Suggested API is Node 20+; project targets Node 18. Use the polyfill or upgrade target?" |
| Conflicts with prior decision | "ADR-0007 chose Pattern X over the suggested Pattern Y on 2026-03-12 because <reason>. Revisit ADR, or implement another way?" |

How to push back well:

- **Technical reasoning first.** Cite the file, line, test, or commit.
- **End with a question, not an assertion.** Lets the reviewer accept your verification or correct it.
- **No defensiveness.** "I disagree" alone is not pushback — it is friction. "I disagree because <X>; what is the path you want?" is pushback.

## Handling Unclear Feedback

If any item is unclear, **stop**. Do not implement the clear items first.

```text
IF any item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on the unclear items, naming them by number / quote
WHY: Items are often related. Partial implementation of item 3 because items
     4 and 5 are unclear produces work that has to be re-done once items 4
     and 5 land.
```

Example:

> Reviewer: "Fix items 1-6"
> You understand 1, 2, 3, 6. Unclear on 4, 5.
>
> ❌ Wrong: implement 1, 2, 3, 6 now; ask about 4 and 5 later.
> ✅ Right: "I understand items 1, 2, 3, 6. Need clarification on 4 and 5 before implementing — specifically, what behavior do you want for <X> in item 4, and is item 5 asking for <Y> or <Z>?"

## Source-Specific Handling

The level of skepticism scales with the source.

### From the user (human partner)

- **Trusted by default.** Implement after understanding (Step 2) and verification (Step 3).
- **Still ask** if scope is unclear.
- **Still push back** when the user is technically wrong — courteously, with reasoning.
- **No performative agreement.** Skip to the action or the technical acknowledgment.

### From an external human reviewer

- **Skeptical, with care.** External reviewers often see the diff without the surrounding context.
- Before implementing, run the verification checklist:

  1. Technically correct for **this** codebase?
  2. Does it break any existing tests?
  3. Is there a documented reason for the current implementation?
  4. Does it work on all supported platforms / versions?
  5. Does the reviewer have the full context, or is there context they lack?

- If you cannot easily verify a claim, say so: "I cannot verify <X> without <Y>. Should I (a) investigate, (b) ask <person>, or (c) proceed assuming the claim?"

### From a bot reviewer (CodeRabbit, Codex Review, Claude Review)

- **Skeptical, more so.** Bots lack project-specific context — the `as any` is deliberate, the `eslint-disable-next-line` is documented, the dead branch is a feature flag.
- Apply the YAGNI check: does the suggested "professional implementation" cover something that is actually used?
- If the bot suggests >5 items, batch by category (lint / type / behavior / docs) and address the categories — not the individual items — to avoid acknowledgment-thrash.

### Conflicts with prior architectural decisions

When a suggestion contradicts a documented ADR, prior PR, or the user's stated direction: **stop**. Surface the conflict to the user before implementing or pushing back. The reviewer may not have seen the prior decision; the user is the one who decides whether to revisit it.

## Acknowledging Correct Feedback

When feedback **is** correct and you have verified it, acknowledge by stating the fix. No gratitude.

| Good | Bad |
|---|---|
| "Fixed. `auth.ts:42` now rejects expired tokens with 401." | "You're absolutely right! Let me fix that!" |
| "Fixed. `pagination.ts:18` had the off-by-one." | "Thanks for catching that, fixing now." |
| (Just commit the fix and reply with the commit hash) | "Great point! Implementing now." |

When acknowledging via the GitHub thread (per `ywc-handle-pr-reviews`), reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:

| Good | Bad |
|---|---|
| "You were right — verified <X>, the suggestion does hold because <Y>. Implementing now." | Long apology + defense of why you pushed back |
| "Verified, my initial read missed <Z>. Fixing." | Over-explanation, undermining future pushbacks |

State the correction factually and move on. The codebase records the fix, not the apology.

## Implementation Order

After all items are clarified and verified, implement in this order:

```text
1. Blocking issues (security, data loss, broken builds)
2. Simple fixes (typos, imports, lint)
3. Complex fixes (refactoring, logic, architecture)
```

Test each fix individually. Verify each via `ywc-verify-done` before claiming "fix applied".

## Output Format

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Items handled: <n>
Implemented fixes: <file:line + verification command>
Pushbacks/questions: <technical reason + question>
Remaining blockers: <none or explicit blocker>
```

## Integration

- **Upstream callers**: user invocation; `ywc-handle-pr-reviews` (per inline-comment iteration — this skill is its attitude layer); `ywc-finish-branch` (post-CI bot reviews surfaced by `scripts/poll-pr-reviews.sh`).
- **Downstream**: `ywc-verify-done` (per-fix verification block); `ywc-debug-rootcause` (when a "fix" attempt fails ≥ 2 times on the same comment — escalate); `ywc-impl-review` (when the reviewer's suggestion turns out to expose a class of defects beyond the current PR — open a finding for follow-up).
- **Pairs with**: `ywc-handle-pr-reviews` (automation of inline-comment fetching / threading / replying — this skill governs the **what to say** and **what to do**, the other governs the **how to send**).

## Validation Checklist

Before submitting any reply to review feedback, verify:

- [ ] Every reviewer item was READ in full (no skim)
- [ ] Every item is UNDERSTOOD or has been explicitly asked about
- [ ] Every claim was VERIFIED against the current codebase (file read, test run, grep)
- [ ] Every fix has a one-sentence rationale tied to the verification, not to the reviewer's authority
- [ ] No forbidden vocabulary appears in the reply ("You're absolutely right!", "Thanks!", "Great point!")
- [ ] Pushbacks include a technical reason + a question
- [ ] Acknowledgments name the fix or commit hash, not gratitude
- [ ] Unclear items are asked about, not partially implemented around
- [ ] Multi-item replies follow the order: blockers → simple → complex
- [ ] If reviewer's suggestion conflicts with a prior decision (ADR / PR / user direction), the conflict was surfaced before implementing

## Common Mistakes

(Procedural failure modes specific to this skill. Behavioral rationalizations are in the table above — do not duplicate here.)

- **Replying to the easy comments first to show progress, leaving the hard ones for later.** The hard ones often constrain the easy ones; the easy fixes become rework when the hard answers arrive.
- **Replying in bulk with a single "Will address" comment.** Each reviewer item deserves its own response thread on the PR (`ywc-handle-pr-reviews` handles the threading mechanics). Bulk replies hide the per-item verification and make the reviewer re-read everything.
- **Pushing back without a question.** "I disagree" is friction; "I disagree because <X>, want me to do <Y> instead?" is pushback. Always end with a path forward.
- **Acknowledging correct feedback with "Thanks!" anyway, because it feels rude not to.** The codebase does not record politeness. State the fix; the speed and accuracy of the fix are the courtesy.
- **Carrying a wrong pushback forward with a long apology after the reviewer corrects you.** Apologies undermine future pushbacks (the reviewer learns "they cave under pressure"). State the correction in one sentence and move on.

## References

| Reference | Use when |
|---|---|
| [references/forbidden-acknowledgments.md](references/forbidden-acknowledgments.md) | Auditing a draft reply for performative-agreement language; full vocabulary list with replacements |
| [references/pushback-templates.md](references/pushback-templates.md) | Composing technical pushback for the five common conditions (broken functionality, missing context, YAGNI, stack incompatibility, prior decision) |
| [../ywc-handle-pr-reviews/SKILL.md](../ywc-handle-pr-reviews/SKILL.md) | Automation for fetching unresolved comments, threading replies, and managing the PR-review loop — this skill governs the response *content*, that skill governs the response *plumbing* |
| [../ywc-verify-done/SKILL.md](../ywc-verify-done/SKILL.md) | Per-fix verification block (command + exit code + claim) attached to every "fixed" acknowledgment |
