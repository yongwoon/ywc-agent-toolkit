---
name: ywc-impl-review
version: 1.0.0
description: >-
  (ywc) Use after implementation is complete and before creating a PR, when the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review. Triggers: "구현 검증", "impl review", "implementation review", "사양 적합성", "코드 리뷰", "구현 리뷰", "PR 전 검증", "check my implementation", "実装レビュー". Do not use during active code generation, for spec-only review (use ywc-spec-validate), or for product/business-level review (use ywc-product-review).
category: review
phase: quality
requires: []
advisor_budget: 5
---

# ywc-impl-review

**Announce at start:** "I'm using the ywc-impl-review skill to run a five-axis (architecture / design / devex / security / QA) implementation review."

Implementation conformance review skill. Runs five parallel reviewers (Phase 1: 4 Sonnet + 1 Haiku) and escalates only ambiguous findings to a short Opus advisor pass (Phase 2). The four code-review aspects (architecture / design / devex / security) follow the gstack review-army pattern; QA stays as a separate axis because coverage analysis is mechanical and benefits from a lighter model. See [Advisor Pattern](../references/advisor-pattern.md) for why this shape is used.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Phase 1 had no findings, the spec is satisfied" | Absence of findings ≠ proof of conformance. State what was checked, not what was missing. |
| "This finding looks ambiguous, send it all to Opus" | Phase 2 budget is 5. Reserve for genuinely ambiguous cases — not first-pass uncertainty. |
| "Forwarding the full spec gives Opus better context" | Never forward full files or full project context. Only the finding text + bounded snippet + spec excerpt. |
| "Severity feels somewhere between High and Medium" | Pick based on impact, not feeling. If truly between, that is a Phase 2 candidate. |
| "`--no-advisor` saves time on this review" | Skip Phase 2 only on throwaway/prototype code. Production review needs ambiguity escalation. |
| "Reviewer agents agree, so the finding is correct" | Three Sonnet agents drawing the same wrong conclusion is still wrong. Escalate when stakes are high. |
| "User wants a quick review, severity ratings are optional" | Without severity, the user cannot triage. Always rate Critical / High / Medium / Low. |

**Violating the letter of these rules is violating the spirit.** Review without honest severity is theater.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--spec` | `--spec <path>` | `--spec docs/outline/02-api.md` | Specification file path (required) |
| `--code` | `--code <path>` | `--code api/src/routes/` | Code path to review (required). `--code` and `--git-range` are mutually exclusive |
| `--git-range` | `--git-range <sha>..<sha>` | `--git-range abc1234..HEAD` | Git range to derive the review target. Run `git diff --name-only <range>` to obtain the changed-file list. `--code` and `--git-range` are mutually exclusive |
| `--no-advisor` | flag | | Skip Phase 2 entirely. Use when running on throwaway or prototype code where frontier judgment on ambiguous findings is not worth the latency |
| `--advisor-budget` | `--advisor-budget <n>` | `--advisor-budget 3` | Maximum number of Phase 2 Opus calls. Default: 5. Applies across all categories combined |
| `--format` | `--format markdown\|html` | `--format html` | Output format. Default `markdown`. With `html`, writes a self-contained HTML report to `claudedocs/`. See [html-output.md](../references/html-output.md) |

## Advisor Pattern

This skill uses **Pattern B (Two-Phase Review)** from [advisor-pattern.md](../references/advisor-pattern.md). The rationale: review findings range from mechanical (hardcoded secret, missing null check, trivial OWASP match) to genuinely ambiguous (architectural judgment call, severity debate between two OWASP categories, spec-conformance question with more than one reasonable reading). Running every reviewer on Opus wastes frontier capacity on the mechanical cases; running every reviewer on Sonnet undersells the ambiguous ones. Phase 1 handles the mechanical cases at Sonnet/Haiku cost; Phase 2 escalates only the ambiguous ones to Opus with tightly bounded context.

Budget discipline (see advisor-pattern.md §6): default cap is 5 Opus calls per invocation, shared across all categories. Use fewer when possible. Never forward full files or full project context to the Phase 2 advisor — only the finding text, a bounded snippet, and the relevant spec excerpt.

## Execution Steps

1. **Collect Project Context** — Read `CLAUDE.md`, `package.json` to identify conventions, tech stack, and PR gate conditions. If `docs/ubiquitous-language.md` exists, read it — the Reviewer subagent must flag identifiers that match a "Synonyms to Avoid" entry instead of the canonical term.

2. **Read Spec + Code** — When `--git-range` is provided instead of `--code`: run `git diff --name-only <range>` to obtain the changed-file list and treat those files as the review target. Read the specification file and all target code files. This context stays with the parent; do not forward it wholesale to Phase 2.

3. **Phase 1 — Parallel Executor Review** — Use the Task tool to spawn five subagents in parallel. Pass `model` explicitly on each call so the executor layer stays at Sonnet or Haiku cost:
   - **Architecture subagent** (`model: sonnet`) — Module boundaries, layering, structural patterns, dependency direction, simplicity / over-abstraction, structural spec conformance. Reference: `references/architecture-agent.md`.
   - **Design subagent** (`model: sonnet`) — API/interface design, naming, signatures, error models, return shapes, public-surface discipline, contract spec conformance. Reference: `references/design-agent.md`.
   - **Devex subagent** (`model: sonnet`) — Readability, error messages, logging, documentation, debuggability, config UX. The operator-experience dimension. Reference: `references/devex-agent.md`.
   - **Security subagent** (`model: sonnet`) — OWASP Top 10 analysis. Reference: `references/security-agent.md`.
   - **QA subagent** (`model: haiku`) — Test coverage gaps and missing test cases. Reference: `references/qa-agent.md`. Haiku is appropriate because coverage-gap detection is largely mechanical (file enumeration, assertion counting, branch enumeration) and does not typically require frontier reasoning.

   Each subagent must return two artifacts:
   - **Confirmed findings** — issues the executor is confident about (Phase 1 complete, no escalation needed).
   - **Advisor candidates** — findings the executor flags for Phase 2 review. Each candidate must include: the finding text, a bounded code snippet (≤100 lines), the relevant spec excerpt (if any), and a one-sentence reason the executor wants a second opinion.

   Each reference file (`references/*-agent.md`) explains what "confident" vs "needs advisor" means for that category. The four code-review aspects (architecture / design / devex / security) stay in their own lanes: an Architecture finding does not include naming polish (Design) or error-message wording (Devex). Cross-aspect concerns surface as one-line cross-references, never as duplicated findings.

4. **Aggregate and Select Phase 2 Candidates** — Combine candidate lists from all five subagents:
   - Deduplicate findings that share `{file}:{line}` across categories.
   - Cap the total at `--advisor-budget` (default 5). If candidates exceed the cap, prioritize: Critical > High > Medium, and within the same severity prefer Security > Architecture > Design > Devex > QA. (Architecture / Design / Devex order reflects irreversibility — structural decisions are hardest to walk back, then contracts, then operator UX.)
   - Log the candidates that were dropped due to the cap in the final report so the user can see what was not escalated.

5. **Phase 2 — Advisor Pass** (skip entirely if `--no-advisor`) — For each surviving candidate, spawn a short Opus subagent via the Task tool with `model: opus`:
   - **Context payload**: only the candidate's finding text, the bounded snippet, the spec excerpt, and the category-specific severity rubric from the matching reference file. Do **not** forward the full spec, the full file, or the Phase 1 transcripts.
   - **Expected output**: a short verdict (≤200 words) containing: confirmed severity, a one-line rationale, and either "confirmed" or "adjusted" (with the adjustment if any). The 200-word cap is tighter than [advisor-pattern.md §3](../references/advisor-pattern.md)'s observed ceiling of "typically <500 words" — 200 is an operational choice for this skill. If a genuinely complex candidate needs more room, invoke the §6 override: exceed the cap and justify the overrun in the final report's `Advisor Budget Report` section.
   - Opus calls are sequential, not parallel — each is small and fast, and sequential execution keeps the budget enforcement simple and auditable.

6. **Merge and Output Report** — Combine Phase 1 confirmed findings with Phase 2 verdicts. Mark each finding in the final report with its provenance (Phase 1 vs Phase 2) so the user can see which decisions involved frontier judgment.

## Output Format

```text
## Implementation Review Result: {spec} vs {code}

### Summary
- Phase 1 findings (Sonnet/Haiku executor): Architecture A, Design D, Devex V, Security M, QA K
- Phase 2 advisor calls (Opus): X of Y budget used
- Phase 2 adjustments: N confirmed as-is, M severity-adjusted

### Architecture
1. [severity] [P1|P2] {file}:{line} — Description
   (if P2) Advisor verdict: {one-line rationale}

### Design
1. [severity] [P1|P2] {file}:{line} — Description
   (if P2) Advisor verdict: {one-line rationale}

### Developer Experience (Devex)
1. [severity] [P1|P2] {file}:{line} — Description
   (if P2) Advisor verdict: {one-line rationale}

### Security
1. [severity] [P1|P2] {file}:{line} — Description
   (if P2) Advisor verdict: {one-line rationale}

### Testing (QA)
1. [severity] [P1|P2] — Description
   (if P2) Advisor verdict: {one-line rationale}

### Fix Priority
1. (Sorted by Critical first, with [P1|P2] markers preserved)

### Advisor Budget Report
- Used: X of Y calls
- Dropped (over budget): {list, if any}

### Completion Status
(One of: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT)
```

**Reporting Symbols**: Replace the bracketed `[severity]` placeholder above with the corresponding symbol from [symbols.md](../references/symbols.md). Severity vocabulary is shared across all `ywc-*` review skills — use the same symbol for the same tier.

| Symbol | Severity | Replaces |
|--------|----------|----------|
| `🚨` | Critical | `[Critical]` |
| `🔴` | High | `[High]` |
| `🟡` | Medium | `[Medium]` |
| `🔵` | Low | `[Low]` |
| `ℹ️` | Info | `[Info]` |

Example finding line:

```
🚨 [P2] src/api/users.ts:42 — SQL injection: input concatenated into query.
   Advisor verdict: confirm Critical; remediation requires parameterization.
```

The `[P1]` / `[P2]` marker is preserved unchanged — it describes Phase 1 vs Phase 2 escalation history, while the severity symbol describes finding impact. Both pieces of information are needed; do not collapse them.

For the Confidence Gate score in the report header, use the band marker from [symbols.md](../references/symbols.md): `✅` for PROCEED, `⚠️` for REVIEW, `❌` for STOP.

**Completion Status rules:**

| Status | When to use |
|--------|------------|
| `DONE` | Review complete, no Critical or High findings |
| `DONE_WITH_CONCERNS` | Review complete but Critical/High findings were identified — the report details them; human action required before merging |
| `BLOCKED` | Review cannot proceed — spec file missing, code unreadable, or a Phase 2 escalation returned an inconclusive verdict |
| `NEEDS_CONTEXT` | Spec and code paths are ambiguous; cannot determine what conformance means without clarification |

`[P1]` marks findings confirmed entirely by the Phase 1 executor. `[P2]` marks findings that went through the Phase 2 advisor. This distinction matters when the user calibrates trust in the output — Phase 2 items represent the decisions the executor deemed genuinely ambiguous.

> **HTML mode (`--format html`)** — emits the same findings as a self-contained HTML report: severity color coding, tab navigation, and a `Copy as Markdown` button. Structure and conventions follow [html-output.md](../references/html-output.md). The Markdown surface is preserved inside the file, so downstream integration is unaffected.

## Agent Prompt References

Read the corresponding reference file when spawning each subagent and include the relevant section in the subagent prompt. The reference files describe both the standard review dimensions **and** the "advisor candidate" criteria specific to each category:

- `references/architecture-agent.md` — Architecture's review dimensions (structural spec conformance, pattern consistency, module interface, simplicity, surgical changes) + advisor triggers
- `references/design-agent.md` — Design's review dimensions (contract spec conformance, naming, signatures, error model, return shapes, public-surface discipline) + advisor triggers
- `references/devex-agent.md` — Devex's review dimensions (readability, error messages, logging, documentation, debuggability, config UX) + advisor triggers
- `references/security-agent.md` — Security's OWASP Top 10 checklist and advisor-escalation triggers
- `references/qa-agent.md` — QA's coverage analysis and advisor-escalation triggers

If a reference file does not yet contain an "Advisor Candidate Criteria" section, fall back to the three-property test in [advisor-pattern.md §5](../references/advisor-pattern.md): objective trigger, irreversibility, ambiguity. A finding must satisfy all three to be a Phase 2 candidate.

## Confidence Gate

This skill applies the [Confidence Gate](../references/confidence-gate.md) to the aggregated review output before emitting the final report. The gate sits between Phase 2 advisor consolidation and report emission.

In addition, when the report's gate band lands in **PROCEED** and findings include a `DONE` (or `DONE_WITH_CONCERNS`) completion claim against the implementation, the surface must follow `ywc-verify-done`: the verification block (command, output excerpt, exit code) appears before the status line, no `should` / `probably` / `seems` wording appears in the conclusion, and any "this finding's fix was verified" claim cites the fresh command output that proves it. A report that reads "all clear, looks good" without an evidence block is not a Confidence-Gate PROCEED — downgrade to REVIEW until the evidence is attached.

**Required dimensions** (must each score ≥ 70):

- **Evidence quality** — Every finding must cite a verified source: file path, line number, or test output. Findings phrased as "this *might* be wrong" without primary evidence reduce the score even if the finding itself is plausible.
- **Root cause identified** — A finding that names only the symptom ("test fails") without identifying the underlying cause ("test fixture is shared across cases") cannot be remediated correctly. The reviewer must reach root cause before recording the finding.

**Band-to-status mapping** for this skill:

| Gate band | Completion status | Action |
|-----------|-------------------|--------|
| PROCEED (≥ 90) | DONE or DONE_WITH_CONCERNS | Emit the report; status follows from the existing Critical/High count rule. |
| REVIEW (70 – 89) | NEEDS_CONTEXT | Emit the report with the gate score and weakest dimension flagged at the top. Reviewer judgment required before merge. |
| STOP (< 70) | BLOCKED | Do not emit findings as authoritative. Report which dimensions failed and what additional Phase 2 advisor calls would be needed to raise the score. |

The gate score must appear in the report header. Per-finding `[P1]` / `[P2]` markers remain unchanged — they describe escalation history, while the gate describes overall report confidence.

## Integration

- **upstream**: `ywc-sequential-executor` or `ywc-parallel-executor` (auto-invoked via `--review` flag)
- **downstream**: PR creation
- **pattern source**: [`references/advisor-pattern.md`](../references/advisor-pattern.md)
