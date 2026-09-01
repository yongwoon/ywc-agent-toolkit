# 000082-010-test-trigger-cases-planning-core

## Purpose

`ywc-plan`, `ywc-brainstorm`, `ywc-tech-research`, `ywc-confidence-gate`, `ywc-spec-writer`, `ywc-spec-validate` (S1, 6개 skill)에 대해 독립적으로 소스된(session-trace 또는 user-prompt) positive/collision trigger case를 `evals/trigger-cases.json`에 추가하여, S1(skill activation accuracy, weight 30/100) 측정을 가로막는 coverage floor(`positives >= 3`, `collisions >= 2`)를 충족시킨다.

## Scope

- 이 batch(Batch 19)의 root task. `evals/trigger-cases.json`에 직접 append하는 첫 task이므로 predecessor 없음.
- FR-1(mining) → FR-2(fallback authoring) 순서로 이 6개 item 각각에 대해 case를 확보한다.
- **Open Question 2 dry-run 겸용**: mining만으로 확보되는 positive/collision 비율을 Implementation Notes에 기록해, 이후 8개 task가 FR-2 fallback 부하를 가늠할 수 있게 한다(사용자 결정: 별도 dry-run task를 추가하지 않고 이 task에 접는다).
- Fix C2/S/Z id-inventory, Fix E2/R mining filter, Fix F2 collision override, Fix A2/L/V dedup을 모두 적용한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-toolkit-eval-trigger-coverage.md` — FR-3 batch S1 item 목록, Iteration 1–4 amendment 전체(Operative Sections 우선순위표에 따라 원문 대신 최신 Fix를 따른다: Fix A2/Fix X(FR-5), Fix C2/Fix S/Fix Z(id 규칙), Fix E2/Fix R(mining filter), Fix F2(collision), Fix G(AC1 exception), Fix M/Fix W(exception evidence), Fix N/Fix Y(AC9 regex), Fix O(AC10))
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` — canonical case 작성 규칙(case taxonomy, provenance/independence condition). Global Constraints: 이 문서를 재서술/재해석하지 않는다.
- `.claude/skills/ywc-toolkit-eval/scripts/score.py:73-74,340-360` — coverage floor 상수와 `load_coverage()` — 이 task의 Task Verify가 직접 대조하는 ground truth

### Summary
S1은 planning 단계 핵심 skill 6개로, 서로 anti-trigger로 자주 등장하는 cluster다(예: `ywc-plan` vs `ywc-brainstorm`, `ywc-tech-research` vs `ywc-plan`, `ywc-spec-writer` vs `ywc-spec-validate`). 이 task가 batch의 root이므로 mining 결과가 이후 fallback 부하를 가늠하는 dry-run 데이터가 된다.

### Out of Scope (from spec)
- Codex-side `.codex/skills/ywc-codex-toolkit-eval` coverage — 별도 root, 이 plan 범위 밖
- `score.py`의 coverage floor 상수·banding formula·mechanical scorer 자체 변경 — read-only로만 사용
- 대상 skill의 `SKILL.md`/description 본문 수정 — 이 task는 trigger-case JSON만 authoring한다
- 이미 충분한 4개 skill(`ywc-commit`, `ywc-create-pr`, `ywc-debug-rootcause`, `ywc-handle-pr-reviews`) 재검토

## Criticality

`normal` — 편집 대상은 toolkit 자체 유지보수용 eval data(`evals/trigger-cases.json`)이며 auth/payment/token 등 보안 keyword 경로가 아니다 (spec §Critical Surfaces: N/A).

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000082-020-test-trigger-cases-spec-execution` — 동일 파일에 이어서 append (Depends On 체인으로 single-writer invariant 보장)

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` — 6개 item에 대한 새 case를 `cases` 배열에 append (구조 변경 없음, append-only)

## Notes
- **Fix F2 override(dispatch prompt에 verbatim 포함 필수)**: "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."
- Collision sibling은 반드시 같은 root(skill↔skill)에서만 고른다 (`trigger-eval-method.md:20`). S1의 anti-trigger sibling이 S2/S5 등 다른 batch 소속이어도 무방하다(Fix I) — 이 task가 그 sibling의 case를 대신 작성해도 된다.
- Mining tool: `mcp__plugin_oh-my-claudecode_t__session_search`, `mcp__plugin_claude-mem_mcp-search__search`(`type: "prompts"`), fallback `grep` over `~/.claude/projects/**/*.jsonl`. Filter: Fix E2 rule 1–4 + Fix R(tool-output/데이터 덤프 제외) + Fix E2 rule 5(이 plan 문서·`trigger-eval-method.md` 등 reference doc 자체를 논의/재현하는 hit 제외).
- id 번호는 Fix C2(`<slug>` = `ywc-` 접두어 제거형) prefix query로 우선 조회하되, Fix S/Z에 따라 hit이 3개 미만이면 `expected`/`impostor` 필드 기반 fallback query도 함께 실행해 진짜 `max_n`을 구한다.
- dedup(Fix A2 step 4a + Fix L + Fix V): 이 task가 batch의 root이므로 기존 381개 case와만 대조하면 되고, 이 task 자신의 output 내부에서도 상호 대조한다. 완전/near-duplicate는 버리되, **legitimate positive+collision pair**(같은 prompt, 다른 kind, `expected`/`impostor`가 서로를 지칭)는 예외로 유지한다.
- **Open Question 2 (dry-run) 처리**: mining 완료 후, 이 6개 item의 mined positive/collision 개수와 필요 개수(3/2) 대비 비율을 Implementation Notes 최상단에 요약해 이후 task가 FR-2 fallback 부하를 가늠할 수 있게 한다.
- 어떤 item이 mining+fallback을 모두 거쳐도 3개의 non-circular positive를 만들 수 없으면(Edge Cases 시나리오), Fix G exception list 후보로 기록한다 — category (a) genuine content gap 인지 (b) process failure 인지 판단하고 증거(mining query 결과, FR-2 시도 로그, 또는 실패한 단계 trace)를 첨부한다(Fix M/W). category (b)는 exception 대상이 아니라 이 task 안에서 버그로 재수정한다.

## Out of Scope
- `codex/skills/ywc-codex-toolkit-eval` 및 `.codex/**` 편집 금지 (별도 root)
- `score.py` / `evals/scorecard.md` / `evals/history.json` 편집 금지 (read-only 사용만, 최종 재검증은 `000083-010`)
- 대상 skill의 `SKILL.md` / `description` / README 편집 금지
- 새 script, 새 dependency 추가 금지

## Parallel Execution Metadata

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (append-only, `cases` 배열만)

### Shared Surfaces
- `evals/trigger-cases.json` 전체 — 이 batch의 모든 10개 task가 같은 파일에 append한다.

### Conflicts With
- 이 batch의 다른 모든 task(`000082-020`~`000082-090`, `000083-010`) — Depends On 체인이 이미 순차 실행을 강제하므로 worktree 병렬 실행은 사용하지 않는다.

### Parallelizable After
- (Root task — 선행 불필요)

### Task Verify
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-plan --format json` → `signals.coverage.sufficient == true`
- 동일 명령을 `ywc-brainstorm`, `ywc-tech-research`, `ywc-confidence-gate`, `ywc-spec-writer`, `ywc-spec-validate`에 대해 반복
- `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); ids=[c['id'] for c in d['cases']]; assert len(ids)==len(set(ids))"` — AC7 id 중복 없음
- `git diff .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json | grep -c '"source": "description-derived"'` → `0` (AC3, 신규 case는 description-derived 금지)
