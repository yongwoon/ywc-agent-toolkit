---
name: ywc-refactor-clean
description: >-
  (ywc) Use when removing dead code (unused functions / exports / files /
  dependencies / imports), consolidating near-duplicate utilities, or running a
  scheduled hygiene pass on a codebase. Triggers: "dead code 제거", "unused
  import 정리", "knip / depcheck / ts-prune 돌려줘", "refactor clean", "dead
  code cleanup", "remove unused exports", "デッドコード削除", "未使用
  import 整理", "ywc-refactor-clean". Do not use for active feature
  implementation in the same branch (the cleanup competes with the feature
  diff — finish the feature, then clean), for behavior-changing refactors
  (use ywc-tdd-ritual + ywc-code-gen so behavior is captured by tests first),
  or for performance / architecture restructuring (out of scope — this skill
  is byte-for-byte equivalence on the public surface).
---

# ywc-refactor-clean

**Announce at start:** "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."

This skill is the canonical dead-code-removal discipline for ywc. It exists because hand-rolled cleanup (`grep + delete + hope`) routinely breaks dynamic imports, public package exports, and CI-only code paths. Adapted from `ECC/refactor-cleaner` (Sonnet agent) and `ECC/refactor-clean` (slash command), tightened to delegate completion claims to `ywc-verify-done` and to forbid bundled behavior changes (those route to `ywc-tdd-ritual` + `ywc-code-gen`).

## The Iron Law

```text
NEVER DELETE WITHOUT (1) DETECTION TOOL CONFIRMS + (2) GREP CONFIRMS NO REFERENCES + (3) TESTS PASS AFTER EACH BATCH
```

A symbol that `knip` says is unused but `grep` finds in a `require()` string is **not** dead — that is a dynamic import. A function that `ts-prune` says is unused but is the package's public export is **not** dead — that is an external consumer. Single-source confirmation is not confirmation; the discipline requires two independent witnesses (tool + grep) plus a behavioral witness (tests).

If a deletion is committed and a downstream test breaks, **revert that commit first**, then re-classify the item to CAUTION or DANGER. Do not chase the failure forward with a follow-up "fix" commit — the original commit is the regression.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "knip / ts-prune already says it is unused — skipping the grep step" | The detection tool runs static analysis over the module graph. It cannot see: (a) `require(`${name}`)` dynamic imports, (b) string references in CI configs / IaC / docker / docs, (c) plugin auto-discovery (e.g., `*.test.ts` collected by a test runner via glob), (d) public package exports consumed by an external repo. The grep is the second witness — without it, ~5% of "unused" deletions break something. |
| "I'll batch 30 deletions into one commit — faster to review" | Each deletion is one commit. Bisectability is the ENTIRE point — when test X starts failing two weeks later, `git bisect` must land on the exact deletion that caused it. A 30-deletion commit forces a human to re-classify all 30 by hand. |
| "Tests passed locally, no need to re-run after each batch" | "After each batch" means after each tier (SAFE all done → run, CAUTION all done → run). Skipping intra-batch test runs means you lose the cheap rollback signal — a broken test now requires manual diff inspection to find which deletion broke it, instead of `git revert <last-commit>`. |
| "The duplicate helpers look identical — I'll merge them in this PR" | Consolidating duplicates is a behavior change (call sites now resolve to a different implementation). Behavior changes belong to `ywc-tdd-ritual` + `ywc-code-gen`, not this skill. This skill removes dead code; it does not refactor live code. |
| "Removing this dependency would shave 200kb — even though some tests still import it" | Tests are code. If a test imports the dependency, the dependency is not unused. Either the test is dead (delete it under the same tier discipline), or the dependency is live (skip it). "Remove the dep and rewrite the test" is a feature-PR sized scope creep — out of scope here. |
| "knip flagged `src/legacy/` as unused — deleting the whole directory" | Directory-scale deletion crosses the SAFE boundary into DANGER regardless of what the tool says. Each file in the directory needs its own tier classification + per-file delete + test run. Bulk-deleting a directory and then "fixing the fallout" is the inverse of the discipline. |
| "I'm in a hurry — I'll skip the verify-done block at the end" | The per-batch test run is the discipline. The `ywc-verify-done` block at the end is the **claim** that the cleanup is complete and safe — without it, the PR description says "removed N items" without evidence the suite passed. The reviewer cannot tell whether you ran the suite or hoped. |
| "I'll run this during the active feature branch — kill two birds" | The feature branch's diff already mixes new behavior + new tests. Adding 30 deletions on top makes the review impossible (reviewer cannot distinguish "this delete was safe" from "this delete broke the new feature"). Always cleanup in its own branch. |

**Violating the letter of this discipline is violating the spirit.** Cleanup that introduces a regression is more expensive than the cleanup ever saved — the regression debugging cost typically exceeds the bundle-size win by 10×.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--scope` | `--scope <dir>` | `--scope src/` | Restrict detection + deletion to a path. Default: repository root. |
| `--tier` | `--tier safe\|safe+caution\|all` | `--tier safe` | Stop after the named tier. Default: `safe` (most conservative). |
| `--dry-run` | flag | `--dry-run` | Run detection + classification + grep verification, but emit a report instead of mutating files. |
| `--skip-verify-done` | flag | `--skip-verify-done` | Skip the final `ywc-verify-done` handoff. Only valid when the caller (e.g., `ywc-finish-branch`) will run it. |

## Workflow

### Step 1: Detect

Run the language-appropriate detection tools in **parallel**. The matrix below is the canonical mapping — extend [`references/detection-tools.md`](references/detection-tools.md) when adding a new language / tool, not this body.

| Ecosystem | Primary tool | What it finds | One-line invocation |
|---|---|---|---|
| JS / TS | `knip` | Unused files, exports, dependencies, types | `npx knip` |
| JS / TS | `depcheck` | Unused npm dependencies | `npx depcheck` |
| TS only | `ts-prune` | Unused TypeScript exports | `npx ts-prune` |
| Python | `vulture` | Unused functions, classes, imports | `vulture src/` |
| Go | `deadcode` | Unused functions, types | `deadcode ./...` |
| Rust | `cargo-udeps` | Unused crate dependencies | `cargo +nightly udeps` |
| Universal fallback | `grep` | Symbols defined but never referenced | see `references/detection-tools.md` |

For an unsupported ecosystem, use the `grep`-based fallback in [`references/detection-tools.md`](references/detection-tools.md) — do not invent a new tool.

### Step 2: Classify into tiers

Sort every finding into exactly one tier. Items that match multiple tiers escalate to the highest tier.

| Tier | Pattern | Action |
|---|---|---|
| **SAFE** | Internal helper, test fixture, private function with no `export` keyword, internal type alias | Delete with per-item verification (Step 3) |
| **CAUTION** | Component, route handler, middleware, public-but-internal export, any symbol with `import()` or `require()` patterns matching its name anywhere in the repo | Manual verification (Step 4) before deletion |
| **DANGER** | Public package export (in `exports` / `main` / `module` field of `package.json`), config file, entry point, type definition consumed by an external API, anything `git log` shows touched in the last 7 days | Investigate (Step 5) — do not delete in this skill's scope |

Full classification rules with concrete examples live in [`references/safety-tiers.md`](references/safety-tiers.md).

### Step 3: SAFE deletion loop

The 5-substep loop below is the work the Codex operator performs per item. If another runtime provides a dedicated deletion worker, treat that worker as an execution detail only; Codex still owns the same SAFE worklist discipline, evidence capture, and rollback rules inline.

For each SAFE item, in order:

1. **Run the test suite scoped to the item's domain.** Establish that the suite is green *before* the deletion, so a later failure can be attributed to the deletion (and not pre-existing).
2. **Verify with grep.** `git grep -nE '<symbol>'` (or pattern-matched variant for dynamic patterns). Zero hits = proceed. Any hit = re-classify to CAUTION and skip.
3. **Delete the item** with the `Edit` tool — surgical removal, no adjacent re-formatting.
4. **Re-run the same test suite.** If green, commit (next step). If red before the commit, restore the edited files to the pre-delete state and re-classify to CAUTION. If a regression appears after the commit lands, `git revert <commit>` and re-classify to CAUTION — `git revert` is the atomic rollback for multi-file deletions.
5. **Commit** with shape `chore(cleanup): remove unused <symbol> (knip)` — name the tool that flagged it. One deletion per commit.

Do **not** batch multiple deletions into one commit. Bisectability is the entire reason for per-item commits — when a regression surfaces in week 3, `git bisect` lands on the exact deletion.

### Step 4: CAUTION verification

Before deleting any CAUTION item, run all three checks:

1. **Dynamic import search**: `git grep -nE "(import|require)\\([\\\"'\\\\\`].*<symbol>.*[\\\"'\\\\\`]\\)"` — catches `import('./modules/' + name)` patterns where the symbol appears as a string fragment.
2. **String-reference search**: `git grep -nE "[\\\"'\\\\\`]<symbol>[\\\"'\\\\\`]"` — catches route names, plugin slugs, config keys, doc references.
3. **Public-API check**: `cat package.json | jq '.exports, .main, .module, .bin'` (or language equivalent) — if the symbol appears in any of these, it is reachable from outside the repo. Re-classify to DANGER.

Zero hits across all three → proceed with Step 3 deletion loop. Any hit → escalate to DANGER (do not delete in this skill).

### Step 5: DANGER — do not delete

For each DANGER item, **emit a report entry** (Step 7) but do not delete. DANGER deletions belong to a separate intentional change (a major version bump, an API deprecation cycle, an external-consumer migration) — not this skill.

### Step 6: Consolidate duplicates

This step is **opt-in via `--tier all`** and is reserved for `git diff`-quality consolidations. Skip if `--tier` is `safe` or `safe+caution`.

> When choosing the canonical implementation and judging what "simpler" means, apply the shared readable-code rubric and respect its anti-dogma guardrails (do not over-simplify or drop a helpful abstraction). See [../references/readable-code.md](../references/readable-code.md).

For near-duplicate functions (>80% AST or text similarity by inspection):

1. Pick the canonical implementation (best-tested, most-complete, fewest call sites needing rewrite).
2. Update each call site to import from the canonical location.
3. Run the full test suite — if green, delete the duplicate. If red, revert and skip the consolidation.

If the consolidation requires **any** behavior reconciliation (the two implementations differ in edge-case handling, error shape, type signatures), it is no longer cleanup — it is a behavior change. Route to `ywc-tdd-ritual` + `ywc-code-gen` and skip the consolidation here.

### Step 7: Verify-done handoff

Hand off to `ywc-verify-done` with the cleanup report (Output Format below). The handoff is mandatory unless `--skip-verify-done` was passed by an upstream caller that will perform its own verify.

## Output Format

The cleanup commit series is closed by a single Verification Report following the Output Format below. The report is what the PR description quotes when delegating to `ywc-create-pr`.

```text
Dead Code Cleanup Report
─────────────────────────────────────────────────
Scope:           src/   (or --scope value)
Tier reached:    safe   (or safe+caution / all)
Detection tools: knip 5.x, depcheck 1.4, ts-prune 0.10

Deleted (SAFE):
  - 12 unused functions      (12 commits)
  -  3 unused files          ( 3 commits)
  -  5 unused dependencies   ( 5 commits)

Deleted (CAUTION):           N/A — --tier was safe

Skipped (re-classified up):
  - 2 SAFE items moved to CAUTION (grep found dynamic import)
  - 1 CAUTION item moved to DANGER (public package export)

DANGER items reported (not deleted):
  - src/legacy/v1-api.ts          (public package export)
  - src/plugins/registry.ts       (plugin auto-discovery target)

Verification (per ywc-verify-done):
  $ npm test
  exit 0  (PASS  — 482 / 482)
  $ npm run build
  exit 0  (PASS  — bundle reduced from 2.41 MB → 2.38 MB)
  $ npm run lint
  exit 0  (PASS)
─────────────────────────────────────────────────
Bundle delta:    -30 KB gzipped (-1.2 %)
Lines removed:   ~450
```

The verification block at the bottom MUST follow `ywc-verify-done`'s `command → exit code → claim` shape. The "PASS" / "FAIL" wording is required; vocabulary like "should pass" / "probably green" is forbidden by `ywc-verify-done`.

## Integration

- **Upstream**: user invocation; scheduled hygiene pass (e.g., monthly cleanup branch); `ywc-onboard-repo` (when entering a repo where prior dead-code accumulation blocks comprehension).
- **Downstream**: `ywc-verify-done` (mandatory final claim); `ywc-create-pr` (cleanup branches ship as their own PRs); `ywc-impl-review` (reviewer audit of the per-commit deletions, especially CAUTION reclassifications).
- **Pairs with**: `ywc-confidence-gate` (when a deletion is ambiguous between CAUTION and DANGER, the gate's PROCEED / REVIEW / STOP bands map directly: ≥90 = CAUTION delete, 70-89 = REVIEW with reviewer, <70 = re-classify to DANGER).
- **Must not be paired with**: `ywc-code-gen` in the same branch (cleanup and feature must ship separately — see Rationalization Defense row 8).

## Validation Checklist

Before declaring the cleanup pass complete, verify:

- [ ] At least one detection tool ran and its output is captured in the report
- [ ] Every deleted item has a one-line commit (`chore(cleanup): remove ...`)
- [ ] Every reclassification (SAFE → CAUTION → DANGER) is logged in the report
- [ ] Tests passed after each tier transition (not just at the end)
- [ ] No commit in the series contains a behavior change (only deletions)
- [ ] No commit consolidates duplicates with reconciled semantics (those route to `ywc-code-gen`)
- [ ] Final `ywc-verify-done` block uses the canonical wording (PASS / FAIL — never "should pass")

## Common Mistakes

(Procedural failure modes specific to dead-code removal. Behavioral rationalizations are in the table above — do not duplicate here.)

- **Re-running detection tools mid-loop to "re-check" after each deletion.** Detection tools cache module graphs; the second run will report stale findings. Run detection **once** at Step 1, classify **once** at Step 2, then process the worklist linearly. Re-running mid-loop wastes CI minutes and produces false-positive re-flags.
- **Treating `git checkout -- <file>` as the rollback for a multi-file deletion.** If the deletion spanned files (e.g., removed a function and its sole caller's import), the checkout reverts only one file and leaves the codebase in a half-deleted state. Use `git revert <commit>` instead — atomic rollback of the entire commit.
- **Deleting a `--dry-run` finding without re-running the tool live.** `--dry-run` output is a snapshot; if another commit landed between the snapshot and the live run, the finding may be stale. Always re-run live before deletion.
- **Skipping the SAFE tier "because there's nothing interesting there" and jumping to CAUTION.** SAFE items are where the test suite proves the discipline works for this codebase — they validate that the suite covers the deletion paths. Skipping them means the first signal that the suite is incomplete arrives during a CAUTION deletion, where the rollback cost is higher.
- **Letting bundle-size pressure shortcut the discipline.** "We need this 10 KB win for the launch" is exactly when CAUTION deletions break production. The launch pressure makes you skip the grep step; the grep step is the protection. Either ship the launch without the cleanup or budget extra time for the cleanup gate.

## References

| Reference | Use when |
|---|---|
| [references/detection-tools.md](references/detection-tools.md) | Picking a tool for a new ecosystem; writing the grep-based fallback for an unsupported language |
| [references/safety-tiers.md](references/safety-tiers.md) | Classifying a borderline item (SAFE vs CAUTION vs DANGER) — full rules with concrete examples |
| `ywc-verify-done` | Per-batch verification block shape (command + exit code + claim) — mandatory at Step 7 |
| `ywc-code-gen` | When a "duplicate consolidation" turns out to require behavior reconciliation, route there |
| `ywc-confidence-gate` | Borderline CAUTION ↔ DANGER classifications — use the 5-dimension rubric to decide |
