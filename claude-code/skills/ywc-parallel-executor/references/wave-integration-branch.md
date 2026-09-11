# Wave Integration Branch (`wave-int/<N>`) — Lifecycle, Promotion, Conflict Handling

> Tier-3 reference extracted from `SKILL.md` (ywc-skill-author A8/A14, FR-9 line-cap discipline). Linked from Step 4e's `> **Action required**` directive. Implements FR-1, FR-2, FR-4 of `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md`.

## Why this exists

Today, Step 4e delivers every wave task directly into the base branch and stamps `wave-complete`, then Step 4e.5's Hardener runs against the already-merged base — too late for a `BLOCKED` verdict to prevent anything reaching base. The fix is not to gate *before* merge (Hardener needs the merged diff to see cross-task interaction gaps) — it is to move the merge *target* to a wave-scoped integration branch, gate promotion of that branch into base on the Hardener verdict.

**The rule**: an isolation branch can only protect state whose point-of-no-return sits after the gate. **The consequence**: `--per-task-pr` reaches its point-of-no-return at `gh pr merge --delete-branch`, once per task, inside the wave — no branch topology can move that behind the wave boundary. So `wave-int/<N>` applies only to `--local-merge`, `--draft`, and `--aggregate-pr` (the three modes whose actual point-of-no-return — a local merge push, a still-open draft, or an unmerged aggregate PR — sits after the wave completes). Under `--per-task-pr` the wave-boundary Hardener is reporting-only and may not return `BLOCKED` even under an `enforced` contract; blocking authority for that mode stays entirely at Step 4c.5, which already runs per-task before PR creation. See `../../references/quality-gates.md` for the enforcement-eligibility rule this carve-out follows.

## Contract-bearing wave scan (Pre-flight, before `init-parallel`)

`cmd_init_parallel`'s only input is the `--waves` JSON array (task names only) — it has no access to any task's declared `quality_gate_contract` field. Before calling `init-parallel`, compute a per-wave `has_contract` boolean:

1. For each wave, read every member task's declared `quality_gate_contract` field from its task-directory spec/README.
2. OR across the wave's tasks against the exact `N/A — no quality gate contract` sentinel (`../../references/quality-gates.md` §7) — contract-bearing if any task's field differs from that sentinel.
3. Extend the `--waves` entry: `{"wave":1,"tasks":["t-a","t-b"],"has_contract":true}`.
4. **Malformed / missing field / absent task directory** — each of these three cases stops Pre-flight with `NEEDS_CONTEXT`, naming the offending task and the missing/malformed field. Never silently resolve to `false` — that would route a possibly contract-bearing wave direct to base, the exact regression the no-block invariant forbids.

This evaluation happens **once per wave**, during this Pre-flight scan, never re-derived at Step 4e.

## Creation (Step 4e, before per-task delivery)

Step 4e creates `wave-int/<N>` **if and only if** that wave's `integration_branch` field is already non-`None` in `.ywc-run-state.json` (seeded by the Pre-flight scan above via `init-parallel`'s `has_contract` input — see `yw-000036-010`). Step 4e never re-derives the contract check itself. A wave where `integration_branch` is `None` (every task contract-less) delivers direct to base exactly as today — no `wave-int/<N>` is created, and the rest of this document does not apply to that wave.

**Reuse verification (checkpoint ownership + tip-SHA).** Before creating or reusing `wave-int/<N>`, verify ownership rather than reusing unconditionally — a checkpoint claiming ownership of a branch that no longer exists must never be silently treated as a fresh creation, and a different run's stale `BLOCKED` branch must never be silently promoted. The procedure:

1. Run `python3 claude-code/skills/scripts/update-state.py wave-int-status <N>` to read `integration_branch_owner` / `integration_branch_tip_sha`. This succeeds even against a pre-this-spec checkpoint with no `run_id` at all (prints `unset unset`), so the procedure always reaches step 5 below.
2. Check whether `wave-int/<N>` exists (local or `origin`) — verify against `refs/heads/wave-int/<N>` explicitly rather than the bare short name, since Git resolves ambiguous names by checking `refs/tags/` before `refs/heads/`; a same-named tag would otherwise make `rev-parse --verify` succeed against the wrong ref and skip the remote check entirely:
   ```bash
   git rev-parse --verify refs/heads/wave-int/<N> 2>/dev/null || git ls-remote --exit-code --heads origin wave-int/<N> >/dev/null 2>&1
   ```
3. **Owner recorded, branch missing** (`integration_branch_owner` is set but neither a local nor an `origin` `wave-int/<N>` exists) → call `python3 claude-code/skills/scripts/update-state.py wave-int-blocked <N> --reason wave-int-branch-missing --detail "branch=wave-int/<N> recorded-owner=<owner> recorded-tip=<tip-sha>"`. Do not create a fresh branch under this wave number without operator intervention.
4. **Branch does not exist, no owner recorded** → branch it from the current base:
   ```bash
   git checkout <base-branch>
   git pull origin <base-branch>
   git checkout -b wave-int/<N>
   git push origin wave-int/<N>
   ```
   then immediately call `python3 claude-code/skills/scripts/update-state.py wave-int-owner <N> --tip-sha "$(git rev-parse refs/heads/wave-int/<N>)"`.
5. **Branch exists** → verify before reuse:
   1. If `integration_branch_owner` is unset, or is set but does not equal the current run's `run_id` (read from `.ywc-run-state.json`) → call `python3 claude-code/skills/scripts/update-state.py wave-int-blocked <N> --reason wave-int-ownership-mismatch --detail "branch=wave-int/<N> owner=<recorded-owner-or-none> current-run=<run_id>"`. Do not merge, promote, or delete the branch.
   2. If owner matches, materialize the local ref if needed (see FR-4 below), then run `git cat-file -e <recorded-tip-sha>`. If this fails (object unreachable), call `wave-int-blocked <N> --reason wave-int-materialize-failed --detail "branch=wave-int/<N> recorded-sha=<recorded-sha> unreachable: <raw git error>"` — never `wave-int-tip-mismatch` for a git-internal failure. Otherwise check `git merge-base --is-ancestor <recorded-tip-sha> refs/heads/wave-int/<N>`: exit `0` (the checkpoint's last-known-good tip is an ancestor of, or equal to, the branch's current tip) → reuse it, merge the wave's remaining `pending` tasks onto it exactly as if the run had never stopped (this is what makes a partial-merge interruption safe to resume — see `checkpoint-resume.md`'s partial-merge case). Non-zero exit (history diverged from what this run last recorded) → call `wave-int-blocked <N> --reason wave-int-tip-mismatch --detail "branch=wave-int/<N> recorded=<recorded-sha> actual=<actual-tip-sha>"`.

This ancestor-check (rather than exact SHA equality) is what makes the ordinary resume case above satisfiable: ownership is recorded only at creation and post-base-merge (see below), so a legitimate in-progress wave's actual branch tip routinely runs ahead of the last recorded `integration_branch_tip_sha` — an equality check would misclassify that gap as a divergence on every ordinary resume.

**Push at creation is mandatory.** `wave-int/<N>` is pushed to origin immediately at creation, before any task's `ywc-finish-branch` call runs against it. `ywc-finish-branch`'s `local-merge` sequence (`SKILL.md:218-226`) runs `git pull origin <base-branch>` unconditionally per task, which fails with `fatal: couldn't find remote ref` against a local-only branch. No change to `ywc-finish-branch` itself is needed once the remote ref exists — this generalizes `ywc-sequential-executor/references/aggregate-pr.md:30,34-35`'s `WORK_BRANCH` push-at-creation precedent from a run-level branch to a wave-level one.

**Origin-only branch materialization (FR-4).** Before the ancestor-check comparison in step 5.2 above, if `git rev-parse --verify wave-int/<N>` fails locally but `git ls-remote --exit-code --heads origin wave-int/<N>` succeeds, fetch and create the local tracking branch:

```bash
git fetch origin refs/heads/wave-int/<N>:refs/heads/wave-int/<N>
```

This must run whether or not ownership/tip verification has already passed for a prior materialization within the same run (idempotent — a second fetch when the local ref already matches origin is a no-op fast-forward). This also satisfies `ywc-finish-branch/SKILL.md:91`'s local-ref `--base-branch` precondition when the branch previously existed only on `origin`.

**Mode-mapping**: for the three isolated modes, redirect `ywc-finish-branch`'s `--base-branch` from the real base to `wave-int/<N>`:

| parallel-executor mode | finish-branch invocation |
|---|---|
| `--local-merge` | `--mode local-merge --keep-branch --base-branch wave-int/<N>` |
| `--draft` | `--mode local-merge --keep-branch --defer-push --base-branch wave-int/<N>` |
| `--aggregate-pr` | `--mode local-merge --keep-branch --defer-push --base-branch wave-int/<N>` |
| `--per-task-pr` | unchanged — no `wave-int/<N>`, per-task PR lifecycle targets the real base directly |

No new concurrency mechanism is needed: Step 4e's per-task delivery loop is already sequential (topological order within the wave), so merging multiple tasks onto the shared `wave-int/<N>` target introduces no new race — delivery was single-threaded against base today and stays single-threaded against `wave-int/<N>` under this scheme.

## Promotion (step `4e.6`, after Hardener, before Clean Up)

After Step 4e.5's Hardener returns for a wave that created `wave-int/<N>`, promote it into the base branch **only** when the gate did not block. A fully contract-less wave never created `wave-int/<N>` and is unaffected — it already delivered direct to base at Step 4e.

**A Hardener dispatch failure (`DONE_WITH_CONCERNS`) is not a blocking verdict** — per `SKILL.md:351`'s existing rule, preserved verbatim here, a dispatch failure must still allow promotion.

**On a passing (or dispatch-failed / absent-contract) Hardener:**

```bash
git checkout <base-branch>
git merge --ff-only refs/heads/wave-int/<N>
```

- Succeeds → push (`--local-merge`, immediate) or defer (`--draft` / `--aggregate-pr`, accumulate locally). Stamp `wave-complete` only **after** this succeeds — its existing "refuses while any task is pending" guard in `update-state.py:162-163` is retained unchanged as the promotion precondition.
- **Postcondition**: after the fast-forward, the main checkout's `HEAD` is left on `<base-branch>` — the postcondition the next wave's Step 4a (worktree creation) already assumes when it branches from base. Post-promotion base content is identical to the integration branch, so wave N+1 still branches from base and the cross-wave lineage invariant holds unchanged; lineage changes only *within* a wave, never across waves.

**On fast-forward failure (base advanced during the wave):**

1. Merge base **into** `wave-int/<N>` — never rebase, per `../../references/pr-conflict-resolution.md`:
   ```bash
   git checkout refs/heads/wave-int/<N>
   git merge --no-ff <base-branch> -m "Merge <base-branch> into wave-int/<N>"
   git push origin wave-int/<N>
   ```
   then immediately call `python3 claude-code/skills/scripts/update-state.py wave-int-owner <N> --tip-sha "$(git rev-parse refs/heads/wave-int/<N>)"` (FR-5's second checkpoint — the branch's identity could have shifted here, not just its accumulating content).
2. **Re-run Hardener** against the merged result before retrying promotion. This is a second wave-boundary Hardener dispatch and gets its **own fresh 3 approved Mutation Loop Cap attempts** (`../../references/quality-gates.md` §"Mutation Loop Cap") — a base-merge produces genuinely new content the prior dispatch never measured; giving the re-run 0 attempts left would silently downgrade "re-run Hardener" to inspection-only.
3. **Two-counter attempt bound** — the re-run's mutation attempts and the live-lock retry count are bounded separately:
   - **Mutation Loop Cap**: fresh 3 attempts per dispatch (see above).
   - **Live-lock cap**: a separate per-wave counter, `promotion_retry_count` (via `yw-000036-010`'s `promotion-retry` subcommand), capped at **2**. Exceeding it marks the wave `BLOCKED` with reason `promotion-churn` — distinct from the textual-conflict `BLOCKED` reason below.
   - Worst case: 3 dispatches × 3 mutation attempts = 9 total Hardener attempts per wave, then `BLOCKED`.
4. A **real textual conflict** on the base-merge (step 1) marks the wave `BLOCKED`, preserves the integration branch and every task worktree, and surfaces the conflicting files to the user — no auto-resolution, no force-push.

**On a blocking Hardener verdict** (`hardener_verdict` of `BLOCKED` or `NEEDS_CONTEXT` — after exhausting the above, or an immediate `BLOCKED`/`NEEDS_CONTEXT` with no base-advance): base is left untouched, `wave-complete` is not stamped, the integration branch is preserved, and Step 4g cleanup is skipped for every task in the wave — matching the existing preserved-failure convention, for both values alike.

## `--per-task-pr` carve-out (advisory-only wave-boundary check)

Under `--per-task-pr`, the wave-boundary cross-task-interaction check still **runs** — it is reporting-only, per the rule stated above — but its result is never assigned to `gate_state` (`../../references/quality-gates.md` §9), and never written to `.ywc-run-state.json`. It is recorded as a plain descriptive note in the wave's Completion Report only. Blocking authority for `--per-task-pr` stays concentrated entirely at Step 4c.5 (per-task, pre-PR).

## Step 4i third bucket: tasks-succeeded-but-wave-Hardener-blocking-verdict (`BLOCKED` or `NEEDS_CONTEXT`)

Step 4i's terminal-state audit classifies run outcome into two buckets today (success / preserved failure). Add a third: a wave whose tasks all individually succeeded (`DONE`, already moved to `completed/` by Mark Complete) but whose `wave-int/<N>` promotion has a blocking Hardener verdict — `hardener_verdict` of `BLOCKED` or `NEEDS_CONTEXT`. This bucket must be distinguishable from a fully completed wave — the underlying task directories look identical (all in `completed/`, since Mark Complete runs before the wave-boundary gate) — so key off the wave's `status` / `hardener_verdict` / `integration_branch` state (`.ywc-run-state.json`), never task-directory location alone. The two values carry distinct recovery semantics (see [checkpoint-resume.md](checkpoint-resume.md)'s Resume cases 3 and 4) but share this bucket's audit mechanics identically.
