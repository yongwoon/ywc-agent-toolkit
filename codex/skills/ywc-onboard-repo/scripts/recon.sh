#!/usr/bin/env bash
# Phase 1 reconnaissance for ywc-onboard-repo — runs all six passes and prints
# a structured Reconnaissance Summary in one shot. Deterministic replacement for
# the ~25 separate Glob/find/grep tool calls the LLM otherwise issues by hand.
#
# Usage:
#   bash codex/skills/ywc-onboard-repo/scripts/recon.sh [repo-dir]
#
# Run from (or pass) the target repository root. Reads nothing into the model
# beyond the summary it prints; the skill consumes that summary directly.
set -uo pipefail   # NOT -e: an absent tool surface must not abort a pass

ROOT="${1:-.}"
cd "$ROOT" 2>/dev/null || { echo "error: cannot cd to $ROOT" >&2; exit 1; }

PRUNE='-not -path */node_modules/* -not -path */.git/* -not -path */dist/* -not -path */build/* -not -path */__pycache__/* -not -path */target/* -not -path */vendor/* -not -path */.next/*'

show() { ls -d "$@" 2>/dev/null | sed 's/^/  /'; }

echo "=== Pass 1: Package manifest ==="
show package.json pnpm-workspace.yaml turbo.json nx.json \
     pyproject.toml setup.py requirements*.txt Pipfile poetry.lock \
     go.mod Cargo.toml pom.xml build.gradle Gemfile composer.json mix.exs pubspec.yaml

echo "=== Pass 2: Framework fingerprint ==="
show next.config.* vite.config.* nuxt.config.* astro.config.* angular.json \
     nest-cli.json remix.config.* svelte.config.* gatsby-config.* \
     manage.py wsgi.py asgi.py electron.config.* tauri.conf.json
# shellcheck disable=SC2086
find . -maxdepth 4 -name main.go -path '*/cmd/*' $PRUNE 2>/dev/null | head -5 | sed 's/^/  /'

echo "=== Pass 3: Entry points ==="
# shellcheck disable=SC2086
find . -maxdepth 3 -type f \
  \( -name 'main.*' -o -name 'index.*' -o -name 'server.*' -o -name 'app.*' \) \
  $PRUNE 2>/dev/null | head -30 | sed 's/^/  /'

echo "=== Pass 4: Directory structure (top 2 levels) ==="
# shellcheck disable=SC2086
find . -maxdepth 2 -type d $PRUNE 2>/dev/null | sort | sed 's/^/  /' | head -40

echo "=== Pass 5: Tooling ==="
show .eslintrc* .prettierrc* biome.json eslint.config.* prettier.config.* \
     ruff.toml setup.cfg .golangci.y*ml rustfmt.toml clippy.toml \
     Dockerfile Dockerfile.* docker-compose*.y*ml \
     Makefile justfile Taskfile.y*ml taskfile.y*ml \
     .env.example .env.template env.sample
find .github/workflows -maxdepth 1 \( -name '*.yml' -o -name '*.yaml' \) 2>/dev/null | sed 's/^/  /'
show .circleci/config.yml .gitlab-ci.yml .travis.yml azure-pipelines.yml

echo "=== Pass 6: Test structure ==="
show jest.config.* vitest.config.* playwright.config.* cypress.config.* \
     pytest.ini tox.ini conftest.py .mocharc.* karma.conf.*
TESTS_DIR_COUNT=$(find . -type d \( -name tests -o -name test -o -name __tests__ \) -not -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')
COLLOCATED_COUNT=$(find . -type f \( -name '*.test.*' -o -name '*.spec.*' -o -name '*_test.go' -o -name 'test_*.py' \) -not -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')
echo "  TESTS_DIR=$TESTS_DIR_COUNT  COLLOCATED=$COLLOCATED_COUNT"
if [ "$COLLOCATED_COUNT" -gt "$TESTS_DIR_COUNT" ]; then
  echo "  → collocated test convention"
elif [ "$TESTS_DIR_COUNT" -gt 0 ]; then
  echo "  → tests/ directory convention"
fi
