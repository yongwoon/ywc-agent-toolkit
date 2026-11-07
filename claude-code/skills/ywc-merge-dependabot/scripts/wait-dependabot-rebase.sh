#!/usr/bin/env bash
# wait-dependabot-rebase.sh <pr-number>
#
# Sequential-flow conflict recovery (Step 3a): records the current head,
# comments `@dependabot rebase`, then polls with a bounded, query-first loop
# (up to 9 queries, 60 s apart — issue as one Bash call with `timeout: 600000`).
#
# The rebase counts as done only when `headRefOid` differs from the recorded
# value AND `mergeable` is exactly MERGEABLE (allowlist: CONFLICTING, UNKNOWN,
# empty, `null` or any other value is unresolved). Both heads must
# match ^[0-9a-f]{40}$: a recorded head that does not (empty, `null`, a failed
# query) exits as "head unreadable"; a polled head that does not is unresolved —
# polling continues; it is never evidence of a finished rebase.
#
# stdout (last line): REBASED=<0|1> ATTEMPTS=<n> NEW_HEAD=<sha or empty>
#
# Exit codes:
#   0  rebased — wait for CI on NEW_HEAD, re-check the head before merging
#   1  not rebased within the window (`mergeable` never became MERGEABLE — any other
#      value counts as not rebased), or the current head
#      could not be read / the rebase comment could not be posted, so no rebase
#      was requested — skip + surface
#   2  usage error

set -euo pipefail

MAX_ATTEMPTS=9
POLL_SECONDS=60

[ $# -eq 1 ] && [[ "$1" =~ ^[0-9]+$ ]] || { echo "usage: wait-dependabot-rebase.sh <pr-number>" >&2; exit 2; }
PR="$1"

OLD_HEAD="$(gh pr view "$PR" --json headRefOid --jq .headRefOid)" || OLD_HEAD=""
if [[ ! "$OLD_HEAD" =~ ^[0-9a-f]{40}$ ]]; then
  # Without a recorded head, any later head would look "new" — never report a rebase on that.
  echo "cannot read the current head of PR $PR — not requesting a rebase" >&2
  echo "REBASED=0 ATTEMPTS=0 NEW_HEAD="
  exit 1
fi
if ! gh pr comment "$PR" --body "@dependabot rebase"; then
  # Dependabot was never asked to rebase — polling would only report a misleading "not rebased".
  echo "failed to post '@dependabot rebase' on PR $PR — not waiting for a rebase that was never requested" >&2
  echo "REBASED=0 ATTEMPTS=0 NEW_HEAD="
  exit 1
fi
ATTEMPT=0; REBASED=0; NEW_HEAD=""; FAILED=0; LAST_ERR=""
ERR_FILE="$(mktemp)"; trap 'rm -f "$ERR_FILE"' EXIT
until [ "$REBASED" -eq 1 ] || [ "$ATTEMPT" -ge "$MAX_ATTEMPTS" ]; do
  ATTEMPT=$((ATTEMPT + 1))
  # stdout alone is the state; stderr goes to a file so a successful call's diagnostics
  # (e.g. GH_DEBUG=api) never leak into it, and a persistent gh failure is reported below.
  if ! STATE="$(gh pr view "$PR" --json headRefOid,mergeable --jq '"\(.headRefOid) \(.mergeable)"' 2>"$ERR_FILE")"; then
    FAILED=$((FAILED + 1)); LAST_ERR="$(tail -n 1 "$ERR_FILE")"; STATE=""
  fi
  NEW_HEAD="${STATE%% *}"; MERGEABLE="${STATE##* }"
  if [[ "$NEW_HEAD" =~ ^[0-9a-f]{40}$ ]] && [ "$NEW_HEAD" != "$OLD_HEAD" ] \
     && [ "$MERGEABLE" = "MERGEABLE" ]; then
    REBASED=1
  elif [ "$ATTEMPT" -lt "$MAX_ATTEMPTS" ]; then
    sleep "$POLL_SECONDS"
  fi
done
[ "$REBASED" -eq 1 ] || NEW_HEAD=""
if [ "$REBASED" -eq 0 ] && [ "$FAILED" -eq "$ATTEMPT" ]; then
  echo "every status query for PR $PR failed — the rebase state is unknown, not stuck (last error: ${LAST_ERR:-none})" >&2
fi
echo "REBASED=$REBASED ATTEMPTS=$ATTEMPT NEW_HEAD=$NEW_HEAD"
[ "$REBASED" -eq 1 ]
