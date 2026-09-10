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

**Idempotent creation.** Before creating `wave-int/<N>`, check whether it already exists (locally or on `origin`):

```bash
git rev-parse --verify wave-int/<N> 2>/dev/null || git ls-remote --exit-code --heads origin wave-int/<N> >/dev/null 2>&1
```

- **Exists** → reuse it. Merge the wave's remaining `pending` tasks onto it exactly as if the run had never stopped — this is what makes a partial-merge interruption safe to resume (see `checkpoint-resume.md`'s partial-merge case).
- **Does not exist** → branch it from the current base:
  ```bash
  git checkout <base-branch>
  git pull origin <base-branch>
  git checkout -b wave-int/<N>
  git push origin wave-int/<N>
  ```

**Push at creation is mandatory.** `wave-int/<N>` is pushed to origin immediately at creation, before any task's `ywc-finish-branch` call runs against it. `ywc-finish-branch`'s `local-merge` sequence (`SKILL.md:218-226`) runs `git pull origin <base-branch>` unconditionally per task, which fails with `fatal: couldn't find remote ref` against a local-only branch. No change to `ywc-finish-branch` itself is needed once the remote ref exists — this generalizes `ywc-sequential-executor/references/aggregate-pr.md:30,34-35`'s `WORK_BRANCH` push-at-creation precedent from a run-level branch to a wave-level one.

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
git merge --ff-only wave-int/<N>
```

- Succeeds → push (`--local-merge`, immediate) or defer (`--draft` / `--aggregate-pr`, accumulate locally). Stamp `wave-complete` only **after** this succeeds — its existing "refuses while any task is pending" guard in `update-state.py:162-163` is retained unchanged as the promotion precondition.
- **Postcondition**: after the fast-forward, the main checkout's `HEAD` is left on `<base-branch>` — the postcondition the next wave's Step 4a (worktree creation) already assumes when it branches from base. Post-promotion base content is identical to the integration branch, so wave N+1 still branches from base and the cross-wave lineage invariant holds unchanged; lineage changes only *within* a wave, never across waves.

**On fast-forward failure (base advanced during the wave):**

1. Merge base **into** `wave-int/<N>` — never rebase, per `../../references/pr-conflict-resolution.md`:
   ```bash
   git checkout wave-int/<N>
   git merge --no-ff <base-branch> -m "Merge <base-branch> into wave-int/<N>"
   git push origin wave-int/<N>
   ```
2. **Re-run Hardener** against the merged result before retrying promotion. This is a second wave-boundary Hardener dispatch and gets its **own fresh 3 approved Mutation Loop Cap attempts** (`../../references/quality-gates.md` §"Mutation Loop Cap") — a base-merge produces genuinely new content the prior dispatch never measured; giving the re-run 0 attempts left would silently downgrade "re-run Hardener" to inspection-only.
3. **Two-counter attempt bound** — the re-run's mutation attempts and the live-lock retry count are bounded separately:
   - **Mutation Loop Cap**: fresh 3 attempts per dispatch (see above).
   - **Live-lock cap**: a separate per-wave counter, `promotion_retry_count` (via `yw-000036-010`'s `promotion-retry` subcommand), capped at **2**. Exceeding it marks the wave `BLOCKED` with reason `promotion-churn` — distinct from the textual-conflict `BLOCKED` reason below.
   - Worst case: 3 dispatches × 3 mutation attempts = 9 total Hardener attempts per wave, then `BLOCKED`.
4. A **real textual conflict** on the base-merge (step 1) marks the wave `BLOCKED`, preserves the integration branch and every task worktree, and surfaces the conflicting files to the user — no auto-resolution, no force-push.

**On a blocking Hardener verdict** (after exhausting the above, or an immediate `BLOCKED` with no base-advance): base is left untouched, `wave-complete` is not stamped, the integration branch is preserved, and Step 4g cleanup is skipped for every task in the wave — matching the existing preserved-failure convention.

## `--per-task-pr` carve-out (advisory-only wave-boundary check)

Under `--per-task-pr`, the wave-boundary cross-task-interaction check still **runs** — it is reporting-only, per the rule stated above — but its result is never assigned to `gate_state` (`../../references/quality-gates.md` §9), and never written to `.ywc-run-state.json`. It is recorded as a plain descriptive note in the wave's Completion Report only. Blocking authority for `--per-task-pr` stays concentrated entirely at Step 4c.5 (per-task, pre-PR).

## Step 4i third bucket: tasks-succeeded-but-wave-Hardener-`BLOCKED`

Step 4i's terminal-state audit classifies run outcome into two buckets today (success / preserved failure). Add a third: a wave whose tasks all individually succeeded (`DONE`, already moved to `completed/` by Mark Complete) but whose `wave-int/<N>` promotion is Hardener-`BLOCKED`. This bucket must be distinguishable from a fully completed wave — the underlying task directories look identical (all in `completed/`, since Mark Complete runs before the wave-boundary gate) — so key off the wave's `status` / `hardener_verdict` / `integration_branch` state (`.ywc-run-state.json`), never task-directory location alone.
