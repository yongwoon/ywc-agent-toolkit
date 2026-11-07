# yk-000006-020-domain-worktrees-existing-branch

## Purpose
Add `--existing-branch` to `ywc-worktrees` create mode with strict branch-name validation (AC16).

Spec item: C2 (#347) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- Value-less flag `--existing-branch`: checkout the branch named by `--branch`; local branch checked out, origin-only branch gets a tracking branch; mutually exclusive with `--base-branch` (both or neither → exit 1 usage error); `--base-branch` required only when `--existing-branch` is absent.
- Branch-name validation before any `ls-remote` / `fetch` / `worktree add`: `^[A-Za-z0-9._/-]+$`, no leading `-`, no `..`, `git check-ref-format "refs/heads/<branch>"` success; otherwise `invalid branch name`, exit 1; quote every branch argument.
- Update Arguments, Modes table, Error handling and four Tier 1 READMEs (Tier 2 per policy). `--keep-branch` and `prune` already exist and stay unchanged.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 15 (C2), AC16, Failure Modes 'malicious branch name'
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-worktrees/SKILL.md` — upstream `:49-50`, `:129` (T0 snapshot)

### Summary
C3 needs a way to attach a worktree to an existing PR head branch without creating a new one. The remote-supplied branch name is untrusted, so validation precedes every git call.

### Out of Scope (from spec)
- PR-specific logic (C3)
- Changes to `--keep-branch` / `prune`

## Criticality
normal — Per spec only `ywc-handle-pr-reviews --worktree` (C3) is a Critical Surface; NOTE: this task defines the branch-name validation C3 relies on, so a reviewer should still check it closely.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream `ywc-worktrees`
- `yk-000006-010-domain-agent-description-alignment` — serializes the baseline file (B-chain → C1 → C2)

### Depended By
- `yk-000006-030-domain-handle-pr-reviews-worktree` — needs the output of this task

## Key Files
- `claude-code/skills/ywc-worktrees/SKILL.md` — Arguments, Modes, validation, Error handling
- `claude-code/skills/ywc-worktrees/README{,.en,.ja,.ko}.md` — flag docs
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — baseline

## Notes
- `ywc-worktrees/SKILL.md:95` (`git worktree add … -b`) remains the create-new-branch path.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (no M1 trigger: Owned Interface is None; no M2: Ownership is not docs-only per include list)

### Ownership
- `claude-code/skills/ywc-worktrees/**`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- Contract: `ywc-worktrees --mode create` flags used by `ywc-handle-pr-reviews`, `ywc-parallel-executor`

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000006-010-domain-agent-description-alignment`

### Task Verify
- `[ "$(grep -c -- '--existing-branch' claude-code/skills/ywc-worktrees/SKILL.md | tr -d ' ')" -ge 3 ]`
- `grep -q 'check-ref-format' claude-code/skills/ywc-worktrees/SKILL.md`
- `grep -q 'invalid branch name' claude-code/skills/ywc-worktrees/SKILL.md`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-worktrees/SKILL.md`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
