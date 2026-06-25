# 000029-010-refactor-plan-spec-contracts

## Purpose

develop-with-llm PR #132 / #134 / #140 의 **spec·planning·PR-contract 계열 skill** 변경을 claude-code 트리에 port한다. 대상: `ywc-plan`(#132 spec-ready opt-in), `ywc-create-pr`(#134 Author Self-Review Gate), `ywc-spec-validate`(#134 `--tasks` Cross-Artifact + #140 band-mapping), `ywc-spec-writer`(#140 model 갱신).

## Scope

- `ywc-plan/SKILL.md`: Step 5 Medium/Large handoff를 `ywc-spec-ready` opt-in y/n prompt로 전환 + Validation/Integration 줄 갱신.
- `ywc-plan/README` 6 locale: "Related Skills"에 `ywc-spec-ready` 추가, `ywc-spec-validate`를 "manual next step"으로 재서술.
- `ywc-create-pr/SKILL.md`: Rationalization Defense 1행 추가 + `### 6.5. Author Self-Review Gate (mandatory)` 신설(`### 7. Create PR` 앞).
- `ywc-create-pr/README` 6 locale: Key Features self-review 항목 + 실행 흐름 renumber(기존 7→8, 신규 7=Self-Review Gate).
- `ywc-spec-validate/SKILL.md`: (#134) Rationalization 1행 + `--tasks` 인자 + Step 4c Cross-Artifact Consistency; (#140) band-mapping table 분할(PROCEED no-Critical→DONE / PROCEED+Critical→DONE_WITH_CONCERNS) + finding-count 표기 `Critical/High/Medium/Low`→`Critical/Warning/Suggestion` + Integration "Not applicable"→"Cross-artifact (Analyze)".
- `ywc-spec-validate/README` 6 locale: `--tasks tasks/` usage 예시 + Cross-Artifact note.
- `ywc-spec-writer/SKILL.md` + `references/full-gen-workflow.md`: `claude-opus-4-7`→`claude-opus-4-8`(fallback 4-5→4-7).

## Spec Reference

**Primary Sources**

- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-claude-code-port.md` (Phase 1 #132, Phase 3 #134 create-pr/spec-validate, Phase 4 #140 spec-validate/spec-writer)
- 대응 upstream PR: `yongwoon/develop-with-llm` #132, #134, #140

**Summary**

spec·planning·PR-contract skill 4종을 upstream과 정합화한다. spec-validate는 #134+#140 두 PR이 동시에 편집하므로 이 task가 단독 소유하여 분할 충돌을 방지한다. README는 toolkit 6 locale(md/en/es/ja/ko/zh) 전부에 반영하되, upstream diff는 4 locale만 담으므로 es/zh는 동일 변경을 직접 적용한다(세 skill 모두 es/zh 이미 존재 → 편집).

**Out of Scope (from spec)**

- `codex/**` / `plugins/**` 미접촉(Codex는 Batch 12 담당).
- spec-writer README 변경 없음(#140은 SKILL.md + reference만 변경).
- `evals/` 추가 없음.

## Criticality

`normal` — instruction/doc 편집만 수행하며 auth/payment/crypto/token/secret/password 코드 surface를 변경하지 않는다. (`ywc-create-pr`의 self-review gate가 secret 탐지를 *서술*하지만, 이는 skill 본문 내용이지 보안 코드 경로가 아니다.)

## Dependencies

**Depends On**: (없음 — root)

**Depended By**: (없음 — 동일 phase의 다른 task와 의존 관계 없음)

## Key Files

- `claude-code/skills/ywc-plan/SKILL.md`
- `claude-code/skills/ywc-plan/README.{md,en,es,ja,ko,zh}.md`
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-create-pr/README.{md,en,es,ja,ko,zh}.md`
- `claude-code/skills/ywc-spec-validate/SKILL.md`
- `claude-code/skills/ywc-spec-validate/README.{md,en,es,ja,ko,zh}.md`
- `claude-code/skills/ywc-spec-writer/SKILL.md`
- `claude-code/skills/ywc-spec-writer/references/full-gen-workflow.md`

## Notes

- spec-validate SKILL.md는 #134 영역(인자/Step 4c)과 #140 영역(band table/finding-count 표기)이 disjoint하므로 두 번의 분리된 edit로 적용하고 사이에 재확인한다.
- `ywc-create-pr/evals/evals.json`은 기존 파일 — 미접촉, 신규 README 산문에서 참조 금지.
- model 명은 upstream과 동일하게 `claude-opus-4-8`로 통일(이 환경의 최신 Opus와 일치).

## Out of Scope

- `ywc-handle-pr-reviews`, executor, agentic, onboard, gen-testcase, project-docs/scaffold (각각 다른 task 소유).
- 동작 검증을 넘어선 skill 재구조화.

## Parallel Execution Metadata

**Ownership**

- `claude-code/skills/ywc-plan/**`
- `claude-code/skills/ywc-create-pr/SKILL.md`, `claude-code/skills/ywc-create-pr/README.*.md` (단, `evals/` 제외)
- `claude-code/skills/ywc-spec-validate/**`
- `claude-code/skills/ywc-spec-writer/SKILL.md`, `claude-code/skills/ywc-spec-writer/references/full-gen-workflow.md`

**Shared Surfaces**: `bash scripts/validate.sh` + markdownlint CI 게이트(전 task 공유).

**Conflicts With**: (None identified) — 소유 skill이 다른 task와 겹치지 않음.

**Parallelizable After**: 즉시(root). 사전 머지 baseline 불필요.

**Task Verify**

- `rg -n "ywc-spec-ready|opt-in|자동 수렴|auto-converge" claude-code/skills/ywc-plan/SKILL.md`
- `rg -n "Author Self-Review Gate|git diff <base-branch>\.\.\.HEAD|does not replace independent" claude-code/skills/ywc-create-pr/SKILL.md`
- `rg -n -- "--tasks <dir>|Cross-Artifact Consistency|Requirement Coverage|Task Provenance" claude-code/skills/ywc-spec-validate/SKILL.md`
- `rg -n "Critical/Warning/Suggestion|PROCEED.*no Critical|PROCEED.*Critical.*DONE_WITH_CONCERNS" claude-code/skills/ywc-spec-validate/SKILL.md`
- `rg -n "claude-opus-4-8" claude-code/skills/ywc-spec-writer/SKILL.md claude-code/skills/ywc-spec-writer/references/full-gen-workflow.md`
- `! rg -n "claude-opus-4-7" claude-code/skills/ywc-spec-writer/SKILL.md` (4-7 잔존 없음, fallback 줄 제외)
