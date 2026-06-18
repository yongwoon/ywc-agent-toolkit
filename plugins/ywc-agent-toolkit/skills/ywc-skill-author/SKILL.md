---
name: ywc-skill-author
description: >-
  (ywc) Use when creating a new ywc-* skill, restructuring an existing one's
  frontmatter/body sections/references/agents metadata, or auditing existing
  ywc-* skills against the canonical rule set. Triggers: "ywc skill 생성", "create ywc
  skill", "ywc skill 만들어줘", "ywc skill 개선", "new ywc skill", "ywc skill
  upgrade", "ywcスキル作成", "ywc skill audit", "ywc skill 룰 점검". Do not use
  for editing skill content during normal task execution, for non-ywc-* skills,
  or for renaming/moving skills (use `git mv` directly).
---

# ywc-skill-author

**Announce at start:** "I'm using the ywc-skill-author skill to apply the canonical ywc-* skill rules."

This skill captures the conventions that every `ywc-*` skill must follow, derived from the synchronized Claude Code, Codex, and Pi skill bundles. Use it whenever authoring or restructuring a ywc-* skill so that new work matches the established quality bar without manual cross-referencing of sibling skills.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "This skill is small, full structure is overkill" | Even small skills must follow the rule set. Inconsistency across siblings hurts skill activation accuracy. |
| "Description trigger summary is fine, I'll skip 'Do not use for...'" | Description must include explicit anti-triggers. Without them, the skill collides with siblings under fuzzy matching. |
| "Rationalization Defense table is generic, I'll copy from another skill" | Each table must be **domain-specific**. Generic tables become noise that the agent ignores. |
| "I covered hallucination with one generic row, that is enough" | Future skills need domain-specific defenses for guessing missing context, adjacent cleanup, overbuilding, and completion without goal-specific verification. Each row must name the workflow shortcut it blocks. |
| "References are optional, keep everything inline" | Body >500 lines violates progressive disclosure. Extract long sections to `references/`. |
| "Skill name does not need `ywc-` prefix" | Always `ywc-` prefix. Differentiates from upstream skills and signals project ownership. |
| "`agents/openai.yaml` is UI-only, so it can wait" | Stale UI metadata causes wrong skill chips and default prompts. Update it with every meaningful SKILL.md change. |
| "A `requires:` frontmatter key makes the dependency clear" | Codex skill frontmatter must stay strict: `name` and `description` only. Document dependencies in `## Integration`. |
| "Cross-references can use tool-specific force-load syntax" | Never force-load sibling skills from documentation. It causes unnecessary context loading and unintended activation. Always reference by skill name only. |
| "Korean README only, English/Japanese later" | Always create the full `README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` set together. |
| "Add a README or changelog inside the skill for clarity" | Do not add auxiliary docs beyond the required locale README set. Use `references/` only for task-relevant material the agent should load on demand. |

**Violating the letter of these rules is violating the spirit.** Inconsistent ywc-* skills degrade the activation accuracy of every other ywc-* skill.

## Mandatory Rules

These rules apply to **every** ywc-* skill without exception.

### Frontmatter

| # | Rule |
|---|---|
| A1 | Skill name MUST be prefixed `ywc-` (e.g., `ywc-commit`, `ywc-task-generator`) |
| A2 | `description` MUST start with `(ywc) Use when...` (trigger-only, never a workflow summary) |
| A3 | `description` MUST include explicit `Do not use for...` anti-triggers pointing to the correct sibling skill where applicable |
| A4 | `description` MUST include multilingual triggers (Korean / English / Japanese) when the skill is user-facing |
| A5 | Frontmatter MUST contain only `name` and `description`. Do not add `requires`, `category`, `metadata`, `allowed-tools`, or other non-schema fields |

### Body

| # | Rule |
|---|---|
| A6 | First non-heading line MUST be `**Announce at start:** "I'm using the ywc-<name> skill to ..."` |
| A7 | MUST include a `## Rationalization Defense` section with a table of at least 5 domain-specific Excuse / Reality pairs |
| A8 | SKILL.md body MUST be ≤500 lines; longer sections MUST be extracted to `references/<topic>.md` with a brief inline pointer |
| A9 | Cross-references to sibling ywc-* skills MUST use the skill name only (e.g., `ywc-impl-review`). Never use `@` syntax |
| A10 | Empty sections MUST use `N/A — <reason>` rather than being omitted (so future readers can tell the section was considered, not forgotten) |

### Filesystem

| # | Rule |
|---|---|
| A11 | Each skill MUST ship the full README locale set: `README.md` (Korean), `README.en.md`, `README.ja.md`, `README.ko.md` |
| A12 | Long-form content goes under `references/`. Reusable templates use `.template` suffix (e.g., `task.md.template`) — see Progressive Disclosure §A14 for extraction criteria |
| A13 | Test scenarios under `evals/evals.json` when the skill has objectively verifiable outputs |
| A14 | Tier 3 extraction MUST trigger when any single inline section exceeds **30 lines of static content** (lookup tables, decision trees, vocabulary lists, code-block templates). Workflow / step prose stays in Tier 2 even when long, so the agent reads it on activation. See [references/progressive-disclosure.md](references/progressive-disclosure.md) for the full decision tree |
| A15 | Each skill MUST ship `agents/openai.yaml` with `interface.display_name`, `interface.short_description`, and `interface.default_prompt` synchronized to SKILL.md |
| A16 | Do not add auxiliary documentation such as per-skill `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, or `QUICK_REFERENCE.md`; only `SKILL.md`, required locale READMEs, `agents/openai.yaml`, and truly needed resources belong in the skill folder |

Rationalization Defense rows must cover the skill's concrete failure modes, including guessing missing context, adjacent cleanup, overbuilding abstractions, and declaring completion without goal-specific verification. Acceptable: `"This migration task only mentions one table; I can also normalize neighboring tables"` -> `Adjacent schema cleanup changes review scope and belongs in a separate task unless the spec names it.` Unacceptable: `"Do not hallucinate"` -> `Be careful.`

## Progressive Disclosure (3-Tier Loading Model)

Every ywc-* skill is consumed by the agent in **three tiers**, each with different load semantics and different cost profiles. Skill design must respect what loads when:

| Tier | What | Cap | When loaded |
|---|---|---|---|
| **1 — Metadata** | YAML frontmatter `description` (and Triggers list it contains) | Trigger-matching only, no workflow summary | Always, into the auto-trigger cache — every conversation pays the cost |
| **2 — SKILL.md body** | Rules, workflow steps, anti-patterns, validation checklist | ≤500 lines (A8) | Only when the skill activates (description matched or `Skill` tool invoked) |
| **3 — references/** | Lookup tables, decision trees, vocabulary lists, full templates, worked examples | No cap (loaded on demand) | Only when SKILL.md body explicitly directs the agent to read a specific file |

The cost asymmetry is the entire reason for the model. Tier 1 cost is paid every turn, so descriptions must stay trigger-focused (anti-pattern: workflow summary). Tier 2 cost is paid once per activation, so workflow steps and rules belong here. Tier 3 cost is paid only when a deep dive is genuinely needed, so the per-language tool matrices, full classification rubrics, and templates go here.

**Decision tree (inline vs. extract to Tier 3)** — see [references/progressive-disclosure.md](references/progressive-disclosure.md) for the full version with worked examples from `ywc-refactor-clean`, `ywc-onboard-repo`, and `ywc-code-gen`. Quick form:

```text
Is the section >30 lines of static content (lookup table / decision tree / template)?
├─ YES → extract to references/<topic>.md with one-line pointer in SKILL.md body
└─ NO → keep inline
     │
     └─ Is the content workflow / step / rule prose?
        ├─ YES → MUST stay inline regardless of length (the agent needs it
        │        on activation to execute the skill correctly)
        └─ NO → keep inline if <30 lines, extract otherwise
```

The Workflow / Rationalization Defense / Validation Checklist sections are **Tier 2 by definition** — never extract them to Tier 3, even when they grow. The agent must read them on activation, not on demand.

## Recommended Rules

These improve quality but are not strictly required.

| # | Rule | Apply when |
|---|---|---|
| B1 | Document upstream dependencies in `## Integration` | Skill expects another ywc-* skill to have run first |
| B2 | Add `## Arguments` table | Skill accepts flags or positional arguments |
| B3 | Add `## Workflow` or `## Execution Steps` numbered list | Skill performs a multi-step process |
| B4 | Add `## Output Format` block with sample | Skill emits a structured report or artifact |
| B5 | Add `## Validation` or `## Common Mistakes` | Skill has well-known failure modes |
| B6 | Reference an Advisor Pattern (A / B / C) from the bundle-level `references/advisor-pattern.md` | Skill uses an advisor/escalation pass for cost-bounded review |
| B7 | Add `## Banned Output Patterns` table | Skill generates code or other parseable artifacts |
| B8 | Define a `--skip-<side-effect>` flag and document propagation in `## Arguments` + `## Integration` + the relevant bundle instruction file | Skill performs a side effect (UL update, CI check, etc.) that an upstream caller may have already performed. See [references/cross-skill-graph.md#flag-propagation-patterns](references/cross-skill-graph.md) for the canonical pattern. |

## Format Conventions

| Area | Rule |
|---|---|
| Korean prose | Keep technical terms in English (Database, API, Backend, etc.). Follow the active repository or bundle instruction file (`AGENTS.md`, `CLAUDE.md`, or Pi bundle guidance). |
| Comparisons | Use markdown tables, not bullet lists |
| Multilingual triggers in description | Quoted form: `"키워드", "key", "キーワード"` |
| Multi-line shell commands | Use heredoc (`git commit -m "$(cat <<'EOF' ... EOF\n)"`) |
| Empty section placeholder | `N/A — <reason>` (e.g., `N/A — no external spec, housekeeping only`) |
| Code blocks | Always include language tag (\`\`\`bash, \`\`\`python, etc.) |

## Anti-patterns (Never Do These)

| Anti-pattern | Why bad | Replace with |
|---|---|---|
| Description summarizing the workflow | The agent may follow the description shortcut and skip SKILL.md body discipline | Trigger conditions only |
| `// TODO`, `// ...rest`, stub implementations in examples | A stub committed today is a runtime crash tomorrow | Complete examples or marked PAUSE |
| Tool-specific force-load cross-reference | Causes unnecessary context loading or unintended activation | Plain skill name reference |
| Long bullet lists for decisions | Hard to scan | Markdown table |
| Vague language ("appropriate", "as needed") | Cannot be operationalized | Explicit threshold or condition |
| Empty section | Reader cannot tell if forgotten or absent | `N/A — <reason>` |
| Single-language description triggers (English only) | User-facing skill misses Korean/Japanese intent | Add 한/英/日 triggers |

## Workflow (Adapted from superpowers:writing-skills)

Treat skill authoring as TDD applied to documentation: **RED → GREEN → REFACTOR**.

### Step 1: RED — Baseline Behavior

Before writing or restructuring the skill, run a representative scenario without the skill present (or with the current version) and document:

- What did the agent do incorrectly?
- What rationalizations did the agent use verbatim?
- Which mandatory rule would have prevented the failure?

This step ensures the skill addresses real gaps, not hypothetical ones.

### Step 2: GREEN — Minimal Skill

Draft the skill addressing exactly the failures identified in RED. Do not pre-emptively cover hypothetical cases.

Use [references/skill-template.md](references/skill-template.md) as the starting structure.

For a new bundle skill in this repository, place it at `codex/skills/<skill-name>/` unless the user explicitly asks for an installed local skill. For an installed local skill outside this bundle, ask for the destination and default to `${CODEX_HOME:-$HOME/.codex}/skills` so Codex can discover it automatically.

### Step 3: REFACTOR — Close Loopholes

Re-run the scenario with the new skill. Document any new rationalizations the agent invented to bypass the new rules. Add those to the Rationalization Defense table.

Repeat until the agent cannot find a loophole.

### Resource and Metadata Pass

After drafting SKILL.md, add only the resources that directly support execution:

- `agents/openai.yaml`: write deterministic `interface.display_name`, `interface.short_description`, and `interface.default_prompt` from the final SKILL.md. Include optional fields such as icons or brand color only when explicitly provided.
- `references/`: move long static rules, lookup tables, rubrics, and templates here, then add an explicit pointer from SKILL.md.
- `scripts/`: add scripts only when repeated manual code would be fragile or deterministic reliability matters. Run each new script, or a representative sample for similar scripts, before completion.
- `assets/`: add files that the skill uses as output material, not documentation to load into context.

Delete placeholder files and do not create empty resource directories.

## Forward-testing

Use subagents to forward-test substantial or tricky skill changes when available and when doing so will not require risky approvals or long-running work.

Prompt subagents as if they are solving a real task, for example:

```text
Use $ywc-<skill-name> at <path/to/skill> to solve <realistic user request>.
```

Do not ask them to "review the skill" unless the user explicitly requested a review. Pass raw artifacts and the task-local request, not the intended answer, suspected bug, or planned fix. Review their outputs for generalization failures, then tighten SKILL.md or references and retest if needed.

## Templates and References

| Reference | Use when |
|---|---|
| [references/skill-template.md](references/skill-template.md) | Drafting a brand-new ywc-* skill |
| [references/rationalization-defense-cookbook.md](references/rationalization-defense-cookbook.md) | Writing or expanding the Rationalization Defense table |
| [references/description-anti-patterns.md](references/description-anti-patterns.md) | Auditing or rewriting a description field |
| [references/cross-skill-graph.md](references/cross-skill-graph.md) | Deciding `## Integration` upstream/downstream entries, "Do not use for..." cross-pointers, and `--skip-<side-effect>` flag propagation between caller/callee skills |
| [references/progressive-disclosure.md](references/progressive-disclosure.md) | Deciding whether a section stays inline (Tier 2) or extracts to `references/` (Tier 3); auditing existing skills for tier compliance |

## Validation Checklist

Run the bundled mechanical gate first — it enforces the deterministic subset of the checklist below (name/description shape, announce line, 500-line cap, README locale set, no `@ywc-` force-loads, reference pointers + min-length) for a single skill and exits non-zero on any failure:

```bash
VALIDATE_SKILL_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/ywc-skill-author/scripts/validate-skill.sh"
[ -f "$VALIDATE_SKILL_SCRIPT" ] || VALIDATE_SKILL_SCRIPT="codex/skills/ywc-skill-author/scripts/validate-skill.sh"
bash "$VALIDATE_SKILL_SCRIPT" <skill-dir>
```

Then verify the judgment-based items the script cannot check, before merging a new or modified ywc-* skill:

**Frontmatter**
- [ ] `name` starts with `ywc-`
- [ ] `description` starts with `(ywc) Use when...`
- [ ] `description` ends with `Do not use for...` anti-triggers
- [ ] `description` includes Korean / English / Japanese triggers (if user-facing)
- [ ] No frontmatter keys other than `name` and `description`

**Body**
- [ ] First content line is `**Announce at start:** "..."`
- [ ] `## Rationalization Defense` has ≥5 domain-specific rows
- [ ] No `@` cross-references
- [ ] No vague language without threshold
- [ ] Body ≤500 lines (`wc -l SKILL.md`)
- [ ] Empty sections use `N/A — <reason>` rather than being omitted

**Filesystem**
- [ ] Full README locale set: `.md`, `.en.md`, `.ja.md`, `.ko.md`
- [ ] `agents/openai.yaml` exists and matches the current SKILL.md purpose and invocation
- [ ] Long sections (>30 lines of static content) extracted to `references/` (Tier 3 — A14)
- [ ] `evals/evals.json` exists if outputs are objectively verifiable
- [ ] No auxiliary docs such as per-skill `CHANGELOG.md`, `INSTALLATION_GUIDE.md`, or `QUICK_REFERENCE.md`
- [ ] New scripts were run, or a representative sample was run when many similar scripts were added

**Progressive Disclosure (Tier compliance)**
- [ ] Description (Tier 1) contains trigger conditions only — no workflow summary
- [ ] Workflow / Rationalization Defense / Validation Checklist / Common Mistakes are in SKILL.md body (Tier 2), not in `references/`
- [ ] Every `references/*.md` file has at least one explicit pointer from the SKILL.md body
- [ ] No `references/*.md` file is <30 lines (over-extraction)

**Catalog Sync**
- [ ] Relevant bundle catalog or root distribution docs updated when the repository has one for the affected bundle
- [ ] Relevant routing guide updated if the bundle has one and the skill is user-facing
- [ ] If skill is part of a pipeline, the 표준 개발 Pipeline diagram updated

## Cross-Skill Etiquette

- If skill A's purpose overlaps with skill B's responsibility, document the relationship in `## Integration` and add `(use ywc-B)` to A's `Do not use for...` line.
- For shared conventions across multiple skills (e.g., Advisor Pattern), extract to the bundle-level `references/<topic>.md` rather than duplicating.
- New skill that supersedes an existing one: do **not** silently delete the old skill in the same PR. Add a deprecation note pointing to the successor, then delete in a later PR after a soak period.

## Common Mistakes

- **Skipping the RED step** because "the gap is obvious" — gaps that look obvious to the author are often not the gap the agent actually has. Always observe baseline behavior.
- **Copying a sibling's Rationalization Defense table verbatim** — tables must be domain-specific to be effective. Adapt every excuse to the new skill's actual failure modes.
- **Adding everything inline because "references is overhead"** — this scales poorly. The 500-line cap exists because skills are loaded into context whenever activated.
- **Forgetting to update `skills/README.md` catalog** — invisible skills do not get discovered.
