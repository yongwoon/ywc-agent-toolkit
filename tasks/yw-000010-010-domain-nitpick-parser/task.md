# yw-000010-010-domain-nitpick-parser — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md` (the three new files under `claude-code/skills/ywc-handle-pr-reviews/scripts/`)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if the parsing contract needs a field not listed in the spec's FR-1 (`hash`, `path`, `line_start`, `line_end`, `title`, `body`, `severity`, `parse_status`) — surface to the user rather than inventing one
- [ ] Stop if implementing the log-sanitization guard would require a new third-party dependency — stdlib only
- [ ] Stop if another in-flight task already owns `claude-code/skills/ywc-handle-pr-reviews/scripts/**`

## Implementation Steps

- [ ] **Build `extract-nitpick-comments.py`'s HTML walker**
  - [ ] Subclass `html.parser.HTMLParser` (stdlib) to locate the `<details><summary>Nitpick comments (N)</summary>` section in the review body read from stdin
  - [ ] Iterate per-file `<details>` blocks, parsing each summary's `path (count)` text with a regex
  - [ ] Within each file block, split buffered inner markup into items on `<!-- cr-comment:v1:<hash> -->` marker boundaries
  - [ ] Per item, extract `line_start`/`line_end` from a leading `` `N` `` or `` `N-M` `` prefix (regex), `title` from a leading `**title**` markdown bold span, and `body` from the remaining text with HTML tags and comments stripped

- [ ] **Implement `raw_fallback` and count-mismatch handling**
  - [ ] When a per-file block cannot be parsed into a well-formed item (no hash marker found, or the item structure is malformed), emit `{"hash": "", "parse_status": "raw_fallback", "path": <path>, "body": <raw preserved text>, "severity": "nitpick", "line_start": null, "line_end": null, "title": null}` — never drop the content
  - [ ] Compare the summary's declared `(N)` count against the actual parsed item count for that file block; on mismatch, write a warning to stderr (never a non-zero exit) — the count is documented as a hint only, not authoritative
  - [ ] When the review body has no `Nitpick comments (N)` section at all, or the section declares count `0`, emit `[]` on stdout (both cases, same output)

- [ ] **Implement `_sanitize_for_log`**
  - [ ] Port the log-injection guard: strip/escape CR (`\r`) and LF (`\n`) characters, truncate to a bounded length, before any bot-authored text reaches a log/stderr line
  - [ ] Apply it to every stderr warning that includes bot-authored content (e.g., the count-mismatch warning above)
  - [ ] Never call `eval`/`exec`/dynamic code execution on any part of the parsed body

- [ ] **Write the fixture**
  - [ ] Create `scripts/fixtures/nitpick-review-body.html` with: a well-formed multi-file, multi-item Nitpick section; one malformed per-file block (triggers `raw_fallback`); one file-block count mismatch case
  - [ ] Include a body with no Nitpick section at all (either as a second fixture file or a second in-test literal, implementer's choice, as long as the empty-array test case in AC1 is covered)

- [ ] **Write `test_extract_nitpick_comments.py`**
  - [ ] Follow the repo's plain `unittest`/assert-based idiom (no pytest) — mirror `.claude/skills/ywc-toolkit-eval/scripts/test_score.py`'s style
  - [ ] Cover: multi-file/multi-item body → correct N objects with correct fields (AC1)
  - [ ] Cover: malformed block → `raw_fallback` with raw text preserved, `hash: ""` (AC1, Amendment B)
  - [ ] Cover: log-sanitization guard strips CR/LF and truncates length (NFR Security)
  - [ ] Cover: no-section-at-all and zero-count-section both yield `[]` (Amendment G)
  - [ ] Cover: count-mismatch emits a stderr warning, exit code still 0 (Edge Cases)

## Task Verify
- [ ] `python3 claude-code/skills/ywc-handle-pr-reviews/scripts/test_extract_nitpick_comments.py` exits 0

## Verification
- [ ] lint passes — N/A (no repo-wide Python lint configured; rely on test coverage and manual read)
- [ ] typecheck passes — N/A (no mypy/type-check pipeline configured for this repo's Python scripts)
- [ ] unit tests pass (`python3 claude-code/skills/ywc-handle-pr-reviews/scripts/test_extract_nitpick_comments.py`)
- [ ] integration tests pass — N/A (covered end-to-end by Task 020's fetch-script test once wired)
- [ ] app builds without error — N/A (no build step for standalone Python scripts in this repo)
