# 000082-090-test-trigger-cases-agents

## Purpose

`ywc-architect`, `ywc-backend-coder`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-doc-writer`, `ywc-cloud-engineer`, `ywc-refactor-cleaner`, `ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`, `ywc-performance-engineer`, `ywc-root-cause-analyst`, `ywc-security-engineer` (A1, 13개 agent — Fix D 이후 agents는 단일 batch)에 대해 독립적으로 소스된 positive/collision trigger case를 `evals/trigger-cases.json`에 추가하여, A2(agent dispatch accuracy, weight 25/100) 측정을 가로막는 coverage floor를 충족시킨다.

## Scope

- `000082-080`이 append한 결과 위에서 이어서 append한다 (Depends On 체인). Phase 000082의 마지막 authoring task.
- **AC8 요건**: 13개 agent 전부를 이 하나의 task에서 처리한다(2-batch 분할 금지 — Fix D가 원래 FR-4의 A1/A2 2-batch 분할을 폐기한 이유).
- **Open Question 1 처리(사용자 결정: dispatch-trigger text를 독립 source로 허용)**: agent dispatch는 대부분 프로그램적(`Task(subagent_type=...)`)이라 사용자가 직접 typing하지 않는다. caller skill의 실제 dispatch-trigger 문장을 session-trace와 동등한 독립 source로 취급한다.
- Fix C2/S/Z id-inventory, Fix E2/R mining filter(agent용으로 확장), Fix F2 collision override, Fix A2/L/V dedup을 모두 적용한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-toolkit-eval-trigger-coverage.md` — Fix D(FR-4 단일 batch로 수정), Iteration 1–4 amendment 전체(특히 Fix T — AC2 exception carve-out, Fix Q/Fix J — Open Question 1 해소는 Fix D로 이미 처리됨)
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md:20` — "Collision siblings must share a root" (agent는 agent끼리만 collision)
- `.claude/skills/ywc-toolkit-eval/scripts/score.py:73-74,340-360` — coverage floor 상수와 `load_coverage()`

### Summary
Reviewer 계열 6개(`go-reviewer`/`python-reviewer`/`typescript-reviewer`/`performance-engineer`/`root-cause-analyst`/`security-engineer`)와 implementer 계열 7개(`architect`/`backend-coder`/`frontend-coder`/`qa-engineer`/`doc-writer`/`cloud-engineer`/`refactor-cleaner`)로 나뉜다. 각 agent의 `.md` 정의 자체(`claude-code/agents/*.md`)의 "Triggers:" 절, 그리고 이 agent를 `Task(subagent_type=...)`로 dispatch하는 `claude-code/skills/**/SKILL.md` 본문의 자연어 trigger phrase가 이 task의 주 mining 대상이다.

### Out of Scope (from spec)
- Codex-side `.codex/agents` coverage — 별도 root, 이 plan 범위 밖
- `score.py`의 coverage floor 상수·banding formula·mechanical scorer 자체 변경 — read-only만
- 대상 agent의 `.md` 정의(description, Triggers) 본문 수정 — 이 task는 trigger-case JSON만 authoring한다
- skill↔agent collision 작성 — root가 다르므로 애초에 무효 (`trigger-eval-method.md:20`)

## Criticality

`normal` — toolkit 자체 유지보수용 eval data이며 auth/payment/token 등 보안 keyword 경로가 아니다 (spec §Critical Surfaces: N/A). `ywc-security-engineer`는 대상 agent 이름에 "security"가 있으나, 편집 대상은 그 agent의 trigger case JSON일 뿐 실제 보안 코드가 아니다.

## Dependencies

### Depends On
- `000082-080-test-trigger-cases-testing-misc` — S1~S8 case가 append된 `trigger-cases.json` 상태

### Depended By
- `000083-010-infra-toolkit-eval-coverage-rerun` — 이 task를 포함한 Phase 000082 전체 완료가 최종 검증의 입력

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` — 13개 agent에 대한 새 case를 `cases` 배열에 append

## Notes
- **Fix F2 override(verbatim)**: "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."
- **Collision siblings must share a root** (`trigger-eval-method.md:20`) — 이 13개 agent끼리만 collision을 만든다. 다른 batch(S1~S8)의 skill과는 collision을 만들지 않는다.
- **Dispatch-trigger source (Open Question 1)**: `claude-code/skills/**/SKILL.md` 전체를 grep해 `Task(subagent_type=<agent>)`를 실제로 유발하는 자연어 trigger 문장(agent 자신의 description을 재서술한 것이 아니라, 호출을 유발하는 caller skill의 실제 조건문)을 찾는다. 발견 시 `"source": "session-trace"`로 기록하고 `note`에 어느 caller skill/조건에서 왔는지 남긴다. agent 자신의 `.md` 정의(description, Triggers 절)를 그대로 옮기면 description-derived로 간주되어 배제된다 — caller skill 쪽 문구여야 한다.
- Mining tool/filter는 `000082-010`과 동일(Fix E2/Fix R)하되, 위 dispatch-trigger 확장을 추가로 적용한다.
- id 번호는 Fix C2 prefix query + Fix S/Z fallback 병행 — 기존 `agent-tsreviewer-vs-pyreviewer-1`처럼 agent 계열은 `agent-` 접두어를 쓰는 경우가 있으므로(Fix Z) prefix 후보를 두 가지(`<slug>-`, `agent-<slug>-`)로 모두 조회한다.
- dedup: 기존 381개 + `000082-010`~`000082-080`이 append한 case, 그리고 이 task 자신의 output(13개 item)과 대조.
- **AC12**: 어떤 agent가 exception으로 빠지면 AC2 목표는 `13 − |agent exceptions|`로 조정된다(Fix T). exception 후보는 Fix G와 동일한 evidence 요건(Fix W)을 따른다.
- 3 positive를 못 만드는 agent는 Fix T exception list 후보로 기록, category (a)/(b) evidence 첨부. Open Question 1 확장을 적용해도 진짜 mineable 이력이 0인 agent가 있을 수 있음(FR-1 note: "likely for most agents") — 그 경우가 category (a)의 전형적 예다.

## Out of Scope
- `codex/agents/**` 편집 금지 (별도 root)
- `score.py` / `evals/scorecard.md` / `evals/history.json` 편집 금지
- 대상 agent의 `.md` 정의 편집 금지
- 새 script, 새 dependency 추가 금지
- skill↔agent collision case 작성 금지 (root mismatch)

## Parallel Execution Metadata

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (append-only, `cases` 배열만)

### Shared Surfaces
- `evals/trigger-cases.json` 전체

### Conflicts With
- 이 batch의 다른 모든 task — Depends On 체인이 순차 실행을 강제한다.

### Parallelizable After
- `000082-080-test-trigger-cases-testing-misc`

### Task Verify
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-architect --format json` → `signals.coverage.sufficient == true`
- 동일 명령을 나머지 12개 agent(`ywc-backend-coder`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-doc-writer`, `ywc-cloud-engineer`, `ywc-refactor-cleaner`, `ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`, `ywc-performance-engineer`, `ywc-root-cause-analyst`, `ywc-security-engineer`)에 대해 반복
- id 중복 없음 확인 (AC7)
- `description-derived` source 신규 추가 0건 (AC3)
- 이 task 하나가 13개 agent 전부를 커버함을 확인 (AC8 — 2-batch 분할 아님)
