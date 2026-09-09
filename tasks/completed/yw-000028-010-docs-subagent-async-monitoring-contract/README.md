# yw-000028-010-docs-subagent-async-monitoring-contract

## Purpose
Establish the shared Subagent Async Monitoring Contract that consumer claude-code skills will cite so an orchestrator never loses track of a concurrently-dispatched subagent whose completion notification arrives out of order or late.

## Scope
Add the new top-level reference file `claude-code/skills/references/subagent-async-monitoring.md` and register it in `claude-code/skills/CLAUDE.md` with a new `## Subagent Async Monitoring Contract` section. This task establishes and registers the contract only — it does not wire any consumer skill's SKILL.md body to cite it.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#functional-requirements` — FR1 (reference content), FR8 (CLAUDE.md registration)
- `docs/ywc-plans/20260909-subagent-async-monitoring-contract-port.md#acceptance-criteria` — AC5, AC6
- `claude-code/skills/references/subagent-status-actions.md` — existing adjacent contract (BLOCKED triage); the new file cites this rather than redefining escalation handling

### Summary
Port (not copy) the async-monitoring contract from develop-with-llm PR #229/#230, generalized to this repo's tool-agnostic prose convention: never name `ListAgents`/`ScheduleWakeup` literally, only "the `Agent` tool" and "the orchestrating session's agent-roster-listing and scheduled-recheck capability, where the runtime provides one." The file has exactly four sections (Unique Dispatch Labeling, Full-Roster Reconciliation, Mandatory Fallback Wakeup, Bounded Escalation on Stall) plus a Known Limitations note. `claude-code/skills/CLAUDE.md` gets a new section mirroring the existing `## Bot Review Polling Parameters` format (purpose, key parameters summarized, explicit "Action required" directive, consumer list).

### Out of Scope (from spec)
- Wiring `ywc-parallel-executor`'s 4b-monitor gate and Status Routing row — handled by `yw-000029-010-domain-parallel-executor-monitor-gate`
- Wiring `ywc-sequential-executor`'s Rationalization Defense row and Advisor Escalation Policy citation — handled by `yw-000029-020-domain-sequential-executor-advisor-monitor`
- Wiring `ywc-impl-review`'s Phase 1 / Step 4.5 dispatch citations — handled by `yw-000029-030-domain-impl-review-monitor-citation`
- `codex/skills/` porting — out of scope for the whole spec (separate follow-up)
- Rewriting `references/subagent-status-actions.md` — unaffected, only cited

## Criticality
normal — orchestration/documentation prose only; no auth, payment, crypto, PII, or external-input-handling code path (spec's Critical Surfaces: None).

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000029-010-domain-parallel-executor-monitor-gate` — cites this reference for the new `4b-monitor` gate
- `yw-000029-020-domain-sequential-executor-advisor-monitor` — cites this reference from the new Rationalization Defense row and the Advisor Escalation Policy paragraph
- `yw-000029-030-domain-impl-review-monitor-citation` — cites this reference from the Phase 1 and Step 4.5 dispatch paragraphs
- `yw-000030-010-infra-async-monitoring-validation` — validates the reference file's structure and the CLAUDE.md registration

## Key Files
- `claude-code/skills/references/subagent-async-monitoring.md` — new file
- `claude-code/skills/CLAUDE.md` — new `## Subagent Async Monitoring Contract` section, inserted adjacent to the existing `## Subagent Return Payload Contract and Structured Surface-to-User` section

## Notes
- Threshold table (adapted from develop-with-llm PR #230's 480s/900s hardening): batch size 2–4 → soft-check 480s / hard escalation 900s; batch size 5+ (e.g. impl-review Phase 1, Step 4.5) → soft-check 300s / hard escalation 600s.
- Full-Roster Reconciliation must state the idempotency clause explicitly: a duplicate terminal-status notification for an already-reconciled name is a no-op, never a second batch member.
- Cancel the fallback the instant full-roster reconciliation confirms every dispatched name has a terminal status — never let a stale fallback fire after the batch is already known complete.
- Bounded Escalation on Stall routes to the batch-level equivalent of `BLOCKED` per `../references/subagent-status-actions.md` — surface which named subagent(s) are unaccounted for; never silently re-dispatch.
- Known Limitations note: this contract mitigates but does not eliminate notification races; a subagent whose process exits without ever emitting a terminal status is indistinguishable from one that is merely slow until the hard threshold fires.
- Expected file length: roughly 60–90 lines, comparable to `references/subagent-status-actions.md`'s 59 lines — do not let it approach the ~500-line skill/reference guidance.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/references/subagent-async-monitoring.md`
- `claude-code/skills/CLAUDE.md` (new section only — do not edit any existing section)

### Owned Interface
- The four section headings (`Unique Dispatch Labeling`, `Full-Roster Reconciliation`, `Mandatory Fallback Wakeup`, `Bounded Escalation on Stall`) plus the `Known Limitations` note, and the reference's file path `../references/subagent-async-monitoring.md` (relative to each consumer skill directory) — downstream tasks cite this path and these heading names verbatim.

### Shared Surfaces
- `claude-code/skills/CLAUDE.md` — shared file; this task adds only the new section, no edits to any existing section.

### Conflicts With
- (None identified) — no other task in this batch touches these two files.

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `test -f claude-code/skills/references/subagent-async-monitoring.md`
- `rg -n "Unique Dispatch Labeling|Full-Roster Reconciliation|Mandatory Fallback Wakeup|Bounded Escalation on Stall|Known Limitations" claude-code/skills/references/subagent-async-monitoring.md`
- `rg -n "ListAgents|ScheduleWakeup" claude-code/skills/references/subagent-async-monitoring.md` — must return no matches (tool-agnostic prose requirement)
- `wc -l claude-code/skills/references/subagent-async-monitoring.md`
- `rg -n "## Subagent Async Monitoring Contract" claude-code/skills/CLAUDE.md`
- `rg -n "ywc-parallel-executor" claude-code/skills/CLAUDE.md`

## Out of Scope
- Any edit to `claude-code/skills/ywc-parallel-executor/SKILL.md`, `claude-code/skills/ywc-sequential-executor/SKILL.md`, or `claude-code/skills/ywc-impl-review/SKILL.md`.
- Any edit to `claude-code/skills/references/subagent-status-actions.md`.
- `codex/skills/` and generated plugin package files.
