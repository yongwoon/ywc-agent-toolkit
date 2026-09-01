# Create and Restructure Rules

Read this reference only before creating or restructuring a `ywc-*` skill.
Audit runs remain report-only and must not load it.

## Decide the Smallest Shape

Start from the target's existing files and sibling conventions. Reuse an
existing reference, script, or template before adding one. A new file needs a
specific execution purpose; do not add auxiliary guides, changelogs, or setup
documents. Keep the skill directory in kebab case and retain the `ywc-` prefix.

## Frontmatter and Interface

Codex `SKILL.md` frontmatter contains only `name` and `description`. The
description starts `(ywc) Use when...`, contains Korean, English, and Japanese
user-facing triggers when applicable, and ends with clear anti-triggers. Review
`agents/openai.yaml` after editing: `display_name`, `short_description`, and
`default_prompt` must still describe the final purpose rather than the old text.

## Body Construction

Put the announce line first, then a domain-specific Rationalization Defense
table with at least five concrete shortcuts. Keep executable workflow, audit
safety, validation, and completion checks inline. Link sibling skills by name,
not force-load syntax. Use `N/A — reason` for an intentionally empty considered
section. Keep the body at 500 lines or fewer.

## Progressive Disclosure

Extract a static lookup table, decision tree, vocabulary list, or template when
one inline section exceeds 30 lines. The new resource must be substantive,
directly linked from `SKILL.md`, and at least 30 lines itself. Do not extract
workflow prose merely to reduce activation tokens: the entrypoint must still
tell the agent when to act, what not to do, and how to verify completion.

## RED → GREEN → REFACTOR

First record a representative failure or the existing coverage that protects a
refactor. Then make the smallest rule or wording change that addresses it.
Re-run the scenario, preserve observed constraints, and add a defense only for
an actual loophole. Do not grow the skill around hypothetical edge cases.

## Before Completion

Run the bundled validator for the target skill. Confirm README locales,
references, metadata, and evals where outputs are objectively verifiable. For
a changed public skill purpose, check catalog or routing documentation only when
the repository has an affected entry. Keep generated files on their designated
sync path; never hand-edit a generated package mirror.
