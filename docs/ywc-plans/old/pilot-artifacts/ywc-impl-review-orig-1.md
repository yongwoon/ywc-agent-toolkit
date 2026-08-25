# Dispatch artifact: ywc-impl-review (original body, run 1)

**Key**: claude-code/skills/ywc-impl-review/SKILL.md:21-21
**Scenario**: I need help with the following: implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Not a refusal — an escalation via clarifying question. The skill's Arguments table marks --spec and (--code XOR --git-range) as required, and the Completion Status table explicitly defines NEEDS_CONTEXT for exactly this situation ("Spec and code paths are ambiguous; cannot determine what conformance means without clarification"). The user's request states the general intent (pre-PR spec-conformance / quality review) but supplies neither a spec file path nor a code path / git range, so before running Step 1 onward I would ask the user to confirm which spec file is the source of truth and whether the review target is a --code path or a --git-range (proposing main..HEAD as the likely default given the current feature branch, but confirming rather than assuming) before spawning any of the five Phase 1 subagents.

## Actions
- Announce: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."
- Check Arguments table: --spec and (--code XOR --git-range) are required and neither was supplied by the user request
- Ask a clarifying question rather than guess: request the spec file path and either a --code path or a --git-range (proposing main..HEAD as a likely default given current branch feature/skill-hell-base, to confirm not assume)
- (Once args supplied) Step 0: invoke ywc-review-learnings --mode read --target <changed files/--code path> to load docs/review-learnings.md into a DO/DO-NOT/FALSE-POSITIVE block; proceed with empty set if file absent
- Step 1: Read root CLAUDE.md and claude-code/skills/CLAUDE.md for conventions/PR gates; check for package.json (likely absent in this toolkit repo); Read docs/ubiquitous-language.md if present
- Step 2: if --git-range given, run `git diff --name-only <range>` (e.g. `git diff --name-only main..HEAD`) to derive changed-file list; Read the spec file and all target code files in full
- Step 3: spawn 5 parallel Task-tool subagents with explicit model params: Architecture (sonnet, references/architecture-agent.md, + schema checklist cross-ref if DB touched), Design (sonnet, references/design-agent.md), Devex (sonnet, references/devex-agent.md), Security (sonnet, references/security-agent.md, prefer subagent_type ywc-security-engineer since claude-code/agents/ catalog is installed in this repo), QA (haiku, references/qa-agent.md)
- Inject Step 0 learnings per-aspect into each subagent prompt; apply --profile chill default (suppress Low/Info nitpick tail); require each finding cite file:line/traced symbol/command output or be dropped, not hedged
- Run any available linters/scanners over the changed files (e.g. shellcheck on scripts/*.sh via scripts/validate.sh, markdownlint config) and feed output as evidence, not verdict, to the relevant subagent
- Check changed-file dominant language for Tier-2 reviewer substitution (ywc-typescript-reviewer / ywc-python-reviewer / ywc-go-reviewer); this repo is markdown SKILL.md + bash scripts, so no Tier-2 substitution applies and generic Design/Devex sonnet subagents are kept
- Step 4: aggregate each subagent's Advisor candidates, dedupe by {file}:{line}, cap at --advisor-budget (default 5), prioritize Critical>High>Medium then Security>Architecture>Design>Devex>QA; log dropped-over-cap candidates
- Step 5: for each surviving candidate spawn a sequential Task-tool call with model: opus (subagent_type ywc-architect for Architecture-origin candidates, ywc-performance-engineer for performance-ambiguous ones), passing only finding text + bounded ≤100-line snippet + spec excerpt + category rubric — never the full file/spec/Phase-1 transcript; cap verdict at 200 words
- Step 6: merge Phase 1 confirmed findings with Phase 2 verdicts, tagging each [P1]/[P2]
- Apply the Confidence Gate (score-gate.py logic) on Evidence quality and Root cause identified dimensions before emitting; map band to Completion Status (PROCEED→DONE/DONE_WITH_CONCERNS, REVIEW→NEEDS_CONTEXT, STOP→BLOCKED)
- Emit the final report in the specified Output Format template with severity emoji symbols, Fix Priority list, Advisor Budget Report, and Completion Status
- Step 7: offer (not auto-write) to promote recurring confirmed findings and any user-dismissed false positives into docs/review-learnings.md via ywc-review-learnings --mode update --source review, gated on user-confirmed CHANGESET
- Stop after report + learnings offer — do not create the PR myself; that is the downstream ywc-create-pr skill's responsibility

## Files touched
- claude-code/skills/ywc-impl-review/SKILL.md (read only, procedure source)
- CLAUDE.md (root, project context)
- claude-code/skills/CLAUDE.md (skills-directory context)
- docs/review-learnings.md (read in Step 0, offered update in Step 7)
- docs/ubiquitous-language.md (read if present)
- <spec file path> — to be supplied by user
- <code path or git-diff-derived file list> — to be supplied by user
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

## Gates enforced
- Required-argument gate: --spec and --code/--git-range must both be resolvable before Step 1 proceeds
- Rationalization Defense table (11 excuse/reality pairs) checked before skipping any step
- Advisor budget cap (default 5 Opus calls, shared across categories)
- Phase 2 context payload bound: finding text + ≤100-line snippet + spec excerpt + rubric only, never full file/spec/transcript
- Phase 2 verdict length cap: ≤200 words unless justified overrun logged in Advisor Budget Report
- Verify-before-surface: every finding needs primary evidence (file:line / traced symbol / command output) or is dropped, not hedged
- --profile chill default: Low/Info nitpick tail suppressed unless --profile assertive
- Surgical-changes check: every changed hunk must trace to a spec line or PR-description intent, else flagged out-of-scope
- Confidence Gate: Evidence quality and Root cause identified dimensions must each score >=70, banded to PROCEED/REVIEW/STOP mapped to DONE/NEEDS_CONTEXT/BLOCKED
- ywc-verify-done evidence-block requirement when gate band is PROCEED and status claims DONE/DONE_WITH_CONCERNS
- Step 7 learnings capture requires explicit user-confirmed CHANGESET, never an inferred silent write
- NEEDS_CONTEXT gate: ambiguous/unspecified spec or code path blocks proceeding without clarification

## Full narrative

Implementation review before a PR is exactly what ywc-impl-review is built for, so I'd invoke it. I'd start by announcing: "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."

Before doing anything else, I'd check the skill's Arguments table. --spec is required, and exactly one of --code or --git-range is required. The request as given only describes intent ("validate code matches the spec," "comprehensive review before PR") — it does not name a spec file or a code path/git range. The skill's own Completion Status table has a rule for exactly this: NEEDS_CONTEXT — "Spec and code paths are ambiguous; cannot determine what conformance means without clarification." So rather than guessing, I would stop and ask the user two concrete questions: (1) which specification document is the source of truth (e.g., a docs/outline/*.md file or a task spec under tasks/<id>/), and (2) whether to scope the review to an explicit --code path or derive it from a --git-range against the base branch — I'd propose `main..HEAD` as the likely default given the branch is `feature/skill-hell-base`, but I would confirm it rather than assume, since guessing the review scope wrong defeats the point of a spec-conformance check.

Once those two arguments were supplied, here is exactly what I'd execute:

Step 0 (Learnings): invoke `ywc-review-learnings --mode read --target <the resolved code path or changed-file set>` to pull `docs/review-learnings.md` into a compact DO/DO-NOT/FALSE-POSITIVE block. If the file doesn't exist I would not block — I'd proceed with an empty learnings set.

Step 1 (Project context): Read the root `CLAUDE.md` and `claude-code/skills/CLAUDE.md` for conventions and PR-gate conditions; check for a `package.json` (this repo is a skill/agent distribution toolkit, so I'd expect none at the target and would note that explicitly rather than assume Node conventions); Read `docs/ubiquitous-language.md` if it exists so any reviewer subagent can flag synonym drift.

Step 2 (Read spec + code): if `--git-range` was given, run `git diff --name-only <range>` (e.g. `git diff --name-only main..HEAD`) via Bash to get the changed-file list and treat that as the review target; Read the spec file in full and every target code file in full. This context stays local to me — I would not forward it wholesale into Phase 2.

Step 3 (Phase 1 — five parallel Task-tool subagent calls, each with an explicit `model:` param):
- Architecture (`model: sonnet`, `references/architecture-agent.md`) — module boundaries, dependency direction, over-abstraction, structural spec conformance; if the diff touches DB schema I'd also apply `references/schema/core.md` Part C and cross-reference cascade/tenant-scope gaps to Security as one-liners, not duplicated findings.
- Design (`model: sonnet`, `references/design-agent.md`) — API/interface design, naming, error models, contract conformance.
- Devex (`model: sonnet`, `references/devex-agent.md`) — readability, error messages, logging, docs, config UX.
- Security (`model: sonnet`, `references/security-agent.md`) — OWASP Top 10; since this repo has `claude-code/agents/`, I'd prefer `subagent_type: ywc-security-engineer` over the generic prompt.
- QA (`model: haiku`, `references/qa-agent.md`) — coverage gaps, missing test cases.

Into each prompt I'd inject the filtered Step 0 learnings, apply `--profile chill` by default (suppressing the Low/Info Style/Docs nitpick tail, never suppressing Critical/High/Medium), and require every finding to cite `file:line`, a traced symbol, or fresh command output — anything that can't be substantiated gets dropped, not hedged with "might be." I'd run any linters this repo already ships (e.g. shellcheck on `scripts/*.sh` via `scripts/validate.sh`, markdownlint) and feed their raw output to the relevant subagent as evidence, not as a verdict. I'd check whether the changed-file set is dominated by one language for the Tier-2 reviewer swap (`ywc-typescript-reviewer` / `ywc-python-reviewer` / `ywc-go-reviewer`); given this repository is primarily Markdown SKILL.md files and Bash scripts, none of the three currently-shipped Tier-2 reviewers match, so I'd keep the generic Design/Devex sonnet subagents. I'd also instruct every subagent to flag any changed hunk that doesn't trace back to the spec or stated PR intent as an out-of-scope/drive-by-refactor finding.

Step 4 (Aggregate): combine the five subagents' "Advisor candidates" lists, dedupe on shared `{file}:{line}`, cap the total at `--advisor-budget` (default 5), and if over budget prioritize Critical > High > Medium, then within a severity tier Security > Architecture > Design > Devex > QA. Anything dropped for exceeding the cap gets logged in the final report's Advisor Budget Report section, not silently discarded.

Step 5 (Phase 2 — sequential Opus advisor calls, only if `--no-advisor` was not passed): for each surviving candidate, one `model: opus` Task-tool call (or `subagent_type: ywc-architect` for Architecture-origin candidates, `ywc-performance-engineer` for performance-ambiguous ones), with a strictly bounded payload — the finding text, a ≤100-line snippet, the spec excerpt, and the category rubric only, never the full spec/file/Phase-1 transcript. Each verdict is capped at ≤200 words unless I explicitly justify an overrun in the report.

Step 6 (Merge): combine Phase 1 confirmed findings with Phase 2 verdicts, tagging each with `[P1]` or `[P2]` provenance.

Confidence Gate: before emitting, I'd score Evidence quality and Root cause identified (each must be ≥70) and map the resulting band to the Completion Status — PROCEED → DONE or DONE_WITH_CONCERNS (per the existing Critical/High count rule), REVIEW (70–89) → NEEDS_CONTEXT with the weakest dimension flagged at the top, STOP (<70) → BLOCKED with findings held back as non-authoritative. If the band lands PROCEED and I'm claiming DONE/DONE_WITH_CONCERNS, I'd attach a verification evidence block (command + output excerpt + exit code) rather than writing an unsupported "looks good."

I'd then emit the report in the skill's exact template — Summary counts per axis, per-axis finding lists with `🚨/🔴/🟡/🔵/ℹ️` severity symbols and `[P1]/[P2]` markers, Fix Priority sorted by severity, Advisor Budget Report, and the final Completion Status line.

Step 7 (Learnings capture, optional): I'd offer — not silently write — to promote any confirmed finding that recurs across files/reviews, or any finding the user dismisses as a false positive (with their stated reason), into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`, gated on the user confirming the CHANGESET.

Finally, per the skill's own Integration section, this skill's downstream is PR creation, not PR creation itself — I would stop after the report (and the Step 7 offer) and hand off to `ywc-create-pr` only if/when the user asks to open the PR; I would not create the PR as part of this review.

So concretely: my first real action here would not be any of the above execution steps — it would be pausing to ask the user for the missing `--spec` and `--code`/`--git-range` values (with a proposed `main..HEAD` default to confirm), since the skill explicitly treats an unresolved spec/code target as a NEEDS_CONTEXT condition rather than something to infer silently.
