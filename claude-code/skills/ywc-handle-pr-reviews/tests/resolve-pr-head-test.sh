#!/usr/bin/env bash
# Security fixture suite for resolve-pr-head.sh. A stubbed `gh` placed first on
# PATH serves a JSON fixture through the real `jq`, applying the exact --jq
# expression the script passes, so the escaping of hostile headRefName values
# is exercised end to end. Any hostile name that executes leaves a PWNED file.
# Hostile fixture strings are single-quoted on purpose; they must not expand.
# shellcheck disable=SC2016
set -euo pipefail

skill_dir="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
script="$skill_dir/scripts/resolve-pr-head.sh"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/resolve-pr-head-test.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

mkdir -p "$tmpdir/bin" "$tmpdir/work"
export STUB_JSON_FILE="$tmpdir/pr.json"
export STUB_CALLS_FILE="$tmpdir/gh-calls"
export STUB_FAIL_FILE="$tmpdir/gh-fail"

cat > "$tmpdir/bin/gh" <<'STUB'
#!/usr/bin/env bash
# Stub `gh pr view <n> --json ... --jq <expr>`: log the call, then either fail
# like gh does or apply <expr> to the fixture with jq -r (gh --jq prints raw).
printf '%s\n' "$*" >> "$STUB_CALLS_FILE"
if [ -f "$STUB_FAIL_FILE" ]; then
  echo "GraphQL: Could not resolve to a PullRequest" >&2
  exit 1
fi
expr=""
while [ "$#" -gt 0 ]; do
  if [ "$1" = "--jq" ]; then expr="$2"; break; fi
  shift
done
[ -n "$expr" ] || { echo "stub: --jq missing" >&2; exit 1; }
jq -r "$expr" "$STUB_JSON_FILE"
STUB
chmod +x "$tmpdir/bin/gh"

# Run the script from an empty scratch dir so a payload such as `touch PWNED`
# would land where the test looks for it.
run() {
  rm -f "$STUB_CALLS_FILE" "$tmpdir/work/PWNED"
  set +e
  out="$(cd "$tmpdir/work" && PATH="$tmpdir/bin:$PATH" bash "$script" "$@" 2>"$tmpdir/stderr")"
  code=$?
  set -e
  err="$(cat "$tmpdir/stderr")"
}

good_oid='0123456789abcdef0123456789abcdef01234567'

fixture() { # fixture <state> <isCrossRepository-json> <headRefName-json> [headRefOid-json]
  rm -f "$STUB_FAIL_FILE"
  printf '{"state":"%s","isCrossRepository":%s,"headRefName":%s,"headRefOid":%s}\n' \
    "$1" "$2" "$3" "${4:-\"$good_oid\"}" > "$STUB_JSON_FILE"
}

expect_ok() { # expect_ok <expected-head>
  [ "$code" -eq 0 ] || fail "expected exit 0, got $code (stderr: $err)"
  [ "$out" = "$1" ] || fail "expected stdout '$1', got '$out'"
}

expect_blocked() { # expect_blocked <stderr-substring>
  [ "$code" -eq 1 ] || fail "expected exit 1, got $code (stdout: $out)"
  [ -z "$out" ] || fail "BLOCKED run must print nothing on stdout, got '$out'"
  case "$err" in *"$1"*) ;; *) fail "expected stderr to contain '$1', got '$err'" ;; esac
  [ ! -e "$tmpdir/work/PWNED" ] || fail "hostile input was executed"
}

# 1. Happy path: a same-repo OPEN PR prints its validated head branch and SHA.
# Fails if: the script stops printing the head or SHA, or rejects a legal name.
fixture OPEN false '"feature/yk-000006-030-x.y_z"'
run 42
expect_ok "feature/yk-000006-030-x.y_z"$'\n'"$good_oid"

# 2. Non-numeric PR numbers are refused before gh is ever called.
# Fails if: the ^[0-9]+$ check is removed or moved after the gh call.
for bad in '12;touch PWNED' '12 13' '-1' '' '1e3' '$(touch PWNED)' $'12\n13'; do
  fixture OPEN false '"main"'
  run "$bad"
  expect_blocked "BLOCKED: PR number must be numeric"
  [ ! -e "$STUB_CALLS_FILE" ] || fail "gh was called for PR number '$bad'"
done

# 3. Wrong argument count is a usage error (exit 2), not a lookup.
# Fails if: the arity check is dropped and gh runs with no PR number.
run
[ "$code" -eq 2 ] || fail "expected usage exit 2 with no args, got $code"
[ ! -e "$STUB_CALLS_FILE" ] || fail "gh was called without a PR number"
run 42 43
[ "$code" -eq 2 ] || fail "expected usage exit 2 with two args, got $code"
[ ! -e "$STUB_CALLS_FILE" ] || fail "gh was called with two PR numbers"

# 4. Fork PRs are refused, and so is a missing/non-boolean flag (fail closed).
# Fails if: the isCrossRepository check is removed or only rejects literal true.
for cross in true null '"false"'; do
  fixture OPEN "$cross" '"main"'
  run 42
  expect_blocked "BLOCKED: --worktree does not support fork PRs"
done

# 5. Non-OPEN PRs are refused with their state.
# Fails if: the state check is removed or narrowed to one state (!= MERGED).
for state in MERGED CLOSED; do
  fixture "$state" false '"main"'
  run 42
  expect_blocked "BLOCKED: PR is $state"
done

# 6. A gh failure fails closed and surfaces gh's stderr.
# Fails if: the gh exit status is ignored.
fixture OPEN false '"main"'
: > "$STUB_FAIL_FILE"
run 42
expect_blocked "Could not resolve to a PullRequest"
expect_blocked "BLOCKED: gh pr view failed"

# 7. Hostile head branch names are rejected and never executed.
# Fails if: the allowlist, the leading '-' check or the check-ref-format call
# is removed, or the name is evaluated by a shell. Removing only the '..' check
# keeps the suite green: check-ref-format rejects 'a..b' too (kept per C2).
hostile=(
  '"$(touch PWNED)"'        # command substitution
  '"`touch PWNED`"'         # backtick substitution
  '"$(id>PWNED)"'           # passes git check-ref-format; only the allowlist stops it
  '"a;touch PWNED"'         # command separator
  '"main\ntouch PWNED"'     # embedded newline (jq @tsv escapes it to \n)
  '"main\t$(touch PWNED)"'  # embedded tab
  '"-ufoo"'                 # option injection
  '"a..b"'                  # range syntax
  '"feature/x.lock"'        # allowlisted, rejected only by check-ref-format
  '"feature/"'              # allowlisted, rejected only by check-ref-format
  '"x@{1}"'                 # reflog syntax
  '""'                      # empty
  'null'                    # missing
)
for name in "${hostile[@]}"; do
  fixture OPEN false "$name"
  run 42
  expect_blocked "BLOCKED: invalid head branch name"
done
# Legal git names outside the allowlist say so, so the refusal is not a mystery.
# Fails if: the allowlist rejection stops naming the allowlist.
for name in '"fix/a+b"' '"feature/#1"'; do
  fixture OPEN false "$name"
  run 42
  expect_blocked "allowlist ^[A-Za-z0-9._/-]+$"
done

# 8. The head commit must be a full lowercase 40-hex SHA; the caller pins
# origin/<H> to it, so a malformed value must not reach the caller.
# Fails if: the headRefOid validation is removed or loosened.
for oid in null '""' '"0123456"' '"0123456789ABCDEF0123456789ABCDEF01234567"' \
    '"0123456789abcdef0123456789abcdef01234567\n"' '"$(touch PWNED)"'; do
  fixture OPEN false '"main"' "$oid"
  run 42
  expect_blocked "BLOCKED: invalid head commit"
done

echo "PASS: resolve-pr-head-test.sh"
