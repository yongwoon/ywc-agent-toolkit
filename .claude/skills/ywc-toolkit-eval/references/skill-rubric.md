# Skill Rubric — 0–5 Banding per Axis

Each axis is scored `0` (absent/broken) to `5` (exemplary). The weighted sum (weights below) normalizes to `/100`. "Mechanical" rows are produced by `scripts/score.py`; "judgment" rows by the agent judge pass.

| Axis | Weight | Tier |
|---|---|---|
| S1 Activation accuracy | 30 | mixed |
| S2 Structure compliance | 15 | mechanical |
| S3 Behavioral efficacy | 20 | judgment |
| S4 Token economy | 10 | mechanical |
| S5 Consistency & integrity | 15 | mechanical |
| S6 Catalog fit | 10 | judgment |

Total weight = 100. Item total = Σ(axis_score / 5 × weight).

## S1 — Activation Accuracy (weight 30)

The single highest-leverage axis. A skill that does not fire is worthless; one that over-fires pollutes every sibling. Combines a mechanical collision signal with a judged precision/recall over `evals/trigger-cases.json` (see `trigger-eval-method.md`).

| Score | Band |
|---|---|
| 5 | Recall ≥ 0.95 on positive cases AND precision ≥ 0.95 (≤1 false-positive on negative/collision cases). Description has explicit `Do not use for...` pointing at the real sibling for every near-collision. |
| 4 | Recall ≥ 0.90 and precision ≥ 0.90. Minor anti-trigger gap on one sibling. |
| 3 | Recall ≥ 0.80 or precision ≥ 0.80 (one weak). One unresolved collision pair (two skills plausibly fire on the same prompt). |
| 2 | Recall or precision in 0.60–0.80. Anti-triggers missing or generic. |
| 1 | < 0.60 on either. Description summarizes the workflow instead of stating triggers (Tier-1 anti-pattern). |
| 0 | No multilingual triggers, or description is a workflow summary with no trigger phrases at all. |

Mechanical sub-signal (caps S1 at 3 until fixed): if `score.py` reports an n-gram overlap pair with a sibling above the collision threshold AND neither description names the other in a `Do not use for...` clause, S1 cannot exceed 3 regardless of the judged precision.

## S2 — Structure Compliance (weight 15)

Mechanical. Scores the **10-rule mechanical structural subset** of `ywc-skill-author`'s A1–A14 — the rules `scripts/score.py` can verify deterministically. Score = round(satisfied / 10 × 5). This is deliberately **not** full A1–A14 coverage: A5 (model-tier — agents only), A10, A12, and A13 are out of mechanical scope (judgment-tier or exempt-by-design) and are excluded from the denominator. The 10 checked rules:

| Signal | Rule |
|---|---|
| `name:` present and `ywc-` prefixed, matches dir | A1 |
| description starts `(ywc) Use when` | A2 |
| description contains `Do not use for` | A3 |
| description has Korean + Japanese chars (multilingual) | A4 |
| first body line is `**Announce at start:**` | A6 |
| `## Rationalization Defense` with ≥5 data rows (excluding the header and separator rows) | A7 |
| body ≤ 500 lines | A8 |
| no `@`-prefixed skill cross-reference | A9 |
| required README locale set (md/en/ja/ko) present; es/zh optional, not scored | A11 |
| every `references/*.md` has ≥1 inbound pointer | A14 |

## S3 — Behavioral Efficacy (weight 20)

Judgment. "If an agent followed ONLY this SKILL.md body on the skill's canonical scenario, would the output satisfy the stated purpose?"

| Score | Band |
|---|---|
| 5 | Every workflow step is executable without inference; stop-conditions explicit; Rationalization Defense closes the real loopholes an agent would try. |
| 4 | Executable, but one step relies on unstated context the agent must guess. |
| 3 | Workflow is correct in outline but ≥2 steps use vague language ("appropriately", "as needed") with no threshold. |
| 2 | A step contradicts another, or the happy path is covered but the documented failure mode is not handled. |
| 1 | Workflow is aspirational prose, not executable steps. |
| 0 | Following the body would produce the wrong artifact. |

## S4 — Token Economy (weight 10)

Mechanical. Progressive-disclosure discipline.

| Score | Band |
|---|---|
| 5 | Description (Tier 1) is trigger-only; body ≤ 500; every static section >30 lines is extracted to `references/`; no `references/*.md` < 30 lines (no over-extraction). |
| 4 | One of: body 450–500, or one borderline section left inline. |
| 3 | Body 500–550 (slightly over), or one >30-line static table left inline. |
| 2 | Body 550–700, or description carries a workflow-summary sentence (Tier-1 bloat). |
| 1 | Body > 700, or multiple un-extracted large static blocks. |
| 0 | Body > 1000, or Tier-3 content (templates/tables) inlined wholesale. |

## S5 — Consistency & Integrity (weight 15)

Mechanical. Cross-file coherence.

Only the required locale set (`md`/`en`/`ja`/`ko`) is scored. `es`/`zh` are officially optional — they match neither `validate.sh` nor the project locale policy — so their absence does not deduct (an informational `missing_optional_locales` signal is still emitted).

| Score | Band |
|---|---|
| 5 | All required locales (md/en/ja/ko) present and non-empty; every `Do not use for (use ywc-X)` pointer resolves to a real sibling; every `references/` pointer resolves; no dangling file links. |
| 4 | All resolve, but one required locale README is materially shorter than the others (likely stale). |
| 3 | One stale/short required locale, or a single minor pointer inconsistency. |
| 2 | A `Do not use for` pointer names a non-existent skill, or one `references/` link is dangling. |
| 1 | Multiple dangling pointers/links. |
| 0 | Required locale (md/en/ja/ko) missing — would fail validate.sh CI. |

## S6 — Catalog Fit (weight 10)

Judgment. Position in the skill graph.

| Score | Band |
|---|---|
| 5 | One skill = one responsibility; no sibling overlaps its trigger surface; fills a real need. |
| 4 | Slight conceptual overlap with one sibling, but anti-triggers cleanly separate them. |
| 3 | Overlaps one sibling's surface; a user request could reasonably route to either. |
| 2 | Substantially duplicates a sibling — merge candidate. |
| 1 | Duplicates a sibling AND lacks anti-triggers to disambiguate. |
| 0 | Redundant (another skill fully subsumes it) or orphaned (documents a workflow nothing routes to). |
