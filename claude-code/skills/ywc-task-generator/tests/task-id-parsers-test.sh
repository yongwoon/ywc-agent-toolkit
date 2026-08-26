#!/usr/bin/env bash
# Fixture suite for the optional INITIALS prefix in the task id grammar.
#
# Covers scaffold-task-dir.sh name validation and compact-dependency-graph.py
# on a graph where legacy unprefixed and prefixed ids coexist. The compactor
# rewrites dependency-graph.md in place, so a partial-match regression corrupts
# data silently — these assertions are the loud version of that failure.
set -euo pipefail

skill_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
scaffold="$skill_dir/scripts/scaffold-task-dir.sh"
compact="$skill_dir/scripts/compact-dependency-graph.py"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/task-id-parsers-test.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# --- scaffold-task-dir.sh name validation (AC8) ------------------------------
scaffold_out="$tmpdir/scaffold"
mkdir -p "$scaffold_out"

set +e
bash "$scaffold" yk-000001-010-db-x --out "$scaffold_out" > "$tmpdir/prefixed.log" 2>&1
prefixed_status=$?
bash "$scaffold" 000001-010-db-x --out "$scaffold_out" > "$tmpdir/legacy.log" 2>&1
legacy_status=$?
bash "$scaffold" TOOLONG-000001-010-db-x --out "$scaffold_out" > "$tmpdir/toolong.log" 2>&1
toolong_status=$?
set -e

[ "$prefixed_status" -eq 0 ] || fail "prefixed task name rejected (exit $prefixed_status)"
[ -f "$scaffold_out/yk-000001-010-db-x/task.md" ] || fail "prefixed task dir not scaffolded"
! grep -q 'warning:' "$tmpdir/prefixed.log" || fail "prefixed task name emitted a shape warning"

[ "$legacy_status" -eq 0 ] || fail "legacy task name rejected (exit $legacy_status)"
[ -f "$scaffold_out/000001-010-db-x/task.md" ] || fail "legacy task dir not scaffolded"
! grep -q 'warning:' "$tmpdir/legacy.log" || fail "legacy task name emitted a shape warning"

[ "$toolong_status" -eq 1 ] || fail "over-length initials prefix accepted (exit $toolong_status)"
[ ! -e "$scaffold_out/TOOLONG-000001-010-db-x" ] || fail "rejected name still created a directory"
grep -q 'invalid initials prefix' "$tmpdir/toolong.log" || fail "no initials-prefix error message"

# --- compact-dependency-graph.py mixed-format fixture (AC6) ------------------
tasks="$tmpdir/tasks"
mkdir -p \
  "$tasks/completed/000001-010-db-alpha" \
  "$tasks/completed/000001-020-api-beta" \
  "$tasks/completed/yk-000001-010-db-alpha" \
  "$tasks/completed/yk-000001-020-api-beta" \
  "$tasks/completed/000002-010-ui-gamma" \
  "$tasks/completed/yk-000002-010-ui-gamma"

graph="$tasks/dependency-graph.md"
cat > "$graph" <<'GRAPH'
# Dependency Graph

## Phase 000001 — legacy foundation

- `000001-010-db-alpha` — depends on nothing
- `000001-020-api-beta` — depends on `000001-010`

## Phase yk-000001 — prefixed foundation

- `yk-000001-010-db-alpha` — depends on nothing
- `yk-000001-020-api-beta` — depends on `yk-000001-010`

## Phase 000002 — mixed surface

- `000002-010-ui-gamma` — completed
- `yk-000002-010-ui-gamma` — owned by phase yk-000002, not by this phase
- `000002-020-lib-delta` — not done yet

## Parallel Execution Notes

- 000001-010 and yk-000001-010 are independent.

## Open Questions

- none
GRAPH

python3 "$compact" "$tasks" > "$tmpdir/compact-run1.log"
grep -q 'compacted 2 phase(s), dropped 1 ' "$tmpdir/compact-run1.log" \
  || fail "unexpected run-1 summary: $(cat "$tmpdir/compact-run1.log")"

# Legacy and prefixed phases compact independently, never merged into one.
grep -Fqx '## Phase 000001 — done' "$graph" || fail "legacy phase not compacted"
grep -Fqx '## Phase yk-000001 — done' "$graph" || fail "prefixed phase not compacted"

legacy_completed="$(grep -F -A1 '## Phase 000001 — done' "$graph" | tail -1)"
case "$legacy_completed" in
  *yk-*) fail "legacy phase claimed prefixed ids: $legacy_completed" ;;
esac
case "$legacy_completed" in
  *'`000001-010-db-alpha`'*'`000001-020-api-beta`'*) : ;;
  *) fail "legacy phase lost its own ids: $legacy_completed" ;;
esac

prefixed_completed="$(grep -F -A1 '## Phase yk-000001 — done' "$graph" | tail -1)"
case "$prefixed_completed" in
  *'`yk-000001-010-db-alpha`'*'`yk-000001-020-api-beta`'*) : ;;
  *) fail "prefixed phase lost its own ids: $prefixed_completed" ;;
esac

# No prefixed id was partially matched and rewritten down to its legacy form.
grep -Fq 'yk-000001-010-db-alpha' "$graph" || fail "yk-000001-010-db-alpha vanished from the graph"
grep -Fq '`yk-000002-010-ui-gamma`' "$graph" || fail "yk-000002-010-ui-gamma vanished from the graph"

# A phase with outstanding work stays untouched, and a foreign-prefix bullet
# inside it is not counted as owned by that phase.
grep -Fqx '## Phase 000002 — mixed surface' "$graph" || fail "incomplete phase was compacted"
grep -Fq '`000002-020-lib-delta`' "$graph" || fail "outstanding task id dropped"

# The fully completed notes section is droppable through both id forms.
! grep -Fq '## Parallel Execution Notes' "$graph" || fail "completed notes section was kept"

# --- idempotency -------------------------------------------------------------
cp "$graph" "$tmpdir/after-run1.md"
python3 "$compact" "$tasks" > "$tmpdir/compact-run2.log"
grep -Fqx 'nothing to compact' "$tmpdir/compact-run2.log" \
  || fail "second run was not a no-op: $(cat "$tmpdir/compact-run2.log")"
diff -u "$tmpdir/after-run1.md" "$graph" || fail "compaction is not idempotent"

echo "PASS: task-id-parsers-test.sh"
