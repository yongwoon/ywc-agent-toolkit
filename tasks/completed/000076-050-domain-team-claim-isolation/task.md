# 000076-050-domain-team-claim-isolation — Implementation Checklist

## Prerequisites
- [ ] `000075-020-domain-subagent-claim-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-team-assemble/**`.
- [ ] Read but do not redefine the canonical Claim contract.

## Stop Conditions
- [ ] Stop if an independent reviewer would receive peer conclusion, recommendation, or transcript.
- [ ] Stop if a dependent role requires uncited or raw evidence.
- [ ] Stop if more than three Claims are emitted.

## Hardening Gate
- [ ] Record RED-first role-isolation/privacy fixture targets.
- [ ] Record role-specific input/output contracts before changing prompt templates.
- [ ] Require full review for privacy-sensitive payload filtering.

## Implementation Steps
- [ ] Update `references/prompt-templates.md` with included scope, excluded scope, artifacts, and Claims inputs.
- [ ] Filter independent reviewer payloads to exclude peer claims, conclusions, and recommendations.
- [ ] Filter dependent-role payloads to Claims and cited artifacts only.
- [ ] Enforce Claim cap and evidence/privacy validation at prompt assembly boundaries.
- [ ] Update skill metadata and eval descriptions for the new role-isolation contract.

## Task Verify
- [ ] `rg -n "Claims|peer|conclusion|recommendation|transcript|cited artifact" codex/skills/ywc-team-assemble`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] structure validation passes
- [ ] team/privacy focused fixtures pass (added in `000077-010`)

## Implementation Notes

