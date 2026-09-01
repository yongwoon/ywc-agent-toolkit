# Claude Code PR #223 Nitpick Comment Detection Port

> Status: Draft
> Scale: Medium
> Created: 2026-08-26
> Confidence Gate: 88 (REVIEW band; weakest dimension `root_cause`=80 — expected for a feature port, not a bug fix)
> Spec Reference: [develop-with-llm PR #223](https://github.com/yongwoon/develop-with-llm/pull/223)
> Related: [20260826-codex-pr223-review-artifact-test-hardening.md](./20260826-codex-pr223-review-artifact-test-hardening.md) (Codex-side, test-hardening only, explicitly defers Nitpick work — this plan is the first to add Nitpick detection, and is Claude-Code-only)

## Global Constraints

- `claude-code/skills/` is the distributed Claude Code skill source; each skill directory requires `SKILL.md` plus Tier-1 README locale files (`README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`) per `claude-code/skills/CLAUDE.md`.
- Bot-polling and PR-conflict logic must not be inlined in `SKILL.md` — reference `references/pr-bot-polling.md` / `references/pr-conflict-resolution.md` (already followed by this skill; unaffected here).
- `bash scripts/validate.sh` is the required repository validation command (skill structure, shellcheck, README locale presence, `--list` dry run).
- `codex/skills/` and `tools/codex-skill/` are maintained independently — **no auto-sync**. This plan touches `claude-code/skills/ywc-handle-pr-reviews/` only.
- New shell scripts use `set -euo pipefail` (repo convention, confirmed in `fetch-unresolved-comments.sh` and `build-pr-title.py`'s sibling `.sh` scripts).
- Per `claude-code/skills/CLAUDE.md` "Bundled Execution Scripts", a new deterministic-parsing script belongs in `<skill>/scripts/` with a one-line SKILL.md invocation, not inlined logic.

## Purpose

`develop-with-llm` PR #223 added CodeRabbit **Nitpick-tier** review comment detection to its `ywc-handle-pr-reviews` skill. CodeRabbit's Nitpick items are not individual PR review-thread comments — they are pseudo-comments nested inside `<details><summary>Nitpick comments (N)</summary>` blocks in a single review body. This repo's current `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh` only fetches thread-level comments via the PR review-comments API, so every Nitpick item CodeRabbit posts is currently invisible to this skill and never gets addressed, replied to, or tracked as resolved.

This plan ports the two new scripts and the SKILL.md integration from PR #223 into this repo's Claude Code skill, adapted to this repo's file layout (`claude-code/skills/...` not `tools/claude-code/skills/...`), test conventions, and Tier-1 README requirement.

## Scope

- Add `claude-code/skills/ywc-handle-pr-reviews/scripts/extract-nitpick-comments.py` — pure stdin→stdout HTML/regex parser (no network calls) that reads one CodeRabbit review body and emits a JSON array of Nitpick pseudo-comment objects (`hash`, `path`, `line_start`, `line_end`, `title`, `body`, `severity: "nitpick"`, `parse_status`).
- Add `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh` — fetches all CodeRabbit reviews on a PR via `gh api`, pipes each body through the parser, merges/dedups by `hash` keeping the latest review, and excludes items already marked addressed via a PR-level `<!-- nitpick-addressed:<hash> -->` issue comment.
- Add a fixture (`scripts/fixtures/nitpick-review-body.html`) and two tests, each matching this repo's existing per-language test convention rather than PR #223's uniform naming: `scripts/test_extract_nitpick_comments.py` (Python `unittest`, imports the parser module directly — same idiom as the toolkit-eval `test_score.py` pattern) for the pure-Python parser, and `tests/fetch-nitpick-comments-test.sh` (Bash test with a fake `gh` stub, same shape as `claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh`) for the Bash orchestrator.
- Update `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`:
  - Step 2: fetch both the existing thread-comment array and the new Nitpick array as two labeled lists — "Actionable" (this port's new label for the existing thread-comment tier, matching PR #223's own vocabulary; SKILL.md currently has no explicit tier name since only one tier exists) and "Nitpick" — carried into Steps 3–5. Define "Actionable" at its first use in Step 2 so the new term is not left implicit.
  - Step 3: group-by-file across both lists.
  - Step 4: Nitpick items are always either a clear fix or a deferred-to-user item — CodeRabbit Nitpicks are advisory by definition, so "Question only" and "Approval" categories rarely apply, but the same four-category classification is reused.
  - Step 5: Nitpick items have no thread to reply to. Add a consolidated PR-level `gh pr comment` reply per handling pass that lists every processed Nitpick hash, each tagged with a `<!-- nitpick-addressed:<hash> -->` marker line, or the same items resurface on every future run.
  - Rationalization Defense table: port the PR #223 row about silently fixing Nitpicks without posting the marker.
- Sync `claude-code/skills/ywc-handle-pr-reviews/README.md` / `.en.md` / `.ja.md` / `.ko.md` to mention Nitpick-tier detection in the feature bullet list (mirroring the existing "주요 특징" style).
- Add the new script to the "Bundled Execution Scripts" table in `claude-code/skills/CLAUDE.md`.

## Out of Scope

- Any change to `codex/skills/ywc-handle-pr-reviews/` or `tools/codex-skill/skills/ywc-handle-pr-reviews/` — Codex bundle is explicitly out of scope per the user's request ("claude code 한정"). The Codex-side collector already has its own separate test-hardening plan ([20260826-codex-pr223-review-artifact-test-hardening.md](./20260826-codex-pr223-review-artifact-test-hardening.md)) that explicitly defers Nitpick work.
- Porting PR #223's `build-pr-title.py` `yw-<initials>-` prefix bugfix — verified already present and more robust in this repo's `claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py:44-72` (negative-lookahead-guarded `[a-z0-9]{2,4}` prefix regex vs. PR #223's simpler `[a-z]{1,8}` prefix regex). No action needed.
- Porting the unrelated bundled doc changes from PR #223 (`docs/claude-code-stssion-...md`, `prompts/ko-document-guidelines.md`) — these were an incidental author-retained addition in the upstream PR, not part of the Nitpick-detection feature, and have no counterpart need in this repo.
- Changing `fetch-unresolved-comments.sh`'s existing thread-comment contract or output schema.
- Any change to `ywc-create-pr`, `ywc-finish-branch`, or other skills beyond the one `references/CLAUDE.md` table-row addition.

## Existing Constraints Touched

| Existing artifact | Verified behavior | New code's interaction |
|---|---|---|
| `claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh:1-40+` | Fetches paginated thread comments, skips threads with a `<!-- <review_comment_addressed> -->` marker or a newer self-reply; outputs a JSON array with `id`, `body`, `path`, `line`, `user`, `created_at`, `thread_comment_count`. | Unchanged. The new `fetch-nitpick-comments.sh` runs alongside it as an independent second fetch — SKILL.md Step 2 carries both arrays as separate labeled lists, never concatenated, since Nitpick items lack an `id`/thread to reply to. |
| `claude-code/skills/ywc-handle-pr-reviews/SKILL.md:69-104` (Step 2 / Step 3) | Single fetch call, single JSON array, "if `[]` skip Steps 3–5 but still run Steps 7–8" gate logic. | Extend the empty-array check to both arrays: skip Steps 3–5 only when **both** are `[]`; a PR with 0 Actionable but nonzero Nitpick items (or vice versa) must still proceed to Step 3. |
| `claude-code/skills/ywc-handle-pr-reviews/SKILL.md:125-148` (Step 5) | Replies via the thread-reply API (`.../comments/{in_reply_to_id}/replies`) per processed comment. | Nitpick items use a different reply channel (`gh pr comment`, PR-level, not thread-level) since they have no `in_reply_to_id`. Both reply paths coexist in Step 5, branched by item tier. |
| `claude-code/skills/CLAUDE.md` "Bundled Execution Scripts" table | Lists `ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh` as the sole script for this skill. | Add one new row for `fetch-nitpick-comments.sh` following the existing table format (script path, skill, purpose). |
| `claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py:44-72` | Already handles `[a-z0-9]{2,4}-` initials prefixes via a negative-lookahead-guarded regex, more robust than PR #223's fix. | Confirms this plan does not need to touch this file — cited here only to close the "is this bugfix already applied" question raised in the request. |
| `scripts/validate.sh` | Runs shellcheck across `scripts/`, README Tier-1 presence checks, and `--list` dry run; does **not** currently execute per-skill Python/Bash unit tests directly (confirmed via `grep -n "shellcheck\|test_\|scripts/" scripts/validate.sh`) — those run standalone via their own `test_*.py` / `*-test.sh` invocation, following the pattern in `claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh`. | New tests follow the same standalone-invocation convention; `validate.sh` itself only needs the new script to be present, executable (for the `.sh` file), and shellcheck-clean. |

## Acceptance Criteria

- [ ] **AC1 — Parser correctness**: `extract-nitpick-comments.py`, given a CodeRabbit review body fixture with N Nitpick items across multiple files, emits a JSON array of exactly N objects with correct `hash`/`path`/`line_start`/`line_end`/`title`/`body`/`severity`/`parse_status` fields; a malformed per-file block yields a `parse_status: "raw_fallback"` item with its raw text preserved (never silently dropped).
- [ ] **AC2 — Fetch/dedup correctness**: `fetch-nitpick-comments.sh`, given multiple CodeRabbit reviews where the same Nitpick hash reappears, keeps only the most recent review's copy; items with a matching `nitpick-addressed:<hash>` marker in an existing PR-level comment authored by the current user are excluded from the output.
- [ ] **AC3 — Non-CodeRabbit reviews ignored**: Reviews authored by anyone other than `coderabbitai[bot]` are filtered out before parsing, so a human reviewer's prose is never misparsed as a Nitpick block.
- [ ] **AC4 — SKILL.md two-tier integration**: Step 2 fetches both arrays and labels them explicitly; the "skip Steps 3–5" condition requires **both** arrays to be `[]`; Step 5 adds the PR-level consolidated-comment reply path with the `nitpick-addressed:<hash>` marker for every processed Nitpick item.
- [ ] **AC5 — Regression safety**: The existing `fetch-unresolved-comments.sh` behavior and output schema are unchanged; existing Step 7/8 CI and merge-readiness gates are unaffected.
- [ ] **AC6 — Doc sync**: `README.md`/`.en.md`/`.ja.md`/`.ko.md` mention Nitpick-tier detection in the feature bullet list, each in the locale's required language per `claude-code/skills/CLAUDE.md`.
- [ ] **AC7 — Validation passes**: `bash scripts/validate.sh`, `shellcheck claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh`, and the two new test files (run standalone) all pass.
- [ ] **AC8 — Scope boundary**: No file under `codex/skills/` or `tools/codex-skill/` is touched.

## Functional Requirements

### FR-1: Nitpick body parser (`extract-nitpick-comments.py`)

Port PR #223's `HTMLParser`-based walker: locate the `<details><summary>Nitpick comments (N)</summary>` section, iterate per-file `<details>` blocks (`path (count)` summary), split each block's buffered inner markup into items terminated by `<!-- cr-comment:v1:<hash> --> ` markers, and extract `line_start`/`line_end` (from a `` `N` `` or `` `N-M` `` prefix), `title` (from a leading `**title**`), and `body` (remaining text, tags/comments stripped). Preserve PR #223's `raw_fallback` behavior and its `_sanitize_for_log` guard against log-injection from untrusted bot-authored text (CR/LF stripping, length truncation) — this handles genuinely untrusted third-party content and must not be dropped as "simplification."

### FR-2: Fetch/dedup/mark-exclusion orchestrator (`fetch-nitpick-comments.sh`)

Port PR #223's five-stage pipeline: (1) validate `<owner>/<repo>` and PR-number arguments, resolve the current `gh` user; (2) fetch all PR reviews via `gh api ... --paginate --slurp`, filter to `coderabbitai[bot]` only; (3) pipe each review body through the Python parser, tagging each item with `review_id`/`review_submitted_at`; (4) merge across reviews and dedup by `hash`, keeping the item from the most recent `review_submitted_at` (empty-hash `raw_fallback` items are excluded from hash-based dedup, since they are distinct per-occurrence); (5) fetch PR-level issue comments authored by the current user, scan for `nitpick-addressed:<hash>` markers, and exclude any item whose hash is already marked.

### FR-3: SKILL.md Step 2/3/5 integration

> ⚠️ SUPERSEDED by Iteration 1 — see §Amendment D (also covers Steps 4, 6, 9, and the Definition-of-Done table, not just Steps 2/3/5)

Step 2 gains a second `bash .../fetch-nitpick-comments.sh` call, documented with the same exit-code contract style as the existing call. The "if array is `[]`" skip-condition is rewritten to require both arrays empty. Step 3's grouping instruction is reworded to say "from both labeled lists." Step 5 gains a new subsection describing the PR-level consolidated reply: after processing all Nitpick items in a run, post one `gh pr comment` (not a per-item thread reply) listing each addressed item with its `<!-- nitpick-addressed:<hash> -->` marker, so `fetch-nitpick-comments.sh`'s FR-2 dedup-exclusion step can find it on the next run.

### FR-4: Rationalization Defense row

Add the PR #223 row verbatim (adapted to this skill's existing table voice): *"Nitpick items have no thread to reply to, so I'll just fix them silently without posting anything" → "Nitpick items still need a consolidated PR-level reply. Skipping it leaves no `nitpick-addressed` marker, so the fetch script's dedup never excludes them and the same items resurface on every future run."*

### FR-5: Test coverage

> ⚠️ SUPERSEDED by Iteration 1 — see §Amendment C (second bullet: bash test is `tests/fetch-nitpick-comments-test.sh`, not `scripts/test_fetch_nitpick_comments.sh`/`.py`)

- `scripts/test_extract_nitpick_comments.py`: fixture-driven, covers multi-file/multi-item bodies, a malformed block (`raw_fallback`), and the log-sanitization guard, following this repo's existing Python test idiom (plain `unittest`/assert-based, no pytest dependency — confirmed by scanning sibling skills' `test_*.py` files for their harness style before writing).
- `scripts/test_fetch_nitpick_comments.sh` (or `.py`, matching whichever idiom the sibling `build-pr-title-test.sh` establishes as this repo's `.sh`-script test convention): stubs `gh` with a fake executable returning fixture JSON, asserts dedup-by-hash-keeps-latest, marker-exclusion, and non-CodeRabbit-review filtering.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Determinism | `extract-nitpick-comments.py` makes no network calls (pure stdin/stdout); tests for both scripts must not require live `gh` authentication or network access — stub `gh` the same way `build-pr-title-test.sh`'s sibling tests and the Codex collector's test harness (see the related plan) do. |
| Security | Bot-authored review body content is untrusted third-party text; the log-sanitization guard (CR/LF escape, length cap) in FR-1 must be preserved, and the parser must never `eval`/execute any part of the body. |
| Idempotency | Re-running `fetch-nitpick-comments.sh` after a handling pass must exclude every previously marked item — verified by AC2's marker-exclusion test. |
| Compatibility | No changes to `fetch-unresolved-comments.sh`'s existing output contract; downstream consumers of that script's array shape are unaffected. |

## Edge Cases

- Zero CodeRabbit reviews on the PR → `fetch-nitpick-comments.sh` outputs `[]`, no error.
- A CodeRabbit review with a "Nitpick comments (N)" summary but zero actual parsed items (count mismatch) → emit an empty-array-for-that-review plus a stderr warning (never an error exit), matching PR #223's "hint only, never authoritative" rule for the `(N)` count.
- A Nitpick item's file path collides with a path already covered by an Actionable (thread) comment in the same run → Step 3's file-grouping naturally coalesces both into one file-level pass; no special-case code needed, this falls out of the existing "group by file" instruction extended to both lists.
- A `nitpick-addressed:<hash>` marker exists but was later edited/deleted from the PR-level comment → the hash is simply absent from the next scan and safely resurfaces (matches PR #223's documented safe-default; not a bug).
- PR has Nitpick items but zero Actionable comments → must still proceed past Step 2 to Steps 3–5 per AC4; verified by a dedicated test/manual-check scenario, not just code-read.

## Open Questions

- N/A — none identified. The reference implementation (PR #223) is merged and battle-tested upstream; this plan is a scoped, adapted port with no unresolved design decisions.

## Confidence Gate Note

Aggregate score 88 → **REVIEW** band (weakest dimension: `root_cause`=80). This is expected and accepted: `root_cause` scores lower because this plan ports an existing, already-validated upstream feature rather than diagnosing a fresh defect — there is no "root cause" to establish, only a faithful-adaptation risk (file-layout differences, test-harness idiom differences), which the Existing Constraints Touched and FR-5 rows above directly address. Proceeding without a second re-investigation cycle.

## Operative Sections

This spec has one amendment (Iteration 1). The amendment below **supersedes** the following original passages — treat the amendment's text as authoritative wherever it conflicts with the original:

- FR-2 (marker-scan scope, dedup semantics for `raw_fallback` items)
- FR-3 (Step 2/3/5 integration — extended to also cover Steps 4, 6, and 9, and the Definition-of-Done table)
- FR-5 / Scope's test-file description (bash test file path/name/language)
- Scope's README-locale bullet and AC6 (both said 4 Tier-1 files only; superseded by Amendment F's 6-file list)
- AC1, AC2, AC4 (superseded by Amendment B, A, and D respectively — see "Updated Acceptance Criteria" below)
- The Idempotency NFR row (superseded by Amendments A and E)

All other original sections (Out of Scope, Existing Constraints Touched, AC3/AC5/AC7/AC8, Edge Cases, other NFR rows) remain authoritative as originally written.

## Iteration 1 Amendments

> Source: `ywc-spec-validate` Iteration 1 report — 3 Critical, 6 Warning, 7 Suggestion. All Critical and Warning findings are addressed below; two cheap Suggestions are folded in as well. Remaining Suggestions (test-CI-registration note, HTMLParser external-dependency framing, "the new script" singular wording, Edge Case row 5 test-naming, `gh api` rate-limit NFR parity) are deferred — none block `DONE`.

### Amendment A — FR-2: marker-scan trust boundary (supersedes FR-2 dedup description; Critical #1)

`fetch-nitpick-comments.sh`'s marker scan (stage 5) intentionally checks **only** PR-level comments authored by the currently-authenticated `gh` user for `<!-- nitpick-addressed:<hash> -->` markers — this is a deliberate trust-boundary decision, not an oversight. Broadening the scan to any commenter would let a spoofed or compromised third-party comment containing the marker pattern silently suppress a real, unaddressed Nitpick.

**Stated limitation (add to NFR Idempotency row, spec:98):** this trust boundary means the idempotency guarantee holds only for reruns by the *same* authenticated identity. If a different team member re-runs `ywc-handle-pr-reviews` on the same PR under a different `gh` login, they will not see markers the first identity posted, and previously-addressed Nitpicks will resurface and be re-classified (re-fixing an already-fixed item is a no-op in practice, since the fix is already in the diff, but a redundant consolidated reply will be posted). This is accepted as a known limitation of the single-operator-per-PR-handling-pass model this skill already assumes elsewhere (the same is implicitly true of `fetch-unresolved-comments.sh`'s self-reply-timestamp check, which also reasons from "the authenticated user's" prior replies). No cross-identity marker-sharing mechanism is in scope for this port.

**AC2 update:** "items with a matching `nitpick-addressed:<hash>` marker in an existing PR-level comment **authored by the current authenticated user** are excluded from the output" (the current-user scoping is now an explicit, intentional part of the criterion, not an implementation detail).

### Amendment B — FR-1/FR-2/FR-3: `raw_fallback` items are never marked addressed (supersedes the marker-posting description in FR-3; Critical #2)

`raw_fallback` items (from FR-1, items with `hash: ""` or a syntactically-derived-but-unreliable hash) are **excluded from the consolidated-marker mechanism entirely**:

- **FR-1** (parser): unchanged — `raw_fallback` items may still carry `hash: ""` when no `<!-- cr-comment:v1:<hash> -->` marker could be located for the segment.
- **FR-2** (fetch/dedup): already correctly excludes empty-hash items from hash-based *dedup across reviews* (spec:77, unchanged). This amendment adds: empty-hash `raw_fallback` items are **also** excluded from the *addressed-marker exclusion* filter (stage 5) — they can never be matched against, and therefore never suppressed by, a `nitpick-addressed:<hash>` marker.
- **FR-3** (SKILL.md Step 5 reply channel): when composing the consolidated PR-level reply, `raw_fallback` items with `hash: ""` are still listed and described in the reply body (so the reviewer/user sees they were surfaced), but **no** `<!-- nitpick-addressed: -->` marker line is emitted for them. They will therefore always resurface on the next `fetch-nitpick-comments.sh` run for fresh review — this is the intended, safer behavior for content the parser could not confidently attribute to a stable identity, rather than risking hash-collision suppression across unrelated malformed items.

**AC1 update:** add "a `raw_fallback` item's empty hash (`hash: ""`) is never eligible for marker-based dedup or addressed-exclusion — verified by a dedicated test case."

### Amendment C — FR-5: bash test file path/name corrected (supersedes FR-5's test-file description; Critical #3)

FR-5's second bullet is corrected to read exactly as Scope already states (Scope:29 was correct; FR-5 diverged from it):

> `tests/fetch-nitpick-comments-test.sh`: a pure-Bash test script following the exact convention of `claude-code/skills/ywc-finish-branch/tests/build-pr-title-test.sh` — an `expect_*`-style assertion helper, a stubbed `gh` executable placed first on `PATH` (returning fixture JSON for `gh api user`, `gh api .../reviews`, `gh api .../comments`), and `fail()`-on-mismatch semantics. It is **not** a Python `subprocess`+`unittest` test, and it is **not** located under `scripts/` — both of FR-5's original hedges ("or `.py`", "matching whichever idiom the sibling `build-pr-title-test.sh` establishes") are resolved: the idiom is bash, in `tests/`, and this is now stated directly rather than deferred to implementation time.

The Python test (`scripts/test_extract_nitpick_comments.py`) is unaffected by this amendment — FR-5's first bullet (stdlib `unittest`, fixture-driven) was already consistent with Scope and is unchanged.

### Amendment D — FR-3 extended scope: Steps 4, 6, 9, and Definition-of-Done (supersedes FR-3's "Step 2/3/5 integration" framing; Warnings #5, #6, #7, #8)

FR-3 is retitled **"SKILL.md Step 2/3/4/5/6/9 and Definition-of-Done integration"** and gains the following, in addition to its original Step 2/3/5 content (unchanged):

- **Step 4 (classification):** insert the classification note already described in Scope (spec:33) — Nitpick items go through the same four-category classification as Actionable comments; "Question only" and "Approval" categories rarely apply since Nitpicks are advisory by definition, but no separate classification logic is introduced.
- **Step 6 (Error Handling table):** add one new row — `gh pr comment` (Nitpick consolidated reply) returns non-zero / 403 / 404 → log the error with the PR number and affected item count; do **not** write any `nitpick-addressed` marker for that batch (so the excluded-by-marker filter in FR-2 correctly re-surfaces them next run); report the failure and affected item count in Step 9's Final Summary. This is distinct from the existing thread-reply-API error row and does not modify it.
- **Step 9 (Final Summary):** add one new reporting line, separate from the existing "Comments: total processed vs skipped..." bullet — "Nitpick: total Nitpick items processed (Fixed/Deferred/No fix needed) vs any that failed to post (the `gh pr comment` error case above)."
- **Definition-of-Done table, Gate #1 row:** reword from "Every unresolved **thread** is fixed-or-answered and replied to" to "Every unresolved thread **and every unaddressed Nitpick item** is fixed-or-answered and replied to (via the thread-reply API or the consolidated PR-level comment, respectively)."

**AC4 update:** "Step 2 fetches both arrays and labels them explicitly; the 'skip Steps 3–5' condition requires both arrays to be `[]`; **Step 4 applies the same four-category classification to both tiers; Step 5 adds the PR-level consolidated-comment reply path with the `nitpick-addressed:<hash>` marker for every processed non-`raw_fallback` Nitpick item (per Amendment B); Step 6 gains the `gh pr comment` failure-handling row; Step 9 reports Nitpick counts separately; and the Definition-of-Done Gate #1 row covers both tiers.**"

### Amendment E — NFR Idempotency: concurrent-run race acknowledged (Warning #9)

Add to the Idempotency NFR row (spec:98): "Two concurrent invocations of `ywc-handle-pr-reviews` against the same PR (by the same identity) can race — both may fetch the same unaddressed Nitpick items before either posts its consolidated marker comment, resulting in two overlapping marker comments. This is an accepted limitation, not solved by this port (no distributed lock is introduced); the skill's existing single-operator-per-handling-pass usage pattern makes this a low-likelihood scenario, and a duplicate marker comment is self-correcting (both comments' hashes are still valid exclusions on the next run)."

### Amendment F — Scope/AC6: Tier-2 README locale sync (Warning #4)

Scope (spec:36) and AC6 (spec:65) are extended: the Nitpick-tier feature bullet is also added to `README.zh.md` and `README.es.md` — both already shipped by this skill (verified: `claude-code/skills/ywc-handle-pr-reviews/README.zh.md` and `README.es.md` exist on disk) — per `claude-code/skills/CLAUDE.md`'s rule that Tier-2 locales are "additionally maintained on skills that ship them." All six README files (`.md`, `.en.md`, `.ja.md`, `.ko.md`, `.zh.md`, `.es.md`) get the same one-bullet addition, each in its required language per the skills-directory language policy.

### Amendment G — Suggestion-tier folds (cheap fixes, no new FR needed)

- **FR-2 stage 2** (`gh api ... --paginate --slurp`): add one clause — "`--slurp` on a paginated array endpoint yields an array-of-page-arrays; flatten with `jq 'add // []'` (or equivalent) after `--slurp`, or use plain `--paginate` alone, which self-flattens multi-page array responses. The implementer verifies the actual `pulls/{pr}/reviews` response shape before finalizing this stage, since a silent wrong-nesting bug would feed malformed input to the parser without erroring."
- **AC1** (parser correctness): add — "A review body with no `Nitpick comments (N)` section at all (not just a zero-count section) yields `[]`, the same as the zero-count case."

### Updated Acceptance Criteria (affected items only)

- **AC1** — adds the no-section-at-all `[]` behavior (Amendment G) and the `raw_fallback` empty-hash non-eligibility clause (Amendment B).
- **AC2** — adds the explicit current-user-scoping statement (Amendment A).
- **AC4** — expanded per Amendment D to cover Steps 4/6/9 and the Definition-of-Done table, not just Steps 2/3/5.
- All other Acceptance Criteria (AC3, AC5, AC6 [text extended per Amendment F], AC7, AC8) are unchanged in substance.

### Step 4b.5 Self-Consistency Re-check (post-amendment)

- **Pass A (cross-section):** AC1/AC2/AC4 now map 1:1 to the amended FR-1/FR-2/FR-3 content (Amendments A/B/D/G) — no orphan ACs or FRs introduced. AC6's locale-file list (spec:65) now matches Scope's amended Amendment F list (6 files, not 4) — resolved, no residual drift.
- **Pass B (claim vs. reality):** Amendment C's precedent citation (`build-pr-title-test.sh`) was re-verified on disk during Iteration 1 review (confirmed pure-bash, `tests/` dir, `expect_*` helpers) — the amendment's description now matches the cited file exactly, closing the self-contradiction Critical #3 identified. Amendment A's "no cross-identity marker-sharing" claim is stated as an explicit accepted limitation, not an implicit gap — closing Critical #1.
- **Pass C (schema invariants):** N/A — no DB/schema change in this spec.

All three passes resolve to "yes, see Amendment A–G above." No fresh drift introduced by this amendment.
