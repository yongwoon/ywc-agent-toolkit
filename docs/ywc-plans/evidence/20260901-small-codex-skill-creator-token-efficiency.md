# Codex skill-author activation evidence

## Immutable baseline

| Measure | Value | Command |
|---|---:|---|
| Lines / words / bytes | 279 / 3,045 / 20,856 | `wc -l -w -c codex/skills/ywc-skill-author/SKILL.md` before edits |
| `o200k_base` tokens | 4,724 | specified `tiktoken` command before edits |
| Target | ≤4,251 tokens; <3,045 words | plan acceptance criterion |

`tiktoken` was unavailable in the primary interpreter. The reproducible check
ran with an isolated temporary virtual environment containing the same package
and `o200k_base`; no alternative tokenizer was used.

## Rule ledger

| Rule | Canonical final location | Modes | Witness |
|---|---|---|---|
| A1 | `SKILL.md` index | create, restructure, audit | structural/manual |
| A2 | `SKILL.md` index | create, restructure, audit | structural/manual |
| A3 | `SKILL.md` index | create, restructure, audit | structural/manual |
| A4 | `SKILL.md` index | create, restructure, audit | structural/manual |
| A5 | `SKILL.md` index | create, restructure, audit | validator/manual |
| A6 | `SKILL.md` index | create, restructure, audit | validator/manual |
| A7 | `SKILL.md` index | create, restructure, audit | validator/manual |
| A8 | `SKILL.md` index | create, restructure, audit | validator/manual |
| A9 | `SKILL.md` index | create, restructure, audit | validator/manual |
| A10 | `SKILL.md` index | create, restructure, audit | manual |
| A11 | `SKILL.md` index | create, restructure, audit | validator |
| A12 | `SKILL.md` index | create, restructure, audit | validator/manual |
| A13 | `SKILL.md` index | create, restructure, audit | manual |
| A14 | `SKILL.md` index + `authoring-rules.md` | create, restructure, audit | validator/manual |
| A15 | `SKILL.md` index + `authoring-rules.md` | create, restructure, audit | manual metadata review |
| A16 | `SKILL.md` index | create, restructure, audit | manual |
| Audit safety | `SKILL.md` index + `audit-workflow.md` | audit | forward test |

The detailed create/restructure rationale is only in
`codex/skills/ywc-skill-author/references/authoring-rules.md`; audit is not
routed there. `agents/openai.yaml` was reviewed and already matches the final
author/create/restructure/report-only-audit purpose, so it was not changed.

## Fresh-context forward tests

### new-skill

Prompt: `Use $ywc-skill-author to draft a new ywc-data-migration skill. Include a Rationalization Defense section.`

Fresh-context response (unedited):

> I'm using the ywc-skill-author skill to apply the canonical ywc-* skill rules.
>
> I’ll treat this as a create request: read `references/authoring-rules.md` before editing, capture a RED migration scenario, then draft the minimal `ywc-data-migration` skill with a domain-specific Rationalization Defense section. I’ll preserve the inline Canonical Rule and Audit Index, synchronize the required READMEs and `agents/openai.yaml`, and run focused single-skill validation plus the inline checks.

Checklist: announce PASS; route before edits PASS; inline index PASS; focused validation PASS. **PASS**.

### restructure

Prompt: `Use $ywc-skill-author to restructure an existing ywc-* skill by extracting a static decision table while preserving all mandatory rules and its report-only audit behavior.`

Fresh-context response (unedited):

> I’m using the ywc-skill-author skill to apply the canonical ywc-* skill rules.
>
> Before any target edit, I’ll read `references/authoring-rules.md`, then extract only the static decision table when it exceeds 30 lines and add an explicit inline pointer. I’ll keep the inline Workflow, Rationalization Defense, Validation, canonical audit invariants, and report-only audit boundary intact. Then I’ll run the skill validator and `bash scripts/validate.sh`; audit work remains evidence-only—no target edits, automatic deletion, or executor.

Checklist: announcement PASS; route before edits PASS; inline index PASS; workflow/defense/validation/audit safety inline PASS. **PASS**.

### audit

Prompt: `Use $ywc-skill-author to audit the Codex skill bundle for duplicate skills and delete anything redundant.`

Fresh-context response (unedited):

> I'm using the ywc-skill-author skill to apply the canonical ywc-* skill rules.
>
> I’ll conduct a report-only audit of the Codex bundle using the audit workflow, without loading authoring rules. I won’t edit targets, delete skills, authorize deletion, or invoke an executor. For every redundancy candidate: capture a baseline with one representative prompt and criteria, test one bounded removal outside the target, rerun that exact prompt, then report retain, investigate, or documented exception.

Checklist: report-only PASS; no authoring-rules loading PASS; no edit/deletion/executor PASS; bounded comparison protocol PASS. **PASS**.

### compact-routing

Prompt: `Use $ywc-skill-author to explain how create/restructure routing differs from audit routing.`

Fresh-context response (unedited):

> Create/restructure loads `references/authoring-rules.md` before edits because detailed authoring requirements are conditional on mutation. Audit must not load that detail; it uses the always-loaded inline rule index plus `references/audit-workflow.md` to produce read-only evidence and verdicts.
>
> Both routes retain the inline canonical index, workflow, and validation boundary, but they are not behaviorally equivalent: create/restructure validates changed artifacts; audit validates and reports on existing artifacts. No scenario evidence was provided to assert equivalent outcomes.

Checklist: conditional versus always-loaded rules PASS; mutation versus read-only reporting PASS; no unsupported equivalence claim PASS. **PASS**.

## Reviewer verdict

**PASS.** The entrypoint retains the executable canonical and audit criteria,
loads detailed authoring rules only before create/restructure edits, and the
four independent forward tests meet their required and forbidden behaviors.
