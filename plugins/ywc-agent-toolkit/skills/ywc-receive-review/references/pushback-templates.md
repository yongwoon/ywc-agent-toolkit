# Pushback Templates

Composition templates for technical pushback. Pick the template matching the condition, fill the placeholders with file paths / test names / commit references, end with a question.

The rule: pushback **must** include (a) a technical reason citing a primary source, and (b) a question that lets the reviewer accept or correct your verification.

## Template 1 — Breaks existing functionality

**Condition**: the suggested change would break a behavior covered by an existing test or known to be used.

```text
<Suggestion paraphrased in one sentence> would break <existing behavior>.

Evidence:
- `<test path:line>` covers this case (passes today; would fail under the suggestion).
- `<source file:line>` is the call site that depends on the current behavior.

Options I can see:
- (a) Keep current behavior; address the suggestion's intent via <alternative>.
- (b) Drop <dependent surface> and apply the suggestion.

Which direction do you want?
```

## Template 2 — Reviewer lacks full context

**Condition**: the suggestion is reasonable in isolation but conflicts with a deliberate decision the reviewer did not see (gated debug, feature flag, intentional `as any`, documented exception).

```text
<Suggestion paraphrased> would also remove <context the reviewer may not have seen>.

Context I want to surface:
- `<source file:line>` carries <comment / linter-disable / feature flag> documenting that <X> is intentional because <Y>.
- The case is exercised by <test / production trigger>.

Two paths:
- (a) Keep the intentional pattern; close the review item with this rationale.
- (b) Remove the rationale (and the gated behavior); apply the suggestion.

Which?
```

## Template 3 — YAGNI

**Condition**: the suggestion is "implement this properly" but the surface is not used.

```text
Before implementing, grepped the codebase: <symbol / endpoint / feature> is not referenced outside <self-reference / its own tests>.

Options:
- (a) Remove the surface entirely (YAGNI).
- (b) Implement the "proper" version anyway because <future requirement>.

Where is the usage I'm missing, or is (a) the call?
```

## Template 4 — Technically incorrect for this stack

**Condition**: the suggestion assumes a runtime / language / platform feature not available in the project's target environment.

```text
<Suggestion> uses <API / syntax / feature> available in <version X+>; project targets <version Y> (see `<config file:line>`).

Options:
- (a) Polyfill / shim — adds <transitive dependency / complexity>.
- (b) Upgrade the project's target to <X+> — coordinates with <CI / consumers / SLA>.
- (c) Apply the spirit of the suggestion using <project-compatible alternative>.

Which fits the project's current direction?
```

## Template 5 — Conflicts with prior decision

**Condition**: the suggestion contradicts an ADR, a documented previous PR decision, or the user's stated direction.

```text
<Suggestion> would reverse the decision in <ADR-NNNN / PR #NNNN / chat decision on YYYY-MM-DD>:

> <one-line quote of the prior decision>

The original reason was <one sentence>. If that reason still holds, the suggestion is out of scope for this PR; if it no longer holds, the path forward is to update <ADR / decision record> first.

Should I:
- (a) Close the review item referencing the prior decision (kept as-is)?
- (b) Open a follow-up to revisit <ADR-NNNN>?
- (c) Apply the suggestion in this PR and update the decision record together?
```

## Template 6 — Cannot verify locally

**Condition**: verifying the claim requires access / data / environment you do not have.

```text
Verification I can do here: <X>. Result: <evidence>.
Verification I cannot do locally: <Y> — requires <production access / pageviews / staging deploy / customer report>.

Three options for the next step:
- (a) I proceed assuming the claim, with rollback ready if <Y> contradicts.
- (b) You verify <Y> and share the result here.
- (c) Add monitoring / instrumentation to surface <Y> before merging.

Which fits?
```

## Template 7 — Reviewer items are interrelated; one needs clarification before any can be addressed

**Condition**: items 4 and 5 are unclear in a way that affects how items 1, 2, 3, 6 should be implemented.

```text
Understanding for items 1, 2, 3, 6: <one line each>.

Need clarification on 4 and 5 before implementing any of these:
- Item 4: <quote>. Does this mean (a) <…> or (b) <…>?
- Item 5: <quote>. The current code at `<file:line>` does <X>; the suggestion implies <Y>. Confirm <Y>?

Holding implementation of all items until 4 and 5 are clear, because the answers affect how 1, 2, 3, 6 should land.
```

## Template 8 — Bot reviewer suggested a "professional" feature that is unused

**Condition**: CodeRabbit / Codex Review / Claude Review proposed expanding a feature with no current consumer.

```text
Bot suggestion: <one-line summary>.
Project state: <symbol / endpoint> is not referenced — confirmed by `git grep <symbol>`.

Applying YAGNI:
- (a) Remove the unused surface (preferred).
- (b) Keep the surface; do not "properly implement" until a consumer exists.

Going with (a) unless there is upcoming use I should know about. Calling this out so the reviewer can correct if (b) is intended.
```

## Composition rules

Every template above follows the same shape:

1. **One-sentence paraphrase** of the suggestion (proves you read it).
2. **Evidence** citing file path / line / test name / ADR / commit / grep result.
3. **2–3 explicit options** with the path forward for each.
4. **Question** that gives the reviewer the next move.

If a draft pushback is missing any of (1)–(4), it is not pushback — it is friction. Add the missing element before sending.

## Sending pushback in the GitHub thread

Per `ywc-handle-pr-reviews`, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment. Top-level comments hide the relationship between the pushback and the original suggestion.

## After the pushback lands

If the reviewer **accepts** the pushback: close the thread by replying with the rationale ("Closed — keeping current behavior per <reason>"), no gratitude. Move to the next item.

If the reviewer **corrects** the pushback (you were wrong): apply the correction in one sentence and implement. Do not apologize at length — see `references/forbidden-acknowledgments.md` § "Apology-loops after a wrong pushback".

If the reviewer **does not respond** within the team's normal review window: the silence is itself a decision in most teams (default to the reviewer's original suggestion). Confirm the team's convention before defaulting.
