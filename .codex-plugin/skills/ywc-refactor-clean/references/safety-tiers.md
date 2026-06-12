# Safety Tier Classification — full rules

This reference is the canonical classification rubric for `ywc-refactor-clean` Step 2. The SKILL.md body shows the three tiers in a summary table; this file holds the full rules, concrete examples, and the escalation procedure for borderline items.

## Classification Algorithm

For each detection-tool finding, apply the rules in order. The **first** matching rule determines the tier. Items that match multiple rules escalate to the highest tier (DANGER > CAUTION > SAFE).

```text
1. Is the symbol exported in package.json (exports / main / module / bin)?       → DANGER
2. Is the symbol a config file, entry point, or schema definition?               → DANGER
3. Has `git log` touched this file in the last 7 days?                           → DANGER
4. Is the symbol a route handler / middleware / page / component?                → CAUTION
5. Does the symbol's name appear as a string anywhere in the repo?               → CAUTION
6. Is the symbol referenced via import() / require() with a dynamic argument?    → CAUTION
7. Is the symbol a public-but-internal export (used across packages in monorepo)? → CAUTION
8. Otherwise: internal helper, private function, type alias, test fixture        → SAFE
```

Each rule has a concrete detection procedure below.

## DANGER Tier

DANGER items are **reported but not deleted** by this skill. They require a separate intentional change (API deprecation, major version bump, external-consumer migration).

### D1: Public package export

**Procedure**:
```bash
cat package.json | jq '.exports, .main, .module, .bin, .types' 2>/dev/null
```

If the symbol's file appears in any of these fields, the file is reachable from outside the repository. Examples:

- `"main": "./dist/index.js"` — `dist/index.js` is the package entry; any symbol exported from it is consumable by `import { x } from "your-pkg"`.
- `"exports": { ".": "./src/index.ts", "./util": "./src/util.ts" }` — `src/util.ts` is a subpath export.
- `"bin": { "your-cli": "./dist/cli.js" }` — `dist/cli.js` is an executable entry.

**Why DANGER**: deletion breaks downstream consumers silently. The detection tool cannot see them.

### D2: Config / entry / schema

Files that the runtime, build tool, or test runner reads by **path, not by import**:

| Pattern | Example |
|---|---|
| Framework config | `next.config.ts`, `vite.config.ts`, `nuxt.config.ts`, `astro.config.mjs` |
| Build / package | `package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` |
| CI / deploy | `.github/workflows/*.yml`, `Dockerfile`, `docker-compose.yml`, `vercel.json` |
| Linter / formatter | `.eslintrc.*`, `.prettierrc.*`, `biome.json`, `ruff.toml` |
| Schema | `prisma/schema.prisma`, `*.graphql`, `*.proto`, `openapi.yaml` |
| Test runner | `jest.config.*`, `vitest.config.*`, `playwright.config.*`, `pytest.ini` |
| Entry point | `main.ts`, `index.ts`, `app.tsx`, `cmd/<name>/main.go` |

**Why DANGER**: the runtime / build tool reads these by string path, so static-analysis tools cannot see the reference.

### D3: Recently touched (<7 days)

**Procedure**:
```bash
git log --since="7 days ago" --name-only --pretty=format: -- <file> | sort -u
```

If output is non-empty, the file was edited in the last 7 days — there is in-flight work in this area. Cleanup must wait until the in-flight work merges, or the cleanup PR will conflict.

**Why DANGER**: high probability of merge conflict; high probability the touching author has unstaged dependent work.

## CAUTION Tier

CAUTION items can be deleted, but **only after** the three additional verification checks in SKILL.md Step 4.

### C1: Route / middleware / page / component

| Pattern | Detection |
|---|---|
| Express / Koa / Fastify route | File matches `routes/**/*.{ts,js}` or registers via `app.get(...)` |
| Next.js / Remix page | File path matches framework's route convention (`app/**/page.tsx`, `routes/$slug.tsx`) |
| React component | File ends `.tsx`, exports default function whose name is PascalCase |
| Middleware | Function whose signature is `(req, res, next)` or framework-equivalent |
| GraphQL resolver | File matches `resolvers/**/*.ts` or registered in schema builder |

**Why CAUTION**: framework reaches these via convention-based discovery (filesystem-routed, decorator-registered, schema-bound). The tool sees no import; the framework knows by path / name.

### C2: Name appears as a string

**Procedure**:
```bash
git grep -nE "['\"\\\`].*\\b<symbol>\\b.*['\"\\\`]"
```

If the symbol's name appears inside any string literal anywhere in the repo, it may be:

- A plugin slug registered in config
- A route name in a router definition
- A docs reference (`See \`processOrder\` for ...`)
- A test name (`it('processOrder handles ...')` — false positive but worth checking)
- A feature flag key
- A telemetry event name

Each hit must be inspected individually — if any hit is a **functional** reference (not docs / test name), re-classify to DANGER.

### C3: Dynamic import / require

**Procedure**:
```bash
git grep -nE "(import|require)\\([^)]*\\+[^)]*\\)" -- 'src/**'
git grep -nE "(import|require)\\([\\\`].*\\$\\{" -- 'src/**'
```

Any `import('./modules/' + name)` or `` require(`./plugins/${type}`) `` pattern means the runtime resolves modules by string at runtime. Symbols referenced this way are invisible to the static detection tool.

**If the symbol's path or name fragment could match any dynamic import, treat as CAUTION minimum, often DANGER.**

### C4: Monorepo cross-package export

In a monorepo (`packages/*`, `apps/*`):

```bash
# For a candidate symbol in packages/util/src/foo.ts:
git grep -nE "from ['\"]@your-org/util['\"]" -- 'packages/*' 'apps/*'
```

If any other package / app imports from this package, treat any internal `export` as CAUTION — it may be re-exported through the package's index.

## SAFE Tier

If the item passed all DANGER and CAUTION checks, it is SAFE:

- Internal helper called only within its own file or package-internal module
- Test fixture / mock factory
- Private function (no `export` keyword in JS / TS, lowercase first letter in Go)
- Type alias with no external consumers
- Eslint / Ruff / Pylint disable directive that no longer applies

**SAFE deletion still runs the Step 3 verification loop**: scoped test run before, grep verification, deletion, scoped test run after, single-item commit. The tier name names the **starting confidence**, not the deletion procedure.

## Borderline Item Escalation

When you cannot decide between two tiers, **always pick the higher tier**:

| Ambiguity | Resolution |
|---|---|
| SAFE vs CAUTION | CAUTION — extra grep step costs ~30 seconds; deletion regression costs hours |
| CAUTION vs DANGER | DANGER — report only, do not delete in this skill's scope |
| "It is internal but I think it could be exported soon" | CAUTION at minimum — soon-to-be-exported is a behavior change |

When the ambiguity persists after both checks, route through `ywc-confidence-gate` — the 5-dimension rubric (duplicate / architecture / docs / OSS / root-cause) translates directly:

- ≥90 confidence the symbol is CAUTION → delete as CAUTION
- 70-89 → request reviewer second opinion before deletion
- <70 → re-classify to DANGER

## Worked Examples

### Example 1: `formatCurrency` utility

- Found by: `ts-prune` (`src/util/format.ts:12 - formatCurrency`)
- Procedure:
  - D1: Not in `exports` / `main` / `module` → not D1
  - D2: Not a config file → not D2
  - D3: `git log --since="7 days ago" -- src/util/format.ts` returns empty → not D3
  - C1: Not a route / middleware / page → not C1
  - C2: `git grep -nE "['\"\\\`].*\\bformatCurrency\\b.*['\"\\\`]"` → returns docs hits only → C2 with note
  - C3: No dynamic imports match → not C3
  - C4: `git grep -nE "from ['\"]@org/util['\"]"` from other packages → 0 hits → not C4
- **Tier: CAUTION** (because of docs-string hit; verify the docs are not load-bearing)

### Example 2: Default export of `src/cli.ts`

- Found by: `knip` (`src/cli.ts: default export`)
- Procedure:
  - D1: `package.json` has `"bin": { "your-tool": "./dist/cli.js" }` → **DANGER (D1)**
- **Tier: DANGER** (report only; do not delete)

### Example 3: Old `legacyReducer` in `src/state/legacy/`

- Found by: `knip` (`src/state/legacy/reducer.ts`)
- Procedure:
  - D1: Not in package exports → not D1
  - D2: Not a config → not D2
  - D3: Not touched in 7 days → not D3
  - C1: Not a route / page → not C1
  - C2: `git grep -nE "['\"\\\`].*\\blegacyReducer\\b.*['\"\\\`]"` → 0 hits → not C2
  - C3: No dynamic imports → not C3
  - C4: Single-package repo → not C4
- **Tier: SAFE** — proceed with Step 3 deletion loop
