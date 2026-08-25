# Dispatch artifact: ywc-spec-writer (original body, run 1)

**Key**: claude-code/skills/ywc-spec-writer/SKILL.md:23-23
**Scenario**: I need help with the following: creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The request describes the two incremental-update capabilities (task-range, PR-based) in the abstract but supplies no concrete driver — no task ID range, no PR numbers, and no explicit --full/--update flag, and it's unclear whether docs/specification/ already exists in this repository. Per the skill's own discipline ('a spec writer transcribes decided intent, it does not decide it' — Step 1.5 and the Rationalization Defense table), I would not guess a task range or PR set, nor silently default to --full generation. I would ask a clarifying question first: which task ID range and/or which PR numbers should drive the update (or, if no prior spec exists, whether to run --full instead), plus confirm the output language if not the ko default — and only then execute Steps 2 through 8 exactly as specified.

## Actions
- Read claude-code/skills/ywc-spec-writer/SKILL.md (already done, sole procedure)
- Announce skill usage: 'I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/.'
- Step 1 (Determine Mode): recognize the request carries no concrete flag (--full/--update/--from-task/--from-tasks/--from-commit/--from-pr/--from-prs) and no concrete task IDs or PR numbers
- Ask a clarifying question rather than guess: request the specific task ID range (e.g. 000002-010..000003-020) and/or PR numbers (e.g. 42 43 51) to drive the update, and whether docs/specification/ already exists (full generation vs incremental)
- Run ls docs/specification/ to check current state before deciding full-vs-incremental once params are supplied
- Read docs/specification/README.md (if it exists) for current spec state
- Read CLAUDE.md for language policy and domain conventions
- Read docs/ubiquitous-language.md (if it exists) for canonical terms
- Step 3: resolve output language via references/language-resolution.md precedence chain (--lang flag > project CLAUDE.md ## Language Policy > user ~/.claude/CLAUDE.md ## Language Policy > terminal fallback); default to ko absent an explicit policy
- Step 4: if docs/specification/ absent, run bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh <lang> "<ProjectName>"
- Step 5 (Task Range branch, once IDs supplied): run bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range/glob/ids>, then read each resolved task's README.md category field and map via references/section-mapping.md
- Step 5 (PR branch, once PR numbers supplied): run bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <nums> piped into scripts/detect-affected-sections.sh, and gh pr view <num> --json number,title,body,headRefOid for each PR to capture narrative context and headRefOid
- Union all detected sections across task-range and PR sources; if the union exceeds 4 sections, stop and propose --update (Full Refresh) to the user instead of patching piecemeal
- Step 6: write/update only the affected docs/specification/*.md section files following non-negotiable rules (zero code, dual-audience prose, user-story format, section size caps, record ambiguous readings under ## Open Questions instead of deciding them)
- Step 7: update docs/specification/README.md — set Last updated to today's date and append a change-log row with the <source> column populated per mode (tasks <range> (<n> tasks) with every resolved ID listed; PRs #<n> @ <headRefOid-short> for each)
- Run the Validation checklist (no code leaked, language correct, only affected sections touched, README log has source+today's date+resolved IDs/SHAs, >4-section threshold explicitly confirmed if exceeded, no placeholder content remains, technical terms kept in English)
- Report the Output Format block for Task Range / Multi and for PR-based per the skill's templates

## Files touched
- claude-code/skills/ywc-spec-writer/SKILL.md (read only)
- docs/specification/README.md
- docs/specification/01-overview.md ... 07-glossary.md (only sections mapped to affected scope)
- CLAUDE.md
- docs/ubiquitous-language.md

## Gates enforced
- Step 1 mode-determination gate: no flag/parameters supplied by user, so mode cannot be silently assumed
- Step 1.5 intent-confirmation gate: irreversible/ambiguous choices are surfaced as a question or recorded under Open Questions rather than decided unilaterally
- Step 5 safety threshold: >4 unioned affected sections triggers a stop-and-propose-`--update` gate instead of piecemeal patching
- Rationalization Defense: never auto-run --full without explicit flag + user confirmation
- Rationalization Defense: never fabricate task IDs or PR numbers to proceed without them
- Validation checklist gate before declaring the write complete

## Full narrative

I would begin by announcing the skill per its required opening line: "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."

Following Step 1 (Determine Mode), the skill routes on an explicit flag: --full, --update, --from-task, --from-tasks, --from-commit, --from-pr, --from-prs, or Auto (no flags, last-commit diff). The user's message names the two incremental modes generically ("task-range and PR-based incremental updates") but supplies no actual task ID range, no PR numbers, and no explicit --full/--update flag. Per Step 1.5 (Scope & Intent Pre-Check) and the Rationalization Defense table's explicit warnings against silently picking a reading or auto-generating without the explicit flag, I would not proceed by guessing parameters. I would ask a clarifying question: "Could you specify the task ID range (e.g. --from-tasks 000002-010..000003-020) and/or the PR number(s) (e.g. --from-prs 42 43) that should drive this spec update? Also, does docs/specification/ already exist in this repository, or is this the first time the spec is being generated (in which case --full would apply instead)?" I would wait for that answer before touching any files.

Once concrete identifiers are supplied, I would proceed exactly as the procedure specifies:

Step 2 (Collect Context) — read docs/specification/README.md if it exists (to learn current spec state), CLAUDE.md (language policy, domain conventions), and docs/ubiquitous-language.md if present (canonical terms to reuse verbatim).

Step 3 (Language Setup) — resolve output language via the precedence chain in references/language-resolution.md: --lang flag, then project CLAUDE.md's ## Language Policy section, then the user's ~/.claude/CLAUDE.md ## Language Policy section, then the skill's terminal fallback (honor a declared primary documentation language if present, otherwise default to Korean/ko). I did not find an explicit "## Language Policy" section in either CLAUDE.md I have visibility into, so absent a --lang flag I would default to Korean and note that in my summary, only asking the user directly if they explicitly want to pick a language.

Step 4 (Prepare Spec Directory) — check whether docs/specification/ exists; if not, run `bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh <resolved-lang> "<ProjectName>"` to scaffold the 7-section skeleton with no LLM calls.

Step 5 (Determine Affected Sections) — for the task-range path, run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range-or-ids>` to resolve absolute task directory paths, then for each resolved task read its README.md `category` field and map it via references/section-mapping.md. For the PR-based path, run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <pr-numbers>` piped into `scripts/detect-affected-sections.sh`, and additionally run `gh pr view <num> --json number,title,body,headRefOid` for each PR to capture narrative context (the "why") and the headRefOid needed for reproducibility. I would union every detected section across both sources. If that union exceeds 4 sections, I would stop and propose `--update` (Full Refresh) to the user instead of patching piecemeal, per the explicit safety threshold.

Step 6 (Write or Update Spec Content) — write only the unioned affected section files, obeying: zero program code anywhere (including inline backticks that would parse as Prisma/SQL/ORM syntax), user-story format ("As a [user], I want [action] so that [benefit]") for features, plain-language data/flow descriptions, section size caps (400 lines default, scaling up for large projects), and recording any ambiguous reading from the task/PR diff under `## Open Questions` rather than silently resolving it myself.

Step 7 (Update README Index) — update docs/specification/README.md: set "Last updated" to today's date, and append a change-log row whose `<source>` column follows the mandated format — `tasks <range> (<n> tasks)` with every resolved task ID listed (inline or sub-bullet if >5) for the task-range path, or `PRs #<n1> @ <sha1>, #<n2> @ <sha2>` for the PR-based path.

Step 8 (Hook Setup) — skipped, since --setup-hook was not requested.

Before declaring the work complete I would run through the Validation checklist: confirm zero code leaked into any section, language matches the resolved default/flag, only the affected sections were touched, the README change log has today's date plus the `<source>` column, every resolved task ID and every PR number + headRefOid short SHA is recorded, the >4-section threshold was respected (or explicitly overridden with user confirmation), no "To be written" placeholders remain, and technical terms stayed in English rather than being transliterated. I would then report using the skill's specified Output Format templates for Task Range / Multi and for PR-based updates, listing exactly which section files were modified versus left unchanged, and confirming the README index was updated.

If the union of task-range plus PR-based changes ever touched genuinely conflicting sections (e.g., the same NFR reinterpreted two different ways by the task README versus the PR body), I would record both readings under Open Questions in the relevant section file rather than pick one, consistent with the skill's insistence that a spec writer transcribes decided intent rather than deciding it.
