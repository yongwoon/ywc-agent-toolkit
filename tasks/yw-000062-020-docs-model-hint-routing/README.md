# yw-000062-020-docs-model-hint-routing

## Purpose
task 별 Model Hint 로 implementer subagent 의 model 을 라우팅해 비용을 줄인다 (Phase E, FR-E2~E4, FR-E6).

## Scope
- `references/model-routing.md` 신규 (M1 적응, M2, M3, Version floor, source 라벨) (FR-E2)
- task-generator template / metadata reference / SKILL.md pointer (FR-E3)
- parallel-executor Step 1 / 3 / 4b / 5 (FR-E4)
- 두 skill 의 Tier 1 README 갱신 (FR-E6)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — FR-E2~FR-E4, FR-E6, AC-10/16/17(README 부분), FM-3
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #288 의 Claude 측을 적응 반영한다. 이 저장소에는 Criticality 가 없으므로 M1 은 "Depended By task bullet ≥2 이고 `(None` 으로 시작하지 않는 Owned Interface bullet ≥1 → opus". Escalation Ladder 와 `escalated` 라벨은 제외. Model Hint 는 template 의 `## Parallel Execution Metadata` 아래 `### Ownership` 앞 단독 줄.

### Out of Scope (from spec)
- #288 Escalation Ladder (`subagent-status-actions.md`)
- Codex routed installer
- README Tier 2 (zh / es)

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- `yw-000061-010-docs-fastify-scaffold` — Phase D 머지 base

### Depended By
- (None — no downstream dependency)

## Key Files
- `claude-code/skills/references/model-routing.md` (신규)
- `claude-code/skills/ywc-task-generator/SKILL.md`, `references/README.md.template`, `references/parallel-execution-metadata.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (`:156-163`, `:191`, `:211`, `:416`), `references/subagent-directives.md`
- `claude-code/skills/ywc-{parallel-executor,task-generator}/README{,.en,.ja,.ko}.md`

## Notes
- parallel-executor 는 Phase A 이후 500 줄 근접 — 상세는 `model-routing.md` 로, SKILL.md 에는 pointer 만.
- Version floor (`CLAUDE_CODE_SUBAGENT_MODEL`, upstream 기준 v2.1.251) 는 upstream 출처 기재 — 이 저장소에서 독립 검증되지 않음을 명시.
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: haiku — M2 (Ownership 전부 `*.md`, category docs)

### Ownership
- `claude-code/skills/references/model-routing.md`
- `claude-code/skills/ywc-task-generator/SKILL.md`
- `claude-code/skills/ywc-task-generator/references/README.md.template`
- `claude-code/skills/ywc-task-generator/references/parallel-execution-metadata.md`
- `claude-code/skills/ywc-task-generator/README*.md` (Tier 1)
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/references/subagent-directives.md`
- `claude-code/skills/ywc-parallel-executor/README*.md` (Tier 1)

### Owned Interface
- README 의 `- Model Hint: <haiku|sonnet|opus> — <rule>` 줄 형식과 M1~M3 규칙 (`references/model-routing.md`)
- Completion Report 표기 `<model> (<source>)`, source ∈ `hint` / `frontmatter` / `env` / `default`

### Shared Surfaces
- task README 형식 (`README.md.template`) — 이후 생성되는 모든 task

### Conflicts With
- (None identified — 같은 phase 의 010 / 030 과 파일 겹침 없음)

### Parallelizable After
- `yw-000061-010-docs-fastify-scaffold`

### Task Verify
- `grep -c "Model Hint" claude-code/skills/references/model-routing.md claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md` 각 ≥1 (AC-10)
- `grep -c "CLAUDE_CODE_SUBAGENT_MODEL" claude-code/skills/references/model-routing.md` ≥1, `grep -c "Model Hint" claude-code/skills/ywc-task-generator/references/README.md.template claude-code/skills/ywc-task-generator/references/parallel-execution-metadata.md` 각 ≥1 (AC-16)
- `grep -c "Model Hint" claude-code/skills/ywc-parallel-executor/README.md claude-code/skills/ywc-parallel-executor/README.en.md claude-code/skills/ywc-parallel-executor/README.ja.md claude-code/skills/ywc-parallel-executor/README.ko.md` 및 task-generator 동일 각 ≥1 (AC-17)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- sequential-executor 의 hint 소비 (설계상 무시)
- README zh / es
