# yw-000010-030-docs-skill-nitpick-integration

## Purpose
Wire the new Nitpick scripts (Tasks 010, 020) into `ywc-handle-pr-reviews`'s actual workflow — SKILL.md Steps 2/3/4/5/6/9 and the Definition-of-Done table — and sync the skill's documentation (six README locales, `claude-code/skills/CLAUDE.md`'s Bundled Execution Scripts table) so the feature is discoverable and correctly described. Without this task, the scripts from 010/020 exist but are never invoked by the skill.

## Scope
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`:
  - Step 2: add the `fetch-nitpick-comments.sh` call as a second, explicitly labeled "Nitpick" array alongside the existing "Actionable" (thread-comment) array; define "Actionable" at its first use; rewrite the "if array is `[]`" skip-condition to require **both** arrays empty.
  - Step 3: reword the grouping instruction to "from both labeled lists."
  - Step 4: insert the classification note — Nitpick items go through the same four-category classification; "Question only"/"Approval" rarely apply but no new logic is introduced.
  - Step 5: add the PR-level consolidated-reply subsection — one `gh pr comment` per handling pass listing every processed non-`raw_fallback` Nitpick item with its `<!-- nitpick-addressed:<hash> -->` marker; `raw_fallback` items are listed in the reply body but never get a marker line (Amendment B).
  - Step 6 (Error Handling table): add the `gh pr comment` failure row (non-zero/403/404 → log error + affected count, write no marker for that batch, report in Step 9).
  - Step 9 (Final Summary): add the separate "Nitpick:" reporting line.
  - Definition-of-Done table, Gate #1 row: reword to cover both thread comments and Nitpick items.
  - Rationalization Defense table: add the PR #223 row verbatim (adapted to this skill's voice) about not silently fixing Nitpicks without posting the marker.
- `claude-code/skills/ywc-handle-pr-reviews/README.md` / `.en.md` / `.ja.md` / `.ko.md` / `.zh.md` / `.es.md` — one feature bullet each, in the file's required language, mentioning Nitpick-tier detection (Amendment F: all six Tier-1+Tier-2 files, not just the four Tier-1 files).
- `claude-code/skills/CLAUDE.md` — one new row in the "Bundled Execution Scripts" table for `fetch-nitpick-comments.sh`, following the existing table format (script path, skill, purpose).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment D` — FR-3's full amended scope (Steps 2/3/4/5/6/9 + Definition-of-Done), supersedes the original FR-3.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#FR-4: Rationalization Defense row` — verbatim row text to add.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment B` (FR-3 sub-bullet) — `raw_fallback` items are listed in the reply but never get a marker line.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Amendment F` — Scope/AC6 six-file README locale sync.
- `docs/ywc-plans/20260826-claude-pr223-nitpick-comment-detection.md#Existing Constraints Touched` (spec:49-56) — exact before/after behavior for SKILL.md Step 2/3 and Step 5, and the `claude-code/skills/CLAUDE.md` table row format.
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (current file, already read in full) — Step 2 lines ~69-104 (empty-array skip gate), Step 5 lines ~125-148 (thread-reply channel), Definition of Done table lines ~34-46, Rationalization Defense table lines ~14-32.
- `claude-code/skills/CLAUDE.md` "Bundled Execution Scripts" section — existing table format and the one-line-per-script invocation convention.

### Summary
This task is pure documentation/workflow wiring — no new script logic. It threads the two scripts from Tasks 010/020 into the skill's step-by-step instructions so an LLM executing `ywc-handle-pr-reviews` actually calls `fetch-nitpick-comments.sh`, classifies and replies to Nitpick items correctly (via a PR-level consolidated comment rather than a thread reply, since Nitpick items have no `in_reply_to_id`), and reports Nitpick counts separately in the Final Summary. It also syncs all six README locale files and the shared `CLAUDE.md` Bundled Execution Scripts table so the feature is discoverable outside the SKILL.md body itself.

### Out of Scope (from spec)
- Any change to `codex/skills/` or `tools/codex-skill/` — Claude-Code-only per the whole spec's Out of Scope (spec:41).
- `build-pr-title.py`'s initials-prefix bugfix — already present and more robust in this repo (spec:42), no action.
- The unrelated bundled doc changes from upstream PR #223 (spec:43) — not ported.
- Changing `fetch-unresolved-comments.sh`'s contract (spec:44) — untouched by this task.

## Dependencies

### Depends On
- `yw-000010-020-domain-nitpick-fetch-orchestrator` — SKILL.md Step 2 must document and invoke this script's final, tested CLI contract (exact args, exit codes, output shape); writing the doc before the script's contract is finalized risks drift.

### Depended By
- (None — terminal task in this phase)

## Key Files
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.en.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.ja.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.ko.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.zh.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.es.md`
- `claude-code/skills/CLAUDE.md` (Bundled Execution Scripts table row only — do not touch other sections)

## Notes
- README locale writing rules are strict per `claude-code/skills/CLAUDE.md`: `.md` in Korean, `.ja.md` in Japanese, `.ko.md` in Korean, `.zh.md` in Simplified Chinese, `.es.md` in Spanish, `.en.md` in English — technical terms (API, Database, Skill, Agent, etc.) stay in English in every locale. Follow each file's existing "주요 특징"-equivalent bullet-list style; do not restructure the surrounding section.
- The Rationalization Defense row text is prescribed verbatim by FR-4 — do not paraphrase it away from the spec's given excuse/reality pair, only adapt voice/formatting to match the table's existing rows.
- This task edits `claude-code/skills/CLAUDE.md`, a file shared across all skills — touch only the one new table row; do not reformat or reorder existing rows.
- AC8 (scope boundary: no `codex/skills/` or `tools/codex-skill/` file touched) applies to the whole spec but is only fully verifiable once all three tasks are merged — run the AC8 grep check listed in Task Verify as this phase's final scope-boundary confirmation.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.en.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.ja.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.ko.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.zh.md`
- `claude-code/skills/ywc-handle-pr-reviews/README.es.md`
- `claude-code/skills/CLAUDE.md` (Bundled Execution Scripts table row only)

### Shared Surfaces
- `claude-code/skills/CLAUDE.md` "Bundled Execution Scripts" table — a document shared across every `ywc-*` skill; this task adds exactly one row and must not disturb others.

### Conflicts With
- (None identified)

### Parallelizable After
- `yw-000010-020-domain-nitpick-fetch-orchestrator`

### Task Verify
- `bash scripts/validate.sh`
- `grep -RIl 'nitpick' claude-code/skills/ywc-handle-pr-reviews/README*.md` — confirms all six locale files were touched
- `git diff --name-only` scoped to this task's commits, confirming zero paths under `codex/skills/` or `tools/codex-skill/` (AC8, manual scope check)

## Criticality
`normal` — documentation and workflow-wiring only, no new code execution paths.

## Out of Scope
- Any change to `codex/skills/` or `tools/codex-skill/`.
- Modifying `fetch-unresolved-comments.sh`'s existing thread-comment logic, Step 7 (CI gate), or Step 8 (merge-readiness gate) in SKILL.md — untouched by this spec.
- Restructuring or reformatting existing SKILL.md sections beyond the specific Step 2/3/4/5/6/9 and Definition-of-Done edits listed in Scope.
