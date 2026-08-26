# Task: Codex Eval Sync and Validation Gate

## Summary

Synchronize generated Codex plugin output and run all required validation gates for the improvement cycle.

## Implementation Steps

- [ ] Confirm implementation tasks are merged.
  - Related AC/FR: AC6, AC7, AC8, FR-6
  - Contract / Behavior Change: This task starts only after all Phase `000020` tasks are complete.
  - Verification Command / Evidence: Check branch history or task completion markers before running sync.
- [ ] Run generated plugin sync.
  - Related AC/FR: AC6, FR-6
  - Contract / Behavior Change: Generated plugin diffs must correspond to changed `codex/skills/**` source files.
  - Verification Command / Evidence: `bash scripts/sync-codex-plugin.sh` followed by `git diff --name-only`.
- [ ] Run repository and install validation.
  - Related AC/FR: AC7, FR-6
  - Contract / Behavior Change: Required repo validation and Codex install scans must exit 0.
  - Verification Command / Evidence: `bash scripts/validate.sh`, `bash scripts/install.sh --list --codex`, and `bash scripts/install.sh --list --codex-agents`.
- [ ] Run evaluator CI baseline.
  - Related AC/FR: AC7, FR-6
  - Contract / Behavior Change: Mechanical scorer CI must remain regression-free.
  - Verification Command / Evidence: `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci`.
- [ ] Check scope boundary.
  - Related AC/FR: AC8, FR-6
  - Contract / Behavior Change: Final diff contains no `.claude/**`, `claude-code/**`, product code, dependency churn, or manual generated plugin edits.
  - Verification Command / Evidence: `git diff --name-only`.

## Task Verify

```bash
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
bash scripts/install.sh --list --codex
bash scripts/install.sh --list --codex-agents
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci
git diff --name-only
```

Expected Passing Signal:

- All commands exit 0.
- Generated plugin output is synced from source.
- Final diff respects the Codex-only scope boundary.

Pre-change Failing Evidence / Exception:

- Before this gate, generated plugin output may be stale after `codex/skills/**` edits and validation has not been rerun across the completed batch.

Contract/Test Evidence:

- Command outputs provide the acceptance evidence for AC6, AC7, and AC8.

## Out of Scope

- New quality improvements unrelated to making validation pass.
- Reverting unrelated user changes.
