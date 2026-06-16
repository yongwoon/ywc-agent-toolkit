# Spec — ywc-toolkit-eval Quality Improvements

**Scale:** Medium (≈13 tasks; multi-file, multi-concern; no DB migration, no new library)
**Target skill:** `.claude/skills/ywc-toolkit-eval/` (internal-only meta skill; NOT distributed under `claude-code/skills/`)
**Author route:** ywc-plan (Medium path) → ywc-spec-validate → ywc-task-generator
**Sibling spec (different target, do not conflate):** `docs/ywc-plans/codex-toolkit-eval-improvements.md` covers the Codex eval skill `ywc-codex-toolkit-eval`; this spec covers the Claude Code `ywc-toolkit-eval`.
**Architectural Advisor Gate (Step 3.5):** Skipped — all design forks (A5 heuristic shape, coverage-gate vs full authoring, locale exemption) were resolved by explicit user decision; no unresolved module-boundary / sync-async / abstraction trade-off remains.

---

## Purpose

`ywc-toolkit-eval` is the graded quality harness for the toolkit's own `ywc-*` skills and agents. A prior review found an 11-item gap between **what the harness documents it measures** and **what its implementation + data actually measure**. Because the skill's own value proposition is "certify health, never flatter," these gaps are self-undermining: the highest-weighted axes (S1 30%, A2 25%) are effectively blind on ~80% of the catalog, two mechanical axes disagree with their own rubric, and one mechanical axis emits a constant. This spec closes all 11 findings so the scorecard's reported precision matches its real precision.

## Why

- **Credibility:** The skill explicitly warns against "rubric and reality drifting silently" (`SKILL.md:151`). Items 4/5/6 ARE that drift, inside the tool that polices it.
- **Coverage:** Activation accuracy (55% of combined weight across S1+A2) depends on `evals/trigger-cases.json`, which holds 14 cases covering 9 of 50 items. The two highest-leverage axes are unmeasured for most of the catalog.
- **Correctness:** `--ci --item` can silently corrupt the committed regression baseline; A5 is a no-op constant. Both produce false confidence — the worst failure mode for an evaluation tool.

## Scope

In scope — all 11 reviewed findings:

| # | Severity | Finding | Primary surface |
|---|---|---|---|
| 1 | High | Trigger-case coverage 14/9 vs 50 items; method requires ≥3 pos + ≥2 collision per item | `evals/trigger-cases.json`, `scripts/score.py` |
| 2 | High | `--ci --item` clobbers `history.mechanical.json` baseline to a single item | `scripts/score.py` |
| 3 | High | A5 mechanical sub-score is constant 4 (all agents declare `model:`) | `scripts/score.py`, `references/agent-rubric.md` |
| 4 | Medium | A7 row threshold: rubric "≥5 rows" vs script `>=6` pipe-lines | `scripts/score.py`, `references/skill-rubric.md` |
| 5 | Medium | S2 claims "A1–A14 compliance" but scores a fixed 10-check subset with no exemption logic | `scripts/score.py`, `SKILL.md`, `references/skill-rubric.md` |
| 6 | Medium | Collision exclusion is substring-anywhere, not "Do not use for" clause-aware | `scripts/score.py` |
| 7 | Low | Catalog counts stale (docs say 36 skills / 12 agents; actual 38 / 12) | `SKILL.md`, `README.md` |
| 8 | Low | `--mode` / `--advisor-budget` documented as args but are orchestrator-level, not script flags | `SKILL.md`, `README.md` |
| 9 | Low | `Math.random()`-style wording is a JS idiom in a Python/agent harness | `references/trigger-eval-method.md` |
| 10 | Low | `_unresolved_sibling_pointers` resolves only against skill roots; future `use ywc-<agent>` pointer would false-flag | `scripts/score.py` |
| 11 | Low | This skill lacks the en/ja/ko README locale set | `SKILL.md` (exemption note) |

## Out of Scope

- The two-tier architecture, the six skill axes / six agent axes, and the fixed weights — unchanged.
- Codex skill/agent evaluation (`tools/codex-internal/skills/ywc-codex-toolkit-eval`) and its spec — separate owner, not touched.
- `scripts/validate.sh` binary gate — unchanged; this skill remains the graded layer on top.
- Re-tuning any 0–5 banding thresholds beyond the specific A7 / A5 / S2 corrections named above.
- Producing a NEW scorecard run / regenerating `evals/scorecard.md` content as a deliverable — verification re-runs the scorer but does not re-grade the catalog as output.
- Adding README locale files for this skill (decision: internal-only exemption, Item 11).

## Existing Constraints Touched (verified, file:line)

Every claim below was read end-to-end during investigation; downstream tasks must preserve these behaviors unless the FR explicitly changes them.

- `scripts/score.py:30` — `REPO_ROOT = Path(__file__).resolve().parents[4]`; the scorer evaluates `claude-code/skills` + `claude-code/agents`, NOT its own `.claude/skills` location. Self-exclusion is intentional and must remain.
- `scripts/score.py:36` — `HISTORY_MECH = .../evals/history.mechanical.json`; currently holds 50 keys (verified).
- `scripts/score.py:92-107` — `find_collisions`; exclusion test at `:104` is `if b not in ad and a not in bd` (substring-anywhere). FR6 narrows this to the `Do not use for` clause.
- `scripts/score.py:136-137` — A7 check counts `body.count("\n|", ...) >= 6`. FR4 changes to data-row semantics ≥5.
- `scripts/score.py:129-143` — `checks` dict = fixed 10 rules {A1,A2,A3,A4,A6,A7,A8,A9,A11,A14}; `s2 = round(sum/len*5)`. FR5 reframes/documents this subset.
- `scripts/score.py:220-226` — `_unresolved_sibling_pointers` resolves only against `SKILL_ROOTS`. FR10 adds `AGENT_ROOTS`.
- `scripts/score.py:271` — `a5 = 4 if model else 0`. FR3 replaces with a role↔tier heuristic.
- `scripts/score.py:356-382` — `ci_gate` overwrites `HISTORY_MECH` with `current` on PASS (`:380`); `:394-397` filters by `--item` BEFORE `ci_gate`. FR2 guards this.
- `scripts/score.py:386-391` — argparse accepts only `--target`, `--item`, `--format`, `--ci`. No `--mode` / `--advisor-budget` (orchestrator-level). FR8 clarifies docs.
- `.github/workflows/validate.yml:34,37` — CI invokes `score.py --ci` (no `--item`); the FR2 guard must not break this call.
- `references/skill-rubric.md:42` — "≥5 table rows" (A7 rubric text). FR4 aligns script to this.
- `references/trigger-eval-method.md:14` — "≥3 positives and ≥2 collisions" per item (coverage minimum). FR1 enforces + satisfies this.
- `references/trigger-eval-method.md:75` — `Math.random()`-style wording. FR9 rewords.
- `claude-code/agents/ywc-architect.md:18` (`model: opus`), `ywc-backend-coder.md:13` (`model: sonnet`) — all 12 agents declare `model:`, hence A5≡4 today; FR3's heuristic reads these values.

## Acceptance Criteria

Form: *When `<trigger>`, the system does `<behavior>`, observable as `<concrete check>`.*

**AC1 (Item 1 — coverage data).** When `evals/trigger-cases.json` is loaded, every one of the 50 evaluated items (38 skills + 12 agents) has ≥3 `positive` cases and ≥2 `collision` cases naming the sibling that should win, observable as the coverage report (FR1b) printing `0 items below minimum`.

**AC2 (Item 1 — coverage gate).** When `score.py` runs and an item has fewer than the minimum cases, the item's `signals.coverage` is `{"positives": n, "collisions": m, "sufficient": false}` and its S1/A2 is reported by the judge as `insufficient-coverage` (not a numeric band), observable as a JSON field per item and a scorecard tag.

**AC3 (Item 2 — CI guard).** When `score.py --ci` is combined with `--item`, the script exits non-zero with a clear error and does NOT write `history.mechanical.json`, observable as: `score.py --ci --item ywc-commit` prints an error and leaves the 50-key baseline byte-identical.

**AC4 (Item 2 — CI unaffected).** When `score.py --ci` runs with no `--item` (the CI path at `validate.yml:37`), behavior is unchanged from today, observable as the existing CI job still passing on an unmodified catalog.

**AC5 (Item 3 — A5 heuristic).** When an agent declares a `model:` that mismatches its role tier (e.g., an architecture/root-cause/security-boundary/critic role on a non-Opus model, or a mechanical-enumeration role on Opus), A5 mechanical drops below 5 per `references/agent-rubric.md:76-82` bands, observable as ≥1 catalog agent receiving mechanical A5 ≠ 4 where the role/model pairing warrants it, and well-matched agents receiving 5.

**AC6 (Item 4 — A7 threshold).** When a skill's Rationalization Defense table has exactly 5 data rows, the A7 structural check passes; with 4 it fails, observable as the script counting *data rows* (excluding header + separator) and the rubric text, `SKILL.md`, and script agreeing on the number 5.

**AC7 (Item 5 — S2 honesty).** When S2 is computed, the documented scope matches the implementation, observable as: `references/skill-rubric.md` and `SKILL.md` state S2 scores a defined structural subset (the 10 mechanically-checkable rules), name which A-rules are in/out of mechanical scope, and no longer imply unqualified full "A1–A14" coverage.

**AC8 (Item 6 — clause-aware collision).** When skill A's description mentions sibling B only outside a `Do not use for` clause, `find_collisions` still reports the A↔B collision; when B appears inside A's `Do not use for ... (use ywc-B)` clause, it is excluded, observable as a unit-level check distinguishing the two cases.

**AC9 (Item 7 — counts).** When the docs cite catalog size, the number is current or count-agnostic, observable as `SKILL.md` + `README.md` showing 38 skills / 12 agents (or phrasing that does not hard-code a drifting number), with example scorecards labeled illustrative.

**AC10 (Item 8 — arg ownership).** When a reader consults the Arguments table, script-level vs orchestrator-level flags are distinguished, observable as `SKILL.md` marking `--mode` and `--advisor-budget` as skill/orchestrator args and `--target`/`--item`/`--format`/`--ci` as `score.py` flags.

**AC11 (Item 9 — wording).** When `references/trigger-eval-method.md` discusses determinism, it uses runtime-neutral phrasing, observable as no `Math.random()` token remaining in the file.

**AC12 (Item 10 — agent pointers).** When a description says `use ywc-<name>` where `<name>` is an agent, `_unresolved_sibling_pointers` resolves it against the agent root and does NOT flag it, observable as a unit check over a pointer to a known agent returning empty.

**AC13 (Item 11 — locale exemption).** When this skill's distribution status is questioned, the SKILL.md states it is internal-only and exempt from the en/ja/ko locale-set requirement, observable as an explicit one-line note in `SKILL.md`.

**AC14 (verification & re-baseline).** When `score.py --target all --format json` runs after all changes, it completes without error over all 50 items, and `score.py --ci` regenerates a 50-key `history.mechanical.json` reflecting the new A5/A7/S2 logic, observable as a clean exit and a committed baseline diff limited to intended axis changes.

## Functional Requirements

### FR1 — Trigger-case full authoring + coverage gate (Item 1)
- **FR1a (data):** Author `evals/trigger-cases.json` to cover all 50 items with ≥3 `positive` and ≥2 `collision` cases each, following the `version`/`cases` schema and the paired-collision convention in `references/trigger-eval-method.md:14-43` (the same prompt is a `positive` for the owner and a `collision`+`impostor` for the near sibling). Include ≥1 `negative` per item-cluster. Author in collision-risk order: reviewer family (`ywc-*-reviewer`), executor family (`ywc-*-executor`), PR-lifecycle family (`ywc-commit`/`ywc-create-pr`/`ywc-finish-branch`/`ywc-handle-pr-reviews`) first.
- **FR1b (gate):** `score.py` reads `trigger-cases.json`, computes per-item `{positives, collisions, sufficient}` against the minimum (≥3/≥2), and emits it under `signals.coverage`. When `sufficient` is false, the mechanical output marks S1/A2 as coverage-insufficient so the judge tier and scorecard surface `insufficient-coverage` instead of a fabricated band. A catalog-level summary line prints the count of items below minimum.
- Satisfies AC1, AC2.

### FR2 — Guard `--ci` against `--item` (Item 2)
- In `main()`, reject the `--ci` + `--item` combination before `ci_gate` runs: print a one-line error explaining the baseline would be partial, and `return` non-zero WITHOUT writing `HISTORY_MECH`. The no-`--item` CI path (`validate.yml:37`) is unchanged.
- Satisfies AC3, AC4.

### FR3 — Real A5 heuristic (Item 3)
- Replace `a5 = 4 if model else 0` with a role↔tier heuristic: infer the expected tier from name/description role keywords (architecture / root-cause / critic → Opus; standard coder/reviewer/security static-analysis → Sonnet; mechanical enumeration / formatting / doc → Haiku) and compare to the declared `model:`. Band per `references/agent-rubric.md:76-82`: match → 5; reasonable-but-unjustified → 4; over-provisioned (Opus for mechanical) → 3; under-provisioned (Haiku for frontier judgment) → 2; contradictory catalog pairing → 1; no model where required → 0. Emit `signals.model_expected` alongside `signals.model`.
- **Authoritative mapping is pinned by the current catalog (see `## Iteration 1 Amendments` §A1); FR3 must not regress any agent listed there as expected-correct.**
- Satisfies AC5.

### FR4 — Align A7 row threshold (Item 4)
- Change the A7 check to count Rationalization-Defense **data rows** (total table lines minus header and separator) and require **≥5**. Update `references/skill-rubric.md:42` and `SKILL.md`/the `ywc-skill-author` reference to state the same canonical number (5 data rows). Script and rubric must cite the identical threshold.
- Satisfies AC6.

### FR5 — Make S2 scope honest (Item 5)
- Keep the fixed 10-rule mechanical subset but rename/annotate it as the **S2 mechanical structural subset** in `references/skill-rubric.md` and `SKILL.md`: enumerate the 10 checked rules and explicitly mark A5/A10/A12/A13 (and any other A-rule) as out of mechanical scope (judgment-tier or exempt-by-design). The denominator stays the count of *checked* rules; documentation no longer claims unqualified "A1–A14 compliance."
- Satisfies AC7.

### FR6 — Clause-aware collision exclusion (Item 6)
- In `find_collisions`, replace the substring test `b not in ad` / `a not in bd` with a check that the sibling is named inside a `Do not use for` clause (and its locale equivalents where present). A sibling mentioned only in a cooperative/positive sentence no longer suppresses a real collision.
- Satisfies AC8.

### FR7 — Refresh catalog counts (Item 7)
- Update `SKILL.md` (line ~16/123 region) and `README.md` to 38 skills / 12 agents, OR reword to count-agnostic phrasing; label the Output Format example scorecard as illustrative so it does not read as a current count.
- Satisfies AC9.

### FR8 — Clarify argument ownership (Item 8)
- In `SKILL.md` (and README usage), split the Arguments table into **`score.py` flags** (`--target`, `--item`, `--format`, `--ci`) and **skill/orchestrator args** (`--mode`, `--advisor-budget`), with a note that the latter are not passed to the script.
- Satisfies AC10.

### FR9 — Reword determinism note (Item 9)
- In `references/trigger-eval-method.md:75`, replace the `Math.random()`-style phrasing with runtime-neutral wording (e.g., "no nondeterministic sampling is used; the judge returns its single best match, ties broken by listing order").
- Satisfies AC11.

### FR10 — Resolve agent pointers (Item 10)
- In `_unresolved_sibling_pointers`, resolve `use ywc-<name>` against both `SKILL_ROOTS` and `AGENT_ROOTS` (agents are `claude-code/agents/ywc-<name>.md` files, not directories — match the file form). A pointer to a real agent is not flagged.
- Satisfies AC12.

### FR11 — Internal-only locale exemption note (Item 11)
- Add a one-line note in `SKILL.md` stating this skill lives in `.claude/skills/` as an internal toolkit-maintenance tool, is not distributed under `claude-code/skills/`, and is therefore exempt from the en/ja/ko README locale-set requirement that `validate.sh` enforces on distributed skills.
- Satisfies AC13.

### FR12 — Verify & re-baseline (cross-cutting)
- Run `score.py --target all --format json` and `--format markdown`; confirm clean exit over 50 items and that A5/A7/S2/coverage signals reflect the new logic. Regenerate `evals/history.mechanical.json` via `score.py --ci` and review the diff is limited to intended axis movements. Add a stdlib unit test (`scripts/test_score.py`, runnable via `python3 -m unittest`) covering FR2 (guard), FR3 (A5 bands), FR4 (row count), FR6 (clause exclusion), FR10 (agent pointer) so rubric↔script alignment is regression-protected.
- Satisfies AC14, and protects AC3/AC5/AC6/AC8/AC12.

## Non-Functional Requirements

- **Stdlib-only:** `score.py` and its test must remain dependency-free (`scripts/score.py:16` convention). No third-party packages.
- **Determinism:** Mechanical outputs must stay deterministic and stable run-to-run (no time/random in scored signals).
- **Backward-compatible CI:** `score.py --ci` exit semantics and the `history.mechanical.json` schema (flat `{root/name: {axis: score}}`) must remain compatible with `validate.yml`.
- **Body cap:** `SKILL.md` must stay ≤500 lines after edits (158 today); push any net-new long content to `references/`.

## Data Model — `evals/trigger-cases.json`

```jsonc
{
  "version": 1,
  "cases": [
    { "id": "<item>-pos-N",  "prompt": "<NL prompt>", "expected": "ywc-<owner>", "kind": "positive" },
    { "id": "<owner>-vs-<sibling>-N", "prompt": "<NL prompt>", "expected": "ywc-<owner>",
      "kind": "collision", "impostor": "ywc-<sibling>", "note": "<why owner wins>" },
    { "id": "neg-<topic>-N", "prompt": "<NL prompt>", "expected": null, "kind": "negative" }
  ]
}
```
- `expected` must be a real item name in the evaluated roots; `impostor` (collision only) must be a real sibling.
- Coverage invariant (FR1b enforces): per item, `count(positive where expected==item) ≥ 3` and `count(collision where impostor==item OR expected==item) ≥ 2`.

## API / CLI Contract — `score.py`

| Invocation | Behavior after this spec |
|---|---|
| `score.py --target all --format json` | Per-item axes + `signals` incl. new `coverage`, `model_expected`; otherwise unchanged schema shape |
| `score.py --ci` | Full-catalog regression gate; writes 50-key baseline on PASS (unchanged) |
| `score.py --ci --item X` | **NEW:** non-zero exit, error message, no baseline write (FR2) |
| `score.py --target claude-code/agents --format markdown` | A5 column now varies per role/model fit (FR3) |
| `python3 -m unittest` over `scripts/test_score.py` | **NEW:** runs FR2/FR3/FR4/FR6/FR10 unit checks (FR12) |

`--mode` and `--advisor-budget` are NOT `score.py` flags (FR8) — the skill orchestrator interprets them.

## Edge Cases

- **Agent without `model:`** — A5 = 0 (no model where the harness needs one); must not crash the heuristic.
- **Skill with an empty/absent Rationalization Defense** — A7 fails (0 data rows < 5); no false pass.
- **Item appearing as both owner and impostor across cases** — coverage counts collisions where the item is either `expected` (owner side) or `impostor` (impostor side) per the paired convention; do not double-count the same case id.
- **`Do not use for` written in Japanese/Korean** — clause detection (FR6) should match the locale equivalents actually used in descriptions, or fall back safely (treat an unrecognized-locale clause as present rather than silently dropping a real collision — fail toward reporting).
- **New 39th skill added later** — coverage gate (FR1b) reports it below-minimum until cases are authored; the gate is the guardrail that keeps coverage from decaying, complementing the one-time full authoring.
- **`--item` naming a nonexistent item** — existing behavior (empty results) preserved; `--ci --item` still rejected before that path.

## Open Questions

1. **A5 role-keyword taxonomy source of truth (FR3):** Hard-code the role→tier mapping in `score.py`, or read a small table from `references/agent-rubric.md`? *Proposed default:* hard-code in `score.py` with a comment pointing at the rubric section, mirroring how thresholds already live in the script. *(Non-blocking.)*
2. **Self-test delivery (FR12):** `scripts/test_score.py` runnable via `python3 -m unittest` (proposed default) vs an in-script `--selftest` subcommand. *(Non-blocking — keeps `score.py` free of test scaffolding.)*

(Both are minor implementation-shape choices with stated defaults; neither blocks task decomposition.)

---

## Iteration 1 Amendments

Addresses the `ywc-spec-validate` (iteration 1) findings: 1 Critical, 2 Warning, 2 Suggestion. Original sections above remain authoritative except where a marker or this section supersedes them.

### A1 — (Critical) Pin the A5 role→tier mapping to the current catalog (amends FR3, AC5)

The naive "security-boundary → Opus" reading would have scored the deliberately-Sonnet `ywc-security-engineer` as under-provisioned (A5=2) and frozen that disputed regression into `history.mechanical.json`. The authoritative role→tier table below is derived from the **12 current agents** (verified `model:` values). FR3's heuristic MUST reproduce the "Expected A5" column for these agents; any deviation is an FR3 implementation bug, not a finding about the agent.

| Agent | Declared `model:` | Role class | Expected tier | Expected A5 |
|---|---|---|---|---|
| ywc-architect | opus | architecture judgment | Opus | 5 |
| ywc-root-cause-analyst | opus | root-cause judgment | Opus | 5 |
| ywc-security-engineer | sonnet | **security static-analysis (Sonnet is correct)** | Sonnet | 5 |
| ywc-backend-coder | sonnet | standard implementation | Sonnet | 5 |
| ywc-frontend-coder | sonnet | standard implementation | Sonnet | 5 |
| ywc-qa-engineer | sonnet | standard implementation | Sonnet | 5 |
| ywc-refactor-cleaner | sonnet | standard implementation | Sonnet | 5 |
| ywc-go-reviewer | sonnet | standard review | Sonnet | 5 |
| ywc-python-reviewer | sonnet | standard review | Sonnet | 5 |
| ywc-typescript-reviewer | sonnet | standard review | Sonnet | 5 |
| ywc-performance-engineer | sonnet | standard analysis | Sonnet | 5 |
| ywc-doc-writer | haiku | doc/formatting | Haiku | 5 |

**Mapping rules (authoritative):**
- Opus-expected role keywords: `architect`, `root-cause` / `root_cause` / `rootcause`, `critic`. (Frontier judgment only.)
- Haiku-expected: `doc-writer` / documentation / formatting / mechanical enumeration.
- **Everything else, including `security`, `reviewer`, `coder`, `engineer`, defaults to Sonnet-expected.** Security review in this toolkit is static analysis on Sonnet by design — it is NOT an Opus-expected role. AC5's earlier "security-boundary on non-Opus" example is **superseded**: it is no longer an under-provisioning trigger.
- Band when declared == expected → 5. Opus where Sonnet expected → 3 (over-provisioned). Haiku where Opus expected → 2 (under-provisioned). No `model:` → 0.

**Amended AC5:** When `score.py` scores the 12 current agents, every agent receives mechanical **A5 = 5** (all are correctly tiered per the table above), observable as the agent scorecard showing no A5 < 5 for the current catalog AND a synthetic unit fixture (an Opus-on-mechanical agent and a Haiku-on-architecture agent) receiving 3 and 2 respectively. This proves the heuristic *discriminates* without regressing a correct agent.

### A2 — (Warning) Coverage marking stays out of the CI-flattened axes (amends FR1b, AC2, NFR)

`flatten_mech` (`score.py:348-353`) feeds `ci_gate`'s `val < old` comparison (`score.py:372`); a non-int in the `axes` dict would crash the gate. Therefore:
- FR1b emits coverage **only under `signals.coverage`**. S1 and A2 remain `null` in the `axes` dict (their current state), so `flatten_mech` continues to exclude them and the CI baseline schema `{root/name: {axis: int}}` is unchanged.
- The "insufficient-coverage" surfacing is a **scorecard/judge-tier annotation** read from `signals.coverage.sufficient`, never a value placed in `axes`.
- **Amended AC2:** observable as `signals.coverage = {positives, collisions, sufficient}` present per item AND `flatten_mech` output containing no S1/A2 key (CI baseline shape byte-compatible with today's 50-key file).

### A3 — (Warning) FR3 + FR12 must land atomically (amends FR12, adds NFR)

FR3 shifts mechanical A5 values; `score.py --ci` fails on any per-axis drop vs the committed baseline. To avoid a red CI:
- The FR3 code change and the `evals/history.mechanical.json` regeneration (FR12) MUST be in the **same commit/PR**. The task decomposition must NOT split "change A5 logic" and "re-baseline" into separately-mergeable tasks.
- Per A1, the current catalog yields A5=5 for all 12 agents (same as today's constant 4 → 5 is an *increase*, never a drop), so the baseline diff for agents is a uniform A5 4→5 with **no regression** — CI passes. The re-baseline still must be committed because an increase changes the stored value the next run compares against.
- **Amended AC14:** additionally observable as `git diff evals/history.mechanical.json` showing agent A5 entries moving 4→5 (no value decreasing), confirming no CI regression is introduced.

### A4 — (Suggestion, accepted) Simplify FR6 to the live clause form (amends FR6, Edge Cases)

All 40 `Do not use for` occurrences in the current catalog are English. FR6 matches the literal English `Do not use for` clause; localized (JA/KO) clause detection is **deferred** (future-proofing, not implemented now). The "fail toward reporting on unrecognized-locale clause" edge case is retained as the safe default but is currently unexercised.

### A5 — (Suggestion, accepted) One shared case file (amends FR1a, Data Model)

Skills and agents share a single `evals/trigger-cases.json`. `expected` and `impostor` may name either a skill or an agent (cross-root), since activation/dispatch collisions can occur within each root. The coverage invariant (FR1b) is computed per item name regardless of root.

### Step 4b.5 re-run on the whole spec (original + amendment)
- **Pass A (cross-section):** Amended AC5/AC2/AC14 each map to FR3/FR1b/FR12 respectively; no orphan AC or FR introduced. A5 table values are internally consistent (all 12 → 5). ✓
- **Pass B (claim↔reality):** A1 table verified against live `model:` values (`grep '^model:' claude-code/agents/ywc-*.md`); `flatten_mech`/`ci_gate` line citations re-confirmed; "40 English clauses" verified by grep count. ✓
- **Pass C (schema):** No DB schema. `trigger-cases.json` and `history.mechanical.json` schemas restated; A2 guarantees the CI baseline shape is unchanged. ✓

