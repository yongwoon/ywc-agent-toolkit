# yk-000004-020-domain-finish-branch-remote-guard

## Purpose
Port the 'Remote deletion guard' so `ywc-finish-branch` checks for open PRs before any remote branch deletion and uses a strict 'merged' test (AC4).

Spec item: A3 (#346) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- Add the snapshot 'Remote deletion guard' paragraph at the local remote-deletion point (Step 5, near `gh pr merge --delete-branch`) so the open-PR check is written BEFORE any deletion command.
- Rules (snapshot text, in full): remote deletion only via `gh pr merge --delete-branch`; any other remote deletion (`git push origin --delete "$branch"`, even when the user asks) requires `gh pr list --head "$branch" --state open` to succeed AND parse to empty (non-empty → stop and report; command/parse failure → `BLOCKED` or `NEEDS_CONTEXT`); branch name passes `git check-ref-format --branch "$branch"` and is only passed as a quoted variable.
- Same paragraph's 'merged' rule: `gh pr list --head "$branch" --state merged --json number,baseRefName,headRefOid` where `baseRefName` is the intended base and `headRefOid` equals the `git ls-remote origin "refs/heads/$branch"` tip; otherwise stop and report; never use `git branch -r --merged HEAD`.
- Port Rationalization Defense row 1 (`:28`). Do NOT add a separate stacked-PR `--base` open check.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 3 (A3), AC4, Critical Surfaces, Failure Modes row 'finish-branch remote deletion'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-finish-branch/SKILL.md` — upstream `:369` guard paragraph and `:28` row (T0 snapshot)

### Summary
Remote branch deletion is the one path that can silently close another open PR (stacked PRs). The guard makes the open-PR check precede every deletion and treats unverifiable results as blocked, never as safe.

### Out of Scope (from spec)
- Stacked-PR `--base` open check (explicitly not added)
- `ywc-finish-branch/scripts/mark-task-complete.sh` (installed-bundle-only file; guard does not depend on it)
- Other finish-branch edits — B2 later rewrites script paths in the same file

## Criticality
critical — Spec Critical Surface: remote branch deletion must never auto-close an open PR.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream `ywc-finish-branch/SKILL.md`

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-finish-branch/SKILL.md` — Remote deletion guard paragraph, Rationalization Defense row 1

## Notes
- Local file is ~336 lines; no extraction needed.
- Failure statuses must match the Scope: `BLOCKED` or `NEEDS_CONTEXT`.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-finish-branch/SKILL.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Delivery contract: remote branch deletion semantics

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`

### Task Verify
- `[ "$(grep -c 'gh pr list --head' claude-code/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" -ge 2 ]`
- `[ "$(grep -c -- 'Remote deletion guard' claude-code/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 1 ]`
- `grep -q 'check-ref-format' claude-code/skills/ywc-finish-branch/SKILL.md`
- `grep -q 'headRefOid' claude-code/skills/ywc-finish-branch/SKILL.md`
- `python3 -c "t=open('claude-code/skills/ywc-finish-branch/SKILL.md',encoding='utf-8').read(); g=t.index('Remote deletion guard'); d=t.find('git push origin --delete'); assert d==-1 or g<d"` (guard text precedes any explicit deletion command)
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
