# 000006-030-infra-claude-worktree-rollout

## Purpose

PR #129의 Claude Code worktree rollout을 이 repository에 port한다: `ywc-sequential-executor --worktree`(+ `worktree-run.md`), `ywc-worktrees --keep-branch`, `ywc-finish-branch --worktree-path`, 그리고 `ywc-parallel-executor`의 sequential/parallel granularity note. 대응 PR: **PR-C (#129)**.

## Scope

- `claude-code/skills/ywc-sequential-executor/`: `--worktree` flag + Run-level Worktree mode 섹션 + `references/worktree-run.md` 신규 + README locale 4개 갱신
- `claude-code/skills/ywc-worktrees/`: `--keep-branch` arg + prune table 갱신 + cleanup-step prose + README locale 4개 + `scripts/cleanup-worktree.sh` 갱신
- `claude-code/skills/ywc-finish-branch/`: `--worktree-path` arg + Worktree-path mode 섹션 + Step 1/5/6/7/8 `-C <path>` note + README locale 4개
- `claude-code/skills/ywc-parallel-executor/SKILL.md`: sequential vs parallel granularity note 1줄

## Spec Reference

### Primary Sources
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#workstream-c--pr-129-sequential-worktree-rollout--pr-c` - port 대상 file과 hunk 목록
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#existing-constraints-touched-verified` - parallel-executor double-touch(#110·#129) 경고와 runtime path convention

### Summary
PR #129의 Claude Code bundle을 port한다. sequential-executor에 run-level worktree 격리(`--worktree`)와 그 lifecycle 문서(`worktree-run.md`)를 추가하고, 이를 지원하는 `ywc-worktrees --keep-branch`(integration branch 보존)와 `ywc-finish-branch --worktree-path`(worktree HEAD에서 delivery)를 더한다. catalog/count 변경은 없다(신규 skill 없음).

### Out of Scope (from spec)
- Codex bundle - `000003`~`000005` Codex batch 담당
- `claude-code/agents/**`
- docker-isolate / spec-ready - 각각 `000006-010` / `000006-020`
- catalog row / skill count - 본 task는 신규 skill이 없어 §D 변경 없음
- `CHANGELOG.md` / `VERSION` - Release Please 관할

## Dependencies

### Depends On
- (root, 논리적으로는 무의존) - 본 task의 변경은 `000006-010` 없이도 동작한다. 다만 `claude-code/skills/ywc-parallel-executor/SKILL.md`를 공유하므로 merge 충돌 회피를 위해 `000006-010` 이후 실행/rebase를 권장.

### Depended By
- (없음)

## Key Files

신규:
- `claude-code/skills/ywc-sequential-executor/references/worktree-run.md`

수정:
- `claude-code/skills/ywc-sequential-executor/SKILL.md` + `README.md`/`.en`/`.ja`/`.ko`
- `claude-code/skills/ywc-worktrees/SKILL.md` + `README.md`/`.en`/`.ja`/`.ko` + `scripts/cleanup-worktree.sh`
- `claude-code/skills/ywc-finish-branch/SKILL.md` + `README.md`/`.en`/`.ja`/`.ko`
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (granularity note 1줄)

## Notes

- **parallel-executor double-touch**: `000006-010`도 같은 file에 Docker hook을 추가한다. 라인은 다르므로 `000006-010` 먼저 merge 후 본 task를 rebase하면 충돌 없음. 병렬 실행 금지.
- `cleanup-worktree.sh`는 `--keep-branch` 분기 + 누락 branch idempotent 처리 추가. `bash -n` 통과 필요.
- runtime path는 이미 `claude-code/` convention인 기존 file을 수정하는 것이므로 신규 path-rewrite는 거의 없으나, port한 hunk 안에 `tools/claude-code/`가 섞이지 않았는지 확인.

## Out of Scope

- Codex / agents / docker-isolate / spec-ready
- catalog / count / `CHANGELOG.md` / `VERSION`

## Parallel Execution Metadata

- **Ownership**:
  - `claude-code/skills/ywc-sequential-executor/**`
  - `claude-code/skills/ywc-worktrees/**`
  - `claude-code/skills/ywc-finish-branch/**`
  - `claude-code/skills/ywc-parallel-executor/SKILL.md` (granularity note 라인만)
- **Shared Surfaces**:
  - `claude-code/skills/ywc-parallel-executor/SKILL.md` - `000006-010`도 수정(Docker hook). 동일 file, 다른 라인.
- **Conflicts With**: `000006-010-infra-claude-docker-isolate` (parallel-executor SKILL.md 공유 — 병렬 금지)
- **Parallelizable After**: `000006-010-infra-claude-docker-isolate` merge 후 (parallel-executor 충돌 회피). `000006-020`과는 무관.
- **Task Verify**:
  ```bash
  bash scripts/validate.sh
  bash -n claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh
  grep -n "keep-branch" claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh   # 존재
  grep -n "worktree-path" claude-code/skills/ywc-finish-branch/SKILL.md                # 존재
  test -f claude-code/skills/ywc-sequential-executor/references/worktree-run.md        # 존재
  grep -rn "tools/claude-code" claude-code/skills/ywc-sequential-executor claude-code/skills/ywc-worktrees claude-code/skills/ywc-finish-branch  # 0
  ```
