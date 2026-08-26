# Dispatch artifact: ywc-spec-writer (original body, run 3)

**Key**: claude-code/skills/ywc-spec-writer/SKILL.md:23-23
**Scenario**: I need help with the following: creating or updating a project specification (사양서) in docs/specification/, including task-range and PR-based incremental updates.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The user's request names the skill's two incremental modes (task-range and PR-based) in general terms but supplies no concrete mode selector or identifiers — no --from-tasks range, no --from-pr/--from-prs numbers, and no explicit --full/--update flag, and it's also unclear whether docs/specification/ already exists in this project. Per Step 1 (Determine Mode) and Step 1.5 (Scope & Intent Pre-Check), and the explicit Rationalization Defense entry against starting to write without an up-front scope check, the procedure requires treating this as undecided intent rather than guessing a mode or fabricating a task range/PR list. The correct move is read-only recon to inform the question, then ask the user to specify the mode and concrete identifiers before any spec content is written.

## Actions
- Announce skill start: "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."
- Run read-only recon: `ls docs/specification/ 2>/dev/null` and `test -f docs/specification/README.md` to check if a spec already exists
- Read docs/specification/README.md (if present) to see current section state, last-updated date, and prior change-log entries
- Read CLAUDE.md at repo root (already available) and scan for a canonical '## Language Policy' section per the language-resolution precedence chain
- Run `ls docs/ubiquitous-language.md 2>/dev/null` to check whether a canonical vocabulary doc exists that would need to be cross-checked before writing
- Run `ls tasks/ 2>/dev/null` to confirm whether resolvable task directories exist for a --from-tasks range
- Run `gh auth status` to confirm the gh CLI is authenticated, since --from-pr/--from-prs depend on it
- Ask the user a clarifying question specifying: which mode (--full / --update / --from-tasks <range> / --from-pr(s) <num...>), the concrete task ID range or PR number(s) if incremental, and language override if not default ko
- Withhold any write/generation step (init-spec-structure.sh, section writing, README index update) until the user supplies the missing mode and identifiers
- (Contingent, once mode is given) For task-range: run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <range>`, read each resolved task's README.md category field, map via references/section-mapping.md, union sections
- (Contingent) For PR-based: run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <nums> | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh` and `gh pr view <num> --json number,title,body,headRefOid` for each PR for narrative context and headRefOid capture
- (Contingent) Apply Step 5 safety threshold: if unioned affected sections > 4, stop and propose --update (Full Refresh) instead of patching piecemeal
- (Contingent) Write only the affected section files under docs/specification/ following Step 6 rules: zero code, dual-audience prose, user-story format for features, file size caps, Open Questions for ambiguous readings, UL cross-check against docs/ubiquitous-language.md Synonyms-to-Avoid if that file exists
- (Contingent) Update docs/specification/README.md: set Last updated to today's date and append a change-log row with section(s), source (task IDs or PR#s + headRefOid), and one-line summary
- (Contingent) Run the Validation checklist (no code leaked, language matches resolved default, only affected sections touched, source/headRefOid recorded, no placeholder content) before declaring completion

## Files touched
- claude-code/skills/ywc-spec-writer/SKILL.md (read only)
- docs/specification/README.md (read; would edit only after clarification)
- CLAUDE.md (read for language policy)
- docs/ubiquitous-language.md (read, if present)
- tasks/*/README.md (read, contingent on task-range branch)
- docs/specification/0X-*.md (would edit, contingent on clarification)

## Gates enforced
- Step 1 Determine Mode — no explicit --full/--update/--from-tasks/--from-pr(s) flag or identifiers present in the request
- Step 1.5 Scope & Intent Pre-Check — ambiguous/irreversible mode choice must be surfaced as a clarifying question or recorded under Open Questions, never silently decided
- Rationalization Defense: 'Intent is clear enough — start writing without an up-front scope check' — explicitly rejected
- Arguments table: --from-tasks and --from-pr/--from-prs require concrete identifiers not supplied by the user
- Arguments table: --full requires explicit flag AND user confirmation before any full generation
- Step 5 safety threshold (>4 affected sections triggers propose --update) — deferred pending mode selection
- Step 2 mandatory context reads (README.md, CLAUDE.md, ubiquitous-language.md) before any writing

## Full narrative

I would begin by posting the mandatory announcement: "I'm using the ywc-spec-writer skill to create or update the project specification in docs/specification/."

Before deciding how to proceed, I'd note that the request doesn't actually pin down a mode. The skill's Step 1 table requires one of: --full, --update, --from-task, --from-tasks <range>, --from-commit, --from-pr(s) <nums>, or Auto (last-commit diff). The user's phrasing — "creating or updating... including task-range and PR-based incremental updates" — describes the skill's capabilities rather than committing to one of them, and gives no concrete task IDs or PR numbers. Per Step 1.5 (Scope & Intent Pre-Check) and the Rationalization Defense row "Intent is clear enough — I'll start writing without an up-front scope check," I would not silently default to Auto mode or invent a range/PR list; the spec writer transcribes decided intent, it does not decide it.

So my first concrete actions would be read-only reconnaissance to make the follow-up question well-informed, not to start writing:

1. `ls docs/specification/ 2>/dev/null` and `test -f docs/specification/README.md` — determine whether a spec already exists (this determines whether --full is even on the table, versus an incremental mode).
2. If it exists, Read `docs/specification/README.md` — the mandatory Step 2 context read, to see the current section state, last-updated date, and change-log history.
3. Re-check `CLAUDE.md` at the repo root (already loaded) for a canonical `## Language Policy` section per the language-resolution precedence chain (--lang flag → project CLAUDE.md → user CLAUDE.md → skill fallback ko). None is present under that exact heading, so the default would remain Korean (ko) unless the user overrides it — I would not need to interrupt the user separately for this unless they raise it, per Step 3's "ask only when the user explicitly asks or guidance conflicts."
4. `ls docs/ubiquitous-language.md 2>/dev/null` — Step 2's conditional read; if present, its Synonyms-to-Avoid column would need to be cross-checked against any new terms introduced during writing.
5. `ls tasks/ 2>/dev/null` — confirm whether resolvable task directories exist at all, since a task-range update depends on `scripts/resolve-task-paths.sh` finding real directories.
6. `gh auth status` — confirm the `gh` CLI is authenticated, since --from-pr/--from-prs are listed as depending on it (external dependency in the Integration section).

With that context gathered, I would ask the user a clarifying question rather than proceed, along the lines of: "To update the spec, could you confirm: (a) should this run from a task ID range (e.g. `--from-tasks 000002-010..000003-020`) or from specific PR number(s) (e.g. `--from-pr 42` or `--from-prs 42 43 51`), or is this a first-time full generation (`--full`) / full refresh (`--update`) instead? (b) If task-range or PR-based, which specific IDs/PRs? (c) Any language override, or should I keep the default Korean (ko)?" I would report what the recon found (spec exists or not, task/PR availability, gh auth state) alongside the question so the user isn't guessing blind either.

I would not proceed past this point in the current turn — no `init-spec-structure.sh`, no section writing, no README index update — because doing so would mean either fabricating task/PR identifiers (forbidden) or silently choosing Auto/--full on the user's behalf on an irreversible-ish choice (also forbidden by Step 1.5).

Once the user answers, the downstream execution would branch concretely:

- **Task-range branch**: run `bash claude-code/skills/ywc-spec-writer/scripts/resolve-task-paths.sh <id-or-pattern>` to resolve the range/glob to absolute task directory paths, Read each resolved task's `README.md` for its `category` field, map each to affected sections via `references/section-mapping.md`, and union the results.
- **PR-based branch**: run `bash claude-code/skills/ywc-spec-writer/scripts/collect-files-from-prs.sh <nums...> | bash claude-code/skills/ywc-spec-writer/scripts/detect-affected-sections.sh` for the changed-file union, plus `gh pr view <num> --json number,title,body,headRefOid` per PR to capture narrative context (title/body inform the "why") and the `headRefOid` short SHA for reproducibility in the change log.
- Either way, apply the Step 5 safety threshold: if the unioned affected-section count exceeds 4, stop and propose `--update` (Full Refresh) instead of patching piecemeal, per both Step 5 and the matching Rationalization Defense row.
- Write only the affected section files under `docs/specification/`, following Step 6's non-negotiable rules: zero program code (including inline-backtick ORM/SQL syntax — only paraphrase, field-reference identifiers like `tenantId` are fine), user-story format for features, dual-audience prose with concrete numbers (not vague placeholders), the file-size caps (≤400 lines default, scaled up for large projects), and recording any ambiguous reading under `## Open Questions` rather than resolving it myself. If `docs/ubiquitous-language.md` exists, cross-check any newly introduced role/entity/concept names against its Synonyms-to-Avoid column before finalizing.
- Update `docs/specification/README.md`: set `**Last updated**` to today's date and append a change-log row with the affected section(s), the `<source>` (task IDs list or PR numbers + headRefOid), and a one-line summary, following the exact table format in Step 7.
- Run the Step 8 hook installation only if the user also asked for `--setup-hook`.
- Before declaring completion, run through the Validation checklist: no code leaked into any section, language matches the resolved default/override, only the affected sections were touched, the README change log includes today's date and the source column, every resolved task ID or every PR number + headRefOid is recorded, no "To be written" placeholders remain, and technical terms stayed in English per the language policy.

Given the actual request as received, though, the concrete next step is the clarifying question above — not spec generation.
