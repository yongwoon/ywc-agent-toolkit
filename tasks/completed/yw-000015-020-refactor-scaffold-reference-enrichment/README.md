# yw-000015-020-refactor-scaffold-reference-enrichment

## Purpose
Enrich the shared JavaScript/TypeScript and Go scaffold references with reusable conventions and the large-service alternative required by the spec.

## Scope
Add shared JavaScript naming and component-logic-colocation guidance with narrow variant links, and add Go Layered/Connect RPC plus `injector/`, `gen/`, and `converter/` convention guidance while preserving existing alternatives and examples.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr4--javascripttypescript-reference-enrichment` — JavaScript reference additions
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr5--go-reference-enrichment` — Go reference additions
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#ac7` — JavaScript acceptance contract
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#ac8` — Go architecture and ownership contract

### Summary
The JavaScript reference gains cross-framework naming exceptions and staged logic colocation, linked from only affected Next.js and Astro variants. The Go reference retains DDD while adding a sibling Layered/Connect RPC layout, precise repository-interface ownership, and generated-code boundaries. These are additive documentation changes; existing examples and variants must remain intact.

### Out of Scope (from spec)
- Skill routing and refresh behavior — handled by `yw-000015-010-domain-scaffold-routing`
- Eval fixtures — handled by `yw-000016-010-test-scaffold-contract-evals`
- Other language references, README locales, Claude Code files, and generated plugin content — handled or excluded by the spec.

## Dependencies
### Depends On
- (None — root task; source reference files are independent of the SKILL.md routing task)

### Depended By
- `yw-000016-010-test-scaffold-contract-evals` — evaluates the completed scaffold contract and reference targets.
- `yw-000017-010-infra-scaffold-sync-validation` — syncs and validates these source references.

## Key Files
- `codex/skills/ywc-project-scaffold/references/javascript.md` — shared naming and colocation sections plus links.
- `codex/skills/ywc-project-scaffold/references/go.md` — Layered/Connect RPC variant and convention rows.

## Notes
Keep reserved Next App Router, informal layout partial, and UI-kit-generated filenames as explicit exceptions. Top-level Go `gen/` is protobuf/Connect output only and never hand-edited; DB generation remains under the DB package.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-project-scaffold/references/javascript.md`
- `codex/skills/ywc-project-scaffold/references/go.md`

### Shared Surfaces
- Language reference anchors consumed by `codex/skills/ywc-project-scaffold/SKILL.md`.

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `rg -n 'Naming Convention|Component Logic Colocation|Go Large \(Layered, Connect RPC\)|injector/|converter/|protobuf/Connect' codex/skills/ywc-project-scaffold/references/javascript.md codex/skills/ywc-project-scaffold/references/go.md`
- `git diff --check -- codex/skills/ywc-project-scaffold/references/javascript.md codex/skills/ywc-project-scaffold/references/go.md`

## Out of Scope
Do not rename existing examples mechanically, remove variants, change unrelated language references, or edit generated marketplace files.
