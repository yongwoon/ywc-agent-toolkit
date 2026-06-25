# 000029-040-refactor-agent-context-compaction

## Purpose

develop-with-llm PR #134 의 long-run compaction · agent-context reconciliation 변경을 claude-code 트리에 port한다. `ywc-agentic`(긴 run의 context compaction 문단), `ywc-onboard-repo`(기존 `AGENTS.md`/`.cursorrules` 탐지·reconcile).

## Scope

- `ywc-agentic/SKILL.md`: `### Step 9: Completion Report` 앞에 "Compaction on long runs (context engineering)" 문단 1개 삽입. **SKILL.md only** — #134는 agentic README를 건드리지 않으며, 이 skill은 현재 4 locale(en/ja/ko)만 보유하고 이 batch에서 보정하지 않는다.
- `ywc-onboard-repo/SKILL.md`: Rationalization Defense 1행(AGENTS.md) + Phase 1 "Agent-context pre-check" 문단 + Phase 4(Output B) AGENTS.md reconcile 문단 + Validation 체크리스트 1행.
- `ywc-onboard-repo/README` 6 locale: Output B reconcile 절(AGENTS.md / .cursorrules). **`README.es.md`·`README.zh.md`는 미존재 → 신규 생성**(README.en 기준 번역 seed 후 reconcile 절 반영).

## Spec Reference

**Primary Sources**

- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-claude-code-port.md` (Phase 3 #134 agentic/onboard)
- 대응 upstream PR: `yongwoon/develop-with-llm` #134

**Summary**

#134의 두 비-executor 변경을 묶는다. agentic은 SKILL.md 한 문단만, onboard-repo는 SKILL.md 4곳 + README 6 locale. onboard-repo의 es/zh는 toolkit에 부재하여 신규 생성 대상(이 batch에서 유일한 create 케이스). agentic README는 변경 대상이 아니므로 4-locale 상태 그대로 둔다.

**Out of Scope (from spec)**

- agentic README 생성/수정(#134 미대상).
- sequential-executor compaction은 `000029-030` 담당(별도 skill).
- `codex/**` 미접촉.

## Criticality

`normal` — instruction/doc 편집만 수행.

## Dependencies

**Depends On**: (없음 — root)

**Depended By**: (없음)

## Key Files

- `claude-code/skills/ywc-agentic/SKILL.md`
- `claude-code/skills/ywc-onboard-repo/SKILL.md`
- `claude-code/skills/ywc-onboard-repo/README.{md,en,ja,ko}.md` (편집)
- `claude-code/skills/ywc-onboard-repo/README.es.md`, `claude-code/skills/ywc-onboard-repo/README.zh.md` (**신규 생성**)

## Notes

- **create-not-edit 주의**: onboard-repo의 es/zh는 부재 → en 기준 번역으로 신규 생성 후 reconcile 절 반영. 검증은 `validate.sh`가 4 locale만 보므로 es/zh는 `ls`로 별도 확인.
- agentic compaction 문단은 `[../references/subagent-status-actions.md](../references/subagent-status-actions.md)` §3.5를 참조(파일 존재 확인됨).
- agentic은 README 미변경 — 4 locale 상태 유지(이 batch의 보정 대상 아님).

## Out of Scope

- agentic README 6-locale 보정.
- onboard-repo의 `references/claude-md-starter.md` 등 reference 변경(#134 diff 밖).

## Parallel Execution Metadata

**Ownership**

- `claude-code/skills/ywc-agentic/SKILL.md`
- `claude-code/skills/ywc-onboard-repo/**`

**Shared Surfaces**: `bash scripts/validate.sh` + markdownlint CI 게이트.

**Conflicts With**: (None identified)

**Parallelizable After**: 즉시(root).

**Task Verify**

- `rg -n "Compaction on long runs|context engineering" claude-code/skills/ywc-agentic/SKILL.md`
- `rg -n "AGENTS.md" claude-code/skills/ywc-onboard-repo/SKILL.md` (Rationalization + Phase 1 + Phase 4 + Validation)
- `rg -n "Agent-context pre-check" claude-code/skills/ywc-onboard-repo/SKILL.md`
- `ls claude-code/skills/ywc-onboard-repo/README.es.md claude-code/skills/ywc-onboard-repo/README.zh.md` (신규 생성 확인)
- `rg -n "AGENTS.md" claude-code/skills/ywc-onboard-repo/README.es.md claude-code/skills/ywc-onboard-repo/README.zh.md`
