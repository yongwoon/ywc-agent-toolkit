# yw-000015-010-domain-scaffold-routing

## Purpose
Define the Codex-native routing and behavioral contract for conditional Trend Check research and approval-gated `reference-refresh` in `ywc-project-scaffold`.

## Scope
Update the source `SKILL.md` description, routing, flow, output contract, boundaries, rationalization safeguards, and validation rules while preserving ordinary scaffold behavior and Codex frontmatter.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr1--discriminating-discovery-and-routing` — routing and safeguards
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr2--conditional-trend-check-for-ordinary-scaffold-generation` — Trend Check behavior
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr3--reference-refresh-mode` — refresh proposal and approval boundary
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#data-model--api-contract` — status and output contracts

### Summary
The skill must keep the existing structured scaffold report and fast uncontested small/medium path. Large or explicitly contested requests trigger a sourced `ywc-tech-research --depth 25` comparison whose material deltas are reported as Extras, never silently applied. Reference review is a separate `reference-refresh` mode that infers language from target paths, produces additive diffs, and stops until explicit approval.

### Out of Scope (from spec)
- JavaScript and Go reference content — handled by `yw-000015-020-refactor-scaffold-reference-enrichment`
- Contract fixtures — handled by `yw-000016-010-test-scaffold-contract-evals`
- Plugin synchronization and repository validation — handled by `yw-000017-010-infra-scaffold-sync-validation`
- Claude Code files, project file generation, automatic research edits, new dependencies, and README locale rewrites remain out of scope.

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000016-010-test-scaffold-contract-evals` — asserts the new routing and output contract.
- `yw-000017-010-infra-scaffold-sync-validation` — validates the source and generated package after all changes.

## Key Files
- `codex/skills/ywc-project-scaffold/SKILL.md` — source routing and behavioral instructions.

## Notes
Use the sibling `ywc-tech-research` skill name and its sourced output contract. Keep the normal project boundary intact: the only approved write exception is a later explicit approval to the skill-owned reference files in `reference-refresh` mode.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-project-scaffold/SKILL.md`

### Shared Surfaces
- `ywc-project-scaffold` output status/mode contract shared with its eval fixture.

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n 'reference-refresh|Trend Check|ywc-tech-research|DONE_WITH_CONCERNS|approval' codex/skills/ywc-project-scaffold/SKILL.md`
- `sed -n '1,240p' codex/skills/ywc-project-scaffold/SKILL.md` and review that frontmatter remains exactly `name` and `description`.

## Out of Scope
Do not edit language references, eval JSON, generated plugin files, localized READMEs, or any Claude Code skill.
