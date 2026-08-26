#!/usr/bin/env bash
# Fixture suite for build-pr-title.py under the optional INITIALS prefix.
#
# The legacy cases are the regression guard: every unprefixed task name must
# produce exactly the output it produced before the prefix became parseable.
set -euo pipefail

skill_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
script="$skill_dir/scripts/build-pr-title.py"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/build-pr-title-test.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# expect_parts <task-name> <expected-task-number> <expected-slug-en>
expect_parts() {
  local name="$1" want_number="$2" want_slug="$3" status want
  set +e
  python3 "$script" "$name" > "$tmpdir/out" 2> "$tmpdir/err"
  status=$?
  set -e
  [ "$status" -eq 0 ] || fail "$name: expected exit 0, got $status ($(cat "$tmpdir/err"))"
  want="$(printf 'TASK_NUMBER=%s\nSLUG_EN=%s\n' "$want_number" "$want_slug")"
  [ "$(cat "$tmpdir/out")" = "$want" ] || fail "$name: got $(cat "$tmpdir/out"), want $want"
}

# expect_title <task-name> <expected-title>
expect_title() {
  local name="$1" want="$2" got
  got="$(python3 "$script" "$name" --format title)"
  [ "$got" = "$want" ] || fail "$name --format title: got $got, want $want"
}

# --- prefixed ids (AC7) ------------------------------------------------------
expect_parts yk-000001-010-db-create-user-table yk-000001-010 "Db Create User Table"
expect_title yk-000001-010-db-create-user-table "[yk-000001-010] Db Create User Table"
expect_parts ab12-000042-030-infra-rotate-keys ab12-000042-030 "Infra Rotate Keys"
# 6-digit legacy phase form, prefixed
expect_parts yk-001010-db-create-users-table yk-001010 "Db Create Users Table"

# --- legacy unprefixed ids stay byte-identical -------------------------------
expect_parts 000001-010-db-create-users-table 000001-010 "Db Create Users Table"
expect_title 000001-010-db-create-users-table "[000001-010] Db Create Users Table"
expect_parts 001010-db-create-users-table 001010 "Db Create Users Table"
expect_parts 1-010-slug 1-010 "Slug"
expect_parts 001-slug 001 "Slug"

# --- unrecognised names keep the exit-1 fallback contract --------------------
set +e
python3 "$script" nonsense > "$tmpdir/out" 2> "$tmpdir/err"
status=$?
set -e
[ "$status" -eq 1 ] || fail "nonsense: expected exit 1, got $status"
[ "$(cat "$tmpdir/out")" = "$(printf 'TASK_NUMBER=\nSLUG_EN=Nonsense\n')" ] \
  || fail "nonsense: unexpected fallback output $(cat "$tmpdir/out")"
grep -q 'WARNING: Could not detect task-number prefix' "$tmpdir/err" \
  || fail "nonsense: missing warning on stderr"

# An initials-like prefix that is too long is not a task number.
set +e
python3 "$script" TOOLONG-000001-010-db-x > "$tmpdir/out" 2> "$tmpdir/err"
status=$?
set -e
[ "$status" -eq 1 ] || fail "TOOLONG-...: expected exit 1, got $status"

echo "PASS: build-pr-title-test.sh"
