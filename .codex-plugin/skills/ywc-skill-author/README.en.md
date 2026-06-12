# ywc-skill-author

A **meta-skill** for authoring new ywc-* skills and restructuring existing ones. Encodes the canonical rules derived from analyzing production ywc-* skills (frontmatter format, Rationalization Defense, multilingual triggers, progressive disclosure, etc.) so that LLMs automatically follow the standard.

## Use Cases

- Authoring a brand-new ywc-* skill from scratch.
- Restructuring an existing ywc-* skill's frontmatter, body sections, or references.
- Auditing ywc-* skills against the canonical rule set.

## Invocation

```bash
/ywc-skill-author
```

Or via natural language:

> "Create a new ywc skill"
> "Audit my ywc skill against the rules"
> "Upgrade ywc skill structure"

## Input

- New skill: skill purpose and primary trigger scenarios.
- Audit: path to the target skill directory.

## Output

- A SKILL.md following the standard structure (Frontmatter + Rationalization Defense + Workflow + Validation Checklist).
- Supplementary `references/` files where appropriate.
- The full README locale set (`README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`).

## Core Rules

The standard enforced by this skill consists of:

- **Mandatory Rules**: Frontmatter / Body / Filesystem (A1–A13).
- **Recommended Rules**: Situational guidelines (B1–B7).
- **Format Conventions**: Korean prose with English technical terms, multilingual triggers, etc.
- **Anti-patterns**: Workflow-summary descriptions, stub code, `@` cross-references, and similar pitfalls.

See `SKILL.md` and the four reference documents under `references/` for the full specification.

## Related Skills

- `ywc-task-generator` — applies the same multilingual policy and reference-extraction pattern.
- All ywc-* skills — must conform to the rules defined here.

## Reference Documents

- `references/skill-template.md` — starting template for new skills.
- `references/rationalization-defense-cookbook.md` — guide for writing the Rationalization Defense table.
- `references/description-anti-patterns.md` — anti-patterns to avoid in the description field.
- `references/cross-skill-graph.md` — prerequisite and cross-reference graph for ywc-* skills.
