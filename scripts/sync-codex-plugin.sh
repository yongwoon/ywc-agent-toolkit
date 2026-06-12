#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/codex/skills"
DEST_DIR="${CODEX_PLUGIN_DEST_DIR:-$ROOT_DIR/.codex-plugin/skills}"

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

echo "Synced codex/skills -> $DEST_DIR"
