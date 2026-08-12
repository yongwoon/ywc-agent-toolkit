# Context Handoff Wire Contract

This document is the canonical v1 contract for `.ywc-context-handoff.json`.
The file is a local, non-authoritative reconstruction cache for executor
transitions. It never changes, replaces, or grants authority over
`.ywc-run-state.json`, task metadata, worktree state, completion, cleanup, or
worktree deletion.

## Contract boundary

The wire value is one closed JSON object. It must contain exactly these eleven
top-level properties, with no additional properties:

```text
schema_version
executor
run_id
checkpoint_identity
current_unit
next_unit
aggregate_status
verified_commands
artifact_paths
unresolved_status
ownership_boundary
```

`schema_version` is the JSON number `1`, not the string `"1"`.
`executor` is either `sequential` or `parallel`. JSON `null`, booleans,
and numbers are not accepted where a string, object, or array is specified
below. Object member names are case-sensitive and duplicate JSON member names
are invalid.

Every ordinary string is UTF-8, non-empty after validation, and at most 512
characters. The explicitly documented empty `next_unit.id` is the only empty
string; `feature_sha` may be JSON `null` for parallel runs. An artifact path
may be at most 4,096 characters. The contract has no claim field; claims
belong to the separate subagent-status-actions contract.

### Closed nested shapes

Each nested object and array item is closed as well. The exact shape is:

```json
{
  "schema_version": 1,
  "executor": "sequential",
  "run_id": "run-20260812-01",
  "checkpoint_identity": {
    "run_id": "run-20260812-01",
    "unit_id": "000075-010-domain-context-handoff-contract",
    "checkpoint_timestamp": "2026-08-12T01:02:03Z",
    "base_sha": "0123456789abcdef0123456789abcdef01234567",
    "feature_sha": "89abcdef0123456789abcdef0123456789abcdef",
    "worker_shas": []
  },
  "current_unit": {
    "id": "000075-010-domain-context-handoff-contract",
    "kind": "task",
    "status": "in_progress"
  },
  "next_unit": {
    "id": "000075-020-domain-subagent-claim-contract",
    "kind": "task"
  },
  "aggregate_status": {
    "status": "DONE",
    "reason": "validated"
  },
  "verified_commands": [
    {"id": "bash scripts/validate.sh", "status": "pass"}
  ],
  "artifact_paths": ["codex/skills/references/context-handoff.md"],
  "unresolved_status": {
    "status": "none",
    "items": []
  },
  "ownership_boundary": {
    "scope": "context-handoff",
    "writable_paths": ["codex/skills/references/context-handoff.md"],
    "authority": "cache_only"
  }
}
```

The nested keys and value rules are:

| Object | Exact keys and rules |
|---|---|
| `checkpoint_identity` | `run_id`, `unit_id`, `checkpoint_timestamp`, `base_sha`, `feature_sha`, `worker_shas`. `run_id` must equal the top-level value; `unit_id` identifies the current task or wave; the timestamp is an ISO 8601 UTC instant; each applicable SHA is a lowercase 40-character Git SHA. `feature_sha` is required for sequential runs and `worker_shas` is empty; parallel runs set `feature_sha` to `null` and provide one or more worker records. |
| `checkpoint_identity.worker_shas[]` | Exactly `worker_id` and `sha`; `worker_id` is a stable worker/task identifier and `sha` is a lowercase 40-character Git SHA. The array is sorted by `worker_id` and has no duplicates. |
| `current_unit` | Exactly `id`, `kind`, `status`; `kind` is `task` or `wave`; `status` is `pending`, `in_progress`, `completed`, or `blocked`. |
| `next_unit` | Exactly `id` and `kind`; `id` is the next task or wave identifier, and `kind` is `task` or `wave`. Use the empty string only when there is no next unit; it remains bounded and is not a guessed path. |
| `aggregate_status` | Exactly `status` and `reason`; `status` is `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`. `reason` is a bounded rule/status label, never source, transcript, or tool content. |
| `verified_commands[]` | Exactly `id` and `status`; `id` is a bounded command identifier, not shell output or an expanded command log; `status` is `pass` or `fail`. The array is deterministic and duplicate-free. |
| `unresolved_status` | Exactly `status` and `items`; `status` is `none`, `open`, or `blocked`; `items` is a deterministic, duplicate-free array of bounded diagnostic labels. `items` must be empty when status is `none`. |
| `ownership_boundary` | Exactly `scope`, `writable_paths`, and `authority`; `scope` is a bounded run-local scope label; `writable_paths` is a sorted, duplicate-free array of canonical repository-relative paths; `authority` is the literal `cache_only`. |

`artifact_paths` is a sorted, duplicate-free array of canonical repository
relative paths. It may contain only paths to existing regular files in the
declared run scope; it is descriptive and does not grant permission to write
or execute them. A handoff must not add a field merely to represent an optional
value: use the documented empty array, empty string, or `null`.

## Identity and path semantics

The reader first loads the authoritative `.ywc-run-state.json` for the
selected run. A handoff is valid only when all of these identity values match
that checkpoint: top-level and nested `run_id`, current task or wave,
checkpoint timestamp, base SHA, and the applicable feature SHA or complete
per-worker SHA set. Any difference is stale or mismatched, including a
different executor, task scope, wave, branch, or worker set. The handoff is
never used to repair or overwrite the checkpoint.

All repository-relative paths use POSIX `/` separators and are resolved from
the repository root. Reject absolute paths, empty paths, `.` or `..`
segments, backslashes, NULs, URI schemes, drive prefixes, leading `~`, and
any path whose lexical or resolved symlink target escapes the repository root.
Reject non-regular files, missing files, and paths outside the declared root.
Do not normalize an invalid path into an accepted one. The path itself is the
only path authority; no basename reconstruction, current-directory lookup, or
unlabelled prose is allowed.

Run identifiers and unit identifiers are opaque bounded identifiers, not paths:
they must match `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`. A task or wave identifier
must be compared as an exact identifier; prefix, basename, and substring
matches are not identity matches. `checkpoint_timestamp` must be a canonical
UTC instant in `YYYY-MM-DDTHH:MM:SSZ` form, and SHA values must match
`[0-9a-f]{40}` exactly.

## Location and adjacency

The filename is exactly `.ywc-context-handoff.json` and is adjacent to the
authoritative `.ywc-run-state.json`:

| Run | Authoritative state | Handoff location | Cardinality |
|---|---|---|---|
| Root | repository-root `.ywc-run-state.json` | repository root | one |
| Sequential worktree | that worktree's `.ywc-run-state.json` | the same sequential worktree | one |
| Parallel aggregate | repository-root `.ywc-run-state.json` | repository root | exactly one aggregate file |

Parallel workers must not create worker handoff files. A reader rejects a
handoff found in a worker worktree or any other directory. The file is run-local
and ignored; it is not copied into a committed artifact, task metadata,
generated source, or shared worker payload.

## Privacy boundary and rejection model

Validation recursively walks every object and array before any value is
accepted. Reject unknown properties at every depth, duplicate keys, and these
property names wherever they occur (case-insensitive comparison is used for
the privacy list):

```text
transcript
chain_of_thought
generated_source
full_diff
raw_tool_output
raw_response
tool_output
```

Also reject values that attempt to encode those fields under an alternate
nested object, array, or serialized JSON string. `verified_commands` records
only an identifier and `pass`/`fail`; it never records stdout, stderr, exit
output, arguments containing content, or a command transcript. Diagnostics must
contain only a bounded status, field/rule name, candidate count, path digest
when needed, and a bounded reason. Never include rejected content, raw JSON,
response text, tool output, or a full path when the path itself may contain
sensitive data.

The reader treats missing, unreadable, malformed, privacy-violating,
out-of-root, stale, and mismatched files as discard-and-reconstruct cases.
Discard means ignore the file under the existing run-local cleanup convention;
it does not delete or mutate `.ywc-run-state.json`. Reconstruction precedence
is strict:

1. authoritative checkpoint state;
2. the current task's repository `README.md` and then `task.md`;
3. no guessed, inferred, or prose-derived values.

If those sources cannot produce a valid bounded handoff, return the smallest
bounded `NEEDS_CONTEXT` or `BLOCKED` diagnostic and do not invoke a downstream
transition.

## Atomic replacement and recovery

Replacement is one transaction over the handoff cache only:

1. Validate and serialize the complete object deterministically before opening
   the destination.
2. Create a temporary sibling named `.ywc-context-handoff.json.tmp` (or a
   unique name with that exact prefix) in the same directory, using restrictive
   permissions.
3. Write all bytes, flush them, and call `fsync` on the temporary file.
4. `rename` the temporary sibling over `.ywc-context-handoff.json` atomically.
5. Call `fsync` on the parent directory where the platform supports it.

Never write in place, truncate the destination, or use a temporary file in a
different directory. On serialization, write, fsync, rename, or directory
fsync failure, remove only the failed temporary sibling when safe and preserve
the previous valid destination. A failed replacement must not alter checkpoint
state, task metadata, worktree state, completion, cleanup, or deletion state. A
reader encountering a leftover temporary sibling ignores it and follows normal
validation/reconstruction; it never promotes the sibling without a successful
rename transaction.

Writers are idempotent for the same checkpoint identity and deterministic
payload. Readers must tolerate a missing destination after a crash and use the
fallback order above. Tests and failure injection must demonstrate malformed,
stale, mismatched, privacy-violating, and atomic-write-failure recovery.

## Non-authority invariants

- The handoff is never a second checkpoint and never advances a task or wave.
- It cannot authorize completion, cleanup, branch deletion, worktree deletion,
  or a retry.
- It cannot carry a transcript, raw response, raw tool output, generated
  source, full diff, or an unbounded diagnostic.
- It cannot cause a prompt or wait state in non-interactive execution.
- Consumers use it only after strict schema, identity, privacy, and path
  validation; otherwise they reconstruct from authoritative sources.
