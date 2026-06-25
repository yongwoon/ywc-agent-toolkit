# 000029-030-refactor-executor-health-sweeps

## Purpose

develop-with-llm PR #133 / #134 의 executor 계열 변경을 claude-code 트리에 port한다. `ywc-parallel-executor`(#133 net-neutral 강화), `ywc-sequential-executor`(#133 rationalization 1행 + #134 long-range compaction 문단). 두 PR이 `ywc-sequential-executor`를 동시에 편집하므로 이 task가 단독 소유하여 분할 충돌을 방지한다.

## Scope

- `ywc-parallel-executor/SKILL.md`: 기존 `--draft` bot 행에 "handle-pr-reviews가 CI·conflict까지 처리해 PR을 mergeable로 남김" 절을 **net-neutral**(줄 추가 없이 기존 행 강화)로 덧붙인다.
- `ywc-sequential-executor/SKILL.md` (#133): Rationalization Defense 1행 추가("Bot comments addressed … clears only one of three blockers").
- `ywc-sequential-executor/SKILL.md` (#134): checkpoint/resume 문단 뒤에 "Compaction on long ranges (context engineering)" 문단 1개 삽입.

## Spec Reference

**Primary Sources**

- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-claude-code-port.md` (Phase 2 #133 executors, Phase 3 #134 seq-exec compaction)
- 대응 upstream PR: `yongwoon/develop-with-llm` #133, #134

**Summary**

executor 두 skill에 PR-health 인식과 long-run compaction 규율을 반영한다. parallel-executor는 현재 501줄(기존 cap 초과)이므로 절대 줄을 늘리지 않는 net-neutral 편집만 한다. sequential-executor는 #133·#134 두 변경을 한 task에서 적용하되 line cap(현재 487, headroom 13)을 지킨다.

**Out of Scope (from spec)**

- `ywc-handle-pr-reviews` 본체 변경은 `000029-020` 담당.
- `references/aggregate-pr.md` 등 executor reference 파일은 #133 claude-code diff 범위 밖(미접촉).
- `codex/**` 미접촉.

## Criticality

`normal` — instruction/doc 편집만 수행.

## Dependencies

**Depends On**: (없음 — root)

**Depended By**: (없음)

## Key Files

- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/SKILL.md`

## Notes

- **parallel-executor net-neutral 불변식**: 편집 후 `wc -l`이 501로 유지되어야 한다(502 이상이면 cap 위반 악화 — 기존 행에 절을 합치고 새 줄 추가 금지).
- **sequential-executor line budget**: 현재 487줄. #133 rationalization 행 ≤3줄, #134 compaction 문단 ≤7줄로 작성해 ≤500 유지. 사후 압축에 의존하지 말 것.
- 두 SKILL은 README 변경 없음(#133/#134 모두 executor README를 건드리지 않음).

## Out of Scope

- executor 외 skill.
- aggregate-pr / branch-lifecycle reference 문서.

## Parallel Execution Metadata

**Ownership**

- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/SKILL.md`

**Shared Surfaces**: `bash scripts/validate.sh` + markdownlint CI 게이트.

**Conflicts With**: (None identified) — sequential-executor의 #133·#134 변경을 모두 이 task가 소유하므로 다른 task와 파일 충돌 없음.

**Parallelizable After**: 즉시(root).

**Task Verify**

- `rg -n "leaves the PR mergeable|three mandatory gates|mergeable" claude-code/skills/ywc-parallel-executor/SKILL.md`
- `test "$(wc -l < claude-code/skills/ywc-parallel-executor/SKILL.md)" -eq 501` (net-neutral 유지)
- `rg -n "clears only one of three blockers|three blockers" claude-code/skills/ywc-sequential-executor/SKILL.md`
- `rg -n "Compaction on long ranges|context engineering" claude-code/skills/ywc-sequential-executor/SKILL.md`
- `test "$(wc -l < claude-code/skills/ywc-sequential-executor/SKILL.md)" -le 500`
