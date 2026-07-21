#!/usr/bin/env bash
# Fast behavioral checks for poll-pr-reviews.sh; no network access required.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SCRIPT_DIR/poll-pr-reviews.sh"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

git -C "$TEMP_DIR" init -q
mkdir -p "$TEMP_DIR/bin"

run_case() {
  local result="$1"
  local pr_number="$2"
  cat > "$TEMP_DIR/bin/gh" <<EOF
#!/usr/bin/env bash
if [ "$result" = fail ]; then
  exit 1
fi
printf '%s\\n' "$result"
EOF
  chmod +x "$TEMP_DIR/bin/gh"
  (
    cd "$TEMP_DIR"
    PATH="$TEMP_DIR/bin:$PATH" \
      YWC_POLL_INITIAL_WAIT_SECONDS=0 \
      YWC_POLL_INTERVAL_SECONDS=0 \
      YWC_POLL_MAX_POLLS=1 \
      YWC_POLL_MAX_FETCH_FAILURES=1 \
      bash "$SCRIPT" "$pr_number"
  )
}

if run_case 0 101; then
  echo "expected a zero-bot poll to exit 1" >&2
  exit 1
fi
(cd "$TEMP_DIR" && PATH="$TEMP_DIR/bin:$PATH" bash "$SCRIPT" --verify 101) | grep -Fq '"complete": true'

run_case 2 102 | grep -Fxq 2
(cd "$TEMP_DIR" && PATH="$TEMP_DIR/bin:$PATH" bash "$SCRIPT" --verify 102) | grep -Fq '"bot_count": 2'

if run_case fail 103; then
  echo "expected failed API reads to fail polling" >&2
  exit 1
fi
if (cd "$TEMP_DIR" && PATH="$TEMP_DIR/bin:$PATH" bash "$SCRIPT" --verify 103) >/dev/null 2>&1; then
  echo "expected no artifact after failed API reads" >&2
  exit 1
fi

echo "PASS: poll-pr-reviews behavior"
