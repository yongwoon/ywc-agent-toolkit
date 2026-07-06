# Codex Skill/Agent Evaluation - 2026-07-06 - full sweep mechanical

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | full sweep (`--target all`) |
| Assets evaluated | 49 (42 skills, 7 agents) |
| Gate failures | 0 |
| Lowest grade | n/a - mechanical partial only |

## Gate Summary

```text
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Exit code: 0.
Result: PASS.
skill_count=42, agent_count=7.
skills_missing_openai_yaml=[].
skills_incomplete_locale_readmes=[].
agent_gate_failures=0.
scripts/validate.sh: All checks passed.
mechanical regression gate: [ci] 49 items, no mechanical regression. PASS
```

Interpreter note: the default `python3` command resolved through pyenv 3.14.0 and completed, but was slow because `scripts/validate.sh` runs the full package validation suite. A separate `/Users/yongwoon.kim/.local/bin/python3.11 ... --skip-gate` run was used only to confirm agent TOML parsing without rerunning the structural validator.

## Mechanical Scorecard

```text
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --format markdown
Exit code: 0.
Result: PASS mechanically, partial only.
codex/skills: 42 items.
codex/agents: 7 items.
codex/agents: all 7 score 60.0/60.0 on mechanical axes.
codex/skills: 41 score 57.0/57.0 on mechanical axes.
codex/skills deterministic gap:
- ywc-setup: S5=0, 44.0/57.0, final=partial
```

Mechanical mode is partial. Skill judgment axes S1, S4, and S8, plus agent judgment axes A1, A3, and A8, remain `·`; no final quality composite is claimed in this report.

Additional deterministic checks:

| Command | Exit code | Result |
|---|---:|---|
| `! test -e codex/skills/ywc-codex-toolkit-eval` | 0 | Local evaluator absent from Codex skill distribution surface |
| `! test -e .codex-plugin/skills/ywc-codex-toolkit-eval` | 0 | Local evaluator absent from plugin skill distribution surface |
| `! rg 'tools/codex-internal/skills/ywc-codex-toolkit-[e]val' .codex/skills/ywc-codex-toolkit-eval scripts/validate.sh` | 0 | No stale internal evaluator path reference found |

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `codex/skills/*` except `ywc-setup` | skill | partial | n/a | judgment axes unscored | 41/42 skills scored 57.0/57.0 mechanically; S1/S4/S8 still require rubric judgment. |
| `codex/skills/ywc-setup` | skill | partial | n/a | S5 | Mechanical S5=0; inventory reports `has_evals=false`. |
| `codex/agents/*.toml` | agent | partial | n/a | judgment axes unscored | 7/7 agents scored 60.0/60.0 mechanically; A1/A3/A8 still require rubric judgment. |

## Priority Backlog

1. [Medium] `codex/skills/ywc-setup` - add or intentionally document eval fixture coverage so S5 no longer scores 0.
   Evidence: mechanical scorecard S5=0; inventory `has_evals=false`.
   Owner: `ywc-skill-author`
   Re-score target: S5 -> 4.
2. [Low] Full Codex bundle - run a judgment pass before claiming final grades.
   Evidence: mechanical output marks S1/S4/S8 and A1/A3/A8 as `·`; final column is `partial`.
   Owner: `ywc-codex-toolkit-eval`
   Re-score target: complete rubric-scored full report.

## Decisions

- No gate cap applied. The inventory gate reported no structural failure.
- No Claude Code paths were scored as Codex assets.
- `ywc-codex-toolkit-eval` remains local-only under `.codex/skills/`; it is absent from `codex/skills/` and `.codex-plugin/skills/`.
- `evals/history.mechanical.json` was not updated; this run compared against the baseline through `scripts/validate.sh`.
- The scoreboard was not updated because this report is mechanical-only and does not supersede the 2026-07-01 judged scoreboard.

## Scoreboard Update

- Added: 1 mechanical asset in scope (`codex/skills/ywc-setup`)
- Improved: 0 claimed from judgment
- Regressed: 0 mechanically against baseline
- Next review scope: targeted `ywc-setup` S5 remediation, then full judgment pass if release readiness requires final grades
