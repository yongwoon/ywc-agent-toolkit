# yw-000028-010-docs-subagent-async-monitoring-contract — Implementation Checklist

## Prerequisites
- [ ] None — this is the root task of the batch.

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`: `claude-code/skills/references/subagent-async-monitoring.md` (new file) and `claude-code/skills/CLAUDE.md` (new section only)
- [ ] If any other edit seems required, stop and report before proceeding

## Stop Conditions
- [ ] Stop if writing the four required sections would push the file's length materially past the ~500-line skill/reference guidance
- [ ] Stop if `claude-code/skills/CLAUDE.md` has no `## Subagent Return Payload Contract and Structured Surface-to-User` section to insert adjacent to (re-verify with `rg -n "## Subagent Return Payload Contract"`)
- [ ] Stop if a literal `ListAgents` or `ScheduleWakeup` identifier is about to be written — replace with the generic capability phrasing instead

## Implementation Steps
- [ ] Create `claude-code/skills/references/subagent-async-monitoring.md` with a top-level `# Subagent Async Monitoring Contract` heading and exactly these four `##` sections plus a trailing `## Known Limitations` note:
  - [ ] **Unique Dispatch Labeling** — every subagent dispatched as part of a concurrent batch (a wave in `ywc-parallel-executor`, the 5-way Phase 1 fan-out, or the 20-way Step 4.5 verifier fan-out in `ywc-impl-review`) must be given a name that deterministically maps back to what it was dispatched for — task name for parallel-executor, `<aspect>-<verifier-index>` for impl-review's verifier fan-out. Never a generic or reused label across a batch.
  - [ ] **Full-Roster Reconciliation** — before treating a batch as complete, the orchestrator must reconcile the full expected roster (the set of names it dispatched) against the set of names it has received a terminal status for, via the runtime's own agent-listing capability where one exists, or otherwise the batch's own tracked state (a checklist of dispatched names ticked off as each terminal status arrives) — never inferring completion from notification arrival order or count alone. State the idempotency clause explicitly: a duplicate terminal-status notification for an already-reconciled name is a no-op, never a second batch member.
  - [ ] **Mandatory Fallback Wakeup** — after dispatching a batch of 2+ concurrent subagents, the orchestrator sets an explicit bounded wait/check point: the runtime's own scheduled-recheck capability where one exists, or otherwise a manual "check back after N seconds" discipline. Include the threshold table (2–4 concurrent → 480s soft-check / 900s hard escalation; 5+ concurrent → 300s soft-check / 600s hard escalation) and the cancellation rule (cancel the fallback the moment full-roster reconciliation confirms every dispatched name has a terminal status).
  - [ ] **Bounded Escalation on Stall** — if the hard escalation threshold is reached and full-roster reconciliation still shows one or more names without a terminal status, treat it as the batch-level equivalent of `BLOCKED` per `../references/subagent-status-actions.md`. Do not keep waiting indefinitely, do not silently re-dispatch. Surface which named subagent(s) are unaccounted for.
  - [ ] **Known Limitations** — this contract mitigates but does not eliminate notification races; a subagent whose process exits without ever emitting a terminal status is indistinguishable from one that is merely slow until the hard threshold fires.
  - [ ] Throughout, use only generic vocabulary: "the `Agent` tool" (matching `ywc-parallel-executor/SKILL.md:207`'s existing phrasing) and "the orchestrating session's agent-roster-listing and scheduled-recheck capability, where the runtime provides one" — never a literal tool identifier such as `ListAgents` or `ScheduleWakeup`.
- [ ] Add a new `## Subagent Async Monitoring Contract` section to `claude-code/skills/CLAUDE.md`, inserted adjacent to the existing `## Subagent Return Payload Contract and Structured Surface-to-User` section, mirroring the `## Bot Review Polling Parameters` section's format:
  - [ ] A short purpose sentence (why the contract exists — the source incident of two concurrently-dispatched subagents' completions being mixed up)
  - [ ] Key parameters summarized (the threshold table's two rows), with a note that the reference file is the canonical source — do not duplicate the full table in `CLAUDE.md`
  - [ ] An explicit `> **Action required on entering the branch that needs it**: Read [references/subagent-async-monitoring.md]` directive
  - [ ] The consumer list: `ywc-parallel-executor`, `ywc-sequential-executor`, `ywc-impl-review`
- [ ] Re-read both edited/created files once complete and confirm no unrelated section of `CLAUDE.md` was touched.

## Task Verify
- [ ] `test -f claude-code/skills/references/subagent-async-monitoring.md`
- [ ] `rg -n "Unique Dispatch Labeling|Full-Roster Reconciliation|Mandatory Fallback Wakeup|Bounded Escalation on Stall|Known Limitations" claude-code/skills/references/subagent-async-monitoring.md`
- [ ] `rg -n "ListAgents|ScheduleWakeup" claude-code/skills/references/subagent-async-monitoring.md` — expect no output
- [ ] `wc -l claude-code/skills/references/subagent-async-monitoring.md` — expect roughly 60–90
- [ ] `rg -n "## Subagent Async Monitoring Contract" claude-code/skills/CLAUDE.md`
- [ ] `rg -n "ywc-parallel-executor" claude-code/skills/CLAUDE.md`

## Verification
- [ ] `git diff --check` reports no whitespace errors
- [ ] `bash scripts/validate.sh` still passes (no skill-structure regression from the CLAUDE.md edit)

## Implementation Notes (optional)
