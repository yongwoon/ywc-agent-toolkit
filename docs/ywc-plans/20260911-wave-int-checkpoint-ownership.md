# Wave Integration Branch — Checkpoint Ownership and Tip-SHA Verification

> Status: Draft
> Scale: Medium
> Created: 2026-09-11
> Author: yongwoon (via ywc-plan)
> Spec Reference: `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md` (parent — introduced `wave-int/<N>`); GitHub Issue [#187](https://github.com/yongwoon/ywc-agent-toolkit/issues/187); PR #186 review thread [discussion_r3977401642](https://github.com/yongwoon/ywc-agent-toolkit/pull/186#discussion_r3977401642)

## Global Constraints

- `.ywc-run-state.json` mutations must go through `scripts/update-state.py` — no hand-edited JSON (`claude-code/skills/scripts/update-state.py:1-10` docstring).
- Real textual conflicts on a branch are a 1-attempt, surface-to-user `BLOCKED` situation — never auto-resolve, never force-push (`claude-code/skills/CLAUDE.md` §PR Conflict & Merge-Readiness Resolution).
- `tools/codex-skill` (here: `codex/skills/`) and `claude-code/skills/` are **not auto-synced** — every change lands in both roots by hand (`claude-code/skills/CLAUDE.md` §Codex-skill: Maintained Independently).
- `plugins/ywc-agent-toolkit/skills/` is a generated mirror of **`codex/skills/`**, not `claude-code/skills/` — verified by diff, its `update-state.py` is byte-identical to `codex/skills/scripts/update-state.py`. The correct procedure is always `bash scripts/sync-codex-plugin.sh` followed by `git add -A plugins/ywc-agent-toolkit` after editing `codex/skills/` — never a direct hand-edit under the plugin path. **Known enforcement gap** (not fixed by this spec): `.githooks/pre-commit:24-27`'s guard against a stale plugin mirror only runs when the commit's staged set *also* touches `codex/skills/`, `.codex-plugin/plugin.json`, `scripts/sync-codex-plugin.sh`, `.codex/skills/`, or `scripts/validate.sh` (`:12,20-22`) — a commit staging **only** a hand-edit under `plugins/ywc-agent-toolkit/skills/` is not caught by the hook today. This spec's own procedure (above) avoids the gap by never hand-editing that path, but does not close the hook's gap for other future changes.

## Purpose

PR #186 introduced `wave-int/<N>` integration branches so a Hardener `BLOCKED` verdict can stop a wave's content from reaching base. The branch-reuse check added at that time only asks "does `wave-int/<N>` exist (local or origin)?" — it cannot tell a legitimate same-run resume apart from a **different** execution reusing a wave number whose `wave-int/<N>` was left over `BLOCKED` by a prior run. A later run can silently promote that stale, non-base content once its own Hardener happens to pass. Separately, a branch that exists only on `origin` has no local ref, so a later `ywc-finish-branch --base-branch wave-int/<N>` call fails its local-ref precondition and the delivery ends `NEEDS_CONTEXT`. This spec closes both gaps with a checkpoint-recorded ownership + tip-SHA verification step before any reuse or promotion.

## Scope

- Add `run_id` to `.ywc-run-state.json` (top level), generated once at `init-parallel`.
- Add `integration_branch_owner` and `integration_branch_tip_sha` fields to each wave's checkpoint entry, written whenever this run creates or advances `wave-int/<N>`.
- Add a verification step to the wave-int reuse procedure: before reusing an existing `wave-int/<N>`, compare the current run's `run_id` and the checkpoint's recorded tip SHA against the branch's actual state; block on any mismatch.
- Add origin-only branch materialization: fetch and create a local tracking ref before reuse when `wave-int/<N>` exists only on `origin`.
- Apply the reuse-verification, materialization, and `update-state.py` changes to `claude-code/skills/ywc-parallel-executor` and `codex/skills/ywc-parallel-executor` as two independent hand-edits (per `claude-code/skills/CLAUDE.md` §Codex-skill: Maintained Independently — the two roots are not auto-synced with each other). The `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` mirror is **not** a third hand-edit target: it is produced by running `bash scripts/sync-codex-plugin.sh` after the `codex/skills/` edit lands, per the pre-commit hook's own remedy.
- Update `checkpoint-resume.md` (both roots) to document the new fields and the resume-time ownership check.
- Add regression coverage for: normal reuse (same run, including with intervening per-task merges), ownership mismatch, tip-SHA divergence, branch-missing-but-owned, origin-only reuse, and each of `wave-int-owner`/`wave-int-blocked`/`wave-int-status`'s `die()` error paths.

## Out of Scope

- The other PR #186 deferred item — extending the terminal-state machine with a distinct `NEEDS_CONTEXT` bucket for wave-boundary ambiguity — is a separate architectural question or a separate GitHub issue, not part of this spec.
- No change to `ywc-finish-branch` itself: per the existing `wave-integration-branch.md:41` precedent ("no change to `ywc-finish-branch` itself is needed once the remote ref exists"), materializing the local ref before the call is sufficient — extending to this spec.
- No change to the promotion fast-forward / base-merge-in / Hardener re-run / `promotion_retry_count` logic (`wave-integration-branch.md:54-85`) — ownership/tip-SHA verification runs strictly before that existing sequence, as an additional guard at the reuse decision point, not a replacement for it.
- No change to non-contract-bearing waves (`integration_branch == None`) — they never create or reuse `wave-int/<N>` and this spec does not touch that path.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md:26-32` | Idempotent creation check only tests branch existence (`git rev-parse --verify` OR `git ls-remote`); on exists, reuses unconditionally | Extend: insert ownership + tip-SHA verification between "exists" and "reuse" |
| `claude-code/skills/scripts/update-state.py:97-118` (`cmd_init_parallel`) | Writes `executor`, `mode`, `tasks_dir`, `started_at`, `current_wave`, `waves` — no run identifier field exists today | Extend: add `run_id` generation and write in the same function |
| `claude-code/skills/scripts/update-state.py:57-68` (`save`) | Atomic write (temp file + `os.replace`), stamps `last_checkpoint` — generic, reused unchanged by any new subcommand | Reuse as-is; new subcommand calls `save(state)` exactly like existing ones |
| `claude-code/skills/scripts/update-state.py:207-215` (`cmd_hardener_verdict`) | Established pattern for a subcommand that loads state, finds the wave via `find_wave`, mutates one/two wave fields, saves | Clone this pattern for the new `wave-int-owner` / `wave-int-blocked` / `wave-int-status` subcommands |
| `claude-code/skills/ywc-finish-branch/SKILL.md:91` | Pre-flight step: "Confirm `--base-branch` is reachable (`git rev-parse --verify <base-branch>` succeeds)" — a **local** ref check, no fallback to `origin` | Comply: this spec must materialize a local ref for `wave-int/<N>` before any `ywc-finish-branch --base-branch wave-int/<N>` call, exactly as `wave-integration-branch.md:41`'s "push at creation" already does for the create path |
| `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md:86-94` (Resume with `wave-int/<N>`) | Three resume cases keyed off `pending` / `status` / `hardener_verdict` — no ownership or tip-SHA field exists yet | Extend: same-run resume must pass the new verification trivially since `run_id` and prior tip SHA are already in this run's own state file |
| `claude-code/skills/scripts/update-state.py:218` (`PROMOTION_RETRY_CAP = 2`) | Existing live-lock cap pattern: a module-level constant, checked and incremented in one subcommand | Follow the same "module-level constant, single subcommand" shape if a bounded retry is later needed for materialization failures — not required by this spec's ACs, noted for consistency only |

## Acceptance Criteria

Test seam: `scripts/update-state.py`'s new subcommand (`wave-int-owner`) as the unit boundary, and the wave-integration-branch reuse bash procedure as the integration boundary (git branch state + `.ywc-run-state.json` as the two observables).

- [ ] **AC1 — Same-run resume succeeds unchanged, including after intervening per-task merges**: When a run that already created and pushed `wave-int/<N>` is interrupted after a partial merge (one or more tasks already merged onto `wave-int/<N>` since the last recorded `integration_branch_tip_sha`) and resumed with the same `.ywc-run-state.json`, the reuse check finds `integration_branch_owner == run_id` and confirms `git merge-base --is-ancestor <recorded integration_branch_tip_sha> wave-int/<N>` exits `0` (the checkpoint's recorded tip is an ancestor of the branch's current tip — not necessarily equal to it, since per-task merges advance the branch without updating the checkpoint per FR-5), observable as the wave continuing to merge its remaining `pending` tasks with no `BLOCKED` state and no prompt.
- [ ] **AC2 — Ownership mismatch blocks reuse**: When `wave-int/<N>` exists (local or origin) but the current run's checkpoint has no `integration_branch_owner` recorded for wave `<N>` (a different, prior run created it), the reuse check refuses to merge onto it, observable as wave `<N>`'s `status` set to `BLOCKED` with `reason: "wave-int-ownership-mismatch"` and `blocked_detail` naming the wave number, branch name, and that no owner was recorded for this run.
- [ ] **AC3 — Tip-SHA divergence blocks reuse**: When `wave-int/<N>`'s recorded `integration_branch_tip_sha` in this run's checkpoint is confirmed to still exist (`git cat-file -e` succeeds) but is **not** an ancestor of the branch's actual current tip (`git merge-base --is-ancestor <recorded-sha> wave-int/<N>` exits non-zero — the branch's history diverged from what this run last recorded, e.g. a force-push or a different process's commit), the reuse check refuses to merge, observable as wave `<N>`'s `status` set to `BLOCKED` with `reason: "wave-int-tip-mismatch"` and `blocked_detail` naming the wave number, branch name, recorded SHA, and actual current tip SHA.
- [ ] **AC4 — Origin-only branch is materialized before reuse**: When `wave-int/<N>` exists on `origin` but has no local ref, and ownership + tip-SHA verification pass, the run fetches and creates a local tracking branch before merging any task onto it, observable as `git rev-parse --verify wave-int/<N>` succeeding locally afterward.
- [ ] **AC5 — `ywc-finish-branch` succeeds against a materialized branch**: When AC4's materialization has run, a subsequent `ywc-finish-branch --base-branch wave-int/<N>` call for a task in that wave passes its local-ref precondition check (`SKILL.md:91`), observable as the call proceeding past Pre-flight instead of returning `NEEDS_CONTEXT`.
- [ ] **AC6 — Ownership recorded at every branch-advancing event**: When `wave-int/<N>` is created, or base is merged into it during promotion-conflict handling (`wave-integration-branch.md:70-77`), the run records the resulting tip SHA and its own `run_id` via the `wave-int-owner` subcommand, observable as `.ywc-run-state.json`'s wave entry reflecting the new tip SHA immediately after each such git operation, before the next task's merge or the next promotion attempt begins.
- [ ] **AC7 — `run_id` is present in every parallel run**: When `init-parallel` runs, the resulting `.ywc-run-state.json` contains a non-empty top-level `run_id` string, observable by reading the file immediately after `init-parallel` completes.
- [ ] **AC8 — Both skill roots agree, and the plugin mirror is regenerated, not hand-edited**: When the same reuse scenario (AC1–AC4) is exercised against `claude-code/skills/ywc-parallel-executor` and `codex/skills/ywc-parallel-executor`, both hand-edited roots document and implement identical verification and failure behavior, observable as identical `update-state.py` subcommand behavior (verified by the new regression test running against both copies) and equivalent prose in each root's `wave-integration-branch.md`. Separately, after the `codex/skills/` edit is committed, running `bash scripts/sync-codex-plugin.sh` and committing its output must leave `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` byte-identical to the freshly-synced `codex/skills/ywc-parallel-executor`, observable as `git diff` showing no unexpected divergence. This AC verifies the sync procedure itself, not the pre-commit hook's enforcement of it — see Global Constraints' "Known enforcement gap" note for the hook's actual (partial) coverage.
- [ ] **AC9 — Branch missing but checkpoint claims ownership blocks, never silently re-creates**: When this run's checkpoint has `integration_branch_owner` set for wave `<N>` but `wave-int/<N>` exists neither locally nor on `origin` (deleted after this run created it — manual cleanup, a bug in the Step 4g exclusion, or any other cause), the reuse check refuses to treat this as a fresh "does not exist" case, observable as wave `<N>`'s `status` set to `BLOCKED` with `reason: "wave-int-branch-missing"` and `blocked_detail` naming the wave number, branch name, and the recorded owner/tip-SHA that no longer has a branch to verify against — never a silent re-creation from base.
- [ ] **AC10 — Every new subcommand's own failure paths are covered**: When `wave-int-owner <N> --tip-sha <sha>` or `wave-int-blocked <N> --reason <reason>` is invoked against a state file whose `run_id` is unset, whose `executor` is not `"parallel"`, or against a wave number not present in `waves`, the subcommand exits non-zero via `die()` and writes nothing to `.ywc-run-state.json` — observable independently for each of these two subcommands. `wave-int-status <N>` has no `run_id` precondition (FR-2) — its own die() coverage is limited to the `executor`-mismatch and wave-not-found rows; invoking it against a `run_id`-unset state file succeeds and prints `unset unset` (or the wave's actual recorded values), never `die()`.

## Functional Requirements

### FR-1: Run identifier

`cmd_init_parallel` in `scripts/update-state.py` generates a `run_id` (8 hex characters, `uuid.uuid4().hex[:8]` — collision-irrelevant since it only needs to distinguish concurrent/sequential runs within one project checkout, not survive a distributed namespace) and writes it as a new top-level field in the initialized state, alongside the existing `executor`, `mode`, `tasks_dir`, `started_at`, `current_wave`, `waves` fields. `run_id` is immutable for the life of the run — no subcommand ever modifies it after `init-parallel`, including across a resume (the resumed run reads the same file and therefore the same `run_id`).

### FR-2: Ownership + tip-SHA checkpoint fields

Each wave's dict in `.ywc-run-state.json` gains two optional fields, both absent (key omitted entirely, never set to `null`) until the wave's `wave-int/<N>` is first created: `integration_branch_owner` (string, the `run_id` of whichever run created or last advanced the branch) and `integration_branch_tip_sha` (string, the branch's tip commit SHA immediately after that run's most recent write to it — a **last-known-good checkpoint**, not necessarily the branch's current tip; see FR-3's ancestor-check semantics). A new `scripts/update-state.py` subcommand, `wave-int-owner <N> --tip-sha <sha>`, sets both fields — owner is always read from the state's own `run_id` (never passed as an argument, so a caller cannot accidentally claim ownership on behalf of a different run) — and stamps `last_checkpoint`, following the exact load → `find_wave` → mutate → `save` shape of `cmd_hardener_verdict` (`update-state.py:207-215`).

A second new subcommand, `wave-int-blocked <N> --reason <reason> [--detail <text>]`, sets `wave["status"] = "BLOCKED"` and `wave["reason"] = args.reason`, and when `--detail` is given also sets `wave["blocked_detail"] = args.detail`, then stamps `last_checkpoint` — cloning `cmd_promotion_retry`'s BLOCKED-write shape (`update-state.py:225-229`) with one added optional field. `--detail` is the mechanism that satisfies AC2/AC3/AC9's requirement that the BLOCKED diagnostic name the branch and the recorded/actual SHA(s): the calling bash procedure formats that detail string and passes it verbatim, so the diagnostic content the ACs promise is actually written to `.ywc-run-state.json`, not left as an unenforced prose expectation. FR-3 calls this subcommand for every `BLOCKED` outcome it produces; no reuse-verification failure is ever expressed as a bare prose instruction to "mark the wave BLOCKED" or as a hand-edit of `.ywc-run-state.json`, per this spec's own Global Constraint against hand-edited JSON.

A third new **read-only** subcommand, `wave-int-status <N>`, prints the wave's `integration_branch_owner` and `integration_branch_tip_sha` (or the literal string `unset` for either that is absent) as two space-separated tokens on one line, e.g. `a1b2c3d4 8f3e9c1...` or `unset unset`. This is the canonical read mechanism FR-3's outer step 1 uses — it exists so all roots parse the checkpoint identically (AC8) rather than each root inventing its own `jq`/`python -c` extraction snippet. Unlike `wave-int-owner` and `wave-int-blocked`, `wave-int-status` has **no `run_id` precondition** — it never writes the `run_id`-derived owner field and performs no state mutation, so a state file whose `run_id` is unset (a pre-this-spec checkpoint) is not an error case for it: it prints `unset unset` exactly as it would for a wave that simply never had these fields set. This is what lets FR-3's procedure reach its own AC2 ownership-mismatch branch for that Edge Case instead of failing before step 1 completes.

### FR-3: Reuse verification procedure

`wave-integration-branch.md`'s "Idempotent creation" section (`:26-32`) is rewritten so that discovering an existing `wave-int/<N>` (local or origin) no longer reuses unconditionally, and so that a checkpoint claiming ownership of a branch that no longer exists is never silently treated as a fresh creation. The rewritten procedure:

1. Run `wave-int-status <N>` to read the wave's `integration_branch_owner` / `integration_branch_tip_sha`. This call succeeds even against a pre-this-spec checkpoint with no `run_id` at all (prints `unset unset` per FR-2), so the procedure always reaches step 5.1 below rather than failing before the ownership check runs.
2. Check whether `wave-int/<N>` exists (local or origin), exactly as today's `:26-32` check does.
3. **Owner recorded, branch missing** (`integration_branch_owner` is set but neither a local nor an `origin` `wave-int/<N>` exists) → **AC9**: call `wave-int-blocked <N> --reason wave-int-branch-missing --detail "branch=wave-int/<N> recorded-owner=<owner> recorded-tip=<tip-sha>"`. Do not create a fresh branch under this wave number without operator intervention.
4. **Branch does not exist, no owner recorded** → proceed to fresh creation exactly as today (`:33-39`), then call `wave-int-owner <N> --tip-sha <new-branch-tip-sha>` immediately after `git push origin wave-int/<N>` (**AC6**, creation half).
5. **Branch exists** → verify before reuse:
   1. If `integration_branch_owner` is unset (this run's own checkpoint never recorded creating or touching this branch) → **AC2**: `wave-int-blocked <N> --reason wave-int-ownership-mismatch --detail "branch=wave-int/<N> no owner recorded for run <run_id>"`. Do not merge, do not promote, do not delete the branch.
   2. If `integration_branch_owner` is set but does not equal the current run's `run_id` → same **AC2** outcome (this covers the resumed-with-a-different-state-file edge case identically to a fresh run's collision), with `--detail "branch=wave-int/<N> owner=<recorded-owner> current-run=<run_id>"`.
   3. If owner matches, materialize the local ref if needed (FR-4), then run `git cat-file -e <recorded integration_branch_tip_sha>` to confirm the recorded object still exists locally. If `cat-file` fails (object unreachable — e.g. after an aggressive `gc` or a shallow re-clone of the worktree), this is a git-internal failure, not a content divergence: call `wave-int-blocked <N> --reason wave-int-materialize-failed --detail "branch=wave-int/<N> recorded-sha=<recorded-sha> unreachable: <raw git error>"`, never `wave-int-tip-mismatch`. Otherwise check `git merge-base --is-ancestor <recorded integration_branch_tip_sha> wave-int/<N>`: exit `0` means the checkpoint's last-known-good tip is an ancestor of (or equal to) the branch's current tip — the branch has only advanced through this run's own expected delivery (per-task merges FR-5 deliberately does not checkpoint after) or is unchanged. A non-zero exit means the branch's history diverged from what this run last recorded — **AC3**: `wave-int-blocked <N> --reason wave-int-tip-mismatch --detail "branch=wave-int/<N> recorded=<recorded-sha> actual=<actual-tip-sha>"`.
   4. If the ancestor check passes → reuse exactly as today: merge the wave's remaining `pending` tasks onto it (**AC1**).

This ancestor-check design (rather than exact SHA equality) is what makes AC1's own resume scenario satisfiable: FR-5 deliberately checkpoints only at creation and post-base-merge, so a legitimate in-progress wave's actual branch tip routinely runs ahead of the last recorded `integration_branch_tip_sha` — an equality check would misclassify that gap as a **AC3** divergence on every ordinary resume.

### FR-4: Origin-only branch materialization

Before the ancestor-check comparison in FR-3 step 5.3, if `git rev-parse --verify wave-int/<N>` fails locally but `git ls-remote --exit-code --heads origin wave-int/<N>` succeeds, fetch and create the local tracking branch:

```bash
git fetch origin wave-int/<N>:wave-int/<N>
```

This must run whether or not ownership/tip verification has already passed for a prior materialization within the same run (idempotent — a second `git fetch ... :wave-int/<N>` when the local ref already matches origin is a no-op fast-forward). **AC4**, **AC5**.

### FR-5: Ownership recorded at every branch-advancing event

`wave-int-owner <N> --tip-sha <sha>` is called at both points where `wave-integration-branch.md` currently pushes to `wave-int/<N>`:

- After creation (`:34-39`, immediately following `git push origin wave-int/<N>`).
- After the promotion-conflict base-merge-in (`:70-77`, immediately following `git push origin wave-int/<N>` in that block).

It is **not** called after each per-task merge onto `wave-int/<N>` during normal per-task delivery (`ywc-finish-branch`'s own push, not a `wave-integration-branch.md`-owned push) — recording ownership at every intermediate per-task commit would require threading the subcommand call through `ywc-finish-branch`'s internals, which FR-3's verification does not need: the tip-SHA check only has to detect divergence introduced **outside** this run's own delivery sequence (a different run, or manual tampering), and this run's own per-task pushes are exactly the content this run's tip-SHA record is expected to have advanced past by the time promotion runs. The two recorded checkpoints (creation, post-base-merge) bracket the only two points where the branch's identity — as opposed to its accumulating content — is established or could have shifted.

## Quality Gate Contract

N/A — no quality gate contract (this project does not currently declare CRAP/Mutation thresholds for skill-authoring changes; the existing `update-state.py` codebase has no measured baseline either).

## Module Boundaries

N/A — this spec extends one existing script (`update-state.py`) and two existing reference documents per root; no new module is introduced.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Reliability | The verification check must never silently downgrade a mismatch to a warning — every ownership, tip-SHA, or missing-branch condition is a hard `BLOCKED` via `wave-int-blocked`, matching the existing "never a silent `false`" convention already used for the `has_contract` scan (`wave-integration-branch.md:18`). |
| Backward compatibility | A `.ywc-run-state.json` written by a pre-this-spec run (no `run_id`, no `integration_branch_owner`/`tip_sha` fields) resuming after this change is out of scope for graceful migration — the existing 48-hour staleness check in `checkpoint-resume.md:16` already treats old checkpoints as likely-stale, and a run old enough to predate this field addition is expected to hit that path or be discarded per the existing resume flow, not silently upgraded. |
| Consistency | Both skill roots (`claude-code/`, `codex/`) must produce byte-for-byte-identical `update-state.py` subcommand behavior — verified by running the same regression test file against both copies (AC8). The plugin mirror is a build artifact of `codex/skills/`, not an independently-maintained third copy, so it is out of scope for this row (see Global Constraints and Scope). |
| Concurrency precondition | This spec assumes **single parallel-executor run per checkout at a time**, matching the existing single-`.ywc-run-state.json`-per-checkout design (no locking mechanism exists today for any subcommand). FR-3's read-check-then-`wave-int-owner`-write sequence is not atomic across two genuinely interleaved processes sharing one checkout — two overlapping runs could both pass verification before either records, and the second write would silently clobber the first's tip-SHA. Detecting or preventing overlapping runs (e.g. a lockfile) is out of scope for this spec; it inherits the same precondition every other `update-state.py` subcommand already relies on. |

## Critical Surfaces

N/A — no critical surface. This change affects only the internal orchestration state of the parallel executor (a local file, `.ywc-run-state.json`, already `.gitignore`d) and does not touch authentication, payment, or user data.

## Data Model

N/A — no database schema change. `.ywc-run-state.json` is a flat-file checkpoint, not a database table; its shape is documented in `checkpoint-resume.md`'s "State File Format" section, updated below.

### Updated State File Format (documentation only, not a DB migration)

```json
{
  "executor": "parallel",
  "run_id": "a1b2c3d4",
  "args": "<original arguments>",
  "mode": "local-merge|draft|per-task-pr|aggregate-pr",
  "tasks_dir": "tasks/",
  "current_wave": 0,
  "waves": [
    {
      "wave": 0,
      "tasks": ["<task-1>", "<task-2>"],
      "status": "completed|in_progress|planned|failed|BLOCKED",
      "merged": [],
      "pending": [],
      "integration_branch": "wave-int/0",
      "integration_branch_owner": "a1b2c3d4",
      "integration_branch_tip_sha": "<40-char sha>"
    }
  ],
  "started_at": "<ISO 8601 UTC>",
  "last_checkpoint": "<ISO 8601 UTC>"
}
```

`integration_branch_owner` / `integration_branch_tip_sha` are absent — key omitted entirely, never set to `null` — for a wave whose `integration_branch` is `None`, and remain absent for a contract-bearing wave until Step 4e's first creation call. This matches FR-2's field definition exactly; the two sections describe one representation, not two.

## API Contract

N/A — no HTTP API change. The only "contract" introduced is three new `update-state.py` CLI subcommands:

```
wave-int-owner <N> --tip-sha <sha>
wave-int-blocked <N> --reason <reason> [--detail <text>]
wave-int-status <N>
```

**`wave-int-owner <N> --tip-sha <sha>` behavior:**

| Condition | Result |
|---|---|
| `executor` is not `"parallel"` | `die(f"'wave-int-owner' requires executor='parallel', but state is '{actual}'")` — identical to `require_executor`'s existing message shape (`update-state.py:81-84`) |
| `executor == "parallel"` but `state["run_id"]` unset/empty (state predates FR-1) | `die("state has no run_id — re-run init-parallel (state predates wave-int ownership tracking)")` — a distinct condition and message from the row above; `require_executor` alone does not catch this, since it only checks `executor` |
| Wave `<N>` not found | `die(f"wave {n} not found in state")` — identical to existing `find_wave` |
| Success | Sets `wave["integration_branch_owner"] = state["run_id"]`, `wave["integration_branch_tip_sha"] = args.tip_sha`, calls `save(state)`, prints `f"wave {n}: integration_branch_owner -> {owner}, tip_sha -> {sha}"` |

**`wave-int-blocked <N> --reason <reason> [--detail <text>]` behavior:** identical `executor`/wave-not-found error rows as above; on success sets `wave["status"] = "BLOCKED"`, `wave["reason"] = args.reason`, and `wave["blocked_detail"] = args.detail` when `--detail` was given, calls `save(state)`, prints `f"wave {n}: status -> BLOCKED ({args.reason}) — {args.detail}"` when `--detail` was given, else `f"wave {n}: status -> BLOCKED ({args.reason})"` — cloning `cmd_promotion_retry`'s BLOCKED-write shape (`update-state.py:225-229`) with one added optional field.

**`wave-int-status <N>` behavior:** identical `executor`-mismatch and wave-not-found error rows as `wave-int-owner`'s first and third rows above — but **no `run_id`-unset row**: an unset `run_id` is not an error for this subcommand (it never reads or writes `run_id`), so a `run_id`-unset state file is treated identically to one where `run_id` is set but this wave's owner/tip-sha fields are simply absent. On success prints one line, two space-separated tokens — `integration_branch_owner` and `integration_branch_tip_sha`, each either the recorded value or the literal string `unset` — and does not call `save()` (no checkpoint stamp for a pure read).

## Edge Cases

- **Wave has no `integration_branch` at all (contract-less wave)**: FR-3's verification never runs — the existing `integration_branch is None` short-circuit in `wave-integration-branch.md:24` is unchanged and takes precedence.
- **`wave-int/<N>` exists locally but was never pushed (network failure right after `git checkout -b`, before `git push`)**: this is indistinguishable from "a different run created it locally and crashed before push" from `origin`'s point of view, but the local git repository is shared within one checkout, so the same-run resume case (AC1) still applies as long as `.ywc-run-state.json`'s `run_id` matches — ownership is about *this checkout's run history*, not about push status. Push-at-creation (`wave-integration-branch.md:41`) remains mandatory and unchanged; a wave whose branch exists locally but was never pushed and whose owner matches proceeds to push before any task delivery, exactly as today.
- **Two runs started back-to-back in the same checkout with genuinely different task sets happening to compute the same wave number**: the intent-match guard already in `checkpoint-resume.md:18-33` fires first (different explicit specifier → user is asked to choose resume-vs-discard) before Step 4e's per-wave reuse check is ever reached; this spec's FR-3 is the second line of defense for the case where that guard was bypassed (e.g., auto-detect mode with a coincidentally-overlapping task name) or the state file was deleted between runs so the guard never saw the prior run at all.
- **`git fetch origin wave-int/<N>:wave-int/<N>` fails (network error, branch deleted from origin between the `git ls-remote` check and the fetch)**: treat as an unexpected git failure — call `wave-int-blocked <N> --reason wave-int-materialize-failed --detail "branch=wave-int/<N> <raw git error>"`, no retry loop (this is not the promotion-conflict retry path, which is bounded and documented separately; a materialization failure here has no established retry precedent to reuse and inventing one is out of scope).
- **A wave is resumed after this spec ships, but its checkpoint was written by a pre-this-spec run (missing `run_id`/`integration_branch_owner` entirely)**: per the Backward compatibility NFR, this is treated as an ownership mismatch (AC2) — no owner recorded — which is the safe default (forces a `BLOCKED` + manual decision rather than a silent, potentially-wrong reuse).

## Dependencies

- N/A — no external dependency. Uses only Python's stdlib `uuid` module (new import in `update-state.py`) and existing `git` CLI commands already used elsewhere in the same reference document.

## Open Questions

N/A — none identified. The issue's Acceptance Criteria section fully specifies the required behavior; no product or business decision is outstanding.

## References

- GitHub Issue [#187](https://github.com/yongwoon/ywc-agent-toolkit/issues/187) — source of this spec's requirements, written in Korean; this spec is the English task-generation-ready translation plus the concrete file/line grounding.
- PR #186 review thread [discussion_r3977401642](https://github.com/yongwoon/ywc-agent-toolkit/pull/186#discussion_r3977401642) — original reviewer comment that this issue formalizes.
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md` — parent spec that introduced `wave-int/<N>` and `.ywc-run-state.json`'s current wave schema.

## Amendment Log

### Iteration 1 — 2026-09-11

**Driven by**: ywc-spec-validate DONE_WITH_CONCERNS, 5/6/4 (Critical/Warning/Suggestion) findings
**Signatures**: `completeness:branch-missing-falls-through-to-recreate`, `feasibility:tip-sha-equality-check-false-positives-on-legit-resume`, `code-compatibility:plugin-mirrors-codex-not-claude-code`, `feasibility:blocked-write-has-no-subcommand`, `consistency:none-vs-omitted-key-wording`, `consistency:api-contract-row-conflates-two-die-conditions`, `feasibility:reuse-check-read-mechanism-unspecified`, `completeness:wave-int-owner-error-paths-uncovered`, `code-compatibility:line-citation-off-by-three`, `completeness:no-atomicity-guard-for-interleaved-runs`

> This iteration's largest change is a design revision, not a wording fix: FR-3's tip-SHA comparison moved from exact SHA equality to a `git merge-base --is-ancestor` check, because AC1's own resume scenario (interrupted after a partial merge) is incompatible with FR-5's deliberate choice not to checkpoint after every per-task merge — the equality check would have false-positived `BLOCKED` on the run's own legitimate work. AC1 and AC3 were reworded to match; FR-3 gained a `wave-int-status` read subcommand and a `wave-int-blocked` write subcommand so no step of the procedure requires hand-editing `.ywc-run-state.json`; a new pre-step (AC9) and a new subcommand-error AC (AC10) were added.

| Section edited | What changed | Why |
|---|---|---|
| `## Global Constraints` | Corrected the plugin-mirror provenance claim: mirrors `codex/skills/`, not `claude-code/skills/`, per `.githooks/pre-commit`'s enforcement | Was: "generated mirror of the claude-code root" — factually wrong, verified false by diff |
| `## Scope` | Replaced "apply symmetrically to three roots" with "two independent hand-edits + one regenerated mirror via `scripts/sync-codex-plugin.sh`"; expanded the regression-coverage bullet | Was: implied the plugin path is a third hand-edit target, which the pre-commit hook rejects |
| `## Acceptance Criteria` | Reworded AC1/AC3 to ancestor-check semantics; reworded AC8 to split hand-edited-root parity from mirror-regeneration verification; added AC9 (branch-missing) and AC10 (subcommand error paths) | AC1 was: exact tip-SHA equality, which contradicts the resume scenario the AC itself describes; AC8 was: implied plugin is a third independently-verified copy; AC9/AC10 were previously uncovered gaps |
| `## Functional Requirements` (FR-2, FR-3) | FR-2: reworded field-absence wording to match Data Model section; added `wave-int-blocked` and `wave-int-status` subcommand definitions. FR-3: fully rewritten as a 5-step procedure (was 5-step exists-only procedure) adding the branch-missing pre-step and replacing exact-equality tip-SHA comparison with the ancestor check | FR-2 was: "absent (`None`/unset)" — read as literal JSON `null`, contradicting the Data Model note. FR-3 was: no handling for checkpoint-owned-but-branch-gone; comparison was exact equality, infeasible per AC1 |
| `## Non-Functional Requirements` | Reworded Reliability row to include the missing-branch condition; added a new "Concurrency precondition" row | Reliability row didn't yet name the new `wave-int-branch-missing` condition; concurrency race between FR-3's read and the ownership write was previously unaddressed |
| `## API Contract` | Split the single `wave-int-owner` error row into two distinct `die()` conditions; documented `wave-int-blocked` and `wave-int-status` behavior | Was: one row claiming `require_executor`'s shape covers both the executor-mismatch and missing-`run_id` cases, which it does not |
| `## Data Model` | Reworded the absent-fields note to state one representation, cross-referencing FR-2 | Was: "not `null`, simply not present as keys" stated the same fact FR-2 stated differently, inviting divergent implementations |
| `## Edge Cases` | Reworded the fetch-failure edge case to route through `wave-int-blocked` instead of a bare "surface BLOCKED" instruction | Duplicate-claim sweep: this site restated the same "how does BLOCKED get written" fact FR-3 now answers via subcommand, needed the same correction |
| `## Existing Constraints Touched` | Corrected `update-state.py:204-215` citation to `:207-215` | Was off by 3 lines relative to FR-2's own citation of the identical function |

### Iteration 2 — 2026-09-11

**Driven by**: ywc-spec-validate DONE_WITH_CONCERNS, 1/3/6 (Critical/Warning/Suggestion) findings
**Signatures**: `completeness:blocked-diagnostic-detail-never-actually-written`, `feasibility:ancestor-check-cant-distinguish-git-error-from-divergence`, `completeness:ac10-only-names-one-of-three-subcommands`, `code-compatibility:global-constraints-overstates-hook-coverage`

> This iteration closes the gap between what the Acceptance Criteria *promise* (a BLOCKED diagnostic naming branch and SHA) and what the API Contract's subcommands actually *write* — `wave-int-blocked` gained an optional `--detail` field so the promised content has a real place to land, and every FR-3 call site now shows its exact `--detail` string.

| Section edited | What changed | Why |
|---|---|---|
| `## Global Constraints` | Added a "Known enforcement gap" note stating the pre-commit hook's plugin-sync guard only fires when the staged set also touches `codex/skills/` or a short list of other paths — a plugin-only hand-edit is not caught today | Was: implied the hook universally rejects any plugin-path change, which is false — the guard has an early-exit condition the prior wording never named |
| `## Acceptance Criteria` (AC2, AC3, AC8, AC9, AC10) | AC2/AC3/AC9 now say `blocked_detail` instead of a bare "diagnostic naming"; AC3 adds the `git cat-file -e` precondition; AC8 clarifies it verifies the sync procedure, not hook enforcement; AC10 broadened from `wave-int-owner`-only to all three subcommands | AC2/AC3/AC9 previously promised diagnostic content with no subcommand field to hold it; AC8 implied the hook enforces what it doesn't; AC10 left two of three new subcommands' error paths untraceable to any AC |
| `## Functional Requirements` (FR-2, FR-3) | FR-2: `wave-int-blocked` gained `--detail`; explained its purpose. FR-3: steps 3/5.1/5.2/5.3 each now pass an explicit `--detail` string; step 5.3 gained a `git cat-file -e` existence check before the ancestor-check, routing a missing-object error to `wave-int-materialize-failed` instead of `wave-int-tip-mismatch` | FR-2 was: `wave-int-blocked` had no field for the diagnostic content ACs require. FR-3 was: no step passed any detail to `wave-int-blocked`; the ancestor-check's binary branching conflated "diverged" with "git-internal failure" |
| `## API Contract` | Updated the `wave-int-blocked` subcommand signature and behavior row to include `--detail`/`blocked_detail` | Was: no `--detail` parameter existed, so the behavior described didn't yet support what FR-3's rewritten steps now call it with |
| `## Edge Cases` | Duplicate-claim sweep: added `--detail` to the fetch-failure edge case's `wave-int-blocked` call | Same "no detail parameter existed yet" fact as the API Contract row, restated at this second site |

### Iteration 3 — 2026-09-11

**Driven by**: ywc-spec-validate DONE_WITH_CONCERNS, 1/0/0 (Critical/Warning/Suggestion) findings
**Signatures**: `completeness:ac10-broadening-created-contradiction-with-legacy-checkpoint-edge-case`

> Iteration 2's own fix (broadening AC10 to cover `wave-int-status`'s `run_id`-unset die() path) directly contradicted a pre-existing Edge Case entry: a legacy checkpoint missing `run_id` was promised a graceful `BLOCKED` (AC2) outcome, but with `wave-int-status` dying first in FR-3 step 1, the procedure would hard-crash before ever reaching that branch. The fix removes `wave-int-status` from the `run_id`-unset die() set entirely — it is a pure read with no actual need for `run_id` — rather than special-casing FR-3's call order, since the read genuinely has no precondition to violate.

| Section edited | What changed | Why |
|---|---|---|
| `## Functional Requirements` (FR-2) | Added an explicit statement that `wave-int-status` has no `run_id` precondition and explained why (pure read, no mutation) | Was: silent on this, letting AC10's broadening (Iteration 2) apply the same die() rule to all three subcommands including this one |
| `## Functional Requirements` (FR-3) | Step 1 gained a clarifying sentence that `wave-int-status` succeeds even against a `run_id`-unset checkpoint, which is what lets the procedure reach step 5.1's AC2 branch | Was: silent on why step 1's unconditional call doesn't fail for the pre-spec-checkpoint Edge Case |
| `## Acceptance Criteria` (AC10) | Rescoped the `run_id`-unset die() row to `wave-int-owner`/`wave-int-blocked` only; `wave-int-status`'s AC10 coverage is now explicitly limited to the executor-mismatch/wave-not-found rows | Was: named all three subcommands under the same `run_id`-unset die() behavior, contradicting the Edge Case entry this iteration reconciles against |
| `## API Contract` | `wave-int-status`'s behavior row no longer lists a `run_id`-unset error condition | Was: "identical executor/wave-not-found error rows as above" ambiguously could be read as including `wave-int-owner`'s `run_id`-unset row too; now explicit that only two of `wave-int-owner`'s three rows carry over |
