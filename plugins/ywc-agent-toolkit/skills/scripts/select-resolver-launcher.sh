#!/usr/bin/env bash
# Resolve the trusted path to resolve-bundle-executable.sh: the installed
# bundle first, an explicitly authorized development source root second.
# Every SKILL.md caller invokes this script instead of duplicating the
# selection logic inline, so the trust checks below are enforced exactly
# once for all callers.
set -euo pipefail

EXPECTED_ORIGIN_PATTERN='^(https://github\.com/yongwoon/ywc-agent-toolkit(\.git)?|git@github\.com:yongwoon/ywc-agent-toolkit(\.git)?|ssh://git@github\.com/yongwoon/ywc-agent-toolkit(\.git)?)$'

blocked() {
  echo "BLOCKED: $1" >&2
  exit 3
}

# Fully resolve a path's own symlink chain (not just its parent directory),
# then canonicalize the containing directory. Returns the canonical absolute
# path of the final regular file/dir on stdout, or fails.
canonicalize_file() {
  local target="$1" link dir base
  while [ -L "$target" ]; do
    link="$(readlink -- "$target")" || return 1
    case "$link" in
      /*) target="$link" ;;
      *) target="$(dirname -- "$target")/$link" ;;
    esac
  done
  dir="$(cd -- "$(dirname -- "$target")" 2>/dev/null && pwd -P)" || return 1
  base="$(basename -- "$target")"
  printf '%s/%s\n' "$dir" "$base"
}

is_contained() {
  case "$1" in
    "$2"/*) return 0 ;;
    *) return 1 ;;
  esac
}

# --- Installed bundle (first) ---
CODEX_SKILLS_ROOT="$(cd -- "${CODEX_HOME:-$HOME/.codex}/skills" 2>/dev/null && pwd -P)" || CODEX_SKILLS_ROOT=""
if [ -n "$CODEX_SKILLS_ROOT" ]; then
  INSTALLED_CANDIDATE="$CODEX_SKILLS_ROOT/scripts/resolve-bundle-executable.sh"
  if [ -f "$INSTALLED_CANDIDATE" ]; then
    RESOLVED="$(canonicalize_file "$INSTALLED_CANDIDATE")" || blocked "installed resolver launcher cannot be canonicalized"
    is_contained "$RESOLVED" "$CODEX_SKILLS_ROOT" || blocked "installed resolver launcher escapes the installed skills tree"
    [ -f "$RESOLVED" ] && [ -r "$RESOLVED" ] || blocked "installed resolver launcher is not a readable file"
    printf '%s\n' "$RESOLVED"
    exit 0
  fi
fi

# --- Development source fallback (second, explicit opt-in only) ---
[ "${YWC_BUNDLE_DEVELOPMENT:-}" = "1" ] || blocked "installed Codex resolver launcher is missing; development source fallback requires YWC_BUNDLE_DEVELOPMENT=1 and YWC_BUNDLE_SOURCE_ROOT"
[ -n "${YWC_BUNDLE_SOURCE_ROOT:-}" ] || blocked "YWC_BUNDLE_SOURCE_ROOT is required for development fallback"

SOURCE_ROOT="$(cd -- "$YWC_BUNDLE_SOURCE_ROOT" 2>/dev/null && pwd -P)" || blocked "YWC_BUNDLE_SOURCE_ROOT is not accessible"
SOURCE_TOPLEVEL="$(git -C "$SOURCE_ROOT" rev-parse --show-toplevel 2>/dev/null)" || blocked "YWC_BUNDLE_SOURCE_ROOT is not a Git repository"
[ "$SOURCE_TOPLEVEL" = "$SOURCE_ROOT" ] || blocked "YWC_BUNDLE_SOURCE_ROOT must be the canonical Git root, not a subdirectory"
SOURCE_ORIGIN="$(git -C "$SOURCE_ROOT" config --get remote.origin.url 2>/dev/null)" || blocked "source origin cannot be read"
[[ "$SOURCE_ORIGIN" =~ $EXPECTED_ORIGIN_PATTERN ]] || blocked "source origin is not the authorized ywc-agent-toolkit repository"

SOURCE_SKILLS="$(cd -- "$SOURCE_ROOT/codex/skills" 2>/dev/null && pwd -P)" || blocked "source root is missing the expected codex/skills layout"
SOURCE_CANDIDATE="$SOURCE_SKILLS/scripts/resolve-bundle-executable.sh"
[ -f "$SOURCE_CANDIDATE" ] || blocked "source resolver launcher is missing"
RESOLVED="$(canonicalize_file "$SOURCE_CANDIDATE")" || blocked "source resolver launcher cannot be canonicalized"
is_contained "$RESOLVED" "$SOURCE_SKILLS" || blocked "source resolver launcher escapes the source skills tree"
[ -f "$RESOLVED" ] && [ -r "$RESOLVED" ] || blocked "source resolver launcher is not a readable file"

printf '%s\n' "$RESOLVED"
