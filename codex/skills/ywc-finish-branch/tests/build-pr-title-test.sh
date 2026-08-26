#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
script="$script_dir/../scripts/build-pr-title.py"
fail() { echo "FAIL: $*" >&2; exit 1; }
expect() {
  local name=$1 number=$2 slug=$3 output
  output=$(python3 "$script" "$name") || fail "$name rejected"
  [ "$output" = "TASK_NUMBER=$number
SLUG_EN=$slug" ] || fail "$name output: $output"
}
expect yk-000001-010-db-create-users yk-000001-010 "Db Create Users"
expect ab12-000042-030-infra-rotate-keys ab12-000042-030 "Infra Rotate Keys"
expect yk-001010-db-create-users yk-001010 "Db Create Users"
expect 000001-010-db-create-users 000001-010 "Db Create Users"
expect 001010-db-create-users 001010 "Db Create Users"
expect 1-010-db-create-users 1-010 "Db Create Users"
expect 1234-000001-010-db-x 1234-000001 "010 Db X"

set +e
python3 "$script" TOOLONG-000001-010-db-x > /dev/null 2>/dev/null
status=$?
set -e
[ "$status" -eq 1 ] || fail "malformed initials accepted"
echo "PASS: PR-title parser fixtures"
