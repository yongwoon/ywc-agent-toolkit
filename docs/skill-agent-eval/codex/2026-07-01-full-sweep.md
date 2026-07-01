# Codex Skill/Agent Evaluation - 2026-07-01 - full sweep

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | full sweep (`--target all`) |
| Assets evaluated | 48 (41 skills, 7 agents) |
| Gate failures | 0 |
| Lowest grade | A |

## Gate Summary

```text
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
Exit code: 0.
Result: PASS.
skill_count=41, agent_count=7.
skills_missing_openai_yaml=[].
skills_incomplete_locale_readmes=[].
skills_without_evals=[].
agent_missing_required_keys=[].
```

## Mechanical Scorecard

```text
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --format markdown
Exit code: 0.
Result: PASS mechanically, partial only.
codex/skills: 41 items. codex/agents: 7 items.
codex/agents: all 7 score 60.0/60.0 on mechanical axes.
codex/skills deterministic gaps:
- S5=3: ywc-code-gen, ywc-task-generator, ywc-ubiquitous-language
- S7=3: ywc-commit, ywc-confidence-gate, ywc-handle-pr-reviews, ywc-merge-dependabot, ywc-onboard-repo, ywc-parallel-executor, ywc-receive-review
```

Mechanical mode is partial. Skill judgment axes S1, S4, and S8, plus agent judgment axes A1, A3, and A8, were filled in this report from the rubrics and asset bodies.

Additional deterministic checks:

| Command | Exit code | Result |
|---|---:|---|
| `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --ci` | 0 | `[ci] 48 items, no mechanical regression. PASS` |
| `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_score.py` | 0 | 18 tests passed |
| `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py --fixtures .codex/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json --outputs .codex/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output` | 0 | 13/13 agent smoke fixtures passed |
| `! test -e codex/skills/ywc-codex-toolkit-eval && ! test -e .codex-plugin/skills/ywc-codex-toolkit-eval && ! rg 'tools/codex-internal/skills/ywc-codex-toolkit-[e]val' .codex/skills/ywc-codex-toolkit-eval scripts/validate.sh` | 0 | Local evaluator did not leak into Codex distribution surfaces |

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `codex/skills/ywc-agentic` | skill | A | 3.92 | S8 | Broad orchestrator across plan/task/execute/evaluate; handoff boundaries remain clear but deserve watch. |
| `codex/skills/ywc-brainstorm` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-changelog-release-notes` | skill | A | 3.90 | S7 | Manual S7 exception: uses `AskUserQuestion` literal rather than Codex-native user-input wording. |
| `codex/skills/ywc-code-gen` | skill | A | 3.79 | S5, S8 | S5=3 mechanical gap; broad generation/orchestration surface needs tight executor handoff wording. |
| `codex/skills/ywc-commit` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap. |
| `codex/skills/ywc-confidence-gate` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap. |
| `codex/skills/ywc-create-pr` | skill | A | 3.82 | S7, S8 | Manual S7 exception for `AskUserQuestion`; broad commit/PR/CI/UL boundary is clear but large. |
| `codex/skills/ywc-debug-rootcause` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-design-renew` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-docker-isolate` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-e2e-test-strategy` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-finish-branch` | skill | A | 3.92 | S8 | Broad delivery workflow spanning merge, CI, PR, and cleanup; delegation boundaries are documented. |
| `codex/skills/ywc-gen-testcase` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-handle-pr-reviews` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap. |
| `codex/skills/ywc-impl-review` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-incident-postmortem` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-merge-dependabot` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap. |
| `codex/skills/ywc-onboard-repo` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap. |
| `codex/skills/ywc-parallel-executor` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap; body remains near the progressive-disclosure watch line. |
| `codex/skills/ywc-plan` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-product-review` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-project-docs` | skill | A | 3.92 | S8 | Broad project-documentation surface, but boundaries and explicit-request rule prevent overreach. |
| `codex/skills/ywc-project-scaffold` | skill | A | 3.90 | S7 | Manual S7 exception: examples use `/project-scaffold` and `/sc:implement` slash commands. |
| `codex/skills/ywc-receive-review` | skill | A | 3.90 | S7 | Mechanical S7=3 Codex runtime-fit gap. |
| `codex/skills/ywc-refactor-clean` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-release-pr-list` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-review-learnings` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-security-audit` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-sequential-executor` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4; body remains near the progressive-disclosure watch line. |
| `codex/skills/ywc-skill-author` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-spec-ready` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-spec-validate` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-spec-writer` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-task-generator` | skill | A | 3.87 | S5 | Mechanical S5=3 output/verification-contract gap. |
| `codex/skills/ywc-tdd-ritual` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-team-assemble` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-tech-research` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-ubiquitous-language` | skill | A | 3.69 | S5, S7, S8 | S5=3 mechanical gap; manual S7 exception because completion prompt only targets `CLAUDE.md`; adjacent ownership with project-docs remains clear but close. |
| `codex/skills/ywc-ui-ux-review` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/skills/ywc-verify-done` | skill | A | 3.90 | S7 | Manual S7 exception: refers to `run_in_background: true` as a tool field. |
| `codex/skills/ywc-worktrees` | skill | A | 4.00 | none | Gate clean; mechanical axes 4; judgment axes 4. |
| `codex/agents/ywc-architect.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |
| `codex/agents/ywc-go-reviewer.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |
| `codex/agents/ywc-performance-engineer.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |
| `codex/agents/ywc-python-reviewer.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |
| `codex/agents/ywc-root-cause-analyst.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |
| `codex/agents/ywc-security-engineer.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |
| `codex/agents/ywc-typescript-reviewer.toml` | agent | A | 4.00 | none | Routing/mission boundaries precise; A8 backed by passing smoke fixtures. |

## Priority Backlog

1. [Medium] `codex/skills/ywc-ubiquitous-language` - tighten Codex runtime and output contract.
   Evidence: S5=3 mechanical; manual S7 exception at `CLAUDE.md Integration Prompt`; S8=3 adjacent docs ownership.
   Owner: `ywc-skill-author`
   Re-score target: S5/S7/S8 -> 4.
2. [Medium] `codex/skills/ywc-code-gen` - close the remaining output-contract gap and document orchestration boundaries more tightly.
   Evidence: S5=3 mechanical; S8=3 judgment.
   Owner: `ywc-skill-author`
   Re-score target: S5/S8 -> 4.
3. [Medium] `codex/skills/ywc-create-pr` - replace `AskUserQuestion` wording and keep PR/commit/CI/UL ownership boundaries explicit.
   Evidence: manual S7 exception; S8=3 judgment.
   Owner: `ywc-skill-author`
   Re-score target: S7/S8 -> 4.
4. [Low] Mechanical S7 group - resolve deterministic Codex runtime-fit gaps.
   Evidence: S7=3 on `ywc-commit`, `ywc-confidence-gate`, `ywc-handle-pr-reviews`, `ywc-merge-dependabot`, `ywc-onboard-repo`, `ywc-parallel-executor`, and `ywc-receive-review`.
   Owner: `ywc-skill-author`
   Re-score target: S7 -> 4.
5. [Low] Manual S7 exception group - remove Codex-unfriendly runtime wording not caught by the scorer.
   Evidence: `AskUserQuestion` in `ywc-changelog-release-notes`; slash-command examples in `ywc-project-scaffold`; `run_in_background: true` in `ywc-verify-done`.
   Owner: `ywc-skill-author`
   Re-score target: S7 -> 4, and consider extending the scorer patterns.
6. [Low] Broad orchestrator group - preserve boundaries while raising S8.
   Evidence: S8=3 on `ywc-agentic`, `ywc-finish-branch`, and `ywc-project-docs`.
   Owner: `ywc-skill-author`
   Re-score target: S8 -> 4.
7. [Low] Body-size watch list - monitor progressive-disclosure drift near the 500-line threshold.
   Evidence: inventory `body_lines`: `ywc-gen-testcase` 489, `ywc-parallel-executor` 503, `ywc-sequential-executor` 504, `ywc-task-generator` 454; mechanical S3 remains passing.
   Owner: `ywc-skill-author`
   Re-score target: no immediate score movement; extract only if S3 drops or editing cost rises.

## Decisions

- No gate cap applied. The inventory gate reported no structural failure.
- No Claude Code paths were scored as Codex assets.
- `ywc-codex-toolkit-eval` remains local-only under `.codex/skills/`; it is absent from `codex/skills/` and `.codex-plugin/skills/`.
- Mechanical axes were not silently overridden. Manual S7 exceptions are named for issues the current deterministic regex misses: `AskUserQuestion`, non-ywc slash-command examples, `run_in_background: true`, and Claude-only context-injection wording.
- Agent A8 stays 4 because the local smoke harness passed 13/13 fixtures with captured outputs.
- `evals/history.mechanical.json` was not updated; this run compared against the baseline only.

## Scoreboard Update

- Added: 0
- Improved: 26
- Regressed: 1 (`ywc-ubiquitous-language`, due to newly named S7/S8 qualitative exceptions)
- Next review scope: targeted S5/S7/S8 remediation for the backlog above
