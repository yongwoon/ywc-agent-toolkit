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
(`yk-000001-010-name`). Legacy IDs remain readable and countable for legacy
compatibility, but never claim another collaborator's namespace. For a
resolved `yk`, only prefixed candidates matching `^yk-\d{6}-\d{3}-` contribute
to the `yk` maximum. Union candidates from the resolved graph, active tasks,
completed tasks, and corresponding linked-worktree directories. With no owned
prefixed candidate, start at `000001`; preserve `010` as the first sequence.

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

Only after reservation succeeds may generation create the prefixed task names,
write the dependency graph, or persist a preview. Existing legacy names and
references are never renamed.

## Evidence expected from a generator run

Task `Verify` entries for this behavior should name focused contract checks for
config precedence and malformed tiers, linked-worktree active/completed/graph
scans, scoped maximum selection, empty graphs, concurrent reservation races,
and missing-initials `NEEDS_CONTEXT` before artifact-write checks.
