# Wide Refactor Preview Contract

This reference defines the canonical identity fields for preview approval and
the metadata that must invalidate a previously approved preview.

## Canonical Preview Identity

The preview identity binds the following fields together:

- `spec_path` — project-relative `docs/...` spec input
- `tasks_dir` — the target task output root
- `lang` — resolved output language
- `mode` — `human` or `llm`
- `initials` — validated collaborator namespace
- `reserved_phase` — the phase used by the preview task rows
- `phase_reservation_ref` — exact common-Git reservation ref for those initials and phase
- `preview_path` — persisted preview artifact path
- `preview_revision` — monotonic revision label for the persisted preview
- `preview_digest` — hash over every other identity field, including reservation ownership, and task rows

If any field above changes, the preview is a different artifact and cannot be
consumed by `--approve-preview`.

## Safe Path Rules

- `--spec` is mandatory for persisted previews and approved-preview task writes. Direct generation without preview flags retains Step 1 input forms, including inline specs, and does not require `--spec`.
- `--spec` must be repository-relative, must stay under `docs/`, and must not
  resolve through `..` traversal or symlink escape.
- `--preview-path` must be repository-relative Markdown and stay under
  `docs/ywc-plans/` unless the project defines another safe root explicitly.
- Absolute paths, parent-directory escape, symlink escape, and non-Markdown
  preview paths are rejected before any artifact write.

## Two-Phase Flow

1. `--preview-only` selects and reserves a phase under the common-Git lock,
   then writes the preview identity with `initials`, `reserved_phase`, and
   `phase_reservation_ref`; it writes no task directories or dependency graph.
2. `--approve-preview` reuses that persisted preview without re-decomposing or
   selecting a new phase. Under the lock, verify that the exact reservation ref
   still has its fixed non-zero value, matches the preview identity, and that
   the task rows remain collision-free; then reuse the reserved phase and IDs.
   Do not compare-and-create another ref or advance to another phase.
3. The approved call must match every identity field, including `initials`,
   `reserved_phase`, `phase_reservation_ref`, and `preview_digest`.
4. Missing preview, reservation, approval, stale digest, mismatched identity,
   or unsafe paths return `NEEDS_CONTEXT` before task directories are written.
   A rejected consume leaves the existing reservation intact; reservations are
   never released.

## Wide Refactor Invalidation Fields

For wide-refactor previews, approval is invalidated when any generated row
changes one of these fields:

- `Refactor Phase`
- `Batch ID`
- `Depends On`

These fields are part of the preview digest because they affect execution order
and merge safety even when task names remain stable.

## Consume-Only Guarantee

`--approve-preview` is consume-only:

- It does not re-open decomposition choices.
- It does not silently regenerate task rows.
- It writes task artifacts only from the matching persisted preview.
- If the preview no longer matches the current request, it stops and asks for a
  fresh preview approval cycle.
