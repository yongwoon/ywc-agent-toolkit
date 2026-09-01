# 000004-030-test-trigger-fixture-coverage

## Purpose

Codex toolkit evaluator의 trigger fixture coverage를 확장하여 모든 evaluated Codex skill과 agent가 최소 하나의 positive trigger case를 갖도록 한다.

## Scope

- `trigger-cases.json`에 39개 Codex skill과 7개 Codex agent의 positive case 추가 또는 보강
- high-overlap sibling group에 collision case 추가
- 기존 case는 명확히 잘못된 경우가 아니면 보존
- JSON ordering과 case id convention을 deterministic하게 유지

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-5-expand-trigger-fixture-coverage` — trigger fixture coverage 요구사항
- `docs/ywc-plans/codex-toolkit-eval-improvements.validation.md#warning-issues` — reference ideal 대비 잔여 Warning
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md` — trigger evaluation method

### Summary

이 task는 S1/A1 judgment uncertainty를 낮추기 위해 trigger fixture를 확장한다. Spec의 minimum target은 모든 evaluated item에 positive case 하나 이상과 high-risk group collision coverage다. 가능하면 reference ideal인 3 positive / 2 collision에 가까워지되, 이번 batch의 acceptance criterion을 넘는 과도한 fixture expansion은 피한다.

### Out of Scope (from spec)
- Skill body contract 보강 — `000004-010-refactor-skill-s5-contracts`에서 처리
- Agent caller/status 보강 — `000004-020-refactor-agent-integration-status`에서 처리
- Trigger coverage helper script 작성 — validation report Suggestion이며 이번 task의 필수 범위 아님

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000005-010-test-evaluation-report-refresh` — final evaluation report에서 trigger fixture coverage를 설명해야 함

## Key Files

| 파일 | 변경 유형 |
|---|---|
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json` | positive / collision cases 추가 |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md` | 필요 시 fixture convention과 실제 JSON이 불일치할 때만 최소 수정 |

## Notes

- Prompt는 synthetic keyword list가 아니라 실제 user request처럼 작성한다.
- Collision case는 sibling skill이 잘못 activate되지 않아야 하는 상황을 검증해야 한다.
- Current fixture는 16 cases이므로 coverage expansion 후 count와 item coverage를 직접 확인한다.

## Parallel Execution Metadata

### Ownership
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`

### Shared Surfaces
- Internal evaluator fixture schema
- Trigger activation evidence for S1/A1 judgment pass

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 -m json.tool tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json >/dev/null`
- `bash scripts/validate.sh`

## Out of Scope

- Implementing a new trigger coverage analyzer script
- Changing evaluator scoring model or baseline
- Rewriting existing trigger cases for style only
