# yw-000048-020-docs-granularity-readmes — Implementation Checklist

## Prerequisites
- [ ] `yw-000048-010-docs-granularity-contract` is completed and merged.
- [ ] The maintained locale policy is identified before changing non-default README files.

## Allowed Edit Scope
- [ ] Edit only the granularity guidance in `codex/skills/ywc-task-generator/README.md` and maintained locale counterparts.
- [ ] Do not edit `plugins/ywc-agent-toolkit/skills/**` directly.

## Stop Conditions
- [ ] Stop if the translation workflow does not identify a locale as maintained for the changed strings.
- [ ] Stop if README guidance requires a new rule absent from the canonical source contract.
- [ ] Stop if validation identifies a missing required locale file; report rather than recreating unrelated documentation.

## Hardening Gate
- [ ] Classify as docs-only contract alignment.
- [ ] Record named exception: verify via targeted searches and `bash scripts/validate.sh`.
- [ ] Record the public README contract and downstream distribution consumer before edits.
- [ ] Mark Data Integrity and critical-surface review as N/A.

## Implementation Steps
- [ ] Update the default Korean README mode table to `human: ~15 files / ~500 LOC` and `llm: ~35 files / ~1,200 LOC`.
- [ ] Add the advisory-threshold disclaimer and one-feature LLM bundling guardrails.
- [ ] Update only locale files whose changed strings are maintained by the repository workflow.
- [ ] Confirm README wording retains category splitting and all Safety Invariants.

## Task Verify
- [ ] `rg -n '~15 files|~500 LOC|~35 files|~1,200 LOC' codex/skills/ywc-task-generator/README*.md`
- [ ] `! rg -n '~10 files|~300 LOC|~25 files|~800 LOC' codex/skills/ywc-task-generator/README*.md`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Markdown-only task)
- [ ] unit tests pass (N/A — covered by contract eval task)
- [ ] integration tests pass (N/A — docs-only task)
- [ ] app builds without error (N/A — generated distribution is downstream)

## Implementation Notes

