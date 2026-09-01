# 000082-020-test-trigger-cases-spec-execution

## Purpose

`ywc-spec-ready`, `ywc-task-generator`, `ywc-agentic`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-code-gen` (S2, 6개 skill)에 대해 독립적으로 소스된(session-trace 또는 user-prompt) positive/collision trigger case를 `evals/trigger-cases.json`에 추가하여, S1(skill activation accuracy, weight 30/100) 측정을 가로막는 coverage floor(`positives >= 3`, `collisions >= 2`)를 충족시킨다.

## Scope

- `000082-010`이 append한 결과 위에서 이어서 append한다 (Depends On 체인으로 single-writer invariant 보장).
- FR-1(mining) → FR-2(fallback authoring) 순서로 이 6개 item 각각에 대해 case를 확보한다.
- `000082-010`의 Implementation Notes에 기록된 dry-run 비율을 참고해 fallback authoring 부하를 미리 가늠한다.
- Fix C2/S/Z id-inventory, Fix E2/R mining filter, Fix F2 collision override, Fix A2/L/V dedup을 모두 적용한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-toolkit-eval-trigger-coverage.md` — FR-3 batch S2 item 목록, Iteration 1–4 amendment 전체(Operative Sections 우선순위표 기준 최신 Fix 적용)
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` — canonical case 작성 규칙. Global Constraints: 이 문서를 재서술/재해석하지 않는다.
- `.claude/skills/ywc-toolkit-eval/scripts/score.py:73-74,340-360` — coverage floor 상수와 `load_coverage()`

### Summary
S2는 spec 수렴과 실행 orchestration 계층으로, `ywc-plan`(S1)과 `ywc-code-gen`/`ywc-agentic` 사이 anti-trigger가 자주 얽힌다. `ywc-sequential-executor` vs `ywc-parallel-executor`가 이 batch 내부의 가장 직접적인 collision 쌍이다.

### Out of Scope (from spec)
- Codex-side `.codex/skills/ywc-codex-toolkit-eval` coverage — 별도 root, 이 plan 범위 밖
- `score.py`의 coverage floor 상수·banding formula·mechanical scorer 자체 변경 — read-only로만 사용
- 대상 skill의 `SKILL.md`/description 본문 수정 — 이 task는 trigger-case JSON만 authoring한다
- 이미 충분한 4개 skill(`ywc-commit`, `ywc-create-pr`, `ywc-debug-rootcause`, `ywc-handle-pr-reviews`) 재검토

## Criticality

`normal` — 편집 대상은 toolkit 자체 유지보수용 eval data이며 auth/payment/token 등 보안 keyword 경로가 아니다 (spec §Critical Surfaces: N/A).

## Dependencies

### Depends On
- `000082-010-test-trigger-cases-planning-core` — S1 6개 item의 case가 이미 append된 `trigger-cases.json` 상태(dedup 대조 기준선), Implementation Notes의 dry-run 비율

### Depended By
- `000082-030-test-trigger-cases-devenv` — 동일 파일에 이어서 append

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` — 6개 item에 대한 새 case를 `cases` 배열에 append (구조 변경 없음, append-only)

## Notes
- **Fix F2 override(dispatch prompt에 verbatim 포함 필수)**: "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."
- Collision sibling은 반드시 같은 root(skill↔skill)에서만 고른다. S2의 anti-trigger sibling이 S1(예: `ywc-plan`)에 있어도 이 task가 대신 작성한다(Fix I).
- Mining tool 및 filter는 `000082-010`과 동일(Fix E2/Fix R).
- id 번호는 Fix C2(`<slug>` = `ywc-` 접두어 제거형) prefix query 우선, Fix S/Z fallback(hit < 3 시 `expected`/`impostor` 필드 기반 query) 병행.
- dedup(Fix A2 step 4a + Fix L + Fix V): 신규 case를 (i) 기존 381개 + `000082-010`이 append한 case, (ii) 이 task 자신의 output 내 다른 case와 대조. legitimate positive+collision pair는 예외.
- 어떤 item이 mining+fallback을 모두 거쳐도 3개의 non-circular positive를 만들 수 없으면 Fix G exception list 후보로 기록하고 category (a)/(b) evidence를 첨부한다(Fix M/W). category (b)는 exception 대상이 아니라 버그로 재수정한다.

## Out of Scope
- `codex/skills/ywc-codex-toolkit-eval` 및 `.codex/**` 편집 금지
- `score.py` / `evals/scorecard.md` / `evals/history.json` 편집 금지 (최종 재검증은 `000083-010`)
- 대상 skill의 `SKILL.md` / `description` / README 편집 금지
- 새 script, 새 dependency 추가 금지

## Parallel Execution Metadata

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (append-only, `cases` 배열만)

### Shared Surfaces
- `evals/trigger-cases.json` 전체 — 이 batch의 모든 10개 task가 같은 파일에 append한다.

### Conflicts With
- 이 batch의 다른 모든 task(`000082-010`, `000082-030`~`000082-090`, `000083-010`) — Depends On 체인이 순차 실행을 강제한다.

### Parallelizable After
- `000082-010-test-trigger-cases-planning-core`

### Task Verify
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-spec-ready --format json` → `signals.coverage.sufficient == true`
- 동일 명령을 `ywc-task-generator`, `ywc-agentic`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-code-gen`에 대해 반복
- `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); ids=[c['id'] for c in d['cases']]; assert len(ids)==len(set(ids))"` — AC7 id 중복 없음
- `git diff .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json | grep -c '"source": "description-derived"'` → `0`
