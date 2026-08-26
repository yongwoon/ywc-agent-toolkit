#!/usr/bin/env bash
set -euo pipefail

# Bounded contract fixture. The generator is instruction-driven in this
# repository, so textual checks prove the documented behavior and the
# temporary Git repository proves the shared reservation primitive.
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
skill="$script_dir/../SKILL.md"
reference="$script_dir/../references/collaborator-initials.md"
fail() { echo "FAIL: $*" >&2; exit 1; }
must_have() { grep -Fq -- "$2" "$1" || fail "$3"; }

must_have "$skill" 'resolve validated initials before any scan' \
  'initials are not resolved before discovery'
must_have "$skill" 'exclusive lock rooted in the repository common Git directory' \
  'transaction-wide common-Git lock is missing'
must_have "$skill" 'complete task-artifact/dependency-graph writes' \
  'lock does not cover complete graph writes'
must_have "$reference" 'Malformed or unsupported config tiers are skipped' \
  'malformed config-tier fallback is missing'
must_have "$reference" '1. Explicit `--initials <value>`' \
  'explicit precedence tier is missing'
must_have "$reference" '2. Project `.codex/ywc.json` `initials`' \
  'project precedence tier is missing'
must_have "$reference" '3. User `~/.codex/ywc.json` `initials`' \
  'user precedence tier is missing'
must_have "$reference" 'Interactive derivation is only a proposal' \
  'invalid/empty interactive derivation contract is missing'
must_have "$reference" 'absolute path' \
  'safe repository-relative tasks path contract is missing'
must_have "$reference" 'corresponding linked-worktree directories' \
  'linked-worktree source coverage is missing'
must_have "$skill" 'Empty owned scope starts at' \
  'empty initials-scoped maximum is missing'
must_have "$reference" 'collision: retain the existing ref' \
  'reservation retry contract is missing'
must_have "$reference" 'NEEDS_CONTEXT' \
  'missing-initials contract is missing'
scan_line=$(grep -n '^1\. Scan the resolved graph' "$reference" | cut -d: -f1)
select_line=$(grep -n '^2\. Select the next candidate' "$reference" | cut -d: -f1)
reserve_line=$(grep -n '^3\. Compare-and-create' "$reference" | cut -d: -f1)
write_line=$(grep -n '^4\. Write the complete task artifact batch' "$reference" | cut -d: -f1)
[ "$scan_line" -lt "$select_line" ] && [ "$select_line" -lt "$reserve_line" ] \
  && [ "$reserve_line" -lt "$write_line" ] \
  || fail "scan/select/reserve/write transaction order is not documented"
context_line=$(grep -n 'return before graph compaction' "$reference" | cut -d: -f1)
artifact_line=$(grep -n 'Only after reservation succeeds' "$reference" | cut -d: -f1)
[ "$context_line" -lt "$artifact_line" ] \
  || fail "NEEDS_CONTEXT is not documented before artifact writes"

root=$(mktemp -d "${TMPDIR:-/tmp}/ywc-initials-reservation.XXXXXX")
trap 'rm -rf "$root"' EXIT
git -C "$root" init -q
git -C "$root" config user.email test@example.com
git -C "$root" config user.name Test
git -C "$root" commit --allow-empty -qm fixture
git -C "$root" branch linked
git -C "$root" worktree add -q "$root/linked" linked

# Cover graph, active, completed, and linked-worktree sources in one fixture.
mkdir -p "$root/tasks/completed/yk-000002-010-done" \
  "$root/tasks/yk-000004-010-active" \
  "$root/linked/tasks/yk-000005-010-linked-active" \
  "$root/linked/tasks/completed/yk-000006-010-linked-done"
cat >"$root/tasks/dependency-graph.md" <<'GRAPH'
## Phase yk-000003
- yk-000003-010-graph
- js-000099-010-other
- 000098-010-legacy
GRAPH
cat >"$root/linked/tasks/dependency-graph.md" <<'GRAPH'
## Phase yk-000006
- yk-000006-010-linked-graph
GRAPH

# Safe repository-relative paths accept tasks and reject absolute/escaping paths.
case tasks in /*|../*|*/../*|*/..|'') fail "safe relative path rejected" ;; esac
for unsafe in /tmp/tasks ../tasks tasks/../../outside; do
  case "$unsafe" in /*|../*|*/../*|*/..) : ;; *) fail "unsafe path accepted: $unsafe" ;; esac
done

# Only yk-prefixed IDs contribute. js and legacy values are deliberately larger.
max=0
while IFS= read -r phase; do
  [ "$phase" -gt "$max" ] && max=$phase
done < <(
  find "$root/tasks" "$root/linked/tasks" -print |
    sed -nE 's#^.*/yk-([0-9]{6})-[0-9]{3}-.*$#\1#p'
  sed -nE 's/^.*yk-([0-9]{6})-[0-9]{3}-.*$/\1/p' \
    "$root/tasks/dependency-graph.md" "$root/linked/tasks/dependency-graph.md"
)
test "$max" = 000006 || fail "scoped maximum expected 000006, got $max"
test "$((max + 1))" = 7 || fail "next scoped phase is not 7"

# Two allocators race for 7. One wins; the other retries 8. Refs are retained.
zero=0000000000000000000000000000000000000000
value=$(git -C "$root" hash-object -w -t blob /dev/null)
reserve() {
  candidate=$1
  while [ "$candidate" -le 8 ]; do
    ref="refs/ywc/task-phase/yk/$(printf '%06d' "$candidate")"
    if git -C "$root" update-ref "$ref" "$value" "$zero" 2>/dev/null; then
      printf '%s\n' "$candidate"
      return 0
    fi
    candidate=$((candidate + 1))
  done
  return 1
}
reserve 7 >"$root/winner-a" & pid_a=$!
reserve 7 >"$root/winner-b" & pid_b=$!
wait "$pid_a"; wait "$pid_b"
first=$(cat "$root/winner-a")
second=$(cat "$root/winner-b")
test "$first" != "$second" || fail "concurrent reservations selected the same phase"
test -n "$(git -C "$root" show-ref --hash "refs/ywc/task-phase/yk/$(printf '%06d' "$first")")" \
  || fail "first reservation was not durable"
test -n "$(git -C "$root" show-ref --hash "refs/ywc/task-phase/yk/$(printf '%06d' "$second")")" \
  || fail "retry reservation was not durable"

echo "PASS: initials allocation contract, bounded scan matrix, and concurrent retry"
