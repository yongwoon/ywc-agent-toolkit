# Scale Assessment Heuristics

This reference complements Step 3 of the `ywc-plan` workflow. Use it when the rubric in `SKILL.md` does not give an obvious answer.

## Default Bias

When ambiguous, **always default to Medium**. Reasoning:

- Cost of writing a spec for an actually-Small change: ~1 hour wasted, no rework
- Cost of skipping a spec for an actually-Medium change: rework, scope drift, re-decomposition

The asymmetry is severe. Lean toward the heavier process when uncertain.

## Hard Disqualifiers from Small

Any one of these forces Medium minimum, regardless of LOC count:

| Trigger | Reason |
|---|---|
| Database migration / schema change | Safety Invariant (mirrors `ywc-task-generator`). Migration must be its own task. |
| New library / framework introduction | Safety Invariant. Library introduction must be its own task. |
| New API contract that other services or clients consume | Contract changes need cross-team coordination — too risky for direct execution. |
| Authentication / authorization logic touched | Security-sensitive. Spec review catches issues code review may miss. |
| Cross-cutting concern modified across >1 module (logging, error handling, i18n) | Pattern changes ripple — needs phased rollout. |
| Public API breaking change (removing endpoints, changing response shape) | Backward-compatibility planning required. |

## Borderline Examples

### Example 1: "Add a new field to the user profile API response"

- Files touched: 2–3 (model, response serializer, possibly a test)
- LOC: ~50
- DB migration: yes (new column)
- **Verdict: Medium** — DB migration is a hard disqualifier, even though LOC is small.

### Example 2: "Fix the 500 error in the export endpoint when CSV has UTF-8 BOM"

- Files touched: 1–2 (endpoint handler, test)
- LOC: ~30
- DB migration: no
- New library: no
- API contract: no (bug fix, contract preserved)
- **Verdict: Small** — single-concern bug fix with no disqualifiers.

### Example 3: "Add a settings page that lets users configure notification preferences"

- Files touched: ~10 (UI components, route, API endpoint, model, migration, tests)
- LOC: ~400
- DB migration: yes
- **Verdict: Medium** — Multi-concern (UI + API + DB), DB migration disqualifier.

### Example 4: "Refactor the email-sending utility to use a queue"

- Files touched: 3–5 (utility, callers updated, queue config)
- LOC: ~200
- DB migration: no
- New library: maybe (queue client)
- Cross-cutting: yes (callers across modules)
- **Verdict: Medium** — cross-cutting concern + possible library introduction.

### Example 5: "Rename the `getUserData` function to `fetchUser` everywhere"

- Files touched: many (mechanical rename)
- LOC: many (mechanical)
- DB migration: no
- New library: no
- Cross-cutting: lexical, not behavioral
- **Verdict: Small** — even though many files change, this is a single mechanical concern with no behavior change. Direct execution path is appropriate.

## Tie-Breakers When Multiple Scales Plausibly Apply

| Tie | Decision rule |
|---|---|
| Small vs. Medium | Choose Medium. (See Default Bias above.) |
| Medium vs. Large | If expected task count is 12–18, choose Medium and proceed. If 18+, choose Large and recommend split. |
| Large vs. "split into multiple specs" | If feature boundaries are genuinely separable (e.g., "user auth" vs. "user profile"), recommend split. If the work is one tightly-coupled feature (e.g., "checkout flow"), keep as Large. |

## When to Stop Investigating

The Step 2 codebase investigation is for **scale assessment and grounding**, not exhaustive understanding. Stop reading code once you can confidently:

1. Pick a scale using the rubric
2. Name concrete files/paths in the plan or spec
3. State the project's actual lint/test/build commands

Going beyond this is `gstack-investigate`'s job. Defer to that skill if the user explicitly wants deep investigation.
