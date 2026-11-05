# Code Compatibility — Iteration 1

Status: DONE
Critical: 0, Warning: 2, Suggestion: 0
Outcome Oracle: complete; Blind Spot action: proceed after correcting the stated current routing assumption.

## Warning CC-1 — FR-1 depends on nonexistent runtime routing

- Spec: `docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:97` and Module Boundaries task metadata row at :83.
- Evidence: `codex/skills/references/subagent-model-routing.md` does not exist. Searching `codex/skills/ywc-parallel-executor/` and `ywc-sequential-executor/` for economy/standard/advanced/model-policy finds no tier routing contract; their current implementation uses inherited execution and bounded advisors (`ywc-sequential-executor/SKILL.md:193`). The module table describes the consumer as existing executor runtime routing, which current source cannot supply.
- Consequence: task generation can emit the new hints, but an implementer would need to invent an unstated routing subsystem or leave a dangling canonical reference.
- Improvement: own a new bounded tier-definition reference for task metadata, make the hint advisory and runtime-neutral under existing executor model behavior, and explicitly defer task-aware model routing. Alternatively specify the entire consumer migration as separately scoped work; do not call it existing.

## Warning CC-2 — interactive agentic-owned planner call needs named migration

- Spec: `docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:162`.
- Evidence: `codex/skills/ywc-agentic/SKILL.md:116-118` forwards --non-interactive only when received and invokes `ywc-plan [--non-interactive] --artifact-profile agentic`. Its readiness phase at :143 onward owns `ywc-spec-ready`; task phase at :163 consumes its verified Result. `ywc-plan/SKILL.md` already owns an agentic Result/Artifact profile. Auth is named in FR-10 while this interactive orchestrator is left to later discovery.
- Consequence: simply replacing upstream plan handoff can double-run readiness and/or replace the current profile's machine-readable Result contract. This is a concrete cross-skill integration boundary, not general caller documentation.
- Improvement: include `codex/skills/ywc-agentic/SKILL.md` and its contract evals as explicit FR-10 owned files; add --no-converge to its planner acquisition and preserve the existing agentic profile Result/Artifact schema and caller-owned readiness. Cover interactive and non-interactive invocation counts.

## Precedent Site Coverage

| Precedent site | Spec coverage |
|---|---|
| `codex/skills/ywc-debug-rootcause/SKILL.md:85` analyst caller | Replicated by FR-2 |
| `codex/agents/ywc-root-cause-analyst.toml:13,24,39` analyst envelope/hypotheses | Replicated by FR-2, existing constraints |
| `codex/skills/ywc-confidence-gate/SKILL.md` root-cause routing | Replicated by FR-2 named owner |
| `codex/skills/ywc-incident-postmortem/SKILL.md` incident analysis | Replicated by FR-2 named owner |
| `codex/skills/ywc-auth-implement/SKILL.md` planner/readiness ownership | Replicated by FR-10 |
| `codex/skills/ywc-agentic/SKILL.md:116-118,143,163` profile acquisition/readiness consumption | Broadly included by “other callers”, but exact contract migration missing; CC-2 |
| `codex/skills/ywc-spec-ready/SKILL.md:62-63,83,103` noninteractive acquisition/replan | Deferred-with-reason: already excluded by FR-10 noninteractive/Re-plan guards, preserve profile |
| `codex/skills/ywc-worktrees/SKILL.md:96-138` audit/prune/keep-branch | Replicated by FR-9 preservation |
| `codex/skills/ywc-task-generator/references/output-and-validation.md:1-24` persisted preview/coverage contract | Replicated by FR-1 preservation in Existing Constraints Touched |
| `codex/skills/ywc-plan/SKILL.md:343` current handoff and agentic Result profile | Replicated by FR-10, profile clarification required CC-2 |

No advisor candidates: both findings are deterministic current-source gaps. No implementation or spec edits performed.

Graft tokens saved: 12,031 (one call).
