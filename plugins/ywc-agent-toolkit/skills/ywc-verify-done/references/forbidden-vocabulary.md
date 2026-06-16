# Forbidden Vocabulary Reference

Auditing checklist for unverified-assertion language in completion-claim messages. Skim this list before surfacing any "done" / "ready" / "passed" statement.

## Hedging modals (replace with evidence)

| Forbidden | Replacement pattern |
|---|---|
| should pass | "Tests pass — 34/34 passed, exit 0" |
| should work | "Behavior X observed: <reproduction step> → <expected output>" |
| should be fine | Drop entirely and surface the verification block |
| ought to | Drop entirely; if unsure, downgrade the claim |
| would normally | Reproduce the case and observe — do not extrapolate |

## Perception verbs (replace with measurements)

| Forbidden | Replacement pattern |
|---|---|
| seems to work | "Reproduction: <command>; observed: <line>; expected: <line>" |
| appears to be | Direct evidence in the block |
| looks correct | Direct evidence in the block |
| feels right | Drop entirely — feelings are not evidence |

## Self-confidence claims (replace with output)

| Forbidden | Replacement pattern |
|---|---|
| I think | "Per `<command>`: <line>" |
| I believe | "Per `<command>`: <line>" |
| I'm confident | Confidence is not evidence; show the command output |
| pretty sure | Show the command output |

## Premature celebration (move below the verification block)

| Forbidden BEFORE the block | Allowed AFTER the block |
|---|---|
| "Great!" | Fine, with evidence above |
| "Perfect!" | Fine, with evidence above |
| "Done!" | Fine, with evidence above |
| "All set!" | Fine, with evidence above |

Rule: celebration is welcome **after** the verification block, not before. Readers parse top-down — the first positive signal becomes the decision.

## Partial-verification weasels

| Forbidden | Why dangerous |
|---|---|
| "mostly passing" | Hides the failing subset; surface the failing test names |
| "almost there" | Drop — a claim is binary; either verify the partial work explicitly or do not claim |
| "no issues that I noticed" | The reader assumes you looked; the absence of detection is not the absence of issue |
| "looks like X" | Always a hedge; replace with the actual measurement |

## Time-shift weasels

| Forbidden | Why dangerous |
|---|---|
| "passed last time" | Last-time evidence does not cover current-state changes |
| "will run CI later" | Verification AFTER the claim is not verification |
| "I'll fix the remaining tomorrow" | "Done with remaining" ≠ "done"; downgrade to "partial: X done, Y remaining" |

## Audit procedure

Before sending any message that contains a completion-adjacent sentence:

1. Search the draft for the exact strings in the tables above (case-insensitive)
2. For each hit, either delete the sentence or replace it with the corresponding evidence pattern
3. Confirm the verification block (`**Verification:** ...`) appears above the claim line
4. Send

This audit takes under 30 seconds and prevents the most common class of false-completion incidents.
