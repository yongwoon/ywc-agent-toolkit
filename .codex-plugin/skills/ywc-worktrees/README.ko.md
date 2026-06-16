# ywc-worktrees (요약)

`ywc-parallel-executor` 와 `ywc-finish-branch` 에서 호출되는 worktree
lifecycle 관리 skill 의 한국어 요약본. 전체 문서는 [SKILL.md](./SKILL.md),
사용 가이드는 [README.md](./README.md) 참조.

## 핵심

- 4 modes: `resolve` (path만 계산) / `create` (생성+검증) / `audit`
  (drift/leak 탐지) / `prune` (cleanup+검증)
- Priority resolution chain: `.worktrees/` > CLAUDE.md `worktree_root` >
  `--root` fallback > legacy `../worktree-<task-name>` fallback
- claude-code / codex-skill 양쪽에 동일 내용 유지 — 자동 sync 없이 각 root
  독립 관리
- Bundled scripts: `scripts/audit-worktrees.sh`, `scripts/cleanup-worktree.sh`
  (prune 시 worktree 제거 + local branch 삭제, 이전
  `ywc-parallel-executor/scripts/` 에서 `git mv` 로 이전, history 보존)

## `--keep-branch`

`--keep-branch` 는 prune 전용입니다. Worktree 와 stale metadata 는 제거하되
`--branch` 를 보존합니다. Non-aggregate `ywc-sequential-executor --worktree`
는 run worktree cleanup 후 accumulated integration branch 를 남기기 위해
이 옵션을 사용합니다.

## 호출 패턴

- `ywc-parallel-executor`: Pre-flight audit / Step 4 per-task create /
  Step 4g prune
- `ywc-finish-branch`: Step 5 / 8 cleanup (post-merge)
