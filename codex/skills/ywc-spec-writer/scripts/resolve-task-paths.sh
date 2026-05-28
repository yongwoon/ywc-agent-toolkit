#!/usr/bin/env bash
# Resolves one or more task identifiers / patterns to absolute task directory
# paths. Searches both tasks/<id>/ (active) and tasks/completed/<id>/.
#
# Usage:
#   resolve-task-paths.sh <id-or-pattern> [<id-or-pattern> ...]
#
# Supported pattern shapes:
#   Single ID (full):    000002-010-api-user
#   ID prefix:           000002-010      (matches 000002-010-*)
#   Phase only:          000002          (matches 000002-*)
#   Glob:                '000002-*'      (shell-style wildcard; quote it)
#   Range (inclusive):   000002-010..000003-020
#                        (lexicographic on directory basename; spans phases)
#
# Output: one absolute path per line, deduplicated, sorted by basename.
# Quote glob patterns in the caller command. zsh and bash may expand or reject
# unquoted globs before this script can resolve them against task basenames.
# Exit 0: at least one task resolved.
# Exit 1: no arguments, or no task matched any provided pattern,
#         or tasks root not found.
#
# Environment overrides:
#   REPO_ROOT   - repository root (default: git rev-parse --show-toplevel)
#   TASKS_ROOT  - tasks root directory (default: $REPO_ROOT/tasks)

set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "ywc-spec-writer: resolve-task-paths requires at least one id or pattern" >&2
  exit 1
fi

REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
TASKS_ROOT="${TASKS_ROOT:-$REPO_ROOT/tasks}"

if [[ ! -d "$TASKS_ROOT" ]]; then
  echo "ywc-spec-writer: tasks root not found at $TASKS_ROOT" >&2
  exit 1
fi

declare -A path_by_base=()
while IFS= read -r dir; do
  [[ -z "$dir" ]] && continue
  base="$(basename "$dir")"
  # Prefer active tasks over completed when both exist with the same basename.
  if [[ -z "${path_by_base[$base]:-}" ]]; then
    path_by_base["$base"]="$dir"
  fi
done < <(
  find "$TASKS_ROOT" -mindepth 1 -maxdepth 1 -type d ! -name completed 2>/dev/null
  find "$TASKS_ROOT/completed" -mindepth 1 -maxdepth 1 -type d 2>/dev/null
)

if [[ ${#path_by_base[@]} -eq 0 ]]; then
  echo "ywc-spec-writer: no task directories found under $TASKS_ROOT" >&2
  exit 1
fi

mapfile -t sorted_bases < <(printf '%s\n' "${!path_by_base[@]}" | sort)

declare -A emitted=()
emit() {
  local base="$1"
  [[ -n "${emitted[$base]:-}" ]] && return
  emitted["$base"]=1
  # Defer output; printed after all args are processed to guarantee global sort.
}

resolve_range() {
  local start="$1" end="$2"
  local start_idx=-1 end_idx=-1 i
  for i in "${!sorted_bases[@]}"; do
    if [[ "${sorted_bases[$i]}" == "$start"* && $start_idx -lt 0 ]]; then
      start_idx=$i
    fi
    if [[ "${sorted_bases[$i]}" == "$end"* ]]; then
      end_idx=$i
    fi
  done
  if (( start_idx < 0 || end_idx < 0 || start_idx > end_idx )); then
    echo "ywc-spec-writer: range '$start..$end' resolved to no tasks" >&2
    return 1
  fi
  for (( i = start_idx; i <= end_idx; i++ )); do
    emit "${sorted_bases[$i]}"
  done
}

resolve_glob() {
  local pattern="$1" base matched=0
  for base in "${sorted_bases[@]}"; do
    # shellcheck disable=SC2053
    if [[ "$base" == $pattern ]]; then
      emit "$base"
      matched=1
    fi
  done
  if (( ! matched )); then
    echo "ywc-spec-writer: glob '$pattern' matched no tasks" >&2
    return 1
  fi
}

resolve_id() {
  local id="$1" base matched=0
  for base in "${sorted_bases[@]}"; do
    if [[ "$base" == "$id" || "$base" == "$id-"* ]]; then
      emit "$base"
      matched=1
    fi
  done
  if (( ! matched )); then
    echo "ywc-spec-writer: id '$id' matched no tasks" >&2
    return 1
  fi
}

any_matched=0
for arg in "$@"; do
  case "$arg" in
    *..*)
      start="${arg%%..*}"
      end="${arg#*..}"
      if [[ -z "$start" || -z "$end" ]]; then
        echo "ywc-spec-writer: invalid range '$arg' (expected START..END)" >&2
        continue
      fi
      resolve_range "$start" "$end" && any_matched=1 || true
      ;;
    *\**|*\?*|*\[*)
      resolve_glob "$arg" && any_matched=1 || true
      ;;
    *)
      resolve_id "$arg" && any_matched=1 || true
      ;;
  esac
done

if (( ! any_matched )); then
  exit 1
fi

# Emit deduplicated results in sorted order
mapfile -t matched_bases < <(printf '%s\n' "${!emitted[@]}" | sort)
for base in "${matched_bases[@]}"; do
  printf '%s\n' "${path_by_base[$base]}"
done
