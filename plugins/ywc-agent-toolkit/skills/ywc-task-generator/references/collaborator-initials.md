# Collaborator Initials

Task generation uses one validated collaborator namespace for newly allocated
task phases. Initials are machine-facing identifiers and must match
`^[a-z0-9]{2,4}$`; preserve the supplied value exactly after validation.
Uppercase, whitespace, punctuation, empty values, and values outside the
length bound are invalid. Never lowercase or otherwise repair an invalid
explicit value.

## Resolution order

Resolve initials before reading a graph, scanning task directories, compacting
a graph, reserving a phase, or writing a preview/task artifact:

1. Explicit `--initials <value>`.
2. Project `.codex/ywc.json` `initials`.
3. User `~/.codex/ywc.json` `initials`.
4. In interactive mode only, derive a candidate from `git config user.email`
   (the local-part before `@`, reduced to lowercase alphanumeric characters) or
   `git config user.name` (the first lowercase alphanumeric characters), show
   the candidate, and ask for one confirmation. Persist only a confirmed,
   validated value through `ywc-setup`.

Malformed or unsupported config tiers are skipped, just as with language
resolution. A malformed higher-priority tier must not hide a valid lower tier,
and it must not be overwritten as a side effect of generation.

Interactive derivation is only a proposal. If Git identity is missing, or its
derived candidate is empty or fails `^[a-z0-9]{2,4}$`, do not auto-fill,
normalize, or persist it: ask the user to provide a valid lowercase value. An
empty confirmation is invalid and keeps the run unresolved; a rejected or
invalid replacement is re-prompted within the bounded interaction, while
non-interactive mode never derives or prompts and returns `NEEDS_CONTEXT`.

Non-interactive generation with no explicit or cached valid initials returns
`NEEDS_CONTEXT` and names `--initials` (or the missing config value). It must
return before graph compaction, linked-worktree scans, reservation attempts,
preview writes, task-directory creation, or dependency-graph writes.

## Scoped allocation

Resolve `--tasks-dir` to a normalized repository-relative path. Reject an
absolute path, `..` escape, symlink escape, or a path that cannot be mapped
below the invoking repository. For each record from `git worktree list
--porcelain`, inspect the same repository-relative tasks path below that
worktree. Report an inaccessible or mismatched corresponding source as a
concern; do not silently treat it as empty. Stop with `NEEDS_CONTEXT` if the
path would escape the repository.

Parse both legacy IDs (`000001-010-name`) and prefixed IDs
(`yk-000001-010-name`). New numbering is **initials-scoped**, not a global
maximum: for a resolved `yk`, only prefixed candidates matching
`^yk-\d{6}-\d{3}-` contribute to the `yk` maximum. Legacy IDs remain readable
and countable for compatibility, but never claim or advance a collaborator's
prefixed namespace. Union candidates from the resolved graph, active tasks,
completed tasks, and corresponding linked-worktree directories. With no owned
prefixed candidate, start at `000001`; preserve `010` as the first sequence.

Do not apply a legacy-global-maximum-plus-one rule to prefixed allocation. A
legacy-only repository therefore starts the first resolved namespace at
`<initials>-000001-010-...`, even when legacy IDs have larger numbers. This
keeps the namespace rule deterministic and prevents an unowned legacy ID from
silently consuming another collaborator's counter.

## Common-Git exclusive transaction

The reservation ref alone prevents two invocations from consuming the same
ref; it does **not** prevent lost updates to the shared dependency graph. The
generator therefore requires one exclusive lock rooted in the repository's
common Git directory. The lock is a repository-wide generator lock shared by
all linked worktrees (not a per-initials lock and not a worktree-private
`.git` lock).

The lock covers this complete critical section, in this order:

1. Scan the resolved graph, active/completed task directories, and linked
   worktree sources.
2. Select the next candidate using the initials-scoped maximum.
3. Compare-and-create the candidate reservation ref.
4. Write the complete task artifact batch and dependency-graph update while
   holding the same lock.

Do not release the lock between scan, reservation, and graph/artifact writes.
If reservation creation collides, keep the lock, select the next candidate,
and retry. If any complete-batch write fails, report the failure while the
reservation remains consumed; never unlock and retry a partial graph update as
if the transaction had completed. A future implementation may use a portable
atomic lock primitive (for example, an exclusive lock directory or a
platform-supported Git-common-dir lock helper), but it must provide this
whole-section mutual exclusion and bounded stale-lock recovery. The contract
is not satisfied by distinct refs alone.

## Durable reservation

Before creating any task directory or graph/preview artifact, reserve the
candidate using the repository common Git directory (not a worktree-private
`.git` path):

```text
refs/ywc/task-phase/<initials>/<phase>
```

Use Git's compare-and-create operation with the all-zero object ID as the
expected old value and a fixed non-zero reservation value. A failed create is
a collision: retain the existing ref, advance to the next candidate, and
retry with a bounded limit. If the common Git directory cannot be determined
or the bounded retry limit is exhausted, return a deterministic conflict and
write no duplicate task directory. Reservations are never released during
normal operation; they are the durable consumed-phase ledger.

Only after reservation succeeds, and while the common-Git exclusive lock is
still held, may generation create the prefixed task names, write the complete
dependency graph, or persist a preview. A preview-only operation follows the
same scan/selection/reservation ordering if it consumes a phase; a
`NEEDS_CONTEXT` result consumes neither a reservation nor an artifact path.
Existing legacy names and references are never renamed.

## Evidence expected from a generator run

Task `Verify` entries for this behavior should name focused contract checks for
config precedence and malformed tiers, invalid/empty interactive derivation,
safe repository-relative task paths, linked-worktree active/completed/graph
scans, scoped maximum selection including empty graphs, concurrent distinct
reservations, collision retry, and missing-initials `NEEDS_CONTEXT` before
artifact-write checks. The fixture must also prove the lock spans the full
scan-to-graph-write transaction rather than merely proving distinct refs.
