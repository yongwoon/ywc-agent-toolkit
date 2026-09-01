# 000005-010-test-evaluation-report-refresh

## Purpose

Skill, agent, and trigger fixture changes 이후 internal Codex evaluator를 다시 실행하고 post-improvement report와 scoreboard를 갱신한다.

## Scope

- `inventory_gate.py --json` 실행 결과 확인
- `score.py --format markdown --target all` 실행 결과 확인
- `bash scripts/validate.sh` 실행
- 새 dated report를 `docs/skill-agent-eval/codex/` 아래에 작성
- `docs/skill-agent-eval/codex/scoreboard.md`를 post-improvement 상태로 갱신

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-6-re-run-evaluation-and-refresh-reports` — final evaluation/report refresh 요구사항
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#acceptance-criteria` — 최종 acceptance criteria
- `docs/ywc-plans/codex-toolkit-eval-improvements.validation.md#completion-status` — task generation base spec 확인

### Summary

이 task는 앞선 implementation tasks의 결과를 검증하고 evaluation documentation을 최신화한다. Pre-change report는 보존하고, after state를 새 report로 남긴다. 최종 결과는 S5 target skills >= 3, target agents A7 >= 3, target agent warnings cleared, repository validation pass를 보여야 한다.

### Out of Scope (from spec)
- Evaluator scoring model 변경 — spec Out of Scope
- Mechanical baseline update with `--update-baseline` — 명시 review 없이는 제외
- 앞선 task에서 누락된 skill/agent 수정 직접 수행 — 누락 발견 시 해당 predecessor task로 되돌림

## Dependencies

### Depends On
- `000004-010-refactor-skill-s5-contracts` — S5 target skill changes 제공
- `000004-020-refactor-agent-integration-status` — A7/status warning changes 제공
- `000004-030-test-trigger-fixture-coverage` — trigger fixture coverage 제공

### Depended By
- (None — 이 task는 leaf task)

## Key Files

| 파일 | 변경 유형 |
|---|---|
| `docs/skill-agent-eval/codex/scoreboard.md` | post-improvement scoreboard 갱신 |
| `docs/skill-agent-eval/codex/<date>-post-improvement.md` | 새 evaluation report 작성 |

## Notes

- 기존 `2026-06-13-full-sweep.md`는 pre-change evidence이므로 보존한다.
- `inventory_gate.py --json`에서 target agent warning이 남으면 report를 쓰기 전에 predecessor task로 되돌린다.
- `score.py`에서 target S5 또는 A7이 acceptance criteria를 만족하지 못하면 report를 쓰기 전에 missing scorer bucket을 분석한다.

## Parallel Execution Metadata

### Ownership
- `docs/skill-agent-eval/codex/**`

### Shared Surfaces
- Evaluation report documentation
- Mechanical score and inventory gate output

### Conflicts With
- (None identified)

### Parallelizable After
- `000004-010-refactor-skill-s5-contracts`
- `000004-020-refactor-agent-integration-status`
- `000004-030-test-trigger-fixture-coverage`

### Task Verify
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
- `bash scripts/validate.sh`

## Out of Scope

- Editing source skill or agent files except to route a failed check back to its predecessor task
- Updating evaluator baseline without explicit review
- Removing or overwriting pre-change evaluation reports
