#!/usr/bin/env bash
#
# audit-docker-stacks.sh — report Docker stacks still running for the expected
# tasks (e.g. left over by an aborted run that occupy the deterministic ports).
# See spec §A1.1 / §A2.W / §A3.W.
#
# Usage:
#   audit-docker-stacks.sh --expect task1,task2,... [--prune]
#
# Detection is by stdout NON-EMPTY (not exit code): `docker compose -p <p> ps -q`
# returns exit 0 whether or not containers exist (§A2.W).
#
# Exit: ALWAYS 0. A residual stack is signalled by non-empty stdout; the caller
#       (parallel-executor pre-flight) decides whether to abort the run.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
. "$SCRIPT_DIR/_lib.sh"

EXPECT=""
PRUNE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --expect) EXPECT="${2:-}"; shift 2 ;;
    --prune)  PRUNE=1; shift ;;
    *) printf 'ywc-docker-isolate audit: unknown argument: %s\n' "$1" >&2; exit 0 ;;
  esac
done

if [[ -z "$EXPECT" ]]; then
  # nothing to audit — not an error (exit 0, empty stdout).
  exit 0
fi

if ! command -v docker >/dev/null 2>&1; then
  # no docker -> nothing can be residual; stay silent, exit 0.
  exit 0
fi

# stack_container_ids <project> — echo running/stopped container IDs for a project.
# Uses label filter so no local compose file is required.
stack_container_ids() {
  local project="$1"
  docker ps -aq --filter "label=com.docker.compose.project=${project}" 2>/dev/null
}

IFS=',' read -r -a TASKS <<< "$EXPECT"
for task in "${TASKS[@]}"; do
  [[ -n "$task" ]] || continue
  sanitized=$(sanitize_task_name "$task") || continue
  project="${PROJECT_PREFIX}${sanitized}"
  ids=$(stack_container_ids "$project" || true)
  if [[ -n "$ids" ]]; then
    count=$(printf '%s\n' "$ids" | grep -c .)
    if [[ $PRUNE -eq 1 ]]; then
      # --prune: tear the residual stack down (down --volumes). Fall back to a
      # per-id `docker rm -f` loop (portable; avoids GNU-only `xargs -r` and
      # whitespace word-splitting on malformed IDs).
      if ! docker compose -p "$project" down --volumes --remove-orphans >/dev/null 2>&1; then
        printf '%s\n' "$ids" | while IFS= read -r id; do
          [[ -n "$id" ]] && docker rm -f "$id" >/dev/null 2>&1 || true
        done
      fi
      echo "pruned residual stack: $project ($count container(s))"
    else
      # report only (fail-loud is the caller's job); non-empty stdout = residual.
      echo "RESIDUAL_DOCKER_STACK: $project ($count container(s))"
    fi
  fi
done

exit 0
