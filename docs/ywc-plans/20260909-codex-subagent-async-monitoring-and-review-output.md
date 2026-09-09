# Codex Subagent Async Monitoring and Review-Worker Output Contract

> Status: Draft
> Scale: Medium
> Created: 2026-09-09
> Author: Codex
> Spec Reference: [develop-with-llm PR #229](https://github.com/yongwoon/develop-with-llm/pull/229), [PR #230](https://github.com/yongwoon/develop-with-llm/pull/230)

## Global Constraints

- `codex/skills/` is the source of truth; the marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from it and must not be edited first (`codex/AGENTS.md:3-10`).
- Codex `SKILL.md` frontmatter must contain only `name` and `description` (`AGENTS.md`, `CLAUDE.md`).
- Codex custom agents are read-only TOML definitions (`AGENTS.md`, `CLAUDE.md:75-78`); `codex/agents/*.toml` is not a place to impose caller-only dispatch identity.
- The completion gate is `bash scripts/validate.sh`; Codex source/package synchronization is required after source edits (`AGENTS.md`, `codex/AGENTS.md:18-20`).

## Purpose

PRs #229 and #230 document a real asynchronous-subagent stall: a completion notification can be missed while a worker continues or has already finished. The current Codex bundle routes parsed terminal statuses but has no shared rule for canonical dispatch identity, whole-roster reconciliation, bounded escalation, or quiescence before lifecycle actions.

This change will port those behavior contracts to the Codex skill source so executors do not mistake an absent notification or a missing roster entry for `DONE`, and implementation review does not claim complete review coverage when a read-only reviewer is unavailable.

## Scope

- Add one shared Codex async-monitoring reference for implementation workers, sequential advisors, and read-only Phase 1 review workers.
- Wire canonical-target roster monitoring into `ywc-parallel-executor` after successful worker dispatch.
- Wire the bounded advisor-monitoring and unavailable fallback into `ywc-sequential-executor` without changing its existing three-call budget or task lifecycle ownership.
- Add the Phase 1 review-worker inline-output exception and monitoring-result precedence to `ywc-impl-review`.
- Add focused contract evals and regenerate the Codex marketplace mirror.

## Out of Scope

- Changes to `codex/agents/*.toml`: standalone agents cannot know the caller-assigned canonical dispatch target, and their existing read-only Status/Summary output is compatible. The caller skill injects the Phase 1-specific inline payload contract only for that dispatch class.
- Claude Code skills, agents, task ledgers, version/release metadata, or a broad rewrite of all subagent consumers.
- Synthetic CLI polling, persisted live-agent state across resumes, automatic re-dispatch after an exhausted escalation, or changes to existing `DONE`/`BLOCKED` semantic ownership in `subagent-status-actions.md`.

## Quality Gate Contract

N/A — no project-owned complexity or mutation quality-gate contract is declared. Structural and behavioral checks are `bash scripts/validate.sh`, the affected skill eval JSON validation, and package-source synchronization.

## Outcome Oracle

| Element | Contract |
|---|---|
| Target | Codex executor and review skills distinguish attributable terminal completion from a missing notification, malformed payload, unavailable reviewer, or possibly-live worker. |
| Quality threshold | Every AC1–AC7 is implemented; a possibly-live lane never permits cleanup, next-wave dispatch, ordinary review aggregation, Completion Report, or `DONE`; a quiescent unavailable reviewer is visible and yields `DONE_WITH_CONCERNS`. |
| Evidence required | The affected `evals/evals.json` scenarios cover the terminal, silent-stall, advisor-unavailable, reviewer-unavailable, and possibly-live branches; `bash scripts/run-codex-skill-contract-evals.sh`, `bash scripts/validate.sh`, `git diff --check`, and source-to-plugin diff inspection succeed. |
| Stop condition | Hand off to task generation only when spec validation has no unresolved Critical or Warning findings; after implementation, declare the change complete only when the implementation verification commands in this document pass. |

## Module Boundaries

| Module | Owned public interface | Consumers | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|---|
| `codex/skills/references/subagent-async-monitoring.md` | Canonical target/roster, terminal-evidence, escalation, and quiescence contract | Parallel executor, sequential executor, impl review | Collaboration APIs; shared status-actions contract | Task-state policy duplication; CLI polling |
| `codex/skills/references/subagent-status-actions.md` | Terminal-status interpretation and bounded payload contract | All orchestrating skills | Async-monitoring reference by citation | Lifecycle ownership for review lanes |
| `ywc-parallel-executor/SKILL.md` | Worker-wave dispatch and failure handling | Implementation workers, downstream delivery | Shared monitoring/status references | Inventing canonical target or proceeding while possibly live |
| `ywc-sequential-executor/SKILL.md` | Advisor budget and owner-specific fallback | Sequential advisor calls | Shared monitoring reference | Background implementation dispatch or wave state transitions |
| `ywc-impl-review/SKILL.md` | Five-lane review aggregation and report status | Read-only review workers, Phase 2 advisors | Both shared references; existing reviewer rubrics | Worktree/task lifecycle transitions |

## Existing Constraints Touched

| Existing artifact | Behavior (verified) | Planned interaction |
|---|---|---|
| `codex/skills/ywc-parallel-executor/SKILL.md:242-276` | Spawns parallel implementation workers and immediately routes only returned statuses; an absent/unparseable status becomes `BLOCKED`. | Add a post-dispatch monitor gate that builds the roster only from successful returned targets, reconciles every wake-up, and blocks lifecycle progression until quiescence is established. |
| `codex/skills/ywc-parallel-executor/SKILL.md:494-500` | Failed tasks preserve branches/worktrees and skip cleanup. | Reuse this handling only after the monitor has evidence of quiescence and exactly one source-task transition; never treat a silent worker as complete. |
| `codex/skills/ywc-sequential-executor/SKILL.md:191-195` | The executor owns a three-call advisor budget and names its remaining advisor conditions. | Add shared 300-second monitoring while retaining the existing budget and each condition's fallback owner. |
| `codex/skills/ywc-sequential-executor/references/advisor-escalation.md:16-18,54-60` | Advisor use is capped and payloads are bounded; the parent executor retains implementation. | Reference monitoring only for successful advisor spawns; do not add background implementation or a second budget. |
| `codex/skills/ywc-impl-review/SKILL.md:168-192` | Dispatches five parallel review lanes, expects findings/candidates, and may route to read-only custom agents. | Define an inline-only, bounded Phase 1 payload and monitor every successfully dispatched lane before Phase 2/aggregation. |
| `codex/skills/references/subagent-status-actions.md:14-41` | Generic fan-out payloads expect artifact paths and forbid full inline review findings. | Add a narrow read-only Phase 1 exception, bounded inline fields, canonical-target validation, and preserve the generic rule elsewhere. |
| `codex/agents/ywc-architect.toml:17-23,40-51` | A custom agent is standalone/read-only and returns its own Status-shaped verdict. | Leave every agent TOML unchanged; canonical target and roster correlation belong to the caller, not the agent definition. |
| `scripts/sync-codex-plugin.sh:47-68` | Copies source `codex/skills` to the generated marketplace directory. | Run only after validated source edits; do not hand-edit the mirror. |

## Acceptance Criteria

- [ ] **AC1 — canonical worker identity:** When a parallel worker spawn returns a canonical task name, the monitor records the source-task-to-returned-target mapping and uses the returned target for collaboration calls; an absent/unparseable returned target stays outside the active roster and enters existing dispatch-failure handling.
- [ ] **AC2 — event-first full-roster reconciliation:** When `wait_agent` wakes, times out, or user steering resumes the parent, the monitor processes attributable terminal payloads, reconciles the full outstanding roster with `list_agents`, routes evidenced terminal statuses, and continues while any target lacks terminal evidence. A missing roster entry alone is never `DONE`.
- [ ] **AC3 — bounded silent-worker handling:** When an implementation worker has no attributable terminal payload after 600 seconds, one status request, one next-heartbeat interrupt, and one final ≤60-second reconciliation occur. Only proven-quiescent workers transition once to preserved failure; possibly-live workers forbid cleanup, next-wave dispatch, Completion Report, and `DONE`.
- [ ] **AC4 — sequential advisor fallback:** When a successfully spawned advisor has no terminal payload after the 300-second bounded sequence, it consumes one existing advisor slot and follows the named condition's existing evidence-based fallback; it is not auto-redispatched and does not alter task-state/worktree lifecycle.
- [ ] **AC5 — honest degraded review:** When a Phase 1 reviewer is quiescent but lacks terminal evidence, the final review lists lane/target, elapsed time, roster state, and raw-evidence category and returns `DONE_WITH_CONCERNS`; when it may still be live, it returns only the minimal monitoring-blocked output with `BLOCKED`, skipping Phase 2 and normal aggregation.
- [ ] **AC6 — read-only reviewer payload:** A successful Phase 1 generic or named reviewer returns only canonical target, Status, one-line Summary, 0–5 bounded confirmed findings, and 0–2 bounded advisor candidates inline; malformed, status-less, ambiguous, or non-attributable output remains non-terminal under the shared monitor.
- [ ] **AC7 — distribution and regression checks:** Source skill validations and affected eval JSON checks pass, then `plugins/ywc-agent-toolkit/skills/` matches the generated source without manual mirror edits.

## Functional Requirements

### FR-1: Shared monitoring contract

Create `codex/skills/references/subagent-async-monitoring.md` as the sole authority for label normalization, successful-dispatch identity capture, three-source reconciliation, ≤60-second heartbeats, 600-second implementation/review-worker escalation, 300-second advisor escalation, API-failure quiescence, and the scenario matrix. It cites but does not duplicate terminal status routing from `subagent-status-actions.md`.

### FR-2: Parallel executor monitor gate

Insert a mechanical post-dispatch gate in `ywc-parallel-executor` that cites FR-1 rather than restating its algorithm. It must retain source task names for state/worktree/report operations, use returned canonical targets for collaboration operations, and route exhausted silent workers through existing preserved-failure handling only after quiescence evidence.

### FR-3: Sequential advisor monitoring

Add a reference and an owner-specific unavailable fallback table to `ywc-sequential-executor`. Cover spec conflict, ambiguous verification failure, borderline stop condition, and Pattern C plan review; retain all current advisor budgets, delivery ownership, and stop rules.

### FR-4: Phase 1 review payload and monitoring precedence

Extend the shared status-actions reference with a Phase 1 read-only inline exception. In `ywc-impl-review`, specify generic fallback selection, prohibit Phase 1 file writes, add a monitor gate after dispatch, and apply `possibly-live → BLOCKED` before `quiescent but unavailable → DONE_WITH_CONCERNS` before ordinary aggregation.

### FR-5: Contract evaluations and generated package

Add eval scenarios for worker silent stall, terminal event during escalation, failed/unparseable spawn, advisor unavailable fallback, reviewer unavailable, reviewer possibly live, and malformed reviewer output. Sync the package after source/eval validation.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Reliability | No absent notification, timeout, or `list_agents` omission may become a completion result without attributable terminal evidence. |
| Safety | No cleanup, next wave, normal review report, or Completion Report may run while a worker/reviewer may still write. |
| Boundedness | Heartbeats are ≤60 seconds; every target receives at most one request and one interrupt; no automatic redispatch is introduced. |
| Compatibility | Existing status semantics, advisor budgets, task-state authority, agent TOML roles, and generated-package workflow remain intact. |

## Data Model

N/A — no persisted schema. The active in-memory monitor mapping is `source task name -> returned canonical task_name`; it is intentionally not resume state.

## API Contract

N/A — no external API. The collaboration API calls remain existing `spawn_agent`, `list_agents`, `wait_agent`, `send_message`, and `interrupt_agent` operations.

## Edge Cases

- A worker finishes during an escalation: its attributable, parseable payload wins; do not mark preserved failure.
- Spawn succeeds but returns no usable canonical target: do not invent identity from an agent ID or requested label.
- Monitoring API failure: process delivered events, interrupt known live targets once, retain raw evidence, and block if quiescence cannot be proved.
- Late terminal evidence after preserved failure: retain it as recovery evidence; do not silently reverse source-task state.
- A read-only review lane is unavailable: it does not touch executor state helpers, worktrees, cleanup, or `preserved_failed`.
- All review workers answer cleanly: existing Phase 2 selection, confidence gate, and report flow remain unchanged.

## Dependencies

- Existing Codex collaboration APIs and their current semantics.
- Existing `subagent-status-actions.md`, executor state/worktree handling, and review report/eval infrastructure.

## Open Questions

N/A — none identified. PR #230's final Codex reference fixes the adopted values at 600 seconds for implementation/review workers and 300 seconds for sequential advisors; the current platform constraint already caps each heartbeat at 60 seconds.

## Implementation Plan

1. Add the shared async-monitoring contract and phase-specific scenario matrix; cross-link it to the existing shared status-actions authority.
2. Update `ywc-parallel-executor` with the post-dispatch monitoring gate, canonical target/source identity split, silent-stall route, and eval coverage.
3. Update `ywc-sequential-executor` with the successful-advisor monitor reference and condition-specific unavailable fallback; add matching eval coverage without changing its budget.
4. Update `subagent-status-actions.md` and `ywc-impl-review` with the read-only inline output exception, monitor precedence, degraded/blocked report schemas, and eval coverage.
5. Run targeted JSON/contract checks, then `bash scripts/sync-codex-plugin.sh` and `bash scripts/validate.sh`; inspect the generated diff to confirm only expected mirror files changed.

## Verification

```bash
node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-impl-review/evals/evals.json", "utf8"))'
bash scripts/run-codex-skill-contract-evals.sh
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
git diff --check
git diff -- codex/skills plugins/ywc-agent-toolkit/skills codex/agents
```

## Risks and Rollback

- **Risk:** Monitoring prose diverges from existing status routing or duplicates lifecycle authority. **Mitigation:** the shared reference owns only identity/liveness/quiescence and cites `subagent-status-actions.md` for terminal-status interpretation.
- **Risk:** A review-worker exception accidentally permits file writes. **Mitigation:** make the exception explicitly inline-only/read-only and leave all agent TOMLs unchanged.
- **Risk:** A worker that may still be live is cleaned up. **Mitigation:** treat missing evidence as non-terminal and block cleanup/next-wave/report paths until quiescence.
- **Rollback:** Revert the source-skill and eval commits together, then re-run `bash scripts/sync-codex-plugin.sh` so the generated marketplace mirror returns to the prior source state.

## References

- [develop-with-llm PR #229](https://github.com/yongwoon/develop-with-llm/pull/229)
- [develop-with-llm PR #230](https://github.com/yongwoon/develop-with-llm/pull/230)
- `codex/skills/ywc-parallel-executor/SKILL.md:242-276`
- `codex/skills/ywc-sequential-executor/SKILL.md:191-195`
- `codex/skills/ywc-impl-review/SKILL.md:168-240`

## Amendment Log

### Iteration 1 — 2026-09-09

Driven by: `ywc-spec-ready` iteration 1 validation.

Signatures: `completeness:missing-outcome-oracle`

| Section edited | What changed | Why |
|---|---|---|
| Outcome Oracle | Added explicit Target, Quality threshold, Evidence required, and Stop condition. | Replaced the implicit completion claim spread across Acceptance Criteria and Verification; the readiness contract requires a compact, testable oracle. |

### Iteration 2 — 2026-09-09

Driven by: `ywc-spec-ready` iteration 2 validation.

Signatures: `consistency:outcome-oracle-handoff-timing`

| Section edited | What changed | Why |
|---|---|---|
| Outcome Oracle | Separated the pre-implementation task-generation handoff from post-implementation verification. | Replaced an impossible readiness condition that required implementation commands to pass before task generation. |
