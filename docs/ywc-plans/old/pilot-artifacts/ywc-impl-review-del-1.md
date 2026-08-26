# Dispatch artifact: ywc-impl-review (deleted body, run 1)

**Key**: claude-code/skills/ywc-impl-review/SKILL.md:21-21
**Scenario**: I need help with the following: implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a refusal — an escalation/clarifying-question gate: the skill's Arguments table marks --spec and --code (or --git-range) as required, and the user's request supplies neither a spec file path nor a code path/git range. Per the skill's own Completion Status rules (BLOCKED when the spec file is missing/unreadable, NEEDS_CONTEXT when spec and code paths are ambiguous), I would first run lightweight git inspection to propose candidate scope, then confirm the exact --spec path and --code/--git-range with the user before spawning the five Phase 1 subagents, rather than guessing at a required parameter.

## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-impl-review-21-21.md (done)
- Announce skill use verbatim per SKILL.md line 9
- Run `git rev-parse --abbrev-ref HEAD`, `git merge-base main HEAD`, `git diff main...HEAD --name-only`, `git log main..HEAD --oneline` to establish candidate review scope
- Search for a candidate --spec file (e.g. `find docs/ywc-plans -iname '*skill-hell*'`, check tasks/ for the originating task spec) since --spec and --code/--git-range are required and not supplied by the user
- Ask user to confirm/provide --spec path and --code path (or confirm git-range main...HEAD) before proceeding, since Completion Status rules mark BLOCKED/NEEDS_CONTEXT on missing or ambiguous spec/code scope
- Step 0: invoke ywc-review-learnings --mode read --target <changed files>, Read docs/review-learnings.md if present, else proceed with empty learnings set
- Step 1: Read root CLAUDE.md and ywc-agent-toolkit/CLAUDE.md, check for package.json, Read docs/ubiquitous-language.md if present, trace changed symbols to callers/callees
- Step 2: Read the confirmed spec file and all target code files in full (parent context only, not forwarded wholesale to Phase 2)
- Step 3: Spawn 5 parallel Task-tool subagents with explicit model params — Architecture (sonnet, references/architecture-agent.md), Design (sonnet, references/design-agent.md), Devex (sonnet, references/devex-agent.md), Security (sonnet, references/security-agent.md; check tools/claude-code/agents/ywc-security-engineer.md and prefer that subagent_type if present), QA (haiku, references/qa-agent.md)
- Check tools/claude-code/agents/ for ywc-typescript-reviewer.md / ywc-python-reviewer.md / ywc-go-reviewer.md to decide Tier-2 language-specific Design/Devex replacement based on dominant changed-file language
- Run available linters/scanners (shellcheck on scripts/, markdownlint, repo's own scripts/validate.sh) and feed output to relevant subagents as evidence, not verdict
- Apply --profile chill default (suppress Low/Info nitpick tail), inject Step 0 learnings per category, enforce verify-before-surface (drop unverified findings), apply surgical-changes out-of-scope check
- Step 4: Aggregate Phase 1 advisor candidates, dedupe by file:line, cap at advisor-budget=5, prioritize Critical>High>Medium and Security>Architecture>Design>Devex>QA, log dropped candidates
- Step 5 (unless --no-advisor): spawn sequential Task-tool Opus subagents per surviving candidate, routing Architecture candidates to ywc-architect and performance-ambiguous candidates to ywc-performance-engineer if those agent files exist under tools/claude-code/agents/, else generic model: opus; pass only finding text, bounded snippet, spec excerpt, severity rubric
- Step 6: Merge Phase 1 + Phase 2 results into final report marking [P1]/[P2] provenance per finding
- Apply Confidence Gate (Evidence quality, Root cause identified, each >=70) before emitting; map gate band to Completion Status (PROCEED->DONE/DONE_WITH_CONCERNS, REVIEW->NEEDS_CONTEXT, STOP->BLOCKED)
- If DONE/DONE_WITH_CONCERNS under PROCEED, attach ywc-verify-done evidence block (command, output excerpt, exit code) before the status line, avoiding hedge language
- Emit markdown report using the fixed Output Format template with severity symbols from references/symbols.md
- Step 7 (unless --skip-learnings): offer to promote recurring confirmed findings and user-dismissed false positives into docs/review-learnings.md via ywc-review-learnings --mode update --source review, gated on user-confirmed CHANGESET
- Do not create the PR myself in this invocation — hand off the report; PR creation is explicitly the downstream skill (ywc-create-pr), invoked separately only after Critical/High items are addressed or the user accepts DONE_WITH_CONCERNS

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-impl-review-21-21.md (read only, per task instructions)

## Gates enforced
- Required-arguments gate: --spec and --code/--git-range are mandatory; ambiguous/missing scope triggers a clarifying question rather than guessing
- Advisor budget cap (default 5 Opus calls, dedup + priority ordering)
- Verify-before-surface: every finding needs file:line or command-output evidence or it is dropped, not hedged
- --profile chill default suppresses Low/Info nitpick tail; Critical/High/Medium never suppressed
- FALSE-POSITIVE learnings from docs/review-learnings.md suppress recurring known non-issues
- Confidence Gate (Evidence quality >=70, Root cause identified >=70) gates report emission and Completion Status mapping
- ywc-verify-done evidence-block requirement before any DONE/DONE_WITH_CONCERNS claim under PROCEED band
- Surgical-changes check: flags any diff hunk not traceable to the spec/PR intent as out-of-scope
- Learnings capture (Step 7) requires explicit user-confirmed CHANGESET before writing to docs/review-learnings.md

## Full narrative

I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review.

Before spawning any reviewers, I need two required inputs the skill's Arguments table mandates: `--spec` (the specification file) and either `--code` (a path) or `--git-range` (mutually exclusive with `--code`). The request as given doesn't specify either, so my first concrete actions are scope-discovery, not review execution:

1. `git rev-parse --abbrev-ref HEAD` and `git status` — confirm the working branch and that the tree is clean.
2. `git merge-base main HEAD`, then `git diff main...HEAD --name-only` and `git log main..HEAD --oneline` — build a candidate changed-file list and commit summary to propose as the `--git-range` target.
3. Search for a candidate spec: `find docs/ywc-plans -iname "*<branch-keyword>*"` and check whether a `tasks/` directory exists with a spec doc for the task that produced this branch, since this repo's recent commits ("mark 000057-010... as completed", "mark 000056-010... as completed") indicate a `ywc-task-generator` / `ywc-sequential-executor` task workflow with per-task spec docs.
4. Present the candidates and ask the user to confirm: "Should I review `main...HEAD` (files: …) against `<candidate spec path>`, or do you want to point `--spec`/`--code` elsewhere?" I would not guess on this — a wrong spec target produces a review that looks authoritative but validates against the wrong contract, and the skill's own Completion Status table treats an unresolved spec/code path as `NEEDS_CONTEXT`, not something to paper over.

Once the user confirms `--spec <path>` and either `--code <path>` or `--git-range <range>`, I'd execute the skill's fixed procedure exactly:

**Step 0 (learnings):** Invoke `ywc-review-learnings --mode read --target <changed files>`, which reads `docs/review-learnings.md`. If that file doesn't exist, proceed with an empty learnings set rather than blocking.

**Step 1 (context):** Read the root `CLAUDE.md` and this repo's `ywc-agent-toolkit/CLAUDE.md`, check for `package.json` (unlikely to be load-bearing here since this is a skill-distribution toolkit, not a JS app), and Read `docs/ubiquitous-language.md` if present so reviewers can flag non-canonical identifiers. I'd trace each changed symbol to its callers/callees rather than judging files in isolation.

**Step 2 (read targets):** If `--git-range` was used, run `git diff --name-only <range>` again to lock the file list, then Read the confirmed spec file and every target code file in full. This stays in my context only — none of it is forwarded wholesale to Phase 2.

**Step 3 (Phase 1, five parallel Task-tool subagents, model set explicitly per call):**
- Architecture (`model: sonnet`, prompt built from `claude-code/skills/ywc-impl-review/references/architecture-agent.md`) — module boundaries, layering, structural spec conformance; if the diff touches DB schema/migrations, also apply `references/schema/core.md` Part C and cross-reference cascade/tenant-scope gaps to Security instead of duplicating.
- Design (`model: sonnet`, `references/design-agent.md`) — API/interface design, naming, error models, contract conformance.
- Devex (`model: sonnet`, `references/devex-agent.md`) — readability, error messages, logging, config UX.
- Security (`model: sonnet`, `references/security-agent.md`) — OWASP Top 10; I'd check whether `tools/claude-code/agents/ywc-security-engineer.md` exists in this repo and if so dispatch with `subagent_type: ywc-security-engineer` instead of the generic prompt.
- QA (`model: haiku`, `references/qa-agent.md`) — coverage gaps, missing test cases.

Before dispatch, I'd check `tools/claude-code/agents/` for `ywc-typescript-reviewer.md`, `ywc-python-reviewer.md`, or `ywc-go-reviewer.md` to see if the changed-file set is dominated by one of those languages, in which case Design/Devex get replaced by the matching Tier-2 reviewer for sharper findings; otherwise the generic Sonnet prompts stand.

Into every subagent prompt I'd inject the Step 0 learnings filtered to that category (`DO`/`DO-NOT` become extra checks, `FALSE-POSITIVE` entries suppress known non-issues), apply `--profile chill` by default (suppress the Low/Info Style/Docs nitpick tail, never suppress Critical/High/Medium), and enforce verify-before-surface: any finding lacking `file:line` evidence, a traced symbol, or fresh command output gets dropped rather than hedged. I'd run whatever linters/scanners this repo ships — `shellcheck` on `scripts/`, `markdownlint` on touched `README*.md`, and the repo's own `bash scripts/validate.sh` — and feed that output to the relevant subagent as evidence to triage, not as the verdict. I'd also apply the surgical-changes check: any hunk that doesn't trace to the spec or the stated PR intent (drive-by formatting, unrelated refactors) gets flagged as out-of-scope.

Each subagent returns confirmed findings plus advisor candidates (finding text, ≤100-line snippet, spec excerpt, one-sentence escalation reason).

**Step 4 (aggregate):** Dedupe candidates sharing `{file}:{line}`, cap at the default advisor budget of 5, prioritizing Critical > High > Medium and, within a tier, Security > Architecture > Design > Devex > QA. Anything cut for budget gets logged in the final report's Advisor Budget Report section.

**Step 5 (Phase 2, unless `--no-advisor`):** For each surviving candidate, spawn a sequential Task-tool subagent with `model: opus`. Architecture candidates route to `subagent_type: ywc-architect` if `tools/claude-code/agents/ywc-architect.md` exists; performance-ambiguous Architecture/Devex candidates route to `ywc-performance-engineer` under the same condition; everything else uses the generic Opus dispatch. Payload is strictly the candidate's finding text, bounded snippet, spec excerpt, and the category's severity rubric — never the full spec, full file, or Phase 1 transcripts. Expected output is ≤200 words: confirmed severity, one-line rationale, confirmed/adjusted verdict (exceeding the cap only with an explicit justification logged in the report).

**Step 6 (merge/report):** Combine Phase 1 confirmed findings with Phase 2 verdicts, tagging each with `[P1]`/`[P2]` provenance.

Before emitting, I'd apply the Confidence Gate — Evidence quality and Root cause identified must each score ≥70 — and map the band to Completion Status: PROCEED → DONE or DONE_WITH_CONCERNS (per the existing Critical/High count rule), REVIEW (70–89) → NEEDS_CONTEXT with the gate score and weakest dimension flagged at the top, STOP (<70) → BLOCKED, reporting which dimensions failed instead of presenting findings as authoritative. If the band lands PROCEED and I'm claiming DONE/DONE_WITH_CONCERNS, I'd attach a `ywc-verify-done`-style evidence block (command run, output excerpt, exit code) before the status line and avoid "should"/"probably"/"seems" language in the conclusion — an "all clear, looks good" report without that evidence block gets downgraded to REVIEW rather than emitted as PROCEED.

The report itself follows the fixed template: Summary (per-axis finding counts, Phase 2 usage), then Architecture / Design / Devex / Security / Testing sections each with `[severity-symbol] [P1|P2] file:line — description` lines (using 🚨🔴🟡🔵ℹ️ from `references/symbols.md`, plus the advisor verdict line where applicable), a Fix Priority list sorted Critical-first, the Advisor Budget Report, and the Completion Status line.

**Step 7 (unless `--skip-learnings`):** After the report, I'd offer — not silently perform — promotion of durable lessons into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`: recurring confirmed-finding classes become `DO`/`DO-NOT` entries, and anything the user dismisses as a false positive becomes a `FALSE-POSITIVE` entry with the stated dismissal reason. This only happens through that skill's user-confirmed CHANGESET step, not by me editing the file directly.

What I would explicitly not do: I would not create the pull request as part of this invocation. `ywc-impl-review`'s own Integration section names PR creation as the downstream consumer, not something this skill performs — so once the report is delivered, the next action (invoking `ywc-create-pr`) would only happen on a separate user instruction, and only after any Critical/High findings are addressed or the user knowingly accepts a `DONE_WITH_CONCERNS` status.
