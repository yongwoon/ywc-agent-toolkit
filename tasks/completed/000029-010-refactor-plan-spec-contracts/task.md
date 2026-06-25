# Task: 000029-010-refactor-plan-spec-contracts

## Prerequisites

- [ ] `feature/port-dwl-skill-drift-20260624` (또는 batch 단일 branch)에서 작업 중인지 확인
- [ ] upstream 참조 diff 확보: `gh pr diff 132 --repo yongwoon/develop-with-llm`, `… 134`, `… 140` (claude-code 경로만)
- [ ] 대상 skill의 "before" 상태 확인: `ywc-spec-validate`에 `PROCEED (≥ 90) | DONE` 단일 행 + `Critical/High/Medium/Low` 표기, `ywc-spec-writer`에 `claude-opus-4-7` 존재

## Allowed Edit Scope

- `claude-code/skills/ywc-plan/**`
- `claude-code/skills/ywc-create-pr/{SKILL.md, README.*.md}` (`evals/` 제외)
- `claude-code/skills/ywc-spec-validate/**`
- `claude-code/skills/ywc-spec-writer/{SKILL.md, references/full-gen-workflow.md}`
- 그 외 경로 편집 금지 (특히 `codex/**`, `plugins/**`, 다른 skill).

## Stop Conditions

- spec-validate의 #134 영역과 #140 영역이 예상과 달리 겹치거나 "before" 상태가 upstream과 불일치하면 중단·보고.
- `ywc-create-pr`에 이미 `### 6.5` 또는 Self-Review Gate가 존재하면 중단(중복 적용 방지).
- es/zh README가 누락된 skill을 만나면 중단·보고(이 task의 세 skill은 es/zh 존재 가정).

## Implementation Steps

- [ ] `ywc-plan/SKILL.md` Step 5: 기존 "Never proceed past the handoff" 3-step 텍스트를 `ywc-spec-ready` opt-in y/n prompt 블록으로 교체(y→`/ywc-spec-ready <path>` 즉시 실행, n/`--non-interactive`→manual 3단계 안내).
- [ ] `ywc-plan/SKILL.md` Validation 체크리스트: "Did not execute the next downstream skill" 줄을 opt-in `ywc-spec-ready` 문구로 갱신.
- [ ] `ywc-plan/SKILL.md` Integration: Medium/Large downstream 줄에 `ywc-spec-ready (auto-converge shortcut) or …` 반영.
- [ ] `ywc-plan/README.{md,en,es,ja,ko,zh}.md`: Related Skills에 `ywc-spec-ready` 줄 추가 + `ywc-spec-validate`를 "manual next step"으로 재서술(es/zh는 en 기준 번역).
- [ ] `ywc-create-pr/SKILL.md`: Rationalization Defense에 "I generated this code … just file the PR" 1행 추가.
- [ ] `ywc-create-pr/SKILL.md`: `### 7. Create PR` 앞에 `### 6.5. Author Self-Review Gate (mandatory)` 신설 — `git diff <base-branch>...HEAD` + 5행 점검 표(intent traceability / debug residue / drive-by edit / secrets / convention fit) + `ywc-impl-review` 위임 note.
- [ ] `ywc-create-pr/README.{md,en,es,ja,ko,zh}.md`: Key Features self-review 항목 + 실행 흐름 renumber(7=Self-Review Gate, 8=PR 생성).
- [ ] `ywc-spec-validate/SKILL.md` (#134): Rationalization 1행 + `--tasks` 인자 행 + `### Step 4c Cross-Artifact Consistency (Analyze)`(Requirement Coverage + Task Provenance 표) + Integration "Not applicable"→"Cross-artifact (Analyze)".
- [ ] `ywc-spec-validate/SKILL.md` (#140, 별도 edit): band-mapping 표를 `PROCEED ≥90, no Critical → DONE` / `PROCEED ≥90, Critical present → DONE_WITH_CONCERNS`로 분할 + confidence-gate §5 인용 + `Critical/High/Medium/Low`→`Critical/Warning/Suggestion`.
- [ ] `ywc-spec-validate/README.{md,en,es,ja,ko,zh}.md`: `/ywc-spec-validate --spec docs/specification/ --tasks tasks/` 예시 + Cross-Artifact note blockquote.
- [ ] `ywc-spec-writer/SKILL.md`: 본문 model 줄 + Model 출력 블록 줄 `claude-opus-4-7`→`claude-opus-4-8`.
- [ ] `ywc-spec-writer/references/full-gen-workflow.md`: priority `4-7 preferred / 4-5 fallback`→`4-8 preferred / 4-7 fallback`.

## Task Verify

- [ ] `rg -n "ywc-spec-ready" claude-code/skills/ywc-plan/SKILL.md` (>0)
- [ ] `rg -n "Author Self-Review Gate" claude-code/skills/ywc-create-pr/SKILL.md` (>0)
- [ ] `rg -n -- "--tasks <dir>|Cross-Artifact Consistency" claude-code/skills/ywc-spec-validate/SKILL.md` (>0)
- [ ] `rg -n "Critical/Warning/Suggestion" claude-code/skills/ywc-spec-validate/SKILL.md` (>0) 및 `! rg -n "Critical/High/Medium/Low" claude-code/skills/ywc-spec-validate/SKILL.md`
- [ ] `rg -n "claude-opus-4-8" claude-code/skills/ywc-spec-writer/SKILL.md` (>0)
- [ ] es/zh 존재 확인: `ls claude-code/skills/ywc-{plan,create-pr,spec-validate}/README.{es,zh}.md`
- [ ] SKILL.md line cap: `wc -l claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-spec-validate/SKILL.md` (각 ≤500)

## Verification

- [ ] `bash scripts/validate.sh` (frontmatter + 4-locale set + `--list` dry run 통과)
- [ ] markdownlint: `npx markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-plan/README*.md" "claude-code/skills/ywc-create-pr/README*.md" "claude-code/skills/ywc-spec-validate/README*.md"` (0 errors; CI config는 MD013/MD060 비활성)
- [ ] `git diff --name-only` 결과가 Allowed Edit Scope 내부로 한정되는지 확인(특히 `codex/` 미포함)
