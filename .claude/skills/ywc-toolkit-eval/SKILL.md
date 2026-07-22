---
name: ywc-toolkit-eval
version: 1.0.0
description: >-
  (ywc) Use when periodically evaluating or scoring the quality of existing ywc-* skills or agents in this toolkit, running the evaluate→improve cycle, or auditing the skill/agent catalog for activation accuracy, structure compliance, and behavioral efficacy. Triggers: "skill 평가", "agent 평가", "toolkit 평가해줘", "skill 점수 매겨줘", "평가 사이클", "evaluate skills", "score the agents", "skill quality eval", "스킬 평가", "에이전트 평가", "スキル評価", "エージェント評価", "evaluation cycle", "toolkit 품질 점검". Do not use for authoring or restructuring a skill (use ywc-skill-author), for reviewing application/product code (use ywc-impl-review), for spec quality review (use ywc-spec-validate), or for one-off structural lint that scripts/validate.sh already covers.
category: meta
phase: quality
requires: []
advisor_budget: 5
---

# ywc-toolkit-eval

**Announce at start:** "I'm using the ywc-toolkit-eval skill to score the toolkit's skills and agents and drive the evaluate→improve cycle."

Graded quality-evaluation harness for the toolkit's own Claude Code `ywc-*` skills and custom agents. Where `ywc-skill-author` defines the **binary compliance rules** for *building* a skill, this skill produces a **graded scorecard** (0–5 per axis, weighted to 100) for *existing* Claude Code skills and agents, ranks the weakest items, and persists score history so quality trends are visible release over release. Input: a target root (`claude-code/skills`, `claude-code/agents`, or both). Output: `evals/scorecard.md` (per-item axis scores + prioritized backlog) and an appended `evals/history.json` row. Codex skill/agent evaluation is owned by `.codex/skills/ywc-codex-toolkit-eval`.

> **Internal-only skill (locale-exempt):** `ywc-toolkit-eval` lives under `.claude/skills/` as a toolkit-maintenance tool and is **not** distributed under `claude-code/skills/`. It is therefore exempt from the en/ja/ko README locale-set requirement that `scripts/validate.sh` enforces on distributed skills.

The harness is **two-tier** by design, because not every quality axis can be measured deterministically:

| Tier | How | Axes | CI |
|---|---|---|---|
| Mechanical | `scripts/score.py` (deterministic, no model) | Structure compliance, token economy, integrity, tool-grant minimality, output-contract presence, description-collision heuristic | Regression-blocking |
| Judgment | Agent judge pass (Workflow / Task subagents) | Activation precision/recall, behavioral efficacy, role-boundary clarity, dispatch accuracy, prompt quality | On-demand, non-blocking |

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Mechanical score is green, the skill is good" | Mechanical axes are ~40% of the weight. A skill can pass every structural check and still never activate (S1) or fail its own workflow (S3). Never report a total from the mechanical tier alone. |
| "This skill scored 5/5 last quarter, skip re-eval" | Sibling skills change descriptions; a collision can appear without this skill changing one line. Activation accuracy is a property of the whole catalog, not one file. Always re-score against the current siblings. |
| "The judge agreed with my guess, so it's right" | A single judge over a single phrasing is one data point. Activation precision needs the full positive/negative/collision case set, not one confirming example. |
| "Score went down but the skill is actually better now" | If the rubric disagrees with reality, fix the rubric in the same PR and say so — do not silently override the number. An unexplained manual score is indistinguishable from gaming. |
| "I'll evaluate skills now, agents later" | Agents are dispatched BY skills. An unscored agent is an unmeasured edge of the same graph. Score both roots in one cycle or the catalog-fit axis (S6/A1) is blind. |
| "Backlog is obvious, skip the prioritized list" | Without the ranked backlog the cycle has no next action and degrades into a one-off audit. The ranked list IS the deliverable that makes it a cycle. |
| "Low score on a rarely-used skill, ignore it" | A rarely-used skill with an over-broad description steals activations from its siblings every turn (Tier-1 cost is paid every conversation). Low usage ≠ low blast radius. |

**Violating the letter of these rules is violating the spirit.** A scorecard that flatters the toolkit is worse than no scorecard — it certifies decay as health.

## Arguments

Two distinct surfaces: the deterministic `score.py` flags, and the skill/orchestrator-level arguments this skill interprets but **never** passes to the script.

**`score.py` flags** (consumed by `scripts/score.py`):

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--target` | `--target <root>` | `--target claude-code/skills` | Root to evaluate: `claude-code/skills`, `claude-code/agents`, or `all` (default). |
| `--item` | `--item <name>` | `--item ywc-commit` | Score a single skill/agent instead of the whole root. Rejected when combined with `--ci`. |
| `--format` | `--format <fmt>` | `--format markdown` | Output format: `json` (default) or `markdown`. |
| `--ci` | flag | | Mechanical-only; compares against the committed `evals/history.mechanical.json` baseline and exits non-zero on any per-axis mechanical regression. Used by the CI gate. |

**Skill / orchestrator arguments** (interpreted by this skill; not `score.py` flags):

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--mode` | `--mode <m>` | `--mode mechanical` | `mechanical` (script only), `judge` (model pass only), or `full` (both, default). |
| `--advisor-budget` | `--advisor-budget <n>` | `--advisor-budget 3` | Max Opus judge escalations for genuinely ambiguous activation/boundary calls. Default 5. |

## Scoring Model

Each item is scored on six axes, each `0–5`, combined by fixed weights into a `/100` total. Skills and agents use **different** axis sets (an agent has no README locale set; a skill has no tool-grant). The full 0–5 banding per axis lives in the references — do not inline the rubric tables (they are >30-line static content, Tier 3 per `ywc-skill-author` A14).

**Skill axes** — see [references/skill-rubric.md](references/skill-rubric.md) for the 0–5 banding:

| Axis | Weight | Tier |
|---|---|---|
| S1 Activation accuracy (trigger precision/recall + collision) | 30 | collision = mechanical, precision/recall = judgment |
| S2 Structure compliance (10-rule mechanical subset of ywc-skill-author A1–A14; A5/A10/A12/A13 out of mechanical scope) | 15 | mechanical |
| S3 Behavioral efficacy (does following SKILL.md produce the right outcome) | 20 | judgment |
| S4 Token economy (Tier-1 leanness, ≤500 body, Tier-3 extraction) | 10 | mechanical |
| S5 Consistency & integrity (locale set, pointer resolution, dangling refs) | 15 | mechanical |
| S6 Catalog fit (redundancy / gap vs siblings) | 10 | judgment |

**Agent axes** — see [references/agent-rubric.md](references/agent-rubric.md) for the 0–5 banding:

| Axis | Weight | Tier |
|---|---|---|
| A1 Role-boundary clarity (crisp, non-overlapping scope) | 20 | judgment |
| A2 Dispatch accuracy (orchestrator picks it at the right time) | 25 | collision = mechanical, rest = judgment |
| A3 Tool-grant minimality (least privilege) | 15 | mechanical |
| A4 Output-contract compliance (Status/Next-action shape) | 15 | mechanical |
| A5 Model-tier appropriateness (Opus/Sonnet/Haiku fit) | 15 | mechanical heuristic + judgment |
| A6 System-prompt quality (clarity, anti-rationalization, no vague language) | 10 | judgment |

The activation methodology (how positive/negative/collision cases yield precision and recall) is in [references/trigger-eval-method.md](references/trigger-eval-method.md). The exact scorecard layout and `history.json` schema are in [references/scorecard-format.md](references/scorecard-format.md).

## Workflow

### Step 1: Inventory Targets

Resolve `--target` to a concrete item list. For `all`, score `claude-code/skills` and `claude-code/agents` only. Do not score `codex/skills` or `codex/agents`; use `.codex/skills/ywc-codex-toolkit-eval` for Codex evaluation. Read `evals/history.json` (if present) to obtain the previous scores for regression comparison.

### Step 2: Mechanical Tier — `scripts/score.py`

Run the deterministic scorer:

```bash
python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target <root> --format json
```

It walks each item, parses frontmatter and body, and emits per-axis mechanical sub-scores plus the raw signals (body line count, locale-set completeness, dangling-reference list, sibling description n-gram overlap pairs, agent tool list, contract-marker presence, trigger-case coverage, `prose_lint`).

`prose_lint` reports no-op exhortations ("write clean code") and non-directive phrasing ("X is recommended" where the body should command). It is **warning-only: it never gates an axis or the CI baseline** — treat its hits as backlog candidates, not deductions. Lines carrying a concrete anchor and lines that quote guidance (tables, block quotes, fenced code) are excluded by design, so a low hit count means the bodies are clean rather than that the check is off. Do not hand-compute these — read them from the script output. Stop and fix the script if a signal is obviously wrong rather than overriding it in prose.

### Step 3: Judgment Tier — Agent Judge Pass

Skip this step when `--mode mechanical` or `--ci`. Otherwise spawn parallel judge subagents (Task tool, `model: sonnet`; escalate only genuinely ambiguous calls to `model: opus` within `--advisor-budget`). One judge per item per judgment axis:

- **Activation judge (S1 / A2)** — given the item's `description` and the case set in `evals/trigger-cases.json`, predict activation for each positive / negative / collision prompt; compute precision & recall. A collision case that the item wins when a sibling should own it is a false positive. **Read the mechanical `signals.coverage.sufficient` first: when it is `false` (the item is below the ≥3-positive / ≥2-collision floor), return S1/A2 as `"unmeasured"` with a one-line reason instead of a fabricated precision/recall — never carry forward a prior run's score.** An unmeasured item enters the prioritized backlog regardless of its total, because its heaviest axis is unmeasurable until the fixture is backfilled.
  - **Run the activation judge 3 times** on the same input and take the majority verdict. The judge is an LLM and a single pass is one data point; without an isolated execution harness, repetition is the only available defense against nondeterminism. If the three runs disagree, do **not** average them — record "descriptions genuinely ambiguous" and treat the spread itself as the S1 signal (see [references/trigger-eval-method.md](references/trigger-eval-method.md) Determinism Note).
- **Behavioral judge (S3)** — **prefer measurement over reading.** When the item has fixtures under `evals/fixtures/`, do not judge: run `scripts/runner.py` over them and take S3 from the observed reliability (`passes / trials` at 6 trials), recording `s3_source: "runner"`. **Band 4 is unreachable at 6 trials** — 5/6 lands in band 3 and 6/6 in band 5 — so a measured 4 is never a valid result (see [references/skill-rubric.md](references/skill-rubric.md) S3). When the item has **no** fixture, fall back to reading the body — if an agent followed only this body on the canonical scenario, would the output satisfy the stated purpose? — score the gap citing the under-specified step, tag it `(read-only)`, and record `s3_source: "read-only"`. A read 4 and a measured 4 are different claims; never merge them. If a fixture exists but every trial errored, S3 is `"unmeasured"`, not `0`. **Runner results never enter `axes.S3`** — they reach the scorecard and backlog only, so `--ci` stays deterministic.
- **Boundary / fit judge (S6 / A1)** — compare the item's responsibility against its nearest siblings; flag overlap (two skills that would both fire) or gap (a real need no skill owns).
- **Prompt-quality judge (A6)** — score persona clarity, anti-rationalization coverage, and vague-language density in the agent body.

Each judge returns a 0–5 score **with a one-line justification and a file:line citation**. A score without a citation is rejected — re-run that judge.

### Step 4: Aggregate the Scorecard

Combine mechanical and judgment sub-scores per the weights above into a `/100` total per item. Write `evals/scorecard.md` using the layout in [references/scorecard-format.md](references/scorecard-format.md): one row per item, per-axis scores, total, and the weakest-axis tag.

Do **not** hand-compute the totals or the run statistics. `score.py` owns those rules: `item_total(axes, weights)` returns `None` when any axis is unmeasured, and `build_history_row(scored, weights)` produces the `history.json` entry with `items.<name>: null` for unmeasured items, `unmeasured[]`, `measured`, `s3_source`, and a `mean_total` / `below_threshold` computed over measured items only. Deriving these in prose is how the two documents drift apart.

### Step 5: Prioritized Improvement Backlog

Rank items ascending by total. Break ties by the activation axis (S1 / A2) — a skill that mis-fires hurts the whole catalog, so it outranks an internally-weak but correctly-scoped one. Emit the top N as a numbered backlog, each line naming the item, its weakest axis, the file:line evidence, and the concrete fix. The fix for a structural axis points at `ywc-skill-author`; the fix for an activation axis names the specific trigger/anti-trigger edit.

### Step 6: Persist History

Append one row to `evals/history.json`: timestamp, per-item totals, and catalog-level aggregates (mean total, count below threshold). This is what turns a one-off audit into a trend. Never overwrite prior rows.

## Output Format

```text
# Toolkit Scorecard — 2026-06-12   (illustrative example — numbers are not current)

## claude-code/skills  (38 items, mean 82/100)

| Item | S1 | S2 | S3 | S4 | S5 | S6 | Total | Weakest |
|------|----|----|----|----|----|----|-------|---------|
| ywc-commit          | 5 | 5 | 4 | 5 | 5 | 4 | 94 | S3 |
| ywc-tech-research   | 3 | 4 | 3 | 3 | 4 | 2 | 64 | S6 |
| ywc-sample-nofx     | 5 | 5 | ? | 5 | 5 | 4 | —  | S3 |
| ywc-sample-mech     | 5 | 5 | · | 5 | 5 | · | —  | —  |

Notation: `?` = cannot be measured (no fixture — backfill it) · `·` = not measured
this run (judgment tier skipped — re-run `--mode full`) · `—` = no total, because
an axis is `?` or `·`. `?` and `·` are never merged: one is coverage debt, the
other is just a cheaper run mode. An item with a missing axis has at most 80
weight available, so any `/100` it reported would understate itself — it records
`items.<name>: null` and is excluded from `mean_total`, but still enters the
backlog. Full legend: [references/scorecard-format.md](references/scorecard-format.md).

## Prioritized Backlog
1. ywc-tech-research (64) — S6 catalog fit: description overlaps ywc-product-review
   on "compare options"; SKILL.md:1. Fix: add "Do not use for product/business
   comparison (use ywc-product-review)" anti-trigger.
2. ywc-sample-nofx (—) — S3 unmeasurable: no fixture under evals/fixtures/.
   Fix: add one happy_path and one negative case, then re-run.
```

## Validation

Before declaring an evaluation cycle complete, verify:

- [ ] Every item in the resolved target list has a row (no silent skips) — count rows == count items.
- [ ] No total is derived from the mechanical tier alone unless `--mode mechanical` was explicit.
- [ ] Every judgment-axis score carries a file:line citation.
- [ ] The prioritized backlog has at least one concrete, actionable fix per listed item.
- [ ] `evals/history.json` gained exactly one new row; no prior row was mutated.
- [ ] Any item whose mechanical `signals.coverage.sufficient` is `false` has its S1 (skill) or A2 (agent) recorded as **"unmeasured"** — not a number, and not a value carried forward from a prior run. Every unmeasured item appears in the prioritized backlog regardless of its total.
- [ ] The activation judge ran **3 times** per item and the reported score is the majority verdict; a three-way disagreement was recorded as "descriptions genuinely ambiguous" rather than averaged.
- [ ] In `--ci` mode, exit code reflects regression (non-zero if any per-axis mechanical score dropped vs the committed `history.mechanical.json` baseline).

## Common Mistakes

- **Reporting mechanical-only totals as the final score** — the script is ~40% of the weight. Always note when the judgment tier was skipped, and never present the partial total as the item's quality.
- **Scoring a skill in isolation** — S1/S6 are relative to siblings. Re-derive collisions against the *current* catalog every run; a description that was unique last quarter may collide today.
- **Letting the rubric and reality drift silently** — if a high-quality item scores low, the rubric is wrong; fix the rubric (in references) and record it, do not patch the number by hand.
- **Treating the scorecard as the deliverable** — the *prioritized backlog* is the deliverable. A scorecard with no ranked next action is a dashboard nobody acts on.

## Integration

- **Upstream**: `ywc-skill-author` — its A1–A14 rules ARE the S2 sub-rubric; this skill scores compliance, it does not redefine the rules. Reference by name; never duplicate the rule text.
- **Downstream**: feed the prioritized backlog back into `ywc-skill-author` (for structural/authoring fixes) or a normal edit pass (for description/trigger fixes), then re-run this skill to confirm the score moved.
- **Pairs with**: `scripts/validate.sh` (binary structural gate — this skill is the graded layer on top) and `ywc-impl-review` (which reviews *application* code; this skill reviews the *toolkit's own* skills/agents).
