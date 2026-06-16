# Architectural Stop Signals

Decision aid for the Phase 4 §5 escape hatch: when 3+ fixes on the same surface have failed, is the next fix worth attempting, or is the architecture wrong?

The default answer after 3 failures is **architecture is wrong**. This document lists the specific signals to confirm that diagnosis and the shape of the surface-to-user that follows.

## Signals that the architecture (not the next fix) is the problem

| Signal | What it looks like in practice |
|---|---|
| **Each fix moves the defect to a new location** | Fix #1 in module A → defect appears in module B. Fix #2 in module B → defect appears in module C. The defect is following the data, not the line. |
| **Each fix requires "massive refactoring" to implement cleanly** | The "correct" version of fix #3 would touch 8 files, span 2 modules, and change a public interface. This is the architecture telling you the seam is in the wrong place. |
| **The pattern itself does not match the requirement** | The code is implementing pattern P (e.g., synchronous request/response) but the requirement is pattern Q (e.g., eventual consistency with retry). No local fix will reconcile these — pattern P is the wrong abstraction. |
| **Fixes contradict each other** | Fix #1 adds a guard at layer A; fix #2 adds the inverse guard at layer B because layer A's guard caused a new failure. The guards are fighting because the responsibility boundary is wrong. |
| **Each fix degrades a previously-working surface** | After fix #2, the failing test passes — but two other tests now fail. After fix #3, those tests pass but a third surface breaks. The fixes are not localized because the coupling is not localized. |
| **The failing surface depends on shared mutable state that no single component owns** | Every fix is "add another check before/after" — none can guarantee correctness because the invariant has no single owner. |

When ≥2 of these signals fire, treat the situation as architectural.

## Signals that the next fix is worth attempting (rare after 3 failures)

| Signal | Why it might justify fix #4 |
|---|---|
| **Each prior fix tested a different hypothesis and was correctly rejected** (not abandoned without verification) | The investigation is converging — the *next* hypothesis genuinely narrows the search space. |
| **The defect surface has not moved** through the prior fixes | Same line, same condition, same value — the bug is local; the prior fixes simply did not match the actual cause. |
| **A new piece of evidence has surfaced** since fix #3 (new log line, new reproduction step, new dependency change) | The hypothesis space has changed; the next attempt is not "fix harder", it is "investigate with new data". |

If none of these apply, do not attempt fix #4.

## Surface-to-user shape

When the diagnosis is architectural, the message to the user has these parts in this order:

```markdown
### Architectural concern (Phase 4 §5 escape)

**Attempted fixes:**

1. <commit hash / file:line> — <one-line description>. Result: <how it failed and what new symptom appeared>.
2. <commit hash / file:line> — <one-line description>. Result: <how it failed and what new symptom appeared>.
3. <commit hash / file:line> — <one-line description>. Result: <how it failed and what new symptom appeared>.

**Pattern observed:** <which of the signals above fired; quote the specific behavior>

**Architectural concern:** <one paragraph: what the architecture currently is, what it should be, why no local fix can bridge the gap>

**Proposed paths (pick one):**

- **A.** <small architectural change with scope and risk>
- **B.** <medium refactor with scope and risk>
- **C.** <pattern replacement with scope and risk>

**Recommendation:** <which option and why>

**This is not a Phase 4 completion** — the next step requires a design decision, not another fix.
```

The user — not the agent — decides which path to take. The agent's job at this point is to surface the architectural mismatch, not to commit to a redesign.

## Anti-patterns at this point

| Anti-pattern | Why it is wrong |
|---|---|
| "Let me try one more fix" | After 3 failures with ≥2 signals firing, the next fix has no better odds than the prior three. Stop. |
| "I'll refactor it myself, no need to ask" | Architectural decisions span beyond the immediate fix — they affect other components, other timelines, other team members. Always surface. |
| "Add a feature flag to switch between old and new pattern" | A feature flag preserves both architectures; the bug now lives in both. Only useful if the new pattern is already validated, which it is not. |
| "Skip the failing test for now" | Hiding the symptom does not fix the architecture; it just removes the evidence. |
| "Open a follow-up issue and move on" | Acceptable only if the user — not the agent — decides the architectural debt is tolerable for this session. |

## Connection to other skills

- **`ywc-plan`** — receives the architectural surface and decides whether to escalate to a Medium/Large spec for the redesign.
- **`ywc-tech-research`** — when the proposed paths involve a library or framework change, route here first.
- **`ywc-impl-review`** — when the architectural concern is symptomatic of a class of defects (not just this one), surface it as a review finding for the broader codebase.
