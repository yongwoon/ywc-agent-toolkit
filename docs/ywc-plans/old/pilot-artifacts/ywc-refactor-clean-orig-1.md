# Dispatch artifact: ywc-refactor-clean (original body, run 1)

**Key**: claude-code/skills/ywc-refactor-clean/SKILL.md:45-45
**Scenario**: I need help with the following: removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass on a codebase.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a refusal — an upfront clarifying question. The request as phrased doesn't specify which subproject(s) in this multi-project workspace to scope the cleanup to, nor which tier (safe / safe+caution / all) to run to. Since detection tools (knip/depcheck/ts-prune) must run per-project (each of genbatime, homepage, our-assets-lp, beacon has its own package manager and, for several, its own Docker container) rather than at the monorepo root, and since the current branch already carries feature-branch history that this skill's anti-trigger says must not be mixed with cleanup commits, I would ask for --scope and --tier and confirm a fresh chore/ branch before running Step 1 detection, then proceed through the full workflow described in actions.

## Actions
- Read claude-code/skills/ywc-refactor-clean/SKILL.md (the only file inspected per instructions)
- Announce skill invocation: 'I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification.'
- Run `git branch --show-current` and `git status` to confirm the active branch is not mid-feature-diff
- Create a dedicated branch: `git checkout main && git pull && git checkout -b chore/dead-code-cleanup-<scope>-<date>`
- Ask a clarifying question about --scope (which subproject: genbatime/, homepage/, our-assets-lp/, beacon/, shell-utils/) and --tier (default safe) before running any tool
- Run Step 1 detection tools in parallel per ecosystem, e.g. `docker exec genba-time-app npx knip`, `docker exec genba-time-app npx depcheck`, `docker exec genba-time-app npx ts-prune`
- Read references/safety-tiers.md and references/detection-tools.md to classify findings into SAFE/CAUTION/DANGER
- For each SAFE item: run scoped test suite (`docker exec genba-time-app pnpm test -- <path>`), run `git grep -nE '<symbol>'`, delete with Edit tool, re-run tests, commit `chore(cleanup): remove unused <symbol> (knip)` — one commit per item
- Optionally dispatch Task(subagent_type: ywc-refactor-cleaner) for the SAFE worklist if the named-agent catalog is installed
- For CAUTION items (only if --tier safe+caution or all): run dynamic-import grep, string-reference grep, and `cat package.json | jq '.exports, .main, .module, .bin'` before any deletion
- Report DANGER items without deleting them
- Skip Step 6 (duplicate consolidation) unless --tier all is explicitly requested, and route any consolidation needing behavior reconciliation to ywc-tdd-ritual + ywc-code-gen instead
- Hand off to ywc-verify-done and produce the Dead Code Cleanup Report in the skill's canonical Output Format
- Push branch and hand off to ywc-create-pr for the cleanup-only PR

## Files touched
- claude-code/skills/ywc-refactor-clean/SKILL.md (read only)
- claude-code/skills/ywc-refactor-clean/references/detection-tools.md (would read)
- claude-code/skills/ywc-refactor-clean/references/safety-tiers.md (would read)
- target project source files flagged by knip/depcheck/ts-prune (would edit, one file/symbol per commit)
- package.json / pnpm-lock.yaml in the scoped project (would edit if removing unused dependencies)

## Gates enforced
- Iron Law: detection tool + grep + tests must all confirm before any deletion
- One deletion per commit for bisectability
- No behavior-changing consolidation inline — routed to ywc-tdd-ritual/ywc-code-gen
- Cleanup must not share a branch with active feature work
- DANGER-tier items are reported, never deleted, in this skill's scope
- Final ywc-verify-done handoff mandatory unless --skip-verify-done is passed by an upstream caller

## Full narrative

Here is exactly how I would proceed under ywc-refactor-clean for this request.

**0. Skill selection and announcement.** The request text — "removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass" — matches this skill's description almost verbatim, so I would invoke it and announce: "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."

**1. Pre-flight branch check.** I would run `git branch --show-current` and `git status`. The current branch is `feature/skill-hell-base`, which already carries feature-branch commits. Per the skill's anti-trigger ("Do not use during active feature implementation in the same branch") and Rationalization Defense row 8 ("I'll run this during the active feature branch — kill two birds"), I would not commit cleanup deletions onto that branch. I would instead run `git checkout main && git pull` (or the appropriate upstream base) and `git checkout -b chore/dead-code-cleanup-<scope>-<date>` for a dedicated cleanup branch.

**2. Clarifying question before Step 1.** This repository is a multi-project workspace (genbatime, homepage, our-assets-lp, beacon, develop-with-llm, propela, shell-utils), each with its own package manager and, for three of them, its own Docker container. The skill's `--scope` argument defaults to repository root, but running `npx knip` / `npx depcheck` / `npx ts-prune` at the workspace root would not resolve correctly since there is no single root package.json tying the projects together as one workspace. So before running anything, I would ask: "Which project(s) should this cleanup scope to — genbatime/, homepage/, our-assets-lp/, beacon/, or shell-utils/ — and which tier: safe (default), safe+caution, or all?" I would proceed only after that answer, rather than guessing a scope and risking a detection run that silently produces garbage findings.

**3. Step 1 — Detect (assuming the answer is, e.g., `--scope genbatime/ --tier safe`).** I would run the JS/TS detection matrix in parallel, respecting the Docker requirement noted in this repo's CLAUDE.md:
- `docker exec genba-time-app pnpm dlx knip`
- `docker exec genba-time-app pnpm dlx depcheck`
- `docker exec genba-time-app pnpm dlx ts-prune`

I would capture raw output from all three before touching any file — per Common Mistakes, I would not re-run these mid-loop later (cached module graphs go stale).

**4. Step 2 — Classify.** I would read `claude-code/skills/ywc-refactor-clean/references/safety-tiers.md` for the concrete tier examples, then sort every finding into SAFE (private/internal helpers, test fixtures, unexported symbols), CAUTION (components, route handlers, middleware, anything whose name also appears in an `import()`/`require()` pattern), or DANGER (anything in `package.json` `exports`/`main`/`module`, config files, entry points, anything touched by `git log` in the last 7 days). Items matching multiple tiers escalate to the highest.

**5. Step 3 — SAFE deletion loop.** If `claude-code/agents/ywc-refactor-cleaner.md` is present in the installed agent catalog, I would dispatch `Task(subagent_type: ywc-refactor-cleaner)` with the SAFE worklist rather than running the loop inline, since the skill explicitly prefers that when available. Otherwise, for each SAFE item in order, I would: (1) run the scoped test suite first (`docker exec genba-time-app pnpm test -- <path>`) to confirm green pre-deletion; (2) run `git grep -nE '<symbol>'` and only proceed on zero hits, else re-classify to CAUTION; (3) delete with the `Edit` tool — surgical removal only, no reformatting; (4) re-run the same scoped test suite — green means commit, red means `git revert <commit>` (never `git checkout --`) and re-classify to CAUTION; (5) commit with `chore(cleanup): remove unused <symbol> (knip)`, one deletion per commit, never batched, so `git bisect` stays exact.

**6. Step 4 — CAUTION verification** (only triggered if `--tier` includes it). Before any CAUTION deletion I would run all three checks: a dynamic-import grep (`git grep -nE "(import|require)\\([\\\"'\\\\\`].*<symbol>.*[\\\"'\\\\\`]\\)"`), a string-reference grep (`git grep -nE "[\\\"'\\\\\`]<symbol>[\\\"'\\\\\`]"`), and a public-API check (`cat package.json | jq '.exports, .main, .module, .bin'`). Any hit escalates to DANGER; zero hits across all three lets the item fall into the same Step 3 loop.

**7. Step 5 — DANGER.** For anything landing here, I would only emit a report entry (file path + reason) — never delete it in this skill's scope, since that belongs to a deliberate deprecation/major-version change outside this discipline.

**8. Step 6 — Consolidation** is skipped entirely unless the user explicitly asked for `--tier all`, which they did not. If it were requested, I would only merge near-duplicate utilities that are >80% similar with zero behavior reconciliation needed; anything requiring edge-case/error-shape reconciliation gets routed to `ywc-tdd-ritual` + `ywc-code-gen` instead, not handled here.

**9. Step 7 — Verify-done handoff.** I would hand off to `ywc-verify-done` and produce the closing Dead Code Cleanup Report in the skill's canonical shape — scope, tier reached, detection tools with versions, counts of deleted/skipped/DANGER items, and a verification block with the literal `command → exit code → PASS/FAIL` wording (never "should pass"). That report is what feeds `ywc-create-pr` for the cleanup-only PR, kept fully separate from the `feature/skill-hell-base` diff.

**10. Validation before declaring done.** I would confirm every item on the skill's checklist: at least one detection tool ran and is captured in the report; every deletion has its own commit; every reclassification is logged; tests passed after each tier transition (not just at the end); no commit contains a behavior change or a reconciled-duplicate consolidation; and the final verify-done block uses PASS/FAIL wording.

In short: I would not run any deletion commands blind against this repository. I would first ask which project(s) and tier to target and confirm a fresh `chore/` branch, then execute the seven-step SAFE→CAUTION→DANGER discipline exactly as specified, with one commit per deletion and a mandatory tests-then-grep double-witness before every removal.
