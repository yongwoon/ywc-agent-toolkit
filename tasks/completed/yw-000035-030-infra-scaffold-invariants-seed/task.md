# yw-000035-030-infra-scaffold-invariants-seed — Implementation Checklist

## Prerequisites
- [ ] None — root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `codex/skills/ywc-project-scaffold/SKILL.md` only.
- [ ] Do NOT edit `claude-code/skills/ywc-project-scaffold/SKILL.md` under any circumstance.

## Stop Conditions
- [ ] Stop if `codex/skills/ywc-architecture-invariants/SKILL.md`'s `--mode draft` interface cannot be located (it must already exist per the spec's Existing Constraints Touched table).
- [ ] Stop if a step numbered "6" or an "Architecture Invariants" section already exists in the target file.

## Implementation Steps
- [ ] Confirm `codex/skills/ywc-project-scaffold/SKILL.md`'s Behavioral Flow ends at step "5. Extras" and `## Output Rules` follows immediately.
- [ ] Insert a new "### 6. Architecture Invariants Seed" step between them:
  - [ ] Scope it to `new-project-plan` mode only.
  - [ ] After the tree/explanation step, offer (do not auto-run) `ywc-architecture-invariants --mode draft --proposal <path> --output <path> --approve-write` to draft a fenced-YAML/JSON manifest from the proposed layer structure.
  - [ ] State: never written to disk without explicit user approval; `enforcement: advisory` always; skipped entirely (no manifest emitted, no offer made) when the proposed structure yields no forbidden edges.
- [ ] Grep `claude-code/skills/ywc-project-scaffold/SKILL.md` for "architecture-invariants" and confirm zero matches remain (do not add any).

## Task Verify
- [ ] `grep -n "Architecture Invariants Seed" codex/skills/ywc-project-scaffold/SKILL.md`
- [ ] `grep -q "ywc-architecture-invariants --mode draft" codex/skills/ywc-project-scaffold/SKILL.md`
- [ ] `! grep -q "architecture-invariants" claude-code/skills/ywc-project-scaffold/SKILL.md`

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies to this repository.
