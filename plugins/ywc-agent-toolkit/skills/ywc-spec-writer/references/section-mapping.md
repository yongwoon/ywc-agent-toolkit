# Section Mapping

Maps task categories and changed file patterns to the spec sections that need updating.

## Task Category → Spec Sections

| Category | Spec Sections to Update |
|----------|------------------------|
| `db` | `03-data.md` |
| `api` | `04-interfaces.md`, `02-features.md` |
| `domain` | `02-features.md`, `03-data.md` |
| `ui` | `05-user-flows.md`, `02-features.md` |
| `worker` | `02-features.md`, `04-interfaces.md` |
| `lib` | `06-requirements.md` (only when the library addresses an NFR) |
| `infra` | `06-requirements.md` |
| `config` | `06-requirements.md` |
| `refactor` | None — refactors have no user-visible behavior change |
| `test` | None — tests do not change the spec |

When the category is ambiguous, use `02-features.md` as the fallback.

---

## File Path Pattern → Spec Sections

| File Pattern | Spec Sections to Update |
|-------------|------------------------|
| `*schema*`, `*migration*`, `prisma/*`, `*/migrations/*` | `03-data.md` |
| `*model*`, `*entity*`, `*domain/*/` | `03-data.md`, `02-features.md` |
| `*routes/*`, `*api/*`, `*endpoints/*`, `*controllers/*` | `04-interfaces.md` |
| `*service*`, `*usecase*`, `*application/*/` | `02-features.md` |
| `*component*`, `*page*`, `*view*`, `*screen*` | `05-user-flows.md`, `02-features.md` |
| `*infra/*`, `*deploy/*`, CI/CD YAML files | `06-requirements.md` |
| `*.env*`, `*config*`, `*settings*` | `06-requirements.md` |
| `docs/ywc-plans/*`, `AGENTS.md`, `CODEX.md`, `CLAUDE.md`, `README.md` | None — documentation, not spec |
| `docs/specification/*` | None — spec files themselves, skip |

---

## When Many Sections Are Affected

If a single commit or task maps to more than 4 sections, consider using `--update` (Full Refresh) instead of incremental patching. Changes of that scope typically represent a feature-level addition best captured holistically.
