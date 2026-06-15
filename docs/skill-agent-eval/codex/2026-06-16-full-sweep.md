# Codex Skill/Agent Evaluation - 2026-06-16 - full sweep

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | full sweep (`--mode full --target all`) |
| Assets evaluated | 48 (41 skills, 7 agents) |
| Gate failures | 0 |
| Lowest carried-forward grade | A / 3.57 (`codex/skills/ywc-tech-research`) |

## Gate Summary

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Result: PASS. skill_count=41, agent_count=7, skill_gate_passed=true, agent_gate_failures=0.
scripts/validate.sh mirror gate: PASS, including Codex plugin package staleness check.
```

## Mechanical Scorecard

```text
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --format markdown
Result: PASS mechanically, partial only.
codex/skills: 41 items. codex/agents: 7 items.
All agents score 60.0/60.0 on mechanical axes.
All previous S5=2 targets now score S5=4.
Lowest skill mechanical score remains 51.25/57.0 on skills with S5=3 and S7=3.
```

Mechanical mode is partial. Judgment axes are carried forward from the 2026-06-13 full sweep for unchanged assets; this run's manual judgment focused on the newly changed low-S5 skills and the two new skills added since that sweep.

## Changed Scorecards

| Asset | Previous | Current | Weakest dimension | Evidence |
|---|---:|---:|---|---|
| `codex/skills/ywc-commit` | A / 3.64 | A / 3.90 | S7=3 | Standardized `## Output Format` and added an explicit status line while preserving the existing eval fixture. |
| `codex/skills/ywc-impl-review` | A / 3.74 | A / 4.00 | No mechanical score below 4 | Added a report validation contract plus an eval fixture for review/advisor budget behavior. |
| `codex/skills/ywc-parallel-executor` | A / 3.64 | A / 3.90 | S7=3 | Renamed completion-report/failure sections to satisfy output and validation contracts without increasing the 500-line body. |
| `codex/skills/ywc-receive-review` | A / 3.64 | A / 3.90 | S7=3 | Added machine-readable output shape and eval coverage for feedback handling. |
| `codex/skills/ywc-security-audit` | A / 3.74 | A / 4.00 | No mechanical score below 4 | Added validation requirements and eval coverage for OWASP evidence/advisor escalation. |
| `codex/skills/ywc-spec-validate` | A / 3.64 | A / 3.90 | No mechanical score below 4 | Added validation handoff checks and eval coverage for spec evidence and task-generator gating. |
| `codex/skills/ywc-tech-research` | B / 3.31 | A / 3.57 | Resolved S5=4 | Added validation requirements and eval coverage for source recency and inference labeling. |
| `codex/skills/ywc-docker-isolate` | new | A / 4.00 | No mechanical score below 4 | New skill is mechanically complete with scripts, output contract, validation, and linked references. |
| `codex/skills/ywc-spec-ready` | new | A / 3.87 | S5=3 | New loop-orchestration skill is structurally sound; next improvement is adding eval fixture coverage. |

## Priority Backlog

1. [Medium] S7=3 runtime-fit polish remains for skills that contain slash-invocation or workspace-path examples.
   Evidence: `score.py` reports S7=3 for `ywc-code-gen`, `ywc-commit`, `ywc-confidence-gate`, `ywc-finish-branch`, `ywc-handle-pr-reviews`, `ywc-merge-dependabot`, `ywc-onboard-repo`, `ywc-parallel-executor`, `ywc-plan`, `ywc-receive-review`, `ywc-refactor-clean`, and `ywc-tdd-ritual`.
   Owner: Codex skill authoring polish.
   Re-score target: S7 -> 4 where the examples can be rewritten without losing usability.
2. [Medium] S5=3 eval fixture gaps remain on otherwise healthy skills.
   Evidence: `ywc-agentic`, `ywc-brainstorm`, `ywc-debug-rootcause`, `ywc-e2e-test-strategy`, `ywc-finish-branch`, `ywc-spec-ready`, `ywc-task-generator`, `ywc-ubiquitous-language`, and `ywc-verify-done` still have S5=3.
   Owner: skill owners.
   Re-score target: S5 -> 4 via concrete eval fixtures or deterministic scripts.

## Decisions

- No evaluator scoring code or regression baseline was changed.
- `.codex-plugin/skills` was refreshed from `codex/skills` after source edits.
- The internal evaluator remained under `tools/codex-internal/skills/ywc-codex-toolkit-eval`; no evaluator files were copied into distributable Codex skills.

## Next Cycle

- Recommended scope: S7 runtime-fit wording cleanup and remaining S5=3 fixture coverage.
- Highest-priority item: decide whether slash-style invocation examples should be allowed by the mechanical runtime-fit scorer or rewritten in affected skills.
- Mechanical baseline update needed: no.
