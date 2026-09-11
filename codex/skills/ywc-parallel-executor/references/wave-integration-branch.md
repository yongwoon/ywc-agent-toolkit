# Wave Integration Branch (`wave-int/<N>`) — Lifecycle, Promotion, Conflict Handling

> Tier-3 reference extracted from `SKILL.md`. Linked from Step 4e's `> **Action required**` directive. Implements FR-1, FR-2, FR-4, FR-7 of `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md` for the codex root.

## Why this exists

Today, Step 4e delivers every wave task directly into the base branch and stamps `wave-complete`, then the wave-boundary Hardener aggregation runs against the already-merged base — too late for an `enforced`-tier `BLOCKED` outcome to prevent anything reaching base. The fix moves the merge *target* to a wave-scoped integration branch and gates promotion of that branch into base on the wave-boundary aggregate outcome.

**The rule**: an isolation branch can only protect state whose point-of-no-return sits after the gate. **The consequence**: `--per-task-pr` reaches its point-of-no-return at `gh pr merge --delete-branch`, once per task, inside the wave — no branch topology can move that behind the wave boundary. So `wave-int/<N>` applies only to `--local-merge`, `--draft`, and `--aggregate-pr`. Under `--per-task-pr` the wave-boundary aggregation still runs, but it stays what it already is today — reporting authority only, never gating promotion (there is no promotion step for `--per-task-pr`, since each task already merged individually via `gh pr merge` in (a)). Blocking authority for `--per-task-pr` stays concentrated entirely at 4c.5, which already runs per-task before PR creation.

## Contract-bearing wave scan (Pre-flight, before `init-parallel`)

`init-parallel`'s only input is the `--waves` JSON array (task names only) — it has no access to any task's declared Quality Gate Contract tier. Before calling `init-parallel`, compute a per-wave `has_contract` boolean:

1. For each wave, read every member task's declared Quality Gate Contract tier from its task-directory spec/README.
2. OR across the wave's tasks against the exact `N/A — no quality gate contract` sentinel (`../references/quality-gates.md` §7) — contract-bearing if any task's tier differs from that sentinel (i.e. `report-only`, `advisory`, or `enforced`).
3. Extend the `--waves` entry: `{"wave":1,"tasks":["t-a","t-b"],"has_contract":true}`.
4. **Malformed / missing field / absent task directory** — each of these three cases stops Pre-flight with `NEEDS_CONTEXT`, naming the offending task and the missing/malformed field. Never silently resolve to `false` — that would route a possibly contract-bearing wave direct to base, the exact regression the no-block invariant forbids.

This evaluation happens **once per wave**, during this Pre-flight scan, never re-derived at Step 4e.

## Creation (Step 4e, before per-task delivery)

Step 4e creates `wave-int/<N>` **if and only if** that wave's `integration_branch` field is already non-`None` in `.ywc-run-state.json` (seeded by the Pre-flight scan above via `init-parallel`'s `has_contract` input — see `yw-000036-020`). Step 4e never re-derives the contract check itself. A wave where `integration_branch` is `None` (every task contract-less) delivers direct to base exactly as today — no `wave-int/<N>` is created, and the rest of this document does not apply to that wave.

**Reuse verification (checkpoint ownership + tip-SHA).** Before creating or reusing `wave-int/<N>`, verify ownership rather than reusing unconditionally — a checkpoint claiming ownership of a branch that no longer exists must never be silently treated as a fresh creation, and a different run's stale `BLOCKED` branch must never be silently promoted. The procedure:

1. Run `python3 codex/skills/scripts/update-state.py wave-int-status <N>` to read `integration_branch_owner` / `integration_branch_tip_sha`. This succeeds even against a pre-this-spec checkpoint with no `run_id` at all (prints `unset unset`), so the procedure always reaches step 5 below.
2. Check whether `wave-int/<N>` exists (local or `origin`) — verify against `refs/heads/wave-int/<N>` explicitly rather than the bare short name, since Git resolves ambiguous names by checking `refs/tags/` before `refs/heads/`; a same-named tag would otherwise make `rev-parse --verify` succeed against the wrong ref and skip the remote check entirely:
   ```bash
   git rev-parse --verify refs/heads/wave-int/<N> 2>/dev/null || git ls-remote --exit-code --heads origin wave-int/<N> >/dev/null 2>&1
   ```
3. **Owner recorded, branch missing** (`integration_branch_owner` is set but neither a local nor an `origin` `wave-int/<N>` exists) → call `python3 codex/skills/scripts/update-state.py wave-int-blocked <N> --reason wave-int-branch-missing --detail "branch=wave-int/<N> recorded-owner=<owner> recorded-tip=<tip-sha>"`. Do not create a fresh branch under this wave number without operator intervention.
4. **Branch does not exist, no owner recorded** → branch it from the current base, following the same push-at-creation idiom `codex/skills/ywc-sequential-executor/references/aggregate-pr.md` already uses for `$WORK_BRANCH`:
   ```bash
   git checkout <base-branch>
   git pull origin <base-branch>
   git checkout -b wave-int/<N>
   git push -u origin wave-int/<N>
   ```
   then immediately call `python3 codex/skills/scripts/update-state.py wave-int-owner <N> --tip-sha "$(git rev-parse refs/heads/wave-int/<N>)"`.
5. **Branch exists** → verify before reuse:
   1. If `integration_branch_owner` is unset, or is set but does not equal the current run's `run_id` (read from `.ywc-run-state.json`) → call `python3 codex/skills/scripts/update-state.py wave-int-blocked <N> --reason wave-int-ownership-mismatch --detail "branch=wave-int/<N> owner=<recorded-owner-or-none> current-run=<run_id>"`. Do not merge, promote, or delete the branch.
   2. If owner matches, materialize the local ref if needed (see FR-4 below), then run `git cat-file -e <recorded-tip-sha>`. If this fails (object unreachable), call `wave-int-blocked <N> --reason wave-int-materialize-failed --detail "branch=wave-int/<N> recorded-sha=<recorded-sha> unreachable: <raw git error>"` — never `wave-int-tip-mismatch` for a git-internal failure. Otherwise check `git merge-base --is-ancestor <recorded-tip-sha> refs/heads/wave-int/<N>`: exit `0` (the checkpoint's last-known-good tip is an ancestor of, or equal to, the branch's current tip) → reuse it, merge the wave's remaining `pending` tasks onto it exactly as if the run had never stopped (this is what makes a partial-merge interruption safe to resume — see `references/checkpoint-resume.md`'s partial-merge case). Non-zero exit (history diverged from what this run last recorded) → call `wave-int-blocked <N> --reason wave-int-tip-mismatch --detail "branch=wave-int/<N> recorded=<recorded-sha> actual=<actual-tip-sha>"`.

This ancestor-check (rather than exact SHA equality) is what makes the ordinary resume case above satisfiable: ownership is recorded only at creation and post-base-merge (see below), so a legitimate in-progress wave's actual branch tip routinely runs ahead of the last recorded `integration_branch_tip_sha` — an equality check would misclassify that gap as a divergence on every ordinary resume.

**Push at creation is mandatory.** `wave-int/<N>` is pushed to origin immediately at creation, before any task's `ywc-finish-branch` call runs against it. `ywc-finish-branch`'s `local-merge` sequence runs `git pull origin <base-branch>` unconditionally per task, which fails against a local-only branch. No change to `ywc-finish-branch` itself is needed once the remote ref exists.

**Origin-only branch materialization (FR-4).** Before the ancestor-check comparison in step 5.2 above, if `git rev-parse --verify wave-int/<N>` fails locally but `git ls-remote --exit-code --heads origin wave-int/<N>` succeeds, fetch and create the local tracking branch:

```bash
git fetch origin refs/heads/wave-int/<N>:refs/heads/wave-int/<N>
```

This must run whether or not ownership/tip verification has already passed for a prior materialization within the same run (idempotent — a second fetch when the local ref already matches origin is a no-op fast-forward). This also satisfies `ywc-finish-branch`'s local-ref `--base-branch` precondition when the branch previously existed only on `origin`.

**Mode-mapping**: for the three isolated modes, redirect `ywc-finish-branch`'s `--base-branch` from the real base to `wave-int/<N>`:

| parallel-executor mode | finish-branch invocation |
|---|---|
| `--local-merge` | `--mode local-merge --keep-branch --base-branch wave-int/<N>` |
| `--draft` | `--mode local-merge --keep-branch --defer-push --base-branch wave-int/<N>` |
| `--aggregate-pr` | `--mode local-merge --keep-branch --defer-push --base-branch wave-int/<N>` |
| `--per-task-pr` | unchanged — no `wave-int/<N>`, per-task PR lifecycle targets the real base directly |

Each of the above applies only to a contract-bearing wave; a contract-less wave omits `--base-branch wave-int/<N>` entirely and targets the real base, unchanged from today.

No new concurrency mechanism is needed: the per-task delivery loop is already sequential (topological order within the wave), so merging multiple tasks onto the shared `wave-int/<N>` target introduces no new race.

## Promotion (step `4e.6`, after the wave-boundary aggregate, before Clean Up)

After the wave-boundary Hardener aggregation returns for a wave that created `wave-int/<N>`, promote it into the base branch **only** when the aggregate outcome under an `enforced` contract is neither `BLOCKED` nor `NEEDS_CONTEXT`. A fully contract-less wave never created `wave-int/<N>` and is unaffected — it already delivered direct to base at Step 4e. Under `report-only` or `advisory`, the aggregate never returns `BLOCKED` against promotion (per their existing tier semantics) — promotion proceeds regardless of `DONE_WITH_CONCERNS`.

**On a non-blocking aggregate outcome:**

```bash
git checkout <base-branch>
git merge --ff-only refs/heads/wave-int/<N>
```

- Succeeds → push (`--local-merge`, immediate) or defer (`--draft` / `--aggregate-pr`, accumulate locally). Stamp `wave-complete` only **after** this succeeds — its existing "refuses while any task is pending" guard in `update-state.py` is retained unchanged as the promotion precondition.
- **Postcondition**: after the fast-forward, the main checkout's `HEAD` is left on `<base-branch>` — the postcondition the next wave's Step 4a (worktree creation) already assumes when it branches from base. Post-promotion base content is identical to the integration branch, so wave N+1 still branches from base and the cross-wave lineage invariant holds unchanged.

**On fast-forward failure (base advanced during the wave):**

1. Merge base **into** `wave-int/<N>` — never rebase, per `../references/pr-conflict-resolution.md`:
   ```bash
   git checkout refs/heads/wave-int/<N>
   git merge --no-ff <base-branch> -m "Merge <base-branch> into wave-int/<N>"
   git push origin wave-int/<N>
   ```
   then immediately call `python3 codex/skills/scripts/update-state.py wave-int-owner <N> --tip-sha "$(git rev-parse refs/heads/wave-int/<N>)"` (FR-5's second checkpoint — the branch's identity could have shifted here, not just its accumulating content).
2. **Re-run the wave-boundary aggregation** against the merged result before retrying promotion. This is a second dispatch and gets its own fresh 3 approved Mutation Loop Cap attempts (`../references/quality-gates.md` §"Mutation Loop Cap") — a base-merge produces genuinely new content the prior dispatch never measured.
3. **Two-counter attempt bound**:
   - **Mutation Loop Cap**: fresh 3 attempts per dispatch (see above).
   - **Live-lock cap**: a separate per-wave counter, `promotion_retry_count` (via `yw-000036-020`'s `promotion-retry` subcommand), capped at **2**. Exceeding it marks the wave `BLOCKED` with reason `promotion-churn` — distinct from the textual-conflict `BLOCKED` reason below.
   - Worst case: 3 dispatches × 3 mutation attempts = 9 total attempts per wave, then `BLOCKED`.
4. A **real textual conflict** on the base-merge (step 1) marks the wave `BLOCKED`, preserves the integration branch and every task worktree, and surfaces the conflicting files — no auto-resolution, no force-push.

**On a blocking outcome (`enforced` + `BLOCKED` or `NEEDS_CONTEXT`)**: base is left untouched, `wave-complete` is not stamped, the integration branch is preserved, and Step 4g cleanup is skipped for every task in the wave — matching the existing preserved-failure convention, for both values alike.

## Step 4i third bucket: tasks-succeeded-but-wave-Hardener-blocking-verdict (`BLOCKED` or `NEEDS_CONTEXT`)

Step 4i's terminal-state audit classifies run outcome into two buckets today (success / preserved failure). Add a third: a wave whose tasks all individually succeeded (`DONE`, already moved to `completed/`) but whose `wave-int/<N>` promotion has a blocking Hardener verdict — `hardener_verdict` of `BLOCKED` or `NEEDS_CONTEXT`. This bucket must be distinguishable from a fully completed wave — the underlying task directories look identical (all in `completed/`, since Mark Complete runs before the wave-boundary gate) — so key off the wave's `status` / `hardener_verdict` / `integration_branch` state (`.ywc-run-state.json`), never task-directory location alone.
