# Dead-Code Detection Tools — per-ecosystem reference

This reference is the canonical tool matrix for `ywc-refactor-clean` Step 1. The SKILL.md body lists the primary tool per ecosystem; this file holds the full invocation details, alternative tools, and the universal grep fallback.

## JavaScript / TypeScript

### Primary: knip

```bash
npx knip --reporter json > .knip-report.json
```

**Finds**: unused files, exports, types, dependencies, dev-dependencies, optional-dependencies, binaries, enum members.

**Config file**: `knip.json` or `knip` field in `package.json`. If no config exists, knip auto-detects entry points from `package.json` (`main`, `bin`, `exports`). Without config, knip may flag legitimate framework auto-discovery (e.g., Next.js pages, Remix routes) as unused — always add the framework preset before trusting the report.

**Common false positives**:
- Framework page / route files (Next.js `app/`, Remix `routes/`) — fix with `entry: ["app/**/page.tsx"]` in `knip.json`
- Test files collected by glob — fix with `project: ["src/**/*.ts", "!src/**/*.test.ts"]`
- Plugin entry points discovered at runtime — add to `entry`

### Primary: depcheck

```bash
npx depcheck --json > .depcheck-report.json
```

**Finds**: unused npm dependencies (dependencies, devDependencies).

**Common false positives**:
- Types-only packages (`@types/*`) consumed only via `tsconfig.json` paths
- Build-tool plugins loaded by name string (e.g., `eslint-plugin-foo`)
- Postinstall script dependencies

Cross-check every depcheck finding against `package.json` scripts, `tsconfig.json`, and any `.eslintrc.*` / `prettier.config.*` files before classifying as SAFE.

### TypeScript only: ts-prune

```bash
npx ts-prune
```

**Finds**: unused TypeScript exports (does not find unused files — combine with knip).

**Output**: `path/to/file.ts:42 - exportName`

**Note**: ts-prune flags an export as unused if no other TypeScript file imports it. It cannot see runtime imports, JSON references, or non-TS consumers. Always pair with grep step before deletion.

### Eslint disable directives

```bash
npx eslint . --report-unused-disable-directives --no-fix
```

Finds `/* eslint-disable-... */` comments whose rule no longer fires. Safe to delete in SAFE tier — they are pure annotation, not code.

## Python

### Primary: vulture

```bash
pip install vulture
vulture src/ --min-confidence 80
```

**Finds**: unused functions, classes, methods, variables, imports.

**Min-confidence**: 80 is the recommended floor. Below 80, vulture reports too many false positives from dynamic attribute access (`getattr`, `__getattr__`, plugin systems).

**Whitelist file**: For known false positives (e.g., Django models picked up by reflection), maintain a `vulture_whitelist.py` that imports the symbols vulture is wrong about.

### Alternative: ruff (F401, F811)

```bash
ruff check --select F401,F811 src/
```

Finds unused imports (F401) and redefined-but-unused (F811). Faster than vulture, narrower scope. Use as the daily-driver in CI; use vulture for the deeper cleanup pass.

## Go

### Primary: deadcode

```bash
go install golang.org/x/tools/cmd/deadcode@latest
deadcode ./...
```

**Finds**: unreachable functions, methods.

**Common false positives**:
- `init()` functions (always reachable by runtime)
- Functions registered via `reflect`
- Interface methods called via interface values where the concrete type is determined at runtime

### Alternative: staticcheck (U1000)

```bash
staticcheck -checks U1000 ./...
```

Slightly narrower than `deadcode` but ships in many existing Go CI pipelines already. Use whichever is already wired up.

## Rust

### Primary: cargo-udeps

```bash
cargo install cargo-udeps --locked
cargo +nightly udeps
```

**Finds**: unused crate dependencies in `Cargo.toml`.

**Nightly requirement**: cargo-udeps requires the nightly toolchain because it uses the unstable `cargo build --build-plan` output. If nightly is not available, fall back to the grep approach (see below).

### Built-in: cargo check warnings

```bash
cargo check --all-targets 2>&1 | grep "warning: unused"
```

Catches unused functions, fields, imports — but not unused dependencies. Use as the fast inner-loop check.

## Universal Grep Fallback

When no ecosystem-specific tool is available (legacy languages, exotic stacks, monorepo packages without a configured tool), fall back to the grep pattern below. This is **slower and noisier** than a dedicated tool, but works anywhere.

### Step 1: Extract exported symbols

```bash
# Example for TS (adapt the regex per language)
git grep -nE '^export (function|const|class|type|interface) [A-Za-z_]+' \
  -- 'src/**/*.ts' \
  | sed -E 's/.*export (function|const|class|type|interface) ([A-Za-z_]+).*/\2/' \
  | sort -u > .exports.txt
```

### Step 2: For each exported symbol, count cross-file references

```bash
while read sym; do
  count=$(git grep -lE "\\b${sym}\\b" -- 'src/**/*.ts' | grep -v "^$(git grep -lE "^export.* ${sym}\\b" -- 'src/**/*.ts')$" | wc -l)
  echo "$count $sym"
done < .exports.txt | sort -n | head -50
```

Symbols with `count = 0` are candidates for deletion. **They are not yet SAFE** — proceed through the standard Step 2 classification (the symbol may still be a public package export or have dynamic references). This grep is the **detection** step only; classification is unchanged.

### Limitations of the grep fallback

- No type-level analysis — type-only exports may be flagged as unused even when consumed via `import type`
- No reachability analysis — a function transitively called from an unused export is not detected as also-unused
- Path-sensitive imports (barrel re-exports) require manual unwinding

Use the grep fallback only when a dedicated tool truly is unavailable. The dedicated tools above are worth 5–10× less false-positive rate.

## Adding a new ecosystem

When extending this matrix for a new language / framework:

1. **Verify the tool exists and is maintained.** Check the GitHub repo activity — abandoned tools (>1 year since last commit) produce stale results.
2. **Document at least one concrete false-positive pattern** for the ecosystem. This forces the author to actually use the tool before adding it to the matrix.
3. **Update the table in [`../SKILL.md`](../SKILL.md) Step 1** with the new row.
4. **Run the SKILL's own validation** (Validation Checklist) on a real cleanup PR before merging the addition.

Do not add a tool to the matrix that you have not personally driven through at least one cleanup pass.
