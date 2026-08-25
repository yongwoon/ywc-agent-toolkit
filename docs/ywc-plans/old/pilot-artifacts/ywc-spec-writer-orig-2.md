# Dispatch artifact: ywc-spec-writer (original body, run 2)

**Key**: claude-code/skills/ywc-spec-writer/SKILL.md:23-23
**Scenario**: I need help with the following: creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a refusal — an escalation via clarifying question. The user's request names the two incremental mechanisms (task-range, PR-based) as capabilities to support but supplies no concrete mode flag, no task ID range, no PR number(s), and no confirmation of --full vs --update. Per Step 1 (Determine Mode) and Step 1.5 (Scope & Intent Pre-Check) plus the Rationalization Defense entry on never auto-generating a full spec without the explicit flag and confirmation and never silently deciding an ambiguous point, the procedure requires stopping to ask which mode applies and, for the incremental modes, the exact identifiers (task id range like 000002-010..000003-020, or specific PR numbers) before any script (resolve-task-paths.sh, collect-files-from-prs.sh, detect-affected-sections.sh, init-spec-structure.sh) is invoked, since those scripts have no valid input to resolve otherwise.

## Actions
- Read claude-code/skills/ywc-spec-writer/SKILL.md (already done per task setup)
- Announce skill usage: 'I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/.'
- Bash: ls docs/specification/ (and git status) to determine whether the spec directory already exists
- Read: docs/specification/README.md (if it exists) — mandatory Step 2 context read
- Read: CLAUDE.md (root and project-level) for language policy and domain conventions
- Read: docs/ubiquitous-language.md (if it exists) for canonical terms
- Determine invocation mode per Step 1 table — none of --full/--update/--from-task/--from-tasks/--from-commit/--from-pr/--from-prs/no-flag-Auto was actually specified with concrete identifiers by the user
- Ask a clarifying question rather than guess: which mode (first-time --full vs --update refresh vs incremental), and if incremental via task range, the exact <start-id>..<end-id>; if PR-based, the exact PR number(s)
- Once identifiers are supplied: Bash: bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range/glob/ids> for task-range mode
- Once identifiers are supplied: Bash: bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <pr#> [<pr#> ...] | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh for PR-based mode
- Bash: gh pr view <num> --json number,title,body,headRefOid for each PR (narrative context + reproducibility SHA), after first checking gh auth status
- Read each resolved task's README.md for its category field and cross-reference references/section-mapping.md to union affected sections
- Enforce Step 5 safety threshold: if unioned affected sections > 4, stop and propose --update (Full Refresh) instead of patching
- If docs/specification/ does not exist: Bash: bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh <lang> "<ProjectName>" to scaffold the 7-section skeleton
- Resolve output language via references/language-resolution.md precedence chain before writing; ask the user only if no policy is found anywhere and disambiguation is needed
- Write/update only the mapped section files under docs/specification/, enforcing: zero program code, user-story format for features, dual-audience readability, section size caps, no ORM/SQL/schema syntax even in inline backticks, quantitative NFR targets, UL avoid-list cross-check
- Update docs/specification/README.md: set Last updated date and append a change-log row with section(s), <source> (task IDs enumerated or PR # @ headRefOid), and one-line summary
- Run the Validation checklist from SKILL.md before declaring done (no placeholders, language matches policy, source provenance recorded, >4-section confirmation logged if applicable)

## Files touched
- claude-code/skills/ywc-spec-writer/SKILL.md (read only)
- docs/specification/README.md
- docs/specification/01-overview.md .. 07-glossary.md (only sections mapped to the affected scope)
- CLAUDE.md
- docs/ubiquitous-language.md

## Gates enforced
- Step 1 Mode Determination — no explicit flag or concrete identifier supplied by user, so mode cannot be inferred
- Step 1.5 Scope & Intent Pre-Check — ambiguous/irreversible choice (which mode, which task range, which PRs) must be surfaced as a clarifying question, never silently decided
- Rationalization Defense: 'User seems to want a full spec — I'll generate it without --full' — full generation requires explicit --full AND user confirmation, never inferred
- Rationalization Defense: dedup union file list before section detection for multi-PR sources
- Rationalization Defense: always record headRefOid and PR numbers / every resolved task ID in the README index entry
- Step 5 Safety threshold (>4 affected sections triggers propose --update instead of patching)
- Step 6 non-negotiable writing rules (zero code, dual audience, section size caps, no ORM/SQL/schema syntax leak, UL cross-check, quantitative NFR targets)
- Step 7 README index update with <source> provenance
- External dependency gate: gh CLI must be authenticated for --from-pr/--from-prs before those scripts are run
- Pre-Review Validation checklist before declaring the skill's task complete

## Full narrative

Here is exactly how I would proceed under the ywc-spec-writer procedure for this request.

First, I would announce the skill per its required opening line: "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."

**Context gathering (Step 2, mandatory before any writing):**
- Run `ls docs/specification/` (and check `git status`) to determine whether the spec directory already exists — this decides whether we're in "create" or "update" territory.
- Read `docs/specification/README.md` if present, to see the current spec state and prior change-log entries.
- Read the project's `CLAUDE.md` for its language policy and domain conventions.
- Read `docs/ubiquitous-language.md` if it exists, to pull canonical terminology I'd need to use verbatim later.

**Mode determination (Step 1) — and where I would stop:**
The skill requires picking exactly one mode from: `--full`, `--update`, `--from-task <path>`, `--from-tasks <range/glob/ids>`, `--from-commit <ref>`, `--from-pr <num>`, `--from-prs <num...>`, or no-flag Auto (last-commit diff). The user's message describes the two incremental mechanisms it wants supported — task-range and PR-based updates — but gives no concrete task ID range, no PR numbers, and doesn't say whether this is a first-time full generation or a refresh of an existing spec.

Per Step 1.5 (Scope & Intent Pre-Check) and the Rationalization Defense table — specifically the entries "User seems to want a full spec — I'll generate it without --full" (full generation needs the explicit flag AND user confirmation) and "Intent is clear enough — start writing without an up-front scope check" (ambiguity must be surfaced, not resolved silently) — I would not guess. I would ask a clarifying question along these lines:

"To proceed, could you confirm: (1) Is docs/specification/ being created for the first time, or is this an update to an existing spec? (2) If incremental, which source should drive the update — a specific task ID range (e.g. `000002-010..000003-020`), specific PR number(s) (e.g. `#42 #43`), or the latest commit? (3) Any preferred output language, or should I default to Korean per the project's language policy?"

**What I would do once those identifiers are supplied**, without further prompting:

- *Task-range mode*: Run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range>` to resolve the IDs/glob to absolute task directory paths, then read each resolved task's `README.md` for its `category` field, cross-reference `references/section-mapping.md`, and union the resulting section lists.
- *PR-based mode*: First check `gh auth status` (the skill's stated external dependency). Then run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <pr#> [<pr#> ...] | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh`, and separately run `gh pr view <num> --json number,title,body,headRefOid` for each PR to capture narrative context and the reproducibility SHA.
- Enforce the Step 5 safety threshold: if the unioned affected-section count exceeds 4, I would stop and propose `--update` (Full Refresh) instead of patching piecemeal, per the Rationalization Defense entry on that exact excuse.
- If `docs/specification/` doesn't exist yet, run `bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh <lang> "<ProjectName>"` with the language resolved via `references/language-resolution.md`'s precedence chain (`--lang` flag → project CLAUDE.md → user CLAUDE.md → Korean default).
- Write only the mapped section files, enforcing the non-negotiable rules: zero program code anywhere (including inline backticks containing executable ORM/SQL syntax), user-story format for features, dual-audience readability, per-section line caps (400 default, scaling for large projects), quantitative NFR targets (no vague placeholders), and the ubiquitous-language avoid-list cross-check before touching `01-overview.md`.
- Update `docs/specification/README.md` with today's date and a change-log row recording the `<source>` (every resolved task ID enumerated, or PR number(s) with `headRefOid` short SHA).
- Run through the Validation checklist (no code, language correctness, only affected sections touched, provenance recorded, no placeholder content) before declaring the work complete.

I would not run `init-spec-structure.sh`, `resolve-task-paths.sh`, or `collect-files-from-prs.sh` speculatively against invented task IDs or PR numbers — those scripts require real identifiers to resolve, and fabricating them would silently commit to a scope the user never specified. That's the one point where I'd pause and ask rather than proceed.
