# 000008-010-infra-eval-surface-validation - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000007-010-infra-score-cli-contract` is completed and merged.
- [ ] `000007-020-test-trigger-coverage` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md`.
- [ ] Stay within `tools/codex-internal/skills/ywc-codex-toolkit-eval/README*.md`.
- [ ] Remove only ignored local artifacts listed in `README.md`.
- [ ] Do not edit `codex/skills/**`, `.codex-plugin/skills/**`, `claude-code/**`, or `.claude/**`.

## Stop Conditions

- [ ] Stop if scorer behavior still conflicts with the intended README examples.
- [ ] Stop if docs require changing distributed Codex skills.
- [ ] Stop if validation requires release metadata edits.
- [ ] Stop if `ywc-codex-toolkit-eval` appears under `codex/skills/` or `.codex-plugin/skills/`.

## Implementation Steps

- [ ] Align `SKILL.md`.
  - [ ] Update the argument table to match implemented `--mode` behavior.
  - [ ] Clarify that `score.py` is deterministic mechanical scoring when `judge/full` are skill-mediated or unsupported by the script.
  - [ ] Update validation checklist text so expected non-zero/no-match checks are not described as plain success commands.
- [ ] Align README locale files.
  - [ ] Update `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md`.
  - [ ] Remove stale direct `$ywc-codex-toolkit-eval --mode full --target all` examples unless direct full mode is genuinely implemented.
  - [ ] Keep the internal-only placement warning in every locale.
- [ ] Clean ignored local artifacts if present.
  - [ ] Remove `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/__pycache__/`.
  - [ ] Remove ignored `evals/history.json` and `evals/scorecard.md` if present and not intentionally retained.
  - [ ] Confirm `git status --short --untracked-files=all` does not hide required tracked changes.
- [ ] Run final verification.
  - [ ] Run the amended verification command block from the spec.
  - [ ] Run `bash scripts/validate.sh`.
  - [ ] If `history.mechanical.json` changes, document why the baseline update is intentional.

## Task Verify

- [ ] `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown`
- [ ] `! python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json`
- [ ] `! rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`
- [ ] `! rg -n '\$ywc-codex-toolkit-eval --mode full' tools/codex-internal/skills/ywc-codex-toolkit-eval/README*.md`
- [ ] `test ! -e codex/skills/ywc-codex-toolkit-eval`
- [ ] `test ! -e .codex-plugin/skills/ywc-codex-toolkit-eval`
- [ ] `bash scripts/validate.sh`

## Verification

- [ ] Focused internal evaluator tests pass.
- [ ] Internal evaluator mechanical mode command passes.
- [ ] Missing item command fails as an assertion-shaped success.
- [ ] Stale trigger wording and stale README full-mode examples are absent.
- [ ] Full repository validation passes.
