#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SCRIPT="$SCRIPT_DIR/write-config.sh"
TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/ywc-setup-config.XXXXXX")
trap 'rm -rf "$TEST_ROOT"' EXIT

fail() { echo "FAIL: $*" >&2; exit 1; }

mkdir -p "$TEST_ROOT/project/.codex"
printf '%s\n' '{"lang":"ja","unknown":{"keep":true}}' >"$TEST_ROOT/project/.codex/ywc.json"
(cd "$TEST_ROOT/project" && bash "$SCRIPT" --scope project --initials yk)
(cd "$TEST_ROOT/project" && bash "$SCRIPT" --scope project --lang english --initials yw)

if (cd "$TEST_ROOT/project" && bash "$SCRIPT" --scope project --initials YK) >/dev/null 2>&1; then
  fail "uppercase initials must be rejected"
fi
if (cd "$TEST_ROOT/project" && bash "$SCRIPT" --scope project --initials) >/dev/null 2>&1; then
  fail "missing initials operand must be rejected"
fi

printf '%s\n' '{"lang":' >"$TEST_ROOT/project/.codex/ywc.json"
if (cd "$TEST_ROOT/project" && bash "$SCRIPT" --scope project --initials yk) >/dev/null 2>&1; then
  fail "malformed config must be rejected"
fi
grep -Fx '{"lang":' "$TEST_ROOT/project/.codex/ywc.json" >/dev/null

printf '%s\n' '{"lang":"en","unknown":{"keep":true}}' >"$TEST_ROOT/project/.codex/ywc.json"

(
  cd "$TEST_ROOT/project"
  bash "$SCRIPT" --scope project --lang ko &
  bash "$SCRIPT" --scope project --initials yw &
  wait
)
python3 - "$TEST_ROOT/project/.codex/ywc.json" <<'PY'
import json
import sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["lang"] == "ko", data
assert data["initials"] == "yw", data
assert data["unknown"] == {"keep": True}, data
PY

echo "PASS: ywc-setup config writer"
