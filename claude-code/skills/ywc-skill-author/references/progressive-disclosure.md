# Progressive Disclosure — Tier 2 vs Tier 3 decision tree + worked examples

This reference is the canonical decision tree for `ywc-skill-author` rule A14. The SKILL.md body summarizes the 3-tier loading model and shows the quick decision; this file holds the full criteria, worked examples from existing ywc-* skills, and the anti-patterns specific to each tier.

## The 3 Tiers (recap)

| Tier | File location | Cap | When loaded | Cost paid |
|---|---|---|---|---|
| **1 — Metadata** | YAML frontmatter `description` | trigger-text only, no workflow summary | Always, into auto-trigger cache | Every conversation turn |
| **2 — SKILL.md body** | `<skill>/SKILL.md` | ≤500 lines (rule A8) | Skill activation (description match or `Skill` invoke) | Once per activation |
| **3 — Bundled references** | `<skill>/references/*.md` | No cap | Only when SKILL.md body explicitly directs the agent to read the file | Once per file read |

The asymmetry **Tier 1 < Tier 2 < Tier 3** in load frequency is the entire reason for the model. Anything that fits in Tier 1 should stay there; anything that doesn't fit in Tier 1 but fits in Tier 2 should stay there; only the residue belongs in Tier 3.

## Decision Tree (full version)

For each section the author considers writing, ask the questions in order:

```text
Q1: Is this content a workflow step, rule, anti-pattern, or validation checklist
    that the agent MUST read on activation to execute the skill correctly?
    ├─ YES → Tier 2 (inline). MUST stay inline regardless of length.
    │        These sections are the skill's "behavior" — Tier 3 extraction
    │        would mean the agent could execute the skill without reading
    │        them, defeating the discipline.
    └─ NO → continue to Q2

Q2: Is this content static reference material (lookup table, decision tree,
    vocabulary list, code-block template, classification rubric)?
    ├─ NO → Tier 2 (inline). Narrative content stays inline.
    └─ YES → continue to Q3

Q3: Does the section exceed 30 lines of static content?
    ├─ NO → Tier 2 (inline). The 30-line threshold reflects the read
    │       cost — below it, the agent reads it as part of the body
    │       sweep, which is faster than an extra Read call.
    └─ YES → Tier 3 (extract). Move the section to references/<topic>.md
             and leave a one-line pointer in the SKILL.md body of the form:

                For the full <topic>, see [references/<topic>.md](references/<topic>.md).
```

The Tier 2 sections that MUST never be extracted are:

- `Rationalization Defense` (loaded for every activation to enforce discipline)
- `Workflow` / numbered steps (the skill's executable procedure)
- `Validation Checklist` (the skill's completion gate)
- `Common Mistakes` (anti-patterns the agent must recognize on activation)
- `Anti-patterns` (when explicitly listed as a Tier 2 section)
- `Iron Law` / "Three Witnesses" / similar gate prose

Even when these grow past 100 lines, they stay in Tier 2. The cost of an extra Tier 2 line is amortized across every activation — the cost of NOT having the discipline available on activation is silent skill regression.

## Worked Examples

### `ywc-refactor-clean` (211 lines, 2 references)

| Section | Tier | Why |
|---|---|---|
| Iron Law (3-witness rule) | 2 | Gate prose — must load on activation |
| Rationalization Defense (8 rows) | 2 | Discipline table — must load on activation |
| Step 1 Detect (with 7-row tool matrix) | **Hybrid** — table summary in Tier 2, full per-language detail in Tier 3 | Table fits in <30 lines summary; per-ecosystem invocation detail is reference material |
| Step 2 Classify (3-tier summary table) | **Hybrid** — summary in Tier 2, full algorithm + worked examples in Tier 3 | Same — summary is workflow, algorithm is reference |
| Steps 3-7 (SAFE/CAUTION/DANGER deletion loop, verify-done handoff) | 2 | Workflow steps — must load on activation |
| Output Format (sample report) | 2 | Output spec — short and load-on-activation |
| Validation Checklist | 2 | Completion gate |
| Common Mistakes | 2 | Anti-patterns |
| `references/detection-tools.md` | 3 | Full per-ecosystem tool invocations + grep fallback (~150 lines) |
| `references/safety-tiers.md` | 3 | Full classification algorithm with worked examples (~180 lines) |

The hybrid sections (Step 1 / Step 2) are the canonical pattern: a workflow step contains a Tier-2 **summary table** of the relevant lookup, and the SKILL.md body links to a Tier-3 reference for the full detail. The agent reads the workflow inline on activation, and only loads the reference when an edge case demands the full lookup.

### `ywc-onboard-repo` (235 lines, 3 references)

| Section | Tier | Why |
|---|---|---|
| Iron Law (3-rule gate) | 2 | Gate prose |
| Rationalization Defense (8 rows) | 2 | Discipline |
| Phase 1 Reconnaissance (6-pass table summary) | **Hybrid** | Per-pass invocations are reference material |
| Phase 2 Architecture Mapping (4-facet table) | **Hybrid** | Directory mapping per framework is reference material |
| Phase 3 Convention Detection (5-row table) | 2 | Direct workflow — inline |
| Phase 4 Generate (Output A + B templates) | **Hybrid** | Onboarding Guide template fits inline; Starter CLAUDE.md template is in Tier 3 |
| Validation Checklist | 2 | Completion gate |
| Common Mistakes | 2 | Anti-patterns |
| `references/reconnaissance-checklist.md` | 3 | Full Glob/Grep/Bash invocations per pass |
| `references/directory-conventions.md` | 3 | Per-framework directory → purpose lookup table |
| `references/claude-md-starter.md` | 3 | Starter CLAUDE.md template with placeholders |

### `ywc-code-gen` (large skill, multiple references)

Anti-pattern note: an earlier version of `ywc-code-gen` had the per-language language conventions inline, bringing the body well over 400 lines. Refactor extracted these to `references/` and the body shrunk to ~300 lines while preserving the workflow steps and verify-done handoff.

## Anti-Patterns (Tier-Specific)

### Tier 1 — Metadata (frontmatter `description`)

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Description summarizes the workflow ("Use to run 7 steps...") | Description loads every turn — workflow summary bloats the trigger cache | Trigger conditions only: "Use when...", "Triggers: ...", "Do not use for ..." |
| Description omits anti-triggers | Sibling skills collide under fuzzy matching | Always include `Do not use for ...` |
| Description omits multilingual triggers | Korean/Japanese activations miss the skill | Always include 한/英/日 |

### Tier 2 — SKILL.md body

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Body >500 lines | Loaded per activation; bloats context | Extract >30-line static sections to Tier 3 (A14) |
| Workflow extracted to Tier 3 | Agent needs workflow on activation; deferring it means the discipline doesn't run | Workflow stays in Tier 2 regardless of length |
| Per-language tool matrices inline | Single-language users pay the cost of every other language's matrix | Extract per-ecosystem detail to Tier 3 reference |

### Tier 3 — references/

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Reference file with no SKILL.md pointer | Agent never loads it (Tier 3 only loads when directed) | Add explicit pointer: `see [references/<topic>.md](references/<topic>.md)` |
| Reference file containing workflow steps | Agent reads workflow on activation, not on demand — putting it in Tier 3 means the workflow doesn't run consistently | Workflow stays in Tier 2 |
| Reference file <30 lines | Cost of the extra Read call exceeds the inline-cost savings | Inline it back into Tier 2 |
| Reference file with the same content as a SKILL.md section | Duplication drifts; one source of truth | Keep one location, link from the other |

## Audit Procedure

When auditing an existing ywc-* skill for progressive disclosure compliance:

1. Run `wc -l <skill>/SKILL.md` — if >500, A8 is violated; identify >30-line static sections to extract.
2. Read each `references/*.md` — does the SKILL.md body explicitly direct the agent to it? If not, either add a pointer or inline the content.
3. Read each `references/*.md` length — if <30 lines, inline it back (over-extraction is also an anti-pattern).
4. Confirm Workflow / Rationalization Defense / Validation Checklist / Common Mistakes are all in SKILL.md, not in references.

The audit is normally part of the `ywc-skill-author` Validation Checklist run on every new or restructured skill.
