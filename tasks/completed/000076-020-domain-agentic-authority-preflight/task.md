# 000076-020-domain-agentic-authority-preflight — Implementation Checklist

## Prerequisites
- [ ] `000076-010-domain-producer-result-artifact-profile` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-agentic/**`.

## Stop Conditions
- [ ] Stop if any downstream artifact must be inferred from logs, prose, basename, or requested output.
- [ ] Stop if a missing required input would require prompting under `--non-interactive`.
- [ ] Stop if status propagation is ambiguous or a producer Result is malformed.

## Hardening Gate
- [ ] Record RED-first routing/preflight cases.
- [ ] Record invocation packet fields and terminal status/error contracts.
- [ ] Require full review for authority and privacy boundaries.

## Implementation Steps
- [ ] Replace caller-constructed planner output with `ywc-plan --artifact-profile agentic` and parse paired Scale/Artifact.
- [ ] Route Small artifacts directly to `ywc-code-gen`; route Medium/Large only through DONE `ywc-spec-ready` artifacts.
- [ ] Add preflight checks for `--mode`, unresolved `--lang`, `--suggestions`, `--resume-disposition`, and external URL configuration.
- [ ] Propagate parseable callee statuses and return bounded `BLOCKED`/`NEEDS_CONTEXT` without downstream invocation on failure.
- [ ] Remove or prohibit hard-coded `plan.md`, basename reconstruction, unlabelled path, and raw-response fallback authority.

## Task Verify
- [ ] `rg -n "--output|plan\.md|raw response|NEEDS_CONTEXT|BLOCKED|artifact-profile agentic" codex/skills/ywc-agentic/SKILL.md`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] structure validation passes (`bash scripts/validate.sh`)
- [ ] agentic focused fixtures pass (added in `000077-010`)

## Implementation Notes

