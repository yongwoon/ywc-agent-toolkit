#!/usr/bin/env bash
#
# teardown-docker.sh — tear down this worktree's Docker stack only and delete
# its port-persist file. Idempotent. See spec §A1.3 / §A1.8 / §A3.1.
#
# Usage:
#   teardown-docker.sh (--task-name <name> | --project-name <proj>) \
#     --worktree-path <dir> [--keep-volumes]
#
# Exit: 0 = teardown verified / nothing to do; 1 = compose down failed
#       (LEAKED_DOCKER_STACK — wave NON-blocking) / sanitize-empty
#       (programming error — wave BLOCKING).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
. "$SCRIPT_DIR/_lib.sh"

TASK_NAME=""
PROJECT_NAME=""
WORKTREE_PATH=""
KEEP_VOLUMES=0

die() { printf 'ywc-docker-isolate teardown: %s\n' "$1" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-name)     TASK_NAME="${2:-}"; shift 2 ;;
    --project-name)  PROJECT_NAME="${2:-}"; shift 2 ;;
    --worktree-path) WORKTREE_PATH="${2:-}"; shift 2 ;;
    --keep-volumes)  KEEP_VOLUMES=1; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done

[[ -n "$WORKTREE_PATH" ]] || die "--worktree-path is required"

# Resolve the COMPOSE_PROJECT_NAME — must match setup's sanitize exactly (§A1.W).
# SANITIZE_ERROR markers distinguish the wave-BLOCKING programming error from the
# wave-non-blocking LEAKED_DOCKER_STACK case (both exit 1 per the CLI Contract).
if [[ -n "$PROJECT_NAME" ]]; then
  PROJECT="$PROJECT_NAME"
elif [[ -n "$TASK_NAME" ]]; then
  SANITIZED=$(sanitize_task_name "$TASK_NAME") \
    || die "SANITIZE_ERROR: task name sanitizes to empty — refusing 'down' on an empty project: '$TASK_NAME'"
  PROJECT="${PROJECT_PREFIX}${SANITIZED}"
else
  die "one of --task-name or --project-name is required"
fi

# sanitize-empty / malformed guard (§A3.W): never run `down` on a degenerate or
# non-allowlisted project name (also guards a raw --project-name bypass).
[[ -n "$PROJECT" && "$PROJECT" != "$PROJECT_PREFIX" ]] \
  || die "SANITIZE_ERROR: empty/degenerate project name ('$PROJECT') — refusing teardown"
[[ "$PROJECT" =~ ^[a-z0-9_-]+$ ]] \
  || die "SANITIZE_ERROR: invalid project name ('$PROJECT') — must match ^[a-z0-9_-]+\$"

PERSIST="$WORKTREE_PATH/$PERSIST_FILE_NAME"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not installed — nothing to tear down ($PROJECT)"
  [[ -f "$PERSIST" ]] && rm -f "$PERSIST"
  exit 0
fi

# FR-5.2 / §A1.8: default `down --volumes`; --keep-volumes opts out.
DOWN_ARGS=(-p "$PROJECT" down --remove-orphans)
[[ $KEEP_VOLUMES -eq 0 ]] && DOWN_ARGS+=(--volumes)

if docker compose "${DOWN_ARGS[@]}" >/dev/null 2>&1; then
  echo "torn down: $PROJECT (volumes: $([[ $KEEP_VOLUMES -eq 0 ]] && echo removed || echo kept))"
  # delete persist only on successful down (§A3.1).
  [[ -f "$PERSIST" ]] && rm -f "$PERSIST"
  exit 0
fi

# down failed -> LEAKED_DOCKER_STACK; preserve persist for next pre-flight audit.
echo "LEAKED_DOCKER_STACK: $PROJECT — manual cleanup: docker compose -p $PROJECT down --volumes" >&2
exit 1
