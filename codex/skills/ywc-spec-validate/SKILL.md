---
name: ywc-spec-validate
description: (ywc) Use after writing a specification and before task decomposition, when the user wants to validate spec completeness, consistency, feasibility, or readiness for implementation. Triggers: "사양 검토", "spec review", "사양 리뷰", "review specification", "스펙 점검", "check the spec", "is this spec complete", "仕様レビュー". Do not use for code-level review (use ywc-impl-review), product/business review (use ywc-product-review), or when no specification document exists yet.
---

# ywc-spec-validate

**Announce at start:** "I'm using the ywc-spec-validate skill to validate specification completeness, consistency, and feasibility."

Spec Reviewer Agent Skill for specification quality validation.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Spec is mostly clear, no need to assess Feasibility" | Feasibility and Code Compatibility require project context. Always read the project instruction files (`AGENTS.md` / `CODEX.md` / `CLAUDE.md` where present), package metadata, and existing code first. |
| "Spec gaps are obvious, just list them and finish" | Each gap must specify which dimension (completeness / consistency / feasibility / compatibility) and propose a concrete clarifying question. |
| "User wrote the spec, do not push back too hard" | Honest review prevents implementation rework. Soften tone, never soften findings. |
| "Spec uses internal jargon, infer the intent" | If a term is undefined, that is a completeness gap. Flag it. |
| "Architecture decision is implicit, do not flag it" | Implicit ≠ specified. Surface implicit assumptions for explicit confirmation. |
| "The spec contradicts project instructions, follow the spec" | Surface the conflict. Do not silently let the spec override project rules. Prefer Codex-native instructions (`AGENTS.md` / `CODEX.md`) over Claude-only guidance when they conflict. |
| "4-dimension review is fast enough sequentially" | Phase 1 fan-out cuts latency on large specs; each Codex worker handles one dimension, reducing per-call context and preventing cross-dimension finding contamination. |

**Violating the letter of these rules is violating the spirit.** A spec review that finds nothing is not a review.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--spec` | `--spec <path>` | `--spec docs/outline/02-api.md` | Specification file path (required) |
| `--mode` | `--mode standard\|socratic` | `--mode socratic` | Output style. `standard` (default) returns the finding report and gate verdict; `socratic` returns learning questions instead. See [references/socratic-mode.md](references/socratic-mode.md). |
| `--focus` | `--focus <area>` | `--focus architecture` | Optional focus hint. When Council Escalation triggers, the generic 4 voices are replaced with domain expert profiles for the chosen area. Valid: `requirements`, `architecture`, `testing`, `compliance`. See [references/expert-profiles.md](references/expert-profiles.md). |

## Execution Steps

1. **Collect Project Context** — Read the following before touching the spec file. The Feasibility and Code Compatibility dimensions cannot be assessed without this context:
   - `AGENTS.md`, `CODEX.md`, and `CLAUDE.md` where present (nearest file first) — language/framework constraints, commit conventions, any explicit out-of-scope rules. Prefer Codex-native instructions (`AGENTS.md` / `CODEX.md`) over Claude-only guidance when they conflict.
   - `package.json` / `pyproject.toml` / `go.mod` — runtime, major dependencies, and their versions
   - Top-level directory structure — identify where DB schemas, API routes, and type definitions live (e.g., `src/`, `app/`, `prisma/`, `migrations/`)
   - `docs/ubiquitous-language.md` (if it exists) — canonical domain terms and their "Synonyms to Avoid"; any spec term matching a Synonyms entry is a Consistency finding
   - Extract and keep: runtime, primary framework, DB type, ORM, existing API pattern (REST / GraphQL / RPC)

   If project instruction files and package metadata are absent, note "project context unavailable" and flag all Feasibility findings as lower-confidence.

2. **Read Specification File** — Confirm the `--spec` path exists before reading. If the file does not exist, stop immediately with `BLOCKED` status and report the missing path.

3. **Check Code Compatibility** — Use repository search (`rg` preferred; fall back to `grep`/`find` only when needed) to locate related DB schemas, API routes, and type definitions that may conflict with the spec. Scope the search to the directories identified in Step 1.

   - **Step 3.5 — Precedent-Completeness Re-grounding (MANDATORY omission check; distinct from the conflict check in Step 3).** Step 3 / Code Compatibility detect where a spec *claim* conflicts with code. They structurally cannot detect an *omission*: an existing integration site the spec never names makes no claim, so nothing conflicts — yet a dropped integration site silently breaks the feature on the un-modeled runtime path while every written claim still validates cleanly. (This is the failure class that survives repeated spec-validation; re-reading spec text can never reveal a site the text never names.)

     For **every** existing pattern the spec mirrors / follows / 踏襲 / extends (a **named precedent X**), you MUST build a **Precedent Site Coverage table** before writing the report — do not reason about it in prose, build the table:

     1. Search X's own identifier(s)/marker(s) across the actual code: `rg -n "<precedentFn>|<precedentMarker>" <src> --glob '!**/*.test.*' --glob '!**/*.spec.*' --glob '!**/__tests__/**'` (exclude test files; use `grep -rn` only if `rg` is unavailable). Integration patterns (snippet/script injection, hooks, interceptors, lifecycle handlers) routinely span a **generation** step, a **preview/transform** step, **and** a **publish/render-time** step — enumerate all of them; the publish/render-time site is the one a memory-driven spec most often drops.
     2. Emit one row **per site X integrates at**:

        | Precedent site (`file:line` + what runs there) | Spec coverage: Replicated / Deferred-with-reason / **OMITTED** |

     3. Every search hit MUST appear as a row. Decide each row's coverage by searching the spec for *that specific site* — never by trusting the spec's own prose summary that it "follows X".
     4. **Every row marked OMITTED is its own Completeness Critical.** Do not fold multiple omitted sites into one finding, and **do not let a louder conflict elsewhere (e.g. a stale-anchor or deprecated-path finding) substitute for explicitly naming the omitted site** — an omission and a conflict are different defects and both must be reported. Each OMITTED Critical names the omitted site's `file:line` and the runtime path on which the feature fails.

     Include the coverage table in the report, and feed each OMITTED row into the Completeness dimension of Phase 1 as a separate Critical. If no named precedent exists, still include the table with a single `(No named precedent identified)` row so downstream readers know the omission check was performed.

4. **Phase 1 — Parallel Dimension Review** — Use Codex subagent delegation when the current session exposes a delegation tool to run 4 workers in parallel, one per review dimension. If no delegation tool is available, run the same four dimension passes inline and record the fallback in the report. Do not use Claude Code-only `Task(...)` fields, `subagent_type`, or explicit Claude model pins in the Codex bundle. Pass each worker the project context from Step 1, the spec text from Step 2, and any Step 3.5 coverage rows relevant to its dimension:

   | Worker | Dimension | Focus |
   |---|---|---|
   | Completeness | Completeness | Missing required items, edge cases, pagination, Step 3.5 OMITTED rows |
   | Consistency | Consistency | Terminology mismatches; Synonyms-to-Avoid violations |
   | Feasibility | Feasibility | Implementable with current stack and dependencies |
   | Code Compatibility | Code Compatibility | Conflicts with existing schema, API routes, type definitions |

   Each worker returns:
   - **Confirmed findings** — dimension label, severity (Critical / Warning / Suggestion), file:line, description, improvement
   - **Advisor candidates** — findings where two reasonable interpretations exist (include the specific choice and its consequence, ≤100 lines per candidate)

   **Step 4b — Aggregate**: Combine and deduplicate findings by `{file}:{line}`. Cap advisor candidates at `advisor_budget` (default: 2), prioritizing Critical over Warning. Log any dropped candidates in the report.

   The 4-dimension analysis runs the same way regardless of `--mode`; the mode only changes how findings are presented in step 5.

5. **Output Report — Branch on `--mode`**
   - `standard` (default): emit the severity-classified finding report in the format below.
   - `socratic`: emit a learning-question list per [references/socratic-mode.md](references/socratic-mode.md). Findings still drive question selection — they are just reshaped from "fix X" into "what would happen if X?". Completion Status is `SOCRATIC` and the gate score is informational only.

## Review Dimensions

| Dimension | Review Focus |
|-----------|-------------|
| Completeness | Missing required items (error handling, edge cases, pagination, etc.) |
| Consistency | Terminology, format, or data structure mismatches across documents; spec terms appearing in the "Synonyms to Avoid" column of `docs/ubiquitous-language.md` |
| Feasibility | Whether the spec can be implemented with the current stack |
| Code Compatibility | Conflicts with existing DB schema, API route patterns |

## Output Format

```text
## Spec Review Result: {filename}

### Summary
- Critical: N, Warning: M, Suggestion: K
- Phase 2 advisor calls used: X of 2 ({single-advisor|council|none})

### Precedent Site Coverage
| Precedent site (`file:line` + what runs there) | Spec coverage: Replicated / Deferred-with-reason / OMITTED |
|---|---|
| ... | ... |

### Critical Issues
1. [{file}:{line}] [P1|P2] Description — Suggested improvement
   (if P2) Advisor rationale: {one-line rationale}

### Warning Issues
1. [{file}:{line}] [P1|P2] Description — Suggested improvement

### Suggestions
1. [{file}:{line}] Description — Suggested improvement

### Completion Status
(One of: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT)
```

**Completion Status rules:**

| Status | When to use |
|--------|------------|
| `DONE` | Review complete, no Critical findings |
| `DONE_WITH_CONCERNS` | Review complete but Critical issues were found — the spec needs revision before task decomposition |
| `BLOCKED` | Review cannot proceed — spec file missing, or a Phase 2 advisor returned an inconclusive verdict |
| `NEEDS_CONTEXT` | `--spec` argument is missing or the file is empty/unreadable |
| `SOCRATIC` | `--mode socratic` was used; output is a learning-question list, not a gate verdict. Downstream skills (especially `ywc-task-generator`) must not consume this status as a handoff signal. |

**Re-plan handoff on `DONE_WITH_CONCERNS`** — after printing the report body, append the following one-liner so the user (or an interactive orchestrator) can resolve findings via `ywc-plan` Re-plan Mode instead of rewriting the spec from scratch:

```
To address the Critical findings above without losing validated sections, run:
/ywc-plan --update-spec <spec-path> --failure-context "<one-paragraph summary of the Critical findings>"
```

This routes findings into the `## Iteration N Amendments` append flow described in `ywc-plan` Step 4c, preserving validated portions of the spec. Print this line only on `DONE_WITH_CONCERNS` — `DONE`, `BLOCKED`, `NEEDS_CONTEXT`, and `SOCRATIC` do not benefit from Re-plan Mode. For programmatic consumers (e.g., `ywc-agentic`), the Programmatic Consumer Policy below already invokes the equivalent flow; this surface is for interactive users who would otherwise re-write from scratch.

## Advisor Escalation Policy

This skill runs Phase 1 as 4 parallel Codex workers (one per dimension) when delegation is available, then aggregates their findings. For a small number of **genuinely ambiguous** findings from Phase 1, request a short higher-capability advisor pass with a bounded payload. If delegation is unavailable, run the advisor checklist inline as a separate bounded pass and record the fallback in the report. This follows **Pattern B** from [advisor-pattern.md](../references/advisor-pattern.md) — parallel executors in Phase 1, frontier judgment applied only where it actually matters in Phase 2.

**Budget**: up to 2 high-capability advisor calls per invocation. Unused budget is good. Spec review is smaller in scope than impl-review, so the cap is tighter.

**Escalation conditions** — each must satisfy all three properties from [advisor-pattern.md §5](../references/advisor-pattern.md) (objective trigger, irreversibility, ambiguity):

1. **Feasibility uncertainty** — The spec appears feasible but hinges on an assumption about an undocumented library feature, version-specific behavior, or performance characteristic. A wrong assumption would make the spec unimplementable or force mid-implementation scope cuts.
2. **Code Compatibility conflict with plausible-either-way resolution** — The spec conflicts with existing code (schema, API contract, or type definition), and both "spec adapts to code" and "code refactors to spec" have plausible precedent in the project. The advisor picks which side moves.
3. **Completeness borderline** — The spec omits a feature that could be intentional (out of scope, deferred to another spec) or an oversight. The wrong verdict delays implementation (if flagged as gap when actually out of scope) or generates incorrect downstream tasks (if dismissed when actually a gap).
4. **Cross-document consistency conflict** — The spec conflicts with another spec or architecture document in the project, and resolving the conflict requires domain judgment about which document is the current source of truth.

**Context payload rules** (critical for cost discipline):
- Forward only the decision: the specific spec clause, the conflicting code or spec excerpt, and the constraint (≤100 lines total).
- Do NOT forward: the full spec, the full target code, or full project instruction files.
- The advisor returns a short verdict (≤200 words) containing the recommended resolution and a one-line rationale.

**Non-goals** — do not escalate for these:
- Terminology nitpicks or formatting inconsistencies (these are Phase 1 Warnings, not advisor material).
- Generic "the spec could be clearer" observations without a specific failure mode.
- Stylistic preferences about how requirements are expressed.
- Missing sections that are clearly an author oversight (just report it as a Warning).

Report escalations in the output: mark Phase 2 findings with `[P2]` prefix and include the advisor's one-line rationale. This preserves auditability of which findings involved frontier judgment.

## Council Escalation (High-Stakes Trade-offs)

When a finding involves a genuine architectural trade-off — where two reasonable positions exist and the wrong choice has significant implementation cost — the single high-capability advisor may be replaced by a 4-voice **Council** review. Use council escalation when all three conditions hold:

1. The trade-off has long-term architectural consequences (e.g., sync vs. async boundary, data ownership model, API versioning strategy).
2. The single-advisor verdict would likely depend on unstated assumptions about team preferences or future requirements.
3. The finding is Critical or Warning severity — not a Suggestion.

**Council voices** (request one high-capability advisor pass per voice when delegation is available, passing only the specific trade-off excerpt — not the full spec; otherwise run the same voices inline as bounded passes and record the fallback):

| Voice | Role | Anti-bias Mandate |
|-------|------|-------------------|
| Architect | Correctness and long-term maintainability | Challenge convenience-driven choices |
| Skeptic | Break the dominant assumption; find what everyone is taking for granted | Ignore sunk cost arguments |
| Pragmatist | Shipping speed and team execution risk | Ignore theoretical purity |
| Critic | Failure modes; what breaks at scale or under adversarial conditions | Assume the happy path is wrong |

**Anti-anchoring rule**: Each voice receives only the trade-off description — not the other voices' verdicts. Collect all four independently before synthesizing.

**Council output format** (append to the relevant finding in the report):
```
[COUNCIL] {trade-off description}
- Architect: {verdict, ≤2 sentences}
- Skeptic: {verdict, ≤2 sentences}
- Pragmatist: {verdict, ≤2 sentences}
- Critic: {verdict, ≤2 sentences}
Consensus: {agreed recommendation, or "No consensus — strongest dissent: <voice>: <reason>"}
```

### Profile Override (Focus-Specific Voices)

When `--focus <area>` is set on the invocation and Council Escalation triggers, replace the 4 generic voices above with 3–4 domain expert profiles from [references/expert-profiles.md](references/expert-profiles.md). The Anti-anchoring rule, output format, and budget rule all apply unchanged — only the voice labels and heuristics change.

| `--focus` value | Profiles to use (in order) |
|---|---|
| `requirements` | Requirements Quality + Specification by Example + Use Case Modeling |
| `architecture` | Interface Design + Service Boundaries + Integration Patterns + Production Resilience |
| `testing` | Risk-Based Testing + Three Amigos + Quality Attribute |
| `compliance` | Production Resilience + Cloud-Native Operations + Audit Trail |

Use generic Council (no `--focus`) when the trade-off spans two or more areas, or when the spec covers multiple domains and no single focus dominates. Mixing generic voices and focus profiles within a single Council session breaks anti-anchoring — pick one mode per session.

Council escalation consumes the full 2-advisor budget. Do not use council and single-advisor escalation in the same invocation.

## Confidence Gate

This skill applies the [Confidence Gate](../references/confidence-gate.md) before declaring the spec ready for `task-generator`.

**Required dimensions** (must each score ≥ 70):

- **Scope clarity** — A spec with undefined scope cannot be decomposed into tasks. If scope is fuzzy, the gate forces STOP.
- **Root cause identified** — The user need behind the spec must be named. Surface-level requirements without a stated user need produce tasks that solve the wrong problem.

**Band-to-status mapping** for this skill:

| Gate band | Completion status | Action |
|-----------|-------------------|--------|
| PROCEED (≥ 90) | DONE | Spec is ready for `task-generator`. |
| REVIEW (70 – 89) | NEEDS_CONTEXT | Present 1-3 open questions; consider council escalation if multiple dimensions are < 80. |
| STOP (< 70) | BLOCKED | Report which dimensions are weak; do not hand off to `task-generator`. |

The gate score must appear in the report header alongside the Critical/High/Medium/Low finding counts. A required dimension scoring below 50 forces STOP regardless of aggregate.

## Integration

- **Primary upstream** — `ywc-spec-writer`: validates `docs/specification/` section files (`01-overview.md` … `07-glossary.md`). All 4 review dimensions (completeness, consistency, feasibility, code compatibility) apply fully.
- **Secondary upstream** — `ywc-plan`: can validate feature plan documents in `docs/ywc-plans/`. Completeness and consistency dimensions apply; feasibility and code compatibility apply partially because plan documents are less implementation-specific.
- **Not applicable** — `ywc-task-generator` output (`tasks/`): task-generator *consumes* a validated spec; it does not produce one. Passing a task directory as `--spec` is a misuse.
- **Downstream**: `ywc-task-generator` — hand off only when completion status is `DONE`. `DONE_WITH_CONCERNS` requires spec revision first.

### Programmatic Consumer Policy

When consumed by an orchestrator that cannot prompt for human input (e.g., ywc-agentic):

| Completion Status | Action |
| --- | --- |
| DONE | Proceed to ywc-task-generator |
| DONE_WITH_CONCERNS | Re-invoke ywc-plan with --update-spec + --failure-context + --non-interactive (max 1 retry), then re-validate |
| BLOCKED | Stop execution; surface a structured triage report containing: (1) attempted triage steps, (2) verbatim blocker text, (3) proposed default action |
| NEEDS_CONTEXT | Stop execution; surface a structured triage report containing: (1) attempted triage steps, (2) verbatim blocker text, (3) proposed default action |
| SOCRATIC | Stop execution and report to user — SOCRATIC output is not a handoff signal; re-run without `--mode socratic` to obtain a gate verdict |
