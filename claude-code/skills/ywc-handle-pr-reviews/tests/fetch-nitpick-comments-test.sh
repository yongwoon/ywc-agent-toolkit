#!/usr/bin/env bash
# Fixture suite for fetch-nitpick-comments.sh, following the exact convention
# of claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh:
# expect_*-style assertion helpers, a stubbed `gh` executable placed first
# on PATH, and fail()-on-mismatch semantics (Amendment C).
set -euo pipefail

skill_dir="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
script="$skill_dir/scripts/fetch-nitpick-comments.sh"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/fetch-nitpick-comments-test.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

mkdir -p "$tmpdir/bin"
STUB_USER_FILE="$tmpdir/stub-user"
STUB_REVIEWS_FILE="$tmpdir/stub-reviews.json"
STUB_COMMENTS_FILE="$tmpdir/stub-comments.json"

cat > "$tmpdir/bin/gh" <<'STUB'
#!/usr/bin/env bash
# Stub `gh` for fetch-nitpick-comments-test.sh -- routes by the subcommand
# text present in "$*" to fixture files the test wrote beforehand.
case "$*" in
  *"api user --jq .login"*)
    cat "$STUB_USER_FILE"
    ;;
  *"/pulls/"*"/reviews --paginate --slurp"*)
    cat "$STUB_REVIEWS_FILE"
    ;;
  *"/issues/"*"/comments --paginate --slurp"*)
    cat "$STUB_COMMENTS_FILE"
    ;;
  *)
    echo "unexpected gh invocation: $*" >&2
    exit 1
    ;;
esac
STUB
chmod +x "$tmpdir/bin/gh"

export STUB_USER_FILE STUB_REVIEWS_FILE STUB_COMMENTS_FILE
export PATH="$tmpdir/bin:$PATH"

# run_script <owner/repo> <pr-number> [...]  -- writes stdout/stderr to
# $tmpdir/out and $tmpdir/err; prints the exit status on stdout.
run_script() {
  set +e
  bash "$script" "$@" > "$tmpdir/out" 2> "$tmpdir/err"
  echo $?
  set -e
}

# expect_items_by_nonempty_hash <owner/repo> <pr-number> <sorted-space-separated-hashes>
# Asserts exit 0 and that the non-empty-hash items in the output, sorted,
# match exactly. Empty-hash (raw_fallback) items are checked separately by
# expect_raw_fallback_count, since join(" ") on repeated "" is unreadable.
expect_items_by_nonempty_hash() {
  local repo="$1" pr="$2" want_hashes="$3" status got_hashes
  status=$(run_script "$repo" "$pr")
  [ "$status" -eq 0 ] || fail "$repo#$pr: expected exit 0, got $status ($(cat "$tmpdir/err"))"
  got_hashes="$(jq -r '[.[] | select(.hash != "") | .hash] | sort | join(" ")' "$tmpdir/out")"
  [ "$got_hashes" = "$want_hashes" ] || fail "$repo#$pr: got hashes [$got_hashes], want [$want_hashes]"
}

# expect_title_for_hash <hash> <expected-title>
# Reads the last run's $tmpdir/out (dedup-keeps-latest-review assertion, AC2).
expect_title_for_hash() {
  local hash="$1" want="$2" got
  got="$(jq -r --arg h "$hash" '.[] | select(.hash == $h) | .title' "$tmpdir/out")"
  [ "$got" = "$want" ] || fail "hash $hash: got title '$got', want '$want'"
}

# expect_raw_fallback_count <expected-count>
# Reads the last run's $tmpdir/out -- proves empty-hash items are never
# collapsed by hash-based dedup (Amendment B).
expect_raw_fallback_count() {
  local want="$1" got
  got="$(jq -r '[.[] | select(.hash == "")] | length' "$tmpdir/out")"
  [ "$got" = "$want" ] || fail "raw_fallback count: got $got, want $want"
}

# --- fixture bodies -----------------------------------------------------------

cat > "$tmpdir/body_a.txt" <<'EOF'
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/a.ts (1)</summary><blockquote>

`1`: **Old Title**

Old body.

<!-- cr-comment:v1:aaa001 -->

</blockquote></details>
</blockquote>
</details>
EOF

cat > "$tmpdir/body_b.txt" <<'EOF'
<details>
<summary>🧹 Nitpick comments (4)</summary><blockquote>

<details>
<summary>src/b1.ts (2)</summary><blockquote>

`1`: **New Title**

New body.

<!-- cr-comment:v1:aaa001 -->

---

`2`: **Addressed by me**

Body.

<!-- cr-comment:v1:bbb001 -->

</blockquote></details>

<details>
<summary>src/b2.ts (2)</summary><blockquote>

`3`: **Addressed by other**

Body.

<!-- cr-comment:v1:ccc001 -->

---

`4`: **Unaddressed item**

Body.

<!-- cr-comment:v1:ddd001 -->

</blockquote></details>

<details>
<summary>src/b3.ts (1)</summary><blockquote>

This block has no marker at all, block one.

</blockquote></details>

<details>
<summary>src/b4.ts (1)</summary><blockquote>

This block has no marker at all, block two.

</blockquote></details>

</blockquote>
</details>
EOF

cat > "$tmpdir/body_c.txt" <<'EOF'
<details>
<summary>🧹 Nitpick comments (1)</summary><blockquote>
<details>
<summary>src/human.ts (1)</summary><blockquote>

`1`: **Should never appear**

Body.

<!-- cr-comment:v1:eee001 -->

</blockquote></details>
</blockquote>
</details>
EOF

# --- scenario 1: dedup + marker-exclusion (current-user-scoped) + non-CodeRabbit filter + raw_fallback never collapsed --

jq -n \
  --rawfile a "$tmpdir/body_a.txt" \
  --rawfile b "$tmpdir/body_b.txt" \
  --rawfile c "$tmpdir/body_c.txt" \
  '[[
    {id: 100, user: {login: "coderabbitai[bot]"}, submitted_at: "2026-01-01T00:00:00Z", body: $a},
    {id: 200, user: {login: "coderabbitai[bot]"}, submitted_at: "2026-01-02T00:00:00Z", body: $b},
    {id: 300, user: {login: "human-reviewer"}, submitted_at: "2026-01-03T00:00:00Z", body: $c}
  ]]' > "$STUB_REVIEWS_FILE"

jq -n '[[
  {user: {login: "ywc-bot-tester"}, body: "Addressed.\n<!-- nitpick-addressed:bbb001 -->"},
  {user: {login: "other-reviewer"}, body: "Also addressed.\n<!-- nitpick-addressed:ccc001 -->"}
]]' > "$STUB_COMMENTS_FILE"

echo "ywc-bot-tester" > "$STUB_USER_FILE"

# bbb001 excluded (marker authored by the current user, Amendment A).
# ccc001 NOT excluded (marker authored by someone else -- the current-
# user trust-boundary scoping means only the current user's markers count).
# eee001 absent entirely (AC3 -- non-CodeRabbit review never parsed).
expect_items_by_nonempty_hash "acme/widgets" "42" "aaa001 ccc001 ddd001"
expect_title_for_hash "aaa001" "New Title"
expect_raw_fallback_count "2"

# --- scenario 2: zero CodeRabbit reviews -> [], exit 0 (Edge Cases) -----------

jq -n '[[]]' > "$STUB_REVIEWS_FILE"
jq -n '[[]]' > "$STUB_COMMENTS_FILE"
echo "ywc-bot-tester" > "$STUB_USER_FILE"

status=$(run_script "acme/widgets" "99")
[ "$status" -eq 0 ] || fail "zero-reviews: expected exit 0, got $status ($(cat "$tmpdir/err"))"
got="$(jq -c . "$tmpdir/out")"
[ "$got" = "[]" ] || fail "zero-reviews: expected [], got $got"

# --- usage / validation errors -------------------------------------------------

status=$(run_script)
[ "$status" -eq 2 ] || fail "no-args: expected exit 2, got $status"

status=$(run_script "not-a-valid-repo-format" "42")
[ "$status" -eq 2 ] || fail "invalid-repo: expected exit 2, got $status"

status=$(run_script "acme/widgets" "not-a-number")
[ "$status" -eq 2 ] || fail "invalid-pr-number: expected exit 2, got $status"

# --- syntax self-check ----------------------------------------------------------

bash -n "$script" || fail "bash -n reported a syntax error in $script"

echo "OK: all fetch-nitpick-comments.sh assertions passed"
