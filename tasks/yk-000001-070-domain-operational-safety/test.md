# Delivery and isolation safety — scenarios

## AC-6 — remote branch deletion gates
1. Exercise a successful parsed empty open-PR result, open PR, nonparseable response, API failure, and invalid branch.
2. Provide merged evidence where the local branch is merged but the intended base differs, the remote tip has moved, or both match.

Expected: remote deletion occurs only for a valid branch after successful parsed empty PR lookup, or for merged evidence bound to both intended base and current remote tip. Every failed/ambiguous lookup and mismatch causes zero remote deletions; local `--merged HEAD` alone is insufficient.

## AC-6 — isolation, polling, and severity
1. Inject isolation setup status 127 and other nonzero statuses; count worker starts.
2. Supply Dockerfile FROM changes and a rebase wait crossing multiple polling chunks, with completion before and after the single 30-minute deadline.
3. Provide a prompt-injection row whose own exception condition applies and one where only internal-only context is present.

Expected: every nonzero isolation setup is BLOCKED before worker start; FROM changes are detected; polling retains one total deadline and never treats incomplete as success; severity follows the row condition. Existing affected helpers run in a temporary repository/fake subprocess. Model invocation counts require live traces; static expected traces are not PASS claims.
