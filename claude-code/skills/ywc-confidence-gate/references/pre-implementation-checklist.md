# Pre-Implementation Probe Questions

Per-dimension question banks for the moment **before** implementation starts. The shared rubric reference (`../../references/confidence-gate.md`) defines the dimensions and scoring bands; this file provides concrete probes tuned to the pre-implementation usage (the post-review usage owned by `ywc-impl-review` has different evidence available, so its probes diverge).

Score each dimension by reading the probes, picking the one(s) that fit the work item, and answering honestly in 1–2 lines of evidence.

## Dimension 1 — Scope clarity (weight 25%)

Score the precision with which the work item is bounded.

- [ ] Can the work item be stated in one sentence with no "and other improvements", "related cleanup", or "as needed"?
- [ ] Is the **out-of-scope** list explicit? (If "out of scope" is empty, score ≤ 80 — every non-trivial work item has things to defer.)
- [ ] Are the touched files / modules enumerable (≤ 10 named explicitly, or a clearly bounded subtree)?
- [ ] Is the user-observable change concrete? ("Add a new screen" alone is ≤ 70; "Add screen X showing fields A, B, C with action D" is ≥ 90.)
- [ ] If the work item depends on another in-flight change, is that dependency named?

**Score 90+** when all five answer yes. **60–89** when two or more answer no — surface the no's as open questions. **< 60** when the scope is "do the thing we discussed last week" with no artifact to point to.

## Dimension 2 — Architecture compliance (weight 25%)

Score how well the planned change aligns with existing structure.

- [ ] Does the plan reuse existing layering (controller / service / repository, or the project's equivalent)?
- [ ] Do new identifiers follow the project's naming convention? (Check 3 sibling files.)
- [ ] If new patterns / abstractions are introduced, has the user agreed to them explicitly? ("Plan said it" counts only if the plan was approved.)
- [ ] If the change touches a public surface (API, schema, exported type), is the migration / compatibility story stated?
- [ ] Are the cross-module boundaries respected? (E.g., a UI module does not directly import a database module.)

**Score 90+** when the plan fits the existing architecture cleanly. **60–89** when one principle is bent and the bend has been justified in writing. **< 60** when the plan would introduce a third parallel pattern in the same area.

## Dimension 3 — Evidence quality (weight 20%)

Score whether the plan rests on primary sources or inference.

- [ ] Does the plan cite specific file paths, line ranges, or commit SHAs?
- [ ] Are any external-library claims backed by the current version's docs (not memory of an older version)?
- [ ] Are runtime assumptions (env vars, feature flags, infrastructure) confirmed by reading the config / dashboard, not inferred from naming?
- [ ] If the plan claims "X already works this way," has that been verified in this session (file read or command output)?
- [ ] For bug fixes, has the failing test or reproduction been observed in this session?

**Score 90+** when each material claim has a cited source. **60–89** when the claims are reasonable but uncited. **< 60** when the plan rests on "I remember" or "we usually do X" without a check.

## Dimension 4 — Reuse verified (weight 15%)

Score how thoroughly existing solutions have been searched and considered.

- [ ] Has the codebase been grep'd for similar function names, identifiers, or behavior?
- [ ] Have the project's package manifests (package.json, pyproject.toml, Cargo.toml, etc.) been scanned for libraries that already solve the problem?
- [ ] If a candidate was found, has it been ruled in (use it) or ruled out (named reason for not using)?
- [ ] If 3+ candidates exist, has the choice been justified with a one-line rationale?
- [ ] For UI work, has the project's design system / component library been checked first?

**Score 90+** when at least one search was performed and the result documented. **60–89** when the search was partial or the rationale is vague. **< 60** when no search has been performed and the plan starts with "let's write a new …".

## Dimension 5 — Root cause identified (weight 15%)

For bug fixes:

- [ ] Does the plan name the **why** (the cause), not just the **what** (the symptom)?
- [ ] If a fix candidate was tried before, has the reason for its failure been understood?
- [ ] Does the fix address the cause at its origin (per `ywc-debug-rootcause`), not at a downstream symptom site?

For greenfield work:

- [ ] Does the plan name the underlying user / business need, not just the surface request?
- [ ] If the request is "add screen X", is the reason for X named? (Surface request alone is ≤ 70.)
- [ ] If multiple stakeholders are implied, is the primary one named?

**Score 90+** when the cause / underlying need is named in one sentence. **60–89** when the cause is partly named. **< 60** when only the symptom or surface request appears.

## Worked example — small change

> "Add a NULL check on `user.profile?.avatarUrl` in `ProfileBadge.tsx` to fix the crash reported in #4521."

| Dimension | Score | Evidence |
|---|---|---|
| Scope clarity | 95 | One file, one expression, one symptom (issue #4521); out-of-scope = "do not refactor the rest of the avatar pipeline" |
| Architecture compliance | 95 | NULL-check follows the project's existing `?.` pattern (3 sibling files use it) |
| Evidence quality | 90 | Issue #4521 has the stack trace; `ProfileBadge.tsx:42` is named |
| Reuse verified | 85 | No utility needed; one-line guard is the project's convention |
| Root cause identified | 80 | Surface cause is the missing guard; the deeper "why is `profile` ever null here?" is a known case (logged-out impersonation), documented in the issue |
| **Aggregate** | **91** → **PROCEED** | |

## Worked example — medium change

> "Add a new Auth provider (Magic Link) alongside the existing Google OAuth."

| Dimension | Score | Evidence |
|---|---|---|
| Scope clarity | 75 | "Magic Link" is named; "alongside Google" implies parallel; the Out of Scope ("does it replace password reset? does it impact session length?") was not explicit |
| Architecture compliance | 70 | The Auth module has one provider pattern; a second provider needs the strategy abstraction extracted first |
| Evidence quality | 60 | Plan cites "Magic Link is how Slack does it" but no specific RFC / provider library was confirmed |
| Reuse verified | 45 | No search has been done for existing magic-link libraries; "we'll write it" is the current plan |
| Root cause identified | 80 | Underlying need (login for users without a Google account) is named |
| **Aggregate** | **67** → **STOP** (aggregate alone already STOPs; Reuse verified at 45 is also `< 50`, which independently forces a one-level downgrade) | |

**Routing**: STOP back to `ywc-tech-research` to pick a magic-link library, then `ywc-plan` to revise the architecture for the second provider.

## Anti-pattern recall

(Echoes the shared rubric's §7. Listed here so the pre-implementation moment has them within reach.)

- Rounding up to clear the threshold.
- Scoring after the fact to justify a decision already made.
- Reporting only the aggregate without per-dimension breakdown.
- Adding a 6th dimension because "my work has a unique aspect".
- Inheriting confidence from an upstream skill instead of re-scoring at the boundary.
