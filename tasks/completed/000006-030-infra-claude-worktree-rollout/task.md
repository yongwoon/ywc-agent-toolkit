# Task: 000006-030-infra-claude-worktree-rollout

## Prerequisites

- [ ] `000006-010-infra-claude-docker-isolate` merge 완료 (parallel-executor SKILL.md 충돌 회피) — 또는 본 task를 그 위에 rebase
- [ ] upstream source 접근 가능 (`gh pr diff 129 --repo yongwoon/develop-with-llm`)
- [ ] `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md` Workstream C 숙지

## Allowed Edit Scope

- `claude-code/skills/ywc-sequential-executor/**`
- `claude-code/skills/ywc-worktrees/**`
- `claude-code/skills/ywc-finish-branch/**`
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (granularity note 라인만)

다른 skill, `codex/**`, `claude-code/agents/**`, root `README*` catalog/count, `claude-code/skills/CLAUDE.md`, `CHANGELOG.md`, `VERSION`은 수정 금지.

## Stop Conditions

- `bash -n claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh` 실패 시 멈추고 보고
- port한 hunk에 `tools/claude-code/` path가 섞여 들어오면 멈추고 보고
- `000006-010` 미merge 상태에서 parallel-executor 충돌이 나면 멈추고 rebase 안내

## Implementation Steps

- [ ] `gh pr diff 129 --repo yongwoon/develop-with-llm`로 upstream Claude Code hunk 확보 (codex hunk 제외)
- [ ] `claude-code/skills/ywc-sequential-executor/references/worktree-run.md` 신규 작성
- [ ] `claude-code/skills/ywc-sequential-executor/SKILL.md`에 `--worktree` flag row, rationalization 2행, flag-conflict note, "Run-level Worktree mode" 섹션 추가
- [ ] `claude-code/skills/ywc-sequential-executor/README.md`/`.en`/`.ja`/`.ko` 각 +2줄 갱신
- [ ] `claude-code/skills/ywc-worktrees/SKILL.md`에 `--keep-branch` arg row + prune-mode table 갱신 + cleanup-step prose (3 hunk)
- [ ] `claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh`에 `--keep-branch` 파싱 + Step 2 skip-branch-delete + 누락 branch idempotent 처리 + verification 분기 추가
- [ ] `claude-code/skills/ywc-worktrees/README.md`/`.en`/`.ja`/`.ko` 갱신
- [ ] `claude-code/skills/ywc-finish-branch/SKILL.md`에 `--worktree-path` arg row + "Worktree-path mode" 섹션 + Step 1/5/6/7/8 `-C <path>` note
- [ ] `claude-code/skills/ywc-finish-branch/README.md`/`.en`/`.ja`/`.ko` 각 1줄 갱신
- [ ] `claude-code/skills/ywc-parallel-executor/SKILL.md`에 sequential vs parallel worktree granularity note 1줄 추가 (Docker hook 라인과 별개 위치)
- [ ] internal link 확인: sequential-executor SKILL.md → `references/worktree-run.md` 해상

## Task Verify

```bash
bash scripts/validate.sh
bash -n claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh
grep -n "keep-branch" claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh   # 존재
grep -n "worktree-path" claude-code/skills/ywc-finish-branch/SKILL.md                # 존재
grep -n "\-\-worktree" claude-code/skills/ywc-sequential-executor/SKILL.md           # 존재
test -f claude-code/skills/ywc-sequential-executor/references/worktree-run.md
grep -rn "tools/claude-code" claude-code/skills/ywc-sequential-executor claude-code/skills/ywc-worktrees claude-code/skills/ywc-finish-branch  # 0
```

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] `bash -n` cleanup-worktree.sh 통과
- [ ] `npx --yes markdownlint-cli2 "claude-code/skills/*/README*.md"` 통과
- [ ] `git diff --check` 통과
- [ ] `codex/**` / `claude-code/agents/**` / catalog·count surface / `CHANGELOG.md` / `VERSION` 무변경 확인
