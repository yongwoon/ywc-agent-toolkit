---
name: ywc-skill-author
description: >-
  (ywc) Use when creating a new ywc-* skill, restructuring an existing one's
  frontmatter/body sections/references, or auditing existing ywc-* skills
  against the canonical rule set. Triggers: "ywc skill 생성", "create ywc
  skill", "ywc skill 만들어줘", "ywc skill 개선", "new ywc skill", "ywc skill
  upgrade", "ywcスキル作成", "ywc skill audit", "ywc skill 룰 점검". Do not use
  for editing skill content during normal task execution, for non-ywc-* skills,
  or for renaming/moving skills (use `git mv` directly).
---

# ywc-skill-author

**Announce at start:** "I'm using the ywc-skill-author skill to apply the canonical ywc-* skill rules."

This skill captures the conventions that every Codex `ywc-*` skill must follow, derived from the production skills in `codex/skills/`. Use it whenever authoring or restructuring a Codex ywc-* skill so that new work matches the established quality bar without manual cross-referencing of sibling skills.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "This skill is small, full structure is overkill" | Even small skills must follow the rule set. Inconsistency across siblings hurts skill activation accuracy. |
| "Description trigger summary is fine, I'll skip 'Do not use for...'" | Description must include explicit anti-triggers. Without them, the skill collides with siblings under fuzzy matching. |
| "Rationalization Defense table is generic, I'll copy from another skill" | Each table must be **domain-specific**. Generic tables become noise that the agent ignores. |
| "References are optional, keep everything inline" | Body >500 lines violates progressive disclosure. Extract long sections to `references/`. |
| "Skill name does not need `ywc-` prefix" | Always `ywc-` prefix. Differentiates from upstream skills and signals project ownership. |
| "Cross-references can use `@` for force-load" | Never use `@`. It burns 200k+ context. Always reference by skill name only. |
| "Korean README only, English/Japanese later" | Always create the full `README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` set together. |
| "The Claude frontmatter has useful metadata, keep it in Codex too" | Codex reads only `name` and `description` for activation. Extra Claude-only fields create drift and fail repository validation. |

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
| A5 | Codex frontmatter MUST contain only `name` and `description`. Do not include Claude-only metadata such as `version`, `category`, `phase`, `requires`, `advisor_budget`, or `allowed tools`. |

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
| A12 | Each Codex skill MUST include `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt` aligned to `SKILL.md` |
| A13 | Long-form content goes under `references/`. Reusable templates use `.template` suffix (e.g., `task.md.template`) |
| A14 | Test scenarios under `evals/evals.json` when the skill has objectively verifiable outputs |

## Recommended Rules

These improve quality but are not strictly required.

| # | Rule | Apply when |
|---|---|---|
| B1 | Document upstream dependencies in `## Integration` instead of frontmatter | Skill expects another ywc-* skill to have run first |
| B2 | Add `## Arguments` table | Skill accepts flags or positional arguments |
| B3 | Add `## Workflow` or `## Execution Steps` numbered list | Skill performs a multi-step process |
| B4 | Add `## Output Format` block with sample | Skill emits a structured report or artifact |
| B5 | Add `## Validation` or `## Common Mistakes` | Skill has well-known failure modes |
| B6 | Reference an Advisor Pattern (A / B / C) from `../references/advisor-pattern.md` | Skill uses high-capability advisor for cost-bounded escalation |
| B7 | Add `## Banned Output Patterns` table | Skill generates code or other parseable artifacts |
| B8 | Define a `--skip-<side-effect>` flag and document propagation in `## Arguments` + `## Integration` + `codex/skills/CLAUDE.md` | Skill performs a side effect (UL update, CI check, etc.) that an upstream caller may have already performed. See [references/cross-skill-graph.md#flag-propagation-patterns](references/cross-skill-graph.md#flag-propagation-patterns) for the canonical pattern. |

## Format Conventions

| Area | Rule |
|---|---|
| Korean prose | Keep technical terms in English (Database, API, Backend, etc.). See [codex/skills/CLAUDE.md](../CLAUDE.md). |
| Comparisons | Use markdown tables, not bullet lists |
| Multilingual triggers in description | Quoted form: `"키워드", "key", "キーワード"` |
| Multi-line shell commands | Use heredoc (`git commit -m "$(cat <<'EOF' ... EOF\n)"`) |
| Empty section placeholder | `N/A — <reason>` (e.g., `N/A — no external spec, housekeeping only`) |
| Code blocks | Always include language tag (\`\`\`bash, \`\`\`python, etc.) |

## Anti-patterns (Never Do These)

| Anti-pattern | Why bad | Replace with |
|---|---|---|
| Description summarizing the workflow | The agent follows description shortcuts and may skip SKILL.md body | Trigger conditions only |
| `// TODO`, `// ...rest`, stub implementations in examples | A stub committed today is a runtime crash tomorrow | Complete examples or marked PAUSE |
| `@skill-name` cross-reference | Force-loads context, burns 200k+ tokens | Plain skill name reference |
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

### Step 3: REFACTOR — Close Loopholes

Re-run the scenario with the new skill. Document any new rationalizations the agent invented to bypass the new rules. Add those to the Rationalization Defense table.

Repeat until the agent cannot find a loophole.

## Templates and References

| Reference | Use when |
|---|---|
| [references/skill-template.md](references/skill-template.md) | Drafting a brand-new ywc-* skill |
| [references/rationalization-defense-cookbook.md](references/rationalization-defense-cookbook.md) | Writing or expanding the Rationalization Defense table |
| [references/description-anti-patterns.md](references/description-anti-patterns.md) | Auditing or rewriting a description field |
| [references/cross-skill-graph.md](references/cross-skill-graph.md) | Deciding `requires:` declarations, "Do not use for..." cross-pointers, and `--skip-<side-effect>` flag propagation between caller/callee skills |

## Validation Checklist

Before merging a new or modified ywc-* skill, verify:

**Frontmatter**
- [ ] `name` starts with `ywc-`
- [ ] `description` starts with `(ywc) Use when...`
- [ ] `description` ends with `Do not use for...` anti-triggers
- [ ] `description` includes Korean / English / Japanese triggers (if user-facing)
- [ ] Codex frontmatter contains only `name` and `description`

**Body**
- [ ] First content line is `**Announce at start:** "..."`
- [ ] `## Rationalization Defense` has ≥5 domain-specific rows
- [ ] No `@` cross-references
- [ ] No vague language without threshold
- [ ] Body ≤500 lines (`wc -l SKILL.md`)
- [ ] Empty sections use `N/A — <reason>` rather than being omitted

**Filesystem**
- [ ] Full README locale set: `.md`, `.en.md`, `.ja.md`, `.ko.md`
- [ ] `agents/openai.yaml` exists and matches the skill purpose
- [ ] Long sections (>30 lines of static content) extracted to `references/`
- [ ] `evals/evals.json` exists if outputs are objectively verifiable

**Catalog Sync**
- [ ] Root `README.md` Skill 목록 table updated
- [ ] `CONTRIBUTING.md` or repository guidance updated if the skill changes authoring rules
- [ ] If skill is part of a pipeline, the 표준 개발 Pipeline diagram updated

## Cross-Skill Etiquette

- If skill A's purpose overlaps with skill B's responsibility, document the dependency in `## Integration` and add `(use ywc-B)` to A's `Do not use for...` line.
- For shared conventions across multiple skills (e.g., Advisor Pattern), extract to a directly linked `references/<topic>.md` file rather than duplicating.
- New skill that supersedes an existing one: do **not** silently delete the old skill in the same PR. Add a deprecation note pointing to the successor, then delete in a later PR after a soak period.

## Common Mistakes

- **Skipping the RED step** because "the gap is obvious" — gaps that look obvious to the author are often not the gap the agent actually has. Always observe baseline behavior.
- **Copying a sibling's Rationalization Defense table verbatim** — tables must be domain-specific to be effective. Adapt every excuse to the new skill's actual failure modes.
- **Adding everything inline because "references is overhead"** — this scales poorly. The 500-line cap exists because skills are loaded into context whenever activated.
- **Forgetting to update root `README.md` catalog** — invisible skills do not get discovered.
