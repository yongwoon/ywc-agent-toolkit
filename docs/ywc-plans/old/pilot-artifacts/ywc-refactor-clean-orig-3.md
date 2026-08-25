# Dispatch artifact: ywc-refactor-clean (original body, run 3)

**Key**: claude-code/skills/ywc-refactor-clean/SKILL.md:45-45
**Scenario**: I need help with the following: removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass on a codebase.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a refusal — a scoped clarifying question mid-narrative. Before doing any detection or deletion work, the procedure requires confirming (a) the target --scope path if the request applies to a specific subdirectory rather than the whole repo, (b) the --tier to stop at (default: safe), and critically (c) that the cleanup will run on a dedicated branch rather than the currently checked-out branch — per the skill's explicit rule that cleanup must never be bundled with active feature-branch work. Since the working tree in this scenario is on a feature branch, I would ask the user to confirm cutting a new chore/dead-code-cleanup branch (or name one) before running Step 1 detection, rather than assuming it is safe to proceed on the current branch.

## Actions
- Read claude-code/skills/ywc-refactor-clean/SKILL.md (already done per task instructions)
- Announce: "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."
- Run: git branch --show-current && git status (gate check: confirm not mixing cleanup into an active feature branch)
- Ask clarifying question if current branch is a feature branch: request confirmation to cut a new branch e.g. chore/dead-code-cleanup off main/HEAD, and confirm --scope / --tier defaults
- Run: git checkout -b chore/dead-code-cleanup (or user-specified branch name) off the base branch
- Run (ecosystem probe, in parallel): ls package.json requirements.txt go.mod Cargo.toml pyproject.toml to pick the Step 1 detection tool matrix row
- Run in parallel: npx knip / npx depcheck / npx ts-prune (JS/TS) OR vulture src/ (Python) OR deadcode ./... (Go) OR cargo +nightly udeps (Rust) OR the grep-based fallback in references/detection-tools.md for an unsupported ecosystem
- Read references/safety-tiers.md to classify every finding into SAFE / CAUTION / DANGER (escalate on any pattern match ambiguity)
- For each SAFE item: dispatch Task(subagent_type: ywc-refactor-cleaner) when the named-agent catalog is installed, else run the 5-substep loop inline: (1) run the domain test suite pre-deletion, (2) git grep -nE '<symbol>' as the second witness, (3) Edit tool surgical delete, (4) re-run the same test suite, (5) git commit -m 'chore(cleanup): remove unused <symbol> (<tool>)' — one deletion per commit, never batched
- On any post-deletion test failure: git revert <commit> (never git checkout -- for multi-file deletions) and re-classify the item to CAUTION
- For each CAUTION item (only if --tier safe+caution or all): run the 3 checks — dynamic-import grep, string-reference grep, and package.json exports/main/module/bin check — before allowing it into the Step 3 loop; any hit escalates to DANGER
- For each DANGER item: do not delete; add a report entry only (public exports, config/entry files, anything touched by git log in the last 7 days)
- Skip Step 6 (duplicate consolidation) unless --tier all was explicitly requested, since it is opt-in and out of default scope
- Run final verification commands (e.g., npm test / pytest / go test, plus build and lint) and record exit codes in the ywc-verify-done command → exit code → claim format
- Emit the Dead Code Cleanup Report (Output Format block) summarizing scope, tier reached, detection tools + versions, deleted/skipped/DANGER counts, and the verification block
- Hand off to ywc-verify-done for the final completion claim, then hand the cleanup branch to ywc-create-pr as its own PR (never bundled with feature-branch commits)

## Files touched
- claude-code/skills/ywc-refactor-clean/SKILL.md (read only, per task instructions)
- claude-code/skills/ywc-refactor-clean/references/detection-tools.md (would read, per Step 1 pointer)
- claude-code/skills/ywc-refactor-clean/references/safety-tiers.md (would read, per Step 2 pointer)
- claude-code/skills/ywc-verify-done/SKILL.md (would read, per Step 7 pointer)
- package.json / requirements.txt / go.mod / Cargo.toml / pyproject.toml (would inspect to select the ecosystem-appropriate detection tool)
- Individual dead-code source files identified by the detection tools (would Edit/delete, one file or symbol per commit)

## Gates enforced
- Iron Law: no deletion without (1) detection tool confirms + (2) grep confirms no references + (3) tests pass after each batch
- Active-feature-branch guard: cleanup must run on its own branch, never mixed with an in-progress feature diff (Rationalization Defense row 8)
- Per-item, per-commit bisectability: exactly one deletion per commit, never batched
- Tier escalation on ambiguity: any grep hit or dynamic-reference pattern moves a SAFE item to CAUTION or a CAUTION item to DANGER rather than proceeding with deletion
- DANGER items are never deleted within this skill's scope — reported only
- Behavior-changing consolidation (Step 6) is opt-in via --tier all and reroutes to ywc-tdd-ritual + ywc-code-gen if it requires semantic reconciliation
- git revert (not git checkout --) is the mandated rollback for any multi-file deletion commit
- Detection tools run exactly once at Step 1 — no mid-loop re-running to avoid stale/false-positive re-flags
- Mandatory ywc-verify-done handoff with PASS/FAIL wording (no hedged language) unless an upstream caller explicitly passes --skip-verify-done

## Full narrative

Here is exactly how I would carry out this request under the ywc-refactor-clean discipline.

First, I would announce the skill per its required opening line: "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."

**Step 0 — branch gate.** Before touching anything, I would run `git branch --show-current` and `git status`. This skill's own rule (and Rationalization Defense row 8) is explicit that cleanup must never be run on an active feature branch, because a mixed diff makes it impossible for a reviewer to tell "this delete was safe" from "this delete broke the new feature." If the current branch looks like in-progress feature work, I would stop and ask the user to confirm a dedicated branch name (e.g. `chore/dead-code-cleanup`) cut from the base branch, then run `git checkout -b chore/dead-code-cleanup <base>`. I would also confirm the intended `--scope` (whole repo vs. a subdirectory) and `--tier` (defaulting to `safe` if unspecified) before proceeding, since those two flags change the entire blast radius of the pass.

**Step 1 — Detect.** I would first identify the ecosystem by checking for `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pyproject.toml`, etc., then run the matching detection tools in parallel per the canonical matrix: `npx knip`, `npx depcheck`, `npx ts-prune` for JS/TS; `vulture src/` for Python; `deadcode ./...` for Go; `cargo +nightly udeps` for Rust. For any ecosystem not in the matrix, I would use the grep-based fallback documented in `references/detection-tools.md` rather than inventing a new tool. I would run this exactly once — the skill explicitly forbids re-running detection tools mid-loop because cached module graphs produce stale, false-positive re-flags.

**Step 2 — Classify.** I would read `references/safety-tiers.md` and sort every finding into exactly one of SAFE / CAUTION / DANGER, escalating anything matching multiple tiers to the highest one. SAFE = internal helpers, test fixtures, unexported symbols. CAUTION = components, route handlers, middleware, or anything with `import()`/`require()` patterns matching its name. DANGER = public package exports (checked against `package.json`'s `exports`/`main`/`module`/`bin`), config files, entry points, or anything touched by `git log` in the last 7 days.

**Step 3 — SAFE deletion loop.** For each SAFE item, if the named-agent catalog is installed I would dispatch `Task(subagent_type: ywc-refactor-cleaner)` with the worklist; otherwise I'd run the same 5 substeps inline: (1) run the test suite scoped to that item's domain to establish a pre-deletion green baseline, (2) `git grep -nE '<symbol>'` as the second independent witness — any hit reclassifies the item to CAUTION and skips deletion, (3) delete the item surgically with the `Edit` tool (no adjacent reformatting), (4) re-run the same test suite, and (5) if green, commit as `chore(cleanup): remove unused <symbol> (<tool-name>)` — one deletion per commit, never batched, so `git bisect` can land on the exact regression later. If a post-deletion run goes red, I would `git revert <commit>` (never `git checkout --`, since that only reverts a single file and leaves multi-file deletions half-applied) and re-classify the item to CAUTION.

**Step 4 — CAUTION verification.** Only if `--tier` is `safe+caution` or `all` would I touch CAUTION items, and only after all three checks pass: a dynamic-import grep, a string-reference grep (route names, plugin slugs, config keys, docs), and a public-API check against `package.json`'s `exports`/`main`/`module`/`bin` fields. Any hit escalates the item to DANGER instead of deleting it.

**Step 5 — DANGER.** These are never deleted in this skill's scope — each gets a report entry only (e.g. public package exports, plugin auto-discovery targets, files touched in the last 7 days).

**Step 6 — Consolidation.** This is opt-in via `--tier all` only, and I would default-skip it unless explicitly requested. For any near-duplicate pair I would pick the canonical implementation (best-tested, fewest call sites to rewrite), update call sites, and run the full suite — but if reconciling the two implementations requires any behavior change (differing edge-case handling, error shapes, signatures), I would stop and route that specific pair to `ywc-tdd-ritual` + `ywc-code-gen` instead of merging it here, since this skill is byte-for-byte-equivalence-only.

**Step 7 — Verify-done handoff.** I would run the full verification suite (tests, build, lint) and record each as `command → exit code → PASS/FAIL` — never hedged language like "should pass." I would then emit the Dead Code Cleanup Report (scope, tier reached, detection tools + versions, counts of deleted/reclassified/DANGER items, and the verification block with bundle-size and line-count deltas), hand off to `ywc-verify-done` for the completion claim (unless an upstream caller already owns that with `--skip-verify-done`), and finally route the cleanup branch to `ywc-create-pr` as its own standalone PR — never bundled with feature-branch commits.

Throughout, I would apply the Validation Checklist before declaring anything complete: at least one detection tool's output captured in the report, one commit per deleted item, every tier reclassification logged, tests green after each tier transition (not just at the end), zero behavior-changing commits in the series, zero unreconciled-semantics consolidations, and the final verify-done block using PASS/FAIL wording only.

The one place I would stop and ask rather than proceed is the branch gate at Step 0 — if the working tree is currently on active feature work, I would not layer cleanup commits on top of it; I'd ask the user to confirm a dedicated cleanup branch name first, since that is a hard boundary in the skill's own Iron Law and Rationalization Defense table, not a judgment call I'd make unilaterally.</narrative>

