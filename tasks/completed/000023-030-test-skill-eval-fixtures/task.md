# Task: 000023-030-test-skill-eval-fixtures

## Prerequisites
- [ ] Read `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-6-add-skill-eval-fixtures-or-omission-reasons`.
- [ ] Read `codex/skills/ywc-skill-author/SKILL.md` around the `evals/evals.json` expectation.
- [ ] Confirm the target skill directories exist under `codex/skills/`.

## Allowed Edit Scope
- `codex/skills/ywc-confidence-gate/evals/**`
- `codex/skills/ywc-debug-rootcause/evals/**`
- `codex/skills/ywc-docker-isolate/evals/**`
- `codex/skills/ywc-e2e-test-strategy/evals/**`
- `codex/skills/ywc-onboard-repo/evals/**`
- `codex/skills/ywc-plan/evals/**`
- `codex/skills/ywc-refactor-clean/evals/**`
- `codex/skills/ywc-spec-writer/evals/**`
- `codex/skills/ywc-tdd-ritual/evals/**`
- Generated plugin counterparts for the listed eval files after `bash scripts/sync-codex-plugin.sh`

## Stop Conditions
- [ ] Stop if an eval case would require live browser, Docker, network, app server, or repository mutation to be objectively verified.
- [ ] Stop if a target skill needs body changes outside eval files; report whether that should move to `000023-040-docs-codex-skill-contracts`.
- [ ] Stop if `bash scripts/sync-codex-plugin.sh` produces generated diffs outside the touched skill eval counterparts.

## Implementation Steps

### Review fixture suitability
- [ ] Inspect each target `SKILL.md` for deterministic trigger, output, and anti-behavior expectations.
- [ ] Classify each target as `fixture-added` or `omission-needed` with a short reason.
- [ ] Prefer objective string/status/template checks over style judgments.

### Add objective eval files
- [ ] For each `fixture-added` target, create `codex/skills/<skill>/evals/evals.json`.
- [ ] Include at least two positive cases and one anti-behavior case when practical.
- [ ] Keep inputs bounded and free of secrets, local absolute paths, and live system dependencies.
- [ ] Ensure fixture names and expected behavior match the skill's actual output contract.

### Sync generated plugin package
- [ ] Run `bash scripts/sync-codex-plugin.sh` after source eval files are added.
- [ ] Inspect generated plugin diffs and confirm they only mirror the intended source eval additions.
- [ ] Record any `omission-needed` target and reason for the final report task.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `git diff --name-only`

## Verification
- [ ] Source Codex skill eval files exist for every `fixture-added` target.
- [ ] Generated plugin counterparts match source changes only.
- [ ] `bash scripts/validate.sh` passes.
