# yw-000031-010-docs-quality-gate-contract — Implementation Checklist

## Prerequisites
- [ ] No predecessor task; confirm the working tree is the intended repository.

## Allowed Edit Scope
- [ ] Modify only `codex/skills/references/quality-gates.md` and directly required shared-reference registration text.

## Stop Conditions
- [ ] Stop if the spec requires raw command text, runtime dependencies, or Claude Code edits.
- [ ] Stop if a consumer needs a field not defined by the canonical packet.

## Hardening Gate
- [ ] Classify as docs-only contract work.
- [ ] Record targeted-search evidence before handoff.
- [ ] Treat the packet and status precedence as a public cross-task interface; mismatches return `NEEDS_CONTEXT`.
- [ ] Data Integrity Hardening: N/A for Markdown-only work.
- [ ] Final implementation review must confirm no raw commands or secrets are authorized.

## Implementation Steps
- [ ] Create `codex/skills/references/quality-gates.md` with the exact contract states, no-contract sentinel, packet fields, and evidence redaction rules from AC1/AC2.
- [ ] Define Cleaner-before-Hardener dispatch eligibility, production/test ownership boundaries, three-attempt cap, and residual-survivor reporting for AC3/AC4.
- [ ] Define `BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE` aggregation and unavailable-tool behavior for AC5/AC6.
- [ ] Document the no-contract path and verify downstream references can cite one shared semantic source.

## Task Verify
- [ ] `rg -n "contract_state|approved.*digest|sanitized.*evidence|three|BLOCKED.*NEEDS_CONTEXT.*DONE_WITH_CONCERNS.*DONE|Cleaner|Hardener" codex/skills/references/quality-gates.md`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] Repository validation passes (`bash scripts/validate.sh`)
- [ ] Typecheck/build: N/A — documentation-only repository change.
