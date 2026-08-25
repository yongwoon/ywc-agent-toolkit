# Dispatch artifact: ywc-impl-review (deleted body, run 3)

**Key**: claude-code/skills/ywc-impl-review/SKILL.md:21-21
**Scenario**: I need help with the following: implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The skill's Arguments table marks --spec (spec file path) and --code (or the mutually-exclusive --git-range) as required, and the user's request supplies neither. Rather than guess which spec document defines conformance or which code/diff scope to review, the procedure's own Completion Status table provides for exactly this: NEEDS_CONTEXT — "Spec and code paths are ambiguous; cannot determine what conformance means without clarification." So before running Steps 0–7, I would ask the user to confirm the --spec path and the --code path or --git-range, and, optionally, whether --profile assertive, --no-advisor, --advisor-budget, or --format html should apply. I have narrated the full downstream execution below assuming those are supplied, since that is the concrete procedure this skill defines.

## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-impl-review-21-21.md (procedure file) — no other tool calls performed
- Announce: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."
- Check required arguments --spec and (--code | --git-range); neither was supplied by the user
- Ask a clarifying question for --spec path and --code path (or --git-range)
- (If answered) Invoke ywc-review-learnings --mode read --target <changed files> to load docs/review-learnings.md
- (If answered) Read CLAUDE.md, check for package.json, check for docs/ubiquitous-language.md
- (If answered) Run git diff --name-only <range> if --git-range given; Read the spec file and all target code files
- (If answered) Spawn 5 parallel Task-tool subagents: Architecture(sonnet), Design(sonnet), Devex(sonnet), Security(sonnet, prefer ywc-security-engineer if tools/claude-code/agents/ installed), QA(haiku), each reading its references/*-agent.md
- (If answered) Check tools/claude-code/agents/ for Tier-2 language reviewers (ywc-typescript-reviewer / ywc-python-reviewer / ywc-go-reviewer) applicability
- (If answered) Run available linters/scanners (e.g. shellcheck on scripts/, markdownlint on skill READMEs) and feed output to subagents as evidence
- (If answered) Aggregate Phase 2 candidates, dedupe by file:line, cap at --advisor-budget (default 5), prioritize Critical>High>Medium then Security>Architecture>Design>Devex>QA
- (If answered) Spawn sequential Phase 2 model:opus advisor subagents for surviving candidates with bounded context payload
- (If answered) Merge Phase 1 + Phase 2 findings marking [P1]/[P2] provenance
- (If answered) Apply Confidence Gate scoring (evidence quality, root cause identified) and map band to Completion Status
- (If answered) Emit final Output Format markdown report with Summary, per-axis findings, Fix Priority, Advisor Budget Report, Completion Status
- (If answered) Offer (not execute) to promote durable learnings via ywc-review-learnings --mode update --source review, gated on user CHANGESET confirmation
- Do not create the PR myself — PR creation is the documented downstream step, handled separately (e.g. by ywc-create-pr) after this review's DONE/DONE_WITH_CONCERNS status

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-impl-review-21-21.md (read only)

## Gates enforced
- Required-argument gate (--spec and --code/--git-range mutually exclusive, both otherwise mandatory) — unmet, triggers clarifying question / NEEDS_CONTEXT path
- Advisor budget cap (default 5 Opus calls, --advisor-budget override)
- Verify-before-surface evidence gate (file:line / traced symbol / command output required or finding is dropped)
- --profile chill default (suppresses Low/Info nitpick tail; Critical/High/Medium never suppressed)
- Confidence Gate (Evidence quality ≥70, Root cause identified ≥70) mapping to PROCEED/REVIEW/STOP → DONE|DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
- ywc-verify-done evidence-block requirement when gate band is PROCEED and status claims DONE/DONE_WITH_CONCERNS
- Learnings capture gated on explicit user-confirmed CHANGESET before writing docs/review-learnings.md

## Full narrative

Having read the ywc-impl-review procedure end to end, here is exactly what I would do for this request.

**Step 0 — Announce and check preconditions.** I would open with the mandated announcement: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review." Then I would check the Arguments table: `--spec` and `--code` (or `--git-range`, mutually exclusive with `--code`) are both marked required, and the user's message contains neither a spec document nor a code path/diff range. Per the Completion Status rules, this is the textbook `NEEDS_CONTEXT` case ("Spec and code paths are ambiguous; cannot determine what conformance means without clarification"), so rather than guessing I would ask: "Which specification document should I treat as the source of truth (--spec), and which code path or git range should I review (--code, e.g. `api/src/routes/`, or --git-range, e.g. `main..HEAD`)? Also let me know if you want `--profile assertive` instead of the default `chill`, a lower `--advisor-budget`, `--no-advisor` for throwaway code, or `--format html`."

Assuming the user then answers with, say, `--spec docs/ywc-plans/<task>/spec.md` and `--git-range main..HEAD`, I would proceed as follows.

**Step 0 (learnings).** Invoke `ywc-review-learnings --mode read --target <changed files>` to pull `docs/review-learnings.md` into a compact "Applicable Review Learnings" block. If the file doesn't exist I would proceed with an empty set rather than block.

**Step 1 (project context).** Read `CLAUDE.md` at repo root (already in context), check for `package.json` (this repo is a bash/skill-distribution toolkit, so likely absent — I would note that and fall back to `scripts/install.sh` / repo structure as the convention source), and check for `docs/ubiquitous-language.md` to load canonical-term rules for the Design reviewer.

**Step 2 (spec + code).** Run `git diff --name-only main..HEAD` to get the changed-file list, then Read the spec file and every changed file in full. This context stays local to the parent turn; none of it is forwarded wholesale to Phase 2.

**Step 3 (Phase 1 — five parallel subagents via the Task tool, each with an explicit `model:`):**
- Architecture (`model: sonnet`) — module boundaries, layering, dependency direction, over-abstraction, structural spec conformance, briefed from `references/architecture-agent.md`. Since this repo has no DB migrations, I'd skip the schema checklist cross-reference.
- Design (`model: sonnet`) — API/interface shape, naming vs `docs/ubiquitous-language.md`, error models, briefed from `references/design-agent.md`.
- Devex (`model: sonnet`) — readability, error messages, logging, docs, config UX, briefed from `references/devex-agent.md`.
- Security (`model: sonnet`) — OWASP Top 10, briefed from `references/security-agent.md`; I would check whether `tools/claude-code/agents/ywc-security-engineer.md` is installed and if so dispatch with `subagent_type: ywc-security-engineer` instead of the generic prompt.
- QA (`model: haiku`) — coverage gaps, briefed from `references/qa-agent.md`.

Before dispatch I'd check the changed-file list for a dominant language to see whether Tier-2 reviewers (`ywc-typescript-reviewer`, `ywc-python-reviewer`, `ywc-go-reviewer`) should replace the generic Design/Devex subagents — for a shell/markdown-heavy skill repo like this one, none currently apply, so I'd keep the generic prompts. I would inject the Step 0 learnings filtered per aspect, apply `--profile chill` (suppress Low/Info Style/Docs nitpicks; never suppress Critical/High/Medium), and run any available linters/scanners as evidence — concretely `shellcheck scripts/*.sh` and `markdownlint` on touched README files — feeding their raw output to the relevant subagent rather than treating it as the verdict. Each subagent must return Confirmed findings plus Advisor candidates (finding text, ≤100-line snippet, spec excerpt, one-sentence escalation reason), and every finding must cite `file:line` or command output or be dropped, not hedged.

**Step 4 (aggregate Phase 2 candidates).** Merge the five candidate lists, dedupe by `{file}:{line}`, cap at `--advisor-budget` (default 5), and if over budget prioritize Critical>High>Medium, then within a tier Security>Architecture>Design>Devex>QA. Log anything dropped by the cap for the final report's Advisor Budget Report section.

**Step 5 (Phase 2 advisor pass).** For each surviving candidate, spawn a sequential `model: opus` subagent with only the bounded payload (finding text, snippet, spec excerpt, category rubric) — never the full spec/file/Phase-1 transcript. I'd route Architecture candidates to `subagent_type: ywc-architect` and performance-flavored Architecture/Devex candidates to `subagent_type: ywc-performance-engineer` if those named agents are installed under `tools/claude-code/agents/`. Each verdict is capped at ≤200 words: confirmed severity, one-line rationale, "confirmed" or "adjusted."

**Step 6 (merge + report).** Combine Phase 1 confirmed findings with Phase 2 verdicts, tagging each `[P1]` or `[P2]`.

**Confidence Gate.** Before emitting, score Evidence quality and Root cause identified (both must be ≥70). Map PROCEED (≥90) → `DONE`/`DONE_WITH_CONCERNS` per the Critical/High count; REVIEW (70–89) → `NEEDS_CONTEXT` with the gate score and weakest dimension flagged at the top; STOP (<70) → `BLOCKED`, withholding findings as authoritative and stating what additional Phase 2 calls would raise the score. If the report lands PROCEED and claims DONE/DONE_WITH_CONCERNS, I would also attach the `ywc-verify-done` evidence block (command run, output excerpt, exit code) before the status line and avoid hedge words like "should"/"probably."

**Output.** Emit the report in the exact template from the skill: Summary (per-axis finding counts, Phase 2 usage X of Y, adjustments), per-axis finding lists using the severity emoji (🚨/🔴/🟡/🔵/ℹ️) with `[P1]`/`[P2]` markers, Fix Priority sorted Critical-first, Advisor Budget Report, and Completion Status. If `--format html` was requested I'd instead write a self-contained HTML report to `claudedocs/` per `references/html-output.md`, preserving the Markdown content inside it.

**Step 7 (learnings capture).** After the report, offer — not silently perform — to promote recurring confirmed findings into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`, and record any user-dismissed finding as a `FALSE-POSITIVE` learning with the dismissal reason, gated on the user-confirmed CHANGESET that skill enforces.

**What I would not do:** I would not create the pull request myself as part of this skill — the skill's own Integration section names PR creation as the downstream step, not something ywc-impl-review performs. I also would not skip Phase 2 by default, would not silently guess at `--spec`/`--code`, would not surface unverified "might be" findings, and would not treat "no findings" as proof of spec conformance — the Rationalization Defense table explicitly calls that out as a false excuse.
