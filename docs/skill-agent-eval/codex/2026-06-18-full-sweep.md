# Codex Skill/Agent Evaluation - 2026-06-18 - full sweep

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | full sweep (`--target all`) |
| Assets evaluated | 48 (41 skills, 7 agents) |
| Gate failures | 0 |
| Lowest carried-forward grade | B / 3.47 (`codex/skills/ywc-create-pr`) |

## Gate Summary

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Result: PASS.
skill_count=41, agent_count=7, skill_gate_passed=true, agent_gate_failures=0.
skills_missing_openai_yaml=[], skills_incomplete_locale_readmes=[].
Embedded validation mirror passed, including Codex plugin package staleness and mechanical regression checks.
```

## Mechanical Scorecard

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --mode mechanical --format markdown
Result: PASS mechanically, partial only.
codex/skills: 41 items. codex/agents: 7 items.
All agents score 60.0/60.0 on mechanical axes.
Lowest skill mechanical score remains 51.25/57.0 on skills with S5=3 and S7=3.
```

Mechanical mode is partial. Skill judgment axes S1, S4, and S8, plus agent
judgment axes A1, A3, and A8, are rendered as `.` in mechanical output and are
not replaced by mechanical points in this report.

## CI Baseline

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci
[ci] 48 items, no mechanical regression. PASS
```

## Judgment Scoring Notes

This sweep does not claim a fresh full manual judgment re-score for every
asset. It records fresh mechanical evidence from 2026-06-18 and carries forward
the latest human judgment grades from the 2026-06-16 report and scoreboard.
The result is therefore `PASS_WITH_ACTIONS`, not plain `PASS`.

| Axis | Treatment | Evidence |
|---|---|---|
| S1 Trigger and anti-trigger precision | Carried forward unless a later task edits the skill wording. | 2026-06-16 report and current scoreboard remain the judgment source of record. |
| S4 Workflow actionability | Carried forward. | No workflow behavior was changed by this report task. |
| S8 Scope discipline | Carried forward. | No scope-boundary changes were introduced by this report task. |
| A1 Routing description | Carried forward. | Agent TOML files pass structure and install gates; no routing text changed yet. |
| A3 Mission and boundaries | Carried forward. | Agent mission/boundary scoring remains from the scoreboard. |
| A8 Behavioral evidence | Carried forward with action. | All agents remain mechanically complete, but A8 still depends on smoke or eval evidence. |

## Fresh Mechanical Findings

### S5 Output and Verification Contract

The fresh mechanical run still shows S5=3 for these skills:

- `ywc-agentic`
- `ywc-brainstorm`
- `ywc-code-gen`
- `ywc-confidence-gate`
- `ywc-debug-rootcause`
- `ywc-e2e-test-strategy`
- `ywc-finish-branch`
- `ywc-plan`
- `ywc-refactor-clean`
- `ywc-spec-ready`
- `ywc-task-generator`
- `ywc-tdd-ritual`
- `ywc-ubiquitous-language`
- `ywc-verify-done`

The current improvement cycle prioritizes objective fixture candidates:
`ywc-spec-ready`, `ywc-verify-done`, `ywc-finish-branch`, `ywc-agentic`, and
`ywc-brainstorm`.

### S7 Codex Runtime Fit

The fresh mechanical run shows S7=3 for these skills:

- `ywc-code-gen`
- `ywc-commit`
- `ywc-confidence-gate`
- `ywc-finish-branch`
- `ywc-handle-pr-reviews`
- `ywc-merge-dependabot`
- `ywc-onboard-repo`
- `ywc-parallel-executor`
- `ywc-plan`
- `ywc-receive-review`
- `ywc-refactor-clean`
- `ywc-tdd-ritual`

This cycle prioritizes frequently invoked or executor-adjacent skills:
`ywc-plan`, `ywc-code-gen`, `ywc-finish-branch`, `ywc-refactor-clean`, and
`ywc-tdd-ritual`.

### A8 Behavioral Evidence

All 7 Codex agents pass mechanical gates with 60.0/60.0 mechanical points.
Their A8 grade is still evidence-limited because no current smoke fixture
harness proves behavioral examples for read-only reviewer-style agents.

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `codex/skills/ywc-code-gen` | skill | A | 3.51 | S5=3, S7=3 | Carried forward from scoreboard; fresh mechanical run still reports 51.25/57.0. |
| `codex/skills/ywc-finish-branch` | skill | A | 3.77 | S5=3, S7=3 | Carried forward; selected for both S7 wording and S5 fixture follow-up. |
| `codex/skills/ywc-plan` | skill | A | 3.67 | S7=2 carried-forward judgment; fresh mechanical S7=3 and S5=3 | Carried forward; selected for S7 wording follow-up because both scoreboard judgment and fresh mechanical evidence flag runtime-fit work. |
| `codex/skills/ywc-refactor-clean` | skill | A | 3.77 | S5=3, S7=3 | Carried forward; selected for S7 wording follow-up. |
| `codex/skills/ywc-tdd-ritual` | skill | A | 3.77 | S5=3, S7=3 | Carried forward; selected for S7 wording follow-up. |
| `codex/skills/ywc-spec-ready` | skill | A | 3.87 | S5=3 | Carried forward; selected for objective eval fixture follow-up. |
| `codex/skills/ywc-verify-done` | skill | A | 3.87 | S5=3 | Carried forward; selected for objective eval fixture follow-up. |
| `codex/skills/ywc-agentic` | skill | A | 3.77 | S5=3 | Carried forward; selected for objective eval fixture review. |
| `codex/skills/ywc-brainstorm` | skill | A | 3.77 | S5=3 | Carried forward; selected for objective eval fixture review. |
| `codex/agents/*.toml` | agent | A | 3.92 or better | A8=3 evidence limitation across all 7 agents | Carried forward; mechanical gates all pass. |

## Priority Backlog

1. [Medium] `codex/skills/ywc-plan`, `ywc-code-gen`, `ywc-finish-branch`, `ywc-refactor-clean`, `ywc-tdd-ritual` - tighten S7 Codex runtime wording.
   Evidence: fresh mechanical score reports S7=3 for each selected target.
   Owner: Codex skill authoring polish.
   Re-score target: S7 -> 4 where wording can be clarified without behavior changes.
2. [Medium] `codex/skills/ywc-spec-ready`, `ywc-verify-done`, `ywc-finish-branch`, `ywc-agentic`, `ywc-brainstorm` - add objective S5 eval fixtures or record omission reasons.
   Evidence: fresh mechanical score reports S5=3 for each selected target.
   Owner: skill owners.
   Re-score target: S5 -> 4 when a deterministic fixture is suitable.
3. [Medium] `codex/agents/*.toml` - document a bounded A8 behavioral evidence strategy.
   Evidence: agent mechanical gates pass, but A8 remains a judgment axis without smoke/eval artifacts.
   Owner: Codex agent evaluation docs.
   Re-score target: A8 -> 4 only after fixture or smoke evidence exists and passes.

## Decisions

- No evaluator scoring code or mechanical baseline was changed in this task.
- No scoreboard movement is claimed here; the scoreboard update belongs to the next task and must cite this report.
- No Codex skill, Codex agent, generated plugin, `.claude/**`, or `claude-code/**` files were edited by this report task.
- Judgment-sensitive axes are carried forward explicitly to avoid presenting mechanical PASS as final quality.

## Next Cycle

- Recommended scope: execute the remaining tasks in this batch: scoreboard update, S7 wording polish, S5 fixtures, A8 evidence strategy, then sync and validation.
- Highest-priority item: complete evidence-backed S7/S5/A8 improvements without broadening beyond Codex eval surfaces.
- Mechanical baseline update needed: no.
