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
Initial embedded validation mirror passed at report creation time. Later source
edits in this batch can make the generated Codex plugin package stale until
`000021-010-infra-codex-eval-sync-validation` runs `scripts/sync-codex-plugin.sh`
and `scripts/validate.sh`.
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

The initial 2026-06-18 mechanical sweep identified S5=3 for these skills
before this batch's fixture update:

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

2026-06-18 fixture update: all five prioritized targets received objective
behavior fixtures. `ywc-spec-ready`, `ywc-verify-done`, `ywc-finish-branch`,
and `ywc-brainstorm` now have new `evals/evals.json` files; `ywc-agentic`
received an additional review-loop fixture. No omission reason is needed for
these five targets in this cycle. Mechanical S5 now reaches 4 for
`ywc-spec-ready`, `ywc-verify-done`, and `ywc-brainstorm`; `ywc-finish-branch`
and `ywc-agentic` remain S5=3 because their remaining S5 gap is in the broader
output/validation contract shape rather than fixture absence alone.

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
`tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md`
now defines the bounded read-only fixture shape, required smoke cases, and
per-agent-family signals for future A8 evidence. A8 remains evidence-limited
because the current evaluator still has no agent smoke harness that consumes and
passes those fixtures.

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `codex/skills/ywc-code-gen` | skill | A | 3.51 | S5=3, S7=3 | Carried forward from scoreboard; fresh mechanical run still reports 51.25/57.0. |
| `codex/skills/ywc-finish-branch` | skill | A | 3.77 | S5=3, S7=3 | Carried forward; received an objective fixture, but still needs broader output/validation contract work for S5. |
| `codex/skills/ywc-plan` | skill | A | 3.67 | S7=2 carried-forward judgment; fresh mechanical S7=3 and S5=3 | Carried forward; selected for S7 wording follow-up because both scoreboard judgment and fresh mechanical evidence flag runtime-fit work. |
| `codex/skills/ywc-refactor-clean` | skill | A | 3.77 | S5=3, S7=3 | Carried forward; selected for S7 wording follow-up. |
| `codex/skills/ywc-tdd-ritual` | skill | A | 3.77 | S5=3, S7=3 | Carried forward; selected for S7 wording follow-up. |
| `codex/skills/ywc-spec-ready` | skill | A | 3.87 | S5 fixture gap closed | Fixture update raises mechanical S5 to 4; no follow-up is tracked for this cycle. |
| `codex/skills/ywc-verify-done` | skill | A | 3.87 | S5 fixture gap closed | Fixture update raises mechanical S5 to 4; no follow-up is tracked for this cycle. |
| `codex/skills/ywc-agentic` | skill | A | 3.77 | S5=3 | Received an objective fixture, but still needs broader output/validation contract work for S5. |
| `codex/skills/ywc-brainstorm` | skill | A | 3.77 | S5 fixture gap closed | Fixture update raises mechanical S5 to 4; no follow-up is tracked for this cycle. |
| `codex/agents/*.toml` | agent | A | 3.92 or better | A8=3 evidence limitation across all 7 agents | Carried forward; behavioral evidence strategy exists, but no harness consumes fixtures yet. |

## Priority Backlog

1. [Medium] `codex/skills/ywc-plan`, `ywc-code-gen`, `ywc-finish-branch`, `ywc-refactor-clean`, `ywc-tdd-ritual` - tighten S7 Codex runtime wording.
   Evidence: fresh mechanical score reports S7=3 for each selected target.
   Owner: Codex skill authoring polish.
   Re-score target: S7 -> 4 where wording can be clarified without behavior changes.
2. [Medium] `codex/skills/ywc-finish-branch`, `ywc-agentic` - tighten the remaining S5 output/validation contract shape.
   Evidence: all five prioritized targets now have objective fixtures, but targeted scoring still reports S5=3 for these two skills.
   Owner: skill owners.
   Re-score target: S5 -> 4 when the remaining contract shape is explicit enough for deterministic validation.
3. [Medium] agent smoke harness - implement fixture execution for the bounded A8 strategy.
   Evidence: agent mechanical gates pass and the fixture strategy is documented, but A8 remains a judgment axis until smoke/eval artifacts execute successfully.
   Owner: Codex evaluator tooling.
   Re-score target: A8 -> 4 only after fixture files exist, the harness executes them, and passing evidence is cited.

## Decisions

- No evaluator scoring code or mechanical baseline was changed in this task.
- No scoreboard movement is claimed here; the scoreboard update belongs to the next task and must cite this report.
- No Codex skill, Codex agent, generated plugin, `.claude/**`, or `claude-code/**` files were edited by this report task.
- No Codex agent TOML was edited for A8; the current task only documents the read-only evidence strategy and defers harness implementation.
- Judgment-sensitive axes are carried forward explicitly to avoid presenting mechanical PASS as final quality.

## Next Cycle

- Recommended scope: finish sync and validation for this batch, then schedule a separate agent smoke harness if A8 should move to 4.
- Highest-priority item: complete evidence-backed S7/S5 improvements and keep A8 at 3 until executable agent fixture evidence exists.
- Mechanical baseline update needed: no.
