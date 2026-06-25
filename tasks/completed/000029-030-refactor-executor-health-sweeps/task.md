# Task: 000029-030-refactor-executor-health-sweeps

## Prerequisites

- [ ] batch 단일 branch에서 작업 중인지 확인
- [ ] upstream 참조: `gh pr diff 133`, `gh pr diff 134` (`--repo yongwoon/develop-with-llm`, executor 경로만)
- [ ] line baseline 기록: `wc -l claude-code/skills/ywc-parallel-executor/SKILL.md` (=501), `… ywc-sequential-executor/SKILL.md` (=487)

## Allowed Edit Scope

- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/SKILL.md`
- 그 외 경로 편집 금지(특히 `ywc-handle-pr-reviews` — `000029-020` 담당, `codex/**`).

## Stop Conditions

- parallel-executor 편집이 줄 수를 501 초과로 늘리면 중단(net-neutral 위반).
- sequential-executor 편집 후 501줄 이상이면 중단·문구 압축.
- 두 변경이 이미 존재하면(중복) 중단.

## Implementation Steps

- [ ] `ywc-parallel-executor/SKILL.md`: Rationalization Defense의 기존 `--draft creates PR at the end, bot review can wait` 행에 "`ywc-handle-pr-reviews` itself also clears CI failures and base conflicts (its three mandatory gates), so handling comments is not 'comments only' — it leaves the PR mergeable." 절을 **기존 행 안에서** 덧붙인다(새 표 행/줄 추가 금지).
- [ ] `ywc-sequential-executor/SKILL.md` (#133): Rationalization Defense에 "Bot comments were addressed via ywc-handle-pr-reviews — the PR is handled, proceed to merge" 행 1개 추가(≤3줄). 요지: comment 처리는 3 blocker 중 하나만 해소; finish-branch가 CI green + mergeable 재확인.
- [ ] `ywc-sequential-executor/SKILL.md` (#134): checkpoint/resume 설명 문단 뒤에 "**Compaction on long ranges (context engineering).**" 문단 1개 삽입(≤7줄). 요지: ~30+ task range에서 `.ywc-run-state.json` + `tasks/completed/<id>/`를 source of truth로 삼고 working context에는 one-line digest만 유지. `[../references/subagent-status-actions.md](../references/subagent-status-actions.md)` §3.5 링크.

## Task Verify

- [ ] `rg -n "mergeable" claude-code/skills/ywc-parallel-executor/SKILL.md` (>0, --draft 행 내)
- [ ] `test "$(wc -l < claude-code/skills/ywc-parallel-executor/SKILL.md)" -eq 501`
- [ ] `rg -n "three blockers" claude-code/skills/ywc-sequential-executor/SKILL.md` (>0)
- [ ] `rg -n "Compaction on long ranges" claude-code/skills/ywc-sequential-executor/SKILL.md` (>0)
- [ ] `test "$(wc -l < claude-code/skills/ywc-sequential-executor/SKILL.md)" -le 500`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `npx markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-parallel-executor/SKILL.md" "claude-code/skills/ywc-sequential-executor/SKILL.md"` (0 errors)
- [ ] `git diff --name-only` 결과가 두 executor SKILL.md로만 한정(특히 `codex/` 미포함)
