# yw-000012-030-infra-resolve-initials-script

## Purpose

Add the deterministic script that resolves collaborator initials, replacing the 190-line
`references/initials-resolution.md` read (single consumer: `ywc-task-generator`) with a script
invocation.

## Scope

- `claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh`: precedence chain and
  derivation algorithm from `references/initials-resolution.md:22-50`, returning
  `RESOLVED <s>` / `NEEDS_CONFIRM <candidate>` / `NONE`.
- Shell test file asserting AC4–AC5.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260901-claude-skill-token-efficiency.md` — FR4, AC4, AC5
- `claude-code/skills/references/initials-resolution.md` — canonical precedence chain, derivation algorithm, section format

### Summary

This is a distinct file from `ywc-task-generator`'s own `references/collaborator-initials.md`
(which governs this skill's own PHASE-numbering ledger behavior for `ywc-task-generator` itself).
This task implements the top-level shared reference's derivation algorithm as a script. The
script never prompts or writes — it only proposes. Rung 3 (derivation + confirmation) requires
a human-confirmation step that stays in the skill body; the script emits `NEEDS_CONFIRM
<candidate>` and lets the calling skill run the prompt.

### Out of Scope (from spec)

- Wiring the script into `ywc-task-generator`'s body — handled by `yw-000013-010`.
- `resolve-language.sh` — handled by `yw-000012-020`.

## Criticality

`normal` — read-only resolution script, no auth/payment/crypto/secret surface.

## Dependencies

### Depends On

- `yw-000012-010` — before-baseline must be captured before this script lands

### Depended By

- `yw-000012-040` — needs this script to exist to extend shellcheck coverage over it
- `yw-000013-010` — wires this script into `ywc-task-generator`

## Key Files

- `claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh` — new
- `claude-code/skills/ywc-task-generator/scripts/test-resolve-initials.sh` — new

## Notes

Never prompts, never writes — NFR3 applies (writing stays with the skill body's confirmation
step, matching `ywc-setup-language`'s ownership of writes in the language case).

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh`
- `claude-code/skills/ywc-task-generator/scripts/test-resolve-initials.sh`

### Owned Interface

- `resolve-initials.sh [--initials <s>]` → stdout `RESOLVED <s>` \| `NEEDS_CONFIRM <candidate>` \| `NONE`; exit 0 always

### Shared Surfaces

- (None identified)

### Conflicts With

- (None identified)

### Parallelizable After

- `yw-000012-010`

### Task Verify

- `bash claude-code/skills/ywc-task-generator/scripts/test-resolve-initials.sh`
- `shellcheck claude-code/skills/ywc-task-generator/scripts/resolve-initials.sh`

## Out of Scope

- Any change to `references/initials-resolution.md` itself.
- Wiring `ywc-task-generator`'s body to invoke this script.
