# Task Metadata Rules

These rules define the task-generator handoff from a plan or scaffold to an
executor. They supplement [quality-gates.md](../../references/quality-gates.md)
and the parallel-execution metadata rules; the shared quality-gate reference is
the source of truth for field names and allowed values.

## Conditional Quality Gate Contract

The packet is opt-in and task-local. Render the complete conditional packet in
both generated `README.md` and `task.md` only when the producer supplied a
complete, validated declaration. When the producer supplied the exact
`N/A — no quality gate contract` sentinel, omit the heading, fields, and
checklist; do not render an empty packet or select a worker.

A declaration with missing, contradictory, unauthorized, unbounded, or
unverifiable metadata returns `NEEDS_CONTEXT` before preview or task-artifact
writes. The generator must not fill fields from repository conventions or
discover a second contract.

## Per-task packet

For an eligible task, project only these sanitized fields:

- `contract_state`: `report-only`, `advisory`, or `enforced`.
- `ownership.production_paths` and `ownership.production_symbols` for Cleaner.
- `ownership.test_fixture_paths` and `ownership.test_fixture_symbols` for Hardener.
- `approved_command_ids` and matching `approved_command_digests` for baseline,
  complexity, and mutation checks. IDs are opaque and never executable text.
- `sanitized_evidence_paths`: one bounded repository-relative file path for each
  authorized evidence artifact; never a glob, directory, or temporary authority.
- `complexity_threshold`, `mutation_target`, and `attempt_cap` (maximum three).
- `residual_survivors` as sanitized references, without equivalence judgments.

Ownership is narrowed to the task's exact changed paths and symbols. The
generator may not broaden it, cross the production/test boundary, or copy raw
commands, output, transcripts, secrets, or full diffs. It also may not emit
placeholder values, inferred digests, invented thresholds, or fabricated
evidence paths. The packet grants no command-execution, staging, commit, push,
PR, merge, or delivery authority.

## Verification and evidence

`task.md` keeps the existing task-specific verification commands separate from
the quality-gate packet. The packet carries command identities and digests only;
it never replaces or fabricates a Task Verify command. Every packet projection
must be checked with targeted contract evals and a JSON/diff inspection before
handoff.
