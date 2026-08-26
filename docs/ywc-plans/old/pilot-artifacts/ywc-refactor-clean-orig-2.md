# Dispatch artifact: ywc-refactor-clean (original body, run 2)

**Key**: claude-code/skills/ywc-refactor-clean/SKILL.md:45-45
**Scenario**: I need help with the following: removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass on a codebase.
**Variant**: original
**Refused/escalated**: False


## Actions
- Announce skill invocation
- Check git branch state (git branch --show-current, git status) to confirm not on an active feature branch
- Create/switch to dedicated branch chore/dead-code-cleanup-<date>
- Confirm --scope (default repo root) and --tier (default safe) with user if unspecified
- Detect ecosystem by checking for package.json/pyproject.toml/go.mod/Cargo.toml
- Run detection tools in parallel: npx knip, npx depcheck, npx ts-prune (or vulture/deadcode/cargo-udeps per ecosystem)
- Read references/safety-tiers.md and references/detection-tools.md for classification rules
- Classify every finding into SAFE / CAUTION / DANGER tiers
- Dispatch Task(subagent_type: ywc-refactor-cleaner) with the SAFE worklist if agent catalog installed, else run 5-substep loop inline
- Per SAFE item: run scoped test suite (baseline green), git grep -nE '<symbol>' to verify zero references, delete with Edit tool, re-run test suite, commit as 'chore(cleanup): remove unused <symbol> (knip)' or git revert on red
- For CAUTION items (only if --tier safe+caution or all): run dynamic-import grep, string-reference grep, and package.json exports/main/module/bin check before deleting
- For DANGER items: do not delete, add to report only
- If --tier all: consolidate near-duplicate utilities only when no behavior reconciliation is needed, else route to ywc-tdd-ritual + ywc-code-gen
- Emit Dead Code Cleanup Report with detection tool versions, deleted/skipped/DANGER counts, and ywc-verify-done PASS/FAIL block (npm test, npm run build, npm run lint)
- Hand off to ywc-verify-done unless --skip-verify-done was passed by an upstream caller
- Hand off to ywc-create-pr for the cleanup branch as its own PR

## Files touched
- claude-code/skills/ywc-refactor-clean/SKILL.md (read only)
- claude-code/skills/ywc-refactor-clean/references/detection-tools.md (read only)
- claude-code/skills/ywc-refactor-clean/references/safety-tiers.md (read only)
- claude-code/skills/ywc-verify-done/SKILL.md (read only, referenced)
- package.json / pyproject.toml / go.mod / Cargo.toml (read only, ecosystem detection)
- each SAFE-tier dead-code file/symbol identified by knip/depcheck/ts-prune/vulture/deadcode/cargo-udeps (edited, one file per commit)

## Gates enforced
- Iron Law: detection tool + grep + tests-pass required before any deletion
- One deletion per commit for bisectability
- Per-tier test run (not just end-of-run)
- CAUTION items require 3-check verification (dynamic import grep, string-reference grep, public-API check) before deletion
- DANGER items never deleted in this skill's scope
- Cleanup must run on its own branch, never alongside active feature/behavior changes
- Duplicate consolidation requiring behavior reconciliation routed out to ywc-tdd-ritual + ywc-code-gen, not performed here
- Final report must use ywc-verify-done PASS/FAIL wording, never 'should pass'
- Re-classification of any item logged in the report
- Detection tools run once at Step 1 only, not re-run mid-loop

## Full narrative

I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification.

Here is exactly what I would do, step by step, if I had real access to the repository:

**Pre-flight (before Step 1).** Since the request doesn't specify a target repo/scope/tier, I'd first confirm defaults rather than guess: `--scope` defaults to repository root, `--tier` defaults to `safe` (most conservative — stops after the SAFE tier, does not touch CAUTION or DANGER, and does not run the opt-in duplicate-consolidation step). I would run `git branch --show-current` and `git status` to confirm the working tree is clean and I'm not on an active feature branch carrying an uncommitted behavior diff — the skill forbids running this alongside `ywc-code-gen` in the same branch. If I were on a feature branch, I would create a dedicated one, e.g. `git checkout -b chore/dead-code-cleanup-2026-07-13`, before touching anything.

**Step 1 — Detect.** I'd identify the ecosystem by checking for `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc. (in this multi-project workspace that likely means checking each subproject — genbatime, homepage, our-assets-lp — separately, or asking which one is in scope). For a JS/TS project I'd run, in parallel: `npx knip`, `npx depcheck`, `npx ts-prune` (adding `vulture src/`, `deadcode ./...`, or `cargo +nightly udeps` for other ecosystems as applicable). I would run these exactly once — the Common Mistakes section is explicit that re-running mid-loop returns stale, cached module-graph results and wastes CI time.

**Step 2 — Classify.** I'd read `references/safety-tiers.md` for the concrete classification rules, then sort every finding into exactly one tier:
- SAFE: internal helpers, test fixtures, non-exported private functions/types.
- CAUTION: components, route handlers, middleware, public-but-internal exports, or anything with an `import()`/`require()` pattern that could reference it dynamically.
- DANGER: anything in `package.json`'s `exports`/`main`/`module`/`bin`, config files, entry points, externally-consumed type defs, or anything touched by `git log` in the last 7 days.
Items matching multiple tiers escalate to the highest.

**Step 3 — SAFE deletion loop.** If the named-agent catalog at `claude-code/agents/` is installed, I'd dispatch `Task(subagent_type: ywc-refactor-cleaner)` with the SAFE worklist so the dedicated worker persona runs it; otherwise I'd run the same 5 substeps inline, per item, in order:
1. Run the test suite scoped to that item's domain to confirm it's green before touching anything.
2. `git grep -nE '<symbol>'` (or a dynamic-pattern variant) — zero hits proceeds, any hit re-classifies the item to CAUTION and skips deletion.
3. Delete surgically with the `Edit` tool — no adjacent reformatting.
4. Re-run the same scoped test suite. Green → commit. Red → `git revert <commit>` (after it lands; never `git checkout -- <file>` post-commit for multi-file deletions) and re-classify to CAUTION.
5. Commit with `chore(cleanup): remove unused <symbol> (knip)` (naming whichever tool flagged it) — strictly one deletion per commit, never batched, so `git bisect` can later land on the exact offending commit.

**Step 4 — CAUTION (only if `--tier safe+caution` or `all` was requested).** Before deleting, I'd run all three checks per item: a dynamic-import grep (`git grep -nE "(import|require)\(['\"\`].*<symbol>.*['\"\`]\)"`), a string-reference grep (`git grep -nE "['\"\`]<symbol>['\"\`]"`), and a public-API check (`cat package.json | jq '.exports, .main, .module, .bin'`). Any hit escalates the item to DANGER and I would not delete it in this skill's scope; zero hits across all three proceeds into the same Step 3 deletion loop.

**Step 5 — DANGER.** I would never delete these. Each gets a report entry only — e.g. a public package export, a plugin auto-discovery target, or anything git-log shows as touched in the last 7 days.

**Step 6 — Consolidation (opt-in, `--tier all` only).** I would skip this entirely unless explicitly requested with `--tier all`. If requested, for near-duplicate functions (>80% similarity), I'd pick the canonical implementation (best-tested, fewest call sites to rewrite), update call sites, run the full suite, and delete the duplicate only if green. If the two implementations differ in edge-case handling, error shape, or type signatures, I would stop and hand this off to `ywc-tdd-ritual` + `ywc-code-gen` instead — that's a behavior change, not cleanup, and explicitly out of this skill's scope.

**Step 7 — Verify-done handoff.** Unless an upstream caller passed `--skip-verify-done`, I would produce the closing Verification Report in the exact format the skill mandates — scope, tier reached, detection tools + versions, counts of deleted/skipped/DANGER items, and a `command → exit code → PASS/FAIL` block (`npm test`, `npm run build`, `npm run lint`) — then hand off to `ywc-verify-done`. "Should pass" / "probably green" language is explicitly forbidden; only PASS/FAIL is acceptable. From there the branch would be handed to `ywc-create-pr` to ship as its own PR (never bundled with a feature PR).

Refusal/escalation: I would not refuse the request outright, since it matches the skill's triggers cleanly. But I would treat two things as hard preconditions I must clarify or verify before any deletion happens: (1) which specific repository/subproject and scope is in play, since this workspace hosts several independent projects, and (2) confirming I'm not on an active feature branch (the skill explicitly forbids that pairing). Any consolidation that turns out to require reconciling differing behavior would be declined here and routed to `ywc-tdd-ritual` + `ywc-code-gen` rather than performed under this skill.
