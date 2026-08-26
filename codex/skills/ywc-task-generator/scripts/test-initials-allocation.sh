#!/usr/bin/env bash
set -euo pipefail

# Bounded contract fixture. The generator is instruction-driven in this
# repository, so textual checks prove the documented behavior and the
# temporary Git repository proves the shared reservation primitive.
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
skill="$script_dir/../SKILL.md"
skill_dir=$(dirname "$script_dir")
reference="$skill_dir/references/collaborator-initials.md"
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
must_have "$reference" "1. Explicit \`--initials <value>\`" \
  'explicit precedence tier is missing'
must_have "$reference" "2. Project \`.codex/ywc.json\` \`initials\`" \
  'project precedence tier is missing'
must_have "$reference" "3. User \`~/.codex/ywc.json\` \`initials\`" \
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
tasks_path=tasks
case "$tasks_path" in /*|../*|*/../*|*/..|'') fail "safe relative path rejected" ;; esac
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

# Missing non-interactive initials stop before any downstream write.
context_root="$root/context"
mkdir -p "$context_root"
missing_initials_transaction() {
  [ -n "${1:-}" ] || {
    printf '%s\n' NEEDS_CONTEXT
    return 0
  }
  return 1
}
test "$(missing_initials_transaction '')" = NEEDS_CONTEXT \
  || fail "missing initials did not return NEEDS_CONTEXT"
! find "$context_root" -mindepth 1 -print -quit | grep -q . \
  || fail "NEEDS_CONTEXT created a downstream artifact"
! git -C "$root" show-ref --verify --quiet refs/ywc/task-phase/yk/000007 \
  || fail "NEEDS_CONTEXT created a reservation"

# Invalid and empty interactive derivations use the same bounded, deterministic
# replacement proposal; no identity normalization is performed implicitly.
resolve_interactive() {
  for candidate in "$@"; do
    if [[ "$candidate" =~ ^[a-z0-9]{2,4}$ ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}
empty_fallback=$(resolve_interactive '' yk) \
  || fail "empty interactive derivation did not reach fallback"
invalid_fallback=$(resolve_interactive 'Y K' yk) \
  || fail "invalid interactive derivation did not reach fallback"
test "$empty_fallback" = yk && test "$invalid_fallback" = yk \
  || fail "interactive fallback was not deterministic"

# Model two concurrent generator transactions. The common Git lock spans the
# scan, selection, reservation, artifact write, and graph write. A holds the
# lock briefly after its scan so B is concurrent but cannot observe a partial
# transaction; A therefore deterministically owns 7 and B owns 8.
zero=0000000000000000000000000000000000000000
value=$(git -C "$root" hash-object -w -t blob /dev/null)
common_git=$(git -C "$root" rev-parse --path-format=absolute --git-common-dir)
lock="$common_git/ywc-task-generator.lock"
scan_max() {
  max=0
  while IFS= read -r phase; do
    [ "$phase" -gt "$max" ] && max=$phase
  done < <(
    find "$root/tasks" "$root/linked/tasks" -type d -print |
      sed -nE 's#^.*/yk-([0-9]{6})-[0-9]{3}-.*$#\1#p'
    sed -nE 's/^.*yk-([0-9]{6})-[0-9]{3}-.*$/\1/p' \
      "$root/tasks/dependency-graph.md" "$root/linked/tasks/dependency-graph.md"
  )
  printf '%s\n' "$max"
}
transaction() {
  id=$1
  until mkdir "$lock" 2>/dev/null; do sleep 0.01; done
  trap 'rm -f "$lock/$id-ready"; rmdir "$lock"' EXIT
  : >"$lock/$id-ready"
  [ "$id" = a ] && sleep 0.05
  candidate=$(scan_max)
  candidate=$((candidate + 1))
  while :; do
    ref="refs/ywc/task-phase/yk/$(printf '%06d' "$candidate")"
    if git -C "$root" update-ref "$ref" "$value" "$zero" 2>/dev/null; then
      break
    fi
    candidate=$((candidate + 1))
  done
  artifact="$root/output/$id-$(printf '%06d' "$candidate").md"
  printf 'allocator=%s phase=yk-%06d\n' "$id" "$candidate" >"$artifact"
  printf '%s\n' "- yk-$(printf '%06d' "$candidate")-010-$id" \
    >>"$root/tasks/dependency-graph.md"
  printf '%s\n' "$candidate"
}
mkdir -p "$root/output"
transaction a >"$root/winner-a" & pid_a=$!
until [ -f "$lock/a-ready" ]; do sleep 0.01; done
transaction b >"$root/winner-b" & pid_b=$!
wait "$pid_a"; wait "$pid_b"
first=$(tr -d '\n' <"$root/winner-a")
second=$(tr -d '\n' <"$root/winner-b")
test "$first" = 7 && test "$second" = 8 \
  || fail "concurrent transactions were not serialized as 7 then 8"
for candidate in "$first" "$second"; do
  ref="refs/ywc/task-phase/yk/$(printf '%06d' "$candidate")"
  test -n "$(git -C "$root" show-ref --hash "$ref")" \
    || fail "reservation $candidate was not retained"
done
grep -Fqx 'allocator=a phase=yk-000007' "$root/output/a-000007.md" \
  || fail "allocator A artifact was not serialized"
grep -Fqx 'allocator=b phase=yk-000008' "$root/output/b-000008.md" \
  || fail "allocator B artifact was not serialized"
grep -Fqx -- '- yk-000007-010-a' "$root/tasks/dependency-graph.md" \
  || fail "allocator A graph output missing"
grep -Fqx -- '- yk-000008-010-b' "$root/tasks/dependency-graph.md" \
  || fail "allocator B graph output missing"
test "$(grep -c '^-' "$root/tasks/dependency-graph.md")" = 5 \
  || fail "graph output was lost or duplicated"
[ ! -d "$lock" ] || fail "common Git lock was not released"

echo "PASS: initials allocation contract, deterministic fallback, and serialized transactions"
