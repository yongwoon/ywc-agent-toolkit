# 000023-030-test-skill-eval-fixtures

## Purpose

Resolve missing objective `evals/evals.json` coverage for the Codex skill targets listed in the spec, or produce evidence-backed omission data for cases that cannot be verified locally in this cycle.

## Scope

- Review each listed Codex skill for objectively checkable trigger/output behavior.
- Add `evals/evals.json` with at least two positive cases and one anti-behavior case where practical.
- Avoid browser, app-server, Docker, or live-repository assumptions inside fixtures.
- Run Codex skill sync after source skill changes and keep generated plugin diffs aligned.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-6-add-skill-eval-fixtures-or-omission-reasons` — target skill list and fixture rules.
- `codex/skills/ywc-skill-author/SKILL.md` — project expectation that objectively verifiable outputs should have eval fixtures.
- `AGENTS.md#testing-guidelines` — required validation commands.
- `codex/AGENTS.md` — source/generated Codex skill sync rule.

### Summary
Nine Codex skills currently lack objective fixture coverage. This task adds local `evals/evals.json` files where the behavior can be checked without live external dependencies. Any skill that remains unsuitable for objective fixtures must have a concrete omission reason ready for the final evaluation report.

### Out of Scope (from spec)
- S5 contract cleanup for `ywc-agentic` and `ywc-finish-branch` — handled by `000023-040-docs-codex-skill-contracts`.
- Progressive disclosure extraction — handled by `000023-040-docs-codex-skill-contracts`.
- Final report wording and scoreboard movement — handled by `000024-010-docs-eval-report-scoreboard`.

## Dependencies

### Depends On
- (None) — can start from the current base branch.

### Depended By
- `000023-040-docs-codex-skill-contracts` — should run after this task to avoid overlapping Codex skill sync churn.
- `000024-010-docs-eval-report-scoreboard` — needs fixture coverage results and omission reasons.

## Key Files
- `codex/skills/ywc-confidence-gate/evals/evals.json`
- `codex/skills/ywc-debug-rootcause/evals/evals.json`
- `codex/skills/ywc-docker-isolate/evals/evals.json`
- `codex/skills/ywc-e2e-test-strategy/evals/evals.json`
- `codex/skills/ywc-onboard-repo/evals/evals.json`
- `codex/skills/ywc-plan/evals/evals.json`
- `codex/skills/ywc-refactor-clean/evals/evals.json`
- `codex/skills/ywc-spec-writer/evals/evals.json`
- `codex/skills/ywc-tdd-ritual/evals/evals.json`
- `plugins/ywc-agent-toolkit/skills/**` generated counterparts after sync

## Notes

- Keep fixtures narrow and deterministic. The goal is not to simulate a full repository or browser session.
- If a skill is omitted, capture the exact reason in the task completion notes so `000024-010-docs-eval-report-scoreboard` can write it into the report.
- Do not patch generated plugin files manually; run `bash scripts/sync-codex-plugin.sh` after source edits.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-confidence-gate/evals/**`
- `codex/skills/ywc-debug-rootcause/evals/**`
- `codex/skills/ywc-docker-isolate/evals/**`
- `codex/skills/ywc-e2e-test-strategy/evals/**`
- `codex/skills/ywc-onboard-repo/evals/**`
- `codex/skills/ywc-plan/evals/**`
- `codex/skills/ywc-refactor-clean/evals/**`
- `codex/skills/ywc-spec-writer/evals/**`
- `codex/skills/ywc-tdd-ritual/evals/**`
- Generated plugin counterparts for the listed skill eval files only

### Shared Surfaces
- Codex skill fixture coverage.
- Generated plugin package sync.

### Conflicts With
- `000023-040-docs-codex-skill-contracts` — both may run Codex skill sync and touch generated plugin counterparts.

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex`

## Out of Scope

- Editing `SKILL.md` bodies except for minimal fixture-discovered corrections that are required to make an objective fixture meaningful.
- Changing evaluator rubric weights.
- Creating fixtures that require network, browser automation, Docker, or live app state.
