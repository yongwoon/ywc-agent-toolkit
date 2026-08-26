# 000076-030-domain-sequential-transition-safety — Implementation Checklist

## Prerequisites
- [ ] `000075-010-domain-context-handoff-contract` is completed and merged.
- [ ] `000075-020-domain-subagent-claim-contract` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-sequential-executor/**`.

## Stop Conditions
- [ ] Stop if a transition would emit a user prompt in non-interactive mode.
- [ ] Stop if resume scope differs and no `--resume-disposition` is present.
- [ ] Stop if URL policy is missing or outside `deny|allow|allowlist` with canonical HTTPS origins.
- [ ] Stop if handoff writing would mutate authoritative checkpoint state.

## Hardening Gate
- [ ] Record RED-first transition and recovery fixtures.
- [ ] Record status, resume, URL-policy, and handoff contracts.
- [ ] Apply atomic state hardening and require full implementation review.

## Implementation Steps
- [ ] Add `--resume-disposition resume|stop` handling at the authoritative checkpoint boundary.
- [ ] Convert branch/worktree conflict, CI wait/timeout, and external URL policy prompts to bounded terminal statuses.
- [ ] Validate `.codex/settings.local.json` `ywDevSequentialExecutor.externalSpecUrls` without creating missing configuration.
- [ ] Write and read `.ywc-context-handoff.json` using checkpoint-first ordering and the shared atomic replacement contract.
- [ ] Update sequential README/localized metadata and focused eval declarations.

## Task Verify
- [ ] `bash codex/skills/ywc-sequential-executor/scripts/verify-transition.sh`
- [ ] `rg -n "resume-disposition|externalSpecUrls|NEEDS_CONTEXT|ywc-context-handoff|prompt" codex/skills/ywc-sequential-executor`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] transition verification passes
- [ ] sequential focused fixtures pass (added in `000077-010`)

## Implementation Notes

