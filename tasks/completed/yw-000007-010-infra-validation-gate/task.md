# yw-000007-010-infra-validation-gate — Implementation Checklist

## Prerequisites
- [ ] `yw-000006-010-docs-task-generator-artifacts-sync` is completed and merged.
- [ ] `yw-000006-020-docs-executor-consumer-sync` is completed and merged.
- [ ] `yw-000006-030-docs-branch-testcase-consumer-sync` is completed and merged.

## Allowed Edit Scope
- [ ] Modify only the toolkit-eval baseline artifacts, and only when a score shift is justified by this batch's SKILL.md edits.

## Stop Conditions
- [ ] Stop and route to the owning task if a gate failure originates in a file this task does not own.
- [ ] Stop if the toolkit-eval score drops for a reason the SKILL.md edits do not explain — do not overwrite the baseline to make a real regression disappear.
- [ ] Stop if markdownlint findings come from `docs/ywc-plans/**`, which is outside the CI scope and not a gate.

## Hardening Gate
- [ ] Record the actual output of all five gate commands, not a summary.
- [ ] Record the before/after per-axis eval scores when the baseline is regenerated, with a one-line justification per moved axis.
- [ ] Confirm re-running `score.py --ci` after regeneration leaves a clean tree.

## Implementation Steps
- [ ] Run `bash scripts/validate.sh` and record the output.
- [ ] Run `bash scripts/install.sh --list` and record the output.
- [ ] Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` and record the per-axis comparison against the committed baseline.
- [ ] If any axis moved, determine whether the movement is explained by this batch's five SKILL.md edits; if it is not, stop and route the finding to the owning task.
- [ ] If the movement is justified, regenerate the baseline and scorecard, commit them together, and re-run `score.py --ci` to confirm a clean tree.
- [ ] Write the CI markdownlint config to a temporary file: `printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD060":false,"MD041":false}' > /tmp/ml.json`.
- [ ] Run `npx markdownlint-cli2 --config /tmp/ml.json "README*.md" "CONTRIBUTING*.md" "claude-code/skills/*/README*.md" "codex/skills/*/README*.md"` and record the output.
- [ ] Run `shellcheck` on `claude-code/skills/ywc-task-generator/scripts/next-task-number.sh` and `claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh`, plus any other `.sh` this batch changed under `claude-code/skills/**/scripts/`.
- [ ] Confirm the pre-commit hook did not trigger a `plugins/ywc-agent-toolkit` sync, since this batch touches only `claude-code/`.
- [ ] Spot-check the end-to-end result: generate one scratch task set with initials resolved and confirm the directory name matches `^yk-[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$` (AC2), then discard the scratch output.

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0
- [ ] `bash scripts/install.sh --list` exits 0
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0
- [ ] markdownlint with the CI config and globs exits 0
- [ ] `shellcheck` exits 0 on each changed shell script
- [ ] AC2 spot check: the scratch task directory name matches the prefixed pattern

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] markdownlint passes with the CI config and scope
- [ ] typecheck passes (N/A — no typed source in this repository)
- [ ] unit tests pass (toolkit-eval mechanical gate)
- [ ] app builds without error (N/A — documentation/tooling repository)

## Implementation Notes

Gate run on `feature/collaborator-initials` with all seven preceding tasks merged.
No behavioral change was required — every gate passed as found, so this task's diff
is limited to this evidence record.

| AC9 gate | Result |
|---|---|
| `bash scripts/validate.sh` | exit 0 — `58 items, no mechanical regression. PASS` |
| `bash scripts/install.sh --list` | exit 0 |
| `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` | exit 0 — `61 items, no mechanical regression. PASS` |
| markdownlint (CI config + CI globs, 570 files) | exit 0 — `0 issues in 0 files` |
| `shellcheck` on each changed shell file (5 files) | exit 0 on all five |

| Feature harness | Result |
|---|---|
| `tests/next-task-number-test.sh` | PASS |
| `tests/task-id-parsers-test.sh` | PASS |
| `tests/build-pr-title-test.sh` | PASS |

AC2 spot check: `scaffold-task-dir.sh yk-000042-010-api-send-invite` produced
`yk-000042-010-api-send-invite`, matching `^[a-z0-9]{2,4}-[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$`.

**Baseline regeneration was NOT required.** The toolkit-eval mechanical gate reported no
regression despite this feature editing several SKILL.md files, so the committed baseline
still holds. It was deliberately not regenerated — doing so without a measured drop would
have masked future movement rather than recording it. The `--ci` run also notes 1 of 61
items below the coverage minimum; that is pre-existing and unrelated to this feature.

**Escalated, not fixed here (out of scope — "any behavioral change"):** nothing in CI or
`scripts/validate.sh` executes the three test harnesses this feature added, and
`.github/workflows/validate.yml` limits shellcheck to `scandir: ./scripts`, so the five
changed shell files under `claude-code/skills/**` are not covered by CI either. Both gaps
were verified locally here, but they will silently rot without a CI owner. Route to a
follow-up task.
