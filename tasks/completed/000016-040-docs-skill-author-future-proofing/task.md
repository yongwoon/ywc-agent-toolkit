# 000016-040-docs-skill-author-future-proofing — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000016-010-docs-principles-guideline-gap` is completed (merged).

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-skill-author/SKILL.md`.
- [ ] Stay within `codex/skills/ywc-skill-author/references/rationalization-defense-cookbook.md` and `codex/skills/ywc-skill-author/references/skill-template.md` if examples/templates need updates.
- [ ] Only create `codex/skills/ywc-skill-author/evals/evals.json` if local eval conventions support it.

## Stop Conditions
- [ ] Stop if the change would rewrite unrelated skill-author workflows.
- [ ] Stop if examples become generic boilerplate instead of domain-specific failure defenses.
- [ ] Stop if adding an eval would require changing the global eval harness.

## Implementation Steps
- [ ] Add a mandatory rule in `codex/skills/ywc-skill-author/SKILL.md` requiring domain-specific Rationalization Defense rows for missing context, adjacent cleanup, overbuilding, and completion without goal-specific verification.
  - Related AC/FR: AC6, FR-4
  - Contract / Behavior Change: future skills must encode concrete failure modes rather than slogans.
  - Verification Command / Evidence: `rg -n "domain-specific|missing context|adjacent cleanup|overbuilding|goal-specific verification" codex/skills/ywc-skill-author/SKILL.md`
- [ ] Add acceptable/unacceptable examples either in `SKILL.md` or `references/rationalization-defense-cookbook.md`.
  - Related AC/FR: AC6, FR-4
  - Contract / Behavior Change: authors can distinguish concrete operational defenses from generic boilerplate.
  - Verification Command / Evidence: `rg -n "Acceptable|Unacceptable|generic|domain-specific" codex/skills/ywc-skill-author`
- [ ] Update `references/skill-template.md` if the template currently omits the new Rationalization Defense expectation.
  - Related AC/FR: AC6, FR-4
  - Contract / Behavior Change: generated skill drafts inherit the stricter authoring rule.
  - Verification Command / Evidence: `rg -n "Rationalization Defense|domain-specific" codex/skills/ywc-skill-author/references/skill-template.md`
- [ ] Inspect whether a `ywc-skill-author` eval is supported; add one only if objective and consistent with local conventions.
  - Related AC/FR: AC9, FR-6
  - Contract / Behavior Change: eval coverage exists or omission is explicitly justified.
  - Verification Command / Evidence: implementation final report states eval added or why omitted.

## Task Verify
- [ ] Run `rg -n "domain-specific|missing context|adjacent cleanup|overbuilding|goal-specific verification|generic" codex/skills/ywc-skill-author`.
- [ ] Run `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-skill-author --format json || true` and report whether the skill has eval support.

## Verification
- [ ] Targeted grep checks pass.
- [ ] Eval support decision is documented.
- [ ] Full repository validation is deferred to `000017-010-infra-codex-karpathy-validation`.
