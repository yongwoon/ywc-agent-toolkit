# 000007-020-test-trigger-coverage

## Purpose

`ywc-codex-toolkit-eval`의 trigger evaluation 기준을 Codex agent 축과 일치시키고, `trigger-cases.json` coverage를 deterministic하게 검증한다. 특히 evaluator 자신(`ywc-codex-toolkit-eval`)은 문서화된 최소 fixture 기준인 positive 3개와 impostor/collision 2개를 만족해야 한다.

## Scope

- `references/trigger-eval-method.md`의 `S1 / A2` 및 Claude activation wording을 Codex metadata wording으로 고친다.
- `evals/trigger-cases.json`에 `ywc-codex-toolkit-eval` collision/impostor coverage를 보강한다.
- `test_score.py` 또는 작은 helper 함수에 trigger coverage counting test를 추가한다.
- broad catalog under-coverage는 task report에서 보이게 하되, 전체 catalog expansion은 이 task의 hard gate로 만들지 않는다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-3-correct-trigger-evaluation-terminology` - axis/wording correction
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-4-add-trigger-fixture-coverage-checks` - coverage checker requirements
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac5---trigger-axis-docs-are-correct` - trigger docs acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac6---trigger-coverage-checker-exists` - checker acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac7---evaluator-target-coverage-is-enforceable` - evaluator target coverage
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac8---broad-catalog-under-coverage-is-visible-without-blocking-unrelated-fixes` - broad under-coverage policy
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#operative-sections` - amended verification precedence

### Summary

The trigger-evaluation reference currently labels agent routing as `A2`, but the agent rubric uses `A1` for routing and `A2` for TOML structure. The same reference also mentions Claude auto-trigger behavior in a Codex-only evaluator. This task fixes that terminology and adds tests/fixtures so trigger coverage gaps are visible and the evaluator's own activation cases satisfy the documented minimum.

### Out of Scope (from spec)

- Scorer CLI mode and item filtering - handled by `000007-010-infra-score-cli-contract`
- README locale and `SKILL.md` usage surfaces - handled by `000008-010-infra-eval-surface-validation`
- Full expansion of all 46 currently under-covered catalog items - explicitly deferred by the spec

## Dependencies

### Depends On

- `000007-010-infra-score-cli-contract` - owns initial `test_score.py` changes and stabilizes focused test suite

### Depended By

- `000008-010-infra-eval-surface-validation` - documents the finalized trigger and fixture behavior

## Key Files

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md` - axis and Codex terminology
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json` - tracked trigger fixtures
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py` - coverage regression tests
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py` - only if a reusable coverage helper belongs in runtime code

## Notes

- `.gitignore` ignores new files under the internal evaluator `evals/` directory, but `trigger-cases.json` is already tracked and can be edited.
- Count positive coverage by `expected == item`.
- Count collision/impostor coverage by `impostor == item`.
- Do not require full catalog coverage unless the implementation deliberately expands the task beyond this spec.

## Parallel Execution Metadata

### Ownership

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py` only for trigger coverage helper code

### Shared Surfaces

- Internal evaluator trigger fixture schema
- Internal evaluator unittest suite
- Codex skill/agent routing rubric terminology

### Conflicts With

- `000007-010-infra-score-cli-contract` - overlaps on `test_score.py`
- `000008-010-infra-eval-surface-validation` - should document this task's final terminology after merge

### Parallelizable After

- `000007-010-infra-score-cli-contract`

### Task Verify

- `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `! rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`
- `python3 -m json.tool tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json >/dev/null`

## Out of Scope

- Full activation judge implementation
- Full catalog trigger fixture expansion
- README locale edits
