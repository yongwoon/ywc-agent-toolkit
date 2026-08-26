# 000075-020-domain-subagent-claim-contract — Implementation Checklist

## Prerequisites
- [ ] Confirm the approved context-safety specification is present.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-sequential-executor/references/subagent-status-actions.md`.

## Stop Conditions
- [ ] Stop if the contract requires forwarding peer conclusions or transcripts.
- [ ] Stop if evidence cannot be represented as a project-relative artifact or `file:line` citation.
- [ ] Stop if more than three claims are needed to explain a result.

## Hardening Gate
- [ ] Record RED-first Claim/privacy fixture targets.
- [ ] Specify the public payload shape, cap, evidence rule, and rejection model before prose changes.
- [ ] Require full review because this is a security/privacy boundary.

## Implementation Steps
- [ ] Add the optional `Claims` field with a maximum of three claim objects.
- [ ] Require each claim statement to include a project-relative artifact or `file:line` evidence citation.
- [ ] Define independent reviewer inputs as scope/exclusions/artifacts only, excluding peer conclusions and recommendations.
- [ ] Define dependent-role inputs as claims plus cited artifacts only.
- [ ] Add recursive rejection rules for transcript, chain-of-thought, raw response, raw tool output, and equivalent fields.

## Task Verify
- [ ] `rg -n "Claims|three|file:line|independent|dependent|transcript|raw_tool_output" codex/skills/ywc-sequential-executor/references/subagent-status-actions.md`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] structure validation passes (`bash scripts/validate.sh`)
- [ ] focused Claim/privacy fixtures are added by `000077-010-test-context-safety-evaluation-matrix`

## Implementation Notes

