# yw-000024-010-domain-parallel-monitor-gate — Implementation Checklist

## Prerequisites
- [ ] `yw-000023-010-docs-subagent-async-monitoring-contract` is completed and merged

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-parallel-executor/SKILL.md` and its `evals/evals.json`
- [ ] Do not edit the shared reference, generated mirror, or agent TOMLs

## Stop Conditions
- [ ] Stop if the implementation needs a new collaboration API or CLI polling
- [ ] Stop if source-task lifecycle identity and returned collaboration target cannot remain separate
- [ ] Stop if cleanup or next-wave behavior would occur while a target may still be live

## Hardening Gate
- [ ] Classify as critical behavior change in shared mutable lifecycle state
- [ ] Add RED-first eval scenarios for silent stall and terminal during escalation
- [ ] Record source/target interface contract before changing the dispatch gate
- [ ] Apply duplicate-sensitive escalation bounds: one request, one interrupt, one final reconciliation
- [ ] Require `ywc-impl-review` before `DONE`

## Implementation Steps
- [ ] Update the successful-spawn path around `codex/skills/ywc-parallel-executor/SKILL.md` to record only usable returned canonical targets and retain source task names for state operations.
- [ ] Add the post-dispatch event-first/full-roster reconciliation gate by citation to `references/subagent-async-monitoring.md`.
- [ ] Route terminal payloads by returned target, continue while terminal evidence is absent, and treat a missing roster entry as non-terminal.
- [ ] Apply the 600-second silent-worker escalation and preserve existing failure handling only after quiescence; block cleanup, next-wave dispatch, reports, and `DONE` when possibly live.
- [ ] Add evals for silent stall, terminal event during escalation, and failed/unparseable spawn without changing existing task lifecycle semantics.

## Task Verify
- [ ] `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-parallel-executor/evals/evals.json", "utf8"))'`
- [ ] `python3 codex/skills/ywc-parallel-executor/scripts/test-transition-safety.py`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] Repository validation passes (`bash scripts/validate.sh`)
- [ ] `git diff --check` passes

## Implementation Notes (optional)

