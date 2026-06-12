# ywc-worktrees (요약)

`ywc-parallel-executor` 와 `ywc-finish-branch` 에서 호출되는 worktree
lifecycle 관리 skill 의 한국어 요약본. 전체 문서는 [SKILL.md](./SKILL.md),
사용 가이드는 [README.md](./README.md) 참조.

## 핵심

- 4 modes: `resolve` (path만 계산) / `create` (생성+검증) / `audit`
  (drift/leak 탐지) / `prune` (cleanup+검증)
- Priority resolution chain: `.worktrees/` > CLAUDE.md `worktree_root` >
  `--root` fallback > legacy `../worktree-<task-name>` fallback
- Bundled scripts: `scripts/audit-worktrees.sh`, `scripts/cleanup-worktree.sh`
  (prune 시 worktree 제거 + local branch 삭제, audit / cleanup logic 을 이
  skill 아래에 centralized)
- Codex bundle source: `codex/skills/ywc-worktrees/` 의 script 와 metadata 를
  기준으로 유지

## 호출 패턴

- `ywc-parallel-executor`: Pre-flight audit / Step 4 per-task create /
  Step 4g prune
- `ywc-finish-branch`: Step 5 / 8 cleanup (post-merge)
