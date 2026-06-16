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
  delete または `--keep-branch` preserve + `git worktree prune` + verify)

## `--keep-branch`

`--keep-branch` は prune 専用です。worktree と stale metadata を削除しつつ
`--branch` を保持します。Non-aggregate `ywc-sequential-executor --worktree`
は run worktree cleanup 後に accumulated integration branch を残すために
この option を使用します。

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

## Root メンテナンス

この skill は universal worktree management 機能のため、claude-code と
codex-skill 両方に同一内容で維持します。auto-sync は廃止され、各 root を
独立して管理します。
