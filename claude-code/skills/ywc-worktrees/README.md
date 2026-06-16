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
  delete + `git worktree prune` + verify). `--keep-branch` flag 를 주면 worktree
  만 제거하고 local branch 는 보존합니다 (예: integration branch 를 최종 trunk PR
  용으로 남길 때).

상세 argument table 과 priority chain 은 [SKILL.md](./SKILL.md) 를 참조하십시오.

## Bundled Scripts

| Script | Purpose |
|---|---|
| `scripts/audit-worktrees.sh` | `--mode audit` 의 핵심 검증 logic |
| `scripts/cleanup-worktree.sh` | `--mode prune` 의 핵심 cleanup + branch deletion logic |

두 script 는 `ywc-parallel-executor/scripts/` 에서 `git mv` 로 이전되어 history 가 보존되었습니다.

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

## 3-Root Sync

이 skill 은 universal worktree management 기능이므로 3 root (claude-code /
codex-skill / pi-skills) 모두에 동일 내용으로 sync 됩니다. `is_diverged()`
대상이 아닙니다.
