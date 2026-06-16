#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/codex/skills"
PLUGIN_ROOT="${CODEX_PLUGIN_ROOT:-$ROOT_DIR/plugins/ywc-agent-toolkit}"
DEST_DIR="${CODEX_PLUGIN_DEST_DIR:-$PLUGIN_ROOT/skills}"
MANIFEST_SRC="$ROOT_DIR/.codex-plugin/plugin.json"
MANIFEST_DEST="${CODEX_PLUGIN_MANIFEST_DEST:-$PLUGIN_ROOT/.codex-plugin/plugin.json}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: Codex skill source directory not found: $SOURCE_DIR" >&2
  exit 1
fi

if [[ ! -f "$MANIFEST_SRC" ]]; then
  echo "ERROR: Codex plugin manifest not found: $MANIFEST_SRC" >&2
  exit 1
fi

if find "$SOURCE_DIR" -type l | grep -q .; then
  echo "ERROR: codex/skills contains symlinks; plugin packaging requires real files." >&2
  exit 1
fi

# codex/skills is the source of truth; plugins/ywc-agent-toolkit is packaging output.
mkdir -p "$(dirname "$MANIFEST_DEST")"
cp "$MANIFEST_SRC" "$MANIFEST_DEST"

rm -rf "$DEST_DIR"
mkdir -p "$DEST_DIR"

(
  cd "$SOURCE_DIR"
  tar -cf - .
) | (
  cd "$DEST_DIR"
  tar -xf -
)

while IFS= read -r -d '' file; do
  tmp_file="$file.tmp"
  if mode="$(stat -f '%Lp' "$file" 2>/dev/null)"; then
    :
  else
    mode="$(stat -c '%a' "$file")"
  fi
  sed -E \
    -e "s#bash codex/skills/([^[:space:]]+)#bash \"\${CODEX_HOME:-\$HOME/.codex}/skills/\\1\"#g" \
    -e "s#python codex/skills/([^[:space:]]+)#python \"\${CODEX_HOME:-\$HOME/.codex}/skills/\\1\"#g" \
    -e "s#cp codex/skills/([^[:space:]]+)#cp \"\${CODEX_HOME:-\$HOME/.codex}/skills/\\1\"#g" \
    "$file" > "$tmp_file"
  chmod "$mode" "$tmp_file"
  mv "$tmp_file" "$file"
done < <(find "$DEST_DIR" -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' \) -print0)

echo "Synced $MANIFEST_SRC -> $MANIFEST_DEST"
echo "Synced codex/skills -> $DEST_DIR"
