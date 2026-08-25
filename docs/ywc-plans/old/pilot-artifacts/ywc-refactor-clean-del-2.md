# Dispatch artifact: ywc-refactor-clean (deleted body, run 2)

**Key**: claude-code/skills/ywc-refactor-clean/SKILL.md:45-45
**Scenario**: I need help with the following: removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass on a codebase.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a full refusal — proceeding with the cleanup — but before executing I would ask a clarifying scoping question, since the request explicitly asks for duplicate-utility consolidation (Step 6), which is opt-in and only runs under --tier all (the skill's default is --tier safe, the most conservative tier). I'd confirm: (1) --scope — whole repo or a specific directory; (2) --tier — safe (default, dead-code-only) vs safe+caution vs all (needed to include consolidation); and (3) whether the current branch is dedicated to this cleanup or whether I need to branch off main first, since the skill forbids bundling this work with an active feature branch/diff. I would also flag upfront that any consolidation requiring behavior reconciliation (differing edge-case handling, error shapes, or signatures between the near-duplicates) is out of scope here and would be handed to ywc-tdd-ritual + ywc-code-gen instead of being merged inline.

## Actions
- Announce skill usage per required announcement string
- Check git state (git status --short, git branch --show-current) to confirm no active feature diff is mixed into the branch
- If on a feature branch: git checkout main && git pull && git checkout -b chore/dead-code-cleanup-YYYYMMDD
- Ask clarifying question on --scope and --tier before proceeding (tier all needed for the consolidation part of the request)
- Detect ecosystem (look for package.json / requirements.txt / go.mod / Cargo.toml)
- Read references/detection-tools.md and references/safety-tiers.md before classification
- Run detection tools in parallel via Bash: npx knip, npx depcheck, npx ts-prune (or vulture/deadcode/cargo-udeps/grep fallback per ecosystem)
- Classify each finding into SAFE / CAUTION / DANGER per Step 2 table, escalating multi-tier matches to the highest tier
- Dispatch Task(subagent_type: ywc-refactor-cleaner) with the SAFE worklist if claude-code/agents/ is installed; otherwise run the loop inline
- For each SAFE item: run scoped test suite (pre-check), git grep -nE '<symbol>' to confirm zero references, Edit tool surgical delete, re-run test suite, commit as chore(cleanup): remove unused <symbol> (tool) or git revert <commit> and reclassify on failure — one deletion per commit
- For each CAUTION item: run dynamic-import grep, string-reference grep, and package.json exports/main/module/bin check via jq; zero hits -> SAFE-style delete loop, any hit -> escalate to DANGER
- For each DANGER item: log a report entry only, no deletion (public exports, config/entry files, anything touched by git log in last 7 days)
- If --tier all confirmed: read ../references/readable-code.md, then for near-duplicate utilities pick canonical implementation, update call sites via Edit, run full test suite, delete duplicate on green or git revert + skip on red; abort consolidation and route to ywc-tdd-ritual + ywc-code-gen if any behavior reconciliation is needed
- Hand off to ywc-verify-done: run full test suite, build, and lint commands and require PASS/exit 0 evidence for each
- Assemble the Dead Code Cleanup Report in the mandated Output Format (scope, tier reached, detection tools, deleted/skipped/DANGER counts, verification block with command -> exit code -> PASS/FAIL)
- Hand cleanup branch + report to ywc-create-pr to open a standalone PR (never bundled with feature work)
- Walk the Validation Checklist before declaring the pass complete

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-refactor-clean-45-45.md (read only, procedure source)
- references/detection-tools.md (read, per-ecosystem tool matrix and grep fallback)
- references/safety-tiers.md (read, tier classification rules)
- ../references/readable-code.md (read, only if --tier all is confirmed, for consolidation judgment)
- ../ywc-verify-done/SKILL.md (read, for the mandatory final verification block shape)
- package.json / requirements.txt / go.mod / Cargo.toml (read, to detect ecosystem and confirm public-API surface for CAUTION/DANGER checks)
- Individual source files containing the flagged unused functions/exports/files (edited one at a time, one per commit)
- package.json or equivalent dependency manifest (edited to drop unused dependencies flagged by depcheck, one per commit)

## Gates enforced
- Iron Law: no deletion without detection-tool confirmation + grep confirmation + tests passing after the batch
- Two-witness rule (tool finding + git grep) before any SAFE deletion
- Three-check CAUTION gate (dynamic-import grep, string-reference grep, public-API/package.json check) before any CAUTION deletion
- DANGER items are reported, never deleted, within this skill's scope
- One deletion per commit for bisectability; no batching
- git revert (not git checkout --) as the rollback mechanism for any multi-file deletion
- No behavior-changing consolidation without routing to ywc-tdd-ritual + ywc-code-gen
- Cleanup must run on its own branch, never mixed with an active feature branch/diff
- Mandatory ywc-verify-done handoff with PASS/FAIL (never 'should pass') wording before claiming completion
- Full Validation Checklist walked before declaring the pass complete

## Full narrative

Before touching anything, I would announce: "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."

**Preconditions.** I would run `git status --short` and `git branch --show-current`. If the current branch carries an in-progress feature diff, I would not layer cleanup on top of it — per the skill's Rationalization Defense, mixing the two makes review impossible (a reviewer can't tell "this delete was safe" from "this delete broke the new feature"). I would instead run `git checkout main && git pull && git checkout -b chore/dead-code-cleanup-<date>` and do the work there.

**Clarifying question first.** Since the user explicitly asked for duplicate-utility consolidation, and that step (Step 6) is opt-in and only runs under `--tier all` (default is `--tier safe`), I would ask: which tier to stop at (`safe` / `safe+caution` / `all`), whether to scope to the whole repo or a specific `--scope <dir>`, and confirm the dedicated-branch assumption above. I would proceed with the narrative below assuming the answer authorizes `--tier all` so the consolidation request is actually served.

**Step 1 — Detect.** I would check for `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml` to determine the ecosystem(s) present, then read `references/detection-tools.md` for the exact invocation/fallback matrix. For a JS/TS surface I'd run, in parallel Bash calls: `npx knip`, `npx depcheck`, `npx ts-prune`. For Python: `vulture src/`. For Go: `deadcode ./...`. For Rust: `cargo +nightly udeps`. For anything unsupported, the grep-based fallback documented in that reference file — never an invented tool.

**Step 2 — Classify.** I would read `references/safety-tiers.md` and sort every finding into exactly one of SAFE (internal helper, test fixture, unexported private function/type alias), CAUTION (component, route handler, middleware, public-but-internal export, or anything with an `import()`/`require()` string match on its name), or DANGER (public package export in `package.json` exports/main/module/bin, config file, entry point, anything touched by `git log` in the last 7 days). Items matching multiple tiers escalate to the highest.

**Step 3 — SAFE deletion loop.** If `claude-code/agents/ywc-refactor-cleaner.md` is installed, I would dispatch `Task(subagent_type: ywc-refactor-cleaner)` with the SAFE worklist so the dedicated persona/boundaries apply; otherwise I'd run the loop inline. For each SAFE item, strictly in order: (1) run the test suite scoped to that item's domain to confirm green pre-deletion; (2) `git grep -nE '<symbol>'` — zero hits required to proceed, any hit reclassifies to CAUTION and skips; (3) delete with the `Edit` tool, surgical only, no adjacent reformatting; (4) re-run the same scoped test suite — green commits, red triggers `git revert <commit>` (never `git checkout --` for multi-file deletions) and reclassification to CAUTION; (5) commit with `chore(cleanup): remove unused <symbol> (<tool>)`, one deletion per commit, never batched — this is what makes `git bisect` viable later.

**Step 4 — CAUTION verification.** Before deleting any CAUTION item I would run all three: dynamic-import search `git grep -nE "(import|require)\([\"'\`].*<symbol>.*[\"'\`]\)"`, string-reference search `git grep -nE "[\"'\`]<symbol>[\"'\`]"`, and a public-API check `cat package.json | jq '.exports, .main, .module, .bin'` (or the language equivalent). Zero hits across all three → run the same Step 3 delete loop. Any hit → escalate to DANGER and do not delete.

**Step 5 — DANGER.** For each DANGER item I would only add a report entry (file path + reason, e.g., "public package export" or "touched in last 7 days") — no deletion. Those belong to a separate intentional change (version bump, deprecation cycle), not this pass.

**Step 6 — Consolidate duplicates (only under `--tier all`).** I would first read `../references/readable-code.md` for the shared readable-code rubric so I don't over-simplify or strip a useful abstraction. For each near-duplicate pair at >80% AST/text similarity: pick the canonical implementation (best-tested, most complete, fewest call-site rewrites — checked via `git log --follow` and a grep for call sites); update each call site to import the canonical version via `Edit`; run the full test suite — green deletes the duplicate, red triggers `git revert` and the consolidation is skipped. If reconciling the two implementations requires touching edge-case behavior, error shape, or type signatures, that is no longer cleanup — I would stop and hand that specific pair to `ywc-tdd-ritual` + `ywc-code-gen` rather than merge it here.

**Step 7 — Verify-done handoff.** I would hand off to `ywc-verify-done` with the cleanup report, running the full (not scoped) test suite, build, and lint commands and requiring literal `PASS`/exit-0 evidence for each — "should pass" or "probably green" wording is explicitly forbidden. I would then assemble the Dead Code Cleanup Report in the exact Output Format specified (scope, tier reached, detection tools with versions, deleted counts per category, reclassifications logged, DANGER items listed, and the command → exit code → PASS/FAIL verification block, plus bundle delta and lines-removed summary).

**Downstream.** The cleanup branch and report would go to `ywc-create-pr` to open a standalone PR — never bundled with feature work — and I'd note `ywc-impl-review` as the expected reviewer pass over the per-commit deletions, especially any CAUTION reclassifications.

**Guardrails I would hold to throughout:** detection tools run once at Step 1 only (re-running mid-loop reports stale module-graph findings); any `--dry-run` finding gets re-confirmed live before deletion since it's a snapshot; SAFE tier is never skipped even if it looks uninteresting, because it's the signal that the test suite actually covers the deletion paths; and no amount of "we need this bundle-size win now" pressure would shortcut the grep step, since that is precisely where CAUTION deletions break production. Before declaring the pass complete I would walk the Validation Checklist item by item: at least one detection tool's output captured, every deletion has its own commit, every reclassification logged, tests green after each tier transition, no commit contains a behavior change, no commit reconciles semantics inline, and the final verify-done block uses PASS/FAIL wording.
