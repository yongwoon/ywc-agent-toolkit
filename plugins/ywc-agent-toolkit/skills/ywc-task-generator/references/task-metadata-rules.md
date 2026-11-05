# Task Metadata Rules

These rules define the task-generator handoff from a plan or scaffold to an
executor. They supplement [quality-gates.md](../../references/quality-gates.md)
and the parallel-execution metadata rules; the shared quality-gate reference is
the source of truth for field names and allowed values.

## Advisory Model Hint

Exactly one advisory `Model Hint` is required for every task: `economy`, `standard`, or `advanced`, followed by a concise evidence-based rationale tied to scope and criticality.

- `economy`: narrow, clear, non-critical work with evidence that the change follows a known pattern.
- `standard`: ordinary existing-pattern work, or insufficient difficulty evidence to justify another tier.
- `advanced`: architecture judgment or critical-surface work; name the relevant decision or surface in the rationale.

Unclear requirements return `NEEDS_CONTEXT`; raising the tier is not a substitute for clarification.

Preserve current-session model selection, specialist model pins, and installer fallback. Do not pin an effective model ID in task metadata or introduce task-aware runtime routing.
The hint supplies review metadata only; it does not promise executor model selection.
This reference owns the tier definitions independently of the quality-gate packet.

Provenance: adapted from `yongwoon/develop-with-llm` #338 merge
`0622ba580d2ad2bf8c8936726dd400c00752ab3e`,
`tools/codex-skill/skills/ywc-task-generator/{SKILL.md,references/task-metadata-rules.md,references/README.md.template,references/output-and-validation.md}`.
The approved adoption specification FR-1 excludes upstream runtime routing claims.

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
