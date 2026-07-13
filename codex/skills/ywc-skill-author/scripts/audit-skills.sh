#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: audit-skills.sh --root <dir> --counterpart-root <dir> [--near-line-cap <1..500>]" >&2
  exit 2
}

root=""
counterpart_root=""
near_line_cap=450

while [ "$#" -gt 0 ]; do
  case "$1" in
    --root) [ "$#" -ge 2 ] || usage; root="$2"; shift 2 ;;
    --counterpart-root) [ "$#" -ge 2 ] || usage; counterpart_root="$2"; shift 2 ;;
    --near-line-cap) [ "$#" -ge 2 ] || usage; near_line_cap="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[ -n "$root" ] && [ -n "$counterpart_root" ] || usage
[ -d "$root" ] && [ -d "$counterpart_root" ] || { echo "error: roots must be existing directories" >&2; exit 2; }
case "$near_line_cap" in *[!0-9]*|'') usage ;; esac
[ "$near_line_cap" -ge 1 ] && [ "$near_line_cap" -le 500 ] || usage

section() {
  printf '## %s\n' "$1"
  if [ -s "$2" ]; then
    sed 's/^/- /' "$2"
  else
    echo "none"
  fi
  rm -f "$2"
}

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/audit-skills.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT
inventory="$tmpdir/inventory"
near_cap="$tmpdir/near-cap"
unpointed="$tmpdir/unpointed"
force_load="$tmpdir/force-load"
sibling_calls="$tmpdir/sibling-calls"
counterpart="$tmpdir/counterpart"

if [ -f "$root/SKILL.md" ]; then
  printf '%s\n' "$root"
else
  find "$root" -mindepth 1 -maxdepth 1 -type d -name 'ywc-*' -print | LC_ALL=C sort
fi | while IFS= read -r skill; do
  name="$(basename "$skill")"
  lines=0
  [ -f "$skill/SKILL.md" ] && lines="$(wc -l < "$skill/SKILL.md" | tr -d ' ')"
  printf '%s: %s lines\n' "$name" "$lines" >> "$inventory"
  [ "$lines" -ge "$near_line_cap" ] && printf '%s: %s lines\n' "$name" "$lines" >> "$near_cap"
  if [ -f "$counterpart_root/SKILL.md" ]; then
    [ "$(basename "$counterpart_root")" = "$name" ] || printf '%s\n' "$name" >> "$counterpart"
  else
    [ -d "$counterpart_root/$name" ] || printf '%s\n' "$name" >> "$counterpart"
  fi

  if [ -d "$skill/references" ]; then
    find "$skill/references" -type f -name '*.md' -print | LC_ALL=C sort | while IFS= read -r ref; do
      base="$(basename "$ref")"
      matches="$(find "$skill" -type f -name '*.md' ! -path "$ref" -exec grep -Fl "$base" {} + 2>/dev/null || true)"
      if [ -z "$matches" ]; then
        printf '%s/%s\n' "$name" "$base" >> "$unpointed"
      fi
    done
  fi

  if [ -f "$skill/SKILL.md" ]; then
    grep -nE '@ywc-[a-z0-9-]+' "$skill/SKILL.md" 2>/dev/null | sed "s#^#$name:#" >> "$force_load" || true
    grep -oE '[$/]ywc-[a-z0-9]+(-[a-z0-9]+)*' "$skill/SKILL.md" | sed 's#^[/$]##' | LC_ALL=C sort -u | while IFS= read -r called; do
      [ "$called" = "$name" ] || printf '%s -> %s\n' "$name" "$called" >> "$sibling_calls"
    done || true
  fi
done

for file in "$inventory" "$near_cap" "$unpointed" "$force_load" "$sibling_calls" "$counterpart"; do
  [ -s "$file" ] && LC_ALL=C sort -u "$file" -o "$file"
done

section "Inventory" "$inventory"
section "Near Line Cap" "$near_cap"
section "Unpointed Local References" "$unpointed"
section "Force-load References" "$force_load"
section "Declared Sibling Calls" "$sibling_calls"
section "Counterpart Coverage" "$counterpart"
