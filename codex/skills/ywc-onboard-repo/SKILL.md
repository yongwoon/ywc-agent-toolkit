---
name: ywc-onboard-repo
description: >-
  (ywc) Use when entering an existing / unfamiliar repository for the first
  time, generating a starter AGENTS.md from detected conventions, or
  producing an architecture / convention briefing for a new joiner. The
  output is a printed Onboarding Guide plus a Starter AGENTS.md written to
  the repo root (enhancing the existing one in place if present). Triggers:
  "onboard me", "이 repo 처음이야", "이 codebase 를 이해하게 해줘",
  "generate AGENTS.md", "walk me through this repo", "리포 분석해줘", "コー
  ドベースを案内して", "onboarding 가이드", "ywc-onboard-repo". Do not use
  for creating a brand-new repository from scratch (use ywc-project-scaffold
  — that is the inverse direction), for creating a CodeTour `.tour` JSON
  walkthrough artifact (out of scope — this skill emits Markdown not
  .tour), for ad-hoc "explain this one file" requests (answer directly),
  or for incremental codemap refreshes on a repo you already understand
  (this skill is the cold-start; refreshes belong to a separate hygiene
  pass).
---

# ywc-onboard-repo

**Announce at start:** "I'm using the ywc-onboard-repo skill to reconnoiter the repository in 4 phases and emit an Onboarding Guide + Starter AGENTS.md."

This skill is the canonical cold-start procedure when entering a repository for the first time. It exists because the default agent behavior — reading the README, then guessing — produces an AGENTS.md filled with framework defaults rather than the conventions this codebase actually follows. Adapted from `ECC/codebase-onboarding`, tightened to delegate dead-code cleanup to `ywc-refactor-clean` and to forbid Read-every-file expansion (Glob + Grep reconnaissance only).

## The Iron Law

```text
RECONNAISSANCE WITH GLOB/GREP FIRST — NEVER READ EVERY FILE
CONVENTION DETECTED FROM CODE WINS OVER CONVENTION DETECTED FROM CONFIG
EXISTING AGENTS.md IS ENHANCED IN PLACE, NEVER OVERWRITTEN
```

The 4-phase workflow (Reconnaissance → Architecture → Conventions → Generate) is sequential — each phase's output is the input to the next. Skipping reconnaissance to "just read the source" defeats the entire purpose: the agent ends up with intuition about a handful of files instead of structural insight about the whole repo.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "I'll just Read the top 20 files and figure it out" | Reading exhausts context before reconnaissance finishes. A 50-file repo has ~80 KB of source; a 5000-file monorepo has ~10 MB. Glob + Grep yield structural signals at ~1% of that token cost. Reading is for the 3-5 files reconnaissance flags as ambiguous, not the survey. |
| "The README already explains the architecture — I'll copy from it" | READMEs document what the author *intended* to ship, not what the repo actually contains. New features land without README updates; deprecated modules linger after README purges. The repo on disk is the source of truth; the README is a hint. |
| "package.json says React 18 — that's the framework" | A `package.json` dependency does not prove the framework is used. Many repos carry vestigial deps from past refactors. Verify by grepping for the framework's distinctive symbols (`useState`, `React.FC`, `'react-router'`) in the actual source. |
| "I'll generate a fresh AGENTS.md — easier than reading the old one" | Overwriting AGENTS.md silently destroys project-specific instructions the team has accumulated (rare-failure notes, secret commands, do-not-touch zones). Always Read the existing file first; if regenerating, diff before write and call out what was added vs preserved. |
| "Convention detection is vague — I'll just say `we use TypeScript and React`" | "TypeScript and React" is the framework, not a convention. A convention is "files use kebab-case", "errors return `Result<T, E>` not throws", "tests live next to source as `*.test.ts` not in `tests/`". If you cannot point to 2+ files demonstrating the convention, do not document it. |
| "The repo is empty — I'll produce a generic AGENTS.md skeleton" | An empty (or just-cloned-shallow) repo cannot support convention detection. Phases 2-3 must report "insufficient signal" honestly rather than emit framework boilerplate. A generic skeleton invites the next reader to treat it as ground truth. |
| "I detected 3 frameworks (Next.js, NestJS, Remix) — listing all three" | Frameworks in a monorepo belong to specific workspaces. Locate each in the directory tree, scope the detection per workspace, and document accordingly. A flat "this repo uses Next.js + NestJS" claim is wrong; it uses Next.js in `apps/web/` and NestJS in `services/api/`. |
| "Git history is shallow — I'll skip convention detection" | Shallow history (e.g., `git clone --depth 1`) means commit-message and branch-naming conventions cannot be detected. Report the gap explicitly ("Git history unavailable or too shallow"); do not invent conventions from file content. |

**Violating the letter of this discipline is violating the spirit.** A wrong AGENTS.md is worse than no AGENTS.md — it teaches future agents the wrong conventions, and the error compounds across every subsequent skill invocation.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--scope` | `--scope <dir>` | `--scope apps/web/` | Limit reconnaissance to a workspace (useful in monorepos). Default: repository root. |
| `--guide-only` | flag | `--guide-only` | Emit the Onboarding Guide but skip writing the Starter AGENTS.md. |
| `--agents-md-only` | flag | `--agents-md-only` | Emit only the Starter AGENTS.md, skip the Guide. |
| `--enhance` | flag | `--enhance` | Force the "existing AGENTS.md enhancement" path even when no AGENTS.md is present (creates an empty stub first). |

## Workflow

### Phase 1: Reconnaissance — Glob + Grep, never Read-all

Run **all six signal-gathering passes** (no Read tool — Glob and Grep only). The fastest path is the bundled script, which runs every pass in one shot and prints the structured summary:

```bash
RECON_SCRIPT="codex/skills/ywc-onboard-repo/scripts/recon.sh"
[ -f "$RECON_SCRIPT" ] || RECON_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/ywc-onboard-repo/scripts/recon.sh"
bash "$RECON_SCRIPT" [repo-dir]
```

Full per-pass tool invocations (for when you need to run or extend a single pass by hand) live in [`references/reconnaissance-checklist.md`](references/reconnaissance-checklist.md).

| Pass | What it surfaces | Tool |
|---|---|---|
| 1. Package manifest | Language, dependency footprint, scripts | Glob: `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `mix.exs`, `pubspec.yaml` |
| 2. Framework fingerprint | Web framework, build tool, runtime | Glob: `next.config.*`, `vite.config.*`, `nuxt.config.*`, `astro.config.*`, `angular.json`, `nest-cli.json`, `manage.py`, `app/__init__.py`, `cmd/*/main.go` |
| 3. Entry points | Where execution starts | Glob: `main.*`, `index.*`, `server.*`, `app.*`, `cmd/`, `src/main/` |
| 4. Directory structure | Top-level shape (2 levels) | Bash: `find . -maxdepth 2 -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/build/*'` |
| 5. Tooling | Linter, formatter, CI, container | Glob: `.eslintrc*`, `biome.json`, `.prettierrc*`, `ruff.toml`, `Makefile`, `Dockerfile`, `docker-compose*`, `.github/workflows/`, `.env.example` |
| 6. Test structure | Test framework, file convention | Glob: `**/*test*`, `**/*spec*`, `pytest.ini`, `jest.config.*`, `vitest.config.*`, `playwright.config.*` |

At the end of Phase 1, write a 10-line **Reconnaissance Summary** internally (not yet shown to the user): one line per pass, e.g. `Pass 1: package.json present, runtime = Node 20.x, scripts = dev/build/test/lint`.

### Phase 2: Architecture Mapping

From the reconnaissance summary, identify the four architecture facets below. **Verify each one by grepping the source**, not just by reading the config.

| Facet | Question | Verification |
|---|---|---|
| Tech stack | Which language and major libraries are *actually* used? | Cross-check `package.json` deps against `git grep -lE "from ['\"]<dep>['\"]"` — discard any dep with zero source hits. |
| Architecture pattern | Monolith / monorepo / microservices / serverless? | Monorepo: `packages/` or `apps/` directory present, root `package.json` has `workspaces`. Microservices: separate deploy units per service directory. Serverless: `serverless.yml`, `vercel.json`, AWS SAM template. |
| Key directories | What does each top-level directory hold? | Sample 1-2 file names per directory; infer purpose from filename pattern. Use [`references/directory-conventions.md`](references/directory-conventions.md) for the canonical per-framework mapping. |
| Request lifecycle | How does one request travel from entry → response? | Locate one route handler, follow imports outward: handler → service → repository → DB. Document the chain as a 3-5 step trace. |

When a facet cannot be determined with confidence ≥7/10, document it as `Unknown — <one-line reason>` rather than guessing.

### Phase 3: Convention Detection

Inspect existing source to surface patterns *the codebase already follows* (not what frameworks default to).

| Convention | Source of truth | Procedure |
|---|---|---|
| File naming | `find src -type f \| sed 's/.*\///' \| sort -u` then inspect majority pattern | Pick from: kebab-case, camelCase, PascalCase, snake_case. Report the pattern that wins ≥80% of files; report "mixed" otherwise. |
| Error handling | `git grep -nE "throw new \\w+\\(\|Result<\|return \\{ error\|raise [A-Z]"` | Categorize: throw-based (try/catch), Result/Either type, error-codes, exception with `raise`. Pick the dominant style. |
| Async pattern | `git grep -nE "async function\|await \|\\.then\\(\|go func\\(\|channels\|coroutine"` | Categorize: async/await, promise chains, callbacks, goroutines/channels, coroutines. |
| Git conventions | `git log --pretty=format:'%s' -n 50 \| head -20` + `git branch -a \| head -10` | Detect commit-message format (conventional commits?, scope prefix?), branch prefix (feature/, fix/, etc). If history is shallow (`< 10 commits`), report "shallow history — convention undetectable". |
| Test placement | Compare `find . -path '*/tests/*' \| wc -l` vs `find . -name '*.test.*' \| wc -l` | If first dominates: `tests/` directory convention. If second dominates: collocated `*.test.*`. If both, scope per workspace. |

Detected convention with <3 supporting examples is **not** a convention — leave it out rather than over-claim.

### Phase 4: Generate Artifacts

Emit two outputs. Both are required unless `--guide-only` or `--agents-md-only` is set.

#### Output A: Onboarding Guide (printed to conversation)

```markdown
# Onboarding Guide: <repo-name>

## Overview
<2-3 sentences: what this project does and who it serves, derived from README + package description>

## Tech Stack
| Layer | Technology | Version | Source |
|-------|-----------|---------|--------|
| Language | <name> | <version> | <package.json / go.mod / etc.> |
| Framework | <name> | <version> | <config file> |
| Database | <name> | <version> | <ORM config / docker-compose> |
| Testing | <name> | <version> | <config file> |

## Architecture
<3-5 sentences: monolith / monorepo / microservices, frontend-backend split, API style>

## Key Entry Points
- **<purpose>**: `<path>` — <one-line role>
- **<purpose>**: `<path>` — <one-line role>

## Directory Map
| Path | Purpose |
|------|---------|
| `<top-level>` | <one-line purpose, inferred from sampled files> |

## Request Lifecycle
1. <entry: router / handler>
2. <middleware / validation>
3. <business logic: service / use-case>
4. <persistence: repo / ORM>
5. <response shape>

## Conventions
- File naming: <kebab-case / camelCase / ...>
- Error handling: <throw / Result / ...>
- Async: <async-await / promise / ...>
- Tests live: <collocated / tests-dir>
- Git: <conventional-commits / freeform; branch prefix=<feature/, fix/>>

## Common Tasks
- Dev server: `<command from package.json scripts>`
- Tests: `<command>`
- Lint: `<command>`
- Build: `<command>`
- Database: `<command if detected>`

## Where to Look
| I want to... | Look at... |
|--------------|-----------|
| <add an API endpoint> | `<path>` |
| <add a UI component> | `<path>` |
| <add a test> | `<path-pattern>` |
| <change build config> | `<path>` |

## Detection Confidence
- Detected: <N> facts
- Inferred (medium confidence): <N> facts
- Unknown / shallow: <N> facts (listed inline above as "Unknown — ...")
```

#### Output B: Starter AGENTS.md (written to repo root)

If an `AGENTS.md` already exists, **Read it first** and merge — preserve existing project-specific instructions, append a clearly-labeled `## Detected Conventions (<YYYY-MM-DD>)` section at the bottom with the new findings. Never overwrite.

When no AGENTS.md exists, the canonical starter template lives in [`references/agents-md-starter.md`](references/agents-md-starter.md). Copy it and fill in the placeholders from Phases 1-3.

Keep the generated AGENTS.md **under 100 lines** — if it grows beyond that, the new content belongs in a project doc that AGENTS.md links to, not in AGENTS.md itself.

## Output Format

The conversation surface emits the Onboarding Guide (markdown) directly. The Starter AGENTS.md is written to the repo root and confirmed with a one-line claim:

```text
Wrote AGENTS.md (<N> lines, <M> sections) at <repo-root>/AGENTS.md
  - Preserved existing sections: <list or "none — file did not exist">
  - Appended sections: ## Detected Conventions (<YYYY-MM-DD>)
```

The claim line follows `ywc-verify-done`'s vocabulary rules (no "should" / "probably" / "seems"). The file was either written or it was not.

## Integration

- **Upstream**: user invocation (most common); a subagent runner that needs an AGENTS.md before delegating implementation.
- **Downstream**: `ywc-refactor-clean` (when reconnaissance reveals prior dead-code accumulation that blocks comprehension); `ywc-impl-review` (the Onboarding Guide is read by a reviewer entering the repo cold); `ywc-plan` (Phase 2's Request Lifecycle is the architectural anchor for plan Step 2).
- **Pairs with**: `ywc-project-scaffold` (the inverse — scaffold *creates* a repo with conventions; onboard *discovers* conventions in an existing one). Never both in the same session; pick the direction.
- **Must not be paired with**: `ywc-code-gen` in the same session — onboarding produces an AGENTS.md the code-gen will consume; running both in one session means the code-gen reads a half-written AGENTS.md.

## Validation Checklist

Before declaring the onboarding pass complete, verify:

- [ ] All 6 reconnaissance passes ran (or were explicitly skipped with reason)
- [ ] Architecture facets have a verification source — not just a config-file claim
- [ ] Every documented convention is supported by ≥3 source examples
- [ ] Existing AGENTS.md (if any) was **Read before write** — diff captured in the claim line
- [ ] Generated AGENTS.md is ≤100 lines
- [ ] Confidence section lists at least the count of Unknown facts (zero is allowed; missing the section is not)
- [ ] If git history is shallow (<10 commits), conventions section reports the shallow-history caveat

## Common Mistakes

(Procedural failure modes specific to repo onboarding. Behavioral rationalizations are in the table above — do not duplicate here.)

- **Reading the README and stopping there.** The README is one signal among six. Skipping Phase 1's other five passes means the Onboarding Guide reflects what the author wrote about the project, not what is in the project. Always complete all six passes.
- **Documenting framework defaults as conventions.** "Uses TypeScript strict mode" is not a convention if it ships in every Next.js scaffold — it is the framework's default. Convention = a choice the team made, not a default they accepted. Filter the output accordingly.
- **Bundling cleanup or refactor work into the onboarding PR.** Onboarding is a read-only survey + an AGENTS.md write. Cleanup is a separate skill (`ywc-refactor-clean`) and a separate branch. Mixing them produces a PR that is impossible to review.
- **Skipping the existing-AGENTS.md Read because "it's outdated anyway".** Outdated content may include load-bearing rules (security gates, hidden directory constraints, integration secrets handling) that you cannot detect from the source. Read, preserve, append.
- **Producing a 300-line AGENTS.md "for completeness".** An AGENTS.md the reader does not read is worse than a shorter one they do. Hard cap at 100 lines; everything past that goes in a linked doc.

## References

| Reference | Use when |
|---|---|
| [references/reconnaissance-checklist.md](references/reconnaissance-checklist.md) | Running Phase 1's six passes — full Glob / Grep / Bash invocations per ecosystem |
| [references/directory-conventions.md](references/directory-conventions.md) | Mapping `src/api/`, `src/pages/`, `cmd/`, etc. to canonical purpose during Phase 2 |
| [references/agents-md-starter.md](references/agents-md-starter.md) | Phase 4 Output B — starter AGENTS.md template with placeholders |
| [../ywc-project-scaffold/SKILL.md](../ywc-project-scaffold/SKILL.md) | When the user actually wants to *create* a new repo, not survey an existing one — route there |
| [../ywc-refactor-clean/SKILL.md](../ywc-refactor-clean/SKILL.md) | When reconnaissance reveals significant dead-code accumulation — schedule a follow-up cleanup PR |
| [../ywc-verify-done/SKILL.md](../ywc-verify-done/SKILL.md) | Vocabulary rules for the final "Wrote AGENTS.md" claim |
