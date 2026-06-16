# 000008-010-infra-eval-surface-validation

## Purpose

Scorer and trigger behavior changes를 `ywc-codex-toolkit-eval`의 사용자-facing surface에 반영하고, ignored local artifacts를 정리한 뒤 repository validation으로 implementation batch를 닫는다.

## Scope

- `SKILL.md` argument table, workflow, validation checklist를 실제 scorer behavior와 맞춘다.
- `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md` usage examples를 최종 command contract와 맞춘다.
- stale direct `$ywc-codex-toolkit-eval --mode full` README example을 제거하거나 skill-mediated usage로 바꾼다.
- ignored local runtime artifacts가 있으면 정리한다.
- final validation command set을 실행한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-5-update-localized-readme-files` - README locale alignment
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#fr-6-clean-ignored-local-artifacts` - local artifact cleanup
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac9---readme-usage-examples-match-reality` - README acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac11---full-repo-validation-passes` - validation acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac12---no-internal-evaluator-leak` - internal-only boundary
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#ac13---ignored-local-artifacts-are-cleaned-if-present` - artifact cleanup acceptance
- `docs/ywc-plans/codex-toolkit-eval-improvements.md#iteration-1-amendments` - amended verification command block

### Summary

After the CLI and trigger fixture behavior is implemented, the skill body and README locale files must no longer show commands that fail against the actual scripts. This final task updates the documentation surface, cleans ignored artifacts if present, and runs the amended verification block plus repository validation. It is the hard gate before implementation can be considered complete.

### Out of Scope (from spec)

- CLI implementation - handled by `000007-010-infra-score-cli-contract`
- Trigger fixture and trigger reference implementation - handled by `000007-020-test-trigger-coverage`
- Distributed Codex skills under `codex/skills/**` - out of scope entirely
- Claude Code files and `.claude/**` - out of scope entirely

## Dependencies

### Depends On

- `000007-010-infra-score-cli-contract` - provides final scorer CLI behavior
- `000007-020-test-trigger-coverage` - provides final trigger terminology and fixture coverage behavior

### Depended By

- (None - final task)

## Key Files

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.en.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.ja.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.ko.md`
- Ignored local artifacts under `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/__pycache__/`
- Ignored local artifacts under `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/history.json`
- Ignored local artifacts under `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/scorecard.md`

## Notes

- Keep `ywc-codex-toolkit-eval` internal-only; do not copy it under `codex/skills/` or `.codex-plugin/skills/`.
- Do not add new frontmatter fields to `SKILL.md`.
- `docs/ywc-plans` is ignored, so this task should not rely on the plan/log files appearing in `git status`.
- If `history.mechanical.json` changes, update it only after reviewing the mechanical score output.

## Parallel Execution Metadata

### Ownership

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README*.md`
- Local ignored artifact paths listed in Key Files

### Shared Surfaces

- Internal evaluator user-facing documentation
- Repository validation gate
- Internal-only packaging boundary

### Conflicts With

- `000007-010-infra-score-cli-contract` - docs must wait for final CLI behavior
- `000007-020-test-trigger-coverage` - docs must wait for final trigger wording and fixture policy

### Parallelizable After

- `000007-010-infra-score-cli-contract`
- `000007-020-test-trigger-coverage`

### Task Verify

- `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown`
- `! python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json`
- `! rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`
- `! rg -n '\$ywc-codex-toolkit-eval --mode full' tools/codex-internal/skills/ywc-codex-toolkit-eval/README*.md`
- `test ! -e codex/skills/ywc-codex-toolkit-eval`
- `test ! -e .codex-plugin/skills/ywc-codex-toolkit-eval`
- `bash scripts/validate.sh`

## Out of Scope

- Functional scorer changes beyond documentation alignment
- Trigger fixture expansion
- Release metadata edits
- Distributed Codex package sync
