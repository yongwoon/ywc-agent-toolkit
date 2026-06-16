# Codex Toolkit Eval Improvements

> Status: Ready for task generation
> Scale: Medium
> Created: 2026-06-16
> Author: Codex
> Spec Reference: Review findings from `ywc-codex-toolkit-eval` audit on 2026-06-16

## Operative Sections

Task generation must treat the original sections as authoritative except where
`## Iteration 1 Amendments` supersedes them. In particular, use the amended
verification command block in Iteration 1 instead of the original `##
Verification Commands` block.

## Purpose

Improve the internal `ywc-codex-toolkit-eval` skill so its documented
workflow, scorer behavior, trigger-evaluation references, fixtures, and README
usage examples agree with each other. The current skill validates structurally,
but the review found drift that can mislead future evaluators: documented flags
that do not exist, a mislabeled agent routing axis, insufficient trigger fixture
coverage against the skill's own threshold, a targeted item miss that exits
successfully, and Codex-only docs that still describe Claude trigger behavior.

The outcome is a taskable implementation plan only. No implementation belongs
to this planning pass.

## Scope

- Align `--mode` behavior across `SKILL.md`, README locale files, and
  `scripts/score.py`.
- Make `score.py --item <name>` fail loudly when the requested target is not
  found.
- Correct trigger-evaluation axis wording from `A2` to `A1` for Codex agents.
- Add deterministic trigger fixture coverage checks for the documented minimum
  of 3 positive cases and 2 impostor/collision cases per evaluated item.
- Replace Claude activation wording in Codex-only references with Codex
  metadata terminology.
- Update tests so every behavior above is covered before implementation is
  considered complete.
- Clean local ignored runtime artifacts if they are present in the working tree.

## Out of Scope

- Rewriting the evaluator's judgment rubric beyond the axis-label correction.
- Expanding every under-covered trigger fixture to full 3-positive/2-collision
  coverage in the same implementation batch. The batch must add enforcement and
  at least cover `ywc-codex-toolkit-eval`; broad catalog fixture expansion can
  be a follow-up if the checker initially runs in warning/report mode.
- Changing distributed Codex skills under `codex/skills/**`.
- Changing Claude Code skills, Claude agents, or `.claude/**`.
- Running `ywc-task-generator` or implementing this spec in this planning turn.
- Updating root release metadata such as `VERSION` or `CHANGELOG.md`.

## Existing Constraints Touched

| Existing artifact | Behavior verified by reading the file | New code's interaction |
|---|---|---|
| `AGENTS.md:5` | Codex skills require README locale files and `agents/openai.yaml`; internal Codex material is separate from distributed skills. | Keep this internal evaluator under `tools/codex-internal/skills/ywc-codex-toolkit-eval/` and retain the README locale set. |
| `AGENTS.md:15` | `bash scripts/validate.sh` is the required pre-PR test. | The implementation must keep this command green. |
| `CLAUDE.md:68` | Codex `SKILL.md` frontmatter must contain only `name` and `description`. | Do not add frontmatter metadata while editing `SKILL.md`. |
| `CLAUDE.md:85` | CI validates structure, markdown, translation warnings, and shell checks. | Add tests through existing Python unittest/local validation surfaces. |
| `codex/AGENTS.md:24` | There is no package test runner; development is primarily Markdown and shell scripts. | Use focused Python unittest and `bash scripts/validate.sh`, not a new package toolchain. |
| `.gitignore:4` | `__pycache__/` is ignored. | Local `scripts/__pycache__/score.cpython-314.pyc` may be removed as cleanup, but it is not a tracked deliverable. |
| `.gitignore:20` | The internal evaluator `evals/` directory is ignored for new untracked files. | Avoid adding brand-new ignored eval files unless `.gitignore` is intentionally adjusted. Existing tracked eval files can be edited. |
| `scripts/validate.sh:389` | Internal toolkit evaluator is validated as an internal tool. | Keep `SKILL.md`, README locale files, `agents/openai.yaml`, `scripts/score.py`, `scripts/inventory_gate.py`, and `scripts/test_score.py` present. |
| `scripts/validate.sh:516` | Local validation runs `score.py --ci` as the mechanical regression gate. | Any scoring change must keep `history.mechanical.json` reviewed and `--ci` passing. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md:54` | `--target` is documented for `score.py` as `all`, `codex/skills`, or `codex/agents`. | Preserve this contract. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md:56` | `--mode mechanical|judge|full` is documented, but `score.py` does not parse it. | Either implement mode parsing or remove it from script-facing docs; this spec chooses implementation for `score.py`. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md:79` | Skill judgment axes are S1/S4/S8 and agent judgment axes are A1/A3/A8. | Trigger-eval references must name `A1`, not `A2`. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md:198` | Validation refers to `score.py --format markdown` unless `--mode judge` is explicit. | After `--mode` is implemented, validation wording and command behavior must agree. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py:345` | The scorer output mode is always `"mechanical"`. | In `--mode mechanical`, preserve this output; in `--mode full` or `judge`, report unsupported/partial behavior explicitly unless implemented. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py:330` | Filtering by `--item` can produce zero items and still exit 0. | Add a not-found failure path when `--item` is supplied. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py:101` | Current tests verify mechanical partial axes. | Extend tests for `--mode`, item-not-found, and trigger fixture coverage. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md:1` | The title currently says `S1 / A2`. | Change to `S1 / A1`. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md:52` | The text says description-only judging mirrors Claude auto-trigger behavior. | Replace with Codex skill/agent metadata activation wording. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json:3` | The fixture describes the 3-positive/2-collision goal as future expansion. | Add checker behavior that reports under-coverage deterministically and can gate the evaluator's own target coverage. |
| `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.md:16` | README shows `$ywc-codex-toolkit-eval --mode full --target all`. | Keep or rewrite this example consistently with the chosen `--mode` contract, and mirror across README locale files. |

Architectural Advisor Gate: skipped. The change is a bounded maintenance fix
inside one internal skill, with no unresolved architecture decision.

## Scale Assessment

Scale: Medium.

Reason: the work touches 4-15 expected tasks across the internal skill body,
Python scorer, tests, trigger reference, tracked fixture(s), and README locale
files. No database migration, new library, external API contract, or
cross-cutting application runtime change is involved.

## Confidence Gate

Confidence Gate Report

Aggregate: 91/100 - PROCEED

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 95 | The review findings define six bounded changes and explicit exclusions. |
| Architecture compliance | 90 | Existing internal-tool layout and validation hooks already support this change. |
| Evidence quality | 90 | Findings are grounded in file:line reads and command output from `score.py`, `inventory_gate.py`, and tests. |
| Reuse verified | 85 | Existing `score.py`, `test_score.py`, and `validate.sh` are sufficient; no new framework needed. |
| Root cause identified | 95 | Root cause is documentation/runtime/test drift in the evaluator, not missing packaging structure. |

Decision: PROCEED to task generation after spec validation. Do not implement in
this planning turn.

## Acceptance Criteria

- [ ] **AC1 - `--mode` contract works**: When `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown` is run, it exits 0 and produces the same mechanical partial scorecard shape currently produced without `--mode`.
- [ ] **AC2 - unsupported modes are explicit**: When `score.py --mode judge` is run before any judge implementation exists, it exits non-zero with a clear message that judge mode is not implemented by the deterministic scorer, or the implementation supplies a real judge-mode path. The README and `SKILL.md` must match whichever behavior is implemented.
- [ ] **AC3 - targeted miss fails**: When `score.py --target codex/skills --item no-such-skill --format markdown` is run, it exits non-zero and stderr names the missing item and selected target.
- [ ] **AC4 - targeted hit still works**: When `score.py --target codex/skills --item ywc-plan --format json` is run, it exits 0 and returns exactly one skill item under `roots.codex/skills`.
- [ ] **AC5 - trigger axis docs are correct**: When `rg -n "S1 / A2|agent-rubric.md.*A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md` is run, it returns no matches.
- [ ] **AC6 - trigger coverage checker exists**: When the focused test suite is run, it verifies that trigger coverage reporting counts positive cases and impostor/collision coverage per item using `trigger-cases.json`.
- [ ] **AC7 - evaluator target coverage is enforceable**: The checker asserts that `ywc-codex-toolkit-eval` has at least 3 positive cases and 2 impostor/collision cases, or emits a deterministic failure naming the missing counts.
- [ ] **AC8 - broad catalog under-coverage is visible without blocking unrelated fixes**: The checker can report the full under-covered catalog count, but the initial implementation must not require immediately expanding all 46 currently under-covered items unless the implementation task explicitly chooses a full fixture-expansion batch.
- [ ] **AC9 - README usage examples match reality**: `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md` no longer show a command shape that fails against the implemented scripts.
- [ ] **AC10 - tests cover regressions**: `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py` includes and passes tests for `--mode mechanical`, missing `--item`, successful targeted item, and trigger coverage calculation.
- [ ] **AC11 - full repo validation passes**: `bash scripts/validate.sh` exits 0 after the changes.
- [ ] **AC12 - no internal evaluator leak**: `test ! -e codex/skills/ywc-codex-toolkit-eval && test ! -e .codex-plugin/skills/ywc-codex-toolkit-eval` exits 0.
- [ ] **AC13 - ignored local artifacts are cleaned if present**: `find tools/codex-internal/skills/ywc-codex-toolkit-eval -path '*/__pycache__/*' -o -path '*/evals/history.json' -o -path '*/evals/scorecard.md'` returns no local runtime artifacts after cleanup, or the implementation report states why ignored local files were intentionally left untouched.

## Functional Requirements

### FR-1: Implement or reconcile `--mode`

Add `--mode` to `scripts/score.py` or remove it from user-facing command
surfaces. This spec selects the implementation path:

- Add `--mode` choices: `mechanical`, `judge`, `full`.
- Treat omitted `--mode` as `mechanical` for backward compatibility.
- For `mechanical`, preserve current behavior and output schema.
- For `judge` and `full`, either:
  - implement real orchestration if the implementation scope intentionally
    expands to it, or
  - fail with a clear non-zero message explaining that `score.py` is the
    deterministic mechanical scorer and the skill body owns judgment/full
    evaluation.
- Update `SKILL.md` arguments and validation wording so users understand which
  command is script-supported and which behavior is skill-mediated.
- Update README locale usage examples to avoid showing a failing command.

### FR-2: Fail loudly on missing `--item`

Modify the scorer so a requested `--item` that matches no skill/agent in the
selected target exits non-zero. The error must include:

- the item name;
- the target root;
- enough context to distinguish "wrong target" from "typo".

Do not fail when no `--item` is supplied and a root is legitimately empty.

### FR-3: Correct trigger-evaluation terminology

Update `references/trigger-eval-method.md`:

- Change the title and mapping section from `S1 / A2` to `S1 / A1`.
- Replace references to `agent-rubric.md (A2)` with `agent-rubric.md (A1)`.
- Replace Claude activation wording with Codex metadata wording. The principle
  remains description-only judging, because runtime activation sees metadata
  before any body loads.
- Keep the scoring method intact unless tests prove the formula itself is wrong.

### FR-4: Add trigger fixture coverage checks

Add deterministic coverage logic near the existing scorer tests. Prefer a small
pure function in `score.py` only if it is useful to runtime output; otherwise
keep the checker in `test_score.py` to avoid expanding the scorer API.

Minimum behavior:

- Parse `evals/trigger-cases.json`.
- Count per item:
  - positive cases where `expected == item`;
  - collision/impostor cases where `impostor == item`.
- Verify `ywc-codex-toolkit-eval` reaches at least 3 positives and 2
  impostor/collision cases.
- Produce a readable under-coverage report for the broader catalog.
- Keep broad catalog under-coverage as informational unless the implementation
  explicitly commits to fixture expansion for every item.

If the implementation adds new tracked fixture files under `evals/`, first
adjust `.gitignore` intentionally because `.gitignore:20` ignores new files in
that directory. Editing existing tracked files (`evals.json`,
`history.mechanical.json`, `trigger-cases.json`) does not require an ignore
change.

### FR-5: Update localized README files

Update all README locale files for `ywc-codex-toolkit-eval` so examples match
the final command contract:

- If `--mode mechanical` is implemented, README examples may include it.
- If `judge/full` stay skill-mediated rather than script-supported, README
  examples must not imply direct script support for `--mode full`.
- Keep the internal-only boundary warning intact in every locale.

### FR-6: Clean ignored local artifacts

During implementation cleanup, remove ignored runtime artifacts if present:

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/__pycache__/`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/history.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/scorecard.md`

These removals are local hygiene unless the files are tracked. Do not add new
ignored artifacts to the commit.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Compatibility | Existing invocations without `--mode` continue to work. |
| Determinism | New tests and coverage checks must not depend on network, model calls, or current date beyond existing scorecard date output. |
| Scope control | Changes remain inside the internal evaluator plus plan/log docs. |
| Maintainability | Prefer focused functions and tests over a broad evaluator rewrite. |
| Localization | README locale examples must remain semantically aligned across Korean, English, Japanese, and Korean locale mirror files. |

## Data Model

N/A - no database schema, persistence schema, ORM model, migration, relation,
index, or enum change.

## API Contract

N/A - no HTTP, RPC, GraphQL, or external service API contract change.

## Edge Cases

- **Backward compatibility**: Existing CI calls `score.py --ci`; this must keep
  working without requiring `--mode mechanical`.
- **Mode ambiguity**: If `--mode full` remains skill-mediated, do not leave README
  examples that look like direct script commands.
- **Wrong target**: `--item ywc-plan --target codex/agents` should fail as a
  target mismatch, not silently score zero items.
- **Fixture expansion scope**: The current fixture file has 75 cases across 47
  items and 46 under-covered items by the documented threshold. Do not make
  full-catalog expansion a hidden prerequisite unless the task explicitly opts
  into that larger fixture batch.
- **Ignored eval directory**: New files under `evals/` will be ignored by
  `.gitignore`; either edit tracked files or explicitly change ignore rules.
- **Local runtime artifacts**: `__pycache__` and ignored scorecard/history files
  may exist locally without showing in `git status`; cleanup should use `find`.

## Dependencies

- Python standard library only.
- Existing repository validation commands:
  - `python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
  - `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown`
  - `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown`
  - `bash scripts/validate.sh`

## Open Questions

N/A - none identified. The implementation can choose the smaller compatible
path for `judge/full`: fail explicitly in `score.py` while keeping judgment/full
evaluation as a skill-body workflow.

## Implementation Plan

1. Update `scripts/score.py` argument parsing and target filtering.
   - Add `--mode` with default `mechanical`.
   - Preserve current output for mechanical mode.
   - Add explicit non-zero behavior for unsupported `judge/full` unless the
     implementation intentionally adds those modes.
   - Return non-zero when `--item` matches zero assets in the selected target.
2. Extend `scripts/test_score.py`.
   - Add tests for `--mode mechanical`.
   - Add tests for unsupported `--mode judge/full` if not implemented.
   - Add tests for missing and successful `--item`.
   - Add trigger fixture coverage tests.
3. Update `references/trigger-eval-method.md`.
   - Replace `A2` trigger references with `A1`.
   - Replace Claude activation wording with Codex metadata activation wording.
4. Update `evals/trigger-cases.json`.
   - Ensure `ywc-codex-toolkit-eval` has at least 3 positives and 2 impostor
     collision cases.
   - Keep additions realistic user phrasing in Korean/English/Japanese where
     useful.
5. Update `SKILL.md` and README locale files.
   - Align argument table, examples, and validation checklist with actual
     script behavior.
6. Clean ignored local artifacts if present.
7. Run verification commands and update `history.mechanical.json` only if a
   reviewed mechanical score change intentionally changes the baseline.

## Verification Commands

> SUPERSEDED by Iteration 1 - see `## Iteration 1 Amendments`.

```bash
python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json
rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md
test ! -e codex/skills/ywc-codex-toolkit-eval
test ! -e .codex-plugin/skills/ywc-codex-toolkit-eval
bash scripts/validate.sh
```

Expected notes:

- The missing-item command should exit non-zero after implementation; tests
  should assert that behavior rather than treating it as a failure.
- The `rg` command should return no matches after implementation.

## Spec-Ready Refinement

This plan was refined using the `ywc-spec-ready` readiness criteria before
handoff:

- AC/FR consistency: every acceptance criterion maps to an implementation
  requirement or verification command.
- Feasibility: no new package manager, DB, API, or external service dependency
  is introduced.
- Code compatibility: existing validation hooks and scorer tests are reused.
- Convergence status: no Critical readiness issue remains in this planning
  artifact.

## References

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/SKILL.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/trigger-cases.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.en.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.ja.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/README.ko.md`
- `scripts/validate.sh`

## Iteration 1 Amendments

### Failed Requirement Addressed

The original `## Verification Commands` block mixed normal success commands
with commands whose expected result is non-zero or "no matches." A downstream
task runner could execute that block literally and mark the correct behavior as
a failure.

### Amended Approach

Use assertion-shaped commands for negative expectations:

- A missing `--item` is success only when `score.py` exits non-zero.
- A stale trigger-doc phrase check is success only when `rg` finds no matches.
- README locale examples are checked explicitly for stale direct `--mode full`
  usage.

### Updated Acceptance Criteria

- [ ] **AC14 - negative verification commands are assertion-shaped**: When the
  verification command block is copied into a shell with `set -e`, expected
  negative checks do not abort the run because they are wrapped with `!` or an
  equivalent explicit assertion.

### Amended Verification Commands

```bash
python3 -m unittest tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown
! python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item no-such-skill --format markdown
python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target codex/skills --item ywc-plan --format json
! rg -n "S1 / A2|A2 Band|Claude's auto-trigger" tools/codex-internal/skills/ywc-codex-toolkit-eval/references/trigger-eval-method.md
! rg -n '\$ywc-codex-toolkit-eval --mode full' tools/codex-internal/skills/ywc-codex-toolkit-eval/README*.md
test ! -e codex/skills/ywc-codex-toolkit-eval
test ! -e .codex-plugin/skills/ywc-codex-toolkit-eval
bash scripts/validate.sh
```

### Self-Consistency Re-check

- AC14 maps to the amended verification command block.
- AC1-AC13 remain unchanged.
- The amended commands do not introduce a new data model, API contract, package
  dependency, or implementation scope.
