# 000006-020-infra-claude-spec-ready

## Purpose

PR #120의 Claude Code `ywc-spec-ready` skill을 이 repository에 port하고, `ywc-spec-validate`에 `--advisor-budget`를, `ywc-agentic` Step 3에 spec-ready loop 위임을 반영한다. 배포 catalog/count surface(§D)의 spec-ready 관련 항목도 함께 갱신한다. 대응 PR: **PR-B (#120)**.

## Scope

- `claude-code/skills/ywc-spec-ready/` 신규 생성 (SKILL.md + README locale set + references, 총 7 files)
- `claude-code/skills/ywc-spec-validate/SKILL.md`에 `--advisor-budget` 4개 hunk 반영 + README locale 4개 1줄 갱신
- `claude-code/skills/ywc-agentic/SKILL.md` Step 3을 spec-ready loop 위임으로 rewire (2 hunk)
- §D1: root `README.md`의 **Planning & Spec** catalog table에 `ywc-spec-ready` row 추가
- §D3: skill count `37 → 38` (이 task가 skill 1개 추가) — 6개 count surface 전체
- eval baseline에 `ywc-spec-ready` 등록

## Spec Reference

### Primary Sources
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#workstream-b--pr-120-ywc-spec-ready--advisor-budget--pr-b` - spec-ready port 대상 file과 spec-validate/agentic 수정 범위
- `docs/ywc-plans/port-upstream-skill-prs-110-120-129.md#workstream-d--distribution-catalog--counts-folds-into-existing-prs-no-new-pr` - §D1(Planning & Spec row)·§D3(count 37→38) 규칙

### Summary
PR #120의 Claude Code bundle을 port한다. `ywc-spec-ready`는 spec을 `ywc-spec-validate` DONE까지 수렴시키는 loop skill이며, `ywc-spec-validate`에는 advisor 비용을 제어하는 `--advisor-budget`가 추가되고, `ywc-agentic` Step 3은 단일 validate 호출 대신 spec-ready loop에 위임하도록 바뀐다. 이 skill을 노출하는 root README catalog와 skill count를 함께 갱신한다.

### Out of Scope (from spec)
- Codex bundle - `000003`~`000005` Codex batch 담당
- `claude-code/agents/**`
- docker-isolate / worktree rollout - 각각 `000006-010` / `000006-030`
- `CHANGELOG.md` / `VERSION` - Release Please 관할
- locale README catalog rows - locale README에는 per-skill catalog table이 없음(검증 완료), count만 갱신

## Dependencies

### Depends On
- (root) - 선행 task 없음. `000006-010`과 독립이며 병렬 가능(단, count 증분 순서 주의).

### Depended By
- (없음) - 후속 task가 본 task 산출물에 직접 의존하지 않음.

## Key Files

신규:
- `claude-code/skills/ywc-spec-ready/SKILL.md`
- `claude-code/skills/ywc-spec-ready/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md`
- `claude-code/skills/ywc-spec-ready/references/convergence.md` / `loop-log.md`

수정:
- `claude-code/skills/ywc-spec-validate/SKILL.md` (`--advisor-budget` 4 hunk)
- `claude-code/skills/ywc-spec-validate/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` (1줄씩)
- `claude-code/skills/ywc-agentic/SKILL.md` (Step 3 rewire, 2 hunk)
- `README.md` (Planning & Spec catalog row + count 37→38)
- `README.ko.md` / `README.ja.md` / `README.es.md` / `README.zh.md` / `CLAUDE.md` (count 37→38)
- `.claude/skills/ywc-toolkit-eval/evals/` (baseline 등록)

## Notes

- `ywc-spec-ready`는 script가 없으므로 `claude-code/skills/CLAUDE.md` script catalog table에는 행을 추가하지 않는다.
- port한 file에서 `@skill-name` force-load 참조 금지(repo 규칙), path 참조는 `claude-code/` 또는 `../` style 유지.
- count는 `000006-010`이 36→37을 마친 뒤 37→38이 자연스럽다. 순서가 어긋나면 "count == 실제 `claude-code/skills/ywc-*` 디렉터리 수" 불변식으로 맞춘다.

## Out of Scope

- Codex / agents / docker-isolate / worktree rollout
- `CHANGELOG.md` / `VERSION`
- locale README catalog rows (해당 table 부재)

## Parallel Execution Metadata

- **Ownership**:
  - `claude-code/skills/ywc-spec-ready/**` (신규, 전체)
  - `claude-code/skills/ywc-spec-validate/**` (SKILL.md + README locale set)
  - `claude-code/skills/ywc-agentic/SKILL.md` (Step 3 영역)
  - root `README.md` (Planning & Spec catalog row + Claude count cell)
  - `README.ko.md` / `README.ja.md` / `README.es.md` / `README.zh.md` / `CLAUDE.md` (Claude count 숫자만)
  - `.claude/skills/ywc-toolkit-eval/evals/**` (baseline entry)
- **Shared Surfaces**:
  - skill count surfaces(`README.*`, `CLAUDE.md`) - `000006-010`도 count를 36→37로 증분.
- **Conflicts With**: (None identified) — `000006-010`/`000006-030`과 파일 겹침 없음(공유 count surface는 동일 행의 숫자만, 순차 증분으로 해소)
- **Parallelizable After**: root `main` baseline.
- **Task Verify**:
  ```bash
  bash scripts/validate.sh
  grep -rn "tools/claude-code" claude-code/skills/ywc-spec-ready   # 0
  grep -c "ywc-spec-ready" README.md                               # >= 1 (catalog row)
  grep -n "advisor-budget" claude-code/skills/ywc-spec-validate/SKILL.md   # 존재
  ```
