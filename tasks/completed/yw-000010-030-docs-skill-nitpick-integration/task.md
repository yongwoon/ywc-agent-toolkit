# yw-000010-030-docs-skill-nitpick-integration — Implementation Checklist

## Prerequisites
- [ ] `yw-000010-010-domain-nitpick-parser` is completed (merged)
- [ ] `yw-000010-020-domain-nitpick-fetch-orchestrator` is completed (merged) — `fetch-nitpick-comments.sh`'s final CLI contract (args, exit codes, output JSON shape) is stable

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md` (SKILL.md, the six README locale files, and the one Bundled Execution Scripts table row in `claude-code/skills/CLAUDE.md`)
- [ ] Do not touch `codex/skills/` or `tools/codex-skill/` under any circumstance (AC8)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `fetch-nitpick-comments.sh`'s actual CLI contract (from Task 020) differs from what this task assumes — re-read the merged script before writing Step 2
- [ ] Stop if a README locale file's existing structure has no natural bullet-list section to extend — surface to the user rather than restructuring the file
- [ ] Stop if editing `claude-code/skills/CLAUDE.md`'s Bundled Execution Scripts table would require reformatting existing rows

## Implementation Steps

- [ ] **SKILL.md Step 2 — dual fetch**
  - [ ] Add a second `bash claude-code/skills/ywc-handle-pr-reviews/scripts/fetch-nitpick-comments.sh {owner}/{repo} {pr_number}` call block, documented with the same exit-code contract style as the existing `fetch-unresolved-comments.sh` call
  - [ ] Label the existing thread-comment array "Actionable" at its first use (define the term inline, since SKILL.md currently has no explicit tier name)
  - [ ] Label the new array "Nitpick"
  - [ ] Rewrite the "If the array is `[]`" skip-condition (spec:82 equivalent) to require **both** arrays empty before skipping Steps 3–5; a PR with 0 Actionable but nonzero Nitpick (or vice versa) must still proceed

- [ ] **SKILL.md Step 3 — grouping**
  - [ ] Reword the grouping instruction to "group all remaining comments, from both labeled lists, by target file path"

- [ ] **SKILL.md Step 4 — classification**
  - [ ] Insert a note: Nitpick items go through the same four-category classification table as Actionable comments; "Question only" and "Approval" categories rarely apply since Nitpicks are advisory by definition, but no separate classification logic is introduced

- [ ] **SKILL.md Step 5 — consolidated Nitpick reply**
  - [ ] Add a new subsection: after processing all Nitpick items in a run, post one `gh pr comment` (PR-level, not a thread reply) listing every processed **non-`raw_fallback`** Nitpick item with a `<!-- nitpick-addressed:<hash> -->` marker line per item
  - [ ] `raw_fallback` items (`hash: ""`) are described in the reply body for visibility but never get a marker line — they will always resurface on the next `fetch-nitpick-comments.sh` run by design (Amendment B)
  - [ ] Keep the existing thread-reply-API subsection for Actionable comments unchanged; both reply paths coexist, branched by item tier

- [ ] **SKILL.md Step 6 — error handling row**
  - [ ] Add one new row to the Error Handling table: `gh pr comment` (Nitpick consolidated reply) returns non-zero/403/404 → log the error with PR number and affected item count; do not write any marker for that batch; report the failure and count in Step 9
  - [ ] Do not modify the existing thread-reply-API error row

- [ ] **SKILL.md Step 9 — Final Summary**
  - [ ] Add a new "Nitpick:" bullet, separate from the existing "Comments:" bullet — total Nitpick items processed (Fixed/Deferred/No fix needed) vs any that failed to post

- [ ] **SKILL.md Definition-of-Done table**
  - [ ] Reword Gate #1's "Cleared when" cell from "Every unresolved thread is fixed-or-answered and replied to" to "Every unresolved thread and every unaddressed Nitpick item is fixed-or-answered and replied to (via the thread-reply API or the consolidated PR-level comment, respectively)"

- [ ] **SKILL.md Rationalization Defense table**
  - [ ] Add the row: `"Nitpick items have no thread to reply to, so I'll just fix them silently without posting anything"` → `"Nitpick items still need a consolidated PR-level reply. Skipping it leaves no nitpick-addressed marker, so the fetch script's dedup never excludes them and the same items resurface on every future run."`

- [ ] **README locale sync (six files)**
  - [ ] `README.md` (Korean prose, English technical terms) — add one feature bullet mentioning Nitpick-tier detection
  - [ ] `README.en.md` (English) — same bullet in English
  - [ ] `README.ja.md` (Japanese prose, English technical terms) — same bullet
  - [ ] `README.ko.md` (Korean) — same bullet
  - [ ] `README.zh.md` (Simplified Chinese prose, English technical terms) — same bullet, preserve the file's `AUTO-GENERATED` header if present
  - [ ] `README.es.md` (Spanish prose, English technical terms) — same bullet, preserve the file's `AUTO-GENERATED` header if present

- [ ] **`claude-code/skills/CLAUDE.md` table row**
  - [ ] Add one row to "Bundled Execution Scripts": `fetch-nitpick-comments.sh <owner/repo> <pr>` | `ywc-handle-pr-reviews` | one-line purpose description, matching the existing row format exactly

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0
- [ ] `grep -RIl 'itpick' claude-code/skills/ywc-handle-pr-reviews/README*.md` returns all six files
- [ ] Manual scope check: `git diff --name-only` for this task's commits shows zero paths under `codex/skills/` or `tools/codex-skill/` (AC8)

## Verification
- [ ] lint passes — N/A (Markdown-only changes; `scripts/validate.sh` covers structural checks)
- [ ] typecheck passes — N/A
- [ ] unit tests pass — N/A (no new script logic in this task; Tasks 010/020 own their own tests)
- [ ] integration tests pass — N/A
- [ ] app builds without error — N/A (documentation-only task)
