# yw-000013-020-docs-condition-gate-directives — Implementation Checklist

## Prerequisites

- [ ] `yw-000012-020` is completed (merged)
- [ ] `yw-000012-030` is completed (merged)

## Allowed Edit Scope

- [ ] Stay within the 8 `SKILL.md` files listed in README.md Key Files
- [ ] Do not touch the language/initials directives in `ywc-auth-implement` or `ywc-create-pr` — those are `yw-000013-010`'s scope even though both tasks touch these two files

## Stop Conditions

- [ ] Stop if a directive is reachable by an entry path this task's enumeration missed (E10) — report the missed path rather than shipping a partial gate
- [ ] Stop if gating a directive would change observable behavior (e.g. a branch that's supposed to always read the reference stops reading it) — NFR5 requires every directive's content stay reachable at the branch that needs it

## Implementation Steps

- [ ] Verify `ywc-sequential-executor/SKILL.md:78` against the amended AC7 regex (should already pass, no edit) — use as the shape template for the rest
- [ ] Condition-gate `ywc-auth-implement/SKILL.md:46,56,62,142` — for each, add the branch/step condition (e.g. "when running the policy interview", "when the generic fallback path is taken")
- [ ] Condition-gate `ywc-docker-isolate/SKILL.md:103,105`
- [ ] Condition-gate `ywc-create-pr/SKILL.md:351,369` (bot polling / PR conflict — only fires once CI has passed and a merge is attempted)
- [ ] Condition-gate `ywc-handle-pr-reviews/SKILL.md:224`, `ywc-merge-dependabot/SKILL.md:185`
- [ ] Verify `ywc-finish-branch/SKILL.md:156,196` and `ywc-parallel-executor/SKILL.md:88` and `ywc-sequential-executor/SKILL.md:203` already satisfy the amended AC7 regex (likely no edit — confirm, don't assume)
- [ ] Condition-gate `ywc-parallel-executor/SKILL.md:419` with an explicit "when `--draft` or `--aggregate-pr` is set" prefix — this one is currently unconditioned
- [ ] Condition-gate `ywc-sequential-executor/SKILL.md:126`
- [ ] For every directive touched, enumerate all entry paths into its consuming branch (E10) and confirm the gate holds on each path, not just the one being edited

## Task Verify

- [ ] `grep -rh 'Action required' claude-code/skills/*/SKILL.md | grep -vcE '\b(when|before|if|only)\b'` returns `0`

## Verification

- [ ] `bash scripts/validate.sh` exits 0
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/<each of the 8 dirs>` exits 0 for each

## Implementation Notes (optional)
