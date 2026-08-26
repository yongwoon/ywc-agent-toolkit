# Dispatch artifact: ywc-impl-review (original body, run 2)

**Key**: claude-code/skills/ywc-impl-review/SKILL.md:21-21
**Scenario**: I need help with the following: implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The skill's Arguments table marks --spec and --code (or the mutually exclusive --git-range) as required, and Execution Step 2 depends on having both a specification file to read and a concrete code target. The user's request states only the general trigger condition (\"implementation is complete, before PR, validate against spec\") without naming which spec document or which code path/git range to review. Rather than guessing a spec file or silently defaulting the diff range, I would ask a short clarifying question first — e.g. \"Which specification file should this be checked against, and should I review a specific --code path or derive the diff via --git-range (e.g. main...HEAD)?\" — before running the five-axis Phase 1 dispatch, since running reviewers against the wrong or an inferred-incorrect target would produce a misleading conformance report.

## Actions
- Read claude-code/skills/ywc-impl-review/SKILL.md (already done)
- Announce: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."
- Ask clarifying question: which spec file (--spec) and which code path or --git-range should be reviewed, since both are required arguments with no documented default
- Bash: git branch --show-current; git status; identify base branch (main) and current feature branch
- Bash: git diff --name-only main...HEAD (if --git-range chosen instead of --code)
- Skill: invoke ywc-review-learnings --mode read --target <changed files> to load docs/review-learnings.md (skip if --skip-learnings)
- Read CLAUDE.md and package.json (or repo-equivalent manifest) for conventions/tech stack/PR gate conditions
- Read docs/ubiquitous-language.md if present
- Read the specification file and all target code files
- Read reference files: references/architecture-agent.md, design-agent.md, devex-agent.md, security-agent.md, qa-agent.md, coderabbit-methodology.md, recurring-defects.md, advisor-pattern.md, confidence-gate.md, symbols.md, schema/core.md (if DB/schema touched)
- Task tool: spawn 5 parallel Phase 1 subagents (Architecture/model=sonnet, Design/model=sonnet, Devex/model=sonnet, Security/model=sonnet or ywc-security-engineer if catalog installed, QA/model=haiku), each injected with filtered Step 0 learnings and --profile chill nitpick suppression
- Run available linters/scanners (eslint/ruff/shellcheck/semgrep/gitleaks/ast-grep etc. as applicable) and feed output to relevant subagent as evidence
- Aggregate Phase 1 confirmed findings + advisor candidates; dedupe by file:line; cap at --advisor-budget (default 5) prioritizing Critical>High>Medium then Security>Architecture>Design>Devex>QA; log dropped candidates
- Task tool: sequential Phase 2 Opus advisor calls (model=opus, or ywc-architect/ywc-performance-engineer routing hints) for surviving candidates, bounded context payload only, <=200 word verdicts
- Merge Phase 1 + Phase 2 into final report with [P1]/[P2] provenance markers and severity symbols
- Apply Confidence Gate (Evidence quality, Root cause identified dimensions >=70) to compute PROCEED/REVIEW/STOP band and map to DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED
- If PROCEED + DONE/DONE_WITH_CONCERNS, attach ywc-verify-done evidence block (command, output excerpt, exit code) before status line, no hedging language
- Emit markdown report (or --format html if requested) following the Output Format template
- Offer Step 7: promote recurring confirmed findings / user-dismissed false positives into docs/review-learnings.md via Skill ywc-review-learnings --mode update --source review, gated on user confirmation CHANGESET
- Do not call gh pr create myself — PR creation is the documented downstream step, left for the user or a follow-up ywc-create-pr invocation once Critical/High findings are resolved

## Files touched
- claude-code/skills/ywc-impl-review/SKILL.md
- CLAUDE.md
- package.json (or repo manifest)
- docs/ubiquitous-language.md
- docs/review-learnings.md
- <user-specified spec file>
- <user-specified code path or git-diff-derived files>
- claude-code/skills/ywc-impl-review/references/architecture-agent.md
- claude-code/skills/ywc-impl-review/references/design-agent.md
- claude-code/skills/ywc-impl-review/references/devex-agent.md
- claude-code/skills/ywc-impl-review/references/security-agent.md
- claude-code/skills/ywc-impl-review/references/qa-agent.md
- claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md
- claude-code/skills/ywc-impl-review/references/recurring-defects.md
- claude-code/skills/references/advisor-pattern.md
- claude-code/skills/references/confidence-gate.md
- claude-code/skills/references/symbols.md
- claude-code/skills/references/schema/core.md

## Gates enforced
- Required-argument gate: --spec and (--code XOR --git-range) must be resolved before Phase 1 dispatch
- Rationalization Defense table (no skipping severity ratings, no forwarding full files to advisor, verify-before-surface)
- --profile chill nitpick suppression (Critical/High/Medium never suppressed)
- Advisor budget cap (default 5 Opus calls, dedup by file:line, priority ordering)
- Phase 2 context-payload bounding (finding text + <=100-line snippet + spec excerpt + rubric only, no full files/transcripts)
- Confidence Gate dual-dimension check (Evidence quality >=70, Root cause identified >=70) with PROCEED/REVIEW/STOP banding
- ywc-verify-done evidence-block requirement before any DONE/DONE_WITH_CONCERNS status line
- Completion Status decision table (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT)
- Learnings-capture requires explicit user-confirmed CHANGESET, never inferred write

## Full narrative

Here is exactly how I would proceed under the ywc-impl-review procedure.

First, I would announce the skill per its required opening line: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."

Before doing any real work, I would stop and ask a clarifying question. The skill's Arguments table declares `--spec` and `--code` (or the mutually exclusive `--git-range`) as required, and Execution Step 2 explicitly depends on having a specification file to read and a concrete code target. The user's phrasing only describes the general scenario ("implementation complete, before PR, validate against spec") without naming either. I would ask something like: "Which specification document should this implementation be checked against, and should I review a specific code path (`--code`) or derive the diff from a git range (`--git-range`, e.g. `main...HEAD`)?" I would not guess a spec path or silently default to a git range, because a wrong target would produce a conformance report that is confidently wrong.

Once those two inputs are supplied (for illustration, assume the user answers with `--spec docs/specification/<feature>.md` and `--git-range main...HEAD`, matching this repo's current branch `feature/skill-hell-base` against base `main`), I would execute the full pipeline as written:

**Step 0 (learnings).** Unless `--skip-learnings` is passed, invoke the `ywc-review-learnings` skill with `--mode read --target <changed files>` to pull `docs/review-learnings.md` into a compact "Applicable Review Learnings" block. If the file doesn't exist, proceed with an empty set — never block on its absence.

**Step 1 (context).** Read `CLAUDE.md` at the project root and `package.json` (or the repo's equivalent manifest) to identify conventions, tech stack, and PR gate conditions. Check for `docs/ubiquitous-language.md` and read it if present, since reviewer subagents must flag identifiers matching a "Synonyms to Avoid" entry.

**Step 2 (spec + code).** Since `--git-range` was chosen, run `git diff --name-only main...HEAD` to get the changed-file list and treat those as the review target. Read the specification file in full and every target code file. This context stays local to my parent context — it is never forwarded wholesale to Phase 2.

**Step 3 (Phase 1 — five parallel subagents via the Task tool, model pinned explicitly on each):**
- Architecture (`model: sonnet`) — module boundaries, layering, dependency direction, over-abstraction, structural spec conformance, using `references/architecture-agent.md`; if the diff touches DB schema/migrations, also apply `references/schema/core.md` Part C and cross-reference cascade/multi-tenant gaps to Security rather than duplicating.
- Design (`model: sonnet`) — API/interface design, naming, signatures, error models, contract conformance, using `references/design-agent.md`.
- Devex (`model: sonnet`) — readability, error messages, logging, docs, debuggability, config UX, using `references/devex-agent.md`.
- Security (`model: sonnet`, or `subagent_type: ywc-security-engineer` if the named-agent catalog at `tools/claude-code/agents/` is installed) — OWASP Top 10 analysis using `references/security-agent.md`.
- QA (`model: haiku`) — coverage-gap and missing-test-case detection using `references/qa-agent.md`.

Each subagent prompt gets the filtered Step 0 learnings injected (DO/DO-NOT become extra checks, FALSE-POSITIVE entries suppress known non-issues), applies the `--profile chill` default (suppress Low/Info Style/Docs/polish tail, never suppress Critical/High/Medium), and enforces verify-before-surface (every finding needs `file:line`, a traced symbol, or fresh command output, or it's dropped rather than hedged). Where the project ships linters/scanners (eslint, ruff, golangci-lint, shellcheck, semgrep, gitleaks, ast-grep) I would run them and feed the output to the matching subagent as evidence, not as verdict. I'd also check whether the changed-file list is dominated by a single language (TypeScript/Python/Go) to swap in the Tier-2 named reviewer for Design/Devex; this repo is mostly Markdown/shell, so I'd keep the generic subagent prompts. Each subagent returns Confirmed findings plus Advisor candidates (finding text, ≤100-line snippet, spec excerpt, one-sentence escalation reason).

**Step 4 (aggregate).** Combine all five candidate lists, dedupe on `{file}:{line}`, cap at `--advisor-budget` (default 5), prioritizing Critical > High > Medium and, within a tier, Security > Architecture > Design > Devex > QA. Log anything dropped for budget reasons so the user can see what wasn't escalated.

**Step 5 (Phase 2 — advisor pass, skip if `--no-advisor`).** For each surviving candidate, spawn a sequential Opus subagent (`model: opus`), preferring `subagent_type: ywc-architect` for Architecture candidates or `ywc-performance-engineer` for performance-flavored Architecture/Devex candidates when the catalog is installed. Context payload is strictly the finding text, the bounded snippet, the spec excerpt, and the category severity rubric — never the full spec, full file, or Phase 1 transcripts. Expected output is a ≤200-word verdict: confirmed severity, one-line rationale, "confirmed" or "adjusted."

**Step 6 (merge + report).** Combine Phase 1 confirmed findings with Phase 2 verdicts, marking each with `[P1]`/`[P2]` provenance, and emit the report per the fixed template: Summary (counts per aspect, advisor calls used), per-aspect sections (Architecture/Design/Devex/Security/Testing) with severity symbols (🚨/🔴/🟡/🔵/ℹ️), Fix Priority sorted by severity, Advisor Budget Report, and Completion Status.

Before emitting, I would apply the Confidence Gate: both Evidence quality and Root cause identified must score ≥70; the resulting band (PROCEED ≥90 / REVIEW 70–89 / STOP <70) maps to Completion Status (DONE or DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED respectively). If the band is PROCEED and the report claims DONE/DONE_WITH_CONCERNS, I would attach a `ywc-verify-done`-style evidence block (command run, output excerpt, exit code) before the status line and avoid "should/probably/seems" wording — an unverified "looks good" would get downgraded to REVIEW instead of being accepted at face value.

**Step 7 (capture learnings, skip if `--skip-learnings`).** After the report, I would offer — not silently write — to promote recurring confirmed findings or user-dismissed false positives into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`, gated on the tool's own user-confirmation CHANGESET flow.

What I would explicitly not do: I would not call `gh pr create` or otherwise open the pull request myself. PR creation is documented as this skill's downstream step (`ywc-create-pr`), separate from the review itself, and per the Completion Status rules, if the review lands on DONE_WITH_CONCERNS or BLOCKED I would flag that Critical/High findings need human action before anyone proceeds to that downstream step.
