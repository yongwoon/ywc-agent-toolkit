#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/codex/skills"
DEST_DIR="$ROOT_DIR/.codex-plugin/skills"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: Codex skill source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

if find "$SOURCE_DIR" -type l | grep -q .; then
  echo "ERROR: codex/skills contains symlinks; plugin packaging requires real files." >&2
  exit 1
fi

# codex/skills is the source of truth; .codex-plugin/skills is packaging output.
rm -rf "$DEST_DIR"
mkdir -p "$DEST_DIR"

(
  cd "$SOURCE_DIR"
  tar -cf - .
) | (
  cd "$DEST_DIR"
  tar -xf -
)

echo "Synced codex/skills -> .codex-plugin/skills"
