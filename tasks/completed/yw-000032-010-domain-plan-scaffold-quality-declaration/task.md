# yw-000032-010-domain-plan-scaffold-quality-declaration — Implementation Checklist

## Prerequisites
- [ ] `yw-000031-010-docs-quality-gate-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-plan/**` and `codex/skills/ywc-project-scaffold/**`.

## Stop Conditions
- [ ] Stop if declaration requires raw commands or creates a project file without an explicit request.
- [ ] Stop if a change touches task-generator, executor, or agent ownership.

## Hardening Gate
- [ ] Classify as contract behavior documentation.
- [ ] Add or extend skill contract eval evidence before changing behavior rules.
- [ ] Record the producer/consumer interface above; mismatches return `NEEDS_CONTEXT`.
- [ ] Data Integrity Hardening: N/A.

## Implementation Steps
- [ ] Update `ywc-plan/SKILL.md` and `references/spec-template.md` to require the contract section or exact N/A sentinel and module boundaries for Medium/Large specs.
- [ ] Update `ywc-plan/evals/evals.json` with no-contract, valid declaration, missing-field, and no-fabricated-command cases.
- [ ] Update `ywc-project-scaffold/SKILL.md` to seed advisory metadata only on request and update its evals for omission and command-invention boundaries.
- [ ] Preserve existing handoffs, frontmatter, and non-quality-gate planning behavior.

## Task Verify
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `rg -n "Quality Gate Contract|N/A — no quality gate contract|NEEDS_CONTEXT|invent|command" codex/skills/ywc-plan codex/skills/ywc-project-scaffold`

## Verification
- [ ] Repository contract evals pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] Typecheck/build: N/A — Markdown/eval-only changes.
