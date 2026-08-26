#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
compact="$script_dir/compact-dependency-graph.py"
root=$(mktemp -d "${TMPDIR:-/tmp}/ywc-compact-parser.XXXXXX")
trap 'rm -rf "$root"' EXIT
fail() { echo "FAIL: $*" >&2; exit 1; }

tasks="$root/tasks"
mkdir -p "$tasks/completed/000001-010-legacy" "$tasks/completed/yk-000001-010-prefixed" \
  "$tasks/completed/000003-010-legacy-note" "$tasks/completed/yk-000003-010-prefixed-note"
cat >"$tasks/dependency-graph.md" <<'GRAPH'
# Dependency Graph

## Phase 000001 — legacy foundation
- `000001-010-legacy` — done

## Phase yk-000001 — prefixed foundation
- `yk-000001-010-prefixed` — done

## Phase 000002 — Done prerequisites
- `000002-010-still-open` — not done

## Parallel Execution Notes
- `000003-010` and `yk-000003-010` are complete.
GRAPH

python3 "$compact" "$tasks" >"$root/run.log"
grep -q 'compacted 2 phase(s), dropped 1 ' "$root/run.log" || fail "unexpected summary: $(cat "$root/run.log")"
grep -Fqx '## Phase 000001 — done' "$tasks/dependency-graph.md" || fail "legacy phase not compacted"
grep -Fqx '## Phase yk-000001 — done' "$tasks/dependency-graph.md" || fail "prefixed phase not compacted"
grep -Fqx '## Phase 000002 — Done prerequisites' "$tasks/dependency-graph.md" || fail "non-exact done heading compacted"
! grep -Fq '## Parallel Execution Notes' "$tasks/dependency-graph.md" || fail "completed notes not dropped"
cp "$tasks/dependency-graph.md" "$root/after.md"
python3 "$compact" "$tasks" | grep -Fx 'nothing to compact' >/dev/null
diff -u "$root/after.md" "$tasks/dependency-graph.md" >/dev/null || fail "compaction not idempotent"
echo "PASS: compactor parser fixtures"
