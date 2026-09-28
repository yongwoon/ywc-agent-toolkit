#!/usr/bin/env bash
#
# Smoke test for scripts/install.sh's shared references/scripts sync.
#
# Regression target: develop-with-llm PR #234 documented a case where the
# Claude Code installer silently stopped syncing shared references/scripts
# to the install destination for 111 days because every existing check only
# validated the source tree, never an actual installed destination. This
# test runs the real installer against temporary destinations and confirms
# the shared dirs land there and that an installed skill's relative
# reference link still resolves from its installed location.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEMP_ROOT"' EXIT

assert_support_dirs() {
  local dest="$1"
  local label="$2"

  [ -d "$dest/references" ] || { echo "FAIL: $label missing references/ at $dest"; exit 1; }
  [ -d "$dest/scripts" ] || { echo "FAIL: $label missing scripts/ at $dest"; exit 1; }
  [ -n "$(find "$dest/references" -type f -print -quit)" ] || { echo "FAIL: $label references/ is empty"; exit 1; }
  [ -n "$(find "$dest/scripts" -type f -print -quit)" ] || { echo "FAIL: $label scripts/ is empty"; exit 1; }
}

assert_installed_link_resolves() {
  local dest="$1"
  local label="$2"
  local file link target

  # `|| true` keeps a zero-match grep from tripping `set -e pipefail` before
  # the friendly FAIL message below can run.
  file="$(grep -rlE --include='SKILL.md' -- '(\.\./)+references/[A-Za-z0-9._-]+\.md' "$dest" | head -n 1 || true)"
  if [ -z "$file" ]; then
    echo "FAIL: $label has no installed skill file with a references/ link to check"
    exit 1
  fi

  link="$(grep -oE -- '(\.\./)+references/[A-Za-z0-9._-]+\.md' "$file" | head -n 1 || true)"
  target="$(dirname "$file")/$link"
  if [ ! -f "$target" ]; then
    echo "FAIL: $label installed link does not resolve: ${file#"$dest"/} -> $link"
    exit 1
  fi
}

echo "==> Installing Claude Code skills to a temporary destination..."
CC_DEST="$TEMP_ROOT/cc"
CLAUDE_SKILLS_DIR="$CC_DEST" bash "$REPO_ROOT/scripts/install.sh" --cc >/dev/null
assert_support_dirs "$CC_DEST" "Claude Code"
assert_installed_link_resolves "$CC_DEST" "Claude Code"

echo "==> Installing Codex skills to a temporary destination..."
CODEX_HOME="$TEMP_ROOT/codex"
export CODEX_HOME
bash "$REPO_ROOT/scripts/install.sh" --codex >/dev/null
CODEX_SKILLS_DEST="$CODEX_HOME/skills"
assert_support_dirs "$CODEX_SKILLS_DEST" "Codex"
assert_installed_link_resolves "$CODEX_SKILLS_DEST" "Codex"

echo "PASS: shared references/scripts sync to the real install destination for both CC and Codex"
