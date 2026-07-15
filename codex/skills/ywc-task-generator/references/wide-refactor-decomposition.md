# Wide Refactor Preview Contract

This reference defines the canonical identity fields for preview approval and
the metadata that must invalidate a previously approved preview.

## Canonical Preview Identity

The preview identity binds the following fields together:

- `spec_path` — project-relative `docs/...` spec input
- `tasks_dir` — the target task output root
- `lang` — resolved output language
- `mode` — `human` or `llm`
- `preview_path` — persisted preview artifact path
- `preview_revision` — monotonic revision label for the persisted preview
- `preview_digest` — hash over the approved preview identity + task rows

If any field above changes, the preview is a different artifact and cannot be
consumed by `--approve-preview`.

## Safe Path Rules

- `--spec` is mandatory for any persisted preview or task write path.
- `--spec` must be repository-relative, must stay under `docs/`, and must not
  resolve through `..` traversal or symlink escape.
- `--preview-path` must be repository-relative Markdown and stay under
  `docs/ywc-plans/` unless the project defines another safe root explicitly.
- Absolute paths, parent-directory escape, symlink escape, and non-Markdown
  preview paths are rejected before any artifact write.

## Two-Phase Flow

1. `--preview-only` decomposes the spec once and writes only the canonical
   preview artifact.
2. `--approve-preview` reuses that persisted preview without re-decomposing the
   spec.
3. The approved call must match `spec_path`, `tasks_dir`, `lang`, `mode`,
   `preview_path`, `preview_revision`, and `preview_digest`.
4. Missing preview, stale digest, mismatched identity, or unsafe paths return
   `NEEDS_CONTEXT` before task directories are written.

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
