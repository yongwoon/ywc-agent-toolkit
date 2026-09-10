# yw-000035-090-domain-quality-gate-codex-gaps — Implementation Checklist

## Prerequisites
- [ ] `yw-000032-010-domain-plan-scaffold-quality-declaration` is completed (merged)
- [ ] `yw-000032-020-domain-task-quality-gate-packet` is completed (merged)

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `codex/skills/ywc-plan/references/spec-template.md` and `codex/skills/ywc-task-generator/references/README.md.template` only.
- [ ] If either file requires broader edits than the two named headings, stop and report before proceeding.

## Stop Conditions
- [ ] Stop if `yw-000032-010` / `yw-000032-020` are not actually merged.
- [ ] Stop if a re-grep at task start shows both headings already present (this task becomes a no-op — record that in the report instead of forcing a duplicate edit).
- [ ] Stop if either target file's actual heading sequence has diverged from what this task assumes, such that the described insertion point no longer makes sense.

## Implementation Steps
- [ ] Re-verify the gap: `grep -n "^## " codex/skills/ywc-plan/references/spec-template.md` and confirm no `Quality Gate Contract` / `Module Boundaries` heading exists; `grep -n "^### " codex/skills/ywc-task-generator/references/README.md.template` and confirm no `Owned Interface` heading exists.
- [ ] In `codex/skills/ywc-plan/references/spec-template.md`: insert `## Quality Gate Contract` and `## Module Boundaries` sections (Korean prose, matching the file's existing language), positioned after the heading equivalent to `## Existing Constraints Touched` and before the heading equivalent to `## Acceptance Criteria`. `## Quality Gate Contract` states either the concrete CRAP/Mutation thresholds this spec's tasks must meet, or `N/A — no quality gate contract`; `## Module Boundaries` states the new module's public interface and forbidden edges, or `N/A — no code module introduced`. Both link `../../references/quality-gates.md` (the existing codex `quality-gates.md` from `yw-000031-010`) via an explicit action-required-style pointer — do not restate thresholds inline.
- [ ] In `codex/skills/ywc-task-generator/references/README.md.template`: insert a `### Owned Interface` subsection immediately after `### Ownership`, worded to convey "this task confirms and owns this public interface; other tasks trust this signature and do not read the implementation," with a `(None — no public interface owned)` sentinel and a short explanatory note distinguishing it from the broader `Ownership` field, in the template's own idiom.
- [ ] Confirm neither edit touches any other heading, field, or prose in either file.

## Task Verify
- [ ] `grep -q "Quality Gate Contract" codex/skills/ywc-plan/references/spec-template.md`
- [ ] `grep -q "Module Boundaries" codex/skills/ywc-plan/references/spec-template.md`
- [ ] `grep -q "Owned Interface" codex/skills/ywc-task-generator/references/README.md.template`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies — this repository is a skill/prompt distribution toolkit; `scripts/validate.sh` is the only verification gate.
