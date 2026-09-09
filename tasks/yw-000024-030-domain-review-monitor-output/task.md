# yw-000024-030-domain-review-monitor-output — Implementation Checklist

## Prerequisites
- [ ] `yw-000023-010-docs-subagent-async-monitoring-contract` is completed and merged

## Allowed Edit Scope
- [ ] Stay within `codex/skills/references/subagent-status-actions.md`, `codex/skills/ywc-impl-review/SKILL.md`, and its `evals/evals.json`
- [ ] Do not edit reviewer agent TOMLs, executor state helpers, or generated mirror files

## Stop Conditions
- [ ] Stop if the Phase 1 exception permits file writes or broad artifact mutation
- [ ] Stop if `ywc-impl-review` can aggregate or enter Phase 2 while a lane may still be live
- [ ] Stop if shared terminal-status semantics must be redefined instead of cited

## Hardening Gate
- [ ] Classify as critical behavior change in review lifecycle and shared aggregation state
- [ ] Add RED-first eval cases for unavailable, possibly-live, and malformed reviewer output
- [ ] Record the bounded inline payload contract before implementation
- [ ] Apply duplicate-sensitive lane transition hardening and one request/interrupt bounds
- [ ] Require full implementation review before `DONE`

## Implementation Steps
- [ ] Update `codex/skills/references/subagent-status-actions.md` first with the narrow Phase 1 read-only inline exception and canonical-target validation.
- [ ] Update `codex/skills/ywc-impl-review/SKILL.md` to select generic fallback reviewers, prohibit Phase 1 writes, and cite the shared monitoring gate after dispatch.
- [ ] Encode precedence as possibly-live → `BLOCKED`, quiescent unavailable → `DONE_WITH_CONCERNS`, then existing normal aggregation.
- [ ] Preserve existing Phase 2 selection, confidence gate, and report flow when all lanes answer cleanly.
- [ ] Add evals for reviewer unavailable, reviewer possibly live, malformed/status-less/ambiguous output, and clean-all-lanes compatibility.

## Task Verify
- [ ] `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-impl-review/evals/evals.json", "utf8"))'`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `git diff --check`

## Verification
- [ ] Repository validation passes (`bash scripts/validate.sh`)
- [ ] Manual full implementation review confirms no Phase 1 file-write path and correct precedence

## Implementation Notes (optional)
