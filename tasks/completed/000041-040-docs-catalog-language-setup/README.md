# 000041-040-docs-catalog-language-setup

## Purpose

Users can discover `ywc-setup` and the new language resolution order from repository documentation. This task updates catalog/root documentation without changing the underlying skill behavior.

## Scope

- Add `ywc-setup` to Codex skill catalog documentation.
- Add concise usage examples for project/user language defaults.
- Mention session defaults are unsupported.
- Update root documentation where Codex-only skills are listed or setup guidance belongs.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-ywc-language-setup.md` — FR-7, Scope, Out of Scope, Acceptance Criteria.

### Summary

The feature is not discoverable unless users can find `ywc-setup --scope project --lang ko` and `ywc-setup --scope user --lang ja` in the docs. Documentation should state the resolution order briefly and point to the skill/reference for details. Because this is Codex-only scope, docs must not imply Claude Code support.

### Out of Scope (from spec)

- Creating the `ywc-setup` skill — `000041-010`.
- Wiring existing skills — `000041-020`, `000041-030`.
- Generated marketplace package sync — `000042-010`.

## Dependencies

### Depends On

- `000040-010-docs-codex-language-resolution-reference` — documentation can point to the reference.

### Depended By

- `000042-010-infra-codex-language-setup-validation` — final docs validation and plugin sync.

## Key Files

- `codex/skills/README.md`
- `README.md`
- `README.ko.md`
- `README.ja.md`
- `README.zh.md`
- `README.es.md`

## Notes

- Keep root docs concise; do not duplicate full `language-resolution.md`.
- If root README links are mostly Claude Code oriented, add Codex-only mention in the existing Codex-only area instead of restructuring the whole file.
- Do not edit generated plugin files; final sync belongs to `000042-010`.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only catalog update; verification is markdown presence checks and repository validation.

### Interface Contract

- Contract: docs list `ywc-setup` usage and resolution order.
- Inputs: user reading catalog/root docs.
- Outputs: discoverable invocation examples.
- Error model: N/A.
- Impacted tests: `bash scripts/validate.sh`, targeted `grep`.

### Critical Surface Review

- Review requirement: N/A — docs-only.

### Data Integrity Hardening

- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership

- `codex/skills/README.md`
- `README*.md`

### Shared Surfaces

- Root documentation and Codex skill catalog.

### Conflicts With

- (None identified)

### Parallelizable After

- `000040-010-docs-codex-language-resolution-reference`

### Task Verify

- `grep -q "ywc-setup" codex/skills/README.md`
- `grep -q "ywc-setup" README.md`
- `grep -q ".codex/ywc.json" codex/skills/README.md`
- `grep -q "~/.codex/ywc.json" codex/skills/README.md`

## Out of Scope

- Skill behavior changes.
- Generated plugin package updates.
- Broad README restructuring.
