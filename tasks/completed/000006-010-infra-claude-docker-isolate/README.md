# 000006-010-infra-claude-docker-isolate

## Purpose

PR #110의 Claude Code `ywc-docker-isolate` skill을 이 repository의 `claude-code/skills/` 구조에 port하고, `ywc-parallel-executor`에 Docker isolation hook을 연결한다. 배포 catalog/count surface(§D)의 docker-isolate 관련 항목도 이 task에서 함께 갱신한다. 대응 PR: **PR-A (#110)**.

## Scope

- `claude-code/skills/ywc-docker-isolate/` 신규 생성 (SKILL.md + README locale set + references + scripts, 총 12 files)
- `claude-code/skills/ywc-parallel-executor/SKILL.md`에 Docker audit/setup/teardown hook 3곳 추가 (runtime path를 `claude-code/skills/...`로 rewrite)
- §D1: root `README.md`의 **Task & Execution** catalog table에 `ywc-docker-isolate` row 추가
- §D2: `claude-code/skills/CLAUDE.md` script catalog table(`:213`)에 docker-isolate script 3 rows 추가
- §D3: skill count `36 → 37` (이 task가 skill 1개 추가) — 6개 count surface 전체
- eval baseline에 `ywc-docker-isolate` 등록

## Spec Reference

### Primary Sources
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#workstream-a--pr-110-ywc-docker-isolate--pr-a` - docker-isolate port 대상 file 목록과 path-rewrite 규칙
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#workstream-d--distribution-catalog--counts-folds-into-existing-prs-no-new-pr` - §D1/D2/D3 catalog·count 갱신 규칙
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#existing-constraints-touched-verified` - runtime path convention(`tools/claude-code/` → `claude-code/`) 근거

### Summary
upstream `develop-with-llm` PR #110의 Claude Code bundle을 이 repository로 port한다. 핵심 변환 규칙은 skill body/script 안의 runtime path `tools/claude-code/skills/...`를 이 repository convention인 `claude-code/skills/...`로 rewrite하는 것이다. docker-isolate skill 자체와 parallel-executor hook 연결, 그리고 이 skill을 노출하는 배포 catalog(root README, skills/CLAUDE.md script table)·skill count를 함께 갱신한다.

### Out of Scope (from spec)
- Codex bundle(`codex/skills/**`) - `000003`~`000005` Codex batch가 담당, 본 task와 무관
- `claude-code/agents/**` - 3개 PR 모두 agent를 변경하지 않음
- `ywc-spec-ready` / spec-validate / agentic 변경 - `000006-020`이 담당
- worktree rollout (sequential-executor / worktrees / finish-branch) - `000006-030`이 담당
- `CHANGELOG.md` / `VERSION` 직접 수정 - Release Please 관할

## Dependencies

### Depends On
- (root) - 선행 task 없음. 현재 `main` baseline에서 즉시 시작 가능.

### Depended By
- `000006-030-infra-claude-worktree-rollout` - `claude-code/skills/ywc-parallel-executor/SKILL.md`를 공유하므로, 본 task가 먼저 merge되어야 worktree rollout의 granularity note가 충돌 없이 rebase된다.

## Key Files

신규:
- `claude-code/skills/ywc-docker-isolate/SKILL.md`
- `claude-code/skills/ywc-docker-isolate/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md`
- `claude-code/skills/ywc-docker-isolate/references/port-allocation.md` / `preconditions.md`
- `claude-code/skills/ywc-docker-isolate/scripts/_lib.sh` / `setup-docker-ports.sh` / `teardown-docker.sh` / `audit-docker-stacks.sh`

수정:
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (Docker hook 3곳)
- `README.md` (Task & Execution catalog row + count 36→37)
- `claude-code/skills/CLAUDE.md` (script catalog 3 rows)
- `README.ko.md` / `README.ja.md` / `README.es.md` / `README.zh.md` / `CLAUDE.md` (count 36→37)
- `.claude/skills/ywc-toolkit-eval/evals/` (baseline 등록)

## Notes

- **Path-rewrite는 가장 중요한 불변식**: port한 모든 file에 `grep -rn "tools/claude-code"`가 0이어야 한다. upstream은 `bash tools/claude-code/skills/ywc-docker-isolate/scripts/...`로 작성되어 있으나 이 repository에서는 `bash claude-code/skills/ywc-docker-isolate/scripts/...`가 정답이다 (근거: `claude-code/skills/ywc-parallel-executor/SKILL.md:110`).
- script 4개는 `chmod +x` 유지, `bash -n` 통과 필요.
- count는 Claude Code skill figure만 37로 바꾸고 Codex/agent figure는 건드리지 않는다.

## Out of Scope

- Codex / agents / spec-ready / worktree rollout (각각 별도 task 또는 별도 batch)
- `CHANGELOG.md` / `VERSION`

## Parallel Execution Metadata

- **Ownership**:
  - `claude-code/skills/ywc-docker-isolate/**` (신규, 전체)
  - `claude-code/skills/ywc-parallel-executor/SKILL.md` (Docker hook 라인만)
  - `claude-code/skills/CLAUDE.md` (script catalog table)
  - root `README.md` (Task & Execution catalog row + Claude count cell)
  - `README.ko.md` / `README.ja.md` / `README.es.md` / `README.zh.md` / `CLAUDE.md` (Claude skill count 숫자만)
  - `.claude/skills/ywc-toolkit-eval/evals/**` (baseline entry)
- **Shared Surfaces**:
  - `claude-code/skills/ywc-parallel-executor/SKILL.md` - `000006-030`도 수정(granularity note). 라인은 다르나 동일 file.
  - skill count surfaces(`README.*`, `CLAUDE.md`) - `000006-020`도 count를 37→38로 증분.
- **Conflicts With**: `000006-030-infra-claude-worktree-rollout` (parallel-executor SKILL.md 공유 — 병렬 금지)
- **Parallelizable After**: root `main` baseline (선행 없음). `000006-020`과는 병렬 가능하나 count 증분 순서 주의(본 task 36→37 먼저).
- **Task Verify**:
  ```bash
  bash scripts/validate.sh
  grep -rn "tools/claude-code" claude-code/skills/ywc-docker-isolate claude-code/skills/ywc-parallel-executor   # 결과 0
  bash -n claude-code/skills/ywc-docker-isolate/scripts/*.sh
  grep -c "ywc-docker-isolate" README.md                       # >= 1 (catalog row)
  grep -c "ywc-docker-isolate/scripts" claude-code/skills/CLAUDE.md   # = 3
  ```
