---
name: ywc-codex-toolkit-eval
description: >-
  (ywc) Use when periodically evaluating or scoring the quality of existing
  Codex ywc-* skills or Codex custom agents in this toolkit, running the
  evaluate→improve cycle, or auditing the Codex skill/agent catalog for
  activation accuracy, structure compliance, packaging safety, and behavioral
  efficacy. Triggers: "codex skill 평가", "codex agent 평가", "codex toolkit
  평가해줘", "codex skill 점수 매겨줘", "평가 사이클", "evaluate codex skills",
  "score the codex agents", "codex skill quality eval", "Codex スキル評価",
  "Codex エージェント評価". Do not use for Claude Code skill/agent evaluation
  (use ywc-toolkit-eval in .claude/skills), for authoring or restructuring a
  skill (use ywc-skill-author), for reviewing application/product code (use
  ywc-impl-review), or for one-off structural lint that scripts/validate.sh
  already covers.
---

# ywc-codex-toolkit-eval

**Announce at start:** "I'm using the ywc-codex-toolkit-eval skill to score the Codex toolkit skills and agents and drive the evaluate→improve cycle."

Codex-internal graded quality-evaluation harness for this repository's `codex/skills/ywc-*` skills and `codex/agents/ywc-*.toml` custom agents. It is intentionally **not distributed**: keep it under `tools/codex-internal/skills/`, never under `codex/skills/` or `.codex-plugin/skills/`.

Where `ywc-skill-author` defines binary rules for *building* a skill, this skill produces a graded scorecard (0–5 per axis, weighted to 100), ranks the weakest Codex items, and keeps mechanical score history so regressions become visible across releases.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "scripts/validate.sh is green, so quality is fine" | `validate.sh` is a binary structure gate. It does not measure trigger precision, behavioral clarity, catalog overlap, or score trend. |
| "The Claude eval skill already exists, reuse that directly" | `.claude/skills/ywc-toolkit-eval` is for Claude Code conventions. Codex has different frontmatter, `agents/openai.yaml`, plugin packaging, and TOML agents. |
| "Internal tools can live under codex/skills if we remember not to publish them" | `codex/skills` is packaging source. Internal tools there will eventually leak into install or plugin sync. |
| "Mechanical score is enough for this cycle" | Mechanical axes are useful gates but do not prove activation or behavioral efficacy. Report mechanical-only results as partial. |
| "Score went down but the skill feels better now" | Fix the rubric or explain the regression. Silent manual overrides make the trend useless. |
| "Agents can be evaluated later" | Codex agents are called by skills; an unmeasured agent is an unmeasured edge in the same catalog graph. |

**Violating the letter of these rules is violating the spirit.** A quality cycle is only useful when it catches drift before users feel it.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--target` | `--target <root>` | `--target codex/skills` | Root to evaluate: `codex/skills`, `codex/agents`, or `all` (default). |
| `--mode` | `--mode <m>` | `--mode mechanical` | `mechanical` (script only), `judge` (model pass only), or `full` (both, default). |
| `--item` | `--item <name>` | `--item ywc-plan` | Score a single Codex skill or agent instead of the whole root. |
| `--ci` | flag | | Mechanical-only regression gate against `evals/history.mechanical.json`. |
| `--advisor-budget` | `--advisor-budget <n>` | `--advisor-budget 3` | Max high-reasoning judge escalations for ambiguous activation/boundary calls. Default 5. |

## Scoring Model

Each item is scored on six axes, each `0–5`, combined by fixed weights into a `/100` total. Skills and agents use different axis sets. Full banding is in references:

| Reference | Use |
|---|---|
| [references/skill-rubric.md](references/skill-rubric.md) | Codex skill axis definitions and 0–5 bands |
| [references/agent-rubric.md](references/agent-rubric.md) | Codex agent axis definitions and 0–5 bands |
| [references/trigger-eval-method.md](references/trigger-eval-method.md) | Activation/dispatch precision and recall method |
| [references/scorecard-format.md](references/scorecard-format.md) | Scorecard and history output schema |

Skill axes: S1 Activation accuracy (30), S2 Structure compliance (15), S3 Behavioral efficacy (20), S4 Token economy (10), S5 Consistency/integrity (15), S6 Catalog fit (10).

Agent axes: A1 Role-boundary clarity (20), A2 Dispatch accuracy (25), A3 Tool-grant minimality (15), A4 Output-contract compliance (15), A5 Model-tier appropriateness (15), A6 System-prompt quality (10).

## Workflow

### Step 1: Inventory Codex Targets

Resolve `--target` to `codex/skills`, `codex/agents`, or both for `all`. Do not include `.claude/skills`, `claude-code/skills`, or `claude-code/agents`; those belong to the Claude Code evaluation skill.

### Step 2: Mechanical Tier

Run the deterministic scorer:

```bash
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target <root> --format json
```

It emits mechanical axis scores plus raw signals such as body line count, missing locale README files, dangling references, description collision pairs, sandbox mode, and output-contract markers. Do not hand-compute these signals.

### Step 3: Judgment Tier

Skip when `--mode mechanical` or `--ci`. Otherwise run a bounded judge pass for judgment axes:

- **Activation judge (S1 / A2)** — use only `description` metadata and `evals/trigger-cases.json`; do not read `SKILL.md` bodies for activation.
- **Behavioral judge (S3)** — check whether following `SKILL.md` alone would produce the intended artifact.
- **Boundary / fit judge (S6 / A1)** — compare against nearest Codex siblings and flag overlap or gaps.
- **Prompt-quality judge (A6)** — score clarity, anti-rationalization coverage, and vague-language density in `developer_instructions`.

Each judgment score must include one line of justification and a file:line citation.

### Step 4: Aggregate

Combine mechanical and judgment scores per the weights. In mechanical-only mode, leave judgment axes as `·` and explicitly state that no final `/100` quality score was computed.

### Step 5: Backlog

Rank weakest items by total. Break ties by S1/A2, because a mis-firing skill or agent affects the whole catalog. Each backlog item must name the axis, evidence, and concrete fix.

### Step 6: Persist History

Append full-cycle trend data to `evals/history.json` when doing a full evaluation. In `--ci`, update `evals/history.mechanical.json` only after no mechanical regression is detected.

## Output Format

```text
# Codex Toolkit Scorecard — 2026-06-12

Mode: full

## codex/skills  (37 items, mean 84/100)

| Item | S1 | S2 | S3 | S4 | S5 | S6 | Total | Weakest |
|------|----|----|----|----|----|----|-------|---------|
| ywc-plan | 5 | 5 | 4 | 5 | 5 | 4 | 92 | S3 |

## Prioritized Backlog
1. ywc-example (64) — S1 Activation accuracy: description overlaps ywc-plan at codex/skills/ywc-example/SKILL.md:1.
   Fix: add a concrete `Do not use for...` anti-trigger pointing to the sibling owner.
```

## Validation

Before declaring an evaluation cycle complete, verify:

- [ ] Every Codex item in the resolved target list has one row.
- [ ] Mechanical-only mode is reported as partial, not final quality.
- [ ] Judgment-axis scores include file:line citations.
- [ ] Backlog entries name a concrete fix.
- [ ] `ywc-codex-toolkit-eval` does not appear under `codex/skills/` or `.codex-plugin/skills/`.
- [ ] `bash scripts/validate.sh` passes.

## Common Mistakes

- **Evaluating Claude Code artifacts with this skill** — use `.claude/skills/ywc-toolkit-eval` for Claude Code.
- **Letting internal skill files leak into packaging** — `codex/skills` and `.codex-plugin/skills` are distribution surfaces.
- **Treating collision count as activation accuracy** — collision count is a cap signal; precision/recall still need judge cases.
- **No prioritized backlog** — a scorecard without next actions is not a cycle.

## Integration

- **Upstream**: `ywc-skill-author` for structural rule interpretation.
- **Downstream**: use the prioritized backlog to make targeted Codex skill/agent edits, then re-run this skill.
- **Pairs with**: `scripts/validate.sh`, which enforces the internal-only packaging boundary and runs the mechanical regression gate.
