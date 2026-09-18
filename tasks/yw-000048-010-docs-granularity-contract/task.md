# yw-000048-010-docs-granularity-contract — Implementation Checklist

## Prerequisites
- [ ] Confirm the specification is `docs/ywc-plans/20260918-codex-task-generator-granularity-expansion.md`.
- [ ] Confirm no task edits `codex/agents/ywc-architect.toml`.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-task-generator/SKILL.md` and `codex/skills/ywc-task-generator/references/granularity-modes.md`.
- [ ] Stop before editing README, eval, generated mirror, or agent files.

## Stop Conditions
- [ ] Stop if the source contract requires changing mode selection, task-ID allocation, preview approval, or safety invariants.
- [ ] Stop if a separate maintained example file is discovered and needs independent scope; report it for task re-planning.
- [ ] Stop if the advisor payload cannot name exactly one matching guideline for the selected mode.

## Hardening Gate
- [ ] Classify as docs-only contract change.
- [ ] Record named exception: no production behavior; verify with targeted searches and contract evals.
- [ ] Record the public instruction contract in the README Hardening Evidence block before editing.
- [ ] Mark Data Integrity and critical-surface review as N/A.

## Implementation Steps
- [ ] Replace reviewability values with `human: ~15 files / ~500 LOC` and `llm: ~35 files / ~1,200 LOC` in `SKILL.md`.
- [ ] Update Step 5 mode guidance and explicitly state that thresholds are advisory, not automatic bundling authorization.
- [ ] Update Planning Advisor payload and size-verification rules to carry the selected mode and exactly its matching guideline.
- [ ] State that LLM vertical bundling is limited to one feature with exclusive Ownership and explicit Shared Surfaces.
- [ ] Preserve category splitting and all Safety Invariants, including single phase per task.
- [ ] Align `references/granularity-modes.md` comparison, detailed rules, and examples with the same contract.

## Task Verify
- [ ] `rg -n '~15 files|~500 LOC|~35 files|~1,200 LOC|exclusive Ownership|Shared Surfaces|one feature' codex/skills/ywc-task-generator/SKILL.md codex/skills/ywc-task-generator/references/granularity-modes.md`
- [ ] `! rg -n '~10 files|~300 LOC|~25 files|~800 LOC' codex/skills/ywc-task-generator/SKILL.md codex/skills/ywc-task-generator/references/granularity-modes.md`
- [ ] `git diff --check`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Markdown-only task)
- [ ] unit tests pass (N/A — covered by contract eval task)
- [ ] integration tests pass (N/A — docs-only task)
- [ ] app builds without error (N/A — repository distribution validation is downstream)

## Implementation Notes

