# 000029-020-refactor-pr-health-handler

## Purpose

develop-with-llm PR #133 의 `ywc-handle-pr-reviews` 변경을 claude-code 트리에 port한다. "PR 대응"의 정의를 *comment 응답*에서 *PR을 mergeable로 남기기*(comment·CI·conflict 세 독립 gate)로 재정의하고, comment가 0건이어도 CI·conflict gate를 **매 실행마다** 수행하도록 한다.

## Scope

- `ywc-handle-pr-reviews/SKILL.md`:
  - frontmatter `description` 재작성(mergeable framing + `fix PR CI` / `PR conflict 해결` trigger 추가).
  - Announce 줄 + intro 문단 갱신.
  - Rationalization Defense 1행 추가("No unresolved comments — nothing to handle").
  - `## Definition of Done` 신설(3-gate 표 + 필수 TodoWrite).
  - step 번호 `### 1.`→`### Step 1:` … `### Step 9` 연속화.
  - Step 2 empty-array reroute(`[]`이어도 Step 7·8 실행).
  - `6.5`→`Step 7 CI Gate (EVERY invocation)`, `6.6`→`Step 8 Merge-Readiness Gate (EVERY invocation)`, `7. Final Summary`→`Step 9`(3-gate 보고).
  - 내부 cross-reference(Step 7→8→9) 정합화.
- `ywc-handle-pr-reviews/README` 6 locale: intro mergeable/three-gates 문단 + Key Features 항목(en/ja) + 특징·실행 흐름 renumber(md/ko) + es/zh 동등 반영.

## Spec Reference

**Primary Sources**

- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-claude-code-port.md` (Phase 2 #133)
- 대응 upstream PR: `yongwoon/develop-with-llm` #133

**Summary**

#133의 핵심 reliability 수정을 단일 skill에 적용한다. early-exit 버그(comment 0건 시 CI·conflict gate 건너뜀)를 차단하고, gate를 정수 Step으로 승격하며, Definition of Done으로 3-gate를 명문화한다. README는 6 locale 전부(es/zh 이미 존재 → 편집).

**Out of Scope (from spec)**

- executor(parallel/sequential) 변경은 `000029-030` 담당.
- `codex/**` 미접촉.

## Criticality

`normal` — instruction/doc 편집만 수행. CI·conflict 처리 *절차*를 서술하지만 보안 코드 surface를 변경하지 않는다.

## Dependencies

**Depends On**: (없음 — root)

**Depended By**: (없음)

## Key Files

- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.{md,en,es,ja,ko,zh}.md`

## Notes

- toolkit의 `SKILL.md:59`는 기존 `tools/claude-code/skills/...` 경로(pre-existing)를, `:177`는 이미 `claude-code/skills/...`를 사용한다. 변경된(+) 줄만 적용하고 unchanged context 줄은 toolkit 현재 상태 그대로 둔다(`tools/` prefix 정합화는 별건).
- 적용 후 Step 번호가 1–9 연속이고 DoD의 CI=Step7 / conflict=Step8와 일치하는지 grep 검증.
- 예상 증분 ~30줄 → 현재 206줄에서 ~236줄(cap 500 여유).

## Out of Scope

- executor·agentic·onboard·spec 계열 skill.
- `references/pr-conflict-resolution.md` 자체 변경(참조만, 변경 아님).

## Parallel Execution Metadata

**Ownership**: `claude-code/skills/ywc-handle-pr-reviews/**`

**Shared Surfaces**: `bash scripts/validate.sh` + markdownlint CI 게이트.

**Conflicts With**: (None identified)

**Parallelizable After**: 즉시(root).

**Task Verify**

- `rg -n "Definition of Done" claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `rg -n "run on EVERY invocation|EVERY invocation" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (Step 7·8)
- `rg -n "### Step [1-9]:" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (1–9 연속)
- `rg -n "fix PR CI|PR conflict" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (frontmatter trigger)
- `ls claude-code/skills/ywc-handle-pr-reviews/README.{es,zh}.md`
