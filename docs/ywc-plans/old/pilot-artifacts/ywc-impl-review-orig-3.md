# Dispatch artifact: ywc-impl-review (original body, run 3)

**Key**: claude-code/skills/ywc-impl-review/SKILL.md:21-21
**Scenario**: I need help with the following: implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a refusal — the request matches the skill's intended use exactly. However, the skill's Arguments table marks --spec and --code (or --git-range) as required, and the user's message supplies neither a spec file path nor a code path/git range. Proceeding without resolving this would mean guessing the conformance baseline, which risks reviewing against the wrong spec entirely. Per the skill's own Completion Status rules (NEEDS_CONTEXT: 'Spec and code paths are ambiguous; cannot determine what conformance means without clarification'), the correct move is to ask a targeted clarifying question (while proposing a concrete best-guess default drawn from repo conventions for the user to confirm or override) before spawning any Phase 1 subagents.

## Actions
- Announce skill start with the exact required line: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."
- Check the Arguments table: --spec and --code (or --git-range, mutually exclusive with --code) are required and were not supplied in the request
- Ask a clarifying question before proceeding: which spec file is the conformance baseline, and whether to scope by --code <path> or --git-range <sha>..<sha>; propose a best-guess default (e.g. tasks/<current-task>/spec doc plus git diff main..HEAD) for the user to confirm
- Once params are confirmed: Step 0 - invoke ywc-review-learnings --mode read --target <changed files> to load docs/review-learnings.md (skip cleanly if absent)
- Step 1 - Read CLAUDE.md (root and claude-code/skills/CLAUDE.md), repo convention files (no package.json in this repo; use scripts/validate.sh, .github/workflows/validate.yml as convention signal), and docs/ubiquitous-language.md if present
- Step 2 - run `git diff --name-only <range>` (if --git-range) to get the changed-file list; Read the spec file and every target code file
- Step 3 - spawn five parallel Task-tool subagents with explicit model pins: Architecture (sonnet, references/architecture-agent.md), Design (sonnet, references/design-agent.md), Devex (sonnet, references/devex-agent.md), Security (sonnet, references/security-agent.md, prefer subagent_type ywc-security-engineer if claude-code/agents/ catalog installed), QA (haiku, references/qa-agent.md)
- Check Tier-2 language-reviewer dispatch: since this repo's changed files are likely Bash/Markdown (scripts/, SKILL.md), no ywc-typescript-reviewer/ywc-python-reviewer/ywc-go-reviewer substitution applies; keep generic Design/Devex subagents
- Inject Step 0 learnings into each subagent prompt (DO/DO-NOT as extra checks, FALSE-POSITIVE as suppression instructions); apply --profile chill default (suppress Low/Info nitpicks); enforce verify-before-surface (file:line or command-output evidence required, unverifiable findings dropped not hedged); run shellcheck against changed scripts/*.sh and feed output as evidence
- Collect each subagent's Confirmed findings + Advisor candidates (bounded snippet <=100 lines, spec excerpt, one-sentence escalation reason)
- Step 4 - aggregate all candidates, dedupe by {file}:{line}, cap at --advisor-budget (default 5), prioritize Critical>High>Medium then Security>Architecture>Design>Devex>QA, log any dropped-due-to-cap candidates
- Step 5 - sequentially spawn Opus (model: opus) advisor subagents for each surviving candidate, passing only finding text + bounded snippet + spec excerpt + category severity rubric (never full spec/file/transcripts); prefer ywc-architect for Architecture candidates and ywc-performance-engineer for performance-flavored candidates when the named-agent catalog is installed; expect <=200-word verdict (severity, rationale, confirmed/adjusted)
- Step 6 - merge Phase 1 confirmed findings with Phase 2 verdicts, tagging each finding [P1] or [P2] for provenance
- Apply the Confidence Gate (references/confidence-gate.md) scoring Evidence quality and Root cause identified (>=70 each); map gate band to Completion Status per the band table (PROCEED->DONE/DONE_WITH_CONCERNS with a ywc-verify-done evidence block; REVIEW->NEEDS_CONTEXT with gate score and weakest dimension surfaced; STOP->BLOCKED with findings marked non-authoritative)
- Emit the markdown report in the exact template: Summary, per-aspect sections with severity emoji symbols and [P1]/[P2] markers, Fix Priority, Advisor Budget Report, Completion Status (default markdown format; would only write to claudedocs/ if user passed --format html)
- Step 7 - offer (not auto-write) to promote recurring confirmed findings or user-dismissed false positives into docs/review-learnings.md via ywc-review-learnings --mode update --source review, gated on user confirmation of the CHANGESET
- Stop after the review report; do not auto-invoke PR creation (ywc-create-pr) since that is a separate downstream skill the user must explicitly request next

## Files touched
- claude-code/skills/ywc-impl-review/SKILL.md (read - the only file actually read in this exercise)
- claude-code/skills/ywc-impl-review/references/architecture-agent.md (would read)
- claude-code/skills/ywc-impl-review/references/design-agent.md (would read)
- claude-code/skills/ywc-impl-review/references/devex-agent.md (would read)
- claude-code/skills/ywc-impl-review/references/security-agent.md (would read)
- claude-code/skills/ywc-impl-review/references/qa-agent.md (would read)
- claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md (would read)
- claude-code/skills/ywc-impl-review/references/recurring-defects.md (would read)
- claude-code/skills/references/advisor-pattern.md (would read)
- claude-code/skills/references/confidence-gate.md (would read)
- claude-code/skills/references/symbols.md (would read)
- claude-code/skills/references/html-output.md (would read only if --format html requested)
- CLAUDE.md (root, would read for conventions)
- claude-code/skills/CLAUDE.md (would read for conventions)
- docs/ubiquitous-language.md (would read if present)
- docs/review-learnings.md (would read/write if present, write only on user confirmation)
- the user-specified --spec file (not yet known - would ask)
- the user-specified --code path or --git-range-derived changed files (not yet known - would ask)

## Gates enforced
- required-arguments-check (--spec and --code/--git-range absent -> clarifying question before subagent dispatch)
- verify-before-surface (findings require file:line/traced-symbol/command-output evidence or are dropped, not hedged)
- advisor-budget-cap (default 5 Opus calls, dedupe + priority ordering before Phase 2)
- confidence-gate (Evidence quality + Root cause identified each >=70, band determines DONE/NEEDS_CONTEXT/BLOCKED)
- profile-chill-nitpick-suppression (Low/Info suppressed by default unless --profile assertive)
- user-confirmation-gate on docs/review-learnings.md CHANGESET writes (Step 7, never auto-written)
- downstream-boundary (review skill stops at report; PR creation is a separate explicit step, not auto-chained)

## Full narrative

I read claude-code/skills/ywc-impl-review/SKILL.md in full, as instructed, and treated it as the sole procedure to follow. Here is exactly what I would do to execute the user's request under that procedure.

First, I would announce the skill verbatim, as the SKILL.md mandates: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."

Next, before touching anything else, I would check the Arguments table. `--spec` and `--code` (or `--git-range` as an alternative to `--code`) are both marked required, and the user's request — "implementation is complete and before creating a PR... validate code matches the spec, check implementation quality" — names neither a spec file nor a code path/range. Rather than guessing, I would ask a short clarifying question, something like: "Could you confirm which specification file should serve as the conformance baseline, and whether I should scope the review to a specific `--code <path>` or to a `--git-range` (e.g. `main..HEAD`)? Based on this repo's structure, my best guess would be the spec document for the current task under `tasks/` or `docs/specification/`, reviewed against `git diff --name-only main..HEAD` on the current branch — let me know if that's right or if you'd like a different scope." This follows directly from the skill's own Completion Status semantics: an unresolved spec/code target maps to `NEEDS_CONTEXT`, not a guessed-at review.

Once the user confirms the spec path and code scope, I would execute the eight-step procedure exactly as written:

**Step 0 (Load Review Learnings)** — unless `--skip-learnings` is set, I would invoke `ywc-review-learnings --mode read --target <changed files>` to pull `docs/review-learnings.md` into a compact "Applicable Review Learnings" block. If the file doesn't exist I would proceed with an empty set rather than blocking.

**Step 1 (Collect Project Context)** — Read the root `CLAUDE.md` and `claude-code/skills/CLAUDE.md` (this repo has no `package.json`; I'd instead look at `scripts/validate.sh` and `.github/workflows/validate.yml` for convention/gate signals), and Read `docs/ubiquitous-language.md` if present so any Design finding can flag terms matching a "Synonyms to Avoid" entry.

**Step 2 (Read Spec + Code)** — if `--git-range` was chosen, run `git diff --name-only <range>` via Bash to get the changed-file list, then Read the confirmed spec file and every target code file.

**Step 3 (Phase 1 — Parallel Executor Review)** — spawn five Task-tool subagents in parallel with explicit `model` pins: Architecture (sonnet, `references/architecture-agent.md`), Design (sonnet, `references/design-agent.md`), Devex (sonnet, `references/devex-agent.md`), Security (sonnet, `references/security-agent.md`, preferring `subagent_type: ywc-security-engineer` since `claude-code/agents/` is present in this repo), and QA (haiku, `references/qa-agent.md`). I would check whether the changed-file list is dominated by one language qualifying for Tier-2 dispatch (TypeScript/Python/Go reviewers) — given this repo's changed surface is typically Bash scripts and Markdown skill files, none of the Tier-2 substitutions would apply, so I'd keep the generic Design/Devex prompts. Each subagent prompt would carry the Step 0 learnings filtered to its category, the `--profile chill` default (suppressing Low/Info nitpicks unless the user asked for `assertive`), and the verify-before-surface rule (every finding needs `file:line`, a traced symbol, or fresh command output — unverifiable findings get dropped, not hedged). I would run `shellcheck` against any changed `.sh` files and feed that output to the relevant subagent as evidence. Each subagent returns Confirmed findings plus bounded Advisor candidates (≤100-line snippet, spec excerpt, one-sentence escalation reason).

**Step 4 (Aggregate and Select Phase 2 Candidates)** — combine all candidate lists, dedupe by `{file}:{line}`, cap at `--advisor-budget` (default 5), prioritizing Critical > High > Medium and, within a tier, Security > Architecture > Design > Devex > QA. I would log anything dropped for exceeding the cap.

**Step 5 (Phase 2 — Advisor Pass)** — unless `--no-advisor`, sequentially spawn `model: opus` subagents for each surviving candidate, passing only the finding text, bounded snippet, spec excerpt, and the category's severity rubric excerpt — never the full spec, full file, or Phase 1 transcripts. I'd prefer `subagent_type: ywc-architect` for Architecture candidates and `ywc-performance-engineer` for performance-flavored candidates, per the routing hints, since the named-agent catalog exists in this repo. I'd expect a ≤200-word verdict per candidate: confirmed severity, one-line rationale, confirmed/adjusted.

**Step 6 (Merge and Output Report)** — combine Phase 1 confirmed findings with Phase 2 verdicts, tagging each with `[P1]` or `[P2]` provenance.

Before emitting, I would apply the **Confidence Gate**: score Evidence quality and Root cause identified (each must be ≥70), and map the resulting band to Completion Status — PROCEED → DONE or DONE_WITH_CONCERNS (with a `ywc-verify-done`-style evidence block: command, output excerpt, exit code, no hedging language), REVIEW → NEEDS_CONTEXT (gate score and weakest dimension surfaced at the top), STOP → BLOCKED (findings marked non-authoritative, with the failing dimensions and what Phase 2 escalation would be needed).

I would then emit the markdown report in the exact template from the SKILL.md: Summary (Phase 1/Phase 2 counts), one section per aspect (Architecture, Design, Devex, Security, Testing/QA) using the severity emoji symbols (🚨/🔴/🟡/🔵/ℹ️) and `[P1]`/`[P2]` markers, a Fix Priority list sorted Critical-first, an Advisor Budget Report, and the Completion Status line. I would keep the default `markdown` format and only produce a `claudedocs/*.html` report if the user explicitly passed `--format html`.

**Step 7 (Capture Learnings)** — after presenting the report, I would offer (not silently execute) promoting recurring confirmed findings, or any finding the user dismisses as a false positive with its stated reason, into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`. I would not write to that file without an explicit user-confirmed CHANGESET.

Finally, per the Integration section, this skill's downstream is PR creation (`ywc-create-pr`) — a separate skill. I would stop at the review report and let the user explicitly ask for PR creation next rather than auto-chaining into it.

The one point where I would deviate from "just proceed" is the missing `--spec`/`--code` arguments: I would surface that gap as a clarifying question (with a concrete proposed default) before doing any subagent dispatch, rather than silently picking a spec file that might not be the one the user means.</narrative>

