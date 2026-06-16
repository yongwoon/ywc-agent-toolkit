# ywc-receive-review

An attitude-layer discipline skill that **blocks performative agreement and forces technical verification** when receiving code-review feedback.

## What It Does

Enforces the Iron Law:

> **VERIFY BEFORE IMPLEMENTING. NO PERFORMATIVE AGREEMENT, EVER.**

A 6-step Response Pattern applies to every reviewer comment:

1. **READ** — Read the full feedback without reacting (no agreement, no disagreement, no tool calls yet).
2. **UNDERSTAND** — Restate the technical requirement in your own words; ask if any item is unclear before advancing.
3. **VERIFY** — Open the file, run the test, grep the symbol — check the reviewer's claim against current codebase.
4. **EVALUATE** — Decide whether the suggestion holds for this codebase in its current state (compatibility, prior decisions, YAGNI, platform constraints).
5. **RESPOND** — Acknowledge with a fix sentence, or push back with technical reasoning. **Forbidden**: "You're absolutely right!", "Great point!", "Thanks!"
6. **IMPLEMENT** — One item at a time, test each, surface a verification block per `ywc-verify-done`.

**Forbidden vocabulary** (full list in references/forbidden-acknowledgments.md):

| Forbidden | Replace with |
|---|---|
| "You're absolutely right!" | State the fix: "Fixed — `<file:line>` now <behavior>" |
| "Great point!" / "Excellent feedback!" | State the action or surface the question |
| "Thanks for catching that!" / "Thanks for the review!" | Drop entirely; the fix is the thanks |
| "Let me implement that right now" (before Step 3) | "Verifying before implementing: <check>" |

## When It Triggers

- User says "리뷰 받았어", "review feedback", "コメント返信".
- `ywc-handle-pr-reviews` delegates the attitude layer during inline-comment iteration.
- `ywc-finish-branch` surfaces a post-CI bot review that requires a response.
- About to respond to CodeRabbit / Codex Review / Claude Review.

## When NOT to Use

- Performing a review yourself → `ywc-impl-review`
- Creating a PR → `ywc-create-pr`
- Automation of fetching / threading / replying to PR comments → `ywc-handle-pr-reviews` (this skill is its attitude layer)
- Completion-claim verification → `ywc-verify-done`

## References

Full Response Pattern, forbidden-acknowledgment list, pushback conditions, and source-specific handling (human partner / external reviewer / bot) are in [SKILL.md](./SKILL.md). Adapted from `superpowers:receiving-code-review`, tuned for separation of concerns from `ywc-handle-pr-reviews` (attitude vs. automation).

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
