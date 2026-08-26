# Dispatch artifact: ywc-spec-writer (deleted body, run 3)

**Key**: claude-code/skills/ywc-spec-writer/SKILL.md:23-23
**Scenario**: I need help with the following: creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The user's request names the two incremental-update capabilities (task-range and PR-based) in the abstract but supplies no concrete mode flag, no task ID range/pattern, no PR number(s), and no target language — and it is unclear whether docs/specification/ already exists (i.e., whether this is a first-time --full generation or an incremental --from-tasks/--from-pr update). Step 1.5 of the procedure requires estimating scope and confirming intent before writing, and the Rationalization Defense table explicitly forbids starting to write without that up-front scope check ('Intent is clear enough — start writing without an up-front scope check' is a listed excuse to reject). Given that, before touching any file I would first check whether docs/specification/ exists, then ask the user to specify: (1) which mode — full generation, full refresh, task-range update with the actual ID range/pattern, or PR-based update with the actual PR number(s); and (2) the desired output language. I would proceed with the full Step 2–8 workflow only after receiving that answer.

## Actions
- Read docs/specification/README.md if it exists to establish current spec state
- Read CLAUDE.md for language policy and domain conventions
- Read docs/ubiquitous-language.md if it exists to extract canonical vocabulary and Synonyms-to-Avoid list
- Ask user a clarifying question to pin down mode (--full/--update/--from-tasks/--from-pr/--from-prs), concrete task ID range or PR numbers, and output --lang before doing anything else
- (after clarification, task-range path) run scripts/resolve-task-paths.sh <range> to resolve task directories
- Read each resolved task's README.md for its category field and map via references/section-mapping.md, then union affected sections
- (after clarification, PR-based path) run scripts/collect-files-from-prs.sh <nums> piped into scripts/detect-affected-sections.sh
- Run gh pr view <num> --json number,title,body,headRefOid for each PR to capture narrative context and headRefOid
- Check unioned affected-section count against the >4 safety threshold; if exceeded, stop and propose --update instead of proceeding piecemeal
- If docs/specification/ does not exist, run scripts/init-spec-structure.sh <lang> "<ProjectName>" to scaffold the 7-section skeleton
- Read references/spec-structure.md, references/section-mapping.md, references/language-resolution.md, references/language-policy.md as needed for the resolved mode
- Write/update only the affected section files under docs/specification/, following the no-code / dual-audience / user-story-format / section-size-cap rules
- Grep docs/ubiquitous-language.md's Synonyms-to-Avoid column before drafting 01-overview.md to check for banned terms
- Update docs/specification/README.md: set Last updated date and append a change-log row with mode, source identifiers (task IDs or PR#s + headRefOid), and one-line summary
- Run through the Validation checklist (no code leakage, language match, only affected sections touched, source column present, all resolved task IDs / PR headRefOids recorded) before declaring done

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
- claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh
- claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh
- claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh
- claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh
- claude-code/skills/ywc-spec-writer/references/section-mapping.md
- claude-code/skills/ywc-spec-writer/references/spec-structure.md
- claude-code/skills/ywc-spec-writer/references/language-resolution.md
- claude-code/skills/ywc-spec-writer/references/language-policy.md
- claude-code/skills/ywc-spec-writer/references/full-gen-workflow.md

## Gates enforced
- Step 1.5 Scope & Intent Pre-Check (estimate affected-section count early; confirm intent on irreversible/ambiguous readings before writing)
- Step 1 Determine Mode (no flags/identifiers supplied by user, so mode cannot be safely inferred)
- Rationalization Defense: 'Intent is clear enough — start writing without an up-front scope check' is explicitly disallowed
- Rationalization Defense: 'This is a minor change — I'll update inline without reading existing spec files' — always read docs/specification/README.md and CLAUDE.md first
- Step 5 Safety threshold: >4 unioned affected sections triggers stop-and-propose --update rather than silent patching
- Step 7/Validation: headRefOid + PR numbers and every resolved task ID must be recorded in README change log
- Validation checklist: zero code, language match, only affected sections touched, dedup union file list, UL Synonyms-to-Avoid cross-check

## Full narrative

I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/.

Before writing anything, I would first establish the current state and check whether the request can actually be executed as given, because it names two incremental-update capabilities (task-range and PR-based) without giving me the concrete inputs those modes require.

**Initial reconnaissance (always done, regardless of mode):**
1. Check whether docs/specification/ already exists (e.g., `ls docs/specification/` or a Glob for `docs/specification/README.md`) — this determines whether we're in "nothing exists yet" territory (which points toward `--full`) or "spec already exists, apply an incremental update" territory.
2. Read `docs/specification/README.md` if present, to see the current spec state and change-log history.
3. Read `CLAUDE.md` for the project's language policy and domain conventions.
4. Read `docs/ubiquitous-language.md` if it exists, to pick up canonical terminology I'll need to cross-check against later.

**Why I would not proceed straight to writing:** The request mentions "task-range and PR-based incremental updates" as things the user wants supported, but gives no explicit `--from-tasks <range>` value, no `--from-pr`/`--from-prs` number(s), no `--full`/`--update` flag, and no `--lang`. Step 1.5 (Scope & Intent Pre-Check) requires estimating the affected-section count and confirming intent before writing — and the Rationalization Defense table explicitly calls out "Intent is clear enough — start writing without an up-front scope check" as an excuse to reject. Guessing a task ID range or PR number here would risk writing against the wrong diff entirely, and guessing between `--full` and an incremental mode risks either needlessly regenerating a working spec or silently under-covering a new project.

So at this point I would ask the user directly:

"Could you clarify which spec-update mode you'd like me to run:
1. Full generation (`--full`) — if docs/specification/ doesn't exist yet, generate the complete 7-section spec from scratch. This requires your explicit confirmation and uses the best available model.
2. Full refresh (`--update`) — regenerate all existing sections of an already-present spec.
3. Task-range update (`--from-tasks <id-or-pattern>`) — please give me the actual task ID range or pattern (e.g., `000002-010..000003-020`).
4. PR-based update (`--from-pr <num>` / `--from-prs <num> ...`) — please give me the actual PR number(s).
Also, which output language should the spec use — Korean (default), English, Japanese, Chinese, or Spanish?"

**Once that clarification is received, here is exactly what I would do for each concrete branch:**

*If a task range is given (e.g., `--from-tasks 000002-010..000003-020`):*
- Run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh 000002-010..000003-020` to resolve the range/glob/multi-id into absolute task directory paths.
- For each resolved task directory, read its `README.md` to extract the `category` field, then look up the corresponding spec sections in `references/section-mapping.md`, and union every resulting section across all resolved tasks.
- If the unioned section count exceeds 4, stop and propose `--update` (Full Refresh) instead of patching piecemeal, per the Step 5 safety threshold.

*If PR numbers are given (e.g., `--from-prs 42 43 51`):*
- Run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh 42 43 51 | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh` to get the unioned, deduplicated affected-section list from the changed-file union across PRs.
- Run `gh pr view <num> --json number,title,body,headRefOid` for each PR number to capture the narrative context (title/body, for the "why") and the `headRefOid` short SHA, which must be recorded in the README change-log row for reproducibility.

*Common downstream steps once affected sections are determined:*
- If `docs/specification/` doesn't exist yet, run `bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh <resolved-lang> "<ProjectName>"` to scaffold the 7-section skeleton (no LLM calls).
- Read `references/spec-structure.md` for per-section writing templates, and `references/section-mapping.md` for section boundaries.
- Write only the affected section files (e.g., `02-features.md`, `03-data.md`) under `docs/specification/`, strictly following: zero program code (including inline-backtick ORM/SQL syntax like `@default(...)`, `dbgenerated(...)`, `WHERE ... = $1` — these get paraphrased to plain prose), user-story format for features, dual-audience readability, and the section-size caps (≤400 lines default, ≤800 for large projects, with the `03-data.md` per-entity extension formula for >50 entities).
- Before drafting `01-overview.md`, grep `docs/ubiquitous-language.md`'s Synonyms-to-Avoid column and make sure no banned synonym is introduced anywhere in the new/updated text; replace with canonical terms or log a proposal under `## Open Questions`.
- Where the source diff/task/PR admits two readings on an irreversible design point (data ownership, sync/async boundary, API versioning, etc.), record both readings under `## Open Questions` rather than silently picking one.
- Update `docs/specification/README.md`: set `**Last updated**` to today's date, and append a change-log row with the `<source>` column populated per the Step 7 table (e.g., `tasks 000002-010..000003-020 (3 tasks)` listing every resolved task ID, or `PRs #42, #43, #51 @ <headRefOid-short each>`).
- Only run the hook-installation procedure in `references/hook-setup.md` if the user explicitly asked for `--setup-hook`.

**Final verification before declaring done**, per the skill's Validation checklist:
- Confirm zero program code slipped into any section (including inline-backtick checks).
- Confirm the output language matches what was resolved/confirmed.
- Confirm only the affected sections were touched, not unrelated ones.
- Confirm the README change log has today's date and the correct `<source>` provenance.
- Confirm every resolved task ID (for task-range) or every PR number + headRefOid (for PR-based) is recorded.
- Confirm no "To be written" placeholders remain in touched sections.
- Confirm technical terms were kept in English per language policy rather than transliterated.

Given all of this, my actual first move on receiving the user's message as stated — with no mode flag, no task range, no PR numbers, and no language specified — would be to ask the clarifying question above rather than guess at any of those four missing inputs, since guessing wrong on mode or identifiers would mean writing spec content against the wrong source material entirely.
