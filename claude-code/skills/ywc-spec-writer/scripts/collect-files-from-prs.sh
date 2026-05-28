#!/usr/bin/env bash
# Collects changed file paths for one or more pull request numbers using the
# gh CLI. Output is suitable for piping into detect-affected-sections.sh.
#
# Usage:
#   collect-files-from-prs.sh <pr-number> [<pr-number> ...]
#
# Behavior:
#   - Validates each argument as a positive integer.
#   - Runs `gh pr diff <num> --name-only` for each PR.
#   - Merges results, deduplicates, sorts.
#   - Emits the union file list on stdout (one path per line).
#
# Exit codes:
#   0  one or more files emitted
#   1  no arguments, invalid PR number, gh CLI missing, gh request failed,
#      or no files in the union
#
# Side requirement:
#   gh CLI must be authenticated against the target repository.

set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "ywc-spec-writer: collect-files-from-prs requires at least one PR number" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ywc-spec-writer: gh CLI is required for --from-pr / --from-prs" >&2
  echo "  Install via: brew install gh   (or see https://cli.github.com/)" >&2
  exit 1
fi

declare -A seen_files=()

for pr in "$@"; do
  if ! [[ "$pr" =~ ^[1-9][0-9]*$ ]]; then
    echo "ywc-spec-writer: invalid PR number '$pr' (must be a positive integer)" >&2
    exit 1
  fi
  err_tmp="$(mktemp)"
  if ! diff_output="$(gh pr diff "$pr" --name-only 2>"$err_tmp")"; then
    echo "ywc-spec-writer: failed to fetch PR #$pr file list" >&2
    cat "$err_tmp" >&2
    rm -f "$err_tmp"
    exit 1
  fi
  rm -f "$err_tmp"
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    seen_files["$f"]=1
  done <<< "$diff_output"
done

if [[ ${#seen_files[@]} -eq 0 ]]; then
  echo "ywc-spec-writer: no files found across PRs: $*" >&2
  exit 1
fi

printf '%s\n' "${!seen_files[@]}" | sort
