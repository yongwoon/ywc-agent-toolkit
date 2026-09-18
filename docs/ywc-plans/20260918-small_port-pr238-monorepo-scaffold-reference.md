# Small Plan: Port PR #238 — TypeScript Monorepo (pnpm workspaces) reference for ywc-project-scaffold

## Goal

Add the "TypeScript Monorepo (pnpm workspaces) / TypeScript Monorepo Large (apps + packages)" reference section — already authored and merged upstream in `develop-with-llm` PR #238 — to this repo's Claude Code `ywc-project-scaffold` skill, so agents planning a large-scale TypeScript monorepo (multiple deployable apps + shared packages, or a single backend splitting HTTP/worker processes) have this pattern available here too.

## Why

`develop-with-llm` PR #238 (merged, commit `c273d02c`) added this section to its own `ywc-project-scaffold` skill after discovering the pattern while reviewing a real project's directory design. This repo's `claude-code/skills/ywc-project-scaffold/references/javascript.md` predates that PR and is missing the same section — confirmed by comparing current file structure (TOC ends at Express.js, file ends at the Express Medium code block, 519 lines) against the PR's pre-change diff context, which is identical.

## Out of Scope

- `codex/skills/ywc-project-scaffold/references/javascript.md` — the Codex skill root is not covered by this request (target is Claude Code only per user instruction); it may be ported separately later as its own decision.
- `plugins/ywc-agent-toolkit/skills/ywc-project-scaffold/` — this directory is generated from `codex/skills/` by `.githooks/pre-commit` (`plugins/ywc-agent-toolkit/skills is generated from codex/skills`); it is untouched by this change and requires no manual edit.
- Any other section of `javascript.md` (Next.js, NestJS, Astro, Express.js, etc.) — no existing content is edited.
- `SKILL.md`, `README*.md` — no frontmatter or skill-behavior change; this is a references-file-only addition.
- Introducing this pattern as a scaffold *template* (e.g. a generator script) — this change is documentation/reference only, matching the upstream PR's scope.

## Done When

- `claude-code/skills/ywc-project-scaffold/references/javascript.md` contains the new TOC entries and the full "TypeScript Monorepo (pnpm workspaces)" / "TypeScript Monorepo Large (apps + packages)" section, byte-identical in content to the upstream PR #238 diff (Claude Code skill-root variant).
- `bash scripts/validate.sh` passes (136/136 checks, matching the standard for this repo's skill-structure validation).
- No other file in the repo is modified.

## Existing Constraints Touched

- `.githooks/pre-commit:24` — blocks any staged change under `plugins/ywc-agent-toolkit/skills/` with "generated from codex/skills"; this plan touches only `claude-code/skills/`, so the hook is not triggered and no plugin regeneration is needed.
- `claude-code/skills/ywc-project-scaffold/references/javascript.md` current structure (verified this session): TOC block ends with `- [Express.js](#expressjs)` / `  - [Express Medium](#express-medium)` at lines 20–21; file content ends at line 519 with the Express Medium code fence. The new content is appended after this point, matching the upstream PR's insertion point exactly.
- `scripts/validate.sh` (`check_skill_dir`) validates `SKILL.md` frontmatter and required README locale files per skill directory — it does not parse `references/*.md` content, so this change carries no risk of failing that specific check; the run is still required as the repo's standard verification gate.

## Files to Touch

- `claude-code/skills/ywc-project-scaffold/references/javascript.md` — the only file changed.

## Interfaces

N/A — single file, no shared function/type signature crosses files in this change.

## Implementation Steps

- [ ] In `claude-code/skills/ywc-project-scaffold/references/javascript.md`, insert two new TOC lines immediately after `  - [Express Medium](#express-medium)` (currently line 21):
  ```
  - [TypeScript Monorepo (pnpm workspaces)](#typescript-monorepo-pnpm-workspaces)
    - [TypeScript Monorepo Large (apps + packages)](#typescript-monorepo-large-apps--packages)
  ```
- [ ] Append the following section verbatim to the end of the file (after the existing Express Medium code fence, currently ending at line 519), exactly as merged in upstream PR #238's `tools/claude-code/skills/ywc-project-scaffold/references/javascript.md` diff (captured this session via `gh pr diff 238 --repo yongwoon/develop-with-llm`):

  ```
  ---

  ## TypeScript Monorepo (pnpm workspaces)

  ### TypeScript Monorepo Large (apps + packages)

  Multi-app pnpm workspaces monorepo. Separates deployable applications from reusable packages, and isolates external SDK dependencies behind dedicated packages. Applies at Large scale — multiple deployable apps sharing business logic, or a single backend that must split HTTP/worker processes without a microservices rewrite.

  project-root/
  ├── apps/
  │   ├── web/
  │   │   └── src/
  │   │       ├── app/                   # bootstrap, router, provider, feature registry
  │   │       ├── features/              # per-feature screens
  │   │       └── shared/                # UI parts, API client, generic utilities
  │   └── server/
  │       └── src/
  │           ├── entrypoints/           # api.ts, worker.ts - one file per process
  │           ├── modules/<module>/      # transport-facing routes/handlers per domain
  │           ├── http/                  # framework init, shared plugins, error mapping
  │           ├── jobs/<job-name>/       # background job handlers
  │           └── composition/           # DI wiring at process startup
  ├── packages/
  │   ├── contracts/                     # HTTP/event schema, DTOs, generated client boundary
  │   ├── core/                          # business rules, use cases, ports, state transitions
  │   ├── db/                            # ORM schema/migrations, repository implementations
  │   ├── <external-sdk>/                # provider-specific SDK adapters, isolated behind a port
  │   └── connectors/                    # outbound integration adapters + fakes/contract test kit
  ├── tests/
  │   ├── architecture/                  # forbidden-dependency / single-source rules
  │   ├── contract/                      # API and connector contract tests
  │   ├── integration/                   # DB, job, cross-package integration tests
  │   └── e2e/                           # end-to-end user-flow tests
  ├── package.json
  ├── pnpm-workspace.yaml
  └── tsconfig.base.json

  **Key Points:**

  - `apps/` vs `packages/`: `apps/` holds only what is started and deployed as its own process; `packages/` holds anything shared across 2+ entry points. A single backend can still run HTTP and worker as separate `apps/server/src/entrypoints/*.ts` processes from one codebase, without splitting into microservices yet.
  - `packages/contracts`: the only package with zero dependency on other internal packages - the shared schema/DTO boundary that `apps/*` and `packages/core` consumers build against.
  - External SDK isolation: confine every import of a given external SDK (an agent/LLM provider, a payment gateway, etc.) to one package (e.g. `packages/<external-sdk>/src/providers/<provider>/`) so a provider swap or SDK upgrade touches one location, not every caller.
  - `packages/core` carries no framework or infrastructure imports (no ORM, no HTTP framework, no external SDK) - it depends only on its own ports, and `db` / `<external-sdk>` / `connectors` implement those ports.
  - Root `tests/architecture/`: forbidden-dependency direction (`packages/* → apps/*`, `core → infrastructure`, deep imports across `packages/<name>/src/...`) is enforced by an automated test suite here, not by convention alone.
  - Package public API: each package's `index.ts` exports only its intended public surface; consumers do not deep-import into another package's `src/`.
  - See [Component Logic Colocation](#component-logic-colocation) - it applies inside `apps/web` the same way it applies in the single-app Next.js variants above.
  ```

  Exact source of truth for the byte-for-byte content: run `gh pr diff 238 --repo yongwoon/develop-with-llm -- tools/claude-code/skills/ywc-project-scaffold/references/javascript.md` at implementation time and apply the added (`+`) lines directly — do not retype from this plan, to avoid transcription drift (e.g. the directory-tree box-drawing characters).

## Verification Commands

- `bash scripts/validate.sh` — must report 0 errors (136/136 checks, matching this repo's CI mirror).
- `grep -n "TypeScript Monorepo Large" claude-code/skills/ywc-project-scaffold/references/javascript.md` — confirms both the TOC entry and the section heading are present (2 matches expected).
- `git diff --stat` — confirms exactly one file changed.

## Risks / Rollback

- **Risk**: minimal — additive-only markdown change to a references file with no behavioral or frontmatter impact; no downstream skill logic parses this file's content structurally beyond its existence.
- **Rollback**: `git checkout -- claude-code/skills/ywc-project-scaffold/references/javascript.md` reverts cleanly; no migration, no generated-artifact side effects (plugins mirror is untouched since it syncs from `codex/skills/`, not `claude-code/skills/`).

## Confidence Gate

Aggregate: 97/100 — **PROCEED**
- Scope clarity: 98 | Architecture compliance: 98 | Evidence quality: 97 | Reuse verified: 95 | Root cause identified: 95
- Weakest dimension: Reuse verified (95) — no material gap; scored slightly conservative only because the content is copied rather than newly authored by this repo's own investigation.
