#!/usr/bin/env bash
# Compute the starting task number for a NEW batch.
#
# The task DIRECTORIES are the single source of truth for number allocation.
# Scans BOTH <tasks-dir> and <tasks-dir>/completed (executors archive finished
# tasks into completed/, so scanning the live dir alone risks reusing a number
# that was already used and archived). Takes the highest 6-digit PHASE across
# the union and returns the next phase with SEQUENCE reset to 010.
#
# Cross-check (advisory only): if <tasks-dir>/dependency-graph.md exists, the
# highest PHASE referenced by a full `NNNNNN-NNN-` task ID in it is parsed and
# compared against the directory result. A mismatch means the derived graph has
# drifted from the authoritative directories; a warning is emitted to STDERR but
# the directory result still wins. The graph NEVER overrides directory scan.
#
# ---------------------------------------------------------------------------
# INITIALS MODE (optional second argument)
# ---------------------------------------------------------------------------
# When <initials> is supplied (validated against ^[a-z0-9]{2,4}$) the allocator
# switches to a per-collaborator namespace. See
# claude-code/skills/references/initials-resolution.md#numbering-scope for the
# governing contract; the mechanics below are the single source of truth for
# HOW it is implemented (that reference deliberately delegates them here).
#
#   * Initials-scoped matching — only `<initials>-NNNNNN-NNN-` entries are
#     compared. Other collaborators' prefixes and unprefixed legacy entries are
#     out of scope for the maximum.
#   * Worktree union — every path from `git worktree list --porcelain` is
#     scanned at `<worktree>/<tasks-dir>` and `<worktree>/<tasks-dir>/completed`.
#     Missing paths are skipped silently; absence is not an error.
#   * Path normalization — <tasks-dir> is relativized against
#     `git rev-parse --show-toplevel` before being joined to a worktree path.
#     A path outside the repository disables the union entirely and only the
#     current worktree is scanned.
#   * Legacy seed — if the union yields ZERO entries carrying the resolved
#     prefix AND at least one unprefixed legacy entry exists, the first PHASE
#     seeds from `legacy max + 1`. This keeps `## Phase 000001` and
#     `## Phase yk-000001` from denoting different work at the same number in
#     one dependency-graph.md. A single prefixed entry disables the rule; a
#     DIFFERENT collaborator's prefix neither satisfies nor disables it.
#
# ---------------------------------------------------------------------------
# ATOMIC PHASE RESERVATION (initials mode only)
# ---------------------------------------------------------------------------
# Before the chosen PHASE N is emitted it is reserved with
# `git update-ref "refs/ywc/task-phase/<initials>/<phase>" HEAD ''`.
#
#   * CAS semantics — the EMPTY old-value argument means "create only if this
#     ref does not already exist". git performs the check and the write under
#     its own ref lock, so of two concurrent callers racing for the same PHASE
#     exactly one succeeds (exit 0) and the other is rejected (exit 128,
#     "cannot lock ref ...: reference already exists"). The loser increments N
#     and retries. Retries are capped at 100; exhaustion exits 1 and reports
#     the ref count, since reaching it implies a corrupted ledger rather than
#     ordinary contention.
#   * Refs are NEVER released. They are a local allocation ledger, not a lock.
#     A run that crashes after reserving BURNS its number: the next run's
#     directory scan cannot see the abandoned number, computes it again, and is
#     rejected into N+1. A burned number is strictly preferred over a reused
#     one, so no garbage collection is performed.
#   * refs/ywc/** lives outside refs/heads/, so reservations are never pushed,
#     never fetched, and never pollute `git branch -a`.
#   * SEPARATE CLONES ARE OUT OF SCOPE. Reservations live in the git common
#     dir, which linked worktrees share but a separate clone does not. The
#     initials namespace already removes the cross-person case; the residual
#     risk is one person running two clones concurrently, and it is accepted.
#   * `git update-ref` is used precisely because `flock(1)` is absent on macOS
#     (NFR2); it is platform-independent.
#
# With no <initials> argument every path above is skipped and behavior is
# byte-for-byte identical to the legacy allocator (NFR1).
#
# Usage:
#   bash .../next-task-number.sh [tasks-dir]
#   bash .../next-task-number.sh [tasks-dir] <initials>
#   bash .../next-task-number.sh [tasks-dir] --list-initials
#
# Output (STDOUT): the next batch prefix, e.g. "000017-010" (or "000001-010" when empty).
#   In --list-initials mode: one "<initials> <count>" line per distinct prefix
#   found across the union (empty output when none exist).
# Warnings (STDERR): drift notice when the dependency graph disagrees.
set -euo pipefail

TASKS_DIR="${1:-tasks}"
ARG2="${2:-}"

INITIALS=""
LIST_MODE=0
if [ "$ARG2" = "--list-initials" ]; then
  LIST_MODE=1
elif [ -n "$ARG2" ]; then
  if ! [[ "$ARG2" =~ ^[a-z0-9]{2,4}$ ]]; then
    printf 'ERROR: invalid initials %s — must match ^[a-z0-9]{2,4}$ (2-4 lowercase alphanumeric characters).\n' \
      "$ARG2" >&2
    exit 1
  fi
  INITIALS="$ARG2"
fi

# --- worktree union path normalization (A6) ---------------------------------
# REL_TASKS_DIR is <tasks-dir> expressed relative to the repository root, which
# is the only form safe to join onto another worktree's path. UNION_OK stays 0
# whenever that normalization is impossible (not a git repo, unresolvable
# parent directory, or a path outside the repository) — the union is then
# skipped and only the current worktree is scanned.
REPO_TOP=""
REL_TASKS_DIR=""
UNION_OK=0
normalize_tasks_dir() {
  local parent abs
  REPO_TOP="$(git rev-parse --show-toplevel 2>/dev/null)" || return 0
  [ -n "$REPO_TOP" ] || return 0
  parent="$(CDPATH='' cd -- "$(dirname -- "$TASKS_DIR")" 2>/dev/null && pwd)" || return 0
  [ -n "$parent" ] || return 0
  abs="${parent%/}/$(basename -- "$TASKS_DIR")"
  if [ "$abs" = "$REPO_TOP" ]; then
    REL_TASKS_DIR="."
    UNION_OK=1
  elif [ "${abs#"$REPO_TOP"/}" != "$abs" ]; then
    REL_TASKS_DIR="${abs#"$REPO_TOP"/}"
    UNION_OK=1
  fi
}

# Directories to scan, one per line: the current worktree's <tasks-dir> pair
# plus the same pair under every OTHER linked worktree. The current worktree is
# excluded from the git-reported list because it is already covered by the
# cwd-relative entries, and scanning it twice would double the AC12 counts.
union_dirs() {
  printf '%s\n%s\n' "$TASKS_DIR" "$TASKS_DIR/completed"
  [ "$UNION_OK" -eq 1 ] || return 0
  local line wt
  while IFS= read -r line; do
    case "$line" in
      'worktree '*) wt="${line#worktree }" ;;
      *) continue ;;
    esac
    if [ "$wt" = "$REPO_TOP" ]; then
      continue
    fi
    printf '%s\n%s\n' "$wt/$REL_TASKS_DIR" "$wt/$REL_TASKS_DIR/completed"
  done < <(git worktree list --porcelain 2>/dev/null || true)
}

# --- initials advisory list (AC12 / spec A9) --------------------------------
# Emits every initials prefix occurrence found across the union so the caller
# can build the "<initials> already has N task(s)" confirmation notice. Purely
# informational: this never blocks an allocation.
list_prefix_occurrences() {
  local dir entry name
  while IFS= read -r dir; do
    [ -d "$dir" ] || continue
    for entry in "$dir"/*; do
      [ -e "$entry" ] || continue
      name="$(basename "$entry")"
      if [[ "$name" =~ ^([a-z0-9]{2,4})-[0-9]{6}-[0-9]{3}- ]]; then
        printf '%s\n' "${BASH_REMATCH[1]}"
      fi
    done
  done < <(union_dirs)
}

if [ "$LIST_MODE" -eq 1 ]; then
  normalize_tasks_dir
  list_prefix_occurrences | sort | uniq -c | awk '{ print $2, $1 }'
  exit 0
fi

max=0
legacy_max=0
legacy_count=0
prefixed_count=0

if [ -n "$INITIALS" ]; then
  TASK_RE="^${INITIALS}-([0-9]{6})-[0-9]{3}-"
  normalize_tasks_dir
else
  TASK_RE="^([0-9]{6})-[0-9]{3}-"
fi
LEGACY_RE="^([0-9]{6})-[0-9]{3}-"

scan() {
  local dir="$1" entry name phase
  [ -d "$dir" ] || return 0
  for entry in "$dir"/*; do
    [ -e "$entry" ] || continue
    name="$(basename "$entry")"
    if [[ "$name" =~ $TASK_RE ]]; then
      phase=$((10#${BASH_REMATCH[1]}))
      prefixed_count=$((prefixed_count + 1))
      # Use `if` (not `(( )) && ...`): under `set -e` a false `(( ))` returns 1
      # as the loop's last command, which would exit before the final printf.
      if (( phase > max )); then max=$phase; fi
    fi
    # Legacy tally feeds the seed rule and is only consulted in initials mode.
    if [ -n "$INITIALS" ] && [[ "$name" =~ $LEGACY_RE ]]; then
      phase=$((10#${BASH_REMATCH[1]}))
      legacy_count=$((legacy_count + 1))
      if (( phase > legacy_max )); then legacy_max=$phase; fi
    fi
  done
}

if [ -n "$INITIALS" ]; then
  while IFS= read -r dir; do
    scan "$dir"
  done < <(union_dirs)
else
  scan "$TASKS_DIR"
  scan "$TASKS_DIR/completed"
fi

# Legacy seed (initials mode only): the very first batch of a new namespace
# starts above the highest legacy PHASE so the two numbering schemes never
# collide inside one dependency-graph.md. One prefixed entry disables this.
if [ -n "$INITIALS" ] && (( prefixed_count == 0 )) && (( legacy_count > 0 )); then
  max=$legacy_max
fi

# Advisory cross-check against the derived dependency graph. Only full task IDs
# of the form NNNNNN-NNN- count; bare "depends on 000001" phase references (no
# SEQUENCE) are intentionally excluded so partial mentions never inflate the max.
# In initials mode the scan is scoped to the same prefix, and the comparison is
# skipped outright when the graph holds zero entries for those initials —
# otherwise a graph carrying only legacy ids would warn on every single run.
graph="$TASKS_DIR/dependency-graph.md"
if [ -f "$graph" ]; then
  graph_max=0
  graph_hits=0
  if [ -n "$INITIALS" ]; then
    graph_re="${INITIALS}-[0-9]{6}-[0-9]{3}-"
    graph_field=2
  else
    graph_re='[0-9]{6}-[0-9]{3}-'
    graph_field=1
  fi
  while IFS= read -r phase; do
    [ -n "$phase" ] || continue
    graph_hits=$((graph_hits + 1))
    phase=$((10#$phase))
    if (( phase > graph_max )); then graph_max=$phase; fi
  done < <(grep -oE "$graph_re" "$graph" | cut -d- -f"$graph_field" | sort -u)
  if [ -z "$INITIALS" ] || (( graph_hits > 0 )); then
    if (( graph_max != max )); then
      printf 'WARN: dependency-graph.md highest PHASE (%06d) disagrees with task directories (%06d); directories win. Graph may have drifted — reconcile before generating.\n' \
        "$graph_max" "$max" >&2
    fi
  fi
fi

next=$((max + 1))

# Atomic reservation — see the ATOMIC PHASE RESERVATION block above.
reserve() {
  local phase="$1" attempt=0 ref count
  while :; do
    ref="$(printf 'refs/ywc/task-phase/%s/%06d' "$INITIALS" "$phase")"
    if git update-ref "$ref" HEAD '' 2>/dev/null; then
      printf '%d\n' "$phase"
      return 0
    fi
    attempt=$((attempt + 1))
    if (( attempt >= 100 )); then
      count="$(git for-each-ref --format='%(refname)' "refs/ywc/task-phase/$INITIALS/" 2>/dev/null | wc -l | tr -d '[:space:]')"
      printf 'ERROR: PHASE reservation exhausted %d retries for initials %s; refs/ywc/task-phase/%s/ holds %s ref(s). Reaching this cap implies ledger corruption — inspect it before retrying.\n' \
        "$attempt" "$INITIALS" "$INITIALS" "$count" >&2
      return 1
    fi
    phase=$((phase + 1))
  done
}

if [ -n "$INITIALS" ]; then
  next="$(reserve "$next")"
fi

printf '%06d-010\n' "$next"
