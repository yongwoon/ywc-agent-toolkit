# 000076-010-domain-producer-result-artifact-profile — Implementation Checklist

## Prerequisites
- [ ] `000075-010-domain-context-handoff-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-plan/**` and `codex/skills/ywc-spec-ready/**`.
- [ ] Do not edit `ywc-agentic` consumer logic.

## Stop Conditions
- [ ] Stop if a producer needs to recover an artifact path from prose, `--output`, basename reconstruction, or raw response scanning.
- [ ] Stop if a non-DONE terminal status is treated as a Result authority.
- [ ] Stop if direct non-agentic calls would lose backward compatibility.

## Hardening Gate
- [ ] Record RED-first producer parser fixtures.
- [ ] Record exact producer-specific interface schemas and bounded `BLOCKED` errors.
- [ ] Require full review for artifact authority and privacy behavior.

## Implementation Steps
- [ ] Add `--artifact-profile agentic` to `ywc-plan` and reject it when combined with `--output`.
- [ ] Implement Small and Medium/Large filename rules under `docs/ywc-plans/`.
- [ ] Add exact success Result blocks to `ywc-plan` and `ywc-spec-ready` with no extra fields.
- [ ] Validate artifact paths as existing regular repository-relative Markdown files inside the permitted root.
- [ ] Update both skills' Tier 1/Tier 2 README files, `agents/openai.yaml`, and local eval descriptions to document the contract.

## Task Verify
- [ ] `rg -n "artifact-profile|## Result|Scale:|Artifact:" codex/skills/ywc-plan codex/skills/ywc-spec-ready`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] structure validation passes (`bash scripts/validate.sh`)
- [ ] targeted producer evals pass (added in `000077-010`)

## Implementation Notes

