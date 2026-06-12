# Question Cookbook

Pick the shape of question that fits the anchor you are trying to surface. Each row gives the **anchor**, the **question shape**, and a **concrete template** to adapt.

## Anchor: What (the concrete change)

| Question shape | Template |
|---|---|
| **Surface choice** (preferred — narrows fast) | "Is this a (a) new user-facing screen, (b) modification of an existing flow, (c) backend / API addition with no UI, or (d) internal tooling / dev experience change?" |
| **Behavioral diff** | "Right now, when a user does X, the system does Y. After this change, when a user does X, what should the system do?" |
| **Counter-example clarification** | "If we ship this and a user does X, what would convince them we built the wrong thing?" |
| **Boundary** | "Where does the change end? At <component A> / <component B> / both?" |

## Anchor: Why (the motivating reason)

| Question shape | Template |
|---|---|
| **Multiple-choice motivator** | "Is this driven by (a) a specific user request, (b) a metric we are trying to move, (c) a compliance / legal requirement, (d) a cleanup of past debt, or (e) something else?" |
| **Specific incident** | "Is there a specific incident, ticket, or complaint that triggered this? Can you point me to it?" |
| **Counter-factual** | "If we did not ship this, what concretely would go wrong, and for whom?" |
| **Stakeholder surface** | "Whose decision was this? Who needs to be happy with the result?" |

## Anchor: Out of Scope (the scope-creep guard)

| Question shape | Template |
|---|---|
| **Adjacent-temptation check** | "While we are in this area, what tempts us to also fix / add but we should leave alone this round?" |
| **Deferral confirm** | "X looks related but my read is it is deferred. Is that right? If not, when?" |
| **Surface freeze** | "Will the public API / DB schema / URL structure change in this round, or is it explicitly held stable?" |
| **Negative requirements** | "What should this NOT do, even though a future iteration might?" |

## Anchor: Done When (the success criterion)

| Question shape | Template |
|---|---|
| **Observable outcome** | "What concrete observable outcome would prove this is done? A specific URL returning a specific status, a metric crossing a threshold, a user completing a flow without error?" |
| **Test surface** | "What is the minimal automated test that, when passing, gives confidence the work is done?" |
| **Stakeholder accept** | "Whose acceptance signal closes this? Code review pass, QA sign-off, user pilot, all three?" |
| **Rollback criterion** | "What would force us to roll this back after shipping? That criterion's inverse is part of 'done'." |

## When the user gives a vague answer

| Symptom | Recovery question |
|---|---|
| "Just make it work" | "If 'working' is the bar, what would a failing version look like — what would I have to ship for you to say 'no, that is not it'?" |
| "Like the X system" | "X system has features A, B, C — are we copying all three, or which subset?" |
| "Same as before but better" | "Better in which axis — speed, correctness, UX clarity, observability, cost? Pick the one that matters most." |
| "Whatever you think is best" | "I have a recommendation, but the trade-off depends on <axis>. Where is <axis> in priority for this team this quarter?" |

## When to ask multiple questions at once

Default: one question per message.

The exceptions — when batching is acceptable:

- All four anchors are missing AND the user's initial framing was a one-liner ("can you add X"). One consolidated question covering the four anchors is acceptable in this single case, because the alternative is four turns of nearly-empty exchanges. **Use a numbered list with 4 lines, each ending with a question mark.**
- The user is on a tight time budget and has explicitly said so. Surface this once, ask the consolidated question, accept the response and move on. Do not chain multiple consolidated questions.

Outside these two cases, batching produces shallow answers. Prefer one question per turn.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Asking the question and including the answer you think is right | Pre-fills the option space; user agrees by default |
| Asking yes/no on a question that has 5 possible answers | Buries the actual disagreement; rephrase as multiple choice |
| Asking "what do you want?" with no scaffolding | Open-ended questions on undefined topics yield "make it good"; always provide structure |
| Asking the same anchor twice in different words | Signals you did not absorb the first answer; the user disengages |
| Asking about implementation details ("React or Vue?") in this skill | Implementation choice belongs to `ywc-tech-research` or `ywc-plan`. This skill stays on intent, not tech. |
