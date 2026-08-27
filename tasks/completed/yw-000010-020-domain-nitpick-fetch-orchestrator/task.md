# yw-000010-020-domain-nitpick-fetch-orchestrator — Implementation Checklist

## Prerequisites
- [ ] `yw-000010-010-domain-nitpick-parser` is completed (merged) — `extract-nitpick-comments.py` exists and its JSON item contract is stable

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md` (`scripts/fetch-nitpick-comments.sh`, `tests/fetch-nitpick-comments-test.sh`)
- [ ] If the task requires edits outside Ownership (e.g., to `fetch-unresolved-comments.sh` or `extract-nitpick-comments.py`), stop and report before proceeding

## Stop Conditions
- [ ] Stop if `yw-000010-010`'s parser output contract has changed or is missing
- [ ] Stop if the actual `gh api .../pulls/{pr}/reviews` response shape under `--paginate`/`--slurp` differs from what this task assumes — re-verify against live `gh api` output before finalizing stage 2, per Amendment G
- [ ] Stop if implementing this would require modifying `fetch-unresolved-comments.sh`'s existing behavior or output schema (AC5, out of scope for this whole spec)

## Implementation Steps

- [ ] **Stage 1 — argument validation and user resolution**
  - [ ] Validate `<owner>/<repo>` and PR-number positional args (mirror `fetch-unresolved-comments.sh`'s existing validation shape); usage error → exit 2
  - [ ] Resolve current `gh` user via `gh api user` (auth failure → exit 1, matching `fetch-unresolved-comments.sh`'s existing contract)

- [ ] **Stage 2 — fetch and filter CodeRabbit reviews**
  - [ ] Verify the actual `gh api repos/{owner}/{repo}/pulls/{pr}/reviews` response shape (run it live against a real PR, or inspect `gh api` docs) before choosing `--paginate` alone vs `--paginate --slurp` + `jq 'add // []'` flattening
  - [ ] Filter fetched reviews to `user.login == "coderabbitai[bot]"` only (AC3) — human reviewer prose must never reach the parser

- [ ] **Stage 3 — pipe through parser, tag with review metadata**
  - [ ] For each filtered review, pipe its `body` through `python3 .../extract-nitpick-comments.py`
  - [ ] Tag each returned item with `review_id` and `review_submitted_at` from the source review

- [ ] **Stage 4 — merge and dedup by hash**
  - [ ] Merge items across all reviews into one array
  - [ ] Group by `hash`, keep only the item from the most recent `review_submitted_at` per hash group
  - [ ] Exclude empty-hash (`raw_fallback`) items from this hash-based dedup entirely — they pass through as distinct per-occurrence items, never grouped or collapsed (Amendment B / spec:77)

- [ ] **Stage 5 — addressed-marker exclusion**
  - [ ] Fetch PR-level issue comments authored by the current authenticated user only (`gh api repos/{owner}/{repo}/issues/{pr}/comments`, filtered by `user.login == $CURRENT_USER`) — never scan comments from other authors (Amendment A trust boundary)
  - [ ] Scan those comments for `<!-- nitpick-addressed:<hash> -->` markers
  - [ ] Exclude any **non-empty-hash** item whose hash matches a found marker; empty-hash `raw_fallback` items are never eligible for this exclusion (Amendment B) and always pass through
  - [ ] Emit the final deduped, exclusion-filtered array as JSON on stdout; `[]` when there are zero CodeRabbit reviews (no error)

- [ ] **Write `tests/fetch-nitpick-comments-test.sh`**
  - [ ] Follow `claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh`'s exact convention: `expect_*`-style assertion helpers, a stubbed `gh` executable placed first on `PATH`, `fail()`-on-mismatch semantics
  - [ ] Stub `gh api user`, `gh api .../reviews`, `gh api .../comments` to return fixture JSON
  - [ ] Assert: dedup-by-hash-keeps-latest-review (AC2)
  - [ ] Assert: marker-exclusion works for a matched hash, and is scoped to the current-user's comments only (AC2, Amendment A)
  - [ ] Assert: non-CodeRabbit-authored reviews are filtered out before parsing (AC3)
  - [ ] Assert: a `raw_fallback` (empty-hash) item is never excluded by a marker and is never collapsed by dedup (Amendment B)
  - [ ] Assert: zero CodeRabbit reviews → `[]`, exit 0 (Edge Cases)

## Task Verify
- [ ] `bash claude-code/skills/ywc-handle-pr-reviews/tests/fetch-nitpick-comments-test.sh` exits 0
- [ ] `shellcheck claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh` reports no findings

## Verification
- [ ] lint passes (`shellcheck claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh`)
- [ ] typecheck passes — N/A (bash script)
- [ ] unit tests pass (`bash claude-code/skills/ywc-handle-pr-reviews/tests/fetch-nitpick-comments-test.sh`)
- [ ] integration tests pass — N/A (covered by the stubbed-`gh` test above; no live network test in this repo's convention)
- [ ] app builds without error — N/A (no build step for standalone shell scripts)
