# yw-000005-020-docs-task-generator-skill-initials — Implementation Checklist

## Prerequisites
- [ ] `yw-000005-010-infra-next-task-number-initials-scan` is completed and merged.
- [ ] `claude-code/skills/references/initials-resolution.md` exists on the base branch.

## Allowed Edit Scope
- [ ] Modify only `claude-code/skills/ywc-task-generator/SKILL.md`.

## Stop Conditions
- [ ] Stop if the edit would push SKILL.md past ~500 lines — move the surplus into `references/initials-resolution.md` in a follow-up instead.
- [ ] Stop if the precedence chain, derivation algorithm, or canonical section format would have to be restated in the skill body (NFR3 violation).
- [ ] Stop if the resolution step would block execution when no initials source exists.

## Hardening Gate
- [ ] Record the SKILL.md line count before and after the edit.
- [ ] Record the AC1 idempotency evidence (exactly one `## Task Initials` section after two runs).
- [ ] Record the three AC10 precedence observations.

## Implementation Steps
- [ ] Record `wc -l claude-code/skills/ywc-task-generator/SKILL.md` (currently 434) as the length baseline.
- [ ] Add an `--initials <value>` row to the Arguments table, documenting `^[a-z0-9]{2,4}$` validation and that it takes highest precedence.
- [ ] Add "Resolve collaborator initials first" as the opening item of Step 2, stating it runs on **every** invocation regardless of whether tasks already exist, because Step 7 naming always requires the segment.
- [ ] Insert a `> **Action required**: Read [../references/initials-resolution.md](../references/initials-resolution.md)` directive at that point, following the pattern used for `lang-resolution.md`, and reference the file by path without any `@skill-name` force-load.
- [ ] State in Step 2 that caching writes `## Task Initials` to the project `CLAUDE.md` with create-or-replace semantics, and that append is forbidden.
- [ ] State in Step 2 that the confirmation prompt includes the disk-scanned list of initials already in use, with counts, and that a match warns without blocking.
- [ ] Update the Step 2 numbering-scan description to cite `next-task-number.sh [tasks-dir] [initials]`, the initials-scoped comparison, the worktree union, the legacy seed rule, and the atomic reservation — as citations only, with the rule bodies left in the script comments and the reference.
- [ ] Add the Rationalization Defense row: *"This repository has one user, so initials are overkill"* → *"The moment a second worktree exists, the collision happens silently with no merge conflict; a one-time question costs nothing, skipping it costs unrecoverable numbering ambiguity."*
- [ ] Update the Step 7 Task Naming section to define the format as `[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`, with `INITIALS` as 2–4 lowercase alphanumeric characters, and update every worked example to the prefixed form (`yk-000001-010-db-create-user-table`).
- [ ] State explicitly in Step 7 that legacy unprefixed IDs remain valid and are never renumbered retroactively.
- [ ] Add two rows to the Step 12 Final Validation checklist: INITIALS matches the resolved value and the full segment widths are correct; and exactly one `## Task Initials` section exists in the project `CLAUDE.md`.
- [ ] Re-measure the line count and confirm it remains at or below 500; if not, move the newest prose into the reference.
- [ ] Verify AC1 on a scratch copy: run twice and confirm `grep -c '^## Task Initials'` returns 1 both times, with no second derivation or question.
- [ ] Verify AC10 on a scratch copy across all three states: `--initials ab` overrides a cached `yk`; a cached section alone suppresses derivation; neither present triggers derivation plus exactly one confirmation.

## Task Verify
- [ ] `test "$(wc -l < claude-code/skills/ywc-task-generator/SKILL.md)" -le 500`
- [ ] `grep -q 'initials-resolution.md' claude-code/skills/ywc-task-generator/SKILL.md`
- [ ] `grep -c '@ywc-' claude-code/skills/ywc-task-generator/SKILL.md` returns 0
- [ ] AC1 scratch run: exactly one `## Task Initials` section after two consecutive runs
- [ ] AC10 scratch runs: all three precedence states produce the expected prefix

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] markdownlint passes with the CI config and scope
- [ ] typecheck passes (N/A — documentation only)
- [ ] unit tests pass (N/A — covered by the eval scenario in `yw-000006-010`)
- [ ] app builds without error (N/A — documentation/tooling repository)
