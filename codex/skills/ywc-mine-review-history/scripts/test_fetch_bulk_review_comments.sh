#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)
HELPER="$ROOT/codex/skills/ywc-mine-review-history/scripts/fetch-bulk-review-comments.sh"
REAL_JQ=$(command -v jq)
REAL_RG=$(command -v rg)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
MOCK_BIN="$TMP/bin"
mkdir -p "$MOCK_BIN"
cat >"$MOCK_BIN/gh" <<'MOCK_GH'
#!/usr/bin/env bash
set -eu
printf '%s\n' "$*" >>"${MOCK_LOG:?}"
if [[ "$1 $2" == "pr list" ]]; then
  printf '%s\n' '[{"number":1,"mergedAt":"2026-01-01T00:00:00Z"},{"number":2,"mergedAt":"2026-02-01T00:00:00Z"},{"number":3,"mergedAt":"2026-03-01T00:00:00Z"}]'
  exit 0
fi
if [[ "$1" == api* || "$1" == "api" ]]; then
  url="${*: -1}"
  [[ "$url" == *"/pulls/2/comments" ]] && { echo 'simulated API failure' >&2; exit 1; }
  if [[ "$url" == *"/pulls/1/comments" ]]; then
    printf '%s\n' '[{"user":{"login":"CodeRabbitAI[bot]"},"id":11,"path":"src/a.ts","line":7,"body":"fix a","in_reply_to_id":null},{"user":{"login":"coderabbitai-human"},"id":12,"path":"src/a.ts","line":8,"body":"ignore","in_reply_to_id":null}]'
  else
    printf '%s\n' '[{"user":{"login":"github-actions[bot]"},"id":31,"path":"src/c.ts","line":null,"body":"fix c","in_reply_to_id":21}]'
  fi
  exit 0
fi
exit 2
MOCK_GH
cat >"$MOCK_BIN/jq" <<MOCK_JQ
#!/usr/bin/env bash
set -eu
printf '%s\n' "jq \$*" >>"\${MOCK_LOG:?}"
exec "$REAL_JQ" "\$@"
MOCK_JQ
chmod +x "$MOCK_BIN/gh" "$MOCK_BIN/jq"

run_invalid() {
  local log="$TMP/invalid.log"
  : >"$log"
  set +e
  MOCK_LOG="$log" PATH="$MOCK_BIN:$(dirname "$REAL_JQ"):$(dirname "$REAL_RG"):$(dirname "$(command -v gh)"):/usr/bin:/bin" "$HELPER" "$@" 2>/dev/null
  local status=$?
  set -e
  [[ "$status" -eq 2 ]] || { echo "expected usage exit 2 for $*" >&2; exit 1; }
  ! "$REAL_RG" -q '^pr list|^api ' "$log"
}

run_invalid acme/repo
run_invalid acme/repo --limit 0
run_invalid acme/repo --since 2026-1-01
run_invalid acme/repo --limit 1 --limit 2

LOG="$TMP/calls.log"
: >"$LOG"
set +e
OUTPUT=$(MOCK_LOG="$LOG" PATH="$MOCK_BIN:$(dirname "$REAL_JQ"):$(dirname "$REAL_RG"):$(dirname "$(command -v gh)"):/usr/bin:/bin" "$HELPER" acme/repo --limit 3 --since 2026-01-15 2>"$TMP/stderr")
STATUS=$?
set -e
[[ "$STATUS" -ne 0 ]]
[[ "$OUTPUT" == *'"pr":3'* && "$OUTPUT" != *'"pr":1'* ]]
[[ "$(printf '%s\n' "$OUTPUT" | "$REAL_JQ" -c 'select((keys | sort | join(",")) == "body,id,in_reply_to_id,line,path,pr")' | wc -l | tr -d ' ')" -eq 1 ]]
"$REAL_RG" -q 'failed to fetch.*#2' "$TMP/stderr"
"$REAL_RG" -q -- '--repo acme/repo --state merged --limit 3 --json number,mergedAt' "$LOG"
! "$REAL_RG" -q 'repos/acme/repo/pulls/1/comments' "$LOG"
"$REAL_RG" -q 'repos/acme/repo/pulls/3/comments' "$LOG"
"$REAL_RG" -q 'pulls/2/comments' "$LOG"
echo "PASS: bulk review comment helper contract"
