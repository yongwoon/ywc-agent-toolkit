---
name: ywc-codex-toolkit-eval
description: >-
  (ywc) Use when evaluating, scoring, auditing, or producing a prioritized
  improvement backlog for this repository's Codex ywc-* skills and Codex custom
  agents as a repeatable maintenance cycle.
  Triggers: "Codex skill 평가", "Codex agent 평가", "Codex 평가 기준",
  "codex toolkit 평가해줘", "skill/agent 개선 cycle", "evaluate Codex skills",
  "score Codex agents", "Codex skill maturity", "Codex scoreboard",
  "Codex スキル評価", "Codex エージェント評価". Do not use for Claude Code
  skill/agent evaluation (use .claude/skills/ywc-toolkit-eval), for authoring
  or directly editing a distributable ywc-* skill (use ywc-skill-author), for
  binary validation only (use scripts/validate.sh), or for application code
  review (use ywc-impl-review).
---

# ywc-codex-toolkit-eval

**Announce at start:** "I'm using the ywc-codex-toolkit-eval skill to evaluate this repository's Codex skills and agents."

This local Codex skill runs a Codex-only evaluate -> improve cycle over
`codex/skills/*` and `codex/agents/*.toml`. It must stay under
`.codex/skills/` and must not be copied into `codex/skills/` or
`.codex-plugin/skills/`.

## Boundary

| Included | Excluded |
|---|---|
| `codex/skills/*/SKILL.md` | `.claude/skills/*` |
| `codex/skills/*/agents/openai.yaml` | `claude-code/skills/*` |
| `codex/agents/*.toml` | `claude-code/agents/*` |
| Codex install flow, plugin packaging, and bundle docs | Application source code review |

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "scripts/validate.sh is green, so the Codex bundle is healthy" | Validation proves structure and packaging only. Trigger precision, workflow actionability, runtime fit, and behavioral evidence still need graded evaluation. |
| "The Claude evaluator already scores Codex paths, so keep using it" | Claude Code and Codex have different frontmatter schemas, agent formats, install paths, and runtime assumptions. Shared concepts are acceptable; shared target roots are not. |
| "Local evaluator skills can live under codex/skills if we remember not to publish them" | `codex/skills` and `.codex-plugin/skills` are distribution surfaces. Evaluators there will leak into installs or plugin packaging. |
| "Mechanical score is enough" | Mechanical axes are partial evidence. Judgment axes such as trigger precision, workflow actionability, scope discipline, mission boundaries, and behavioral evidence still decide the grade. |
| "No eval fixtures means no score" | Score from available evidence and mark uncertainty. Missing fixtures are themselves a quality signal. |
| "Fix every issue while evaluating" | Evaluation produces an evidence-ranked backlog. Implement fixes through `ywc-skill-author`, Codex agent authoring, or bundle docs work, then re-score. |
| "CI should rewrite history automatically" | CI compares against the reviewed baseline only. Baseline updates are explicit maintenance actions after reviewing the markdown scorecard. |

**Violating the letter of these rules is violating the spirit.** A quality cycle is useful only when it separates measurement, ownership, and repair.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--target` | `--target <root>` | `--target codex/skills` | Mechanical scorer target: `codex/skills`, `codex/agents`, or `all` (default). |
| `--item` | `--item <name>` | `--item ywc-plan` | Score one Codex skill or agent instead of the whole root. |
| `--mode` | `--mode <m>` | `--mode mechanical` | Skill-level evaluation mode: `mechanical`, `judge`, or `full`. Direct `score.py` runs support `mechanical` only; `judge` and `full` are skill-mediated workflows. |
| `--ci` | flag | `--ci` | Compare deterministic axes against `evals/history.mechanical.json` without rewriting it. |
| `--update-baseline` | flag | `--update-baseline` | Write the reviewed current mechanical baseline after checking the markdown output. |
| `--only` | `--only <scope>` | `--only agents` | Inventory gate scope: `skills`, `agents`, or all. |

## Argument Mapping

Map user arguments to concrete commands before running the workflow:

| User request | Inventory command | Mechanical command |
|---|---|---|
| `--target all` or no target | `inventory_gate.py --json` | `score.py --mode mechanical --target all --format markdown` |
| `--target codex/skills` | `inventory_gate.py --json --only skills` | `score.py --mode mechanical --target codex/skills --format markdown` |
| `--target codex/agents` | `inventory_gate.py --json --only agents` | `score.py --mode mechanical --target codex/agents --format markdown` |
| `--item <name>` | run the matching inventory scope for context | add `--item <name>` to `score.py` and score only that asset in the judgment pass |
| `--ci` | optional unless a full report is requested | `score.py --ci` |
| `--update-baseline` | optional unless reviewing current structure | `score.py --update-baseline` after reviewing markdown output |

Direct `score.py` runs support mechanical mode only. For `--mode judge` or
`--mode full`, use the mechanical output plus the rubric references to complete
the judgment pass.

## Scoring Model

Use three layers:

1. **Gate:** run `scripts/inventory_gate.py` to collect inventory and structural pass/fail evidence. Gate failures cap the affected asset at grade `C`.
2. **Mechanical:** run `scripts/score.py` for deterministic axes and baseline comparison. Judgment axes stay `·` and `final_total` remains unavailable.
3. **Judgment:** score the remaining axes with the rubric references.

Each dimension is scored `0-4`. Weighted composite maps to:
`A >= 3.5`, `B 2.5-3.49`, `C 1.5-2.49`, `D < 1.5`.

| Reference | Use |
|---|---|
| [references/skill-rubric.md](references/skill-rubric.md) | Codex skill dimensions S1-S8 |
| [references/agent-rubric.md](references/agent-rubric.md) | Codex TOML agent dimensions A1-A8 |
| [references/agent-behavioral-evidence.md](references/agent-behavioral-evidence.md) | Codex agent A8 smoke/eval evidence strategy |
| [references/scorecard-format.md](references/scorecard-format.md) | Report, backlog, and scoreboard format |
| [references/trigger-eval-method.md](references/trigger-eval-method.md) | Activation/dispatch precision and recall method |

Skill judgment axes: S1 trigger precision, S4 workflow actionability, and S8 scope discipline.
Agent judgment axes: A1 routing description, A3 mission and boundaries, and A8 behavioral evidence.

## Workflow

### Step 1: Inventory and Gate

Run from the repository root:

```bash
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
```

Use the JSON as evidence. Do not re-derive body line counts, missing README
locale files, missing `agents/openai.yaml`, or TOML key presence by memory.

### Step 2: Mechanical Score

Run the deterministic scorecard:

```bash
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --format markdown
```

For CI or pre-PR regression checks:

```bash
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

If the current mechanical scores are intentionally the new baseline:

```bash
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --update-baseline
```

Do not let CI rewrite `evals/history.mechanical.json`; CI compares only.

### Step 3: Scope the Evaluation

State one scope before scoring:

| Scope | Use when |
|---|---|
| Full sweep | Release readiness or periodic maintenance |
| Skills only | Skill triggering, body, README, metadata, or packaging changed |
| Agents only | TOML agent definitions or dispatch behavior changed |
| Targeted | A named subset needs focused review |

Default to targeted when the user names assets. Default to full sweep only when
the user asks for a general Codex quality evaluation.

### Step 4: Judgment Score

For every target asset:

1. Read the full asset body.
2. Read the matching rubric reference.
3. Assign every dimension a `0-4` score with one evidence note.
4. Apply any gate cap from the inventory payload.
5. Record uncertainty explicitly instead of inflating the score.

Use mechanical score output for deterministic axes. Do not manually override a
mechanical axis without fixing the scorer or naming the exception in Decisions.

### Step 5: Report and Backlog

Write Codex-only results under:

```text
docs/skill-agent-eval/codex/
```

Use [references/scorecard-format.md](references/scorecard-format.md) for the
report and scoreboard layout. Rank every dimension below `2` as backlog. Gate
failures outrank qualitative issues.

### Step 6: Route Fixes

| Finding type | Owner workflow |
|---|---|
| Codex skill structure or content | `ywc-skill-author` |
| Codex TOML agent definition | Codex custom-agent authoring conventions |
| Bundle install/docs/plugin drift | `codex/AGENTS.md`, bundle README set, and packaging scripts |
| Gate or scorer defect | This local skill's `scripts/` and rubric references |

After each improvement batch, rerun Step 1 and Step 2 for the affected scope.

## Output Format

```text
## Codex Skill/Agent Evaluation: <scope>

### Verdict
- Status: PASS | PASS_WITH_ACTIONS | REVIEW_REQUIRED | FAIL
- Assets evaluated: <n>
- Gate failures: <n>
- Lowest grade: <grade>

### Scorecards
| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|

### Priority Backlog
1. [Critical|High|Medium|Low] <asset> - <finding>
   Evidence: <path or gate field>
   Recommended owner: <workflow>

### Scoreboard Update
- Added: <n>
- Improved: <n>
- Regressed: <n>
- Next review scope: <scope>
```

## Validation

Before claiming the evaluation is complete, verify:

- [ ] `inventory_gate.py` was run for the stated scope.
- [ ] `score.py --mode mechanical --format markdown` was run for mechanical evidence unless skill-level `--mode judge` was explicit.
- [ ] Expected negative checks were run as assertion-shaped commands:
  - `! test -e codex/skills/ywc-codex-toolkit-eval`
  - `! test -e .codex-plugin/skills/ywc-codex-toolkit-eval`
  - `! rg 'tools/codex-internal/skills/ywc-codex-toolkit-[e]val' .codex/skills/ywc-codex-toolkit-eval scripts/validate.sh`
- [ ] Every scored skill used [references/skill-rubric.md](references/skill-rubric.md).
- [ ] Every scored agent used [references/agent-rubric.md](references/agent-rubric.md).
- [ ] Mechanical-only mode is reported as partial, not final quality.
- [ ] Report artifacts, if written, are under `docs/skill-agent-eval/codex/`.
- [ ] No Claude-only paths were scored as Codex assets.
- [ ] `ywc-codex-toolkit-eval` does not appear under `codex/skills/` or `.codex-plugin/skills/`.

## Common Mistakes

- **Evaluating Claude Code artifacts with this skill** — use `.claude/skills/ywc-toolkit-eval` for Claude Code.
- **Treating mechanical points as a final grade** — judgment axes must be scored before claiming a composite grade.
- **Letting local evaluator files leak into packaging** — keep the skill under `.codex/skills/`.
- **Skipping the backlog** — the prioritized fix list is the deliverable that makes the cycle actionable.

## Integration

- **Upstream**: `ywc-skill-author` for Codex skill rule interpretation.
- **Downstream**: use the prioritized backlog to make targeted Codex skill/agent edits, then re-run this skill.
- **Pairs with**: `scripts/validate.sh`, which enforces the local-only packaging boundary and runs the mechanical regression gate.
