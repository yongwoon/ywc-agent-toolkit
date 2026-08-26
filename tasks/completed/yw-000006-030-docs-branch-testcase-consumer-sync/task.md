# yw-000006-030-docs-branch-testcase-consumer-sync — Implementation Checklist

## Prerequisites
- [ ] `yw-000005-020-docs-task-generator-skill-initials` is completed and merged.
- [ ] `yw-000004-020-infra-parser-optional-initials-prefix` is merged, so `build-pr-title.py` already accepts prefixed IDs.

## Allowed Edit Scope
- [ ] Modify only `SKILL.md` and `README*.md` under `ywc-finish-branch` and `ywc-gen-testcase`. Do not touch `scripts/` or `references/`.

## Stop Conditions
- [ ] Stop if `build-pr-title.py` appears to need a change — that belongs to `yw-000004-020` and indicates a gap in that task.
- [ ] Stop if a skill would be left with prefixed examples only and no legacy example.

## Hardening Gate
- [ ] Confirm no `.py` or `.sh` file appears in the diff.
- [ ] Confirm each skill retains one legacy unprefixed example.
- [ ] Mark Data Integrity Hardening N/A — documentation only.

## Implementation Steps
- [ ] Re-grep both skills for task-ID-shaped examples (`[0-9]\{6\}-[0-9]\{3\}`) to build the actual edit list.
- [ ] Update `ywc-finish-branch/SKILL.md` task-ID, branch, and PR-title-prefix examples to the prefixed form, keeping one legacy example.
- [ ] Add one sentence to `ywc-finish-branch/SKILL.md` stating that the PR-title prefix carries the initials segment when present and is unchanged for legacy IDs.
- [ ] Update `ywc-gen-testcase/SKILL.md` task-ID examples to the prefixed form, keeping one legacy example, and add one sentence noting that both forms are accepted.
- [ ] Update all six README locales for `ywc-finish-branch` with the same substantive change.
- [ ] Update all six README locales for `ywc-gen-testcase`.
- [ ] Confirm no script file entered the diff.

## Task Verify
- [ ] `git diff --name-only | grep -c '\.py$\|\.sh$'` returns 0
- [ ] `git diff --name-only | wc -l` equals 14
- [ ] Both `SKILL.md` files contain a `yk-` example and a legacy unprefixed example
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] markdownlint passes with the CI config and scope
- [ ] typecheck passes (N/A — documentation only)
- [ ] unit tests pass (N/A — no executable change)
- [ ] app builds without error (N/A — documentation/tooling repository)
