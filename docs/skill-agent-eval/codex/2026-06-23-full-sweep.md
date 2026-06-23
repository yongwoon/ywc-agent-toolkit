# Codex Skill/Agent Evaluation - 2026-06-23 - full sweep

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | full sweep (`--target all`) |
| Assets evaluated | 48 (41 skills, 7 agents) |
| Gate failures | 0 |
| Score movement claimed | Agent A8 only; skills stay carried-forward composites pending judgment re-score |

## Gate Summary

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Exit code: 0.
Result: PASS.
skill_count=41, agent_count=7, skill_gate_passed=true, agent_gate_failures=0.
skills_missing_openai_yaml=[], skills_incomplete_locale_readmes=[].
```

Additional final validation:

| Command | Exit code | Result |
|---|---:|---|
| `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py` | 0 | 18 tests passed |
| `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci` | 0 | `[ci] 48 items, no mechanical regression. PASS` |
| `bash scripts/validate.sh` | 0 | All checks passed |
| `bash scripts/install.sh --list --codex` | 0 | Listed 41 Codex skills |
| `bash scripts/install.sh --list --codex-agents` | 0 | Listed 7 Codex agents |

No final-task Codex source files changed, so `scripts/sync-codex-plugin.sh` was not rerun for this report task. The completed implementation tasks already synced generated plugin copies after their Codex source edits.

## Mechanical Scorecard

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --mode mechanical --format markdown
Exit code: 0.
Result: PASS mechanically, partial only.
codex/skills: 41 items. codex/agents: 7 items.
All agents score 60.0/60.0 on mechanical axes.
38/41 skills have no deterministic axis below 4.
The remaining deterministic skill gaps are S5=3 on:
- ywc-code-gen
- ywc-task-generator
- ywc-ubiquitous-language
S7 remains 3 on:
- ywc-commit
- ywc-confidence-gate
- ywc-handle-pr-reviews
- ywc-merge-dependabot
- ywc-onboard-repo
- ywc-parallel-executor
- ywc-receive-review
```

Mechanical mode is partial. Skill judgment axes S1, S4, and S8, plus agent judgment axes A1, A3, and A8, are rendered as `.` by the scorer. This report uses the smoke evidence below to update A8, but it does not claim a fresh full judgment re-score for skill composites.

## Agent Smoke Evidence

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py --fixtures tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json --outputs tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output
Exit code: 0.
Summary: 13/13 passed
```

Fixture path: `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json`

Captured output path pattern: `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/<agent>/<fixture>.md`

| Agent | Passing fixtures | Captured outputs |
|---|---:|---|
| `ywc-architect` | 2 | `architect-happy-module-boundary.md`, `architect-boundary-security-route.md` |
| `ywc-security-engineer` | 2 | `security-happy-output-escaping.md`, `security-boundary-architecture-route.md` |
| `ywc-root-cause-analyst` | 1 | `root-cause-happy-ranked-hypotheses.md` |
| `ywc-performance-engineer` | 3 | `performance-happy-query-plan.md`, `performance-boundary-security-route.md`, `performance-missing-budget.md` |
| `ywc-typescript-reviewer` | 2 | `typescript-happy-async-error.md`, `typescript-boundary-go-route.md` |
| `ywc-python-reviewer` | 2 | `python-happy-resource-lifecycle.md`, `python-readonly-discipline.md` |
| `ywc-go-reviewer` | 1 | `go-happy-error-wrapping.md` |

A8 rubric decision: move A8 from 3 to 4 for all seven agents. Each agent now has executable bounded behavioral evidence, at least one captured output, a passing validator command, and no forbidden signals in the harness result. The composite movement is +0.08, so agent rows move from A / 3.92 to A / 4.00.

## Skill Fixture Coverage

Task `000023-030-test-skill-eval-fixtures` closed the missing objective fixture coverage for these Codex skills and plugin counterparts:

- `codex/skills/ywc-confidence-gate/evals/evals.json`
- `codex/skills/ywc-debug-rootcause/evals/evals.json`
- `codex/skills/ywc-docker-isolate/evals/evals.json`
- `codex/skills/ywc-e2e-test-strategy/evals/evals.json`
- `codex/skills/ywc-onboard-repo/evals/evals.json`
- `codex/skills/ywc-plan/evals/evals.json`
- `codex/skills/ywc-refactor-clean/evals/evals.json`
- `codex/skills/ywc-spec-writer/evals/evals.json`
- `codex/skills/ywc-tdd-ritual/evals/evals.json`

The final inventory shows all 41 Codex skills now have `evals/evals.json`. No omission reason is needed for the `000023-030` target list because every targeted fixture file was added and validated. Skill score movement is not claimed in this report because the scorer run is mechanical-only and no fresh S1/S4/S8 judgment pass was performed.

## S5, S7, And Progressive Disclosure

Task `000023-040-docs-codex-skill-contracts` resolved the targeted S5 output-contract gaps:

| Skill | 2026-06-18 state | 2026-06-23 mechanical state |
|---|---|---|
| `ywc-agentic` | S5=3 | S5=4, S7=4, 57.0/57.0 mechanical points |
| `ywc-finish-branch` | S5=3, S7=3 | S5=4, S7=4, 57.0/57.0 mechanical points |

Progressive-disclosure review found no extraction needed for the executor-adjacent skills. The final mechanical run reports S3=4 for `ywc-gen-testcase`, `ywc-parallel-executor`, `ywc-plan`, `ywc-sequential-executor`, and `ywc-task-generator`. `ywc-parallel-executor` and `ywc-sequential-executor` are near the 500-line body threshold at 499 body lines each in scorer output, so they remain watch-list items but are not failing S3.

## Scoreboard Decisions

| Asset group | Decision | Evidence |
|---|---|---|
| All 7 Codex agents | Move current score from A / 3.92 to A / 4.00 | Agent smoke fixture path, captured output files, command exit code 0, 13/13 pass, A8 rubric decision above |
| Skills with newly resolved S5/S7 mechanical gaps | Update weakest-dimension and next-action text only | Mechanical command exit code 0 and scorecard summary above; no fresh full skill judgment re-score |
| `ywc-code-gen`, `ywc-task-generator`, `ywc-ubiquitous-language` | Keep score and S5 action | Final mechanical score still reports S5=3 |
| `ywc-commit`, `ywc-confidence-gate`, `ywc-handle-pr-reviews`, `ywc-merge-dependabot`, `ywc-onboard-repo`, `ywc-parallel-executor`, `ywc-receive-review` | Keep score and S7 action | Final mechanical score still reports S7=3 |

## Decisions

- No evaluator scoring code or mechanical baseline was changed in this task.
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/history.mechanical.json` was not regenerated.
- No Codex skill, Codex agent, generated plugin, `.claude/**`, or `claude-code/**` files were edited by this report task.
- Scoreboard agent movement is evidence-backed by fixture paths, captured output paths, command exit code, and the A8 rubric decision.
- Skill composites are carried forward until a separate judgment pass updates S1/S4/S8.

## Next Cycle

1. Re-score skill judgment axes for rows whose deterministic S5/S7 gaps are now resolved.
2. Address remaining S5=3 skills: `ywc-code-gen`, `ywc-task-generator`, and `ywc-ubiquitous-language`.
3. Address remaining S7=3 skills: `ywc-commit`, `ywc-confidence-gate`, `ywc-handle-pr-reviews`, `ywc-merge-dependabot`, `ywc-onboard-repo`, `ywc-parallel-executor`, and `ywc-receive-review`.
