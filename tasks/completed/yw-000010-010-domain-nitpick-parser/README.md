# yw-000010-010-domain-nitpick-parser

## Purpose
Add the pure, network-free parser that turns one CodeRabbit review body into a JSON array of Nitpick pseudo-comment objects. This is the foundation for `ywc-handle-pr-reviews` to see Nitpick-tier items, which today are invisible because `fetch-unresolved-comments.sh` only sees thread-level review comments, not the `<details><summary>Nitpick comments (N)</summary>` blocks CodeRabbit nests inside a single review body.

## Scope
- `claude-code/skills/ywc-handle-pr-reviews/scripts/extract-nitpick-comments.py` — stdin→stdout `HTMLParser`-based walker.
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fixtures/nitpick-review-body.html` — fixture review body with multi-file, multi-item, and malformed-block cases.
- `claude-code/skills/ywc-handle-pr-reviews/scripts/test_extract_nitpick_comments.py` — stdlib `unittest`, fixture-driven.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#FR-1: Nitpick body parser (extract-nitpick-comments.py)` — parser algorithm and required fields.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment B` — `raw_fallback` empty-hash never-eligible-for-marker rule (parser side: emit `hash: ""` only, no other change).
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment G` — the "no section at all → `[]`" AC1 addition (this task); the `gh api --paginate --slurp` flattening note is Task 020's concern.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Edge Cases` (spec:105-111) — zero reviews, count-mismatch-emits-warning-not-error.

### Summary
Locate the `<details><summary>Nitpick comments (N)</summary>` section in a review body; iterate per-file `<details>` blocks (`path (count)` summary); split each block's buffered inner markup into items terminated by `<!-- cr-comment:v1:<hash> -->` markers; extract `line_start`/`line_end` from a leading `` `N` `` or `` `N-M` `` prefix, `title` from a leading `**title**`, and `body` from the remaining text with tags/comments stripped. A malformed per-file block yields a `parse_status: "raw_fallback"` item with `hash: ""` and its raw text preserved — never silently dropped. The `(N)` count in the summary is a hint only, never authoritative: a count mismatch emits a stderr warning, not an error. A body with no Nitpick section at all, or a zero-count section, both yield `[]`.

### Out of Scope (from spec)
- The fetch/dedup/orchestration logic (`fetch-nitpick-comments.sh`) — handled by `yw-000010-020-domain-nitpick-fetch-orchestrator`.
- SKILL.md integration, README sync — handled by `yw-000010-030-docs-skill-nitpick-integration`.
- Any change to `fetch-unresolved-comments.sh` — explicitly out of scope for the whole spec.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000010-020-domain-nitpick-fetch-orchestrator` — needs this parser's stdin/stdout JSON item contract to pipe review bodies through.

## Key Files
- `claude-code/skills/ywc-handle-pr-reviews/scripts/extract-nitpick-comments.py` — new parser script.
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fixtures/nitpick-review-body.html` — new fixture.
- `claude-code/skills/ywc-handle-pr-reviews/scripts/test_extract_nitpick_comments.py` — new test.

## Notes
- **Criticality inference (Notes log per skill Criticality Assignment rule 2)**: marked `critical` below. The spec's NFR Security row explicitly requires the `_sanitize_for_log` guard (CR/LF stripping, length truncation) against log-injection from untrusted bot-authored text, and requires the parser never `eval`/execute any part of the body — this is a genuine untrusted-input handling surface, not a keyword-match false positive. Downgrade to `normal` only if you determine this guard is not security-relevant in this repo's logging context.
- Follow this repo's existing Python test idiom: plain `unittest`/assert-based, no pytest dependency (confirmed convention: `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`).
- `raw_fallback` items always carry `hash: ""` — this task only needs to *emit* that; the "never eligible for marker exclusion" consumption rule lives in Task 020's fetch script, not here.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-handle-pr-reviews/scripts/extract-nitpick-comments.py`
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fixtures/nitpick-review-body.html`
- `claude-code/skills/ywc-handle-pr-reviews/scripts/test_extract_nitpick_comments.py`

### Shared Surfaces
- stdin/stdout JSON item schema: `hash`, `path`, `line_start`, `line_end`, `title`, `body`, `severity: "nitpick"`, `parse_status` — consumed by Task 020's `fetch-nitpick-comments.sh`.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 claude-code/skills/ywc-handle-pr-reviews/scripts/test_extract_nitpick_comments.py`

## Criticality
`critical` — see Notes above (untrusted third-party bot content, log-injection sanitization guard, no-eval requirement).

## Out of Scope
- Network calls of any kind — this script is pure stdin/stdout, verified by code inspection (no `subprocess`, `urllib`, `requests` imports).
- Deduplication across multiple reviews — that is Task 020's concern; this parser handles exactly one review body per invocation.
- Marker-exclusion / addressed-tracking logic — Task 020.
