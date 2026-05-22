# Directory Conventions — canonical per-framework purpose mapping

This reference is the canonical directory → purpose lookup used by `ywc-onboard-repo` Phase 2 ("Key directories"). The SKILL.md body asks the agent to "sample 1-2 file names per directory and infer purpose"; this file is the lookup table that turns sampled signals into named purpose.

## How to use

For each directory in the Phase 1 Pass 4 output:

1. **Look up the directory name** in the per-framework section below.
2. **Verify by sampling** 1-2 filenames inside (Glob — do not Read). If the filename pattern matches the listed convention, adopt the canonical purpose.
3. **If no match**, treat as unknown and document `<path>: Unknown — sampled <filename>, no canonical mapping`. Do not invent a purpose.

When a repo mixes multiple frameworks (monorepo with `apps/web/` + `services/api/`), apply the framework-specific table to each workspace independently.

## Universal directories

| Path pattern | Purpose | Signal |
|---|---|---|
| `src/` | Application source root | Almost any project — confirm by checking the build tool config points here |
| `tests/`, `test/`, `__tests__/` | Test suite | Pass 6 already detected; cross-check the test framework |
| `docs/` | Project documentation | Presence of `.md` files; may include design docs, ADRs, runbooks |
| `scripts/` | Build / deploy / dev scripts | Bash / Python files invoked from `package.json` scripts or Makefile |
| `bin/` | Compiled or wrapper binaries | Executable files; often shipped via `package.json` `bin` field |
| `lib/` | Shared library code | When `src/` is also present, `lib/` typically holds reusable utilities |
| `vendor/` | Bundled third-party code | Should be in `.gitignore` if managed by a package manager — flag if not |
| `examples/`, `samples/` | Usage examples for a library | Often standalone runnable apps |
| `.github/workflows/` | GitHub Actions CI definitions | YAML files |
| `.devcontainer/` | VS Code dev container config | `devcontainer.json` |

## JavaScript / TypeScript

### Next.js (App Router)

| Path | Purpose |
|---|---|
| `app/` | App-Router routes (each `page.tsx` is a URL) |
| `app/api/` | Route handlers (REST endpoints) |
| `app/(group)/` | Route group (URL transparent — for layout grouping only) |
| `components/`, `app/_components/` | Shared UI components |
| `lib/` | Server-side utilities |
| `public/` | Static assets served at `/` |
| `middleware.ts` | Edge middleware (runs before every request) |

### Next.js (Pages Router — legacy)

| Path | Purpose |
|---|---|
| `pages/` | File-system routes (each `*.tsx` is a URL) |
| `pages/api/` | API routes |
| `styles/` | Global / module CSS |

### Remix

| Path | Purpose |
|---|---|
| `app/routes/` | File-system routes with `$slug` dynamic segments |
| `app/root.tsx` | Root layout |
| `app/entry.client.tsx`, `app/entry.server.tsx` | Hydration / SSR entry points |

### Vite + React (SPA)

| Path | Purpose |
|---|---|
| `src/` | Source root |
| `src/main.tsx` | Mount entry |
| `src/App.tsx` | Root component |
| `index.html` | HTML shell (at repo root, not `public/`) |

### NestJS

| Path | Purpose |
|---|---|
| `src/main.ts` | Application bootstrap |
| `src/app.module.ts` | Root module |
| `src/<domain>/` | Feature module (`<name>.controller.ts`, `<name>.service.ts`, `<name>.module.ts`) |
| `test/` | E2E tests (unit tests collocated next to source) |

### Express / Fastify / Koa (loose convention)

| Path | Purpose |
|---|---|
| `routes/` | Route definitions |
| `controllers/` | Handler logic |
| `services/` | Business logic |
| `models/` | Data models / ORM definitions |
| `middlewares/` | Custom middleware |

## Python

### Django

| Path | Purpose |
|---|---|
| `manage.py` | CLI entry |
| `<project>/settings.py` | Configuration |
| `<project>/urls.py` | URL conf |
| `<app>/models.py` | ORM models |
| `<app>/views.py` | Request handlers |
| `<app>/admin.py` | Django admin registration |
| `<app>/migrations/` | Schema migrations |

### FastAPI

| Path | Purpose |
|---|---|
| `app/main.py` | FastAPI app instance |
| `app/routers/` | Path-operation modules |
| `app/models/` | Pydantic models |
| `app/dependencies.py` | Dependency-injection callables |

### Flask

| Path | Purpose |
|---|---|
| `app/__init__.py` | App factory |
| `app/routes.py` or `app/views.py` | Route definitions |
| `app/models.py` | SQLAlchemy models |
| `templates/`, `static/` | Jinja templates + static assets |

## Go

### Standard layout (golang-standards/project-layout)

| Path | Purpose |
|---|---|
| `cmd/<name>/main.go` | One binary per subdirectory |
| `internal/` | Private packages (cannot be imported by other modules) |
| `pkg/` | Public packages (importable) |
| `api/` | OpenAPI / Protobuf / gRPC schemas |
| `web/` | Web app assets |
| `configs/` | Default configs / sample configs |
| `scripts/` | Build / install / analysis scripts |

### Idiomatic alternative (flat)

| Path | Purpose |
|---|---|
| `main.go` (at root) | Single-binary project entry |
| `<package>/` (at root) | Each directory is a Go package |

When neither pattern fits cleanly, document the actual shape — Go's convention is "do what works".

## Rust

| Path | Purpose |
|---|---|
| `src/main.rs` | Binary crate entry |
| `src/lib.rs` | Library crate entry |
| `src/bin/<name>.rs` | Additional binaries |
| `tests/` | Integration tests |
| `examples/` | Runnable examples |
| `benches/` | Benchmarks (`cargo bench`) |

## Monorepo overlays

When the root is a monorepo, the workspace-level table above applies inside each workspace. The root-level conventions are:

| Path | Purpose |
|---|---|
| `apps/` | Deployable applications |
| `packages/` | Reusable libraries (one per directory) |
| `services/` | Backend microservices |
| `tools/` | Build / lint / generator tooling |
| `infra/` | Infrastructure-as-code (Terraform, CDK, Pulumi) |
| `docs/` | Cross-workspace documentation |

Detection signal: root `package.json` has `workspaces: [...]`, or `pnpm-workspace.yaml` / `turbo.json` / `nx.json` exists.

## When a directory does not map

Some directories are project-specific and have no canonical purpose. For these:

- Sample 2-3 filenames inside.
- Read the most recent commit message that touched the directory (`git log -1 --pretty=format:%s -- <path>`).
- Document the directory with the sampled signal:

```text
src/probe/ — sampled: agent-probe.ts, scoring-probe.ts (purpose: research-only experiment runners)
```

Do **not** leave the directory undocumented; an unexplained directory in the Onboarding Guide is a worse signal than "Unknown purpose, sampled X".
