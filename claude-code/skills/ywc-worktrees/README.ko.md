# ywc-worktrees (요약)

`ywc-parallel-executor` 와 `ywc-finish-branch` 에서 호출되는 worktree
lifecycle 관리 skill 의 한국어 요약본. 전체 문서는 [SKILL.md](./SKILL.md),
사용 가이드는 [README.md](./README.md) 참조.

## 핵심

- 4 modes: `resolve` (path만 계산) / `create` (생성+검증) / `audit`
  (drift/leak 탐지) / `prune` (cleanup+검증)
- Priority resolution chain: `.worktrees/` > CLAUDE.md `worktree_root` >
  `--root` fallback > legacy `../worktree-<task-name>` fallback
- 3-root sync (claude-code / codex-skill / pi-skills) — `is_diverged()`
  대상 외
- Bundled scripts: `scripts/audit-worktrees.sh`, `scripts/cleanup-worktree.sh`
  (prune 시 worktree 제거 + local branch 삭제, `--keep-branch` 시 worktree 만 제거하고
  branch 보존, 이전 `ywc-parallel-executor/scripts/` 에서 `git mv` 로 이전, history 보존)

## Task 이름

Task 이름과 branch 이름은 그대로 사용되므로 Task ID 의 `[INITIALS]` 접두가 투명하게 통과합니다.
`--task-name yk-000001-010-db-create-users` 와 legacy 무접두 `--task-name 000001-010-db-create-users`
가 모두 유효하며, `feature/yk-000001-010-db-create-users` 도 유효한 git ref 입니다.

## 호출 패턴

- `ywc-parallel-executor`: Pre-flight audit / Step 4 per-task create /
  Step 4g prune
- `ywc-finish-branch`: Step 5 / 8 cleanup (post-merge)
