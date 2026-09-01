#!/usr/bin/env bash
# Resolve collaborator initials for task-ID namespacing.
#
# Precedence chain (see claude-code/skills/references/initials-resolution.md:22-50):
#   1. --initials <s> flag, validated against ^[a-z0-9]{2,4}$.
#   2. Derive from `git config user.email` local-part (before '@'), falling
#      back to `git config user.name` when email is unset.
#
# Rung 2 of the reference's precedence chain (a project `## Task Initials`
# section in CLAUDE.md) is deliberately out of scope here: this script only
# resolves flag-vs-derivation, never reads project files. It also NEVER
# prompts and NEVER writes anything -- presenting the derived candidate for
# confirmation and caching it is the calling skill's job.
#
# Output (exactly one line on stdout, exit 0 on every path):
#   RESOLVED <initials>       -- rung 1 (explicit flag), already valid
#   NEEDS_CONFIRM <candidate> -- derived from git config, unconfirmed
#   NONE                      -- nothing derivable
#
# Usage:
#   bash resolve-initials.sh [--initials <s>]
set -euo pipefail

INITIALS_RE='^[a-z0-9]{2,4}$'
INITIALS_FLAG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --initials)
      INITIALS_FLAG="${2:-}"
      shift
      [ $# -gt 0 ] && shift
      ;;
    *) shift ;;
  esac
done

# Rung 1: an explicit flag that already validates wins outright. A present
# but invalid flag is not a hard error (this script never errors) -- it just
# fails to satisfy rung 1, so resolution falls through to derivation.
if [ -n "$INITIALS_FLAG" ] && [[ "$INITIALS_FLAG" =~ $INITIALS_RE ]]; then
  echo "RESOLVED $INITIALS_FLAG"
  exit 0
fi

# Rung 3: derive from git config. `git config` exits non-zero when a key is
# unset; swallow that under `set -e` and treat it as empty.
EMAIL="$(git config user.email 2>/dev/null || true)"
if [ -n "$EMAIL" ]; then
  # Local-part before '@'.
  LOCAL_PART="${EMAIL%%@*}"
else
  # user.name fallback: use the raw value untouched. '@' is not a separator
  # here -- trimming it would silently drop real name characters (e.g. a
  # user.name of "a@b" must stay "a@b", not become "a").
  LOCAL_PART="$(git config user.name 2>/dev/null || true)"
fi

if [ -z "$LOCAL_PART" ]; then
  echo "NONE"
  exit 0
fi

# Split on '.', '_', '-' and join each segment's lowercased first character
# (e.g. "yongwoon.kim" -> "yk").
CANDIDATE=""
OLDIFS="$IFS"
IFS='._-'
set -o noglob
# shellcheck disable=SC2086 # intentional word-splitting on the IFS set above
set -- $LOCAL_PART
set +o noglob
IFS="$OLDIFS"
for segment in "$@"; do
  [ -n "$segment" ] || continue
  first_char="${segment:0:1}"
  CANDIDATE="${CANDIDATE}$(printf '%s' "$first_char" | tr '[:upper:]' '[:lower:]')"
done

if [ "${#CANDIDATE}" -lt 2 ]; then
  # Fewer than 2 chars from the join: fall back to the first 2-4 lowercase
  # alphanumeric characters of the original local-part/name instead.
  LOWERED="$(printf '%s' "$LOCAL_PART" | tr '[:upper:]' '[:lower:]')"
  ALNUM="$(printf '%s' "$LOWERED" | tr -cd 'a-z0-9')"
  CANDIDATE="${ALNUM:0:4}"
fi

if [ -z "$CANDIDATE" ] || ! [[ "$CANDIDATE" =~ $INITIALS_RE ]]; then
  # Entirely non-alphanumeric source, too short, or the join produced
  # something outside 2-4 chars (e.g. 5-segment names) -- derivation fails.
  echo "NONE"
  exit 0
fi

echo "NEEDS_CONFIRM $CANDIDATE"
exit 0
