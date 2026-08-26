# Dispatch artifact: ywc-spec-writer (deleted body, run 1)

**Key**: claude-code/skills/ywc-spec-writer/SKILL.md:23-23
**Scenario**: I need help with the following: creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The request names both task-range and PR-based incremental update mechanisms (and 'creating or updating', which implicates --full) but supplies none of the concrete parameters the procedure requires before writing: no explicit --full confirmation, no --from-tasks id-or-pattern, and no --from-pr/--from-prs number(s). Per Step 1.5 (Scope & Intent Pre-Check) and the Rationalization Defense table, the spec writer must never silently pick a mode/flag or default straight to full generation — it transcribes decided intent, it does not decide it. So after doing the deterministic context-collection and language-resolution work, I would pause and ask the user to specify which concrete mode applies right now (full generation with confirmation, a specific task ID range/pattern, and/or specific PR number(s), plus whether --setup-hook should also be installed) before running any detection or write steps.

## Actions
- Announce skill start: "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."
- Bash: test -f docs/specification/README.md (check if a spec already exists) and Read docs/specification/README.md if present, to see current section state and prior change-log entries before writing anything
- Read CLAUDE.md at repo root to confirm language policy and domain conventions
- Bash: test -f docs/ubiquitous-language.md; Read it if present to extract canonical terms and the 'Synonyms to Avoid' column
- Resolve output language per Step 3 precedence: no --lang flag given, no '## Language Policy' header in project CLAUDE.md, but project CLAUDE.md declares 'Documentation: Korean' under Language Conventions -> honor that as the terminal fallback and resolve language = ko without prompting the user
- Determine mode per Step 1: user's request names both 'task-range' and 'PR-based' incremental updates plus 'creating or updating' but supplies no --from-tasks <range>, no --from-prs <numbers>, and no explicit --full/--update flag
- Apply Step 1.5 Scope & Intent Pre-Check: since no concrete task ID range, PR numbers, or explicit --full confirmation were given, treat this as an irreversible-choice ambiguity and stop before writing
- Ask the user a clarifying question distinguishing: (a) initial full generation via --full (requires explicit confirmation) if docs/specification/ does not yet exist, (b) --from-tasks <id-or-pattern> with the exact range/glob/ID list to update from, (c) --from-pr/--from-prs <num...> with the exact PR number(s), and (d) whether --setup-hook should also be installed for ongoing automatic tracking
- Bash: test -d docs/specification (only decision-relevant check performed before pausing; directory creation via init-spec-structure.sh deferred until mode is confirmed)
- (Deferred until user answers) For Task Range mode: run bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range>, then Read each resolved task's README.md for its category field and map via references/section-mapping.md, then union the resulting sections
- (Deferred until user answers) For PR-based mode: run bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <nums> | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh, and run gh pr view <num> --json number,title,body,headRefOid for each PR to capture narrative context and headRefOid
- (Deferred) If unioned affected sections exceed 4, stop and propose --update (Full Refresh) to the user instead of patching piecemeal
- (Deferred) Write/update only the affected section files under docs/specification/, enforcing zero-code, dual-audience, and Open-Questions rules from Step 6
- (Deferred) Update docs/specification/README.md: set Last updated to today's date and append a change-log row with the <source> column (task IDs listed inline/sub-bullet, or PR numbers with headRefOid short SHA)
- (Deferred) Run the Step 254-278 validation checklist (no code leakage, language match, only affected sections touched, source column present, all resolved task IDs / PR SHAs recorded, no placeholder NFRs, UL cross-check, no ORM/SQL syntax leak) before declaring the task complete

## Files touched
- docs/specification/README.md
- CLAUDE.md
- docs/ubiquitous-language.md
- docs/specification/01-overview.md
- docs/specification/02-features.md
- docs/specification/03-data.md
- docs/specification/04-interfaces.md
- docs/specification/05-user-flows.md
- docs/specification/06-requirements.md
- docs/specification/07-glossary.md
- claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh
- claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh
- claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh
- claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh

## Gates enforced
- Step 1.5 Scope & Intent Pre-Check (surface ambiguity before writing, never silently pick a mode)
- Full generation requires explicit --full flag AND user confirmation (Rationalization Defense row 2)
- Safety threshold: unioned affected sections > 4 -> stop and propose --update instead of patching piecemeal
- Zero program code in any spec output, including inline-backtick ORM/SQL syntax
- Dual-audience writing rule (business-readable + task-generator-decomposable)
- Open Questions rule: ambiguous/undecided source readings recorded, never silently resolved
- README index change-log update with mandatory <source> provenance column
- PR headRefOid capture requirement for reproducibility
- Task Range: every resolved task ID enumerated in the change log
- Ubiquitous Language Synonyms-to-Avoid cross-check (when docs/ubiquitous-language.md exists)
- Full/Update-mode NFR quantitative-target requirement (no vague placeholders)
- Full/Update-mode schema-to-03-data.md model enumeration completeness check
- Pre-completion validation checklist (Step 254-278) including language match and no leftover placeholders
- Pipeline alignment gate: spec expected to clear ywc-spec-validate at Gate >= 70 (>= 90 for --full)

## Full narrative

Here is exactly how I would proceed under the ywc-spec-writer procedure for this request.

First, I would announce the skill per its required opening line: "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."

**Context collection (Step 2, always performed before anything else):**
- `Bash: test -f docs/specification/README.md` to check whether a spec already exists, and if so, `Read docs/specification/README.md` to see the current section index and prior change-log entries — writing without reading first risks silently overwriting valid content.
- `Read CLAUDE.md` at the repo root — already available in context, and it establishes the project's Language Conventions: "Documentation: Korean."
- `Bash: test -f docs/ubiquitous-language.md`, and `Read` it if present, to pull canonical terminology and the "Synonyms to Avoid" column for later cross-checking.

**Language resolution (Step 3):** No `--lang` flag was given. The project CLAUDE.md has no literal `## Language Policy` header, but it does declare a primary documentation language ("Documentation: Korean") under Language Conventions. Per the skill's terminal fallback rule, that satisfies "honor a project CLAUDE.md's declared primary documentation language if present" — so I would resolve the output language to Korean (`ko`) without prompting the user, since there's no conflict and the user hasn't asked to choose a language.

**Mode determination (Step 1) and the point where I would stop and ask:** The request says "creating or updating... including task-range and PR-based incremental updates." That phrase spans at least three distinct modes in the skill's mode table — Full Generation (`--full`), Task Range Update (`--from-tasks <id-or-pattern>`), and PR-based Update (`--from-pr`/`--from-prs <num...>`) — but supplies none of the concrete arguments each mode requires: no task ID range or glob, no PR number(s), and no explicit `--full` confirmation. The Rationalization Defense table is explicit that "User seems to want a full spec — I'll generate it without `--full` to save time" is not acceptable, and Step 1.5 requires surfacing ambiguity on any choice that changes the spec's meaning rather than silently picking one. Guessing a task range or PR numbers here would be exactly that kind of silent pick.

So at this point I would ask the user a concrete clarifying question rather than proceed:
"To scope this correctly, could you confirm: (1) does `docs/specification/` already exist, or is this the first write (which would need an explicit `--full` confirmation)? (2) If updating from tasks, what is the exact task ID range or pattern (e.g., `000002-010..000003-020`)? (3) If updating from PR(s), what are the exact PR number(s) (e.g., `42 43 51`)? (4) Would you also like `--setup-hook` installed so future commits automatically flag spec-update-pending work?"

**What I would do once each answer arrives (narrated for completeness):**
- *Directory prep (Step 4)*, only if `docs/specification/` doesn't exist: `Bash: bash claude-code/skills/ywc-spec-writer/scripts/init-spec-structure.sh ko "<ProjectName>"`, passing the resolved `ko` language code so the skeleton itself is scaffolded in Korean.
- *Task Range mode (Step 5)*: `Bash: bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range>` to expand the range/glob/ID-list into absolute task directory paths, then `Read` each resolved task's `README.md` to pull its `category` field, map each to affected sections via `references/section-mapping.md`, and union the results across all resolved tasks.
- *PR-based mode (Step 5)*: `Bash: bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <nums> | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh` to get the deduped affected-section list from the union of changed files, plus `Bash: gh pr view <num> --json number,title,body,headRefOid` for each PR number to capture the "why" narrative and the `headRefOid` needed for reproducibility in the change log.
- *Safety gate*: if the unioned affected-section count from either path exceeds 4, I would stop short of writing and instead propose switching to `--update` (Full Refresh), per the explicit safety threshold — patching that many sections piecemeal risks internal drift.
- *Writing (Step 6)*: only touch the affected section files under `docs/specification/`, enforcing zero program code (including inline-backtick ORM/SQL fragments), the user-story format for features, plain-language data/flow descriptions, the per-section line cap, and recording any two-reading ambiguity from the source task/PR under `## Open Questions` rather than resolving it myself. If Full/Update mode is confirmed, I'd additionally enforce: quantitative NFR targets (no "몇 초 이내" placeholders), full by-name model enumeration in `03-data.md`, a Role × Action matrix if ≥3 actor roles exist, a Data Lifecycle subsection if long-lived high-volume data exists, and the Ubiquitous Language avoid-list cross-check before drafting `01-overview.md`.
- *README index update (Step 7)*: update `docs/specification/README.md`'s "Last updated" date and append a change-log row with the `<source>` column populated correctly — e.g., `tasks 000002-010..000003-020 (3 tasks)` with every resolved ID listed, or `PRs #42 @ a1b2c3d, #43 @ e4f5g6h`.
- *Hook setup (Step 8)*, only if the user confirms wanting it: follow `references/hook-setup.md` to install the actual working script at `tools/scripts/spec-update-hook.sh` — documentation of the approach alone would not satisfy this step.
- *Final validation*: before declaring the work complete, I would walk the full Step 254-278 checklist — zero code leakage, correct language, only-affected-sections-touched, source column present, every task ID / PR SHA recorded, no leftover "To be written" placeholders, and (for Full/Update) the NFR, schema-enumeration, UL cross-check, and ORM/SQL-leak checks — with the expectation that the result should clear `ywc-spec-validate` at Gate ≥ 70 (or ≥ 90 for `--full`).

In short: I would not refuse the request outright, and I would not silently default to any one mode — I would do the deterministic context-collection and language-resolution work up front, then pause and ask the user for the specific task range and/or PR numbers (and full-generation confirmation, if applicable) before running any detection scripts or writing to `docs/specification/`, because the procedure treats guessing those parameters as exactly the kind of silent, irreversible decision a spec writer is not permitted to make on the user's behalf.
