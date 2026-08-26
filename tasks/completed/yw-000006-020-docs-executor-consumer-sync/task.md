# yw-000006-020-docs-executor-consumer-sync — Implementation Checklist

## Prerequisites
- [ ] `yw-000005-020-docs-task-generator-skill-initials` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only `SKILL.md` and `README*.md` under `ywc-sequential-executor`, `ywc-parallel-executor`, and `ywc-worktrees`. Do not touch `scripts/` or `references/` in any of them.

## Stop Conditions
- [ ] Stop if a logic change (not an example change) appears necessary — that would contradict the spec's grep evidence and needs re-scoping.
- [ ] Stop if a skill would be left with prefixed examples only and no legacy example.

## Hardening Gate
- [ ] Confirm no file under `scripts/` or `references/` appears in the diff.
- [ ] Confirm each of the three skills retains one legacy unprefixed example.
- [ ] Mark Data Integrity Hardening N/A — documentation only.

## Implementation Steps
- [ ] Re-grep each of the three skills for task-ID-shaped examples (`[0-9]\{6\}-[0-9]\{3\}`) to build the actual edit list rather than relying on the spec's line numbers alone.
- [ ] Update `ywc-sequential-executor/SKILL.md` task-specifier and branch examples to the prefixed form, keeping one legacy example.
- [ ] Add one sentence to `ywc-sequential-executor/SKILL.md` stating that task specifiers are matched as plain string prefixes, so an initials segment passes through unchanged and legacy unprefixed IDs continue to match.
- [ ] Apply the same example update and one-sentence note to `ywc-parallel-executor/SKILL.md`, mentioning that worktree names carry the task name verbatim.
- [ ] Apply the same example update and one-sentence note to `ywc-worktrees/SKILL.md`, and confirm `feature/yk-000001-010-…` is shown as a valid branch name.
- [ ] Update all six README locales for `ywc-sequential-executor` with the same substantive change.
- [ ] Update all six README locales for `ywc-parallel-executor`.
- [ ] Update all six README locales for `ywc-worktrees`.
- [ ] Confirm no `scripts/` or `references/` file entered the diff.

## Task Verify
- [ ] `git diff --name-only | grep -c 'scripts/\|references/'` returns 0
- [ ] `git diff --name-only | wc -l` equals 21
- [ ] Each of the three `SKILL.md` files contains both a `yk-` example and a legacy unprefixed example
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] markdownlint passes with the CI config and scope
- [ ] typecheck passes (N/A — documentation only)
- [ ] unit tests pass (N/A — no executable change)
- [ ] app builds without error (N/A — documentation/tooling repository)
