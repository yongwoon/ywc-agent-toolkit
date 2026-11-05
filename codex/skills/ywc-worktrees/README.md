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
  delete or `--keep-branch` preserve + `git worktree prune` + verify)

## `--keep-branch`

`--keep-branch` is prune-only. It removes the worktree and stale metadata while
preserving `--branch`; non-aggregate `ywc-sequential-executor --worktree` uses
it to keep the accumulated integration branch after run worktree cleanup.

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

## Root 관리

Claude Code와 Codex의 worktree 지침은 각 소스 루트에서 독립적으로 관리합니다.
자동 플랫폼 간 동기화는 없으며, Codex 배포 패키지는 Codex 소스에서 생성합니다.

## 기존 브랜치와 PR worktree

`create`는 `--base-branch` 또는 `--existing-branch <H>` 중 하나를 받습니다. 기존 브랜치는 정확한 local/origin ref만 사용하고, 미존재와 전송 실패·다른 checkout·dirty·locked 상태를 구분해 중단합니다.
