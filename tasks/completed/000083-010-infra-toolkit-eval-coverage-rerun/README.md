# 000083-010-infra-toolkit-eval-coverage-rerun

## Purpose

Batch 19의 9개 authoring task(`000082-010`~`000082-090`)가 모두 머지된 후, catalog 전체 coverage를 재확인하고 judgment-tier 전체 재평가를 실행해 AC1/AC2/AC5/AC6/AC10/AC11/AC12/AC13을 검증한다. 이 task 자체는 새 trigger case를 작성하지 않는다 — read + 재실행 + 문서화만 한다.

## Scope

- FR-6 step 1: catalog-wide coverage check (`score.py --target all --format json`)
- FR-6 step 1a (Fix O): 신규 작성 case 대상 duplicate-prompt 재확인 (legitimate positive/collision cross-citation 예외 포함)
- FR-6 step 2 (Fix Q): `/ywc-toolkit-eval --mode full --target all` 재실행으로 `57 − |exceptions|` item의 실제 S1/A2 점수 확보
- FR-6 step 3: 새 `history.json` entry를 2026-08-12 baseline과 diff — measured count(48/13, exception만큼 차감), 4개 기존 skill 무회귀(AC6) 확인
- FR-6 step 4: `scorecard.md` 재생성 + 다음 개선 cycle을 위한 prioritized backlog 산출(이 task 범위 밖 — 산출물만)
- Fix G/T exception list 최종 검토(AC11/AC12/AC13): category (a) 항목만 남아있는지, evidence가 첨부됐는지 확인

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-toolkit-eval-trigger-coverage.md` — FR-6(Fix B/Fix H/Fix J/Fix Q로 수정된 최종본), AC1/AC2/AC5/AC6/AC7/AC10/AC11/AC12/AC13(Operative Sections 우선순위표 기준 최신 Fix 적용)
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` — 2026-08-12 baseline scorecard (44/13 unmeasured 목록의 출처)
- `.claude/skills/ywc-toolkit-eval/evals/history.json` — 이 task의 재실행 결과가 diff될 대상
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`, `agent-rubric.md` — S1/A2 band 표

### Summary
이 task는 Batch 19의 마지막 hard gate다. 9개 authoring task가 append한 결과를 catalog 전체 관점에서 검증하고, 실제 judgment-tier 점수를 얻는다. `history.mechanical.json`은 이 task와 무관하다 — S1/A2는 judgment-tier이며 mechanical baseline(`{S2,S4,S5}`)에 저장되지 않는다.

### Out of Scope (from spec)
- 새로 드러난 backlog 항목에 대한 실제 fix 작업 — 다음 개선 cycle의 입력일 뿐, 이 task 범위 밖
- `.codex/skills/ywc-codex-toolkit-eval` 재평가 — 별도 root
- `score.py`의 coverage floor 상수·banding formula·mechanical scorer 자체 변경

## Criticality

`normal` — toolkit 자체 유지보수용 eval 재실행이며 보안 keyword 경로가 아니다 (spec §Critical Surfaces: N/A).

## Dependencies

### Depends On
- `000082-010-test-trigger-cases-planning-core` — S1 case
- `000082-020-test-trigger-cases-spec-execution` — S2 case
- `000082-030-test-trigger-cases-devenv` — S3 case
- `000082-040-test-trigger-cases-iac-infra` — S4 case
- `000082-050-test-trigger-cases-review-quality` — S5 case
- `000082-060-test-trigger-cases-git-release` — S6 case
- `000082-070-test-trigger-cases-durable-memory` — S7 case
- `000082-080-test-trigger-cases-testing-misc` — S8 case
- `000082-090-test-trigger-cases-agents` — A1 case (13개 agent 전부)

### Depended By
- (None — Batch 19 종단. 산출된 backlog는 다음 improvement cycle의 별도 plan 입력이 된다)

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` (read-only)
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` (재생성)
- `.claude/skills/ywc-toolkit-eval/evals/history.json` (append — 새 entry)

## Notes
- `history.mechanical.json`은 이 task와 무관하다 — S1/A2는 judgment-tier이며 mechanical baseline(`{S2,S4,S5}`)에 저장되지 않는다(`score.py` 주석: "signals-only, never axes"). `--ci` 실행 불필요/금지 — 실행하면 아무 의미 없는 mechanical 재baseline만 만든다.
- AC5/FR-6 step 2는 Fix Q에 따라 `57 − |exceptions|`로 목표를 조정한다. 정확한 exception 개수는 9개 authoring task의 Implementation Notes를 취합해 결정한다.
- AC11(process-failure 항목이 exception list에 없어야 함), AC12(agent exception이 있으면 AC2 목표도 `13 − |agent exceptions|`로 조정), AC13(모든 exception entry에 evidence 첨부) 모두 이 task에서 최종 확인한다.
- Fix H/J의 remediation은 이미 각 authoring task 내부에서 1회 완료되었어야 한다 — 이 task는 최종 확인만 하고, 새로운 remediation을 시작하지 않는다(무한 루프 방지).

## Out of Scope
- 새 backlog 항목에 대한 실제 fix 작업(다음 cycle)
- `.codex/**` 재평가
- `trigger-cases.json`에 새 case 추가

## Parallel Execution Metadata

### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md`
- `.claude/skills/ywc-toolkit-eval/evals/history.json`
- (read-only) `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`

### Shared Surfaces
- 없음 — 이 task가 이 batch의 유일한 마지막 writer

### Conflicts With
- `000082-010`~`000082-090` (선행 완료 전 실행 불가)

### Parallelizable After
- `000082-010`, `000082-020`, `000082-030`, `000082-040`, `000082-050`, `000082-060`, `000082-070`, `000082-080`, `000082-090` (전부)

### Task Verify
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` → stderr `[coverage] 0 items below minimum` (또는 기록된 exception만 명명)
- `/ywc-toolkit-eval --mode full --target all` (judgment-tier 재실행 — 이 task의 마지막 단계)
- `evals/history.json` 신규 entry의 `roots.<root>.measured` == `48 − |skill exceptions|` (skills) / `13 − |agent exceptions|` (agents)
