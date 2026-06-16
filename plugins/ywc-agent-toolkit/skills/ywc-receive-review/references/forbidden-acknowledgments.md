# Forbidden Acknowledgments Reference

Auditing checklist for performative-agreement language in code-review reply drafts. Skim before sending any reply to reviewer feedback (human, bot, or human partner).

## Affirmation interjections (replace with the fix sentence)

| Forbidden | Replacement pattern |
|---|---|
| "You're absolutely right!" | "Fixed — `<file:line>` now <behavior>" |
| "You're right!" | "Verified. <fix or commit hash>" |
| "Absolutely!" | Drop. State the action. |
| "Great point!" | "Will fix; verifying <X> first." |
| "Excellent point!" | Drop. State the question or the action. |
| "Excellent feedback!" | Drop. State the action. |
| "Good catch!" | Drop. State the action. ("Good catch" with a fix sentence below it is **not** acceptable — drop the prefix and let the fix stand alone.) |
| "Nice catch!" | Drop. |
| "Fantastic point!" | Drop. |

## Gratitude expressions (always drop)

| Forbidden | Replacement pattern |
|---|---|
| "Thanks for catching that!" | Drop. The fix is the thanks. |
| "Thanks for the review!" | Drop. Get to the technical content. |
| "Thanks for the feedback!" | Drop. |
| "Thanks for taking the time!" | Drop. |
| "Appreciate it!" | Drop. |
| "Much appreciated." | Drop. |
| "Thanks!" (standalone) | Drop. |

The rule: any unsolicited expression of gratitude is performative. The codebase records what was implemented, not how grateful the implementer sounded.

**If you catch yourself about to write "Thanks":** delete it. State the fix or the question instead.

## Premature commitment (acknowledging before verification)

| Forbidden | Why dangerous |
|---|---|
| "Let me implement that right now" (before Step 3 — VERIFY) | Commits you before you have checked the claim. The post-verification reversal is expensive. |
| "Implementing now" (before Step 3) | Same as above. |
| "On it!" | Implies action; the reviewer infers verification has happened. |
| "Will do." | Same. |
| "Sure, I'll fix that." | Same. |
| "Fixing." (without a verification block) | Verification is the bar; the word "fixing" without evidence is acknowledgment, not action. |

**Rule**: the word indicating action ("fixing", "implementing", "on it") must appear *together with* the verification block (`ywc-verify-done` shape) — not before it.

## False-humility softeners (replace with technical content)

| Forbidden | Why it weakens the reply |
|---|---|
| "I think you might be right, but…" | "Might" is the failure mode. Either verify and acknowledge, or push back with reasoning. |
| "Sorry for the oversight" | Apology is not the fix. State the fix; if the oversight matters, it shows in the regression test. |
| "My bad" | Same. Drop. |
| "I should have noticed that" | Drop. Move to action. |
| "Apologies for the confusion" | Drop. Re-state the technical content clearly. |

## Pushback-killers (replace with technical pushback)

| Forbidden | Replacement pattern |
|---|---|
| "I disagree" (alone) | "I disagree because <technical reason cited from file / test / commit>. What is the path you want?" |
| "That won't work for us" (alone) | "<X> would break <Y> because <Z>. Alternatives: (a) <…>, (b) <…>." |
| "We can't do that" (alone) | "<X> conflicts with <prior decision / constraint>. Should we revisit <prior decision> or take alternative <Y>?" |
| "Won't fix" (without rationale) | Provide reasoning and a path: "Won't fix because <X>; if <Y> changes, this becomes addressable." |

## Apology-loops after a wrong pushback

When the reviewer corrects your pushback and you were wrong:

| Forbidden | Replacement pattern |
|---|---|
| Long apology | "Verified, you are right because <X>. Implementing now." |
| Defending the original pushback | Drop the defense. State the correction in one sentence and move on. |
| "I should have known that" | Drop. The correction speaks for itself. |
| "I'm sorry for the back-and-forth" | Drop. The back-and-forth is normal; it does not need apology. |

Over-apologizing after a wrong pushback teaches the reviewer that pushback is fragile. The next time you push back correctly, they may interpret it as another error. Stay flat and factual.

## Bulk-reply anti-patterns

| Forbidden | Why it fails |
|---|---|
| "Will address all comments" (single reply for many comments) | Hides the per-item verification. The reviewer re-reads everything to figure out which item was acknowledged. |
| "Thanks for the comprehensive review, will work through these!" (preamble to bulk reply) | Two anti-patterns at once: gratitude + bulk. Drop both; reply per-item. |
| "Pushed a commit addressing comments 1, 3, 4" (without per-item rationale) | The commit shows the edits but not the per-item decision. Each comment thread should have its own reply with the reasoning. |

## Audit procedure

Before sending any reply to a reviewer comment:

1. Search the draft for the exact strings in the tables above (case-insensitive).
2. For each hit, either delete the sentence or replace it with the corresponding evidence pattern.
3. Confirm the reply contains either (a) a fix description with verification, or (b) a technical pushback ending in a question, or (c) a clarification question — and nothing else.
4. Send.

This audit takes under 30 seconds and prevents the most common class of trust-erosion incidents in code review.

## Acceptable acknowledgment shapes (kept here as a positive reference)

These shapes pass the audit:

- "Fixed in <commit>. `<file:line>` now <behavior>."
- "Verified. `<command>` exit 0. Fix applied."
- "Reproduced via `<test name>`; fix in <commit>."
- "Confirmed via grep — the symbol is unused. Removed."
- "Will fix; first verifying <X> because <Y>."
- "I disagree because <technical reason cited from file / test / commit>. <Path A> or <path B>?"
- "Cannot verify <X> without <Y>. Should I (a) investigate, (b) ask <person>, or (c) proceed assuming the claim?"

All of these (a) commit to evidence, (b) end with the next action or question, (c) contain no gratitude.
