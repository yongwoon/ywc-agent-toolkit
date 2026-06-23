---
name: ywc-tech-research
version: 1.0.0
description: (ywc) Use when comparing libraries, investigating implementation approaches, evaluating technology options, or gathering best practices before writing specifications. Triggers: "기술 조사", "라이브러리 비교", "research", "investigate", "compare options", "어떤 걸 쓸까", "best way to implement", "技術調査", "ライブラリ比較", "ywc-tech-research". Do not use for spec writing (output goes to ywc-spec-validate), code generation (use ywc-code-gen), or simple documentation lookup that does not require comparison/evaluation.
category: spec
phase: planning
requires: []
advisor_budget: 2
---

# ywc-tech-research

**Announce at start:** "I'm using the ywc-tech-research skill to investigate options and produce a structured comparison."

Research Agent Skill for technical investigation and library comparison.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "I know the answer from training data, no need to look up docs" | Training data lags. Use Context7 / WebFetch for up-to-date sources. |
| "One option clearly wins, skip the comparison table" | The user requested research. Always show the trade-off matrix, even if the recommendation is decisive. |
| "Existing project stack constraints are obvious" | Compatibility with the project's existing stack is the hardest dimension to recover later. Always read package.json / pyproject.toml first. |
| "Cite from memory, citation links optional" | Every claim needs a source link or version-specific reference. Unsourced claims are not research. |
| "Combine pros/cons into one paragraph" | Use a structured trade-off matrix. Mixed prose hides the comparison. |
| "Recommend without flagging unknowns" | If a dimension is unverified (e.g., long-term maintenance, license edge cases), explicitly state it as a gap. |
| "Topic is clear enough — skip the scope questions and start searching" | Reversibility and success criteria decide *how deep* to research and what "winning" even means. Researching without them produces a comparison the user cannot act on, and over-researches a reversible one-off. Run the one consolidated clarify round in Step 1.5, then proceed. |
| "Just use the default `--depth 50` for everything" | A reversible single-library lookup wastes tokens at depth 50; an irreversible architecture decision is under-served by it. Classify complexity in Step 1.5 and set the matching default depth — an explicit `--depth` argument still overrides. |

**Violating the letter of these rules is violating the spirit.** Research without verifiable sources is opinion.

## Arguments

Parse `$ARGUMENTS` for:

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| Topic | free text | `"Hono SSE implementation"` | Research topic (required) |
| `--compare` | `--compare "A,B"` | `--compare "Redis,Valkey"` | Comma-separated list of options to compare in parallel |
| `--depth` | `--depth 25\|50\|75\|100` | `--depth 50` | Output depth level (default: 50). 25=summary-only; 50=standard; 75=detailed with evidence; 100=exhaustive with full source excerpts and gap analysis |
| `--format` | `--format markdown\|html` | `--format html` | Output format. Default `markdown`. With `html`, writes a self-contained HTML report to `claudedocs/`. See [html-output.md](../references/html-output.md) |

## Execution Steps

1. **Collect Project Context** — Read `CLAUDE.md`, `package.json`, and directory structure to identify the current tech stack and any constraints (runtime, license, bundle size).

1.5. **Scope & Complexity Assessment** — Before gathering sources, settle scope and right-size the effort. This is the "Right Job, Right Tool" gate: it prevents wasted depth on a trivial lookup and prevents shallow research on an irreversible decision.

   **Clarify (one consolidated round, only for items the topic/context leaves open)** — ask once, then proceed; never invent an answer:
   - **Reversibility** — can this choice be changed later, or does it lock in a dependency, data format, or contract?
   - **Success criteria** — what measurable property decides the winner (latency budget, bundle-size ceiling, license class, throughput)?
   - **Out-of-scope** — which dimensions are explicitly *not* factors (e.g., "cost is irrelevant", "must be permissive-licensed")?

   **Classify complexity → set the default `--depth`** (an explicit `--depth` argument always overrides this default):

   | Class | Signal | Default `--depth` |
   |-------|--------|-------------------|
   | Simple | Single library, known-good pattern, reversible | 25 |
   | Standard | 2–3 mature options compared, reversible | 50 |
   | Complex | Architecture decision spanning concerns, version-specific behavior, or irreversible | 75–100 |

2. **Plan Research Strategy** — Determine approach based on topic characteristics:
   - Library comparison → official docs + package registry stats + GitHub activity
   - Implementation approach → official docs + code examples + existing project patterns
   - Architecture decision → technical blogs + comparable case studies + trade-off analysis

3. **Gather Information** — Use sources in this priority order:

   **Step 3a — context7 MCP (required, not optional)**

   Always query context7 before any web search. context7 returns curated, version-pinned documentation that training data cannot guarantee. Skip context7 only if it explicitly returns no results for the topic — in that case, note the fallback in the References section.

   ```
   mcp__context7__resolve-library-id(libraryName: "<library>")
   mcp__context7__query-docs(context7CompatibleLibraryID: "<id>", topic: "<topic>")
   ```

   **Step 3b — Official documentation and package registries**

   Supplement context7 with direct official docs. For any source, check the last-updated date:
   - Prefer documentation updated within the last 12 months
   - Flag sources older than 2 years as `[potentially stale]` in the References section
   - Distinguish official docs from community resources (Stack Overflow, blogs) — present them separately

   **Step 3c — `--compare` parallel mode**

   When `--compare "A,B[,C...]"` is specified, spawn one research subagent per option in parallel via the Task tool, each with the same project context and quality criteria. Collect all results before synthesizing — do not synthesize from partial results.

4. **Verify Source Recency** — Before writing the report, confirm:
   - At least one official source per option was found
   - Each official source has a visible last-updated date or release version
   - If only community sources are available, state this explicitly in the report

5. **Analyze and Output Report** — Write a structured report focused on compatibility with the current project stack.

## Source Discipline Rules

These rules apply to every claim in the report, regardless of `--depth` level. They exist to prevent confident-sounding hallucination from polluting technical decisions.

1. **Every factual claim must cite a source** — write `[source: <url or "context7">]` inline after the claim. If no source was found, write `[source: NOT FOUND — inference only]`.
2. **Distinguish fact from inference** — prefix inferred claims with `[INFERRED]`. Inferences are acceptable, but must be labeled so readers can weigh them appropriately.
3. **Cross-reference single-source claims** — any claim with only one source and high decision impact (e.g., "library X has known security issues") must be confirmed with a second source before being reported as fact. If a second source cannot be found, label it `[SINGLE SOURCE — verify before acting]`.
4. **Prefer sources ≤12 months old** — sources older than 12 months must be flagged with `[potentially stale: <date>]`. Sources older than 2 years should not be cited without an explicit caveat.
5. **Acknowledge gaps explicitly** — if a required Quality Criteria axis cannot be sourced, write the full `N/A — no data found` entry. Never omit a row silently.
6. **No gap-filling from training data alone** — Claude's internal knowledge may be used to explain concepts, but version numbers, benchmark figures, and security advisories must come from a verifiable external source fetched in this session.

## Research Quality Criteria

Every option in a comparative analysis must be assessed on all axes below. If data for an axis is unavailable, write `N/A — no data found` rather than omitting the row.

| Axis | What to Check | Verification Method |
|------|---------------|---------------------|
| Functional Fit | Does it meet the stated requirements? | Feature matrix against requirements |
| Ecosystem Health | Maintenance status, release cadence, open issue count | GitHub Insights, npm/PyPI stats |
| Learning Curve | Adoption cost relative to the team's current stack | Migration guide existence, API similarity |
| Performance | Throughput, latency, or bundle size vs. alternatives | Official benchmarks or community benchmark links |
| License | Commercial use restrictions, copyleft implications | SPDX identifier from package registry |
| Source Recency | Age of official documentation | Last-updated date or latest release tag |

## Output Format

Output depth is controlled by `--depth` (default: 50):

| Level | Label | Contents |
|-------|-------|----------|
| 25 | Essential | Summary + Recommendation only. No comparison table, no references section. |
| 50 | Standard | Full report below. References section with top 3 sources per option. |
| 75 | Detailed | Full report + per-claim `[source: …]` inline citations + `[INFERRED]` labels throughout. |
| 100 | Exhaustive | Everything in 75 + direct source excerpts (≤3 sentences each) + explicit gap analysis listing every claim that could not be sourced. |

```text
## Research Result: {topic}

### Summary
(1-2 sentence key conclusion. Inferences labeled [INFERRED].)

### Comparative Analysis
| Option | Pros | Cons | Ecosystem Health | License | Source Age | Fit |
|--------|------|------|-----------------|---------|------------|-----|
(At --depth 75/100: each cell's key claim includes inline [source: …] citation)

### Recommended Approach
(Recommendation with rationale, citing specific axes from the table above.
 Any inference prefixed with [INFERRED]. Any single-source claim marked [SINGLE SOURCE — verify before acting].)

### Project-Specific Considerations
(Compatibility with current stack, migration cost, known conflicts)

### References
- [Official] {name} — {url} (last updated: {date})
- [Community] {name} — {url} (flagged [potentially stale: <date>] if >12 months old)
- [context7] used: yes/no — if no, state the reason

### Completion Status
(One of: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT)
```

**Completion Status rules:**

| Status | When to use |
|--------|------------|
| `DONE` | All axes covered with official sources, recommendation is clear |
| `DONE_WITH_CONCERNS` | Research complete but with caveats — stale sources, missing benchmark data, or a recommendation that depends on unstated requirements |
| `BLOCKED` | Cannot research the topic — context7 returned nothing and no official docs are publicly accessible |
| `NEEDS_CONTEXT` | Topic is too vague to produce a useful recommendation without clarification from the user |

> **HTML mode (`--format html`)** — emits the same report as a self-contained HTML file: the comparative analysis rendered as a side-by-side option grid, tab navigation, and a `Copy as Markdown` button. Structure and conventions follow [html-output.md](../references/html-output.md). The Markdown surface is preserved inside the file, so downstream integration is unaffected.

## Integration

- **upstream**: None (standalone execution)
- **downstream**: Used as reference material when writing specifications or as input to `ywc-task-generator`
