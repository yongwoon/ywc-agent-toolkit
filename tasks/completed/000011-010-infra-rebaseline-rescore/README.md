# 000011-010-infra-rebaseline-rescore

## Purpose
Phase 000010 의 모든 편집(FR1–FR8)이 머지된 후, 기계 기준선을 재생성하고 전체 재채점을 수행하여 의도한 항목이 상승하고 무관 항목이 하락하지 않았음을 검증한다(FR9).

## Scope
- `score.py --ci` 로 무회귀 확인 + `history.mechanical.json` 재기준선화(상향만: A2 캡 해제, parallel-executor S4 3→5)
- `ywc-toolkit-eval --mode full --target all` 전체 재채점 → `evals/scorecard.md` 재생성, `evals/history.json` 행 추가
- 8개 대상 항목 상승, 무관 항목 무하락 확인

## Spec Reference
### Primary Sources
- `docs/ywc-plans/ywc-toolkit-activation-fixes.md` — FR9, AC1/AC4/AC6, Amendment A6(S5 포인터 검증)
### Summary
편집은 모두 상향(캡 해제, S4 회복)이므로 `--ci` 는 PASS 하나, 저장 축이 바뀌므로 기준선 재생성이 필요하다(000009-010 의 원자적 재기준선과 동일 규율). 재기준선 전 각 편집 항목의 `unresolved_anti_trigger_pointers` 가 빈 리스트인지 확인(신규 `use ywc-*` 포인터가 실존 형제로 해소됨, A6).
### Out of Scope (from spec)
- 소스/스킬/에이전트 편집(→ Phase 000010)
- Codex 미러 — 후속 plan

## Dependencies
### Depends On
- `000010-010-docs-reviewer-anti-triggers`
- `000010-020-docs-agent-dispatch-boundaries`
- `000010-030-docs-skill-anti-triggers`
- `000010-040-refactor-parallel-executor-extraction`
### Depended By
- (없음)

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (재생성)
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` (재생성)
- `.claude/skills/ywc-toolkit-eval/evals/history.json` (행 추가)

## Notes
- **Phase 하드 게이트:** Phase 000010 의 4개 태스크가 모두 머지된 후에만 시작(편집이 부분만 반영된 채 재기준선화하면 기준선이 불완전).
- `evals/` 는 gitignore 대상이나 history.mechanical.json/scorecard.md/history.json 은 이미 추적됨 → `git add` 정상 동작.
- 재기준선 diff 는 상향(A2 4→5 캡 해제분, S4 3→5)만이어야 함; 하락 발생 시 중단·조사.

## Out of Scope
- 모든 description/본문 편집(Phase 000010 소관)

## Parallel Execution Metadata
- **Ownership:** `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`, `.claude/skills/ywc-toolkit-eval/evals/scorecard.md`, `.claude/skills/ywc-toolkit-eval/evals/history.json`
- **Shared Surfaces:** history.mechanical.json(CI `validate.yml`/score.py --ci 가 읽음)
- **Conflicts With:** (None identified) — Phase 000010 이후 단독 실행
- **Parallelizable After:** `000010-010`, `-020`, `-030`, `-040` 전부 머지 후
- **Task Verify:**
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` PASS(무회귀) 후 기준선 재생성, diff 가 상향만
  - `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` → 리뷰어 3종 `a2_collision_cap == null`, parallel-executor S4==5, 50항목 무오류
  - `bash scripts/validate.sh` 통과
