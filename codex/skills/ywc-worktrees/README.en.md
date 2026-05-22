# ywc-worktrees

Git worktree lifecycle management skill. Single source of truth for worktree
priority resolution (`.worktrees/` > CLAUDE.md `worktree_root` >
`--root` fallback), invoked by `ywc-parallel-executor` and
`ywc-finish-branch`.

## Modes

- `--mode resolve` — print the path where a worktree would land (no side
  effects)
- `--mode create` — run `git worktree add` and verify registration
- `--mode audit` — detect stale / leaked / missing worktrees (Pre-flight or
  wave-end)
- `--mode prune` — post-merge cleanup (`git worktree remove` + local branch
  delete + `git worktree prune` + verify)

For the full argument table and priority resolution chain, see
[SKILL.md](./SKILL.md).

## Bundled Scripts

| Script | Purpose |
|---|---|
| `scripts/audit-worktrees.sh` | Core audit logic for `--mode audit` |
| `scripts/cleanup-worktree.sh` | Core cleanup and branch deletion logic for `--mode prune` |

Both scripts were moved from `ywc-parallel-executor/scripts/` via `git mv` to
preserve their commit history.

## Design Source

Adapted from the
[superpowers / using-git-worktrees](https://github.com/anthropic-experimental/superpowers)
skill — the priority resolution chain and the four-mode interface follow
that pattern. This project's self-contained runtime policy means the
superpowers skill is referenced for design intent only; it is **not**
dispatched at runtime.

## Integration

- **upstream**: [`ywc-parallel-executor`](../ywc-parallel-executor/)
  (Pre-flight audit, Step 4 per-task create, Step 4g prune),
  [`ywc-finish-branch`](../ywc-finish-branch/) (Step 5 / 8 cleanup)
- **downstream**: none (leaf-operation skill)

## 3-Root Sync

This skill ships identical content to all three skill roots (claude-code,
codex-skill, pi-skills) because worktree management is a universal feature.
It is **not** in `is_diverged()`.
