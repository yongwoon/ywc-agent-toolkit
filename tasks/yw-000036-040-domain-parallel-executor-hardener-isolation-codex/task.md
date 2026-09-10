# yw-000036-040-domain-parallel-executor-hardener-isolation-codex — Implementation Checklist

## Prerequisites
- [ ] `yw-000036-020-domain-parallel-executor-codex-state-schema` is completed (merged).
- [ ] `yw-000036-030-domain-parallel-executor-hardener-isolation-claude` is completed (merged) — read its final `SKILL.md` diff for the settled branch-name form and promotion-step label to mirror.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `codex/skills/ywc-parallel-executor/SKILL.md`, `references/wave-integration-branch.md` (new).

## Stop Conditions
- [ ] Stop if `4e.5`'s heading position and step number already agree with each other (contradiction already resolved by other work).
- [ ] Stop if implementing this task requires changing `codex/skills/ywc-parallel-executor/SKILL.md:278-280` (`4c.5`/`4c.6` per-task gate logic) beyond citation — that logic is unaffected and out of scope.
- [ ] Stop if the required body growth would push the file meaningfully further over its ~504-line soft-cap overage — move more content into the new reference file.
- [ ] Stop if `yw-000036-030`'s final branch-name form or promotion-step label cannot be determined from its merged diff.

## Implementation Steps
- [ ] **Pre-flight scan** (codex idiom, generic worker terminology): mirror `yw-000036-030`'s Pre-flight subsection — per-wave `has_contract` OR-scan across member tasks' `quality_gate_contract` field, `NEEDS_CONTEXT` on missing/malformed/absent-directory cases, threaded into `init-parallel --waves`.
- [ ] **`4e` amendment**: create `wave-int/<N>` iff `integration_branch` is non-`None` post-Pre-flight; idempotent reuse; push-at-creation using `codex/skills/ywc-sequential-executor/references/aggregate-pr.md`'s `$WORK_BRANCH` push-at-creation idiom (not the claude-code file's); extend the mode-mapping rows with `--base-branch wave-int/<N>`.
- [ ] **Resolve the `4e.5` numbering/placement contradiction**: renumber/relocate so the heading position agrees with its "Before delivery" prose intent, keeping the existing dispatch-eligibility rules (`4c.5`/`4c.6`, bounded packets, `enforced`/`advisory`/`report-only`) intact — this is a placement fix, not a rewrite of the gate logic itself.
- [ ] **New promotion step**: same semantics as `yw-000036-030`'s (fast-forward on pass, merge-base-and-rerun on fast-forward failure never rebase, two-counter bound, `HEAD` postcondition, `wave-complete` stamped only after success, blocking-gate preservation behavior, dispatch-failure-still-allows-promotion).
- [ ] **Carve-out rule and `--per-task-pr` advisory cap**: same rule statement as `yw-000036-030`; express the advisory cap using codex's existing `report-only`/`advisory`/`enforced` vocabulary directly (this fits naturally per FR-8) rather than inventing new terms.
- [ ] **Step 4i third bucket**: mirror `yw-000036-030`'s addition, in codex idiom.
- [ ] **New `references/wave-integration-branch.md`** (codex idiom): lifecycle, promotion procedure, conflict handling — link via `> **Action required**: Read [...]`.

## Task Verify
- [ ] `grep -n "^\*\*4[a-z]" codex/skills/ywc-parallel-executor/SKILL.md` — confirm ascending step-number/heading-position agreement, no remaining "Before delivery" vs. number contradiction.
- [ ] `grep -n "wave-int/" codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] `grep -c "isolation branch can only protect state whose point-of-no-return" codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] `grep -n "Hardener-BLOCKED\|hardener.*blocked" codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] Confirm no Claude-only frontmatter field was introduced in any touched/created file (`name`/`description` only).

## Verification
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] `git diff --stat plugins/ywc-agent-toolkit/skills` shows changes only in files the sync script produces (run the sync via the pre-commit hook path, do not hand-edit).
- [ ] No lint/typecheck/build/test toolchain applies to this repository beyond `scripts/validate.sh`.

## Implementation Notes (optional)
