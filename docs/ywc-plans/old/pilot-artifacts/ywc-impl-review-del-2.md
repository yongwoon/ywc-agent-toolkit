# Dispatch artifact: ywc-impl-review (deleted body, run 2)

**Key**: claude-code/skills/ywc-impl-review/SKILL.md:21-21
**Scenario**: I need help with the following: implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a refusal — an escalation/clarifying-question point. The user's request matched the ywc-impl-review skill's trigger exactly (\"implementation is complete... before creating a PR... validate code matches the spec, check implementation quality, or run a comprehensive review\"), but the skill's Arguments table marks --spec and --code (or --git-range) as required with no defaults, and the skill itself defines a NEEDS_CONTEXT completion status for exactly this situation (\"Spec and code paths are ambiguous; cannot determine what conformance means without clarification\"). Before running any subagents I would first attempt lightweight inference (diff the current branch against main, look for an associated spec under docs/ywc-plans/ or tasks/), but if that inference did not converge on one unambiguous spec file and code target, I would ask the user to confirm the spec path and the code path or git range rather than guessing — proceeding on a guessed spec risks reviewing against the wrong contract, which the skill treats as a hard gate, not a style preference.

## Actions
- Announce skill start per SKILL.md line 9 (five-axis architecture/design/devex/security/QA review)
- Check for required --spec and --code/--git-range arguments; since neither was supplied, run 'git status' and 'git log main..HEAD' (or equivalent) to attempt inference of a --git-range from the current feature branch, and look under docs/ywc-plans/ or tasks/ for a spec matching the branch
- If a single unambiguous spec file cannot be confirmed, stop and ask the user to confirm --spec <path> and --code <path> (or --git-range <sha>..<sha>) before proceeding, per the skill's own NEEDS_CONTEXT rule
- Step 0: invoke ywc-review-learnings --mode read --target <changed files> to load docs/review-learnings.md into an 'Applicable Review Learnings' block (proceed with empty set if file absent)
- Step 1: Read CLAUDE.md (root and relevant subproject), package.json if present, and docs/ubiquitous-language.md if present, to capture conventions/tech stack/PR gates and canonical-term synonyms
- Step 2: run 'git diff --name-only <range>' (if --git-range used) to get the changed-file list; Read the spec file and every target code file in full
- Step 3: spawn 5 Task-tool subagents in parallel with explicit model params: Architecture (model: sonnet, references/architecture-agent.md), Design (model: sonnet, references/design-agent.md), Devex (model: sonnet, references/devex-agent.md), Security (model: sonnet, prefer subagent_type: ywc-security-engineer if tools/claude-code/agents/ installed, references/security-agent.md), QA (model: haiku, references/qa-agent.md)
- Inject the Step 0 learnings filtered per-category into each subagent prompt (DO/DO-NOT as extra checks, FALSE-POSITIVE as suppression instructions)
- Apply --profile chill by default: subagents surface only correctness/security/logic/runtime-risk findings, suppress Style/Docs/Devex-polish Low/Info tail
- Check whether changed files are dominated by a single language (TypeScript/Python/Go) to swap in Tier-2 language reviewers (ywc-typescript-reviewer / ywc-python-reviewer / ywc-go-reviewer) for Design/Devex; otherwise keep generic Sonnet subagents
- Where linters/scanners exist in the target repo (e.g., 'bash scripts/validate.sh', shellcheck, eslint, ruff), run them and feed output to the relevant subagent as evidence, not as the verdict
- Require each subagent to cite file:line or command output for every finding (verify-before-surface); drop unsubstantiated findings rather than hedging them
- Collect each subagent's two artifacts: Confirmed findings and Advisor candidates (finding text + ≤100-line snippet + spec excerpt + one-sentence escalation reason)
- Step 4: aggregate all Phase 1 advisor candidates, dedupe by {file}:{line} across categories, cap at --advisor-budget (default 5), prioritize Critical>High>Medium and Security>Architecture>Design>Devex>QA within a tier, log any candidates dropped for budget
- Step 5 (skip if --no-advisor): for each surviving candidate, spawn a sequential Task-tool subagent with model: opus (prefer ywc-architect for Architecture-sourced candidates, ywc-performance-engineer for performance-ambiguity candidates), passing only the finding text, bounded snippet, spec excerpt, and category severity rubric — never the full spec or file
- Collect each Opus verdict (≤200 words: confirmed severity, one-line rationale, confirmed/adjusted)
- Step 6: merge Phase 1 confirmed findings with Phase 2 verdicts, tagging each finding [P1] or [P2] for provenance
- Apply the Confidence Gate to the aggregated report before emission: score Evidence quality and Root cause identified (each must be ≥70)
- Map the gate band to Completion Status per the skill's table: PROCEED→DONE/DONE_WITH_CONCERNS (by Critical/High count), REVIEW(70-89)→NEEDS_CONTEXT with weakest dimension flagged, STOP(<70)→BLOCKED with dimensions failed and what Phase 2 calls would raise the score
- If band is PROCEED and a DONE/DONE_WITH_CONCERNS claim is made, attach a ywc-verify-done-style evidence block (command, output excerpt, exit code) before the status line and avoid hedging language ('should'/'probably'/'seems')
- Emit the final markdown report using the skill's fixed template: Summary, per-axis finding lists with severity symbols (🚨🔴🟡🔵ℹ️) and [P1]/[P2] markers, Fix Priority sorted by severity, Advisor Budget Report, Completion Status
- Step 7 (skip if --skip-learnings): after presenting the report, offer to promote recurring confirmed findings into docs/review-learnings.md via ywc-review-learnings --mode update --source review, and capture any user-dismissed finding as a FALSE-POSITIVE learning with the dismissal reason — only after explicit user confirmation of the CHANGESET
- Do not proceed to PR creation myself — per Integration, downstream of this skill is 'PR creation' as a separate step (e.g., ywc-create-pr), not part of this skill's scope

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-impl-review-21-21.md (read only, per task instructions)
- CLAUDE.md (root and relevant subproject, to be read in Step 1)
- package.json (to be read in Step 1, if present)
- docs/ubiquitous-language.md (to be read in Step 1, if present)
- docs/review-learnings.md (to be read in Step 0 via ywc-review-learnings, and potentially updated in Step 7)
- <spec file path> (to be confirmed with the user, then read in full in Step 2)
- <target code files under --code or derived from --git-range> (to be read in full in Step 2)
- references/architecture-agent.md, references/design-agent.md, references/devex-agent.md, references/security-agent.md, references/qa-agent.md (to be read when spawning each Phase 1 subagent)
- references/coderabbit-methodology.md, references/recurring-defects.md, references/advisor-pattern.md, references/confidence-gate.md, references/symbols.md (to be consulted per the skill's own citations)
- claudedocs/<report>.html (only created if --format html is requested)

## Gates enforced
- Required-argument gate: --spec and (--code XOR --git-range) are mandatory; without them the review cannot start
- NEEDS_CONTEXT gate: if spec/code paths remain ambiguous after inference attempts, ask the user rather than guessing
- Verify-before-surface gate: every Phase 1 finding must cite file:line/traced symbol/command output or be dropped, never hedged
- Advisor budget gate: Phase 2 Opus calls capped at --advisor-budget (default 5), shared across all categories, sequential not parallel
- Confidence Gate: Evidence quality and Root cause identified must each score >=70 before the report is treated as authoritative; band (PROCEED/REVIEW/STOP) maps to Completion Status
- ywc-verify-done evidence-block requirement: a DONE/DONE_WITH_CONCERNS claim under a PROCEED band must carry command+output+exit-code evidence, no hedging language
- Learnings-confirmation gate: new entries to docs/review-learnings.md require explicit user confirmation of the CHANGESET before being written
- Severity-never-suppressed gate: Critical/High/Medium findings are always surfaced regardless of --profile; only Low/Info nitpick tail is suppressed under chill

## Full narrative

Here is exactly how I would carry out this review under the ywc-impl-review procedure.

First, I would announce the skill per its own instruction: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."

**Argument check before anything else.** The skill requires `--spec <path>` and either `--code <path>` or `--git-range <sha>..<sha>` (mutually exclusive). The user's request supplied neither. So my very next moves would be diagnostic, not generative: I would run `git status` and `git log main..HEAD --oneline` (or the appropriate base branch) to see what the current feature branch actually changed, and I would look for a candidate spec — e.g. under `docs/ywc-plans/` or a `tasks/*/spec.md`-style location tied to the branch name. If that search resolves to exactly one spec and one clear changed-file set, I would proceed with `--git-range <merge-base>..HEAD` derived automatically. If it does not resolve unambiguously (multiple plausible spec files, or a branch with unrelated commits mixed in), I would stop and ask the user directly: "Which specification file should this be validated against, and should I review a specific code path or the diff since branching from main?" — this is the skill's own NEEDS_CONTEXT case, not something to paper over with a guess.

Assuming the paths are confirmed (either by the user or by unambiguous inference), the rest of the pipeline runs exactly as specified:

**Step 0 — Learnings.** Unless `--skip-learnings` was passed, invoke `ywc-review-learnings --mode read --target <changed files>` to pull `docs/review-learnings.md` into a compact "Applicable Review Learnings" block. If the file doesn't exist, proceed with an empty set — this never blocks the review.

**Step 1 — Project context.** Read `CLAUDE.md` (both the workspace root and the relevant subproject's, since this is a multi-project monorepo), `package.json` if the target subproject has one, and `docs/ubiquitous-language.md` if present, to pick up conventions, tech stack, PR gates, and canonical-term synonyms reviewers must flag against.

**Step 2 — Read spec + code.** If `--git-range` was used, run `git diff --name-only <range>` to get the changed-file list. Read the spec file and every target code file in full. This full context stays with me (the parent); it is never forwarded wholesale to Phase 2.

**Step 3 — Phase 1 parallel review.** Spawn five Task-tool subagents in parallel, each with an explicit `model` param so cost stays at Sonnet/Haiku:
- Architecture (`model: sonnet`, `references/architecture-agent.md`) — module boundaries, layering, dependency direction, over-abstraction, structural spec conformance; if the diff touches DB schema, also apply the shared schema checklist and cross-reference cascade/tenant-scope issues to Security as one-liners rather than duplicating.
- Design (`model: sonnet`, `references/design-agent.md`) — API/interface design, naming, signatures, error models, public-surface discipline.
- Devex (`model: sonnet`, `references/devex-agent.md`) — readability, error messages, logging, docs, debuggability, config UX.
- Security (`model: sonnet`, `references/security-agent.md`) — OWASP Top 10; preferring `subagent_type: ywc-security-engineer` if `tools/claude-code/agents/` is installed in that repo.
- QA (`model: haiku`, `references/qa-agent.md`) — test coverage gaps, missing test cases.

I would inject the Step 0 learnings filtered per category into each prompt (DO/DO-NOT as extra checks, FALSE-POSITIVE as explicit suppression), apply `--profile chill` by default (only correctness/security/logic/runtime-risk findings surface; Low/Info nitpicks are suppressed, Critical/High/Medium never are), and check whether the changed-file list is dominated by a single language warranting a Tier-2 swap (`ywc-typescript-reviewer` / `ywc-python-reviewer` / `ywc-go-reviewer` for Design/Devex). Where the target repo ships linters (eslint, ruff, golangci-lint, shellcheck, semgrep, `scripts/validate.sh` if that's the repo in question), I would run them and hand the output to the relevant subagent as evidence to triage, not as the verdict. Every finding a subagent returns must cite `file:line` or command output — anything that can't be substantiated gets dropped, not hedged with "might be." Each subagent returns Confirmed findings plus Advisor candidates (finding text, ≤100-line snippet, spec excerpt, one-sentence escalation reason).

**Step 4 — Aggregate candidates.** Combine all five candidate lists, dedupe by shared `{file}:{line}`, cap at `--advisor-budget` (default 5) prioritizing Critical > High > Medium and, within a tier, Security > Architecture > Design > Devex > QA. Log anything dropped for budget in the final report.

**Step 5 — Phase 2 advisor pass** (skipped only if `--no-advisor`). For each surviving candidate, spawn a sequential `model: opus` Task-tool call — `ywc-architect` for Architecture-sourced candidates, `ywc-performance-engineer` for performance-ambiguity candidates — passing only the finding text, bounded snippet, spec excerpt, and the category's severity rubric, never the full spec/file/Phase-1 transcript. Each returns a ≤200-word verdict: confirmed severity, one-line rationale, confirmed-or-adjusted.

**Step 6 — Merge.** Combine Phase 1 confirmed findings with Phase 2 verdicts, tagging each `[P1]` or `[P2]` for provenance.

**Confidence Gate.** Before emitting anything, score Evidence quality and Root cause identified (each must be ≥70). Map the resulting band to Completion Status: PROCEED (≥90) → DONE or DONE_WITH_CONCERNS by Critical/High count; REVIEW (70–89) → NEEDS_CONTEXT with the weakest dimension flagged at the top; STOP (<70) → BLOCKED, reporting which dimensions failed and what additional Phase 2 calls would raise the score. If the band is PROCEED and I'm asserting DONE/DONE_WITH_CONCERNS, I would attach a verification evidence block (command run, output excerpt, exit code) before the status line and avoid any hedging language — an "all clear, looks good" without that evidence gets downgraded to REVIEW.

**Report emission.** I would emit the fixed markdown template: Summary (per-axis finding counts, Phase 2 call usage), then Architecture / Design / Devex (Developer Experience) / Security / Testing (QA) sections each with `[severity-symbol] [P1|P2] file:line — description` lines (using 🚨/🔴/🟡/🔵/ℹ️ per the symbols reference, plus the Advisor verdict line for any `[P2]` entries), a Fix Priority list sorted Critical-first, an Advisor Budget Report (used vs. budget, anything dropped), and the Completion Status line.

**Step 7 — Capture learnings** (skipped only if `--skip-learnings`). After presenting the report, I would offer — not silently perform — to promote recurring confirmed findings into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`, and to record any finding the user dismisses as a false positive together with their stated reason. I would not write to that file without the user's explicit confirmation of the changeset, since the skill treats that as a required gate, not a formality.

Finally, per the skill's own Integration section, PR creation is explicitly downstream of this skill, not part of it — so even after a clean DONE report, I would stop here and hand off to a PR-creation flow (e.g., `ywc-create-pr`) rather than opening the PR myself as part of this review.
