#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$ROOT_DIR/.githooks"

if ! git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git work tree: $ROOT_DIR" >&2
  exit 1
fi

if [ ! -x "$HOOKS_DIR/pre-commit" ] || [ ! -x "$HOOKS_DIR/pre-push" ]; then
  chmod +x "$HOOKS_DIR/pre-commit" "$HOOKS_DIR/pre-push"
fi

git -C "$ROOT_DIR" config core.hooksPath "$HOOKS_DIR"

echo "Installed repo git hooks:"
echo "  core.hooksPath=$HOOKS_DIR"
echo
echo "Hooks enabled:"
echo "  pre-commit: syncs Codex marketplace package when codex/skills changes, then runs validation for codex/.codex skill changes"
echo "  pre-push: blocks stale Codex marketplace package and runs validation for Codex skill/package changes"
