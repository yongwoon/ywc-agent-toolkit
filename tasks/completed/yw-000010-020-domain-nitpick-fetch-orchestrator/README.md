# yw-000010-020-domain-nitpick-fetch-orchestrator

## Purpose
Add the orchestrator script that fetches every CodeRabbit review on a PR, pipes each body through Task 010's parser, dedups by hash across reviews, and excludes items already marked addressed — producing the JSON array `ywc-handle-pr-reviews` SKILL.md will consume as the "Nitpick" list.

## Scope
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh` — five-stage `gh api` pipeline.
- `claude-code/skills/ywc-handle-pr-reviews/tests/fetch-nitpick-comments-test.sh` — pure-Bash test with a stubbed `gh` executable.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#FR-2: Fetch/dedup/mark-exclusion orchestrator (fetch-nitpick-comments.sh)` — the five-stage pipeline.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment A` — marker-scan trust boundary (current authenticated user only).
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment B` — `raw_fallback` empty-hash items excluded from both dedup and addressed-marker exclusion.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment C` — corrects the bash test file to `tests/fetch-nitpick-comments-test.sh`, following `claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh`'s exact convention.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment G` (first bullet) — `--paginate --slurp` flattening verification.
- `claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh` — the cited bash test convention to follow exactly (`expect_*` assertion helpers, stubbed executable first on `PATH`, `fail()`-on-mismatch).
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh` — sibling script whose shape (arg validation, `gh api` usage, exit-code contract) this script should mirror; must remain unmodified.

### Summary
Five stages: (1) validate `<owner>/<repo>` and PR-number arguments, resolve the current `gh` user via `gh api user`; (2) fetch all PR reviews via `gh api ... --paginate`, filter to `coderabbitai[bot]` authors only; (3) pipe each review body through `extract-nitpick-comments.py`, tagging each item with `review_id`/`review_submitted_at`; (4) merge across reviews and dedup by `hash`, keeping the item from the most recent `review_submitted_at` — empty-hash `raw_fallback` items are excluded from hash-based dedup entirely, since they are distinct per-occurrence; (5) fetch PR-level issue comments authored by the current authenticated user, scan for `<!-- nitpick-addressed:<hash> -->` markers, and exclude any non-empty-hash item whose hash is already marked. The marker scan is scoped to the current user only — a deliberate trust-boundary decision (Amendment A), not an oversight.

### Out of Scope (from spec)
- The parser itself — `yw-000010-010-domain-nitpick-parser` (already merged before this task starts).
- SKILL.md Step 2/3/4/5/6/9 integration, README sync — `yw-000010-030-docs-skill-nitpick-integration`.
- Posting the `nitpick-addressed:<hash>` marker comment itself — that is a SKILL.md Step 5 responsibility (Task 030), this script only *reads* existing markers to exclude already-addressed items.
- Cross-identity marker sharing, concurrent-run locking — explicitly accepted limitations per Amendments A and E, not solved by this port.

## Dependencies

### Depends On
- `yw-000010-010-domain-nitpick-parser` — provides the `extract-nitpick-comments.py` stdin/stdout JSON item contract this script pipes review bodies through.

### Depended By
- `yw-000010-030-docs-skill-nitpick-integration` — SKILL.md Step 2 documents and invokes this script's final CLI contract (args, exit codes, output shape).

## Key Files
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh` — new orchestrator script.
- `claude-code/skills/ywc-handle-pr-reviews/tests/fetch-nitpick-comments-test.sh` — new test (new `tests/` subdirectory for this skill).

## Notes
- **Criticality**: `normal`. This script orchestrates calls and delegates all untrusted-content handling to Task 010's parser; it does not itself parse HTML/bot text.
- Verify the actual `gh api repos/{owner}/{repo}/pulls/{pr}/reviews --paginate` response shape before finalizing stage 2 — `--paginate` alone self-flattens multi-page array responses; `--slurp` combined with `--paginate` yields an array-of-page-arrays that needs `jq 'add // []'` to flatten. A silent wrong-nesting bug here would feed malformed input to the parser without erroring (Amendment G).
- `raw_fallback` items (`hash: ""`) must be threaded through stages 3–5 unaffected by dedup or marker-exclusion — verify with a dedicated test case, not just code-read (Amendment B).
- The `tests/` directory does not yet exist under this skill — create it as part of this task.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh`
- `claude-code/skills/ywc-handle-pr-reviews/tests/fetch-nitpick-comments-test.sh`

### Shared Surfaces
- Consumes Task 010's parser stdin/stdout JSON item schema (read-only dependency, no shape change).
- Produces the `fetch-nitpick-comments.sh <owner/repo> <pr-number>` CLI contract (args, exit codes, output JSON array shape) that Task 030's SKILL.md Step 2 will invoke and document.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000010-010-domain-nitpick-parser`

### Task Verify
- `bash claude-code/skills/ywc-handle-pr-reviews/tests/fetch-nitpick-comments-test.sh`
- `shellcheck claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh`

## Criticality
`normal` — see Notes above.

## Out of Scope
- Any change to `fetch-unresolved-comments.sh` — its existing output contract and behavior are unchanged (AC5).
- Posting the consolidated PR-level reply comment or the `nitpick-addressed:<hash>` marker — SKILL.md Step 5 (Task 030) owns writing the marker; this script only reads existing markers.
- Distributed locking against concurrent runs — accepted limitation (Amendment E).
