# Dispatch artifact: ywc-refactor-clean (deleted body, run 3)

**Key**: claude-code/skills/ywc-refactor-clean/SKILL.md:45-45
**Scenario**: I need help with the following: removing dead code (unused functions / exports / files / dependencies / imports), consolidating near-duplicate utilities, or running a scheduled hygiene pass on a codebase.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a refusal of the task itself — the request matches the skill's intended scope exactly (dead code removal, near-duplicate consolidation, scheduled hygiene pass). However, before executing I would surface two checkpoints to the user rather than silently deciding: (1) confirm branch strategy — since the working branch is currently the active feature branch feature/skill-hell-base, cleanup must happen on a fresh branch off main per the skill's 'never mix cleanup with feature diff' rule, and (2) confirm intended --tier, since the user's phrasing mentions 'consolidating near-duplicate utilities,' which only runs under the opt-in --tier all and needs an explicit go-ahead before I touch call sites across files. Absent those confirmations I would default to the safest options (new branch off main, --tier safe) and state that choice explicitly rather than blocking entirely.

## Actions
- Announce skill use: "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."
- Run `git status` / `git branch --show-current` (Bash) to confirm current branch state
- Since current branch is feature/skill-hell-base (an active feature branch), run `git checkout main && git pull && git checkout -b chore/dead-code-cleanup-<date>` (Bash) rather than cleaning up in place
- Run `ls -la` at repo root and check for package.json / go.mod / requirements.txt / Cargo.toml (Bash/Read) to determine ecosystem
- Read scripts/install.sh and scripts/validate.sh to understand discovery mechanism (glob vs explicit list) before classifying skill directories
- Run `bash scripts/validate.sh` (Bash) as the pre-deletion green baseline
- Run `shellcheck scripts/*.sh` and any equivalent for codex/skills/scripts/*.sh (Bash) as the grep-based fallback detection tool for this non-JS/Python/Go/Rust repo
- Run `git grep -nE '<symbol>'` per candidate item as the second witness (Bash)
- Classify each finding into SAFE / CAUTION / DANGER per references/safety-tiers.md rules (no tool call, judgment step)
- Dispatch Task(subagent_type: ywc-refactor-cleaner) with the SAFE worklist since claude-code/agents/ywc-refactor-cleaner.md is installed in this repo
- For each SAFE item: run scoped test/validate command, git grep confirm, Edit tool surgical deletion, re-run validate, `git add`/`git commit -m "chore(cleanup): remove unused <symbol> (<tool>)"` (one deletion per commit)
- For each CAUTION item: run the three-check battery (dynamic import grep, string-reference grep, public-API/manifest check) via Bash `git grep` before allowing deletion
- For each DANGER item (scripts/install.sh, .github/workflows/*.yml, any SKILL.md): log in report only, do not delete
- Ask user a clarifying question on --tier before running Step 6 consolidation, since the request mentions 'consolidating near-duplicate utilities' but --tier all is opt-in and not explicitly requested
- If consolidation needed, run full `bash scripts/validate.sh` after updating call sites before deleting the duplicate; if any behavior reconciliation is needed, stop and hand off to ywc-tdd-ritual + ywc-code-gen instead
- Compose the Dead Code Cleanup Report in the canonical Output Format and hand off to ywc-verify-done
- Hand off to ywc-create-pr via `gh pr create` quoting the verification report, as its own standalone cleanup PR

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-refactor-clean-45-45.md (read only, procedure source)
- scripts/install.sh (read, to understand skill discovery/manifest mechanism before classifying skill dirs as SAFE/CAUTION)
- scripts/validate.sh (read + run, as the scoped verification command)
- scripts/install-git-hooks.sh (candidate for near-duplicate/dead-code inspection)
- codex/skills/scripts/* (candidate SAFE-tier targets: shared helper scripts possibly unreferenced by any SKILL.md)
- claude-code/agents/ywc-refactor-cleaner.md (read, to confirm subagent persona before Task dispatch)
- references/safety-tiers.md and references/detection-tools.md (referenced for classification and fallback-tool guidance, not modified)
- Any concrete SAFE-classified file/function found during detection (deleted one per commit via Edit tool)
- .github/workflows/*.yml (read only, DANGER-tier, never deleted by this skill)

## Gates enforced
- Two-witness rule: detection tool (shellcheck/grep-fallback) + git grep confirmation required before every SAFE deletion
- Third witness: scoped test/validate suite must be green before AND after each deletion, per item
- One deletion per commit (bisectability requirement) — no batched delete commits
- SAFE -> CAUTION -> DANGER escalation on any grep hit, dynamic-import hit, or public-API/manifest match
- Cleanup must run on its own branch, never mixed with active feature-branch work (branch switch enforced before Step 1)
- Consolidation (Step 6) gated behind explicit --tier all opt-in; behavior-changing consolidations routed out to ywc-tdd-ritual + ywc-code-gen rather than merged into this pass
- DANGER items (entry points, CI workflows, public SKILL.md surface) reported but never deleted by this skill
- Mandatory ywc-verify-done handoff with PASS/FAIL wording (no 'should pass' claims) before declaring the cleanup complete
- ywc-refactor-cleaner subagent invoked only inside this skill's classification phase, never standalone

## Full narrative

Understood. This falls squarely within the ywc-refactor-clean discipline, so I would run it end to end as follows.

I would open by announcing: "I'm using the ywc-refactor-clean skill to remove dead code under a SAFE/CAUTION/DANGER tier with per-batch verification."

**Branch setup.** I would first check `git status` / `git branch --show-current`. Since the active branch is a feature branch, I would not clean up there — mixing a 30-commit deletion series into a feature diff makes review impossible and is explicitly forbidden by the skill's Rationalization Defense table. I would run `git checkout main && git pull && git checkout -b chore/dead-code-cleanup-<date>` and note this choice to you rather than deciding silently.

**Step 1 — Detect.** I would check the repo root for `package.json`, `go.mod`, `requirements.txt`, `Cargo.toml` to pick the right detection tool per the skill's ecosystem matrix. This repository is a skill/agent distribution toolkit built on Markdown + Bash (`scripts/install.sh`, `scripts/validate.sh`, `scripts/install-git-hooks.sh`), not a JS/Python/Go/Rust application, so none of `knip`/`depcheck`/`ts-prune`/`vulture`/`deadcode`/`cargo-udeps` apply. I would fall back to the "Universal fallback: grep" path described in `references/detection-tools.md`, supplemented by `shellcheck scripts/*.sh` (and any scripts under `codex/skills/scripts/`) since shellcheck flags unreachable/unused code (e.g., SC2317) as a proxy detector for this ecosystem. I would run these in parallel.

**Step 2 — Classify.** Candidates for SAFE would be things like an internal bash helper function inside `scripts/install.sh` with zero call sites anywhere in the repo, or a leftover script under `codex/skills/scripts/` that no `SKILL.md` sources and no other script calls. Before classifying any skill directory, I would read `scripts/install.sh` to determine whether it discovers skills by explicit list or by glob — if it globs `claude-code/skills/*/`, then "not named anywhere else" does not mean unused, since the loop itself is the reference; that changes the tier from SAFE to CAUTION or excludes it entirely. Entry points (`scripts/install.sh` itself), CI workflow files under `.github/workflows/`, and any `SKILL.md` (the actual distributed product surface) would be classified DANGER by definition and never deleted by this pass.

**Step 3 — SAFE deletion loop.** Since `claude-code/agents/ywc-refactor-cleaner.md` is present in this repo, I would dispatch `Task(subagent_type: ywc-refactor-cleaner)` with the SAFE worklist so the dedicated worker persona runs the loop, rather than running it inline myself. For each SAFE item the worker (or I, if the runtime lacked named-agent dispatch) would: run `bash scripts/validate.sh` as the pre-deletion green baseline; run `git grep -nE '<symbol>'` as the second witness; use the `Edit` tool for a surgical, single-item deletion with no adjacent reformatting; re-run `bash scripts/validate.sh`; and on green, `git add <file> && git commit -m "chore(cleanup): remove unused <symbol> (shellcheck)"` — one deletion per commit, never batched, so a future `git bisect` lands on the exact deletion. Any red re-run triggers `git revert <commit>` (never a fix-forward commit) and re-classification to CAUTION.

**Step 4 — CAUTION verification.** For anything reclassified up (e.g., a reference doc under `references/` that no `SKILL.md`'s References table links to, but that might still be read directly by a human or another tool), I would run the three-check battery before touching it: a dynamic-reference grep (`git grep -nE "(source|require)\\(.*<symbol>.*\\)"` adapted for bash `source` calls), a bare string-reference grep (`git grep -nE "[\"'\`]<symbol>[\"'\`]"` to catch mentions in READMEs, CI matrices, or install.sh's manifest), and a "public surface" check — in this repo's case, confirming the item isn't part of what `scripts/install.sh --list` exposes to end users. Any hit escalates to DANGER instead of proceeding to deletion.

**Step 5 — DANGER.** These get a report line only — no deletion. In this repo that would include `scripts/install.sh`, `.github/workflows/*.yml`, and any `SKILL.md`.

**Step 6 — Consolidation (opt-in).** Your request explicitly mentions "consolidating near-duplicate utilities," which only runs under `--tier all`. Before touching call sites across files, I would ask you to confirm you actually want that tier engaged (versus a conservative `--tier safe` pass), since consolidation is the riskiest step — for example, if `scripts/install.sh` and `scripts/install-git-hooks.sh` turned out to share near-identical argument-parsing or path-resolution logic, I would pick the better-tested implementation as canonical, repoint call sites, and only delete the duplicate after a full `bash scripts/validate.sh` run stayed green. If the two implementations differed in any edge-case handling (which is common with hand-rolled bash argument parsing), I would stop the consolidation entirely and hand that specific change off to `ywc-tdd-ritual` + `ywc-code-gen` in a separate branch/PR, since reconciling behavior is out of scope for a pure cleanup pass.

**Step 7 — Verify-done handoff.** I would close the series with the canonical Dead Code Cleanup Report (scope, tier reached, detection tools used, per-tier deletion counts, reclassifications, DANGER items left in place, and a verification block in the mandatory `command → exit code → PASS/FAIL` shape, e.g. `$ bash scripts/validate.sh` / `exit 0 (PASS)`), then hand that report to `ywc-verify-done` as the mandatory final claim — no "should pass" language permitted.

**Final delivery.** With the report in hand, I would hand off to `ywc-create-pr` (`gh pr create`) to open the cleanup branch as its own standalone PR quoting that report, keeping it entirely separate from any feature work — never bundled with `ywc-code-gen` changes in the same branch, per the skill's explicit pairing restriction.

I would not refuse this request — it is exactly the class of work this skill exists for. The two things I would flag to you up front rather than deciding unilaterally are: (1) that I'm moving cleanup off the current feature branch onto a fresh branch from main, and (2) whether you want the opt-in consolidation tier (`--tier all`) engaged given you mentioned near-duplicate utilities, or whether a conservative `--tier safe` first pass is preferred with consolidation as a deliberate follow-up.
