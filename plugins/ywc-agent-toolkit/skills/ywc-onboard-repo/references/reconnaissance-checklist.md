# Phase 1 Reconnaissance — full per-pass invocations

This reference is the canonical command list for `ywc-onboard-repo` Phase 1. The SKILL.md body lists the six passes in summary; this file holds the actual Glob / Grep / Bash invocations per ecosystem.

All six passes must run **in parallel**. They are independent (no pass consumes another's output). Do not Read any source file during Phase 1 — Read is reserved for ambiguous signals surfaced by Phases 2-3.

## Pass 1: Package manifest

```bash
# JS / TS
ls package.json pnpm-workspace.yaml turbo.json nx.json 2>/dev/null

# Python
ls pyproject.toml setup.py requirements*.txt Pipfile poetry.lock 2>/dev/null

# Go / Rust / Java / Ruby / PHP / Elixir / Dart
ls go.mod Cargo.toml pom.xml build.gradle Gemfile composer.json mix.exs pubspec.yaml 2>/dev/null

# Per detected manifest, extract:
#   - Language + runtime version (engines.node, python_requires, go.mod version, rust-toolchain)
#   - Top-level scripts (package.json scripts, pyproject.toml [project.scripts])
#   - Direct dependencies count (do not enumerate — count only at this stage)
```

**Signal captured**: runtime, version, script names. Detailed dep enumeration is a Phase 2 step (after framework fingerprinting narrows the relevant deps).

## Pass 2: Framework fingerprint

```bash
# Web / app frameworks
ls next.config.* vite.config.* nuxt.config.* astro.config.* angular.json \
   nest-cli.json remix.config.* svelte.config.* gatsby-config.* \
   2>/dev/null

# Backend frameworks
ls manage.py app/__init__.py wsgi.py asgi.py \
   2>/dev/null
find . -maxdepth 3 -name "main.go" -path "*/cmd/*" 2>/dev/null | head -5
find . -maxdepth 3 -name "main.rs" 2>/dev/null | head -5

# Mobile / desktop
ls pubspec.yaml ios/Runner.xcodeproj android/build.gradle electron.config.* tauri.conf.json \
   2>/dev/null
```

**Signal captured**: framework presence (config file existence) + framework version (from Pass 1's manifest). **Always verify** in Phase 2 by grepping the framework's distinctive symbols — a `next.config.ts` does not prove Next.js is in active use.

## Pass 3: Entry points

```bash
# Universal entry-point heuristic (top 3 levels)
find . -maxdepth 3 -type f \
  \( -name "main.*" -o -name "index.*" -o -name "server.*" -o -name "app.*" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -not -path "*/dist/*" -not -path "*/build/*" \
  -not -path "*/__pycache__/*" -not -path "*/target/*" \
  2>/dev/null | head -30

# Go-specific: every cmd/<name>/main.go is a separate binary entry
find . -maxdepth 4 -name "main.go" -path "*/cmd/*" 2>/dev/null
```

**Signal captured**: candidate entry points by file pattern. Phase 2 then maps each entry → its purpose (CLI / HTTP server / worker / build tool).

## Pass 4: Directory structure

```bash
# Top 2 levels only — deeper trees burn tokens with little signal benefit
find . -maxdepth 2 -type d \
  -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/dist/*' -not -path '*/build/*' \
  -not -path '*/__pycache__/*' -not -path '*/target/*' \
  -not -path '*/vendor/*' -not -path '*/.next/*' \
  2>/dev/null | sort
```

**Signal captured**: top-level shape (monorepo vs single-app, presence of `src/`, `apps/`, `packages/`, `services/`, `cmd/`, etc.). Phase 2's directory mapping consumes this.

## Pass 5: Tooling

```bash
# Linter / formatter
ls .eslintrc* .prettierrc* biome.json eslint.config.* prettier.config.* \
   ruff.toml pyproject.toml setup.cfg \
   .golangci.yml .golangci.yaml \
   rustfmt.toml clippy.toml \
   2>/dev/null

# CI
find .github/workflows -maxdepth 1 -name "*.yml" -o -name "*.yaml" 2>/dev/null
ls .circleci/config.yml .gitlab-ci.yml .travis.yml azure-pipelines.yml \
   bitbucket-pipelines.yml jenkins.yaml \
   2>/dev/null

# Container / orchestration
ls Dockerfile Dockerfile.* docker-compose*.yml docker-compose*.yaml \
   k8s/ kubernetes/ helm/ \
   2>/dev/null

# Build / task
ls Makefile justfile Taskfile.yml taskfile.yml \
   2>/dev/null

# Env
ls .env.example .env.template env.sample \
   2>/dev/null
```

**Signal captured**: lint tool, format tool, CI platform, container strategy, env-var contract. The Onboarding Guide's "Common Tasks" section pulls scripts from these.

## Pass 6: Test structure

```bash
# Config files
ls jest.config.* vitest.config.* playwright.config.* cypress.config.* \
   pytest.ini tox.ini conftest.py \
   .mocharc.* karma.conf.* \
   2>/dev/null

# Test directory vs collocated heuristic — counts only
TESTS_DIR_COUNT=$(find . -type d \( -name "tests" -o -name "test" -o -name "__tests__" \) \
  -not -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')
COLLOCATED_COUNT=$(find . -type f \
  \( -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.go" -o -name "test_*.py" \) \
  -not -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')

echo "TESTS_DIR=$TESTS_DIR_COUNT  COLLOCATED=$COLLOCATED_COUNT"
```

**Signal captured**: test framework, test placement convention (collocated vs `tests/`), test file naming pattern. Phase 3's "Test placement" convention is the consumer.

## Skipping a pass

A pass may be skipped only when its tool surface is **demonstrably absent** (e.g., no `package.json`, no `requirements.txt`, no `go.mod` anywhere = skip Pass 1 for language detection but still run for sibling languages). Skipping for token-budget reasons is forbidden — the parallelism makes all six passes roughly equal in wall-clock cost.

When a pass is skipped, the Reconnaissance Summary line MUST be `Pass <N>: skipped — <reason>` rather than omitted.

## Output of Phase 1

The internal Reconnaissance Summary (kept in agent working memory, not yet surfaced) shapes:

```text
Pass 1: package.json present, runtime = Node 20.x, scripts = dev/build/test/lint
Pass 2: next.config.ts + vite.config.ts → Next.js app + Vite-bundled library
Pass 3: src/app/page.tsx, src/server.ts (Next.js page + API server entries)
Pass 4: 14 top-level dirs; monorepo shape (apps/, packages/, services/)
Pass 5: biome.json (lint+format), .github/workflows/{ci,deploy}.yml, Dockerfile
Pass 6: vitest.config.ts; TESTS_DIR=2, COLLOCATED=148 → collocated convention
```

Phase 2 consumes this summary directly. Phases 3 and 4 also reference it. Do not regenerate — the summary is the working artifact through the full skill execution.
