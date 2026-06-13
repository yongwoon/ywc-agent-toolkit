---
name: ywc-impl-review
description: >-
  (ywc) Use when implementation is complete and before creating a PR, and the user wants to validate code matches the spec, check implementation quality, or run a comprehensive review. Triggers: "구현 검증", "impl review", "implementation review", "사양 적합성", "코드 리뷰", "구현 리뷰", "PR 전 검증", "check my implementation", "実装レビュー". Do not use for active code generation, for spec-only review (use ywc-spec-validate), for product/business-level review (use ywc-product-review), for capturing or reading accumulated review preferences as durable learnings (use ywc-review-learnings), or for a security-only audit of auth / external-input / sensitive-data code (use ywc-security-audit).
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
| "Surface every nitpick to be thorough" | A review that buries one real bug under ten style nits trains the reader to ignore all of them. `chill` is the default for a reason — suppress the Style/Docs/polish tail unless `--profile assertive`. Thoroughness on correctness, restraint on nitpicks. |
| "This finding is plausible, surface it with a 'might be'" | Verify-before-surface: a finding without primary evidence (file:line, traced symbol, command output) is dropped, not hedged. A hedged finding is noise that costs the reader a round-trip to disprove. |
| "There's a `docs/review-learnings.md` FALSE-POSITIVE entry but I'll flag it anyway to be safe" | A `FALSE-POSITIVE` learning carries the team's reason it is a non-issue here. Re-raising it ignores accumulated project knowledge and reintroduces the exact noise the learning was created to stop. |

**Violating the letter of these rules is violating the spirit.** Review without honest severity is theater.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--spec` | `--spec <path>` | `--spec docs/outline/02-api.md` | Specification file path (required) |
| `--code` | `--code <path>` | `--code api/src/routes/` | Code path to review (required). `--code` and `--git-range` are mutually exclusive |
| `--git-range` | `--git-range <sha>..<sha>` | `--git-range abc1234..HEAD` | Git range to derive the review target. Run `git diff --name-only <range>` to obtain the changed-file list. `--code` and `--git-range` are mutually exclusive |
| `--no-advisor` | flag | | Skip Phase 2 entirely. Use when running on throwaway or prototype code where frontier judgment on ambiguous findings is not worth the latency |
| `--profile` | `--profile chill\|assertive` | Verbosity dial (default `chill`). `chill` surfaces only correctness / security / logic / runtime-risk findings and suppresses the Style/Docs/Devex-polish nitpick tail (`Low`/`Info`); `assertive` emits those too. Critical/High/Medium are never suppressed. See [coderabbit-methodology.md §1](./references/coderabbit-methodology.md) |
| `--skip-learnings` | flag | | Skip Step 0 (loading `docs/review-learnings.md`). Use when no learnings file exists or a clean-room review is wanted |
| `--advisor-budget` | `--advisor-budget <n>` | `--advisor-budget 3` | Maximum number of Phase 2 Opus calls. Default: 5. Applies across all categories combined |
| `--format` | `--format markdown\|html` | `--format html` | Output format. Default `markdown`. With `html`, writes a self-contained HTML report to `claudedocs/`. See [html-output.md](../references/html-output.md) |

## Advisor Pattern

This skill uses **Pattern B (Two-Phase Review)** from [advisor-pattern.md](../references/advisor-pattern.md). The rationale: review findings range from mechanical (hardcoded secret, missing null check, trivial OWASP match) to genuinely ambiguous (architectural judgment call, severity debate between two OWASP categories, spec-conformance question with more than one reasonable reading). Running every reviewer on Opus wastes frontier capacity on the mechanical cases; running every reviewer on Sonnet undersells the ambiguous ones. Phase 1 handles the mechanical cases at Sonnet/Haiku cost; Phase 2 escalates only the ambiguous ones to Opus with tightly bounded context.

Budget discipline (see advisor-pattern.md §6): default cap is 5 Opus calls per invocation, shared across all categories. Use fewer when possible. Never forward full files or full project context to the Phase 2 advisor — only the finding text, a bounded snippet, and the relevant spec excerpt.

## Execution Steps

0. **Load Review Learnings** (skip if `--skip-learnings`) — Invoke `ywc-review-learnings --mode read --target <changed files / --code path>` to load the project's accumulated review preferences from `docs/review-learnings.md`. The result is a compact "Applicable Review Learnings" block: `DO` / `DO-NOT` entries become extra checks injected into the matching reviewer subagent (Step 3), and `FALSE-POSITIVE` entries tell that reviewer to **stop** raising a known non-issue. If the file is absent, proceed with an empty set — never block a review on missing learnings. This is the compounding mechanism that makes review quality rise per repository over time (see [coderabbit-methodology.md §7](./references/coderabbit-methodology.md)).

1. **Collect Project Context** — Read `CLAUDE.md`, `package.json` to identify conventions, tech stack, and PR gate conditions. If `docs/ubiquitous-language.md` exists, read it — the Reviewer subagent must flag identifiers that match a "Synonyms to Avoid" entry instead of the canonical term. Per [coderabbit-methodology.md §3](./references/coderabbit-methodology.md), treat the spec / PR description as the statement of *intent* and trace each changed symbol to its callers/callees before judging it — a locally-fine change can still break a caller's contract.

2. **Read Spec + Code** — When `--git-range` is provided instead of `--code`: run `git diff --name-only <range>` to obtain the changed-file list and treat those files as the review target. Read the specification file and all target code files. This context stays with the parent; do not forward it wholesale to Phase 2.

3. **Phase 1 — Parallel Executor Review** — Use the Task tool to spawn five subagents in parallel. Pass `model` explicitly on each call so the executor layer stays at Sonnet or Haiku cost:
   - **Architecture subagent** (`model: sonnet`) — Module boundaries, layering, structural patterns, dependency direction, simplicity / over-abstraction, structural spec conformance. Reference: `references/architecture-agent.md`. When the diff touches DB schema or migrations, also apply the shared schema review checklist ([../references/schema/core.md](../references/schema/core.md) Part C); raise cascade ↔ API status (B2) and multi-tenant scope (B6) gaps as one-line cross-references to the Security subagent rather than duplicating them.
   - **Design subagent** (`model: sonnet`) — API/interface design, naming, signatures, error models, return shapes, public-surface discipline, contract spec conformance. Reference: `references/design-agent.md`.
   - **Devex subagent** (`model: sonnet`) — Readability, error messages, logging, documentation, debuggability, config UX. The operator-experience dimension. Reference: `references/devex-agent.md`.
   - **Security subagent** (`model: sonnet`) — OWASP Top 10 analysis. Reference: `references/security-agent.md`. When the Claude Code named-agent catalog at `tools/claude-code/agents/` is installed, prefer `subagent_type: ywc-security-engineer` so the subagent carries the dedicated worker persona (`tools/claude-code/agents/ywc-security-engineer.md`).
   - **QA subagent** (`model: haiku`) — Test coverage gaps and missing test cases. Reference: `references/qa-agent.md`. Haiku is appropriate because coverage-gap detection is largely mechanical (file enumeration, assertion counting, branch enumeration) and does not typically require frontier reasoning.

   **Inject the Step 0 learnings** into each subagent prompt, filtered to that aspect's category: a `DO`/`DO-NOT` learning is an extra check; a `FALSE-POSITIVE` learning is an explicit instruction not to raise that finding here. **Apply the `--profile` dial**: in `chill` (default), a subagent suppresses its Style/Docs/Devex-polish nitpick tail (`Low`/`Info`) and surfaces only correctness/security/logic/runtime-risk findings; `assertive` emits the tail too (Critical/High/Medium are never suppressed). **Verify before surfacing** (the precision lever, [coderabbit-methodology.md §2](./references/coderabbit-methodology.md)): every finding must cite primary evidence — exact `file:line`, the symbol traced to its definition/callers, or fresh command output — and a finding that cannot be substantiated by re-reading the code or running a scoped check is **dropped**, not surfaced with a hedge. Where the project ships linters/scanners (ruff, eslint, golangci-lint, shellcheck, semgrep, gitleaks, ast-grep), run them and feed their output to the relevant subagent as *evidence* to triage — not as the verdict ([§4](./references/coderabbit-methodology.md)).

   Each subagent must return two artifacts:
   - **Confirmed findings** — issues the executor is confident about (Phase 1 complete, no escalation needed).
   - **Advisor candidates** — findings the executor flags for Phase 2 review. Each candidate must include: the finding text, a bounded code snippet (≤100 lines), the relevant spec excerpt (if any), and a one-sentence reason the executor wants a second opinion.

   Each reference file (`references/*-agent.md`) explains what "confident" vs "needs advisor" means for that category. The four code-review aspects (architecture / design / devex / security) stay in their own lanes: an Architecture finding does not include naming polish (Design) or error-message wording (Devex). Cross-aspect concerns surface as one-line cross-references, never as duplicated findings.

   **Language-specific reviewer dispatch (Tier 2)** — when the changed-file list is dominated by a single language and the Claude Code named-agent catalog at `tools/claude-code/agents/` is installed, replace the Design and Devex generic `model: sonnet` subagents with the matching language reviewer for sharper findings. Currently shipped:
   - TypeScript / TSX / Vue / Svelte → `subagent_type: ywc-typescript-reviewer` (covers type-system depth, async correctness, framework idioms, tsconfig strictness, ESM/CJS interop)
   - Python / .py / .pyi / pyproject.toml → `subagent_type: ywc-python-reviewer` (covers type-system depth, asyncio correctness, framework idioms — Django / FastAPI / Pydantic v2 / Flask, mypy strict mode, GIL implications, lifecycle patterns)
   - Go / .go / go.mod / go.sum → `subagent_type: ywc-go-reviewer` (covers goroutine lifecycle, channel patterns, interface design — accept interfaces return concrete, error wrapping `%w` / `errors.Is` / `errors.As`, pointer vs value semantics, generics post 1.18, defer + sync primitives)

   Tier 2 reviewers for other languages (Swift / Rust) are follow-up PRs; in the meantime continue with the generic Design / Devex subagent prompts for those files.

4. **Aggregate and Select Phase 2 Candidates** — Combine candidate lists from all five subagents:
   - Deduplicate findings that share `{file}:{line}` across categories.
   - Cap the total at `--advisor-budget` (default 5). If candidates exceed the cap, prioritize: Critical > High > Medium, and within the same severity prefer Security > Architecture > Design > Devex > QA. (Architecture / Design / Devex order reflects irreversibility — structural decisions are hardest to walk back, then contracts, then operator UX.)
   - Log the candidates that were dropped due to the cap in the final report so the user can see what was not escalated.

5. **Phase 2 — Advisor Pass** (skip entirely if `--no-advisor`) — For each surviving candidate, spawn a short Opus subagent via the Task tool with `model: opus`. When the candidate's source category is **Architecture** and the Claude Code named-agent catalog at `tools/claude-code/agents/` is installed, prefer `subagent_type: ywc-architect` so the advisor carries the dedicated architectural-decision persona (`tools/claude-code/agents/ywc-architect.md`). When the candidate's ambiguous axis is **performance** (latency / throughput / memory / bundle-size / Web Vitals regression on an Architecture or Devex candidate), prefer `subagent_type: ywc-performance-engineer` (`tools/claude-code/agents/ywc-performance-engineer.md`) so the advisor carries the dedicated Performance persona with concrete remediation (specific query rewrite, missing-index DDL, dynamic-import split point, Web Vitals fix path, profiler invocation recommendation). This is a routing hint — Phase 2 subagent count and budget are unchanged. Other categories use the generic `model: opus` dispatch.
   - **Context payload**: only the candidate's finding text, the bounded snippet, the spec excerpt, and the category-specific severity rubric from the matching reference file. Do **not** forward the full spec, the full file, or the Phase 1 transcripts.
   - **Expected output**: a short verdict (≤200 words) containing: confirmed severity, a one-line rationale, and either "confirmed" or "adjusted" (with the adjustment if any). The 200-word cap is tighter than [advisor-pattern.md §3](../references/advisor-pattern.md)'s observed ceiling of "typically <500 words" — 200 is an operational choice for this skill. If a genuinely complex candidate needs more room, invoke the §6 override: exceed the cap and justify the overrun in the final report's `Advisor Budget Report` section.
   - Opus calls are sequential, not parallel — each is small and fast, and sequential execution keeps the budget enforcement simple and auditable.

6. **Merge and Output Report** — Combine Phase 1 confirmed findings with Phase 2 verdicts. Mark each finding in the final report with its provenance (Phase 1 vs Phase 2) so the user can see which decisions involved frontier judgment.

7. **Capture Learnings** (skip if `--skip-learnings`) — After the report, offer to promote durable lessons into `docs/review-learnings.md` via `ywc-review-learnings --mode update --source review`: confirmed findings that **recur** (same class across files or recent reviews) become `DO`/`DO-NOT` learnings caught earlier next time, and any finding the user dismisses as a false positive becomes a `FALSE-POSITIVE` learning **with the dismissal reason**. This is what makes the next review on this repository sharper — do not write learnings without the user-confirmation CHANGESET that `ywc-review-learnings` enforces.

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

**CodeRabbit-derived methodology** — the verbosity dial (`--profile`), the verify-before-surface precision gate, the intent/context phase, static-analysis-as-evidence, and the per-project learnings loop are specified in [`references/coderabbit-methodology.md`](./references/coderabbit-methodology.md). These are the techniques imported to raise review quality toward bot-reviewer parity, in a runtime-agnostic form (no CodeRabbit dependency). The learnings half pairs with `ywc-review-learnings`, which owns `docs/review-learnings.md`.

**Recurring real-world defects catalog** — every reviewer agent additionally consults [`references/recurring-defects.md`](./references/recurring-defects.md), a derived-from-data catalog of the defect classes that production bot reviewers (CodeRabbit, Codex Review) flag most often: data-layer access-boundary (ownership / tenant isolation), data-integrity / `NULL` handling, error-swallowing, external-call resilience, validation / fail-fast, HTTP-status semantics, and test fidelity. Each agent's "High-frequency real-world checks" section points at its catalog slice. The catalog tells the reviewer *where real bugs cluster*; the per-aspect rubric still governs severity and escalation. This is the same surface the executors' `--review` flag targets, so these classes get caught before the PR opens — reducing bot-review round-trips after the PR is created.

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
- **pairs with**: `ywc-review-learnings` — loaded in Step 0 (`read`) to apply accumulated review preferences and called in Step 7 (`update --source review`) to capture new ones; `docs/review-learnings.md` is the per-project memory that compounds review quality
- **pattern source**: [`references/advisor-pattern.md`](../references/advisor-pattern.md), [`references/coderabbit-methodology.md`](./references/coderabbit-methodology.md)
