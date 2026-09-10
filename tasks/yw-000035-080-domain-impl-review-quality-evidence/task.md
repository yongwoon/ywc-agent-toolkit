# yw-000035-080-domain-impl-review-quality-evidence — Implementation Checklist

## Prerequisites
- [ ] `yw-000035-010-docs-quality-gate-contract-claude` is completed (merged) — `claude-code/skills/references/quality-gates.md` exists.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/ywc-impl-review/SKILL.md` only.

## Stop Conditions
- [ ] Stop if `claude-code/skills/references/quality-gates.md` does not exist.
- [ ] Stop if the QA subagent description paragraph or the Confidence Gate `## Confidence Gate` section cannot be found.

## Implementation Steps
- [ ] Locate the QA subagent bullet (ends "...does not typically require frontier reasoning.") and append: when the task's Quality Gate Contract ran a Mutation gate, a surviving mutant is required evidence for a P1 Testing finding; absence of a contract or a 0-survivor result must not itself be read as license for unsupported subjective Testing criticism, but must also not force additional criticism where none is warranted.
- [ ] Locate the Confidence Gate's `**Evidence quality**` bullet and append: a score cap applies only when a contract exists and `gate_state` shows the gate did not run (`"not run — tool unavailable"` / `"not run — dispatch failed"`) — never when the contract itself is absent, so a gate-less project is not permanently held below the REVIEW band.
- [ ] Confirm both new clauses reference (do not restate the definition of) the `gate_state` vocabulary from `claude-code/skills/references/quality-gates.md`.

## Task Verify
- [ ] `grep -n "surviving mutant" claude-code/skills/ywc-impl-review/SKILL.md`
- [ ] `grep -n "gate_state" claude-code/skills/ywc-impl-review/SKILL.md`
- [ ] `grep -q "N/A — no quality gate contract" claude-code/skills/ywc-impl-review/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
