# 000076-040-domain-parallel-transition-safety — Implementation Checklist

## Prerequisites
- [ ] `000075-010-domain-context-handoff-contract` is completed and merged.
- [ ] `000075-020-domain-subagent-claim-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-parallel-executor/**`.

## Stop Conditions
- [ ] Stop if implementation creates worker-local handoff authority.
- [ ] Stop if any non-interactive transition waits for approval or progress input.
- [ ] Stop if aggregate handoff conflicts with authoritative checkpoint identity.

## Hardening Gate
- [ ] Record RED-first aggregate and worker-isolation fixture targets.
- [ ] Record aggregate handoff/status interface and failure behavior.
- [ ] Apply shared-state hardening and require full implementation review.

## Implementation Steps
- [ ] Validate resume disposition and convert branch/worktree, CI wait/timeout, and other prompt branches to terminal statuses.
- [ ] Write exactly one `.ywc-context-handoff.json` beside root run state for a parallel run.
- [ ] Exclude worker handoff files and peer conclusions from aggregate payloads.
- [ ] Reconstruct from checkpoint and current task/wave sources after malformed, stale, mismatched, or failed handoff writes.
- [ ] Update parallel README/localized metadata and focused eval declarations.

## Task Verify
- [ ] `rg -n "ywc-context-handoff|aggregate|worker|NEEDS_CONTEXT|timeout|prompt" codex/skills/ywc-parallel-executor`
- [ ] `python3 codex/skills/ywc-parallel-executor/scripts/resume-state.py --help`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] script smoke checks pass
- [ ] parallel focused fixtures pass (added in `000077-010`)

## Implementation Notes

