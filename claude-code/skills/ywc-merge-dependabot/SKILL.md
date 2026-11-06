---
name: ywc-merge-dependabot
version: 1.0.0
description: (ywc) Merge pending Dependabot PRs one by one after CI and safety checks, with a per-PR result summary.
disable-model-invocation: true
category: release
phase: release
requires: []
advisor_budget: 0
allowed tools: Bash, Read
---

# Merge Dependabot Pull Requests

**Announce at start:** "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested."

Safely merge Dependabot PRs with CI verification, conflict resolution, and clear reporting.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "All ecosystems can run in parallel — fire all merges at once without grouping" | No. Within an ecosystem (e.g., multiple npm PRs all touching `package-lock.json`) merges still serialize via GitHub's auto-merge queue. parallel-auto only fans out across non-overlapping ecosystems, not within one. |
| "Mixed-ecosystem PR (touches both `package.json` and `pom.xml`) is fine to auto-merge" | No. Mixed PRs go to a final sequential pass; `--auto` cannot guarantee ordering when a single PR crosses two parallel groups. |
| "Just queue everything with `--auto` and walk away" | The polling loop and final summary are non-optional. Without them users have no audit trail of which PRs failed, why, or whether the queue stalled. |
| "Repo doesn't have auto-merge enabled, fall through silently" | If `parallel-auto` is requested but `gh repo view --json autoMergeAllowed` returns `false`, fall back to sequential mode and tell the user — never pretend the queue is running. |
| "CI is green but lockfile shows different hash, merge anyway" | Lockfile mismatch indicates dirty working state. Stop and rebase the PR first. |
| "Major version bump looks safe, just merge" | Major bumps are always skipped and reported; this skill never merges them. Report them for human review. |
| "Conflicts with main, force-push my own resolution" | Use Dependabot's `@dependabot rebase` comment instead. Hand-resolved conflicts in dep PRs hide breaking changes. |
| "Security mode, but PR has no CVE link" | If `security` mode is requested and CVE/advisory is missing, skip the PR and report it. |
| "All passed, no need for a final summary" | Always emit a per-PR result table (merged / skipped / failed) at the end. |

**Violating the letter of these rules is violating the spirit.** Dependabot velocity is worthless if a bad merge silently breaks main.

## Context

- Repository: !`gh repo view --json nameWithOwner --jq .nameWithOwner`
- Default branch: !`gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

## Mode Selection

This skill supports two orthogonal flags inside `$ARGUMENTS`. Parse the argument string as a set of space-separated tokens.

**Scope flag** — controls which PRs are eligible:

| Token | Scope |
| --- | --- |
| `security` | Security-related Dependabot PRs only |
| _(token absent)_ | All Dependabot PRs |

**Execution flag** — controls how eligible PRs are processed:

| Token | Execution | When to use |
| --- | --- | --- |
| `parallel-auto` | Group eligible PRs by lockfile ecosystem; queue every PR with `gh pr merge --auto`; GitHub serializes within each ecosystem and processes ecosystems in parallel; one final sequential pass clears the `mixed` bucket | Many PRs (≥ 5) across multiple ecosystems (npm + github-actions + python …) where wall-clock CI wait is the bottleneck |
| _(token absent)_ | Sequential — one PR at a time, ascending PR number | Small batches, repos with strict branch protection, or environments where auto-merge is disabled |

Examples:

- `(empty)` → all PRs, sequential (default)
- `security` → security PRs only, sequential
- `parallel-auto` → all PRs, ecosystem-grouped auto-merge
- `security parallel-auto` → security PRs only, ecosystem-grouped auto-merge

Security-related PRs are identified by labels like `security`, PR title containing "security", or Dependabot's security advisory metadata. When in doubt about whether a PR is security-related, check the PR body for CVE references or GitHub Security Advisory links.

**Parallel-auto prerequisite:** before entering parallel-auto mode, verify the repository allows auto-merge:

```bash
gh repo view --json autoMergeAllowed --jq .autoMergeAllowed
```

If the value is `false`, announce the fallback ("Auto-merge is not enabled on this repository — falling back to sequential mode") and proceed as if `parallel-auto` were absent. Never silently skip the queueing and pretend the work is in progress.

Also verify that each PR's own **base branch** has at least one **required** status check. Dependabot PRs may target a branch other than the default one, and `gh pr merge --auto` on a PR that is already mergeable (`CLEAN`/`UNSTABLE`) merges immediately, so without a required check a PR whose CI is still pending would merge before CI finishes.

`baseRefName` is set by the remote, so treat it as hostile input: never paste it into a command line, a shell variable, or a `gh api` path yourself. The bundled script reads it from the PR number and only uses it after it matches `^[A-Za-z0-9._/-]+$`, does not start with `-`, contains no `..`, and passes `git check-ref-format --branch`; it is passed only as a quoted variable to `gh api "repos/{owner}/{repo}/branches/$base/protection/required_status_checks"` and, as a fallback, `gh api "repos/{owner}/{repo}/rules/branches/$base"` (rulesets of type `required_status_checks`):

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/check-base-required-checks.sh" {number}
# last stdout line: CONFIRMED=<0|1> BASE=<validated base, empty when invalid>
# exit 0 = confirmed (at least one required check), 1 = cannot confirm, 2 = usage error
```

If you Read this SKILL.md directly, `${CLAUDE_SKILL_DIR}` is unsubstituted — replace it with the directory containing this SKILL.md; if the script then fails with `No such file or directory`, `can't open file`, or exit `127`, stop with `BLOCKED: unresolved skill path`.

A base branch is confirmed only on exit 0. A 404, a permission error, any other failure, zero required checks, or a `baseRefName` that cannot be read or fails validation means "cannot confirm": that PR is excluded from the `--auto` queue and handled in the Stage 3 sequential pass (Step 3b) instead (report it as `Skipped (no required check confirmed on <base>)` if the sequential pass skips it; use `<base>` only from a `BASE=` value the script printed). If no PR's base branch is confirmed at all, announce the sequential fallback ("No required status checks confirmed on the base branch — falling back to sequential mode") and proceed as if `parallel-auto` were absent.

## Task

### 1. List Dependabot PRs

Retrieve all open PRs created by Dependabot:

```bash
gh pr list --author "app/dependabot" --state open --json number,title,labels,body,baseRefName --limit 100
```

If in **security-only mode**, filter to PRs that match any of:
- Have a `security` label
- Title or body contains "security advisory", "CVE-", "GHSA-", or "vulnerability"
- Created by `dependabot[bot]` with security update metadata in the body

Sort the resulting list by PR number ascending — processing order matters because earlier merges can affect later PRs.

### 2. Pre-Merge Checks

For each PR, run these checks **before** attempting to merge. If any check fails, skip the PR (a `pending` CI status is the one exception in parallel-auto mode, below).

| Check | Skip condition | Skip label |
| --- | --- | --- |
| **Dockerfile FROM change** | PR modifies a `FROM` image version in any Dockerfile | `Skipped (Dockerfile)` |
| **Major version upgrade** | PR bumps a major version (e.g. 2.x → 3.x), which risks breaking changes | `Skipped (Major version upgrade)` |
| **CI status: failed** | A required CI check has failed | `Failed (CI not passing)` |
| **CI status: pending** | Required CI checks are still running or queued (none failed) | parallel-auto with a confirmed base branch: hand to the Stage 1 `--auto` queue; every other case: `Skipped (CI pending)` |

To detect a Dockerfile `FROM` change, match the `FROM` line only inside the hunks of a changed `Dockerfile*` / `*.dockerfile` file — a `FROM` added to a README or shell file must not trigger the skip. The bundled script fetches the patch first so a `gh` failure is reported as unresolved (exit 3), never mistaken for "no match", then scans it by file header:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/detect-dockerfile-from.sh" {number}
# exit 0 = FROM change in a Dockerfile (skip), 1 = none,
# 3 = unresolved (gh failed — never "none"), 2 = usage error
```

Exit 3 skips the PR as `Skipped (Dockerfile check unresolved)` — an unresolved check is never treated as "no `FROM` change".

To detect major version bumps, run the bundled classifier instead of comparing versions by hand — the "leftmost non-zero segment" rule mis-fires easily in the 0.x range (`0.2.0 → 0.3.0` IS breaking, `1.2.0 → 1.3.0` is not), and a wrong call here merges a breaking change to main.

```bash
gh pr list --author "app/dependabot" --state open --json number,title \
  --jq '.[] | "\(.number)\t\(.title)"' \
  | python3 "${CLAUDE_SKILL_DIR}/scripts/detect-major-bump.py"
```

Each output line is one JSON object: `{"number":130,"name":"webpack","from":"4.46.0","to":"5.90.0","major_bump":true,"reason":"..."}`. Treat `"major_bump": true` as the skip condition — major bumps are always skipped, never merged. `"major_bump": null` (group updates, git-sha action bumps, unparseable titles) means the script could not decide — fall back to reading the PR diff and judging manually.

### 2.5. Ecosystem Grouping (parallel-auto mode only)

Skip this step in sequential mode. In parallel-auto mode, classify the eligible PR list by lockfile ecosystem using the bundled script. Resolve the script path relative to this skill folder (the directory containing this `SKILL.md`), not relative to the target repository.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/group-by-ecosystem.py" {pr_numbers...}
```

The script returns single-line JSON of the shape `{"groups": {ecosystem: [pr...]}, "errors": [...]}`. Recognised ecosystems: `npm`, `github-actions`, `python`, `go`, `cargo`, `maven`, `gradle`, `docker`. PRs touching no recognised marker, or markers from two or more ecosystems, land in the `mixed` group.

The grouping serves two purposes:

1. **Audit trail** — the final summary records which ecosystem each PR belonged to and which ones GitHub serialized vs parallelized.
2. **Mixed-bucket isolation** — `mixed` PRs are deliberately held back to a final sequential pass (Step 3b stage 3) so a single PR that crosses two parallel groups cannot race with itself.

Surface the grouping breakdown to the user before merging:

```
Ecosystem grouping (8 PRs eligible):
  - npm:            #201, #205, #207
  - github-actions: #203, #209
  - python:         #204, #208
  - mixed:          #211
```

### 3. Merge Process

Choose the flow based on the execution flag from Mode Selection. Both flows preserve the same safety contract — only the merge invocation and waiting strategy differ.

#### 3a. Sequential Flow (default)

Process PRs one at a time in ascending PR number order. This is important because merging one PR can create conflicts in subsequent PRs.

For each PR that passes pre-merge checks:

```bash
# Record the head CI will verify; anything but a 40-char hex SHA stops here
HEAD_SHA=$(gh pr view {number} --json headRefOid --jq .headRefOid) || HEAD_SHA=""
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "Skipped (head unreadable)"; exit 1; }

# Merge only when the required checks pass (non-zero exit = failed or pending)
gh pr checks {number} --required || { echo "CI not passing"; exit 1; }

# Attempt merge, pinned to the head CI verified
gh pr merge {number} --merge --match-head-commit "$HEAD_SHA"
```

Gate the merge on the exit status of `gh pr checks --required`: a non-zero exit is `Failed (CI not passing)` (failed) or `Skipped (CI pending)` (pending), never a merge. Pin the merge to the recorded head: if Dependabot pushes a new commit between the CI check and the merge, GitHub refuses the merge instead of landing an unverified head. Shell state does not persist between Bash calls, so substitute the literal recorded SHA into the merge command when the CI check runs in a separate call. Output that does not match `^[0-9a-f]{40}$` (empty, `null`, a failed query) means the head is unreadable: skip the PR as `Skipped (head unreadable)` rather than merging without a pin.

If the merge is refused, read `headRefOid` again and apply the same `^[0-9a-f]{40}$` check — an unreadable re-read is `Skipped (head unreadable)`, never a moved head. When a valid re-read differs from the recorded SHA, the head moved: record the new head, re-run the Dockerfile and major-bump checks (Step 2) on it, and restart the CI check on it — at most 2 restarts per PR, then record `Failed (head kept moving)` and move on. When it still matches, the refusal has another cause: record `Failed (merge refused)` with the error. Never retry the merge unpinned.

**If a merge conflict occurs:**

Never hand-resolve a Dependabot PR's conflict — a hand-merged lockfile can mask a
breaking transitive bump (this is the Rationalization Defense rule above). Let
Dependabot regenerate the PR against the fresh base instead:

1. Record the current head (`gh pr view {number} --json headRefOid --jq .headRefOid`),
   then comment `@dependabot rebase` on the PR exactly once (the script below does both) —
   Dependabot rebuilds the branch and lockfile against the current base
2. Poll for the rebase with the bundled bounded, query-first loop below (one Bash call with an
   explicit `timeout: 600000`; up to 9 queries, 60 s apart). The rebase counts as done
   only when `headRefOid` differs from the recorded value **and** `mergeable` is neither
   `CONFLICTING` nor `UNKNOWN`. Empty output, a failed query, or `UNKNOWN` is unresolved — keep
   polling; it is never evidence of a finished rebase. Once done, wait for the rebased
   branch's CI to re-run and pass — bounded to 30 minutes in chunks of at most 540 s
   (`gh pr checks {number} --watch --fail-fast`); past that, report `Failed (CI timeout)`
   and move on
3. Re-run the Dockerfile and major-bump checks (Step 2) on `NEW_HEAD` — the rebase can
   change the diff — then, if CI passes, merge with
   `gh pr merge {number} --merge --match-head-commit "<NEW_HEAD>"` (the literal SHA).
   A refused merge means the head moved: re-read it and restart the checks and CI wait
   on the new head (the same at-most-2-restarts rule as above); never retry unpinned
4. If the loop is exhausted, the new head is still `CONFLICTING`, or CI is red, skip the
   PR and surface it for human review — do not force-push a resolution

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/wait-dependabot-rebase.sh" {number}
# last stdout line: REBASED=<0|1> ATTEMPTS=<n> NEW_HEAD=<sha>
# exit 0 (REBASED=1) → re-check NEW_HEAD, wait for CI on it, then merge pinned with
#   --match-head-commit "<NEW_HEAD>" (step 3)
# exit 1 (REBASED=0) → step 4 (skip + surface for human review) — also returned, before any
#   rebase wait, when the current head cannot be read or the rebase comment cannot be
#   posted; exit 2 = usage error
```

**If CI fails** after conflict resolution or at any point, skip the PR and record the failure.

After each successful merge, note it — the next PR in the queue may now have conflicts caused by this merge.

#### 3b. Parallel-Auto Flow

In parallel-auto mode the client offloads serialization to GitHub's auto-merge queue. The flow has three stages and the client never blocks on per-PR CI manually — GitHub handles rebase and CI orchestration.

**Stage 1 — Queue every non-mixed PR for auto-merge:**

For each ecosystem group's PRs whose base branch is confirmed (exit 0 from the required-check script in Mode Selection; every other PR goes to the sequential pass), queue them all at once — the order across groups does not matter, they are non-conflicting by construction:

```bash
gh pr merge {number} --auto --merge --match-head-commit "<HEAD_SHA>"
```

Record `<HEAD_SHA>` per PR exactly as in 3a (`headRefOid`, must match `^[0-9a-f]{40}$`, else the PR goes to the Stage 3 pass) and write it as a literal. The pin only guards the queueing call; heads Dependabot pushes later are guarded by the confirmed required checks, which GitHub evaluates on the head it actually merges. A refused queue call means the head moved: hand the PR to the Stage 3 sequential pass — never re-queue it unpinned.

This sets the PR to merge automatically as soon as its CI is green and the branch is up to date. PRs sharing a lockfile (same ecosystem) automatically serialize because each merge invalidates the next PR's branch state, and Dependabot rebases the affected PRs; PRs in different ecosystems progress in parallel because GitHub processes them independently.

**Stage 2 — Poll the queue until it drains:**

Track each queued PR's state until it reaches a terminal state with the bundled bounded poller (do not spin in tight retries). One call = one chunk of at most 540 s, so give every call an explicit `timeout: 600000`:

```bash
# First chunk: the 30-minute deadline is computed ONCE here and stored in the state file.
# <state-file> must be a fresh path for this run (e.g. STATE_FILE=$(mktemp)) — --prs with existing state exits 2.
# Shell variables do not persist between Bash calls: print the path once, then write that
# literal path (never "$STATE_FILE") into this and every later chunk call.
python3 "${CLAUDE_SKILL_DIR}/scripts/poll-merge-queue.py" --state <state-file> --prs 101 105 107 203
# Every later chunk: same state file, never new --prs (the deadline is never recomputed).
python3 "${CLAUDE_SKILL_DIR}/scripts/poll-merge-queue.py" --state <state-file>
# stdout: {"done": bool, "deadline": <epoch>, "remaining": [...], "status": {"<pr>": "merged|closed|stalled"}}
# exit 0 = finished (queue drained, or deadline passed and remaining PRs marked stalled)
# exit 3 = chunk ended before the deadline — run the next chunk
# exit 2 = usage error, no usable state, or --prs given while <state-file> already holds state
```

**Chunking:** a single Bash call is capped at 600000 ms, so the poller runs one chunk (`chunk_deadline` = 540 s) per call and persists `deadline`, `remaining`, `rebase_commented`, and `status` to `<state-file>` after every chunk. Each poll issues one `gh pr view --json state,mergeStateStatus` per PR (bounded to 20 s); the 60 s sleep between polls is clamped so it never runs past the chunk. `MERGED` → merged, `CLOSED` → closed, `CONFLICTING`/`DIRTY` → one `@dependabot rebase` comment per PR (recorded only when it posted, so a failed post is retried) and re-queue. Resume condition: exit 3 — run the next chunk with the same `<state-file>`. If the file is missing or unparsable, restart from the PR list with `--prs ... --deadline <original epoch>` when the original deadline is known — never start a fresh 30 minutes. A chunk that ends before the deadline never marks PRs stalled; when the overall deadline passes, the poller marks every remaining PR `stalled` and exits 0 — then run the stalled-PR step below.

PRs that reach `MERGED` are recorded as `Merged`; PRs whose status is `closed` (closed without merging, e.g. superseded by Dependabot) are recorded as `Skipped (closed without merge)`. PRs whose status is `stalled` (still remaining at the deadline) are recorded as `Failed (queue stalled)` so the user can investigate. Before reporting a stalled PR, disable its auto-merge so it cannot merge later unattended: `gh pr merge "$pr" --disable-auto`. If that command fails, still report the PR as `Failed (queue stalled)` and add "auto-merge still enabled" so the user can disable it manually. Do not extend the deadline silently — if the queue genuinely needs more time, the user can rerun the skill.

**Stage 3 — Final sequential pass for the mixed bucket and unconfirmed-base PRs:**

After the parallel queue has drained (Stage 2 returned), process the `mixed` group and every non-mixed PR excluded from the `--auto` queue (base branch not confirmed) using the same logic as Sequential Flow (3a). Mixed PRs run last because earlier merges may have changed the conflict surface they would land in.

### 4. Final Summary

After processing all PRs, report results in this format:

```
## Dependabot Merge Results

Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2), mixed (1)

- ✅ Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- ✅ Merged    (npm)            : #125 Bump lodash from 4.17.20 to 4.17.21
- ✅ Merged    (github-actions) : #129 Bump actions/checkout from 4.1.1 to 4.2.0
- ⏭️ Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- ⏭️ Skipped   (Major version upgrade) : #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed    (queue stalled)  : #132 Bump express from 4.18.0 to 4.19.2 — CONFLICTING after 30 min
- ❌ Failed    (mixed pass)     : #135 Bump aws-sdk + boto3 — manual conflict resolution required

Total: 3 merged / 2 skipped / 2 failed
```

Include:
- Mode line — scope flag + execution flag, so the reader can reproduce the run
- Ecosystem group summary — only when parallel-auto was used; the count tells the reader how many groups GitHub serialized in parallel
- Per-PR result — for parallel-auto, annotate each line with the ecosystem; for sequential, omit the annotation
- If a previous merge affected a subsequent PR, note which PR caused the issue
- Total counts: merged / skipped / failed

## Error Handling

| Error | Action |
| --- | --- |
| `gh` CLI not authenticated | Stop and ask user to run `gh auth login` |
| No Dependabot PRs found | Report "No Dependabot PRs found" and stop |
| Rate limit hit | Wait and retry, or stop and report progress so far |
| Branch protection prevents merge | Skip PR and note the protection rule in the report |

## Notes

- Follow any additional instructions in `$ARGUMENTS`
- Never force-merge or bypass branch protection rules
- If the number of PRs is large (>20), ask the user for confirmation before proceeding. For batches of that size, also recommend `parallel-auto` mode if the eligible PRs span more than one ecosystem
- `parallel-auto` reduces wall-clock time by letting GitHub run the CI cycle for non-conflicting groups concurrently. It does not reduce the *per-PR* CI cost, the safety surface, or the conflict-resolution requirements — it only changes how the queue is orchestrated

## Integration

- **upstream**: None — this skill is triggered directly by the user or a scheduled workflow when Dependabot PRs accumulate
- **downstream**: /ywc-gen-testcase (optional — run after merging dependency updates to verify the updated packages do not break existing test coverage)
