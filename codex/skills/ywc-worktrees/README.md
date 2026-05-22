# ywc-worktrees

`ywc-parallel-executor` 와 `ywc-finish-branch` 에서 호출되는 git worktree
lifecycle 관리 skill. Worktree priority resolution (`.worktrees/` > CLAUDE.md
`worktree_root` > `--root` fallback) 의 single source 입니다.

## Modes

- `--mode resolve` — Worktree 가 land 할 path 만 출력 (side effect 없음)
- `--mode create` — `git worktree add` 실행 + path 검증
- `--mode audit` — Stale / leaked / missing worktree 탐지 (Pre-flight 또는
  wave 종료 시)
- `--mode prune` — Post-merge cleanup (`git worktree remove` + local branch
  delete + `git worktree prune` + verify)

상세 argument table 과 priority chain 은 [SKILL.md](./SKILL.md) 를 참조하십시오.

## Bundled Scripts

| Script | Purpose |
|---|---|
| `scripts/audit-worktrees.sh` | `--mode audit` 의 핵심 검증 logic |
| `scripts/cleanup-worktree.sh` | `--mode prune` 의 핵심 cleanup + branch deletion logic |

두 script 는 이 skill 아래에 centralized 되어 caller 가 서로 다른 worktree
audit / cleanup logic 을 유지하지 않도록 합니다.

## Design Source

[superpowers / using-git-worktrees](https://github.com/anthropic-experimental/superpowers)
skill 의 priority resolution + 4-mode interface 패턴 adaptation. 이 프로젝트는
self-contained runtime 정책이므로 superpowers skill 은 runtime dispatch 가
아닌 **design inspiration** 으로만 인용합니다.

## Integration

- **upstream**: [`ywc-parallel-executor`](../ywc-parallel-executor/) (Pre-flight
  audit, Step 4 per-task create, Step 4g prune), [`ywc-finish-branch`](../ywc-finish-branch/)
  (Step 5 / 8 cleanup)
- **downstream**: 없음 (leaf operation skill)

## Bundle Scope

이 Codex skill 은 Claude Code 대응 skill 과 같은 worktree lifecycle contract 를
따르되, Codex bundle 경로(`codex/skills/ywc-worktrees/`) 안의 script 와 metadata
를 기준으로 유지됩니다.
