# 000082-080-test-trigger-cases-testing-misc

## Purpose

`ywc-gen-testcase`, `ywc-e2e-test-strategy`, `ywc-tdd-ritual`, `ywc-verify-done`, `ywc-auth-implement`, `ywc-setup-language`, `ywc-skill-author`, `ywc-incident-postmortem` (S8, 8개 skill)에 대해 독립적으로 소스된 positive/collision trigger case를 `evals/trigger-cases.json`에 추가하여 S1 coverage floor를 충족시킨다.

## Scope

- `000082-070`이 append한 결과 위에서 이어서 append한다 (Depends On 체인).
- FR-1(mining) → FR-2(fallback authoring) 순서로 이 8개 item 각각에 대해 case를 확보한다. Phase 000082에서 가장 item 수가 많은 task(Fix D 이후 총 9개 authoring task 중 최대).
- Fix C2/S/Z id-inventory, Fix E2/R mining filter, Fix F2 collision override, Fix A2/L/V dedup을 모두 적용한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-toolkit-eval-trigger-coverage.md` — FR-3 batch S8 item 목록, Iteration 1–4 amendment 전체
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` — canonical case 작성 규칙
- `.claude/skills/ywc-toolkit-eval/scripts/score.py:73-74,340-360` — coverage floor 상수와 `load_coverage()`

### Summary
S8은 testing/verification/misc 8개 skill로 서로 이질적이다(`ywc-gen-testcase` vs `ywc-e2e-test-strategy`, `ywc-tdd-ritual`, `ywc-verify-done` 등 테스트 계열 4개와 `ywc-auth-implement`/`ywc-setup-language`/`ywc-skill-author`/`ywc-incident-postmortem`는 서로 독립적인 도메인). Testing 4개 사이의 anti-trigger가 가장 조밀하다.

### Out of Scope (from spec)
- Codex-side `.codex/skills/ywc-codex-toolkit-eval` coverage — 별도 root
- `score.py`의 coverage floor 상수·banding formula·mechanical scorer 자체 변경 — read-only만
- 대상 skill의 `SKILL.md`/description 본문 수정 금지
- 이미 충분한 4개 skill 재검토 금지

## Criticality

`normal` — toolkit 자체 유지보수용 eval data이며 보안 keyword 경로가 아니다 (spec §Critical Surfaces: N/A). `ywc-auth-implement`는 대상 skill 이름에 "auth"가 있으나, 이 task가 편집하는 대상은 그 skill의 trigger case JSON일 뿐 실제 인증 코드가 아니다.

## Dependencies

### Depends On
- `000082-070-test-trigger-cases-durable-memory` — S1~S7 case가 append된 `trigger-cases.json` 상태

### Depended By
- `000082-090-test-trigger-cases-agents` — 동일 파일에 이어서 append

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` — 8개 item에 대한 새 case를 `cases` 배열에 append

## Notes
- **Fix F2 override(verbatim)**: "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."
- Collision sibling은 반드시 같은 root(skill↔skill)에서만 고른다. 8개 중 4개(테스트 계열)는 서로가 서로의 가장 강력한 sibling 후보이므로 이 task 내부에서 우선 소진한다.
- Mining tool/filter는 `000082-010`과 동일(Fix E2/Fix R).
- id 번호는 Fix C2 prefix query + Fix S/Z fallback 병행.
- dedup: 기존 381개 + `000082-010/020/030/040/050/060/070`이 append한 case, 그리고 이 task 자신의 output과 대조. item 수가 많으므로(8개) 자기 자신의 output 내부 dedup을 특히 꼼꼼히 수행한다.
- 3 positive를 못 만드는 item은 Fix G exception 후보로 기록, category (a)/(b) evidence 첨부. 이전 batch(`000082-010`)의 dry-run 비율(Implementation Notes)을 참고해 fallback authoring 분량을 미리 가늠한다.

## Out of Scope
- `codex/skills/ywc-codex-toolkit-eval` 및 `.codex/**` 편집 금지
- `score.py` / `evals/scorecard.md` / `evals/history.json` 편집 금지
- 대상 skill의 `SKILL.md` / `description` / README 편집 금지
- 새 script, 새 dependency 추가 금지

## Parallel Execution Metadata

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (append-only, `cases` 배열만)

### Shared Surfaces
- `evals/trigger-cases.json` 전체

### Conflicts With
- 이 batch의 다른 모든 task — Depends On 체인이 순차 실행을 강제한다.

### Parallelizable After
- `000082-070-test-trigger-cases-durable-memory`

### Task Verify
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-gen-testcase --format json` → `signals.coverage.sufficient == true`
- 동일 명령을 `ywc-e2e-test-strategy`, `ywc-tdd-ritual`, `ywc-verify-done`, `ywc-auth-implement`, `ywc-setup-language`, `ywc-skill-author`, `ywc-incident-postmortem`에 대해 반복
- id 중복 없음 확인 (AC7)
- `description-derived` source 신규 추가 0건 (AC3)
