# yk-000006-030-domain-handle-pr-reviews-worktree

## Purpose
Add `--worktree` to `ywc-handle-pr-reviews` so review feedback is handled in an isolated worktree created only through `ywc-worktrees` (AC16b).

Spec item: C3 (#347) of `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md`.

## Scope
- New `## Arguments` section and Step 1.5 'Worktree Setup': PR number must match `^[0-9]+$` (else `BLOCKED: PR number must be numeric`); head branch validated with the C2 rules; `isCrossRepository` true (fork PR) or non-OPEN PR → `BLOCKED`.
- Decide `in-place` / `created` / reuse of an existing worktree; require a clean tree; refresh remote; re-confirm cwd.
- Worktrees only via `ywc-worktrees --mode create --existing-branch` (no inline `git worktree add`; skill missing → `BLOCKED`), with `--task-name pr-<N>`.
- Step 9 prune guidance must pass `--keep-branch` so the PR head branch is not deleted.
- Rationalization Defense (2 rows), `cross-skill-graph.md` entry, `claude-code/skills/CLAUDE.md` pair row handle-pr-reviews→worktrees, four Tier 1 READMEs.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261105-claude-upstream-issue-69-port.md` — `## Scope` item 16 (C3), AC16b, Critical Surfaces, Failure Modes rows on malicious input and fork PR
- `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-handle-pr-reviews/SKILL.md` — upstream Step 1.5 (T0 snapshot)

### Summary
A PR head branch and PR number come from GitHub and must be validated before they reach a shell. Fork PRs point at another repository's branch and are refused. Worktree creation is delegated to the C2 flag so there is one validated code path.

### Out of Scope (from spec)
- Worktree creation logic (C2)
- Fixing fork PRs by cloning the fork

## Criticality
critical — Spec Critical Surface: remote-controlled PR head branch name enters shell commands and creates worktrees.

## Dependencies

### Depends On
- `yk-000003-010-config-upstream-snapshot` — snapshot of upstream handle-pr-reviews text
- `yk-000006-020-domain-worktrees-existing-branch` — provides `ywc-worktrees --existing-branch`

### Depended By
- (None)

## Key Files
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md` — Arguments, Step 1.5, Step 9, Rationalization Defense
- `claude-code/skills/ywc-handle-pr-reviews/README{,.en,.ja,.ko}.md` — flag docs
- `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md` — edge
- `claude-code/skills/CLAUDE.md` — pair table row
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — baseline

## Notes
- `ywc-handle-pr-reviews/SKILL.md` ~255 lines → ~310; B2 already ran on this file.

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-handle-pr-reviews/**`
- `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md`
- `claude-code/skills/CLAUDE.md` (pair table row)

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `ywc-worktrees` CLI contract
- `claude-code/skills/CLAUDE.md` pair table
- `cross-skill-graph.md`

### Conflicts With
- (None identified)

### Parallelizable After
- `yk-000003-010-config-upstream-snapshot`
- `yk-000006-020-domain-worktrees-existing-branch`

### Task Verify
- `grep -q 'Step 1.5' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `grep -q 'isCrossRepository' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `grep -qF '^[0-9]+$' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `grep -q -- '--keep-branch' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `[ "$(grep -c 'git worktree add' claude-code/skills/ywc-handle-pr-reviews/SKILL.md | tr -d ' ')" = 0 ]`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-handle-pr-reviews/SKILL.md`

## Out of Scope
Anything not listed in Scope, regardless of what the specification mentions elsewhere. In particular: Codex files (`codex/`, `plugins/ywc-agent-toolkit`), `README.zh.md` / `README.es.md` retranslation, validator gates for the script-path rule, and whole-file copies of snapshot content (port only the hunks named in Scope).
