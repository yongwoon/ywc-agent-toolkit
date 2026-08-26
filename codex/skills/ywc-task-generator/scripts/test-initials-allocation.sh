#!/usr/bin/env bash
set -euo pipefail

# Focused, dependency-free contract fixture for the instruction-driven
# generator. It exercises the durable primitive used by the documented
# compare-and-create protocol and checks the safety ordering in SKILL.md.
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
skill="$script_dir/../SKILL.md"
reference="$script_dir/../references/collaborator-initials.md"
fail() { echo "FAIL: $*" >&2; exit 1; }

grep -Eq 'Resolve initials before|initials.*before.*scan|before.*writing' "$skill" \
  || fail "SKILL.md does not require initials before scans/writes"
grep -Fq 'refs/ywc/task-phase/<initials>/<phase>' "$reference" \
  || fail "reservation ref contract missing"
grep -Fq 'git worktree list' "$reference" \
  || fail "linked-worktree contract missing"
grep -Fq 'NEEDS_CONTEXT' "$reference" \
  || fail "missing-initials contract missing"

root=$(mktemp -d "${TMPDIR:-/tmp}/ywc-initials-reservation.XXXXXX")
trap 'rm -rf "$root"' EXIT
git -C "$root" init -q
git -C "$root" config user.email test@example.com
git -C "$root" config user.name Test
zero=0000000000000000000000000000000000000000
value=$(git -C "$root" hash-object -w -t blob /dev/null)
ref=refs/ywc/task-phase/yk/000001

git -C "$root" update-ref "$ref" "$value" "$zero"
if git -C "$root" update-ref "$ref" "$value" "$zero" 2>/dev/null; then
  fail "compare-and-create accepted a duplicate reservation"
fi
test "$(git -C "$root" rev-parse "$ref")" = "$value" \
  || fail "first reservation was not durable"

echo "PASS: initials allocation contract and durable reservation"
