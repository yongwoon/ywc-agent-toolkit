# Dispatch artifact: ywc-spec-writer (deleted body, run 2)

**Key**: claude-code/skills/ywc-spec-writer/SKILL.md:23-23
**Scenario**: I need help with the following: creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The request names multiple possible modes (initial creation, task-range incremental update, PR-based incremental update) but supplies no concrete flag, task ID/range, PR number(s), or commit ref. Per the skill's Step 1 (mode must be determined before acting) and Step 1.5 pre-check plus the Rationalization Defense table ('spec writer transcribes decided intent, it does not decide it'), picking a mode or inventing task/PR identifiers on the user's behalf is exactly the silent-pick behavior the procedure forbids. I would ask a clarifying question specifying the mode menu and requesting the missing identifiers before running any scripts or editing any spec file, rather than guessing.

## Actions
- Announce skill use: 'I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/.'
- Run `ls docs/specification/` (or equivalent existence check) to determine whether a spec already exists
- Read docs/specification/README.md (if present) to see current section index and change log
- Read CLAUDE.md at repo root for language policy / domain conventions
- Check for and Read docs/ubiquitous-language.md if present, for canonical vocabulary
- Apply Step 1.5 scope & intent pre-check: recognize the request names two different incremental modes (task-range, PR-based) plus implicit full create/update, with no concrete flag or identifiers given
- Ask the user a clarifying question to pin down mode and parameters before doing anything else, per the rule that a spec writer transcribes decided intent rather than picking one interpretation silently
- (If user answers with a task range) Run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range>` to resolve task IDs to directories
- (If user answers with a task range) Read each resolved task's README.md for its `category` field and map via references/section-mapping.md, then union the resulting sections
- (If user answers with PR numbers) Run `gh auth status` to confirm gh CLI authentication
- (If user answers with PR numbers) Run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <nums>` piped into `scripts/detect-affected-sections.sh`
- (If user answers with PR numbers) Run `gh pr view <num> --json number,title,body,headRefOid` for each PR to capture narrative context and headRefOid
- Enforce Safety threshold: if unioned affected sections > 4, stop and propose `--update` (Full Refresh) instead of patching piecemeal, and wait for explicit confirmation
- Read then Edit each affected docs/specification/NN-*.md file, writing in the resolved language with zero code, user-story format for features, plain-language data/flow descriptions, respecting per-section line caps
- Grep/inspect drafted text for inline-backtick ORM/SQL syntax (@default, @relation, SELECT, WHERE, dbgenerated) and paraphrase any hits into plain prose
- Cross-check any role/entity/domain terms introduced against docs/ubiquitous-language.md 'Synonyms to Avoid' column before finalizing 01-overview.md wording
- Read then Edit docs/specification/README.md to set Last updated to 2026-07-13 and append a change-log row with the correct <source> column (task IDs or PR numbers + headRefOid short SHAs)
- Run the Validation checklist (zero code, language match, only affected sections touched, changelog row present with source, safety-threshold confirmation if >4, no placeholder content, English technical terms preserved) before declaring done
- Print the Output Format confirmation block (Source, Modified sections, Unchanged sections, Index updated)

## Files touched
- docs/specification/README.md
- docs/specification/01-overview.md
- docs/specification/02-features.md
- docs/specification/03-data.md
- docs/specification/04-interfaces.md
- docs/specification/05-user-flows.md
- docs/specification/06-requirements.md
- docs/specification/07-glossary.md
- CLAUDE.md
- docs/ubiquitous-language.md
- claude-code/skills/ywc-spec-writer/references/section-mapping.md
- claude-code/skills/ywc-spec-writer/references/spec-structure.md
- claude-code/skills/ywc-spec-writer/references/language-resolution.md
- claude-code/skills/ywc-spec-writer/references/full-gen-workflow.md
- claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh
- claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh
- claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh
- claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh

## Gates enforced
- Step 1.5 scope & intent pre-check (ambiguous mode/parameters -> clarifying question, no silent pick)
- Step 1 mode determination gate (must know which of --full/--update/--from-task/--from-tasks/--from-commit/--from-pr/--from-prs applies before acting)
- Always-read-before-writing gate (README.md, CLAUDE.md, ubiquitous-language.md read before any spec edit)
- Safety threshold gate (>4 unioned affected sections -> stop and propose --update, require explicit user confirmation to proceed incrementally)
- Zero-program-code gate across all sections, including inline-backtick ORM/SQL syntax check
- Ubiquitous Language cross-check gate against Synonyms-to-Avoid column
- PR provenance gate (headRefOid + PR numbers must be recorded in README changelog)
- Task Range provenance gate (every resolved task ID listed in README changelog)
- README index/changelog update gate (date + source column) after every write
- Section file size cap gate (400 lines default, higher for large projects)
- Final Validation checklist gate before declaring the skill's task complete

## Full narrative

I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/.

Before touching anything, I would first ground myself in current state, since the skill's non-negotiable rule is "always read before writing" — editing without reading risks silently overwriting valid content:

1. Check whether `docs/specification/` already exists (`ls docs/specification/`). If it exists, Read `docs/specification/README.md` to see the current section index and change-log history — this tells me whether we're in "spec already established, needs an incremental patch" territory or "nothing exists yet, needs Full Generation."
2. Read the repository's `CLAUDE.md` for any documentation language policy or domain conventions that should govern the spec.
3. Check for `docs/ubiquitous-language.md`; if present, Read it so any canonical terms are used verbatim later and so I can cross-check for banned synonyms before drafting `01-overview.md`.

At that point I'd hit a hard stop rather than proceed. Your request bundles together three distinct things the skill treats as separate, mutually-exclusive modes: (a) creating a spec from scratch (`--full`, which additionally requires explicit user confirmation before it's allowed to run), (b) a task-range incremental update (`--from-tasks <range>`), and (c) a PR-based incremental update (`--from-pr`/`--from-prs`). None of these came with the concrete parameters the skill needs to act — no task IDs or range (e.g. `000002-010..000003-020`), no PR numbers, and no indication of whether a spec already exists. The skill's own Rationalization Defense table calls out exactly this trap ("User seems to want a full spec — I'll generate it without --full to save time" and "Intent is clear enough — start writing without an up-front scope check" are both listed as excuses to reject), and Step 1.5 requires surfacing this as a clarifying question rather than silently deciding — a spec writer transcribes decided intent, it doesn't decide it.

So, concretely, my next message to you would be something like:

"To proceed I need to pin down which mode to run:
1. Full generation (if docs/specification/ doesn't exist yet) — I'll need your explicit confirmation to run `--full`, since it invokes the best available model and creates all 7 section files from scratch.
2. Full refresh of an existing spec — `--update`, regenerates all existing sections.
3. Task-range update — please give me the task ID(s)/range/glob, e.g. `000002-010..000003-020`.
4. PR-based update — please give me the PR number(s), e.g. `42, 43`.
5. Latest-commit auto-update — if you just want the last commit's diff reflected, I can run that with no extra input.

Which of these applies, and if it's option 3 or 4, what are the specific IDs/PR numbers?"

I would wait for your answer before running anything. Once you answer, here is exactly what I would do for each named path:

**If you give me a task range** (e.g., `--from-tasks 000002-010..000003-020`):
- Run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh 000002-010..000003-020` to resolve the range/glob/multi-id set to absolute task directory paths.
- For each resolved task directory, Read `<task-dir>/README.md` to pull its `category` field, then look that category up in `claude-code/skills/ywc-spec-writer/references/section-mapping.md` to get the affected spec section(s), and union all the results across tasks.
- Enforce the safety threshold: if the unioned section count exceeds 4, stop and propose `--update` (Full Refresh) instead, and wait for your explicit confirmation before doing anything piecemeal.
- Otherwise, for each affected section file (e.g. `docs/specification/02-features.md`, `docs/specification/03-data.md`), Read current content, then Edit it — user-story format ("As a [user], I want [action] so that [benefit]") for features, plain-language descriptions for data/flows, zero program code, and a check of any inline backticks against ORM/SQL syntax patterns (`@default`, `@relation`, `SELECT`, `WHERE`, `dbgenerated(...)`) to paraphrase rather than leak schema syntax.
- Read then Edit `docs/specification/README.md`: set `**Last updated**` to 2026-07-13, and append a row like `| 2026-07-13 | 02-features.md, 03-data.md | tasks 000002-010..000003-020 (N tasks) | <summary> |`, listing every resolved task ID inline or as sub-bullets if there are more than five.
- Print the confirmation block: Source (task range + every resolved ID), Modified sections, Unchanged sections, Index updated.

**If you give me PR numbers** (e.g., `--from-prs 42 43`):
- Confirm `gh auth status` succeeds (external dependency required for this mode).
- Run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh 42 43 | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh` to get the deduplicated union of affected sections across both PRs' changed files.
- Run `gh pr view 42 --json number,title,body,headRefOid` and the same for PR 43, to capture each PR's title/body as narrative "why" context and to record `headRefOid` for reproducibility.
- Enforce the same >4-sections safety threshold as above.
- Read then Edit each affected section file, folding the PR narrative into the prose, applying the same zero-code / no-ORM-SQL-leak checks.
- Read then Edit `docs/specification/README.md`: update the date and append `| 2026-07-13 | <sections> | PRs #42 @ <headRefOid-short>, #43 @ <headRefOid-short> | <summary> |`.
- Print the confirmation block with Source listing both PR numbers and their head SHAs.

**If you confirm full generation** (`--full`, only after your explicit go-ahead):
- Resolve output language per Step 3 (flag → project CLAUDE.md `## Language Policy` → user `~/.claude/CLAUDE.md ## Language Policy` → terminal fallback). Neither this repo's `CLAUDE.md` nor the global one defines a `## Language Policy` heading, so I'd fall back to the repo's own documented convention of Korean-default docs and default to `ko`, without needing to interrupt you further unless you explicitly want to pick a language.
- Run `bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh ko "<ProjectName>"` to scaffold the 7-section skeleton.
- Follow `claude-code/skills/ywc-spec-writer/references/full-gen-workflow.md` for the detailed analysis steps, using the best available model, reading project directory structure, `docs/ywc-plans/`, schema/config files, etc.
- Apply the full-mode-only non-negotiables: quantitative NFR targets sourced from constants/config files (else moved to Open Questions), every schema model named in `03-data.md`, a Role × Action matrix if ≥3 actor roles exist, a Data Lifecycle subsection if audit/analytics data exists, constants files cited under "Existing Constraints Touched," a Ubiquitous Language cross-check, and no ORM/SQL syntax leakage anywhere.
- Self-check against the `ywc-spec-validate` rubric, targeting Gate ≥ 90 for full mode.

In every branch, before declaring the work done I would run through the skill's Validation checklist: confirm zero code in any section, confirm the language matches what was resolved, confirm only the affected sections were touched (for incremental modes), confirm `docs/specification/README.md`'s change log carries today's date and the correct `<source>` column, confirm every task ID or PR headRefOid is recorded, confirm the >4-section safety-threshold gate was honored, confirm no section still has "To be written" placeholder text, and confirm technical terms stayed in English per the language policy rather than being transliterated.

I would not run any of the above scripts, nor edit any file under `docs/specification/`, until you've told me which mode you want and given me the concrete task IDs or PR numbers, since guessing at that boundary is precisely what the procedure instructs me not to do.
