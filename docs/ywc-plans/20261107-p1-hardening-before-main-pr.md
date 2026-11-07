# P1 Hardening Before the `main` PR

> Status: Draft
> Scale: Medium
> Created: 2026-11-07
> Author: Claude Code (ywc-plan)
> Spec Reference: N/A — follow-up roadmap for branch `feature/improvement-20261106` (Completion Reports of phases yk-000007..yk-000010)

## Global Constraints

- "Codex `SKILL.md` frontmatter must keep only `name` and `description`." — `CLAUDE.md` (Repository Structure)
- "Keep SKILL.md under ~500 lines; extract long sections to `references/`." — `CLAUDE.md` (Skill Authoring Rules)
- "Do not reference other skills with `@skill-name` (force-load)" — `CLAUDE.md` (Skill Authoring Rules)
- "`pre-commit` syncs plugins/ywc-agent-toolkit when codex/skills changes"; "`pre-push` blocks stale Codex generated package before push" — `CLAUDE.md` (Repository Structure). The generated `plugins/ywc-agent-toolkit/` copy is never hand-edited.
- "Unrecognized keys are rejected by the validator" (agent frontmatter, optional-key allowlist) — `claude-code/agents/CLAUDE.md:87`. The validator it names (`tools/scripts/validate_ywc_agents.py`) does not exist in this repo, so the allowlist is a documented rule, not an enforced check.
- Commit types: `feat`, `fix`, `docs`, `i18n`, `ci`, `chore` — `CLAUDE.md` (Commit Conventions)
- Code, comments and skill prose in English; documentation for the user in Korean — workspace `CLAUDE.md` (Language Conventions)

## Purpose

The branch `feature/improvement-20261106` (about 130 commits ahead of `main`) hardened Claude Code skills against remote-controlled values, unverified merge heads and unsafe remote branch deletion, but the Codex copies of `ywc-merge-dependabot` and `ywc-finish-branch` did not receive the same guards, so Codex users keep the weaker behaviour. The trigger-coverage exemption added in yk-000010-060 relies on a prose regex over agent descriptions. This spec closes those gaps (P1), records the remaining items as P2 with a decision rationale, and defines when the branch is ready for its PR to `main`, ending the chain of follow-up phases yk-000007..yk-000011.

## Scope

- **T0 (already generated, prerequisite):** `tasks/yk-000011-010-domain-ci-gate-and-dependabot-lows` — `validate.sh` runs `test_score.py`; `check-base-required-checks.sh` exit 3 = unresolved; `wait-dependabot-rebase.sh` mergeable allowlist; `claude-code/skills/CLAUDE.md` row; `local dependabot_out`.
- **T1 (FR-1, FR-2, FR-3):** Codex `ywc-merge-dependabot` merge-safety parity with the Claude Code copy as it stands after T0 — head pin, required-check gate, base confirmation before every `--auto` — expressed inside the Codex lane/chunk design (the Claude Code rebase-wait script is not ported, see FR-2).
- **T2 (FR-4):** Codex `ywc-finish-branch` Remote deletion guard parity with the Claude Code guard (yk-000010-040), including the `tests/fixtures/codex-issue69/**` clauses that pin the guard text.
- **T3 (FR-5):** an explicit `tags: [dispatch-only]` marker for dispatch-only Claude Code agents, replacing `DISPATCH_ONLY_RE` in `score.py`.
- **Release gate (FR-6):** after T0–T3 merge, one whole-run `/ywc-impl-review` pass (chunked, see FR-6), then the release PR `feature/improvement-20261106 → main` (existing draft #214).

## Out of Scope

- **P2-a — enforce prose-only guards with hooks** (`claude-code/hooks/` already ships `block-dangerous-commands.py`, `protect-secrets.py`, `hooks-registry.json`). Deferred: it is a cross-cutting design decision (which guards, false-positive cost, Codex has no equivalent hook surface) that needs its own plan and an architect verdict.
- **P2-b — scan-secrets residual gaps:** combined-diff lines of the ` +x` form (`--cc`) and the content of untracked files with harmless names (`scan-secrets.sh:86` checks names only). Deferred: both pre-date this branch and are Low.
- **P2-c — real prompts for `ywc-mine-review-history`** coverage (pinned gap in `test_score.py`). Deferred: requires real usage data; fabrication is forbidden by the dataset provenance rule.
- Codex agent TOML files (`codex/agents/*.toml`): `score.py` does not evaluate them, so no marker is added there.
- Any change to `claude-code/skills/ywc-merge-dependabot/**` beyond what T0 already owns.
- Porting `wait-dependabot-rebase.sh`, `poll-merge-queue.py`, `detect-dockerfile-from.sh` or `detect-major-bump.py` to Codex. The rebase script posts the comment and polls about 9 minutes in one call. Codex instead persists `rebase_intent` before the comment and polls in chunks against one deadline (`codex/skills/ywc-merge-dependabot/SKILL.md:159-167`, "no live polling helper is provided"). This was the Iteration 1 advisor verdict.
- **P2-d — Codex `ywc-worktrees` `--existing-branch` C2 form** (`codex/skills/ywc-worktrees/SKILL.md:92`, `codex/skills/ywc-worktrees/references/existing-branch.md:13,35` still use `check-ref-format --branch`). Deferred: it is not a remote-deletion path; it is a separate parity item.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `codex/skills/ywc-merge-dependabot/SKILL.md:169-181` 3a Sequential Flow | `gh pr checks {number} --required` then `gh pr merge {number} --merge` — no head pin, no exit-8 branch, no no-required-checks handling | T1 extends: reuse the Claude Code 3a gate block shape (FR-2) |
| `codex/skills/ywc-merge-dependabot/SKILL.md:183-199` 3a conflict path | after the `@dependabot rebase` attempt, falls back to hand-resolving (`gh pr checkout`, `git commit`, `git push`) and ends in an unpinned `gh pr merge {number} --merge` (`:198`) | T1 overrides: manual fallback deleted; rebased head merged only through the FR-2 gate |
| `codex/skills/ywc-merge-dependabot/SKILL.md:92-96` Step 2 table, `:282-308` Final Summary, `:331-343` Output Format | labels `Skipped (Dockerfile)`, `Skipped (Major version upgrade)`, `Failed (CI not passing)`, `Failed (lane stalled)` only; the CI row (`:96`) fails any not-yet-passed PR, pending included | T1 extends: add the FR-2 labels and the pending row (FR-2) |
| `codex/skills/ywc-merge-dependabot/SKILL.md:209-217` 3b Stage 1 | `gh pr merge {number} --auto --merge` with no prior confirmation that the base has a required check | T1 extends: base check + head pin before `--auto` (FR-3) |
| `codex/skills/ywc-merge-dependabot/SKILL.md:219-276` 3b Stage 2 | "When an active PR merges, start the next PR from the same ecosystem lane" (`:221`, `:246-249`) — a second `--auto` start | T1 extends: the FR-3 base check applies to every lane start |
| `codex/skills/ywc-merge-dependabot/SKILL.md:278-280` 3b Stage 3 | final sequential pass handles the `mixed` group only | T1 extends: also handles PRs whose base was not confirmed (FR-3) |
| `codex/skills/ywc-merge-dependabot/SKILL.md:159-167` one polling deadline + persisted state | single 1800 s deadline, atomic state snapshot, `rebase_intent` written before the comment, `rebase_commented` after it, "no live polling helper is provided" | T1 complies: no polling script, no second deadline; the new persisted entries are `ci_wait` and `stage3` (FR-2, FR-3); neither the base-check result nor an `--auto` intent is persisted (Iteration 6) |
| `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` (merge-dependabot check) | requires literal clauses in Codex merge-dependabot `SKILL.md`, e.g. "Persist `deadline`, `active`, `lanes`, `status`, and `rebase_commented`", "Only a successful rebase comment sets `rebase_commented[pr]`"; asserted by `tests/codex_issue69_contract_test.py:35-43`, which `scripts/run-codex-skill-contract-evals.sh:233` runs from `validate.sh` | T1 complies: every pinned clause stays verbatim; new rules go in new sentences |
| `codex/skills/ywc-merge-dependabot/SKILL.md` `<!-- operational-safety:dockerfile-detector:start/end -->` | extracted and executed by `tests/codex_issue69_behavior_test.py:106-122`; that test is **not** run by `validate.sh` (only the contract test is) | T1 complies: the marked block stays byte-identical; the behavior test is run explicitly (AC3) |
| `codex/skills/ywc-merge-dependabot/scripts/` | contains only `group-by-ecosystem.py`, referenced by the older `python3 /path/to/ywc-merge-dependabot/scripts/...` placeholder (`SKILL.md:133`) | T1 extends: add `check-base-required-checks.sh` + a Codex test there; the placeholder line stays as is |
| `codex/skills/references/shared-script-resolution.md` (resolver contract) and `tests/codex_executable_resolution_test.py:20-37,205-217` | "normative for Codex skills that invoke a shipped helper"; callers use `RESOLVER_LAUNCHER="$(bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/select-resolver-launcher.sh" 2>&1)"` then `bash "$RESOLVER_LAUNCHER" "<skill>/scripts/<file>" bash` (e.g. `codex/skills/ywc-finish-branch/SKILL.md:149-150`); the test pins `CALLER_FILES` and exactly 20 `bash "$RESOLVER_LAUNCHER"` uses; `validate.sh` runs it | T1 complies: the gate script is resolved through it (FR-2); T1 adds the skill to `CALLER_FILES` and raises the count by the number of new call sites |
| `claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh` | allowlist + C2 `refs/heads/` + `HEAD` reject; last line `CONFIRMED=<0\|1> BASE=<…>`; exit 3 after T0 | T1 reuse: copied byte-identical after T0 merges (`cmp`, AC1) |
| `claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py` | also tests `detect-dockerfile-from.sh`, `detect-major-bump.py`, `poll-merge-queue.py`, `wait-dependabot-rebase.sh` (`:21-25`); `SequentialCiGateTest` (`:299-310`) extracts the 3a block by the marker `gh pr checks {number} --required 2>&1` and sets `CLAUDE_SKILL_DIR` | T1 reuse: trimmed copy (FR-1) — `StubbedTest`, `CheckBaseRequiredChecksTest`, `SequentialCiGateTest` run against a temporary `CODEX_HOME` |
| `codex/skills/ywc-finish-branch/SKILL.md:309-315` Remote deletion guard | binds repo; `git check-ref-format --branch`; open-PR check at step 2 (`:312`) before ls-remote and merged check; merged check only "If deletion relies on a merge" (`:314`); tip-bound lease delete | T2 overrides: FR-4 order and rules |
| `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json:24`, `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json:93` | require / bind the literal `git check-ref-format --branch "$branch"` in Codex finish-branch `SKILL.md` (contract test, run by `validate.sh`) | T2 extends: owns both fixtures; replaces that clause with the C2 clause (FR-4) |
| `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json` finish-branch cases (`empty-open-pr`, `invalid-branch`, `wrong-base`, `moved-tip`, `matching-merge`) | encode the old order (open query first) and allow `empty-open-pr` deletion with no merged row; read only by `tests/codex_issue69_behavior_test.py:129-138` (`source_clause` must be a `required` clause of the adoption fixture), which `validate.sh` does not run | T2 overrides: traces follow the FR-4 order (FR-4); AC4 runs the behavior test |
| `codex/skills/ywc-finish-branch/README*.md`, `codex/skills/ywc-merge-dependabot/README*.md` | describe the guard and the polling behavior | T1/T2 extend: update the lines that describe changed behavior |
| `claude-code/skills/ywc-finish-branch/SKILL.md:215-225` | the reference guard (yk-000010-040, security re-reviewed twice); open-PR check is step 6, last before the delete (`:222`) | T2 reuse: port rules, keep Codex numbering/style |
| `codex/skills/ywc-finish-branch/evals/evals.json`, `codex/skills/ywc-merge-dependabot/evals/evals.json` | shape-checked only by `scripts/run-codex-skill-contract-evals.sh` (from `validate.sh:139-146`); the content gate is the issue69 fixtures above | T1/T2 comply: `validate.sh` must stay green |
| `.claude/skills/ywc-toolkit-eval/scripts/score.py:362-386` | `apply_coverage_exemption`: slash-only via `disable-model-invocation`; dispatch-only via `DISPATCH_ONLY_RE` on the description | T3 overrides: dispatch-only from the `tags` value; slash-only unchanged |
| `.claude/skills/ywc-toolkit-eval/scripts/score.py:154-171` `parse_yaml_lite` | top-level `key:` only; a flow list `tags: [dispatch-only]` is read as the string `[dispatch-only]`; a block list (`tags:` + `  - dispatch-only`) as `- dispatch-only` | T3 complies: FR-5 token rule over that string, no YAML library added |
| `claude-code/agents/CLAUDE.md:67-85` optional-key table, `:87` | `tags` (list, lowercase) is listed; "unknown keys rejected" names a validator file that does not exist | T3 reuse: `tags`; T3 documents its meaning there |
| `scripts/validate.sh:520-540` CC agent checks | checks `name:` / `description:` presence and name == filename only | T3: no validator change needed |
| `.claude/skills/ywc-toolkit-eval/scripts/test_score.py:676-689` | `test_dispatch_only_agent_still_needs_collisions`, `test_user_typed_request_owned_elsewhere_marks_dispatch_only` build `fm` from the description only | T3 overrides: rewritten to set `tags` |
| `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` `test_shipped_catalog_has_no_unexplained_gap` | pins the full 8-item exemption map and the single gap `ywc-mine-review-history` | T3 updates the dispatch-only derivation, keeps the same 8-item map |

Complement enumeration for "dispatch-only agents": `score.py --ci` currently exempts exactly `ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`, `ywc-retro-lens` (yk-000010-060 review, `score.py --ci` output). Every other agent in `claude-code/agents/` (10 files) is not exempt and must stay non-exempt; `grep -l '^tags:' claude-code/agents/*.md` → 0 files today.

## Acceptance Criteria

- **AC0** When T0 is merged, `tasks/completed/yk-000011-010-domain-ci-gate-and-dependabot-lows` exists. Baseline: 1 — the task is pending (`tasks/yk-000011-010-...`).
- **AC1** When T1 is done, `codex/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh` exists and is byte-identical to the Claude Code copy (`cmp claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh codex/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh` exits 0), `wait-dependabot-rebase.sh` is not ported (`grep -rq 'wait-dependabot-rebase' codex/skills/ywc-merge-dependabot` exits 1), and the Codex test passes: `python3 codex/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py` exits 0. Baseline: `test -f codex/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh` → 1 (absent); `grep -rq 'wait-dependabot-rebase' codex/skills/ywc-merge-dependabot` → 1; test file → unrunnable — absent.
- **AC2** When T1 is done, every Codex merge command is pinned and the manual conflict path is gone: `grep -q 'match-head-commit' codex/skills/ywc-merge-dependabot/SKILL.md` exits 0; `grep -nE 'gh pr merge (\{number\}|"\$)' codex/skills/ywc-merge-dependabot/SKILL.md | grep -v -- '--match-head-commit' | grep -v -- '--disable-auto'` prints nothing (exit 1) — any indentation, prose `gh pr merge --auto` mentions without a PR operand excluded; `grep -q 'gh pr checkout' codex/skills/ywc-merge-dependabot/SKILL.md` exits 1. The Codex test's `SkillContractTest` (FR-3) passes, and it was seen failing on the pre-change `SKILL.md`. Baseline: 1 / 0 (prints lines 180, 198, 214) / 0; `SkillContractTest` → unrunnable — absent.
- **AC3** When T1 is done, `scripts/validate.sh` runs the Codex merge-dependabot test and counts a failure as an ERROR: `grep -q 'codex/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py' scripts/validate.sh` exits 0, and a deliberately broken assertion made `bash scripts/validate.sh` report that ERROR once (recorded in the task's Implementation Notes, then reverted). After the revert, `bash scripts/validate.sh` exits 0, including the Codex contract evals and `tests/codex_issue69_contract_test.py`. `python3 tests/codex_issue69_behavior_test.py` exits 0 — it is not part of `validate.sh`, so it runs explicitly. `shellcheck codex/skills/ywc-merge-dependabot/scripts/*.sh` exits 0. Baseline: grep → 1; `python3 tests/codex_issue69_contract_test.py` → 0; `python3 tests/codex_issue69_behavior_test.py` → 0 — 15 tests OK (one earlier run in the same session exited 1 and a re-run passed, so treat a single failure as a flake to re-run once, never as a pass); shellcheck → unrunnable — no `.sh` in the Codex `scripts/` yet.
- **AC4** When T2 is done, the Codex guard validates branches by the C2 rule, pins push and host, and runs the open-PR check last: `grep -q 'check-ref-format --branch' codex/skills/ywc-finish-branch/SKILL.md` exits 1; `grep -qF 'check-ref-format "refs/heads/$branch"' codex/skills/ywc-finish-branch/SKILL.md`, `grep -q 'get-url --push' codex/skills/ywc-finish-branch/SKILL.md` and `grep -q 'env -u GH_HOST' codex/skills/ywc-finish-branch/SKILL.md` exit 0; `grep -q 'If deletion relies on a merge' codex/skills/ywc-finish-branch/SKILL.md` exits 1; `python3 -c "t=open('codex/skills/ywc-finish-branch/SKILL.md').read(); assert t.index('--state merged') < t.index('--state open')"` exits 0; `python3 tests/codex_issue69_contract_test.py` exits 0 with the FR-4 fixture clauses, and was seen failing after the fixture update and before the `SKILL.md` edit; `python3 tests/codex_issue69_behavior_test.py` exits 0 (it is the only reader of `expected-traces.json`). Baseline: 0 / 1 / 1 / 1 / 0 / 1 (AssertionError) / 0 / 0.
- **AC5** When T3 is done, exactly the four dispatch-only agents carry `tags: [dispatch-only]` (`grep -l '^tags:.*dispatch-only' claude-code/agents/*.md | wc -l` prints 4), `grep -q DISPATCH_ONLY_RE .claude/skills/ywc-toolkit-eval/scripts/score.py` exits 1, and `score.py --ci` names the same 8 exempt items and 1 gap as before. Baseline: 0 files / exit 0 / 8 exempt + 1 gap.
- **AC6** When T3 is done, tests in `test_score.py` show that: an agent whose description contains "no natural-language triggers" but has no tag is **not** exempt; an agent with the tag but fewer than 2 collisions is insufficient; `[dispatch-only-x]`, `[non-dispatch-only]`, `[Dispatch-Only]`, `[dispatch_only]` and `[language-reviewer] # not dispatch-only` are not exempt; `[dispatch-only, language-reviewer]`, `["dispatch-only"]` and the block-list form are exempt; a block list whose first line is `# dispatch-only (disabled)` is not. Baseline: unrunnable — the tag rule does not exist yet.
- **AC7** When T0–T3 are merged, the whole-run review reports no Critical/High in any chunk, or, after the one FR-6 fix pass, the targeted re-review of the fix commit reports none. The review covers `<run_start_sha>..feature/improvement-20261106`, where `<run_start_sha>` is `git merge-base main feature/improvement-20261106` (`46cafdea…` today), and runs as consecutive `/ywc-impl-review --git-range <a>..<b> --non-interactive` chunks (FR-6). Baseline for the scope: `git diff --shortstat 46cafdea..feature/improvement-20261106` → 225 files, +7028/−848. That is over the `ywc-impl-review` Step 2.5 hard block (200 files / 5,000 lines), so one single-range run is refused. `bash scripts/validate.sh` and `score.py --ci` exit 0 on the branch. The release PR is updated and marked ready. It is #214 (`feature/improvement-20261106 → main`), or the PR FR-6 opens in its place if #214 was closed. `gh pr view <release-pr> --json state,isDraft` reports `OPEN` and `false`. Baseline (#214): `{"state":"OPEN","isDraft":true}`.

## Functional Requirements

### FR-0: Prerequisite task T0 (AC0)
`tasks/yk-000011-010-domain-ci-gate-and-dependabot-lows` is delivered as already generated; this spec does not change its Scope. Its outputs (exit 3, `run_script_test_suites` running `test_score.py`) are inputs to FR-1..FR-3 and FR-5.

### FR-1: Codex merge-dependabot script and test (AC1, AC3)
Copy `check-base-required-checks.sh` from the Claude Code skill (state after T0) into `codex/skills/ywc-merge-dependabot/scripts/`, byte-identical. Do not port `wait-dependabot-rebase.sh` (see Out of Scope). Add a trimmed `codex/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`. From the Claude Code test after T0, keep only the imports, `HERE`, `BASE_CHECK`, `OLD_SHA`, the `base:` arms and the `*)` fallthrough of `GH_STUB`, `StubbedTest`, `CheckBaseRequiredChecksTest` and `SequentialCiGateTest`. Add the new `SkillContractTest` (FR-3). The docstring and constants must not name `wait-dependabot-rebase`, and no Codex file may name it (AC1). `SequentialCiGateTest` extracts the Codex 3a block by the same marker (`gh pr checks {number} --required 2>&1`). It runs the block with `CODEX_HOME` set to a temporary directory that holds copies of `codex/skills/scripts/` and of this skill's `scripts/` under `skills/`, so the real resolver selects the script. `CLAUDE_SKILL_DIR` is never set. The temporary tree holds `skills/scripts/select-resolver-launcher.sh`, `resolve-bundle-executable.sh` and `resolve-bundle-executable.py`, plus `skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh`, as plain copies, not symlinks. Every run sets `YWC_BUNDLE_DEVELOPMENT=""` and `YWC_BUNDLE_SOURCE_ROOT=""`, so a developer shell's source fallback cannot turn the `BLOCKED` case into a pass. The 3a gate stays the first fenced block that contains the marker, because extraction takes the first match. `SkillContractTest` checks that the excluded rebase script is absent through the shape of the text, never through its literal file name. Add `codex/skills/ywc-merge-dependabot/SKILL.md` to `CALLER_FILES` in `tests/codex_executable_resolution_test.py`, and raise both `== 20` counts by the number of new `bash "$RESOLVER_LAUNCHER"` call sites. README files describe the call in prose only and never contain that literal line. The touched `SKILL.md` must stay ≤ 500 lines; if the FR-2/FR-3 text pushes it over, move only the new state rules (`ci_wait`, `stage3` and their resume rules) to `codex/skills/ywc-merge-dependabot/references/lane-state.md`. Link it from `SKILL.md` as `references/lane-state.md`; sibling links inside it use a bare filename. These stay in `SKILL.md`: the fixture-pinned section `SKILL.md:159-167`, the Dockerfile-detector markers, every `gh pr merge` command and every resolver call. `lane-state.md` never contains the literal `bash "$RESOLVER_LAUNCHER"` line. `SkillContractTest` reads `SKILL.md` plus `lane-state.md` when it exists. Wire the test into `scripts/validate.sh` `run_script_test_suites` with the existing pattern (missing file or failure → ERROR, output in a `local` variable, tail on failure). The generated plugin copy is produced by the pre-commit hook.

### FR-2: Codex 3a gate and conflict path (AC2)
Replace the 3a `gh pr checks --required` / `gh pr merge --merge` pair with the Claude Code gate block after T0. The Codex block resolves the script through the shared resolver contract, the same way `codex/skills/ywc-finish-branch/SKILL.md:149-150` does:

```bash
RESOLVER_LAUNCHER="$(bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/select-resolver-launcher.sh" 2>&1)" || { echo "BLOCKED: ${RESOLVER_LAUNCHER#BLOCKED: }" >&2; exit 3; }
BASE_CHECK_SCRIPT="$(bash "$RESOLVER_LAUNCHER" "ywc-merge-dependabot/scripts/check-base-required-checks.sh" bash)" || exit $?
BASE_OUT=$(bash "$BASE_CHECK_SCRIPT" {number}) && BASE_RC=0 || BASE_RC=$?
```

In every block that calls the script, the two resolver lines come directly before the script call, in the same fenced block; in 3a that is inside the "no required checks reported" branch. The `case` reads `${BASE_OUT##*$'\n'}` as in the Claude Code block. A resolver failure is `BLOCKED` for the whole run, never a per-PR "non-zero result". No further merge or `--auto` call is made, and the state snapshot is saved. A PR that already has a terminal label (`Merged`, any `Failed (…)` or `Skipped (…)`, or `auto-merge-uncertain`) keeps it. Every other remaining PR is reported as `Skipped (run blocked)`. In 3b, PRs that are already `active` keep the auto-merge GitHub accepted, which is still gated by their confirmed required checks. They are reported as `Skipped (run blocked) — auto-merge still enabled`, so the user can disable it. The resolver's stderr carries the `BLOCKED:` marker, and that marker, not the exit code, tells it apart from the base check's exit 3. The block never uses `${CLAUDE_SKILL_DIR}`, a `/path/to/` placeholder, or a repo-relative `codex/skills/` path. The gate:

- records `headRefOid` and requires `^[0-9a-f]{40}$`;
- branches on `gh pr checks --required` exit 0 / 8 / other;
- resolves "no required checks reported" with the API Contract outcome table;
- merges with `--match-head-commit "<sha>"`.

A refused merge re-reads `headRefOid,mergeable`. A moved head re-runs the Step 2 Dockerfile and major-version checks and the gate on it, with at most 2 restarts, then `Failed (head kept moving)`. An unchanged head reading `CONFLICTING` enters the conflict path; any other unchanged head is `Failed (merge refused)`. An unreadable re-read is `Skipped (head unreadable)`. Never retry unpinned.

The conflict path is entered only when `gh pr view {number} --json mergeable` reads `CONFLICTING`, either in the read before the gate or in the re-read after a refused pinned merge. Any other value, `UNKNOWN` included, goes through the gate. The conflict path deletes the manual fallback (`SKILL.md:183-199`: checkout, hand-resolve, push, unpinned merge). It keeps the Codex `rebase_intent` → `@dependabot rebase` → chunked polling contract (`SKILL.md:159-167`). A rebase is done when the polled `headRefOid` is 40-hex and differs from the recorded head, and `mergeable` is `MERGEABLE` (the T0 allowlist). Then re-run the Step 2 checks on that `NEW_HEAD` and wait for its fresh CI inside the same run-wide deadline and chunks; this is not a second wait. The deadline is run-wide: it is set once at the start of Step 3 and shared by every 3a wait, the 3b lane session and Stage 3, and it is never reset per PR. Persist `ci_wait[pr] = {head, restarts}` with the snapshot, so the 2-restart cap holds across chunks. Each chunk runs the gate's check step on `NEW_HEAD`, and its sleep is clamped to the remaining chunk and deadline budget:

- Exit 8, or "no required checks reported" with base-check exit 0, means keep waiting while `now < deadline`.
- Base-check exit 1 with a non-empty `BASE=` means wait on every check, by the same rule, and tag the result `(no required checks)`.
- Exit 0 means merge pinned with `--match-head-commit "<NEW_HEAD>"`, with the same restart rule.
- Any other non-zero exit is `Failed (CI not passing)`.
- Base-check exit 1 with an empty `BASE=`, exit 2 or exit 3 maps as in the API Contract table: `Skipped (no required check confirmed)` or `Skipped (required checks unconfirmed)`.
- "no checks reported" on the all-checks run means keep waiting, because a freshly rebased head may not have registered CI yet. If it is still reported at the deadline, the result is `Skipped (no CI checks)`, which takes precedence over the next bullet.
- Otherwise, at `now >= deadline` the result is `Failed (CI timeout)`.

A moved head during the wait restarts it, within the 2-restart cap. Polling exhaustion, a still-conflicting head, or red CI → skip and surface for human review.

Replace the Codex Step 2 "CI status" row with two rows. A failed check is `Failed (CI not passing)`. A pending check goes, in parallel-auto, to its lane and the FR-3 `--auto` start; in every other case it is `Skipped (CI pending)`.

Add the new labels to the Codex Step 2 table (a "CI pending" row), the Final Summary example and the Output Format: `Skipped (CI pending)`, `Skipped (head unreadable)`, `Skipped (no required check confirmed)`, `Skipped (required checks unconfirmed)`, `Skipped (no CI checks)`, `Failed (head kept moving)`, `Failed (merge refused)`, `Failed (CI timeout)`, `Skipped (deadline reached)`, `Failed (auto-merge possibly still enabled)`, `Skipped (run blocked)`. Keep every clause pinned by `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` verbatim. Update the Codex README lines that describe the conflict path (`README.md`, `README.en.md`, `README.ko.md`, `README.ja.md` line 12 or its equivalent) and the script-tree listing (`:93-94`) by hand. Regenerate `README.zh.md` / `README.es.md` through the repo translation flow. Never hand-edit an `AUTO-GENERATED` file. Reword the two lines that still describe manual resolution: the description at `SKILL.md:11` ("conflict resolution" → Dependabot rebase) and the Final Summary example at `SKILL.md:298` (`Failed (mixed pass) … manual conflict resolution required` → a 3a label).

### FR-3: Codex 3b base confirmation before every `--auto` (AC2)
Every `gh pr merge {number} --auto` start runs `check-base-required-checks.sh {number}` and records the head SHA first. In every code block that calls the script, whether a Stage 1 start, a Stage 2 lane start or the 3a gate, the FR-2 resolver lines come directly before the script call. The new call sites are counted for the `tests/codex_executable_resolution_test.py` bump (FR-1). A resolver failure is the run-wide `BLOCKED` of FR-2. This covers Stage 1 and each Stage 2 next-in-lane start (`SKILL.md:221`, `:246-249`). Only exit 0 with a 40-hex head may start the PR, pinned with `--match-head-commit "<sha>"`.

The base-check result is not persisted: the check runs in the same block as its `--auto` call, every time, including on resume. Immediately before `--auto`, re-read `baseRefName` and compare it with the script's `BASE=` value; a difference re-runs the check. No `--auto` intent is persisted (review-5 W1: a persisted intent had no reader). Instead, every `--auto` start, including on resume, first reads `gh pr view {number} --json state,autoMergeRequest,headRefOid`. Membership in the Stage 3 list is persisted as `stage3` (a list of PR numbers). Add it in a new sentence; the pinned "Persist `deadline`, `active`, `lanes`, `status`, and `rebase_commented`" sentence stays unchanged. A missing or malformed snapshot still returns `NEEDS_CONTEXT` per the pinned rule. Comparisons of persisted or remote values run in-process on parsed JSON, never interpolated into `--jq` or a shell string.

The pre-start read decides: `MERGED` / `CLOSED` is recorded as terminal; enabled auto-merge adopts the PR as `active`; empty auto-merge runs the check and the start; a failed read sends the PR out of its lane through the verified-disable rule below. On resume, PRs in `active`, `stage3` and `ci_wait` have their `state` read first, and every lane whose active PR was removed is advanced through the lane-start block (with its pre-start read) before polling, so a PR whose `--auto` was accepted just before a crash is adopted, polled and reported. Stage 3 starts only when `active` is empty and every lane's queue is empty.

Any non-zero result removes the PR from its lane, so the lane advances to its next PR, and adds it to `stage3`. A base-check failure before any `--auto` call goes to `stage3` directly. After any non-zero `--auto` result, re-read `autoMergeRequest` before the PR leaves its lane; this does not try to tell a definite refusal from a transport failure. An empty re-read moves the PR to `stage3`. An enabled or failed re-read means the PR "may already have auto-merge enabled"; the same holds when a resume read finds auto-merge enabled on a PR leaving its lane. Such a PR moves to `stage3` only after `gh pr merge {number} --disable-auto` succeeds and a re-read shows `autoMergeRequest` empty. Otherwise persist `status[pr] = "auto-merge-uncertain"`, report it as `Failed (auto-merge possibly still enabled)`, and leave it out of Stage 3. A resume retries `--disable-auto` once for each such PR. A retry that succeeds and re-reads an empty `autoMergeRequest` moves the PR to `stage3`.

If no PR's base is confirmed at Stage 1, announce "No required status checks confirmed on the base branch — falling back to sequential mode" and process every PR with 3a. Stage 3 processes the `mixed` group and the `stage3` list with the 3a logic (FR-2), under the run-wide deadline (FR-2). PRs that 3a or Stage 3 has not reached before the deadline are `Skipped (deadline reached)`. Update the README lines that describe 3b, in the same locales as FR-2.

`SkillContractTest` (in the FR-1 test file) asserts the following on the Codex `SKILL.md` text:

- the Stage 1 section names `check-base-required-checks.sh` before its `--auto` command;
- the Stage 2 section requires the check for a lane start;
- the Stage 3 section names the unconfirmed-base PRs and the persisted `stage3` list;
- every `gh pr merge {number}` / `gh pr merge "$…"` occurrence, at any indentation, carries `--match-head-commit` or is a `--disable-auto` call;
- the conflict path is entered only on `CONFLICTING`, waits for the rebased head's CI under the run-wide deadline and names `Failed (CI timeout)`;
- the base check runs before every `--auto`, including on resume, preceded by the `state,autoMergeRequest,headRefOid` pre-start read; no `auto_intent` is persisted; resume advances lanes whose active PR was removed;
- the FR-2 label set is present, including `Skipped (no CI checks)` taking precedence at the deadline and `Skipped (run blocked)`;
- a non-zero `--auto` result is followed by an `autoMergeRequest` re-read, `auto-merge-uncertain` is set only when that re-read is enabled or fails, and it is left only after a verified `--disable-auto`;
- `ci_wait` (with `restarts`) and `stage3` are in the persisted set, and `base_check` is not;
- a run-wide `BLOCKED` keeps every terminal label already recorded;
- `baseRefName` is re-read immediately before `--auto`;
- persisted or remote values are compared in-process and never interpolated into `--jq`;
- in every fenced block that calls the base-check script, the two resolver lines come directly before the call.

### FR-4: Codex finish-branch guard (AC4)
Port `claude-code/skills/ywc-finish-branch/SKILL.md:215-225` rule for rule into the Codex numbered guard, in this order, keeping Codex numbering and style:

1. Validate the branch in-process: whole-string allowlist `^[A-Za-z0-9._/-]+$`, no leading `-`, no `..`, then `git check-ref-format "refs/heads/$branch"`. Any failure returns `BLOCKED: invalid branch name`, and no remote command runs.
2. Pin the push target: `url` is `git remote get-url origin` and must not start with `-`. `git remote get-url --push --all origin` must print exactly one line equal to `url`; otherwise `NEEDS_CONTEXT`.
3. Bind the repository: `env -u GH_HOST gh repo view --json url,isFork,parent -- "$url"`, host-qualified. `repo`, and `parent` for a fork, must each match `^[A-Za-z0-9.-]+/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$`, otherwise `NEEDS_CONTEXT`. Every `gh` call is `env -u GH_HOST gh … --repo "$repo"`. When origin is a fork, both the merged check and the open-PR check also run with `--repo "$parent"`, and a parent that is itself a fork returns `NEEDS_CONTEXT`.
4. Read the exact remote tip with `git ls-remote origin "refs/heads/$branch"`. Take the one line whose ref is exactly `refs/heads/$branch`; its tip must have the shape `^[0-9a-f]{40}([0-9a-f]{24})?$`. An absent ref is already absent, with zero deletions. Ambiguous output is `NEEDS_CONTEXT`.
5. Merged check (unconditional, replacing "If deletion relies on a merge"): a merged row with the intended base and `headRefOid` equal to the tip.
6. Open-PR check, last before the delete.
7. Tip-bound lease delete.

Outcomes: a non-zero command exit is `BLOCKED`. An undeterminable repository, a failed shape check, or ambiguous output is `NEEDS_CONTEXT`. An open PR, no matching merged row, or a tip mismatch stops with zero deletions and reports the PR numbers or both SHAs.

JSON comparisons are done in-process, never interpolated into `--jq`. State the race window between step 6 and the delete.

Keep the fixture-pinned clauses verbatim: `**Remote deletion guard**`, "only a successful, parseable, empty result allows deletion", "`baseRefName` is the intended base and `headRefOid` equals the current remote tip", "Never infer a merge from `git branch -r --merged HEAD`", "tip-bound lease". In `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json`, replace the required `git check-ref-format --branch "$branch"` with `git check-ref-format "refs/heads/$branch"`, and add required clauses for `git remote get-url --push --all origin`, `env -u GH_HOST gh`, `--repo "$parent"`, the tip shape `^[0-9a-f]{40}([0-9a-f]{24})?$` and `race window`, plus forbidden `check-ref-format --branch` and `If deletion relies on a merge` (the merged check is unconditional). The strings `check-ref-format --branch` and `If deletion relies on a merge` must appear nowhere in that `SKILL.md`, not even in a "do not use" remark.

In `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json`:

- `invalid-branch`: replace the input with an allowlist failure (`allowlist_match: false`), and set its `source_clause` to the allowlist clause. Add that clause, byte-equal, to the adoption fixture's `required` list.
- Reorder the `expected_trace` arrays of `empty-open-pr`, `wrong-base`, `moved-tip` and `matching-merge` to the FR-4 order: tip, then merged check, then open-PR check.
- Give `empty-open-pr` a matching merged row, so that its `ALLOWED` result follows the unconditional step 5.
- Give `open-pr`, `nonparseable` and `api-failure` the passing earlier steps as inputs (an exact tip and a matching merged row), so that their open-query result is the one that decides.

Update the guard description lines in the Codex finish-branch `README.md`, `README.en.md`, `README.ko.md` and `README.ja.md` by hand, and regenerate the zh/es files.

### FR-5: Dispatch-only tag (AC5, AC6)
Add `tags: [dispatch-only]` to the frontmatter of the four agents named in the complement paragraph under Existing Constraints Touched. In `score.py`, an agent is "dispatch-only" when this procedure yields an element exactly equal to `dispatch-only` (case-sensitive):

1. Cut the raw `tags` value at the first `#` that starts the value or follows whitespace (`re.split(r'(?:^|\s)#', value)[0]`). This drops a trailing comment, including one after a tab. It also drops everything after a leading comment line, so a real tag that follows one is not exempt (fail-closed).
2. Split it on `[`, `]`, `,` and whitespace.
3. Strip `'` and `"` from each element. This accepts the flow form and the block-list form `parse_yaml_lite` produces, and rejects `dispatch-only-x`, `non-dispatch-only`, `Dispatch-Only`, `dispatch_only` and a commented-out mention. `apply_coverage_exemption` is shared with skill scoring, so the rule applies to any item, but this spec tags only the four agents. Delete `DISPATCH_ONLY_RE` and keep the slash-only rule. Update the `score.py` comment block and rewrite `test_score.py:676-689` to set `tags`. Document the tag's meaning in `claude-code/agents/CLAUDE.md` (optional keys table).

### FR-6: Release gate (AC7)
After FR-1..FR-5 merge, run the whole-run review once over `<run_start_sha>..feature/improvement-20261106`, where `<run_start_sha>` is `git merge-base main feature/improvement-20261106`. `ywc-impl-review` has no `--depth` flag, and its Step 2.5 refuses a `--git-range` over 200 files or 5,000 changed lines. So split the first-parent history at task-merge boundaries (the `chore: mark … as completed` commits) into consecutive ranges `<a>..<b>`, with no gap and no overlap. Before dispatching, measure each range with `git diff --shortstat <a>..<b>` and keep it within both limits; a single task merge over the limit is split at its own commits. Adjacent ranges may be merged into one while the result stays within both limits. A range whose `git diff --name-only <a>..<b>` is empty is merged into the next range and never dispatched alone, because `ywc-impl-review` returns `NEEDS_CONTEXT` on an empty range. Run `/ywc-impl-review --git-range <a>..<b> --non-interactive` once per range. Fix Critical/High in one pass; per-task delivery is already done, so fixes for findings from every chunk go in one new commit at the branch tip, and the code each finding names is re-checked at the tip before it is fixed. A targeted re-review of that fix commit (`/ywc-impl-review --git-range <fix_parent>..<fix_sha>`) must then report no Critical/High; it is this re-review that closes AC7. Then reuse the existing draft PR #214 instead of opening a second PR: update its body with `ywc-create-pr` (PR body language per `resolve-config.sh`) and mark it ready. If PR #214 is closed by then, open a new PR with `ywc-create-pr`. If a Critical/High finding cannot be fixed in that pass, leave #214 as a draft, do not mark it ready, and report the finding.

## Module Boundaries

N/A — no new module; changes stay inside existing skills, the eval scorer and agent frontmatter.

## Non-Functional Requirements

- Every new or ported guard has a test seen failing once (RED) before the fix, or a recorded mutation run. For prose guards in a Codex `SKILL.md`, a source assertion counts: `SkillContractTest` (T1) or an issue69 fixture clause (T2) that fails on the pre-change text.
- No new dependency (no YAML library; `awk`/`grep`/`python3` stdlib only).
- `SKILL.md` body ≤ 500 lines for every touched skill.

## Critical Surfaces

- `codex/skills/ywc-merge-dependabot/**` — remote-controlled `baseRefName` / `headRefOid` reaching shell and `gh`; merge of an unverified head. → T1 `critical`.
- `codex/skills/ywc-finish-branch/SKILL.md` Remote deletion guard — remote branch deletion can auto-close an open PR. → T2 `critical`.
- T3 (eval scorer and agent tags) is `normal`.

## Data Model

N/A — no persistent data model change.

## API Contract

N/A — no service API. Script contracts that change: `check-base-required-checks.sh` exit 3 (owned by T0, consumed by T1). How the Codex gate (FR-2) reads the script's last stdout line `CONFIRMED=<0|1> BASE=<…>` together with its exit code:

| Exit | `BASE=` | Meaning | Codex 3a outcome | Codex 3b `--auto` |
|---|---|---|---|---|
| 0 | validated base | base has ≥1 required check | `Skipped (CI pending)` (checks not registered yet) | allowed |
| 1 | non-empty | validated base, zero required checks | gate on every check, result tagged `(no required checks)` | not allowed → Stage 3 |
| 1 | empty | `baseRefName` unreadable or invalid | `Skipped (no required check confirmed)` | not allowed → Stage 3 |
| 3 | any | lookup failed (403, rate limit, unparseable) | `Skipped (required checks unconfirmed)` | not allowed → Stage 3 |
| 2 / other | any | usage error or unexpected | `Skipped (no required check confirmed)` | not allowed → Stage 3 |

## Edge Cases

- Codex 3b resume after a chunk boundary where the base check ran but the lane start did not: the result was not persisted, so the check re-runs before the `--auto` call. `--auto` is never called on an unconfirmed PR.
- Stage 2 lane advance where the next PR's base is unconfirmed: that PR moves to the persisted `stage3` list and the lane advances to its following PR in the same chunk.
- Dependabot pushes a new head between the 3b base check and `--auto`: the pinned `--match-head-commit` call is refused, and the PR moves to Stage 3, which re-reads the head.
- Codex conflict path after the comment, but before `rebase_commented` is saved: the existing `rebase_intent` reconciliation applies, and no second comment is sent.
- The process dies after GitHub accepted `--auto` and before the snapshot that records `active`: on resume the lane is advanced through the lane-start block, whose `state,autoMergeRequest,headRefOid` pre-start read adopts the PR as active; the PR is never started twice or demoted while auto-merge stays enabled.
- An active PR's head moves (Dependabot rebase) after `--auto`: it stays active; the base check is not re-run for started PRs, and GitHub evaluates the confirmed required checks on the merged head.
- A PR's base is retargeted between the base check and `--auto`: the `baseRefName` re-read differs from `BASE=` and the check re-runs.
- PR #214 already exists at the release gate: it is reused and updated, never duplicated (FR-6).
- `gh pr checks --required` exits 8 at the deadline: never merged. A post-rebase wait records `Failed (CI timeout)`, and a lane PR records `Failed (lane stalled)`.
- origin with two `pushurl` entries or a `pushInsteadOf` rewrite: `NEEDS_CONTEXT`, zero deletions.
- An agent whose description happens to say "no natural-language triggers" without the tag: not exempt (AC6).
- `tags: [dispatch-only, language-reviewer]` (multiple tags): still exempt — equality of one element, not of the whole value.

## Failure Modes

| New path | Realistic failure | Handling | Test |
|---|---|---|---|
| Codex 3a gate | `gh` lookup 403 / rate limit | exit 3 → `Skipped (required checks unconfirmed)`, no merge | `CheckBaseRequiredChecksTest` + `SequentialCiGateTest` on the extracted Codex block (FR-1) |
| Codex 3a merge | head moved after the CI check | pinned merge refused → re-read, ≤2 restarts, then `Failed (head kept moving)` | `SequentialCiGateTest` + `SkillContractTest` |
| Codex 3b Stage 1 / Stage 2 start | base without required checks | PR moved to Stage 3; never `--auto` | `SkillContractTest` (FR-3) |
| Codex 3b resume | head or base changed since the last chunk | the base check always re-runs before `--auto`; nothing is reused | `SkillContractTest` asserts the re-run rule and that `base_check` is not persisted |
| Codex post-rebase CI wait | rebased head's CI still pending at the deadline | `Failed (CI timeout)`, no merge | `SkillContractTest` asserts the wait rule and label |
| Codex post-rebase CI wait | all-checks run still reports no checks at the deadline | `Skipped (no CI checks)` (takes precedence over `Failed (CI timeout)`) | `SkillContractTest` |
| Codex resolver | bundle not installed / launcher fails | run-wide `BLOCKED`; remaining PRs `Skipped (run blocked)`; active 3b PRs reported with auto-merge still enabled | `SequentialCiGateTest` (temporary `CODEX_HOME`, `BLOCKED:` stderr) + `tests/codex_executable_resolution_test.py` count |
| Codex conflict poll | `null` / short / unchanged head, or `mergeable` ≠ `MERGEABLE` | not rebased → skip and surface, no merge | `SkillContractTest` asserts the done condition and that no manual path remains |
| Codex finish-branch | push URL differs from fetch URL | `NEEDS_CONTEXT`, zero deletions | issue69 contract fixture clauses (FR-4) + AC4 greps |
| score.py tag rule | tag typo (`dispatch_only`) | agent not exempt → coverage gap → `test_shipped_catalog_has_no_unexplained_gap` (run by `validate.sh` after T0) fails | AC6 `[dispatch_only]` case + that catalog test |
| Release gate | a review range exceeds the `ywc-impl-review` scope guardrail | split that range further at its own commits; never review a partial range | FR-6 `git diff --shortstat` per chunk |
| Release gate | whole-run review finds a High | one fix pass before marking PR #214 ready; if not fixable, report and leave #214 draft | AC7 |

## Rollout & Rollback

Each task merges locally (`--local-merge`) onto `feature/improvement-20261106`; rollback is `git revert -m 1 <merge>`. The PR to `main` is the release point; nothing ships to `main` before AC7.

## Dependencies

- T1 depends on T0 (needs `check-base-required-checks.sh` exit 3, the T0 `MERGEABLE` allowlist rule, and the updated `validate.sh` `run_script_test_suites`).
- T2 owns `tests/fixtures/codex-issue69/upstream-adoption/operational-safety.json` and `tests/fixtures/codex-issue69/upstream-behavior/operational-safety/expected-traces.json`. T1 edits no fixture; it only keeps the merge-dependabot clauses of the first file satisfied. T1 also owns `tests/codex_executable_resolution_test.py` (`CALLER_FILES` and the count) and the Codex merge-dependabot READMEs; T2 owns the Codex finish-branch READMEs.
- T2 and T3 are independent of T0/T1 and of each other. `scripts/validate.sh` is edited by T0 and then T1 only (sequential through the dependency); T3 edits `test_score.py`, which T0 only starts running. So T2 and T3 can run in parallel with T0 → T1.
- `history.mechanical.json`: every task runs `score.py --ci`; parallel tasks restore it and the last task to merge stages it.

## Open Questions

- **Confidence gate (ywc-plan Step 3.6): 89 REVIEW**, weakest = Architecture compliance (88): how the ported scripts bind into Codex 3b's persisted lane/deadline design. Default chosen: **A** — port `check-base-required-checks.sh` unchanged and change only the Codex call sites; the base check runs before every `--auto` and its result is not persisted (FR-3). The rebase-wait script is not ported (Iteration 1 advisor verdict; see Out of Scope). Alternative **B** — prose-only rules in Codex `SKILL.md` without scripts (fewer files, not test-pinned). **Resolved: user accepted A on 2026-11-07.**
- P2-a..P2-d are recorded in Out of Scope with their reason; a separate plan is expected after the `main` PR.

## References

- `tasks/completed/yk-000010-0{10..60}-*/` (Implementation Notes and rulings)
- `docs/review-learnings.md`
- `claude-code/skills/ywc-worktrees/SKILL.md` `--existing-branch` bullet (canonical C2 rule)

## Amendment Log

### Iteration 1 — 2026-11-07

**Driven by**: DONE_WITH_CONCERNS, gate 90 PROCEED, 6/9/11 findings
**Signatures**: `compat:fixture-pins-check-ref-format-branch`, `compat:test-copy-covers-absent-scripts`, `compat:conflict-path-unpinned-merge`, `compat:lane-advance-auto-uncovered`, `compat:stage3-mixed-only`, `feasibility:rebase-script-vs-intent-protocol`, `completeness:3b-base-check-state-undefined`, `completeness:new-head-recheck-omitted`, `completeness:finish-guard-order-and-conditional`, `completeness:finish-guard-untested`, `completeness:tag-token-boundary`, `compat:new-statuses-not-in-labels`, `compat:behavior-test-not-in-validate`, `consistency:stale-line-cite`, `completeness:run-start-sha-undefined`, `completeness:pr-idempotency`

> Advisor verdict (P2): `wait-dependabot-rebase.sh` cannot run under the Codex `rebase_intent`-before-comment and one-deadline contract, so it is not ported; Codex keeps its chunked polling and gates the rebased head. Open Question option A stays the user-pending default, reworded to the one ported script. A draft PR #214 to `main` already exists; FR-6 reuses it.

| Section edited | What changed | Why |
|---|---|---|
| `## Global Constraints` | Corrected the `claude-code/agents/CLAUDE.md` cite to `:87`; noted that the named validator file is absent | "`claude-code/agents/CLAUDE.md:83`" — the sentence is at :87 |
| `## Scope` | Mapped T1..T3 and the release gate to FRs; T1 no longer ports the rebase script; T2 includes the issue69 fixtures | "Codex `ywc-merge-dependabot` parity with the Claude Code copy as it stands after T0." |
| `## Out of Scope` | Added the non-ported scripts with the advisor reason, and P2-d (Codex `ywc-worktrees` C2 form) | n/a — additive |
| `## Existing Constraints Touched` | Added rows for the 3a conflict path, labels, Stage 2/3, issue69 fixtures, the Claude test's extra classes, READMEs, and `test_score.py:676-689`; corrected the evals, behavior-test, `parse_yaml_lite` and `CLAUDE.md` rows | "T1 complies: script calls run inside the existing chunk/state contract; no second deadline" |
| `## Acceptance Criteria` | AC1 `cmp` + non-port check; AC2 unpinned-merge / no-checkout checks + `SkillContractTest`; AC3 explicit behavior test, RED run, shellcheck; AC4 C2 grep, order check, contract test; AC6 token cases; AC7 `run_start_sha` + PR #214 | "Baseline: PR list → `[]`." — PR #214 already exists |
| `## Functional Requirements` | FR-1 trimmed test + `/path/to/` substitution; FR-2 gate, merge-refusal restarts, conflict path without manual fallback, labels; FR-3 every `--auto` start, `base_check` persistence, Stage 3; FR-4 ordered guard + fixtures; FR-5 token rule; FR-6 PR reuse | "The conflict path uses `wait-dependabot-rebase.sh` and the same gate on `NEW_HEAD`." |
| `## Non-Functional Requirements` | Source assertions count as the RED test for prose guards | n/a — additive |
| `## API Contract` | Added the exit × `BASE=` outcome table | n/a — additive |
| `## Edge Cases` | Resume with stale `base_check`, Stage 2 unconfirmed advance, head moved before `--auto`, comment/marker race, existing PR | "the persisted lane state must record the check result so the resume does not call `--auto` on an unconfirmed PR." |
| `## Failure Modes` | Replaced ported-script test references with the Codex test classes and fixture clauses; added head-moved and resume rows | "Codex rebase wait \| `null` / short head \| `REBASED=0`, no merge \| ported `wait-dependabot-rebase` test" |
| `## Dependencies` | T1 needs the T0 `MERGEABLE` rule; T2 owns the two fixtures | n/a — additive |
| `## Open Questions` | Option A reworded to the one ported script; P2 range to P2-d (duplicate-claim sweep) | "port the scripts unchanged and change only the Codex call sites" |

### Iteration 2 — 2026-11-07

**Driven by**: DONE_WITH_CONCERNS, gate 91 PROCEED, 1/9/14 findings
**Signatures**: `compat:conflict-path-ci-wait-omitted`, `compat:pending-handoff-and-base-fallback-omitted`, `completeness:base-check-stale-vs-active`, `completeness:auto-start-crash-window`, `compat:finish-guard-subrules-dropped`, `compat:traces-encode-old-order`, `compat:resolver-contract-unacknowledged`, `consistency:ac4-misses-expected-traces`, `consistency:ac1-grep-vs-trimmed-test-copy`, `completeness:tag-token-comment`, `feasibility:quoted-tag-token`, `completeness:merge-line-regex-col0`, `completeness:stage3-deadline-label`, `completeness:fr6-pr214-failure-state`, `consistency:readme-locale-ownership`

> No advisor call: the post-rebase CI wait follows the existing Codex text ("Rebase completion must be tied to the resulting head and its fresh CI run", `codex/skills/ywc-merge-dependabot/SKILL.md:165`), and the script call follows the normative Codex resolver contract (`codex/skills/references/shared-script-resolution.md`) that the sibling Codex `ywc-finish-branch` already uses.

| Section edited | What changed | Why |
|---|---|---|
| `## Purpose` | "130 commits" → "about 130 commits" | "(130 commits ahead of `main`)" — now 131 |
| `## Existing Constraints Touched` | Corrected Stage 1/2 cites; added the resolver-contract row, the CI-pending row note and the expected-traces row; the scripts row and the Claude test row now use the resolver / temporary `CODEX_HOME` | "same `/path/to/` convention" — the resolver contract is normative for Codex helpers |
| `## Acceptance Criteria` | AC2 merge scan covers any indentation; AC4 runs the behavior test; AC6 adds the typo, quoted and comment cases | "`grep -nE '^gh pr merge ' …` prints nothing" — an indented unpinned merge would pass |
| `## Functional Requirements` | FR-1 lift list, no rebase-script name, resolver-based test + count bump; FR-2 resolver call, post-rebase CI wait, pending row, labels, README locales; FR-3 `{head, base, rc}`, `auto_intent`, started-PR scope, verified `--disable-auto`, sequential fallback, deadline label; FR-4 rule-for-rule port with shape check, ls-remote rule, parent runs, outcomes, trace fixture updates; FR-5 comment/quote handling; FR-6 draft stays draft on an unfixable finding | "Then re-run the Step 2 checks on that `NEW_HEAD` and run the same gate with `NEW_HEAD` as the pinned SHA." — a fresh head is still pending, so every rebased PR would be skipped |
| `## Edge Cases` | Added the crash after an accepted `--auto`, an active PR's moved head, and a base retarget | n/a — additive |
| `## Failure Modes` | Added post-rebase CI wait and resolver rows; fixed the tag-typo test name and the release-gate wording | "if not fixable, report and do not open the PR" — PR #214 already exists |
| `## Dependencies` | T1 owns the resolver test and merge-dependabot READMEs; T2 owns the finish-branch READMEs | n/a — additive |

### Iteration 3 — 2026-11-07

**Driven by**: DONE (suggestion pass), gate 92 PROCEED, 0/12/16 findings
**Signatures**: `completeness:gate-snippet-capture`, `security:remote-values-compare`, `completeness:possibly-enabled-pr-undefined`, `completeness:tag-comment-leading-line`, `completeness:trace-preconditions`, `completeness:ac7-no-recheck`, `feasibility:resolver-test-env-isolation`, `feasibility:test-must-not-name-excluded-script`, `feasibility:count-bump-readme-and-line-budget`, `feasibility:wait-path-unmapped-outcomes`, `compat:cite-offset`, `compat:missing-entry-vs-missing-state`, `compat:stale-manual-resolution-wording`, `consistency:wording-nits`

> Suggestion-focused pass (ywc-spec-ready Step 4). It addresses Suggestions only; the 12 Warnings from the same report are pre-existing and, per the loop rule, are not chased here.

| Section edited | What changed | Why |
|---|---|---|
| `## Existing Constraints Touched` | Corrected the resolver-test cite to `:20-37,205-217` | "`tests/codex_executable_resolution_test.py:20-35,206-217`" |
| `## Acceptance Criteria` | AC7 is closed by the targeted re-review after the one fix pass; added the AC6 leading-comment case | "reports no Critical/High" — unclear after a fix pass |
| `## Functional Requirements` | FR-1: temporary tree contents, env isolation, first-block rule, no literal script name, README prose, line budget; FR-2: `$(…)` capture, lazy resolver, run-wide `BLOCKED`, unmapped wait outcomes, stale manual wording at `:11`/`:298`, new label; FR-3: in-process comparisons, base re-read before `--auto`, per-PR vs snapshot missing rule, `auto-merge-uncertain` status; FR-4: earlier-step inputs for three traces; FR-5: leading `#` cut, shared-scorer scope, cross-reference; FR-6: targeted re-review | "bash \"$BASE_CHECK_SCRIPT\" {number}" — the bare call loses the output the `case` reads |
| `## Edge Cases` | Labels named for exit 8 at the deadline; "element equality" wording | "recorded as pending/stalled, never merged" |

### Iteration 4 — 2026-11-07

**Driven by**: DONE_WITH_CONCERNS (repair-suggestion-regression), gate 91 PROCEED, 1/22/24 findings; scope limited to findings the Iteration 3 pass introduced
**Signatures**: `feasibility:whole-run-review-scope-guardrail`, `feasibility:impl-review-depth-flag`, `consistency:ac7-pr214-vs-fr6-fallback`, `consistency:fr5-procedure-leading-comment`, `consistency:wait-deadline-label-precedence`, `consistency:resolver-scope-vs-3b-nonzero`, `completeness:blocked-3b-and-label`, `compat:lane-state-fallback-moves-pinned-text`, `completeness:uncertain-trigger-undefined`, `completeness:contract-test-gaps`

> Pre-existing Warnings from earlier reports are still not chased, among them the `auto_intent` lifecycle, the conflict trigger, the deadline scope, the persisted restart count and the finish-guard fixture pins. They are listed as residual warnings in the loop log.

| Section edited | What changed | Why |
|---|---|---|
| `## Scope` | Release gate names the chunked `/ywc-impl-review` and PR #214 | "one whole-run `--final-review`, then a PR" — no such flag exists |
| `## Acceptance Criteria` | AC7: chunked ranges with a measured scope baseline (225 files, +7028/−848), no `--depth`, and the release PR is #214 or its replacement | "`/ywc-impl-review --git-range <run_start_sha>..feature/improvement-20261106 --depth full`" — refused by the Step 2.5 hard block |
| `## Functional Requirements` | FR-6 chunking rule; FR-5 step 1 cuts at `(?:^\|\s)#`; FR-2 `Skipped (no CI checks)` precedence, run-wide `BLOCKED` semantics in 3a/3b with `Skipped (run blocked)`; FR-3 resolver lines per block, defined `auto-merge-uncertain` trigger and exit; FR-1 `lane-state.md` keeps pinned text in `SKILL.md`; `SkillContractTest` covers the new guards | "Cut the raw `tags` value at the first ` #`" — misses a leading comment |
| `## Failure Modes` | Rows for the no-checks-at-deadline precedence, the run-wide resolver `BLOCKED`, and an over-limit review range | n/a — additive |

### Iteration 5 — 2026-11-07

**Driven by**: DONE (residual-warning cleanup, user-requested), gate not re-scored (no design change), 0/10/30 findings
**Signatures**: `consistency:resolver-lazy-vs-opens-with`, `completeness:uncertain-trigger-vs-test`, `consistency:blocked-label-precedence`, `completeness:chunk-policy-gaps`, `completeness:stage3-list-unnamed`, `feasibility:persisted-base-check-cache`, `completeness:auto-intent-lifecycle`, `completeness:conflict-trigger-undefined`, `feasibility:deadline-scope-sequential-stage3`, `completeness:finish-guard-subrules-unpinned`

> The user accepted Open Question option A on 2026-11-07. Simplest resolutions taken: `base_check` persistence is dropped (the check re-runs before every `--auto`), and any non-zero `--auto` result is resolved by an `autoMergeRequest` re-read instead of classifying refusal vs transport failure.

| Section edited | What changed | Why |
|---|---|---|
| `## Existing Constraints Touched` | `:159-167` row lists `auto_intent`, `ci_wait`, `stage3` as the new persisted entries; base check not persisted (duplicate-claim sweep) | "the base-check result is a new persisted entry (FR-3)" |
| `## Acceptance Criteria` | AC4 adds the `If deletion relies on a merge` absence grep and its baseline (0) | n/a — additive |
| `## Functional Requirements` | FR-1 `lane-state.md` list (sweep); FR-2 resolver lines directly before each call, `BLOCKED` keeps terminal labels, `CONFLICTING` trigger, run-wide deadline, `ci_wait.restarts`; FR-3 no `base_check`, `stage3` named, `auto_intent` clear points and failed read, re-read after any non-zero `--auto`, deadline label covers 3a; `SkillContractTest` bullets updated; FR-4 more fixture clauses, "race window"; FR-6 range coalescing, empty-range rule, fixes at the tip | "The resolver lines run lazily, inside the \"no required checks reported\" branch" — FR-3 and the test said "opens with" |
| `## Edge Cases` | Resume, active-head and base-retarget cases no longer use `base_check`; `stage3` named (sweep) | "On resume it is reused only when its `head` equals the current `headRefOid`" |
| `## Failure Modes` | 3b resume row: check always re-runs (sweep) | "stale `base_check` entry from an older head" |
| `## Open Questions` | Option A marked resolved; persistence wording dropped (sweep) | "Implementation handoff waits for the user to accept A or pick B." |

### Iteration 6 — 2026-11-07

**Driven by**: yk-000012-010 critical impl-review (DONE, 0 Critical/High), Medium "spec stale against the W1 deviation"; gate not re-scored (spec follows the delivered implementation)
**Signatures**: `consistency:spec-auto-intent-vs-implementation`, `completeness:resume-lane-advance`

> The implementation (yk-000012-010, review-5 W1) dropped the persisted `auto_intent` in favour of a live pre-start read before every `--auto`; its review then added the resume lane-advance rule. This entry brings the spec in line.

| Section edited | What changed | Why |
|---|---|---|
| `## Existing Constraints Touched` | `:159-167` row: new persisted entries are `ci_wait` and `stage3` only | "the new persisted entries are `auto_intent`, `ci_wait` and `stage3`" |
| `## Functional Requirements` | FR-1 `lane-state.md` list drops `auto_intent`; FR-3 replaces the `auto_intent` write/clear/resume rules with the `state,autoMergeRequest,headRefOid` pre-start read, the resume lane advance and the Stage 3 drain condition; `SkillContractTest` bullet updated | "Before the `--auto` call, persist by the same atomic snapshot `auto_intent[pr] = {head}`." |
| `## Edge Cases` | crash-after-`--auto` case decided by the resume lane advance + pre-start read | "the `auto_intent` entry plus an `autoMergeRequest` read decides" |
