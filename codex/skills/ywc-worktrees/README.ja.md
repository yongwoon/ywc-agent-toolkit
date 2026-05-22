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

両 script はこの skill 配下に centralized され、caller 側が divergent な
worktree audit / cleanup logic を持たないようにします。

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

## Bundle Scope

この Codex skill は Claude Code 側の対応 skill と同じ worktree lifecycle
contract に従いつつ、Codex bundle path
(`codex/skills/ywc-worktrees/`) の script と metadata を基準に保守します。
