# 000007-010-infra-score-cli-contract

## Purpose

`ywc-codex-toolkit-eval`의 deterministic scorer CLI 계약을 spec과 일치시킨다. `--mode mechanical`은 기존 scorer와 같은 결과를 내고, 지원하지 않는 `judge/full` mode와 존재하지 않는 `--item`은 조용히 성공하지 않도록 명확히 실패한다.

## Scope

- `score.py`에 `--mode` argument를 추가하고 backward compatibility를 유지한다.
- `--item`이 target root에서 0개 asset과 매칭될 때 non-zero exit와 명확한 stderr를 반환한다.
- `test_score.py`에 mode, missing item, targeted hit regression test를 추가한다.
- 기존 `--ci`, `--update-baseline`, `--format json|markdown`, `--target` 동작을 보존한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-1-implement-or-reconcile---mode` - `--mode` 계약
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-2-fail-loudly-on-missing---item` - missing item 실패 계약
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac1----mode-contract-works` - mechanical mode acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac2---unsupported-modes-are-explicit` - unsupported mode acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac3---targeted-miss-fails` - missing item acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac4---targeted-hit-still-works` - targeted hit acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#operative-sections` - Iteration 1 amendment precedence

### Summary

The scorer currently supports target and item filtering mechanically, but `--mode` is documented without parser support and `--item` misses can return an empty successful scorecard. This task makes the CLI deterministic: mechanical mode is supported, unsupported modes are explicit, and missing item filters fail. Later tasks depend on this stable CLI behavior for documentation and final verification.

### Out of Scope (from spec)

- Trigger fixture coverage and trigger reference wording - handled by `000007-020-test-trigger-coverage`
- README locale and `SKILL.md` surface alignment - handled by `000008-010-infra-eval-surface-validation`
- Full judge/full orchestration implementation - out of scope unless explicitly chosen while satisfying AC2

## Dependencies

### Depends On

- (None - root task)

### Depended By

- `000007-020-test-trigger-coverage` - reuses and may extend `test_score.py`
- `000008-010-infra-eval-surface-validation` - documents the finalized CLI behavior and runs final validation

## Key Files

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py` - CLI parsing and item target filtering
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py` - focused regression tests

## Notes

- Preserve omitted `--mode` as equivalent to `--mode mechanical`.
- Do not make `judge/full` silently behave like mechanical unless the documentation explicitly says they are aliases. The smaller compatible path is to fail non-zero with a clear message that `score.py` is deterministic mechanical-only.
- A missing `--item` should fail only when the user supplied `--item`; roots with no items and no filter can still render `_No items found._`.

## Parallel Execution Metadata

### Ownership

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`

### Shared Surfaces

- Internal evaluator CLI contract
- Internal evaluator Python unittest suite
- Mechanical regression gate invoked by `scripts/validate.sh`

### Conflicts With

- `000007-020-test-trigger-coverage` - both may edit `test_score.py`
- `000008-010-infra-eval-surface-validation` - should wait for finalized CLI contract before documenting it

### Parallelizable After

- (Root task - no predecessor required)

### Task Verify

- `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown`
- `! python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json`

## Out of Scope

- Editing `README*.md` or `SKILL.md` in this task
- Expanding trigger fixtures
- Updating mechanical baseline unless this task intentionally changes reviewed mechanical scores
