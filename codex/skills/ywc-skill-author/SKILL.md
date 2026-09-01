---
name: ywc-skill-author
description: >-
  (ywc) Use when creating or restructuring a ywc-* skill, or auditing ywc-*
  skills against canonical rules. Triggers: "ywc skill 생성", "create ywc
  skill", "ywc skill 만들어줘", "ywc skill 개선", "new ywc skill", "ywc
  skill audit", "ywcスキル作成", "ywc skill 룰 점검". Do not use for normal
  task-execution content edits, non-ywc-* skills, or renaming/moving skills.
---

# ywc-skill-author

**Announce at start:** "I'm using the ywc-skill-author skill to apply the canonical ywc-* skill rules."

Use this only for a ywc-* skill's create, restructure, or report-only audit.
For create or restructure, read [references/authoring-rules.md](references/authoring-rules.md)
before editing. For audit, do not load it; use the inline index and
[references/audit-workflow.md](references/audit-workflow.md).

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "It is small, so structure is optional" | Every ywc-* skill follows the same minimum contract. |
| "The description can summarize the workflow" | It is trigger-only and needs explicit anti-triggers. |
| "One generic defense row is enough" | Use at least five concrete workflow shortcuts. |
| "I can copy a sibling's table" | Defenses must fit this skill's actual failure modes. |
| "The audit found dead content, so delete it" | Audit is report-only; use a bounded deletion test, never auto-delete. |
| "I can move rules to shrink the file" | Keep the executable canonical index, audit boundary, workflow, and checks inline. |

## Canonical Rule and Audit Index

Every mode must be able to locate these rules here; create/restructure reads the
detailed reference before edits.

| Rules | Canonical requirement |
|---|---|
| A1–A5 | `ywc-` name; `(ywc) Use when...` description; anti-triggers; Korean/English/Japanese triggers for user-facing skills; only `name` and `description` frontmatter. |
| A6–A10 | First body line is the announce text; 5+ domain-specific defense rows; body ≤500 lines; plain sibling references; empty considered sections say `N/A — reason`. |
| A11–A16 | Four locale READMEs; substantive resources in `references/`; evals for verifiable outputs; extract static sections over 30 lines; synchronized `agents/openai.yaml`; no auxiliary per-skill docs. |
| Audit invariants | Run mechanical evidence first; classify findings; do not edit targets, authorize deletion, or invoke an executor; test one removal against the same prompt before retain/revert/escalate. |

## Workflow

1. Identify mode and scope. Ask only for genuine interface, naming, or behavior
   ambiguity that repository files cannot resolve.
2. **RED:** capture a representative failure/rationalization or name existing
   coverage for a refactor.
3. **GREEN:** make the smallest change that meets A1–A16. Create/restructure
   must read [references/authoring-rules.md](references/authoring-rules.md)
   before target edits; audit must instead read
   [references/audit-workflow.md](references/audit-workflow.md).
4. **REFACTOR:** close an observed loophole without adding speculative rules.
5. Review `agents/openai.yaml` interface fields, run the validator, and check
   the required locale files, references, evals, and no unintended catalog or
   routing drift.

## Validation

```bash
VALIDATE_SKILL_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/ywc-skill-author/scripts/validate-skill.sh"
[ -f "$VALIDATE_SKILL_SCRIPT" ] || VALIDATE_SKILL_SCRIPT="codex/skills/ywc-skill-author/scripts/validate-skill.sh"
bash "$VALIDATE_SKILL_SCRIPT" <skill-dir>
```

Also verify the inline index manually: frontmatter shape, domain-specific
defenses, resource routing, metadata alignment, and the requested behavior.
Use [references/progressive-disclosure.md](references/progressive-disclosure.md)
for extraction decisions, [references/description-anti-patterns.md](references/description-anti-patterns.md)
for trigger text, [references/rationalization-defense-cookbook.md](references/rationalization-defense-cookbook.md)
for defenses, [references/cross-skill-graph.md](references/cross-skill-graph.md)
for integration/side effects, and [references/skill-template.md](references/skill-template.md)
only when that detail is needed.

## Output Format

Create/restructure: the edited skill files in place (`SKILL.md`, `references/`,
`evals/`, `agents/openai.yaml` as needed).
Audit: a report-only verdict, no file edits.

```text
Status: retain | investigate | exception
```

## Completion Checks

- Create/restructure: rules remain reachable, focused validation passes, and
  no unnecessary file or abstraction was added.
- Audit: report evidence and a retain/investigate/exception verdict only; do
  not modify or delete the audited target.
