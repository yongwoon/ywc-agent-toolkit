#!/usr/bin/env bash
# Verdict checks for poll-pr-reviews.sh; no network access required.
#
# The `gh` stub is driven by a call-index counter so a window can succeed first
# and fail later — the case that must NOT report WINDOW=complete.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SCRIPT_DIR/poll-pr-reviews.sh"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
mkdir -p "$TEMP_DIR/bin"

# fetch_bot_count spends 2 gh calls per poll: `gh pr view`, then `gh api`.
# succeed_calls = how many leading calls succeed; every later call exits 1.
write_gh_stub() {
  local succeed_calls="$1" bot_count="$2"
  cat > "$TEMP_DIR/bin/gh" <<EOF
#!/usr/bin/env bash
COUNTER="$TEMP_DIR/calls"
N=\$(( \$(cat "\$COUNTER" 2>/dev/null || echo 0) + 1 ))
echo "\$N" > "\$COUNTER"
[ "\$N" -le $succeed_calls ] || exit 1
# 'gh api' feeds a line-comment count of 0; 'gh pr view' feeds the top-level count.
[ "\$1" = api ] && exit 0
printf '%s\\n' "$bot_count"
EOF
  chmod +x "$TEMP_DIR/bin/gh"
  rm -f "$TEMP_DIR/calls"
}

run_poll() {
  PATH="$TEMP_DIR/bin:$PATH" \
    YWC_POLL_INITIAL_WAIT_SECONDS=0 \
    YWC_POLL_INTERVAL_SECONDS=0 \
    YWC_POLL_MAX_POLLS="$1" \
    bash "$SCRIPT" 101
}

# Regression: poll 1 succeeds with zero bots, poll 2's queries fail. The window
# is unproven, so it must degrade instead of clearing the zero-bot merge gate.
write_gh_stub 2 0
OUTPUT="$(run_poll 2 2>/dev/null)" && STATUS=0 || STATUS=$?
[ "$STATUS" -eq 3 ] || { echo "expected exit 3 after a late failure, got $STATUS" >&2; exit 1; }
[ "$OUTPUT" = "BOT_COUNT=0 WINDOW=degraded" ] || { echo "expected degraded, got: $OUTPUT" >&2; exit 1; }

# A fully successful zero-bot window still clears the gate.
write_gh_stub 99 0
OUTPUT="$(run_poll 2)" && STATUS=0 || STATUS=$?
[ "$STATUS" -eq 1 ] || { echo "expected exit 1 for a clean zero-bot window, got $STATUS" >&2; exit 1; }
[ "$OUTPUT" = "BOT_COUNT=0 WINDOW=complete" ] || { echo "expected complete, got: $OUTPUT" >&2; exit 1; }

# Bots found is positive evidence: the loop exits on the first non-zero count.
write_gh_stub 99 3
OUTPUT="$(run_poll 2)"
[ "$OUTPUT" = "BOT_COUNT=3 WINDOW=complete" ] || { echo "expected 3 bots, got: $OUTPUT" >&2; exit 1; }

echo "poll-pr-reviews.sh verdict checks passed"
