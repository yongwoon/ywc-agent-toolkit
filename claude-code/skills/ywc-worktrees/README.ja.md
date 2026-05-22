# ywc-worktrees

`ywc-parallel-executor` と `ywc-finish-branch` から呼び出される git worktree
lifecycle 管理 skill。Worktree priority resolution (`.worktrees/` > CLAUDE.md
`worktree_root` > `--root` fallback) の single source です。

## Modes

- `--mode resolve` — worktree が land する path のみ出力 (side effect なし)
- `--mode create` — `git worktree add` 実行 + path 検証
- `--mode audit` — Stale / leaked / missing worktree の検出 (Pre-flight
  または wave 終了時)
- `--mode prune` — Post-merge cleanup (`git worktree remove` + local branch
  delete + `git worktree prune` + verify)

argument table と priority chain の詳細は [SKILL.md](./SKILL.md) を参照して
ください。

## Bundled Scripts

| Script | Purpose |
|---|---|
| `scripts/audit-worktrees.sh` | `--mode audit` の核となる検証 logic |
| `scripts/cleanup-worktree.sh` | `--mode prune` の核となる cleanup + branch deletion logic |

両 script は `ywc-parallel-executor/scripts/` から `git mv` で移動され、
history が保持されています。

## Design Source

[superpowers / using-git-worktrees](https://github.com/anthropic-experimental/superpowers)
skill の priority resolution + 4-mode interface パターンを adapt したもの。
本プロジェクトは self-contained runtime ポリシーであるため、superpowers
skill は runtime dispatch ではなく **design inspiration** としてのみ引用
しています。

## Integration

- **upstream**: [`ywc-parallel-executor`](../ywc-parallel-executor/)
  (Pre-flight audit、Step 4 per-task create、Step 4g prune)、
  [`ywc-finish-branch`](../ywc-finish-branch/) (Step 5 / 8 cleanup)
- **downstream**: なし (leaf operation skill)

## 3-Root Sync

この skill は universal worktree management 機能のため、3 root (claude-code
/ codex-skill / pi-skills) 全てに同一内容で sync されます。`is_diverged()`
対象外です。
